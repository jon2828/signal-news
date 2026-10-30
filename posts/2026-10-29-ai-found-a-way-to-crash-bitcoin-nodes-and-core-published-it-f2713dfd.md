---
title: AI found a way to crash bitcoin nodes, and Core published it six days later
date: 2026-10-29
topic: both
score: 7
candidate_id: f2713dfd80c41501
sources: ["https://www.coindesk.com/tech/2026/10/29/ai-found-a-way-to-crash-bitcoin-nodes-on-windows-and-macs-it-s-now-public"]
triage_reason: "AI-discovered denial-of-service flaws in Bitcoin Core, disclosed under a new bug-disclosure policy, is a genuinely novel research result at the site's"
---

# AI found a way to crash bitcoin nodes, and Core published it six days later

**Date:** 2026-10-29

Bitcoin Core has disclosed three vulnerabilities found by an AI scan, and one of them lets a stranger crash your node. Any computer connected to a node running Windows, macOS, or BSD could flood it with data until it ran out of memory and died, according to CoinDesk.

The speed is the story. The scan flagged the crash bug on **Oct. 23**. Developers confirmed it the same day. Fixes shipped on **Oct. 27**. Full details went public on **Oct. 29**, alongside two other bugs the same scan turned up.

---

## The old rules assumed secrecy helped

Until last week, Core kept medium‑severity flaws like this one quiet for as long as a year. The logic was reasonable enough: give node operators time to upgrade before attackers learned where to look.

That logic changed on **Oct. 22**, when the project revised its disclosure policy for bugs it judges "easily discoverable." The stated reason is blunt: LLMs have made that class of bug cheap to find, so sitting on a fix mostly protects people who already know about it. Fixes for these bugs now go out as soon as possible to every supported version, with a public advisory attached (CoinDesk).

---

## Humans still did the part that matters

One detail worth holding onto before this becomes another "AI finds everything" story: the scan flagged the bugs, but human contributors verified them and wrote the patches. The model compressed the search, which is real and useful, but the pipeline from flag to patch still ran through people who understood what they were looking at.

---

## The asymmetry cuts one way

Both defenders and potential attackers could, in principle, use similar language models. If a malicious actor ran the same scan on the Bitcoin Core codebase, the vulnerabilities could be identified as well. In this context, rapid disclosure may help limit any advantage an attacker could gain, since the advisory itself is not required for an exploit.

Also worth saying plainly: this is a crash bug, not a theft bug. A node going down is a headache for its operator and, if it happened at scale, a health problem for the network. Nobody's coins move. The severity is real but bounded, and the fix is already out.

---

## What comes next

Three more vulnerabilities, rated medium and high severity and fixed in Bitcoin Core 30.0, are expected to be disclosed in about two weeks. Whether those also came from an AI scan is not stated in the reporting.

---

## Sources

- [CoinDesk: AI found a way to crash bitcoin nodes on Windows and Macs. It's now public](https://www.coindesk.com/tech/2026/10/29/ai-found-a-way-to-crash-bitcoin-nodes-on-windows-and-macs-it-s-now-public)
