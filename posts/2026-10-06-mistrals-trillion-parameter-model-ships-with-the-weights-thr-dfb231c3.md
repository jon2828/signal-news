---
title: Mistral's trillion-parameter model ships, with the weights three weeks out
date: 2026-10-06
topic: ai
score: 8
candidate_id: dfb231c34b69f857
sources: ["https://techcrunch.com/2026/10/06/mistrals-new-1t-model-aims-to-leapfrog-closed-and-open-rivals/"]
triage_reason: "Major 1T-parameter multimodal model release from Mistral, a notable lab, directly in the frontier model race."
---

# Mistral's trillion‑parameter model ships, with the weights three weeks out

Mistral AI released **Mistral Large 4** on Tuesday, a multimodal model with 1 trillion parameters that the French lab is pitching as an alternative to both closed American models and open Chinese ones. The internal nickname, per TechCrunch, is **Le Chonk**. The political framing comes from French President Macron, who has described Mistral's approach as *"a third way in AI."*

ML4 is not open‑weight yet. For now it sits behind a public guardrail endpoint, with the weights promised in about three weeks, once safety testing wraps. Pierre Stock, Mistral's VP of Science, told TechCrunch the company will spend that time working with "trusted partners and governments" so the open weights can be used defensively without enabling malicious attacks.

## The three‑week wait

The delay is the interesting part. Mistral's core audience is enterprises and institutions, and the company says security concerns have been mounting there. Stock's counterargument is that an open‑weight model is easier to audit, which the source confirms. **If the weights become public, the guardrail endpoint would no longer be relevant for users who run the model locally**, raising questions about how Mistral will ensure the released weights are used only defensively.

## The compute claim

Mistral says ML4 was trained entirely on its own compute, using **4,000 Nvidia GPUs**. Stock claims that is *"two to three times less than our Chinese competitors, and significantly less than the closed‑source competitors."* Benchmark results are still pending, so the GPU figure remains a claim from the company. If ML4 lands at the top of the open‑weight pack on 4,000 GPUs, efficiency becomes the headline; if it lands in the middle, the GPU count is more of a footnote. Stock said Mistral hopes the model will be best in class among open‑weight models and could beat closed models in specific areas that matter to customers.

## Follow the backers

The optimized use cases Stock named are cybersecurity, finance, and chip design. That last one is not a coincidence. Two of Mistral's main backers are **ASML**, which led its Series C, and **Samsung**, which led its Series D last month at a **€21 billion** valuation (about **$24.39 billion**). A frontier model tuned for chip design naturally aligns with the interests of its chip‑industry investors.

## The frontier‑lab question

The backdrop matters. Mistral recently had to argue that hosting Chinese models did not mean it was pivoting into a mere inference provider. ML4 is the rebuttal: a trillion‑parameter model, trained on its own GPUs, aimed at both the closed labs and the Chinese open‑weight scene.

I keep coming back to the gap between the announcement and the evidence: no benchmarks, no weights yet, and an efficiency claim that comes directly from the company. What actually shipped this week is a guarded endpoint and a promise. The promise is genuinely interesting, a trillion‑parameter open release from outside the US and China is not nothing. Whether the model backs it up is something we will know in about three weeks.

## Sources

- [TechCrunch: Mistral's new 1T model aims to leapfrog closed and open rivals](https://techcrunch.com/2026/10/06/mistrals-new-1t-model-aims-to-leapfrog-closed-and-open-rivals/)
