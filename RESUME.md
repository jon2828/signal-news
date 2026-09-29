# RESUME — how to pick this project back up

State as of 2026-09-29: the pipeline is built, verified end to end, and 2 posts are live. First commit: `15401c5`. This file records everything that happened and every step needed to resume. If anything is "stuck", start here.

## Current state (all verified with real runs)

| Piece | Status |
|---|---|
| Repo `/home/jarvis/ai-bitcoin-news` | 7 scripts + prompts + config + voice bible, committed on `main` |
| Feed gather | Works: 1,235 items from 11 feeds (venturebeat 429s on rate limit — retry later, it's real) |
| Dedupe | Works: 1,071 candidates, 160 multi-source clusters |
| Triage (kimi-k3, NVIDIA) | Works: 60 scored, 1 approved, 50 rejections logged with reasons |
| Writer (kimi-k3, NVIDIA) | Works: 373-word THORChain post, 0 lint hits |
| Fact-checker (gpt-oss-120b, Groq, tries first) | Works: verdict publish in 1s, independent model family |
| Build | Works: index.html, disclosure.html, feed.xml in `site/dist/` |
| Kill switch `PIPELINE_ENABLED=false` | Tested: every script exits cleanly without posting |
| GitHub Actions workflow | Written (`.github/workflows/pipeline.yml`), needs a GitHub repo to run on |
| Cloudflare Pages | Not connected yet — see step 3 below |

## The three steps to go fully live

1. **Push to GitHub.** `gh auth login` (the CLI is installed but not authed), then:
   ```bash
   cd ~/ai-bitcoin-news
   gh repo create signal-news --public --source=. --push
   ```
   Public = free unlimited Actions minutes, and the audit-trail promise (scores, rejections, decisions in the repo history) is real.
2. **Add repo secrets.** In the repo: Settings → Secrets and variables → Actions.
   - `NVIDIA_API_KEY` — from https://build.nvidia.com/settings (the trial key; locally it lives in `~/.hermes/.env` as `HERMES_CUSTOM_INTEGRATE_API_NVIDIA_COM_API_KEY`, use one of the two)
   - `GROQ_API_KEY` — from https://console.groq.com/keys
   - `OPENROUTER_API_KEY` — optional third fallback
   Values never need to appear in chat; the vault tools or the GitHub UI handle them.
3. **Cloudflare Pages.** dash.cloudflare.com → Workers & Pages → Create → Pages → connect the GitHub repo:
   - Build command: `python3 scripts/build.py`
   - Output directory: `site/dist`
   - Free tier covers this (~90 builds/month against 500). Set `site_base_url` in `config/pipeline.json` once the domain is live.

After step 2, the workflow runs on schedule (06:00 and 18:00 UTC) and pushes automatically. Kill switch any time: repo variable `PIPELINE_ENABLED=false`.

## How to run manually

```bash
cd ~/ai-bitcoin-news
set -a && . ~/.hermes/.env; set +a   # loads GROQ_API_KEY etc. into the environment
export NVIDIA_API_KEY="${HERMES_CUSTOM_INTEGRATE_API_NVIDIA_COM_API_KEY}"
python3 scripts/gather.py && python3 scripts/dedupe.py && python3 scripts/triage.py \
  && python3 scripts/write.py && python3 scripts/edit.py && python3 scripts/build.py
```

## Model map (verified live 2026-09-29)

| Job | Provider tried | Model | Notes |
|---|---|---|---|
| Fact-check (edit) | Groq | `openai/gpt-oss-120b` | 1s, clean JSON, independent family — tries FIRST (job_chain) |
| edit fallback | NVIDIA | `moonshotai/kimi-k3` | 6s, the only fast model on NVIDIA's endpoint today |
| Write | NVIDIA | `moonshotai/kimi-k3` | 373-word post, voice-clean |
| write fallback | Groq | `openai/gpt-oss-120b` | strong instruction following |
| Triage | NVIDIA | `moonshotai/kimi-k3` | scored 60 in batches of 20 |
| triage fallback | Groq | `qwen/qwen3.8-27b` | — |
| all fallbacks | OpenRouter | free tier, congested (429s) | bonus only, never a dependency |

Groq's catalog **changed under us** mid-build (llama-3.x chat models removed; gpt-oss + qwen remain). NVIDIA's catalog lists models its trial accounts can't actually run (llama-3.1-nemotron-*-instruct 404'd). Lesson: **a catalog listing is not availability. Always test a model on the real prompt before wiring it in.**

## Failure modes we hit, and their fixes (all in the code now)

| Symptom | Cause | Fix |
|---|---|---|
| HTTP 403 "error code: 1010" | Cloudflare bot ban on urllib's default UA | browser-style UA on API calls (`_common.chat`) |
| HTTP 404 on a model | stale slug after provider catalog drift | re-query `/models`, update `config/pipeline.json` |
| HTTP 504 on glm-5.3/deepseek/gpt-oss-20b (NVIDIA) | reasoning too slow for synchronous serving | fast models only (kimi-k3), or paid option |
| HTTP 429 | free-tier congestion (OpenRouter, venturebeat feed) | provider fallback chain; retry next run |
| `no choices in response` with HTTP 200 | error payload masked as success | `_common.chat` raises; fallback kicks in |
| empty content from a reasoning model | reasoning burned the token budget | empty-content check; bigger max_tokens |
| garbled JSON on a big prompt (nemotron lightning) | model can't handle 18K-char prompts | triage batches of 20, no-preamble instruction |
| feed ParseError "unclosed token" | per-feed size cap truncating XML mid-tag | cap raised to 2MB |
| article extracts to 0 chars (CoinDesk) | JS-heavy page, blocks non-browser agents | r.jina.ai fallback in `_common.extract_article` |
| writer output has preamble before frontmatter | model rambles before the block | `parse_post` salvages the frontmatter block |

## Paid models (the optionality)

`config/pipeline.json` → `paid_options` holds per-provider model presets and the upgrade ladder. Nothing there is active until you add a key or flip a slug into the live `models` section:

1. **Groq pay-per-token** (~$1/month for the whole pipeline) — removes every rate limit
2. **Cloudflare Workers Paid** ($5/month flat) — unlocks `@cf/zai-org/glm-5.3`, `@cf/moonshotai/kimi-k2.7-code`, `@cf/deepseek-ai/deepseek-v4-pro-0813`, with 10K free neurons/day still included
3. **Cloudflare Pro** ($20/month) — not needed; bandwidth is already free

## File map

- `config/feeds.json` — sources (11 enabled, 3 disabled with notes), weights
- `config/pipeline.json` — kill switch, provider chain, job_chain, models, caps, temperatures, paid_options
- `prompts/triage.md`, `prompts/write.md`, `prompts/edit.md` — the quality bar
- `voice/bible.md` — the fixed voice; `scripts/lint.py` enforces it
- `scripts/gather.py` → `dedupe.py` → `triage.py` → `write.py` → `edit.py` → `build.py` — the pipeline
- `scripts/_common.py` — config, kill switch, provider chains, chat with fallback, article extraction
- `posts/` — 2 live posts; `state/` — seen items, candidates, approved, decisions.jsonl (the audit trail), declined/
- `site/pages/disclosure.md` — how the site works (rendered at /disclosure)
- `.github/workflows/pipeline.yml` — cron + all six jobs + commit step
