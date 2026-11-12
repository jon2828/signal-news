---
title: Claude Fable 5.2 tops the Artificial Analysis index, at a price
date: 2026-11-09
topic: ai
story: claude-fable-5-2
score: 8
candidate_id: 255b56db4a4a44d0
sources: ["https://artificialanalysis.ai/models/claude-fable-5-2", "https://www.anthropic.com/claude-fable-and-mythos-5-2"]
triage_reason: "Frontier lab model release with a top benchmark score, sourced to Anthropic and corroborated by multiple HN threads."
---

Anthropic announced the release of Claude Fable 5.2 and Claude Mythos 5.2, and the new model scores **65** on the Artificial Analysis Intelligence Index - well above the median of **40** for comparable models.

That is the headline. The rest of the numbers are more nuanced.

## The independent numbers

Artificial Analysis reports that Fable 5.2 is far above average on intelligence, but its cost profile is steep. Input tokens cost **$8 per million** (median **$2**), and output tokens cost **$40 per million** (median **$10**). Running the model through the index averages **$26.54 per task**.

Speed is a weakness. A single Intelligence Index task takes **48 minutes**, compared with a median of **12.6 minutes** for similar models. The evaluation generated **275 million tokens**, roughly four times the median of **72.8 million**. The model's willingness to generate many tokens can boost answer quality, but it also drives up cost - especially at **$40 per million output tokens**.

## What Anthropic says

Anthropic's announcement frames the release around frontier technical work. The company says that during prerelease testing the models helped engineers complete "otherwise‑infeasible software migrations," design three working electronic devices from scratch, solve two open problems in black‑hole physics, and formalize the proof of Fermat's Last Theorem in 30 hours. Those are Anthropic's claims, not independent validations.

The benchmark table is more concrete. On **FrontierCode 2.0**, Fable 5.2 scored **49.1 %** at its highest‑effort setting, ahead of Opus 5.5 (**45.5 %**), GPT‑6 Astra (**42.8 %**), and Gemini 4 Carbon (**41.1 %**, run at medium effort). Fable 5.2 also posted **69.9 %** on **FrontierSWE v2**, **74.2 %** on **Humanity's Last Exam** with tools, and **41.3 %** on the **Remote Labor Index**, where Opus 5.5 manages **21.3 %**.

Anthropic adds that in early testing Fable 5.2 at **High effort** roughly matched Opus 5.5 at **Max effort** for about **half the cost per task**, highlighting the price‑performance trade‑off.

One internal metric stands out. Anthropic says **over 90 %** of the changes merged into its core codebase are now written by Claude (with human guidance). A team of agents running an earlier Fable 5.2 build migrated a critical production service from Python to Rust, making the service **about 26 times faster**.

## Fable, Mythos, and the safety framing

Fable and Mythos share the same underlying model. Fable includes cybersecurity and biology safeguards and is publicly available. Mythos, without those constraints, is accessible only through Anthropic's Life Sciences and Cyber Verification Programs for approved research.

On safety, Anthropic reports new evaluations targeting behaviors like sandbox escapes, states that high‑stakes misalignment risks **"remain low,"** and claims to have added its strongest‑ever protections against distillation attacks.

A fast‑mode option can speed token generation by up to **2.5×** for **$16 per million input tokens** and **$80 per million output tokens** - essentially double the standard price to make a slow model faster.

## The tension nobody resolved

Anthropic notes that the new models generate output up to **30 % faster** than the 5.1 versions at a lower price. Artificial Analysis, however, finds Fable 5.2 expensive and slow relative to the broader field. Both statements can be true: it is faster and cheaper than its predecessor, yet still slower and pricier than many peers. The high index score is real, as is the cost.

## Sources

- [Claude Fable 5.2 on Artificial Analysis](https://artificialanalysis.ai/models/claude-fable-5-2)
- [Anthropic's Fable 5.2 and Mythos 5.2 announcement](https://www.anthropic.com/claude-fable-and-mythos-5-2)
