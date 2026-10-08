---
title: Claude Haiku 5.5 launches at 75% lower cost than Haiku 4.5
date: 2026-10-08
topic: ai
score: 8
candidate_id: 4bb428a07b2a9a89
sources: ["https://www.anthropic.com/claude-haiku-5-5", "https://tldr.tech/ai/2026-10-08"]
triage_reason: "Frontier-lab model release from Anthropic, confirmed by the official page and multiple sources, squarely in the 9-10 band."
---

# Claude Haiku 5.5 launches at 75% lower cost than Haiku 4.5

Anthropic released Claude Haiku 5.5 in early October 2026, and the number that matters is not a benchmark - it's the price. The company says the new small model costs around 75 % less to run than Haiku 4.5, on average.

The sticker prices mostly back that up. Input tokens run **$0.10 per million** for prompts under 100 k tokens, down from **$1.00** on Haiku 4.5. Output is **$0.50 per million**, down from **$5.00**. Cache reads drop to a penny per million. Going over 100 k tokens the price jumps five‑fold, to **$0.50** input and **$2.50** output, though Anthropic notes roughly 90 % of requests to the previous Haiku model stayed under that line. Convenient cutoff - most customers land in the cheap tier anyway.

## The benchmarks are Anthropic's own

On paper, the capability jump is enormous. Haiku 5.5 scores **72.4 %** on the OSWorld 2.1 computer‑use benchmark, up from **15.7 %** for Haiku 4.5. On Terminal‑Bench 4.0 it hits **39.2 %**, up from a flat **0.0 %**, which says as much about the old model as the new one. It also beats OpenAI's GPT‑6 Luna on every benchmark where Anthropic lists a Luna score, including **1620 vs 1437** on the GDPval‑AA knowledge‑work eval.

I would treat all of this as a starting bid, not a final verdict. These are Anthropic's evaluations, run by Anthropic, published in the launch post. A jump from 15.7 % to 72.4 % on computer use in one generation either means the eval got easier or the model genuinely leapt, and third‑party replication will sort out which. The safer takeaway is the one Anthropic itself notes: Sonnet 5.5, at **70.6 %** on Terminal‑Bench, remains the pick for complex agentic coding. Haiku 5.5 is aimed at narrower work like compaction, summarization, or running as a sub‑agent on coding jobs.

One genuinely new thing: Haiku 5.5 is the first Haiku model with an **adjustable effort setting**, so developers can trade intelligence for cost on each request.

## The rest of the announcement is about money too

Alongside the launch, Anthropic cut Sonnet 5.5 cache reads in half, from **$0.20** to **$0.10** per million tokens, which it says makes Sonnet about 20 % cheaper on most agentic work. It is also handing out monthly API credits to subscribers: **$100** for Max 5x users, **$200** for Max 20x, and up to **$500** pooled across Team plans.

Read together, this is a clear price‑cut strategy. Anthropic is lowering prices across its range and paying subscribers to build agents on the Claude Platform - good news if you're already building on Claude. It also nudges subscription revenue into API lock‑in, since the credits can only be spent on Anthropic's own models.

## Safety, with one awkward choice

Anthropic reports major alignment improvements over Haiku 4.5, with what it calls **"far fewer instances of misaligned behavior"** and a lower willingness to cooperate with misuse. The cybersecurity safeguards are the interesting part: they permit a wider range of defensive tasks than Sonnet 5.5's rules but still block penetration testing outright. Legitimate security teams do penetration testing, so blocking it in the name of safety creates friction that Anthropic seems comfortable with.

Haiku 5.5 is available now on **AWS, Google Cloud, and Azure**, and the Python and TypeScript SDKs are being updated to add support for computer use and browser use in beta. Whether the benchmark claims survive real‑world workloads is an open question, but the price cut is verifiable on the next invoice.

## Sources

- [Anthropic: Introducing Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5)
- [TLDR AI, October 8 2026](https://tldr.tech/ai/2026-10-08)
