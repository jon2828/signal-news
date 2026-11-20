---
title: OpenAI's GPT-6.2 Astra and Sol, with the fine print attached
date: 2026-11-17
topic: ai
story: gpt-6-astra
score: 9
candidate_id: 549a77347d5e1e5f
sources: ["https://openai.com/index/introducing-gpt-6-2-astra-sol", "https://openai.com/index/introducing-gpt-6-2-astra-sol/"]
triage_reason: "Frontier model release from OpenAI, corroborated by two sources, is frontier-shifting."
---

# OpenAI's GPT-6.2 Astra and Sol, with the fine print attached

*Date: 2026‑11‑17*

OpenAI announced two new models in its blog post on **Wednesday, November 17, 2026**: **GPT‑6.2 Astra**, the frontier model for "your hardest projects," and **GPT‑6.2 Sol**, a cheaper, versatile model for everyday work. The [announcement](https://openai.com/index/introducing-gpt-6-2-astra-sol) is long on benchmark wins and cost comparisons, and short on anything measured by an independent party. Both of those things are worth your attention.

## The numbers OpenAI wants you to see

- **Agents' Last Exam** - Astra scores **5.2 points** above GPT‑6 Astra at **less than a third of the cost**, and **5.5 points** ahead of Claude Fable 5.2 at **about 5 % of the cost**.
- **Terminal‑Bench‑Science 0.1** - Astra is **9 percentage points** higher than GPT‑6 Astra.
- **Harvey LAB‑AA v1.1** (legal benchmark) - Astra more than **doubles** Claude Fable 5.2's pass rate at **about one‑sixth the cost**.
- **API pricing** - Input and output token prices are **20 % lower** than GPT‑6 Astra's, with a 60 % discount on cached input: **$8 / M input tokens**, **$0.40 / M cached input**, and **$40 / M output**.
- **Sol** keeps GPT‑6.1 Sol's prices. On **Cognition's FrontierCode 2.0**, Sol is within **0.5 points** of Astra at **roughly one‑fifth the cost** (both at max).
- **LifeVal** - Sol outscores GPT‑6 Astra at **about one‑seventh the cost**.

If those ratios hold up outside OpenAI's own blog, Sol is the more interesting model for most developers. A modest cost advantage can change what people actually build more than a single leaderboard point.

## The fine print

- The **Fable 5.2** comparison carries a footnote: the leaderboard excludes nine tasks that used a fallback model, which narrows the reported gap.
- Several benchmarks are OpenAI‑internal: **GDPval v2** (Astra +6.2 points, 22 % fewer output tokens) and **LifeVal** (released by OpenAI). The numbers are real, but the tests are self‑selected.
- "5 % of the cost" is a per‑task figure derived from token counts and list prices. Real‑world costs also depend on retries, tool calls, and token burn‑rate, which vary by workload.

## What I'd actually take from this

The demo material is genuinely strong. OpenAI had both Astra generations build a valuation workbook for a fictional agricultural‑technology company, forecasting revenue through 2031 and reconciling the three financial statements. On **Artificial Analysis's AA‑AnalystAgent**, which works from real spreadsheets and reports, Astra answered **62.5 %** of questions correctly across **five independent attempts**. That consistency matters more to me than a single leaderboard score.

The direction is clear: OpenAI is pushing cost per task down while nudging quality up, targeting billable professional work such as legal deliverables and valuation models. Whether Astra truly is *"the best model in the world for scientists,"* as OpenAI claims, remains to be validated by independent researchers.

## Sources

- [Introducing GPT‑6.2 Astra and Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-2-astra-sol)
