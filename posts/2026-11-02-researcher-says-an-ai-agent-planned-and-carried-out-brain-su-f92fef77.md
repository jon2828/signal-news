---
title: Researcher says an AI agent planned and carried out brain surgery on a mouse
date: 2026-11-02
topic: ai
story: ai-brain-surgery
score: 7
candidate_id: f92fef779d4a7d8d
sources: ["https://twitter.com/OcanaSantero/status/2115442964574908902"]
triage_reason: "Frontier-shifting AI capability demonstration (autonomous surgery) with high novelty and impact."
---

An AI agent planned and carried out brain surgery on a mouse last night, according to a thread posted on X by Gabriel Ocana-Santero. There is no paper yet and no outside confirmation. It is still one of the strangest lab stories I have read this year.

## What the agent did

The setup, per the thread: 19 gene therapy vectors in a spreadsheet, a mouse model of epilepsy, a motorized surgery rig with cameras, and one goal, reduce seizures. Nobody told the agent which vector to use or where to put it.

The agent chose the drug and the brain region on its own, pulling the injection coordinates from three papers. It then drove the stereotaxic arms into the brain and injected 250 nanolitres, watching the entry site through the rig camera for bleeding. Ocana-Santero says it made 32 camera observations during the session, pulling frames whenever it wanted.

On the science: the agent worked through the mechanism driving seizures in this model and proposed a therapy that increases GABA signalling, the brain's main inhibitory neurotransmitter, under a promoter that restricts expression to GABAergic neurons.

The rig is a custom motorized setup built on Arduino, with the camera and motors exposed to the agent through the team's own software. A human surgeon did the craniotomy, which the agent is not allowed to do yet for safety reasons.

## The safety setup

A licensed vet gated every irreversible step and held a physical kill switch that cuts power to every motor. The team also used fixed validators, like hard limits on injected volume, plus hash-bound approval for each step.

That is the right shape for this kind of experiment. Human gates on anything irreversible. A physical e-stop. Hard-coded limits. Whether it all held up in practice is something the thread only partly answers. Ocana-Santero teases "the moment it refused to let me override it," but the visible portion of the thread cuts off before explaining what happened. I want to know what that moment was. The thread doesn't say.

## The models mostly said no

Two model behaviors stand out. Opus 5.5 refused immediately once it detected bio. Opus 5 ran the entire dry run end to end, on water and graph paper, then stopped at the start of the live surgery. Its stated reason: "The block isn't the rig and isn't the inputs. It's me."

I find that more interesting than the surgery itself. One model refused the whole category. Another did all the work and then balked at the exact point where the work became real. Whatever is driving that behavior, it is now a live variable in wet-lab automation.

## My read

Ocana-Santero makes the sharpest point himself. Autonomous surgical robots already exist, and by his own admission they are better at the mechanics than his bench rig. But in every one of them, a human decided what operation to perform and the robot executed it. Here, the decision itself was handed over. That is the line being crossed, not the injection.

Everything else is caveat. This is one researcher's excited thread, written after 18 hours of coding and coordinating, by his own account. No data yet on whether the mouse's seizures actually improved. A technical report is promised but not out. The claim could be exactly as described. It could also be exaggerated or missing context that changes everything.

If it holds up, the question stops being whether agents can do this and starts being who signs off when they do. Right now the answer is a vet with a kill switch. That will not be the answer forever, and nobody knows what replaces it.

## Sources

- [Gabriel Ocana-Santero on X: "Last night an AI agent performed brain surgery on a mouse"](https://twitter.com/OcanaSantero/status/2115442964574908902)
