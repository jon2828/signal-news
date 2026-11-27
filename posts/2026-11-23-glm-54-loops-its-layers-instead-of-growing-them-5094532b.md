---
title: GLM-5.4 loops its layers instead of growing them
date: 2026-11-23
topic: ai
story: glm-5-4-release
score: 8
candidate_id: 5094532b4e2e63d2
sources: ["https://z.ai/blog/glm-5.4"]
triage_reason: "Release of a new frontier model architecture (Loop Transformer) from a major AI lab is a frontier-shifting event."
---

Z.ai has released GLM-5.4, its first flagship model built on what it calls a Loop Transformer, and the pitch is simple: run the same layers twice instead of adding new ones.

The claim attached to it is big. Z.ai says the 750B model reaches "intelligence levels comparable to 2T-3T parameter models" by looping 28 layers of its GLM-5 base through a second iteration. If that holds up, it dents the bigger-is-better assumption that has driven most frontier progress. If it doesn't, it's a vendor blog post. The comparison is asserted rather than demonstrated in the announcement itself, so treat the headline number as a claim, not a result.

## How the loop works

In a standard transformer, each layer runs once per forward pass. In GLM-5.4, a block of weight-shared layers runs twice, refining the hidden states on the second pass. The idea is not new, and Z.ai says so. It credits the 2018 Universal Transformer and recent recurrent-depth work, and admits that looped models trained from scratch still lag unshared ones at equal pre-training compute. The workaround: don't train from scratch. Convert an already pre-trained model into a looper through continued training, which Z.ai says raises the ceiling for "a relatively small compute overhead."

Making that work at 750B took three fixes:

- Gated progressive updates. Overwriting hidden states directly across iterations blows up activation norms, so each token gets per-iteration gates controlling how much of each pass writes back to the residual stream. After training, the first pass writes conservatively and the second opens the gates fully. The gates also push harder on difficult tokens.
- Hybrid KV cache. A full KV cache per loop would multiply memory by loop count. Instead, the second pass reuses the sparse KV selected in the first pass and keeps only its own sliding-window KV on top. Z.ai says this keeps the deployment cost increase over GLM-5.3 under control even at 1M context.
- Sparse attention index reuse. The second loop reuses the first loop's attention indices outright, adding zero indexing overhead, with what Z.ai calls nearly identical performance to recomputing them.

## The numbers they did publish

The cleanest evidence is a controlled ablation on a 30B model sharing the 750B base architecture. Same parameter count, roughly 10% more training compute, and the looped version showed clear gains, concentrated in math, scientific reasoning, and long-context tasks. Output length dropped 10 to 14 percent on benchmarks like GPQA-Diamond and MMLU-Pro, mostly from shorter chains of thought. Part of the reasoning moves from visible tokens into the loop itself. I find that last point the most interesting result in the whole post.

Throughput is 200 tokens per second off-peak and 70 to 80 at peak load, which is respectable for a model running a chunk of its layers twice.

## What I'd watch

Two things. First, the failure mode Z.ai volunteers: the model tends to get caught in overly long "marathon thinking" loops. That is a funny and slightly alarming property in a model whose entire trick is looping, and the claim that this prolonged reflection "consistently" improves accuracy deserves outside testing. Second, whether anyone independent can replicate the 2T-3T parity claim. Self-reported parity has a long history of shrinking under external evals.

Z.ai frames all this as the start of "Generalized Coding," where code becomes the foundation for a much wider range of tasks. That part is marketing. The architecture underneath it is not. Spending compute on iteration depth rather than parameters, and getting shorter outputs as a side effect, is a genuinely different bet than the one the field has been placing. Whether it pays off at frontier scale, nobody knows yet.

## Sources

- [GLM-5.4: Toward Generalized Coding with Our First Loop Transformer](https://z.ai/blog/glm-5.4)
