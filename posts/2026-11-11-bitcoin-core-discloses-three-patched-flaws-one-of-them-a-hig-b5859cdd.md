---
title: Bitcoin Core discloses three patched flaws, one of them a high-severity mining bug
date: 2026-11-11
topic: bitcoin
story: bitcoin-core-vulnerabilities
score: 7
candidate_id: b5859cdd2ddb87ff
sources: ["https://www.theblock.co/news/ecosystems/2026-11-11-bitcoin-core-discloses-three-patched-security-flaws-including-high-severity-mining-bug-437862"]
triage_reason: "Disclosure of patched Bitcoin Core flaws including a high-severity mining bug is important protocol security news that Bitcoin-focused readers need to"
---

Bitcoin Core publicly disclosed three security vulnerabilities on Tuesday, all of them patched more than a year earlier, including a high-severity bug that could stop mining nodes from producing valid block templates. [The Block has the full rundown.](https://www.theblock.co/news/ecosystems/2026-11-11-bitcoin-core-discloses-three-patched-security-flaws-including-high-severity-mining-bug-437862)

The three bugs were reported between April and September 2025. Fixes shipped in Bitcoin Core 30.0 on Oct. 10, 2025, and in version 29.2 on Oct. 14, 2025. The last vulnerable release went end of life on Oct. 27 this year. The details went public about two weeks after that.

## The mining bug

The serious one is CVE-2025-62861, rated high severity, affecting Bitcoin Core versions 28.0 through 28.2 and 29.0 through 29.1. Niklas Goegge reported it on Sept. 26, 2025.

The mechanics: Bitcoin Core's TRUC "sibling eviction" rules were still being applied to transactions returning to the mempool after a chain reorganization. The bug could evict a transaction without removing its descendants, leaving the mempool inconsistent. Miners hit by it had to restart their nodes before they could build valid block templates again.

A miner silently unable to produce valid templates until somebody notices and restarts the node is a real operational problem. High severity feels right.

## Compact blocks and the 10-minute delay

Eugene Siegel reported the second bug, CVE-2025-62859, back in April 2025. Medium severity. A malicious peer could exploit witness malleation in compact blocks to delay block processing by up to 10 minutes, and the attack could be repeated indefinitely.

The catch for attackers: it only worked against nodes running in "-blocksonly" mode, or where the attacker controlled all three of a node's high-bandwidth peers. That is a narrow set of targets, which is presumably why it landed at medium.

## The Tor whitelist problem

The third bug, CVE-2025-62860, is the one I keep coming back to. If a node operator set the optional "-whitelist" flag with an IP range that happened to include the Tor proxy, incoming Tor peers would receive whitelist permissions. Trusted status, handed out by accident.

Bitcoin Core said "thousands" of reachable mainnet nodes were doing exactly that. Whitelisting removes certain denial-of-service limits and privacy protections from those connections. Nodes without the non-default setting were not affected.

Config interactions are how quiet holes happen. Nobody decides to trust anonymous inbound Tor connections. A range overlaps with a proxy address and the protection is gone, with no warning to the operator. That thousands of nodes were affected tells me the failure mode was invisible in practice, not just in theory.

## The process worked, with a caveat

Credit where due. Each bug was reported and fixed well before disclosure, which came only after the vulnerable code reached end of life. The Block notes it covered a separate high-severity memory safety bug in May that followed the same path.

The part I find less comfortable is the timeline. Siegel's report landed in April 2025. The public learned about it in November 2026. Nineteen months is a long wait, even for a medium-severity bug with a fix already available. The logic behind waiting is sound, but it means the network runs on trust in a process most users never see.

Three patched bugs disclosed on a Tuesday still beats three exploited ones found on a Sunday.

## Sources

- [The Block: Bitcoin Core discloses three patched security flaws, including high-severity mining bug](https://www.theblock.co/news/ecosystems/2026-11-11-bitcoin-core-discloses-three-patched-security-flaws-including-high-severity-mining-bug-437862)
