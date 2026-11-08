---
title: Gemini Omni 1.2 Flash: longer clips, lower price, same caveats
date: 2026-11-05
topic: ai
story: gemini-omni-1-2-flash
score: 10
candidate_id: 63c3d56bc72bc9e8
sources: ["https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/"]
triage_reason: "Google releases Gemini Omni 1.2 Flash with native 15-second video generation and editing capabilities."
---

Google is rolling out Gemini Omni 1.2 Flash, its video generation model, now generally available across the Gemini API and Gemini for business. The headline numbers: clips up to 15 seconds, up from 10 in Omni 1.1, and a 30% price cut that puts 720p generation at $0.07 per second.

## What is actually new

The clip length bump sounds small - five seconds. But you can now specify duration in one‑second increments from 3 to 15 seconds, and Google is pitching that as enough room for product explainers and full social ad spots in a single generation. That tells you exactly who this is for.

The more interesting change, I think, is multi‑turn conversational editing. You can refine the same clip turn by turn, swapping a product or background, changing lighting or weather, switching aspect ratio, instead of re‑generating from scratch. It works across full 15‑second clips. If it holds up outside Google's demos, this is the feature that changes the economics of the thing. Re‑generating a whole clip to fix one detail is where the cost and the frustration live.

Reference adherence also gets a push. You can combine character, product, or style images with short motion clips (up to three seconds) and audio cues, and Google says faces, garments, packaging typography, and brand colors stay consistent across camera angles. The demo examples are the usual glossy stuff: a virtual try‑on sequence built from one model photo plus front‑and‑back product shots, an FPV drone flight through the Pantheon with "zero jump cuts."

Speech gets an upgrade too, with what Google describes as more fluid dialogue, clearer lip‑sync, and distinct multi‑speaker conditioning, so different voices route to the right characters in a scene.

## The workflow is the pitch

Beyond the sticker price, Google is selling a cost structure. Draft fast at 360p or 720p, fix details with follow‑up edits, then upscale the keepers to 1080p or 4K. That is a sensible way to use these tools, and it is also a sensible way to keep you inside Google's pipeline. Provisioned Throughput is available for enterprise buyers, and outputs carry an imperceptible SynthID watermark.

The watermark point deserves a beat. Fifteen‑second, lip‑synced, multi‑speaker video at seven cents a second, generally available to anyone with API access, could enable the creation of convincing synthetic footage. Google's SynthID watermark is intended to help identify such content, though its effectiveness will depend on how widely detection tools are deployed. I remain skeptical about its impact for now.

## What Google admits it cannot do yet

Credit where due: the post names its own weak spots. Development is "ongoing" for fast sports action, rapid script changes, and complex physics. Read that as a warning about the demo reel. Every example in the announcement is a controlled scene with slow, deliberate motion - a conservatory, a poster assembling itself layer by layer, a drone flight through an empty building. Nobody is sprinting, colliding, or pouring a glass of water.

## My take

The price cut matters more than the extra five seconds. At $0.07 per second for 720p, a 15‑second ad variant costs about a dollar, and multi‑turn editing means you stop paying for full re‑generations. That is the point where ad teams stop experimenting and start shipping. Google clearly knows it, given how much of the post is aimed at brands and catalog workflows.

What I cannot tell you is whether the consistency claims survive contact with real prompts. Google's own comparison shows Omni 1.1 failing to match a reference image where 1.2 succeeds, which is honest of them, but it is still their benchmark and their picks. The post says businesses and creatives are already using 1.2 Flash in their workflows, yet names none of them. The gap between "holds references together in the launch post" and "holds references together on a Tuesday afternoon for a junior marketer" is where these launches live or die.

## Sources

- [Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/) (Google blog)
