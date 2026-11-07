---
title: OpenAI says its AI found 948 Linux kernel flaws and wrote an attack for each one
date: 2026-11-05
topic: both
story: openai-linux-exploits
score: 8
candidate_id: 7e36999a57b22695
sources: ["https://www.coindesk.com/tech/2026/11/05/openai-says-its-ai-can-break-into-linux-at-scale-here-s-what-it-means-for-crypto"]
triage_reason: "Frontier lab capability claim with concrete figures (948 flaws, working exploits) that shifts the AI security landscape."
---

# OpenAI says its AI found 948 Linux kernel flaws and wrote an attack for each one

*Date: 2026-11-05*

OpenAI says its AI found 948 security flaws in the Linux kernel and wrote a working attack for each one, at a cost of **$1,279 per flaw**, according to [CoinDesk](https://www.coindesk.com/tech/2026/11/05/openai-says-its-ai-can-break-into-linux-at-scale-here-s-what-it-means-for-crypto).

The attacks are privilege‑escalations. Someone who already has limited access to a Linux machine, a basic user account, for example, could use one to take full control. OpenAI says the tests were run on a standard Linux desktop with normal security protections turned on.

## How the system works

OpenAI describes a multi‑step pipeline:
1. Scan the kernel for risky code and potential flaws.
2. Test each candidate in a safe sandbox.
3. Determine whether the flaw can be turned into a working exploit.
4. Draft a fix for any exploitable flaw.

Human researchers review the results before they are passed to the Linux maintainers.

## Cost and potential value

OpenAI put the total cost of the exercise at **about $1.2 million** and estimated that the 948 flaws could be worth **$18.9 million to $66.3 million** if exploited, based on the source's own figures. Comparing those numbers suggests a potential return of roughly **15× to 55×** on the investment, assuming the hypothetical value is realized.

## What it means for crypto

Linux underpins much of the world's computing infrastructure, including a large share of cryptocurrency and blockchain operations. The article cites crypto‑security voices who argue that decentralization makes the industry more resilient than traditional software stacks.

While decentralization protects the ledger, it does less to protect the individual machines that hold private keys or sign transactions. A kernel exploit that grants root access to a single node can still be a serious threat, even if the broader network remains healthy.

## What we don't know

The report provides limited detail. OpenAI has not disclosed how severe each of the 948 flaws is, how many patches have been accepted by kernel maintainers, or how the exploits perform outside OpenAI's own testing environment. The longevity of this capability in "careful hands" remains an open question.

---

**Sources**
- [OpenAI says its AI can break into Linux at scale. Here's what it means for crypto (CoinDesk)](https://www.coindesk.com/tech/2026/11/05/openai-says-its-ai-can-break-into-linux-at-scale-here-s-what-it-means-for-crypto)
