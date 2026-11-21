---
title: Google launches Gemini 4 Neon, and the scoreboard is Google's own
date: 2026-11-19
topic: ai
story: gemini-4-neon
score: 8
candidate_id: e2b6407cfa6894d3
sources: ["https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/", "https://tldr.tech/ai/2026-11-19"]
triage_reason: "A new model release from frontier lab Google, corroborated by two sources, is frontier-shifting for AI readers."
---

Google announced Gemini 4 Neon on Wednesday, a fast frontier model aimed at coding, knowledge work, and science tasks, priced at $3 per million input tokens and $15 per million output tokens with a 1 million-token context window. Cached input drops to $0.15 per million tokens, a 95% discount. It is rolling out now in the Gemini API, Google AI Studio, the Gemini app for Pro and Ultra subscribers, and Google Antigravity.

## The numbers Google wants you to see

The launch post is a wall of benchmarks. Neon scores 61 on the Artificial Analysis Intelligence Index at its xhigh thinking level, third overall behind what Google calls "larger, slower models." It ranks second on the Vals Index at 70.9% and first on the Artificial Analysis Coding Agent Index at 58.6, with 65.2% on Terminal-Bench 4.1. On the agentic side it takes first on Zapier's AutomationBench (56.3%) and on Andon Labs' Vending-Bench 2, where it ran a simulated business up to $16,843. It debuts at number two on the Agent Arena Index, drawn from more than 4,200 real-world agent sessions.

Google also claims the cost curve bends hard. At its default high thinking level, Neon supposedly costs 32% less per task than Gemini 4 Carbon, and 50% to 80% less per task than "top competing frontier models" on the Vals and Agent Arena indexes. The cyber numbers are aggressive too: 90.5% on SEC-bench Pro for vulnerability finding, and a state-of-the-art 51.26% on WebExploitBench v1.2 at what Google says is half the cost of competing large models.

One detail is worth pausing on. On SWE-sweep, Neon scores 12.8% on the mini-SWE harness and 39.0% inside Google Antigravity. Same model, triple the score, different harness. Google frames this as proof of what Antigravity unlocks. I read it as proof of how much these results depend on the scaffolding around the model, which is exactly the part vendors control and buyers can't easily compare.

## What the launch post leaves out

Two items from TLDR's AI newsletter the morning after fill in the picture. In a private benchmark, Gemini 4 Carbon, Neon's bigger sibling, spent close to an hour on bug fixes that Claude Opus 5.5 and GPT-6 Astra finished in minutes, taking about seven times as many steps as Astra with half of them unnecessary. That is Carbon, not Neon, and Neon is pitched as the fast one. Still, it is a reminder that Google's internal rankings and third-party experience do not always line up.

The second item concerns Antigravity itself. TLDR reports the tool wipes users' prompt caches after a 5-minute pause, and that even a five-word prompt carries 13,800 to 16,800+ tokens of system instructions, MCP schemas, and skills before you type anything. Hold that next to the headline pricing. The 95% cached-input discount only saves you money if the cache survives, and Google's own agent tool apparently clears it while you make coffee.

## My read

If the numbers hold up, Neon looks genuinely strong on steerability and long-horizon agent work, and the price is aggressive for the claimed capability. But every figure in the launch post is either self-reported or from a benchmark Google chose to print, and the two independent data points that surfaced this week point the other direction. I would wait for outside evals before moving any production workload onto it.

## Sources

- [Introducing Gemini 4 Neon (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)
- [TLDR AI, November 19, 2026](https://tldr.tech/ai/2026-11-19)
