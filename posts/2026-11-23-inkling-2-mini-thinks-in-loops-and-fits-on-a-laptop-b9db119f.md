---
title: Inkling 2 Mini thinks in loops and fits on a laptop
date: 2026-11-23
topic: ai
story: inkling-2-mini
score: 7
candidate_id: b9db119f86f5ede9
sources: ["https://thinkingmachines.ai/news/inkling-2-mini/", "https://github.com/ShinMegamiBoson/lookatmyquant", "https://tldr.tech/ai/2026-11-23"]
triage_reason: "New model release from a major AI lab (Thinking Machines) corroborated by three sources, clearly publishable though not confirmed frontier-shifting."
---

# Inkling 2 Mini thinks in loops and fits on a laptop

**Date:** 2026‑11‑23

Thinking Machines released Inkling 2 Mini, an open‑weights model that runs the middle layers of the network three times for every token instead of once. The company calls it a *looped transformer*, and the pitch is simple: spend more compute thinking per token so the model needs fewer tokens to reach the right answer. TLDR's Monday write‑up described it as a model that "does extra internal computation to reason more before it answers," which is about right.

## Specs and performance

The spec sheet is odd in a way I like. Inkling 2 Mini is a Mixture‑of‑Experts model with **26.4 B total parameters**, **3.4 B active per token**, and **5.4 B weight activations per token** (the extra activations come from the three‑fold looping). Most weights were trained and are deployed natively in **NVFP4**, with the last four layers in **MXFP8**, and the total memory footprint is roughly **20 GB**.

Thinking Machines says it **leads every open‑weights model under 100 B parameters** on the DeepSWE v1.1 benchmark (48.2 %) and the Vals Index v2.2 (46.5 %). Their own table shows Inkling 2 Mini ahead of Gemma 4 31B and Qwen 3.8‑27B on most agentic‑coding evaluations, including **77.9 % on SWE‑bench Pro v2**. It does lose to Qwen on Terminal Bench v2.1 (71.6 % vs. Qwen's 73.0 %). These are self‑reported numbers, but the pattern is clear: a relatively small model that uses extra compute per token to punch above its active‑parameter count.

## The loop trick

Thinking Machines also released a **variable‑loop research variant** to measure the effect of looping. Its **no‑CoT time horizon** (how long it can work without writing anything down) improved from **16 s at one pass to 37 s at three passes**. On a serial‑reasoning benchmark, performance kept improving out to **ten loops**, twice the number of loops the model was trained with.

Looping does **not** buy knowledge. The company is blunt about this: "facts live in parameters," and the model's score on **AA‑Omniscience** (a factuality measure) is **in line with other models of the same size**. Long‑context benchmarks improve with more passes, but knowledge‑intensive benchmarks (AA‑Omniscience, SimpleQA Verified, SimpleVQA, WorldVQA) do not.

Inkling 2 Mini narrows the knowledge gap by **efficiently using search and tools**, leading similar‑sized open models on **BrowseComp (79.0 %)**, **DeepSearchQA (85.3 %)**, and **MCP Atlas (82.7 %)**.

## Monitoring implications

Looping lets the model, in Thinking Machines' words, **"reason longer without writing its reasoning down,"** which matters for monitoring because we rely on reading the chain‑of‑thought (CoT). The company notes that the **chain of thought grew shorter with more loops but stayed legible**, and the model **did not trend higher on agentic‑sabotage tests** as loops were added.

These findings come from the lab that built the model, using a research variant designed for clean comparisons. Independent replication would be needed before building a monitoring regime around this behavior.

## From laptop to iPhone in a day

A striking demo: researchers took Inkling 2 Mini on a flight, ran it **offline on a MacBook Pro**, and built a **playable flight simulator in a few minutes**. The model is now available on **Tinker** for inference and customization.

The community moved even faster. Within a day of release, the **MIT‑licensed LookAtMyQuant quantization compiler** produced **six Apple‑Silicon MLX builds** of Inkling 2 Mini, ranging from **12.76 GB down to 3.85 GB** (the latter targeting 8 GB iPhones). The **12.8 GB build matches the BF16 teacher on every benchmark** (349 / 349 pooled) while using **32.5 % less text‑weight memory**. The **3.9 GB iPhone build still solves 89.5 % of the 200 GSM8K problems**, though HumanEval performance drops to **59.1 %**. These numbers are from the LookAtMyQuant repository and are publicly available, though they have not been independently audited.

Historically, squeezing new model weights onto consumer hardware could take months. In this case, the first quantized builds appeared **within roughly 24 hours** of the public release, a dramatic acceleration, though it remains to be seen how robust the looping and monitorability claims are under broader third‑party evaluation.

---

**Sources**

- [Thinking Machines: Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini/)
- [LookAtMyQuant quantization compiler](https://github.com/ShinMegamiBoson/lookatmyquant)
- [TLDR AI, November 23 2026](https://tldr.tech/ai/2026-11-23)
