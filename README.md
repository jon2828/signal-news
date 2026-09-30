# Unspent Thoughts

An autonomous news site for AI and Bitcoin. A GitHub Actions workflow runs twice a day: it pulls feeds from about a dozen sources, dedupes them into story candidates, scores each candidate for importance with a language model, writes a post for the ones that clear the bar, fact-checks the post with a second pass against the same sources, and builds the static site. No human touches a post before it publishes.

Right now the writer and the fact-checker are the same underlying model with different instructions (the fast model that survives the free provider's timeouts); a second model family for the check is a one-line config change (`config/pipeline.json` → `models.edit`) once a free provider handles the job.

The rules: nothing over 1,000 words, every claim links to its source, stories are linked and summarized but never republished, and the site is allowed to post nothing on a quiet day. Scores, rejections, and every dropped draft are logged in `state/` — the repo history is the audit trail.

## Run it

```bash
export GROQ_API_KEY=...        # or OPENROUTER_API_KEY, tried in that order
python3 scripts/gather.py      # feeds -> state/pending.json
python3 scripts/dedupe.py      # cluster -> state/candidates.json
python3 scripts/triage.py      # LLM score -> state/approved.json
python3 scripts/write.py       # LLM -> state/drafts/*.md
python3 scripts/edit.py        # fact-check -> posts/*.md
python3 scripts/build.py       # posts -> site/dist/
```

The GitHub Actions workflow (`.github/workflows/pipeline.yml`) runs all six steps on a schedule (06:00 and 18:00 UTC) and pushes the result, which deploys the site.

## Kill switch

Two ways, both instant:

1. Repo variable `PIPELINE_ENABLED=false` (Settings → Secrets and variables → Actions → Variables). The workflow passes it to every script, which check it first and exit without posting.
2. Edit `pipeline_enabled` in `config/pipeline.json` and push.

## Layout

- `config/feeds.json` — sources, tested live; dead feeds disabled with a note
- `config/pipeline.json` — thresholds, caps, models, provider chain, kill switch
- `prompts/` — triage, write, and edit prompts
- `voice/bible.md` — the site's fixed voice, enforced by `scripts/lint.py`
- `scripts/` — the six pipeline steps plus the anti-AI lint checker
- `posts/` — published posts (the site)
- `state/` — seen items, candidates, scores, decisions, declined drafts
- `site/pages/disclosure.md` — how the site works, rendered at /disclosure

## Hosting

Cloudflare Pages: connect the repo, build command `python3 scripts/build.py`, output directory `site/dist`. Free tier covers this easily (unlimited bandwidth, 500 builds/month against ~90 used). Set `site_base_url` in `config/pipeline.json` once the domain is live, so post links and the RSS feed use absolute URLs.

## Paid models (the optionality)

`config/pipeline.json` → `paid_options` holds per-provider model presets and the upgrade ladder, inert until you add a key or flip a slug into the live `models` section. Ladder, best value first: Groq pay-per-token (~$1/month for the whole pipeline), Cloudflare Workers Paid ($5/month flat, unlocks glm-5.3 / kimi-k2.7 / deepseek-v4 with 10K free neurons/day still included), Cloudflare Pro (not needed; bandwidth is already free).

## Resume

Everything that happened, every failure mode and fix, and the three steps to go fully live are in [RESUME.md](RESUME.md). Start there when picking this project back up.
