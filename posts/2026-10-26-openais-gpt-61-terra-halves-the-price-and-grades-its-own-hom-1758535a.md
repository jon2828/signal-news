---
title: OpenAI's GPT-6.1 Terra halves the price and grades its own homework
date: 2026-10-26
topic: ai
score: 8
candidate_id: 1758535ac6be3e6b
sources: ["https://openai.com/index/introducing-gpt-6-1-terra", "https://openai.com/index/introducing-gpt-6-1-terra/"]
triage_reason: "New frontier-lab model release (GPT-6.1 Terra) for computer use, a frontier-shifting announcement with two sources."
---

# OpenAI's GPT-6.1 Terra halves the price and grades its own homework

**Date:** 2026-10-26

OpenAI announced GPT-6.1 Terra, a model built for computer use and visual reasoning that it positions as a major step up from GPT‑5.6 Terra at half the API price.

The pitch this time focuses on cost per task rather than raw capability. On **Agents' Last Exam**, a benchmark of professional computer work like turning architectural drawings into 3D models, Terra at medium reasoning effort scores 15 percentage points higher than GPT‑5.6 Terra at about one‑third the cost. OpenAI says it also matches GPT‑6 Astra on that benchmark at one‑tenth the price per token. At maximum effort, the company claims Terra is over three times as token‑efficient as Anthropic's Claude Opus 5.5 at one‑fourth the price per token, resulting in roughly a 9× lower cost per task. Tasks finish more than three times faster than on Astra or GPT‑6.1 Sol, per the announcement.

On **MMMU‑Pro**, a visual‑reasoning benchmark, Terra beats GPT‑5.6 Terra at every reasoning setting and nearly matches Astra and Sol. On **OSWorld 2.1**, which tests multistep desktop tasks, its medium‑effort score tops the older model's best score at a fraction of the cost per task.

## The hallucination numbers are the real story

On OpenAI's internal benchmark of error‑inducing prompts, the error rate at low reasoning effort fell from **53.6 %** with GPT‑5.6 Terra to **16.7 %** with the new model. At maximum effort it dropped **18 percentage points** to **4.3 %**, close to Astra and Sol. This is real progress, if it holds up outside OpenAI's test harness. The previous model, at low effort, produced errors on more than half of those prompts, and the new one still fails more than 4 % of the time. Cheaper agents that act on your screen make that residual rate matter more, not less.

## Coding and the rest

On **Terminal‑Bench 4.0**, Terra solves **50.3 %** of command‑line tasks at max effort, more than double GPT‑5.6 Terra's published **21.5 %**. OpenAI is upfront that Sol and Astra remain the better picks for the hardest coding work. On **Terminal‑Bench‑Science 0.1**, Terra beats Sol at lower cost and lands within five points of Opus 5.5 at less than one‑fifth the estimated cost.

## The catch

Every number above comes from OpenAI. The factuality benchmark is internal, as are the prompt‑injection tests. The cost‑per‑task comparisons against Claude are OpenAI's own estimates. That is normal for a launch post, and it means the honest position is to wait for independent evaluations and a few weeks of developer usage before believing any of it.

OpenAI's evaluations also say Terra is better than its predecessor at staying in scope and honestly disclosing limitations, and that it resisted malicious instructions in those internal prompt‑injection tests. Good, if true. Same caveat.

One more thing worth noting: Terra meets the **"Critical"** cybersecurity threshold under OpenAI's Preparedness Framework, and the company is shipping it with safeguards carried over from GPT‑6 Astra. That may be fine, but it deserves more than a brief paragraph in a launch post.

## Pricing and availability

Terra is live now for Plus, Pro, Enterprise, and Edu users in ChatGPT Work and Codex, and in the API as `gpt-6.1-terra`. Standard API pricing is **$1 per million input tokens**, **$0.05 per million cached input tokens**, and **$5 per million output tokens**.

The naming scheme, meanwhile, is a mess: GPT‑6.1 Terra, GPT‑6.1 Sol, GPT‑6 Astra, GPT‑5.6 Terra. I cover this for a living and still had to sketch a family tree.

## Sources

- [OpenAI: Introducing GPT‑6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra)
- [Hacker News submission of the announcement](https://openai.com/index/introducing-gpt-6-1-terra/)
