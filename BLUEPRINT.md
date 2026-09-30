# BLUEPRINT (historical — written when the project was called "Signal")

# Unspent Thoughts: an autonomous AI + Bitcoin news site

## The verdict

Yes, this can be done, mostly free and mostly autonomous. The stack: a Git repo as the database, GitHub Actions cron as the scheduler, free LLM APIs for selection and writing, Cloudflare Pages for hosting. No servers, nothing to maintain, $0/month until traffic makes hosting matter (it won't at this size).

One correction to the premise: "no quota, only the important stuff" is still a quota. A relevance bar is a quota, just a good one. The pipeline enforces it: a candidate must clear dedupe, sourcing checks, and an importance threshold before anything gets written. On a slow news day the site posts nothing, and that is the feature working, not failing.

## What's verified (research done, not guessed)

Free-tier numbers, checked against vendor docs:

| Resource | Free tier | Fit for this project |
|---|---|---|
| Cloudflare Pages | Unlimited bandwidth and static requests, 500 builds/month, 100 custom domains per project | 2-3 posts/day is ~90 builds/month. Effectively unlimited. |
| Cloudflare Workers AI | 10,000 neurons/day; since July 2026 some resource-heavy models return 403 on the Free plan | Optional. Groq covers the LLM work. |
| Groq | 30 req/min; per-model daily ceilings and token caps: llama-3.1-8b-instant 500K tokens/day, llama-3.3-70b 100K/day, gpt-oss-120b 200K/day | Plenty. A full post is ~1,500-2,500 output tokens. |
| Gemini API | Free input and output tokens on Flash models, but free-tier rate limits have been cut with no notice more than once in 2026 | Bonus only, never a dependency. |
| GitHub Actions | Unlimited minutes on a public repo, 2,000 min/month on private | Our jobs use ~20-30 min/day. |

Sources: OpenAI's news RSS and TLDR AI are confirmed good feeds. Bitcoin Optech (weekly newsletters at bitcoinops.org), Bitcoin Core release notes, CoinDesk, Cointelegraph, The Block, Bitcoin Magazine, HN (hnrss.org), VentureBeat AI, Anthropic, and the Google AI blog are strong candidates. The live test of all 14 feed URLs is the first execution step. Your desktop app asked for an update before it can answer tool-approval prompts, so I could not run that test from here yet; it does not change the plan.

## The two hard truths

1. A Git repo is the database. Posts are markdown files with YAML frontmatter, JSON state files track what has been seen. It survives forever, the diff history is a full audit log of every decision the system made, and Pages deploys on push. SQLite in Durable Objects is the upgrade path if this ever outgrows files, which it won't for years.

2. "As human-sounding as possible" needs one fixed voice, not model randomness. The way to get it: a voice bible in the repo (the site's tics written down: short sentences, occasional first person, no "delve", no "landscape", no forced groups of three), the same model and temperature on every run, and a lint pass that rejects AI tells before publishing. The 34 humanizer patterns become the site's lint checklist. A draft containing "pivotal moment" or "underscoring the significance" gets rewritten or dropped automatically.

## Architecture

```
                     ┌─────────────────────────────────────────────┐
                     │           GitHub repo (the database)        │
                     │  posts/*.md   state/*.json   voice/bible.md │
                     └───────▲─────────────────────────▲───────────┘
                             │ commit + push           │ read state
 ┌──────────────┐            │                         │
 │ RSS sources  │───fetch──► JOB 1 gather                │
 │ (14 feeds)   │            │                         │
 └──────────────┘            ▼                         │
                      JOB 2 dedupe (no LLM)            │
                      URL-hash + title clustering      │
                             │ candidates.json         │
                             ▼                         │
                      JOB 3 triage (LLM)               │
                      llama-3.3-70b, score 1-10        │
                      keep >= 7, max 2 per run         │
                             │ approved.json           │
                             ▼                         │
                      JOB 4 write (LLM)                │
                      gpt-oss-120b, voice bible        │
                      under 1,000 words                │
                             │ drafts/*.md             │
                             ▼                         │
                      JOB 5 edit (LLM + code)          │
                      fact-check pass, anti-AI lint    │
                      drop with reason if it fails     │
                             │ posts/*.md              │
                             ▼                         │
                      JOB 6 publish                    │
                      build index + RSS, push,         │
                      Cloudflare Pages deploys         │
```

All six jobs are steps in one GitHub Actions workflow. Cron: 06:00 and 18:00 UTC. Each run ends with a git commit, so every selection decision is in the public log.

## The pipeline

**Job 1, gather** (cron, 2x/day): pull every feed, normalize to {id: url-hash, title, source, published, summary}, save state/seen.json. New items only.

**Job 2, dedupe** (no LLM): cluster by URL hash, then by title similarity (n-gram overlap in Python). One story covered by five outlets becomes one candidate with five sources. Five sources is a relevance signal, not spam.

**Job 3, triage** (LLM, the decision): send candidates in batches to Groq's llama-3.3-70b with a scorer prompt: "Rate 1-10 for importance to someone who follows AI and Bitcoin. 10 = market-moving or frontier-shifting. 7+ = publishable. Output JSON only." Keep 7+, cap at 2 posts per run. Write the score and reasoning to state so the log shows why something ran or didn't.

**Job 4, write** (LLM): one post per approved candidate. Prompt = voice bible + source article text + hard rules: under 1,000 words, link every claim to its source, paraphrase with attribution (never republish), straight quotes, no lint-list phrases. Output markdown with frontmatter (title, date, sources, score, word count).

**Job 5, edit** (LLM + code, the safety net): second pass with a different model than the writer. Check every factual claim against the source text, word count under 1,000, lint hits below threshold, no invented numbers. A post that fails gets dropped with the reason logged. This is the "as much research and check as possible" part, and it is the difference between a news site and slop.

**Job 6, publish**: regenerate index.html and feed.xml with plain Python (no framework), commit, push. Cloudflare Pages builds and deploys automatically. The site is static, so the free tier is effectively unlimited.

## Repo layout

```
ai-bitcoin-news/
├── .github/workflows/pipeline.yml    # cron + all six jobs
├── scripts/
│   ├── gather.py         # feeds -> state/seen.json
│   ├── dedupe.py         # cluster -> candidates.json
│   ├── triage.py         # LLM score -> approved.json
│   ├── write.py          # LLM -> drafts/*.md
│   ├── edit.py           # fact-check + lint -> posts/*.md
│   ├── build.py          # posts -> index.html, feed.xml
│   └── lint.py           # anti-AI tell checker (34 patterns)
├── voice/bible.md        # the site's fixed voice
├── config/feeds.json     # source list + per-source weight
├── config/pipeline.json  # thresholds, caps, model ids
├── posts/*.md            # the published site
├── state/*.json          # seen items, scores, decisions
├── site/                 # templates for index.html
└── README.md
```

## Free-tier budget (monthly, at 2-3 posts/day)

| Resource | Limit | Our use | Cost |
|---|---|---|---|
| GitHub Actions (public repo) | unlimited | ~600-900 min | $0 |
| Groq llama-3.3-70b | 100K tokens/day | ~10-20K/day | $0 |
| Groq llama-3.1-8b | 500K tokens/day | triage batches | $0 |
| Cloudflare Pages | 500 builds, unlimited bandwidth | ~90 builds | $0 |
| Domain | optional | ~$10/year | $0-10 |

Worst case, a free tier vanishes tomorrow: swap the LLM provider in config/pipeline.json (one line), swap Pages for GitHub Pages (one setting). The pipeline is provider-agnostic on purpose.

## Timeline

- Day 1: scaffold the repo, test all 14 feeds live, write the voice bible and lint checker, run the pipeline once end to end, show the first 2 posts.
- Day 2-3: tune the triage bar together (look at scores, adjust the threshold), set up Cloudflare Pages and the domain.
- Week 2+: it runs itself. Check in whenever; the git log is the audit trail.

## What you're missing

- A disclosure page. Readers deserve to know how it's made, and search engines are friendlier to sites that say it. One paragraph: "Every post is selected, written, and checked by software from public sources, with links. Scores and reasoning are in the public repo."
- A kill switch. A repo secret (PIPELINE_ENABLED=false) or disabling the workflow in GitHub settings. One click, no code.
- Review firehose risk: with 2 posts/day you can read everything in 5 minutes. With 10 you stop reading. Cap at 2 for the first month.
- Legal: link and summarize, never republish full articles. The writer prompt enforces this.
- An "about the score" page if scores appear on posts. It is the most interesting part of the site, in my opinion: readers can see why a story made the cut.

## Failure modes and self-healing

- Feed dies: gather.py logs it, the pipeline runs on what's left, and an auto-filed GitHub issue tells you which feed to replace.
- LLM rate limit hit: retry with backoff down the provider chain in config, tried in order.
- Bad post published anyway: git revert one commit. The state files mean the same story won't come back.
- Cloudflare build fails: Pages keeps the last good deploy live. The site never goes down.

## First run (what I execute once tool approvals work)

1. Test all 14 feed URLs live, keep the working ones.
2. Scaffold the repo: scripts, voice bible, lint, workflow.
3. Run the pipeline once end to end.
4. Show you 2 posts and the triage log.
5. Set up Cloudflare Pages once you've created the account.
