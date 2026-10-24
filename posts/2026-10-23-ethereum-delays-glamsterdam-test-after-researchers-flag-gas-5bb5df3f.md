---
title: Ethereum delays Glamsterdam test after researchers flag gas risks to existing contracts
date: 2026-10-23
topic: bitcoin
score: 7
candidate_id: 5bb5df3f2308694a
sources: ["https://www.coindesk.com/tech/2026/10/23/ethereum-delays-glamsterdam-test-after-security-devs-flag-risk-to-existing-contracts"]
triage_reason: "A security-driven delay to a major Ethereum upgrade is an important protocol development with a concrete technical cause."
---

Ethereum developers have called off Monday's Glamsterdam upgrade on the Hoodi test network after security researchers showed that proposed gas changes could alter how existing smart contracts handle failed transactions, in some cases letting errors become permanent.

The upgrade was set to activate on Oct. 26 at 17:42:48 UTC. Developers pulled it during Thursday's All Core Devs Execution meeting, and no replacement date has been announced, per CoinDesk.

## What went wrong

The problem sits with EIP‑8037, a proposal that changes how Ethereum charges for creating new records in its database. The goal is reasonable: slow the growth of that database as the network processes more transactions. The side effects are not.

Security firm ChainSecurity published an analysis on Oct. 13 showing that EIP‑8037, combined with EIP‑8038, could change how contracts behave when another contract they call runs out of gas. Plenty of deployed contracts are written to catch a failed call and keep going. Some developers built on the assumption that a failed call would leave too little gas for any cleanup code to run, so the whole transaction would reverse on its own.

Glamsterdam breaks that assumption. Under the proposed rules, gas spent creating certain records gets restored when those changes are undone. That can leave enough gas for the failure‑handling code to finish, meaning an operation that used to reverse cleanly could now be recorded as a permanent failure.

The risk runs the other way too. ChainSecurity calculated that creating a new storage slot could cost 110,020 gas once a separate allowance is exhausted, up from 22,100 gas under the current rules. A contract working with a fixed gas budget could fail while doing something perfectly valid.

## What the risk actually looks like

Some perspective is in order. ChainSecurity has demonstrated the mechanisms but has not shown that any major production protocol is exploitable. Nothing on mainnet is at risk right now. The findings describe how existing software would behave under proposed rules, not a live attack.

This is also, to be fair, what testnets are for. Glamsterdam completed its Sepolia activation on Oct. 6. Hoodi was the next rehearsal, paired with a planned gas‑limit increase to 200 million, which is now postponed as well. Catching this before mainnet is the process working.

Glamsterdam also brings a new system for choosing block builders and changes meant to let the network handle larger blocks. Ethereum's mainnet has no confirmed activation date for the upgrade, and it remains unclear when a mainnet rollout will be scheduled pending resolution of the gas‑accounting questions.

## Sources

- [CoinDesk: Ethereum delays Glamsterdam test after security devs flag risk to existing contracts](https://www.coindesk.com/tech/2026/10/23/ethereum-delays-glamsterdam-test-after-security-devs-flag-risk-to-existing-contracts)
