---
title: Gemini 4 Carbon arrives with top cyber benchmarks and a defenders-first rollout
date: 2026-10-28
topic: ai
score: 8
candidate_id: 185e559c77b9fcf3
sources: ["https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/"]
triage_reason: "Official Google announcement of a new Gemini model is a frontier-lab model release, the top tier for AI readers, though a single source warrants the l"
---

Google announced Gemini 4 Carbon on October 28, and the pitch is not a friendlier chatbot but a better security researcher. Google calls it "our strongest model," with the gains concentrated in cybersecurity and long-horizon agentic work.

The headline numbers: Carbon ranks first on the updated Artificial Analysis Intelligence Index v5.0 with a score of 59. It posts 88.2% on SEC-bench Pro, which tests finding real vulnerabilities in shipping software. It sets a new mark on ExploitGym at 54.8%, a benchmark for checking whether a flaw is actually exploitable, and it hits 71.0% on Collinear's CWE-bench for turning findings into patches.

Read that middle one again. Google is advertising how good its model is at exploitation. The framing is defensive, since defenders need to know which vulnerabilities are worth fixing first, and that framing is legitimate. But a model that tops an exploitation benchmark is a model that can exploit. Google clearly knows this, because the rollout looks nothing like a normal launch.

## A rollout that looks like a disclosure process

Carbon is not going straight to the API. Google says it is engaged in the U.S. government's "voluntary process for pre-release model testing." Starting this week, access goes to a subset of cyber defenders, then expands gradually to trusted partners through what Google calls the Fairwind Program. Wider availability comes later, after more guardrail work.

I can't remember Google metering out a frontier model like this. Two weeks ago it shipped Gemini 4 Argon. Now Carbon arrives with benchmarks that read like capabilities research, and access is being handed to defenders before anyone else. Whatever you think of the safety-theater critique, this is at least the shape of a company treating offensive cyber capability as a genuine risk.

One caveat Google includes itself: the external cyber evals ran without guardrails. The numbers describe the raw model, not the constrained product defenders will actually use.

## The rest of the card

Google claims more than a 2x internal uplift over Argon in generating secure code, and says the Chrome team found Carbon produced high-quality patches "more than 10X better" than another lab's frontier model. That other lab goes unnamed, which is convenient. On public evals, Carbon jumps 89 elo points to fourth place (1768) on WebDev Arena, and Google says internal teams have watched it run for days on multi-step engineering work, pushing through dead ends to root-cause bugs across large codebases.

The alignment claims deserve a raised eyebrow. Google says Carbon cut successful cheating on Terminal-Bench 4.0 to 0.0%, with attempts down to 0.4%, and that high-severity misalignment alerts in live internal use dropped almost 80%. Unsupported claims are down about 2x versus Argon. All of these are internal measurements. Google is grading its own homework, and a clean 0.0% is the kind of number that makes me want to see the eval harness before believing it.

Pricing matches Argon: $2 per million input tokens, $10 per million output, cached input at 95% off. Note the word "introductory" in Google's pricing line.

## My take

The two-week gap between Argon and Carbon tells you frontier release cycles are getting fast enough to make version numbers meaningless. The cyber results are strong if they replicate outside Google's harness. The staged rollout is either responsible caution or smart positioning ahead of regulation, and quite possibly both. Nobody outside Google's trusted-partner list can test any of this yet, which is, of course, the point.

## Sources

- [Introducing Gemini 4 Carbon (Google blog)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)
