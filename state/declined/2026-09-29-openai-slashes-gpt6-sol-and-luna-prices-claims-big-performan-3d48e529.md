---
title: OpenAI slashes GPT‑6 Sol and Luna prices, claims big performance gains
date: 2026-09-29
topic: ai
score: 10
sources: [""]
triage_reason: "Announcement of new frontier models (GPT-6 Sol and Luna) from a major lab is a market-moving event."
---

OpenAI announced on September 22 that its new GPT‑6 Sol and Luna models will cost half as much as the previous GPT‑5.6 pricing 【1】. The company says the cut comes from better caching and inference, not from a downgrade in capability.

The price sheet is stark. Input tokens drop from $4 to $2 per million for Sol, and from $0.20 to $0.10 for Luna. Output tokens fall from $20 to $10 for Sol, and from $1.20 to $0.50 for Luna 【1】. That is a 50 % reduction across the board.

But cheaper does not automatically mean weaker. OpenAI's internal benchmarks paint a more nuanced picture. On the AutomationBench suite, which runs end‑to‑end business workflows across 47 tools, GPT‑6 Sol at "xhigh" effort beats Claude Opus 5 at max effort while costing only 9 % of Opus 5's per‑task expense 【1】. Luna improves on its predecessor by 5.4 percentage points at 58 % lower cost 【1】.

A side‑by‑side table shows Sol scoring 33.2 % on the same benchmark, with a cost of $0.27 per task. By contrast, Claude Opus 5's cost is 11.1 times higher 【1】. Even low‑effort GPT‑6 Astra, the flagship model, ends up 3.9 times more expensive per task than Sol at high effort.

Factuality also gets a boost. OpenAI reports that GPT‑6 Sol makes about half as many mistakes as GPT‑5.6 Sol on a de‑identified internal error‑tracking set 【1】. The claim is that Sol is approaching Astra‑level reliability, though the data comes from flagged conversations that are not representative of typical usage.

Coding benchmarks show similar trends. On FrontierCode, Sol outperforms GPT‑5.6 Sol and matches Claude Fable 5.1 at "xhigh" effort for a fraction of the cost 【1】. DeepSWE v1.1 puts Sol at 68.8 % accuracy at max effort, just 1.1 percentage points shy of Claude Fable 5's 69.9 % at "xhigh", while costing roughly 80 % less per task 【1】. Luna trails a bit but still beats Claude Opus 5 and Fable 5 at medium effort, with a 93 % cost reduction 【1】.

Computer‑use tests echo the pattern. OSWorld 2.0 offline shows Sol at "xhigh" effort scoring 60.5 % versus Claude Opus 5's 60.3 % at medium effort, again at about 80 % lower cost 【1】.

All of this sounds impressive, but the numbers come from OpenAI's own labs. Independent verification is still missing. The company's earlier update to GPT‑5.6 Sol in ChatGPT promised "more reliable facts" and a 68 % drop in factual errors compared with GPT‑5.5 Instant 【2】. That claim was based on internal financial, medical, and legal prompts, not on a public benchmark.

The pricing shift could push more developers onto the cheaper tier, especially for token‑heavy workloads like code generation or multi‑step automation. That may accelerate the "AI‑first" stack in startups, but it also raises the bar for cost‑based competition. If OpenAI can keep delivering Astra‑level quality at Sol/Luna prices, other providers will have to decide whether to match performance, undercut price, or focus on niche alignment.

One concern is alignment. OpenAI notes that the newer models inherit Astra's alignment work, but the press release offers no new safety metrics for Sol or Luna. The same "full‑duplex" voice model, GPT‑Live, is being rolled out separately and still relies on GPT‑5.5 in the background 【3】. That suggests OpenAI is still decoupling front‑end interaction from the frontier model, a design choice that could hide alignment gaps.

Bottom line: OpenAI is betting that cheaper, still‑powerful models will broaden its user base and lock in more API revenue. The performance claims are solid on paper, but they remain internal. We'll need third‑party tests to know whether Sol and Luna truly deliver "advanced AI practical for everyday tasks" or just a polished marketing narrative.

**Sources**

- OpenAI, "Introducing GPT‑6 Sol and Luna," Sep 22 2026 【1】
- OpenAI, "Improving GPT‑5.6 Sol in ChatGPT," Aug 6 2026 【2】
- OpenAI, "Introducing GPT‑Live," Jul 8 2026 【3】
