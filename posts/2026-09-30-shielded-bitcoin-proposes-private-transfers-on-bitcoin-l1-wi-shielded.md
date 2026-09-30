---
title: Shielded Bitcoin proposes private transfers on Bitcoin L1 without a soft fork
date: 2026-09-30
topic: bitcoin
score: 8
candidate_id: shielded-btc-allocinit
sources: ["https://allocinit.notion.site/Shielded-Bitcoin-Private-Transfers-on-Bitcoin-L1-3e436974087f80f586acf2462bc547a5"]
triage_reason: "Owner-requested coverage: first Bitcoin L1 privacy architecture with no soft fork, no operators, no bridge."
---

A new paper proposes shielded, private bitcoin transfers on the base layer, with no soft fork, no new chain, and no trusted bridge operators. The proposal, called Shielded Bitcoin, comes from Clara Shikhelman, Mikhail Komarov, and Aleksei Moskvin, and it's laid out in a plain-language companion post on Notion.

The pitch is narrow and the authors say so themselves: can bitcoin move without publicly revealing amounts and counterparties, using Bitcoin exactly as it exists today? Their answer is a metaprotocol. Bitcoin keeps doing what it does, storing and ordering bytes. The privacy logic lives entirely off-chain, in software anyone can run.

## How it works

Value inside the system lives in "notes," small encrypted records holding an amount and a way to reach the owner. Notes never appear on-chain in readable form.

A transfer is ordinary Bitcoin transaction data containing three things: encrypted notes, a unique serial number (a nullifier) for each note being spent, and a zero-knowledge proof. The proof asserts that the spent notes exist, that the spender is authorized, and that amounts in equal amounts out. It does this without revealing which notes or how much.

Programs called indexers watch the chain, verify proofs, and check that no nullifier has appeared before. That last check is what prevents double-spends. The authors' analogy: Bitcoin is a public bulletin board. It publishes and orders the data, and anyone can independently replay the rules to compute the state.

Receiving works by trial decryption. Your wallet tries to open each new note with your viewing key. Most fail, since they belong to other people. The one that opens is yours.

## The trust claims

This is where I pay attention, because Bitcoin privacy proposals usually smuggle in an operator somewhere. The authors claim this one doesn't. Only your spending key can move your notes, indexers reject anything without a valid proof, and nobody holds user funds. A dishonest indexer can delay or serve stale data, which can disrupt your wallet, but it can't spend anything. You can switch indexers or replay the history yourself.

The design goals, in their words, are to eliminate "trusted operators, interactivity, liveness dependencies, and liquidity/exit-collateral requirements." That's a direct shot at the tradeoffs in existing L2 and sidechain privacy schemes, and if it holds up, it's meaningful.

## The catch

The obvious gap: getting bitcoin in and out. The post says deposits and withdrawals will use "security vaults on the L1 via PIPEs," but the details are deferred to a companion paper that hasn't been released yet. That's not a footnote. The entry and exit mechanism is exactly where trust assumptions tend to hide in systems like this, and right now it's a promise, not a spec.

So my read is cautiously interested. The transfer mechanics are coherent and the no-soft-fork constraint is real and hard. But the vault design is the part that decides whether this is a genuine privacy architecture or a clever transfer layer bolted to a trusted door. I'll wait for the companion paper before believing the "no operators" claim end to end.

## Sources

- [Shielded Bitcoin: Private Transfers on Bitcoin L1](https://allocinit.notion.site/Shielded-Bitcoin-Private-Transfers-on-Bitcoin-L1-3e436974087f80f586acf2462bc547a5)
