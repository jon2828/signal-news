---
title: Gemini 4 Argon is out, and Google is pointing it at robots
date: 2026-10-13
topic: ai
score: 8
candidate_id: c64515c7bf5202fa
sources: ["https://developers.googleblog.com/gemini-4-argon-for-robotics/", "https://deepmind.google/models/gemini/", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/"]
triage_reason: "Frontier lab model release (Gemini 4 Argon for robotics) confirmed across three sources including Google's own blog."
---

# Gemini 4 Argon is out, and Google is pointing it at robots
---
**date:** 2026-10-13
**topic:** ai
**score:** 8
**candidate_id:** c64515c7bf5202fa
**sources:** ["https://developers.googleblog.com/gemini-4-argon-for-robotics/", "https://deepmind.google/models/gemini/", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/"]
---

Google released Gemini 4 Argon on **Wednesday**, its new frontier model, now available through the API in AI Studio, the Gemini app, and AI Mode in Search at an introductory price of **$2 per million input tokens** and **$10 per million output tokens** (cached input tokens are 95 % off) [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/). The announcement is long on claims, but the robotics demos are the part I keep coming back to.

## The robotics pitch

Google's developer post walks through four workflows. The headline number is **87 % on the Embodied Reasoning (ERQA) benchmark**, which tests physical and spatial problem‑solving in 3‑D environments. Google says that beats every other frontier model, using pure reasoning [[source]](https://developers.googleblog.com/gemini-4-argon-for-robotics/).

The demos themselves:

- **Spot quadruped** - Argon controls a Boston Dynamics Spot (12‑DoF legs + 6‑DoF arm) and learns to step on a foot‑pedal trash bin to throw away soda cans. Before touching the real pedal, it builds an articulated MuJoCo digital twin of the bin and practices there. The prompt even calls for a "2‑agent verification swarm" to check foot placement and hand‑in‑bin alignment before the can is released.
- **Simple robot arm** - Argon drives a wrist‑camera‑fed arm, righting a fallen mug and stuffing a crumpled napkin inside over several closed‑loop turns, using the calibrated coordinate grid shown in the attached image.
- **Gemini Omni video world model** - Argon steers a visual loop that rearranges five Scrabble tiles (G, R, A, N, O) into a row spelling **ARGON**, writing timestamped action prompts and refining them against intermediate keyframes.
- **Digital‑twin generation** - Argon watches a real‑robot tele‑operation episode, creates a physics‑matched simulation from the video, and iteratively tunes assets until contact events in simulation line up with the recorded data.

That last one is the real story: a model that turns raw video into a working physics simulation could automate a costly part of robotics development. If it holds up outside curated clips, it matters more than another benchmark point.

## The engineering claims

The launch post is stacked with internal wins. Argon helped the Chrome team separate core webpage handling from a roughly **6 million‑line** legacy folder inside Chromium's **40 million‑line** codebase, finishing "months of work in weeks" across hundreds of files [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/).

* The ADK team gave Argon a one‑paragraph goal to eliminate framework overhead. An overnight autonomous run cut **in‑memory session‑prep time by 40 %** in long sessions and **sped up cold imports by 21 %** [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/).
* Researchers made the **xTB** quantum‑chemistry package up to **2.3× faster** at predicting molecular structures and **1.8× faster** at conformer search [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/).
* Using Argon, Google achieved a **2.85× inference speed‑up** on Gemma 4 E2B via vLLM, raising throughput from ~37,900 to over 108,000 tokens per second on an A100, with 100 % token parity and no quality drop [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/).
* In Antigravity, Argon lifted **agentic code submissions by >35 %** while **reducing rollbacks by nearly a third** [[source]](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/).

## The skeptical footnotes

All of this is self‑reported. Every partner quote on the model page is a hand‑picked endorsement from an early‑access customer. The robot demos come with the prompts attached, which is good for transparency but tells you nothing about failure rates. The Spot prompt, with its verification swarm and camera checks, reads like a demo engineered to succeed, because it is.

The shape of the thing is still worth watching. A general model that writes its own simulation code, practices in it, then acts on real hardware is a different workflow from training a policy per task. Whether Argon does that reliably, at $10 per million output tokens, is something only people outside Google can answer. Nobody knows yet.

## Sources

- [Introducing Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)
- [Gemini 4 Argon for Robotics](https://developers.googleblog.com/gemini-4-argon-for-robotics/)
- [Gemini models (DeepMind)](https://deepmind.google/models/gemini/)
