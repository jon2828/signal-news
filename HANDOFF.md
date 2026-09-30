# HANDOFF — Unspent Thoughts (formerly "Signal"), an autonomous AI + Bitcoin news site

**Owner:** Jon ("Jarvis" is the assistant's name in his chats).
**Purpose:** a mostly autonomous news site covering AI and Bitcoin. Only important stories publish (no quota pressure); posts under 1,000 words, human-sounding, fact-checked. Free tools only, with paid optionality documented.
**Public URL:** pending (Cloudflare Pages, step 3 below).
**Source repository:** pending — to be created as `signal-news` on Jon's existing GitHub account.

## Known facts and provenance

Verified with real runs (not assumed) unless marked otherwise:

- Build at `~/ai-bitcoin-news`, commits `15401c5` and `28feed4` on `main`. Provenance: git history on this machine.
- Pipeline works end to end: gather (1,235 items, 11 feeds) → dedupe (1,071 candidates) → triage (kimi-k3, 60 scored, 50 rejections logged) → write (kimi-k3, 373-word post, lint-clean) → fact-check (gpt-oss-120b on Groq, independent model family, verdict publish) → static build. Provenance: `state/decisions.jsonl` audit trail.
- Kill switch tested: `PIPELINE_ENABLED=false` makes every script exit cleanly without posting. Provenance: live test 2026-09-29.
- Keys live locally in `~/.hermes/.env`: `GROQ_API_KEY` (verified live), `HERMES_CUSTOM_INTEGRATE_API_NVIDIA_COM_API_KEY` (= NVIDIA trial key, verified live), `OPENROUTER_API_KEY`. Provenance: environment inspection.
- Not yet audited: the GitHub Actions workflow has never run on Actions (no repo existed); feed freshness re-check is due when the first scheduled run happens.

## Change and approval workflow

- **Human changes** (post edits, prompt tweaks, config): feature branch → pull request → **Jon performs the final merge.** No auto-merge, no direct pushes to `main` by humans.
- **The pipeline bot** commits directly to `main` by design — its commits ARE the public audit trail (scores, rejections, decisions), and Pages deploys from `main`. This exception is part of the approved blueprint; a receiving agent must not "fix" it without asking Jon. If Jon wants it hardened later: fine-grained PAT scoped to the repo, or protect `main` with the bot's identity exempted.

## Access boundaries

- Secrets never appear in chat, handoff docs, or repo files. Jon adds them himself via GitHub's UI (Settings → Secrets and variables → Actions) or `gh secret set NAME` (interactive, hidden input).
- Knowledge transfer (this document, RESUME.md, the skill) is separate from access transfer. A receiving bot gets no chat history, no memories, and no credentials — it verifies its own auth where it runs.
- Local keys stay in `~/.hermes/.env`; repo secrets are added one by one by Jon.

## Missing information (a receiving agent must request, not guess)

1. The repository URL (after Jon creates it).
2. Whether Jon wants the `pages.dev` subdomain or a custom domain from day one.
3. Whether the pipeline bot's direct-to-main commits are re-authorized for the new repo (recommended: yes, same design).

## First actions for a receiving agent

1. Read RESUME.md in the repo — the full build record, every failure mode and fix, and the model map (verified live 2026-09-29).
2. Verify your own access: `gh auth status` where you run.
3. Inspect `config/pipeline.json` (kill switch, provider chain, job_chain, models, paid_options) and `.github/workflows/pipeline.yml` before any push — pushing branches or opening PRs can trigger deployments.
4. Propose a focused first task (recommended: watch the first scheduled run and verify the audit trail grows), then wait for Jon's go.

## Go-live steps (Jon executes, ~15 minutes)

1. `gh auth login` (device-code flow; uses whichever account is logged into the browser).
2. `cd ~/ai-bitcoin-news && gh repo create signal-news --public --source=. --push`
3. Repo → Settings → Secrets and variables → Actions:
   - Secrets: `NVIDIA_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY` (optional)
   - Variables: `PIPELINE_ENABLED` = `true`
4. dash.cloudflare.com → Workers & Pages → Create → Pages → connect the repo. Build command `python3 scripts/build.py`, output directory `site/dist`.
5. Watch the first run: repo → Actions tab. Kill switch any time: set `PIPELINE_ENABLED=false`, or Actions → pipeline → Disable workflow.
