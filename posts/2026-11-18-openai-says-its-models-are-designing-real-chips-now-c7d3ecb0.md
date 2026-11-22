---
title: OpenAI says its models are designing real chips now
date: 2026-11-18
topic: ai
story: openai-chip-design
score: 7
candidate_id: c7d3ecb006439a13
sources: ["https://openai.com/index/advancing-chip-design-with-our-models", "https://openai.com/index/advancing-chip-design-with-our-models/"]
triage_reason: "Significant application of frontier AI models to hardware design, indicating a new capability area for OpenAI."
---

# OpenAI says its models are designing real chips now

*Date: 2026-11-18*

OpenAI says its models have started designing the silicon they run on, and it published numbers to back the claim.

The post covers the work on Jalapeño (OpenAI's first custom inference chip), a partnership with AMD, and an internal evaluation tracking how each model generation handles chip‑design tasks. Some of it is genuinely impressive; some of it is a company grading its own homework. Both can be true.

## The Jalapeño numbers

OpenAI started using GPT‑o3 mini on Jalapeño in early 2025. According to the post, model‑proposed changes cut standard‑cell area by about 13 % in the vector unit and 10 % in the matrix unit. One multiplier redesign used roughly 15 % less cell area while dropping latency from two clock cycles to one. A separate adder redesign cut area by about 15 % while keeping its two‑cycle latency.

The part that matters: these were not simulation‑only wins. OpenAI says the optimizations were **"silicon proven"** during Jalapeño's bring‑up, meaning the chip returned from the fab and the changes actually worked.

## The AMD work

The AMD numbers are larger and may be more credible because they were verified by a party outside OpenAI. OpenAI claims up to 14 % improvement in power, performance, and area relative to "heavily optimized baselines" on AMD's flagship GPU IP, achieved by rewriting the SystemVerilog RTL that describes the circuits. AMD verified the results, has already included some changes in a design sent for manufacturing, and separately confirmed single‑digit percentage gains on key blocks of its upcoming next‑generation flagship CPU.

OpenAI frames this as **"roughly a year of progress achieved in less than 5 months."** The claim is the company's own framing, and the "up to" qualifier reflects the range of observed gains.

There is also a partnership with Synopsys to integrate the models into the EDA tools chip engineers already use; those tools verified that each rewrite preserved the block's behavior.

## The evaluation

To track progress across generations, OpenAI tested its models on two open‑source 32‑bit RISC‑V cores, PicoRV32 and Ibex (the embedded processor in OpenTitan's security chip). The task was to raise throughput, measured as instructions per second. Designs scored zero if they failed correctness checks or exceeded 16 × the original area.

With a budget of about 112,000 tokens per run, **GPT‑6.2 Astra** posted the highest average score on both cores, and **GPT‑6.1 Sol** outscored **GPT‑5.6 Sol** on both. The full evaluation covered **9,881** scored runs across both tasks, both cores, and all token budgets.

All five models scored higher when they designed a core from written requirements than when they tried to improve an existing design. OpenAI notes that starting from requirements lets the model omit features such as performance counters and extra instructions that do little for the test workloads, which could explain part of the advantage. Tighter area limits and timing checks after physical synthesis would make the task harder, as the post acknowledges.

## What I make of it

Self‑reported benchmarks deserve skepticism, and the evaluation is in‑house. The AMD involvement provides the strongest external validation, because the results were verified by a party with no incentive to inflate them.

The broader implication is that AI models are now finding double‑digit area savings in the chips that run AI workloads, and each model generation scores better at the task than the one before it. If this trend continues, the feedback loop between model capability and hardware capability could accelerate rapidly. How far it will go remains an open question, but dismissing the work as mere marketing becomes harder when the changes are baked into a taped‑out GPU.

---

**Sources**
- [OpenAI: Advancing chip design with OpenAI models](https://openai.com/index/advancing-chip-design-with-our-models)
