---
title: Ethereum's Glamsterdam upgrade could break up to 15,000 contracts
date: 2026-11-17
topic: bitcoin
story: ethereum-glamsterdam
score: 8
candidate_id: 4f11c6cfd92ae155
sources: ["https://www.coindesk.com/tech/2026/11/17/ethereum-s-glamsterdam-upgrade-risks-breaking-up-to-15-000-contracts"]
triage_reason: "A major Ethereum upgrade risking breakage of up to 15,000 apps with audit findings and a near-term developer decision is significant protocol news."
---

Ethereum's planned Glamsterdam upgrade could break as many as 15,000 smart contracts, according to an Ethereum Foundation developer who shared the estimate on a developer call Monday.

Marius van der Wijden said the affected programs represent a "tiny fraction" of the roughly 90 million smart contracts on the network, and he estimated that a few hundred thousand dollars could be at risk across the potentially affected contracts. CoinDesk notes that this figure is far larger than earlier reviews had identified - the more the audits dig, the more incompatibilities surface.

## What actually changes

Two proposals, EIP‑8037 and EIP‑8038, would rework how Ethereum charges users and applications to store and retrieve data. The stated goal is to curb growth in the network's database.

Under EIP‑8037, creating new permanent state - such as deploying a contract or adding a storage entry - would be billed separately instead of being bundled into ordinary execution gas. Deploying a new contract would cost about 183,600 gas, up from 32,000 gas (roughly 5.7 × higher). Creating a new storage slot would cost roughly 97,920 gas, up from 20,000 gas (about 4.9 × higher).

The applications most likely to break are those built around predictable costs or fixed computing allowances. If a contract hard‑coded assumptions about write costs, a fee change like this could cause a failure mode rather than a minor inconvenience.

## The testing is not going well

Beyond the 15,000‑contract estimate, independent audits have uncovered hundreds of separate compatibility problems, per CoinDesk. Those problems have delayed testing on the Hoodi public test network. Glamsterdam has no confirmed release date, and core developers are set to reconsider the changes on Thursday.

The outcome of Thursday's call is not yet known, but the growing list of compatibility issues suggests that shipping on schedule should not be assumed.

## Sources

- [CoinDesk: Ethereum's Glamsterdam upgrade risks breaking up to 15,000 automated apps](https://www.coindesk.com/tech/2026/11/17/ethereum-s-glamsterdam-upgrade-risks-breaking-up-to-15-000-contracts)
