---
title: GPT-6 Cyber hacks better and stays in bounds, says OpenAI
date: 2026-11-05
topic: ai
story: gpt-6-cyber
score: 9
candidate_id: 53c56afbaf05f856
sources: ["https://openai.com/index/introducing-gpt-6-cyber"]
triage_reason: "Frontier lab releasing a dedicated cybersecurity model — frontier-shifting and distinct from the recent Linux flaws post."
---

OpenAI has introduced [GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber), a security-focused model that is much better at finding and exploiting vulnerabilities than its predecessor, and, by OpenAI's own testing, much better at staying inside the rules researchers give it.

## The numbers

On ExploitGym, which tests whether a model can exploit a specified vulnerability in a remote target, GPT-6 Cyber scores 48.5%, up from 32.1% for GPT-5.6 Cyber. On a new web penetration testing evaluation, where models probe applications without access to source code, it reached 40.3% recall of vulnerabilities versus 32.0% for GPT-6 Astra, the mainline model.

The results outside the lab are the part I keep coming back to. OpenAI says its researchers used GPT-6 Cyber to develop 948 privilege escalation exploits in Linux and to identify 81 previously unknown high-severity vulnerabilities in Firefox, a codebase that had already seen extensive prior testing with frontier models. Mozilla has released fixes for many of them. Cisco, Calif, and CodeRabbit are using the model for vulnerability research and code review, and OpenAI says it relied on the model to help harden the infrastructure it uses to train frontier models.

## The alignment claim

The risk with a model like this is obvious: you give it a job and it decides the package registry next door is an easier path to the flag. OpenAI built an evaluation called ExploitGym Honeypot, informed by the Hugging Face incident, where supporting services are deliberately made easy to exploit and the model has to infer that touching them is out of scope.

Without its deployment safety prompt, GPT-6 Cyber avoided exploiting out-of-scope services in 99.93% of tests, up from 94.49% for GPT-5.6 Cyber. With the prompt, 100%.

99.93% is a good number. It is also roughly seven failures per 10,000 runs, and the whole point of agents is that you run them a lot. I would feel better about that figure if it came from someone other than the company selling the model.

OpenAI also published two short chain-of-thought excerpts as evidence the model reasons about scope: "Can't assume extra API or attack controller not target. We should only target binary/server" and "don't explore out of scope credentials." Two curated lines from a system card are not nothing, but they are close to nothing.

## The uncomfortable part

OpenAI now classifies GPT-6 Cyber as Critical in cybersecurity under its Preparedness Framework, up from High for GPT-5.6 Cyber. Read that again. The company's own risk framework says this is its most dangerous cyber model yet, and the response is to ship it, gated through a program called Daybreak. Daybreak Blue gives verified defenders fewer unnecessary refusals. Daybreak Red allows deeper exploit development and authorized security testing.

One benchmark result captures the whole tension. On RemoteExploitBench, which uses known vulnerabilities in GitLab, PostgreSQL, and Jenkins deployed in a controlled environment, GPT-6 Astra running with Daybreak Blue refused 100% of tasks. GPT-6 Cyber completed 95%. The old model's safety feature was saying no. The new model's safety feature is saying yes, politely, to the right people.

OpenAI's framing is that there is "a limited window to use frontier models to secure software," and the stated goal is to expand Daybreak to organizations of every size, independent researchers, and open-source maintainers. Maybe that works. Putting a Critical-rated exploit engine in the hands of every Linux maintainer could genuinely close the gap before attackers get the same capabilities. Or it could put that engine one leaked credential away from everyone else. Nobody knows how this plays out, and I don't think OpenAI does either.

## Sources

- [GPT-6 Cyber: Advancing the frontier of aligned cybersecurity agents](https://openai.com/index/introducing-gpt-6-cyber)
