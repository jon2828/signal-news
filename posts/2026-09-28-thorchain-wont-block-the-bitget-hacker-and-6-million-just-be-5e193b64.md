---
title: THORChain won't block the Bitget hacker, and $6 million just became bitcoin
date: 2026-09-28
topic: bitcoin
score: 8
sources: ["https://www.coindesk.com/tech/2026/09/28/thorchain-rejects-bitget-request-to-block-hacker-as-usd6-million-moves-to-bitcoin"]
triage_reason: "Original reporting tracing $6M in stolen funds from a $387.5M hack moving through THORChain despite blocking requests."
---

A wallet tied to the Bitget hacker swapped about $6.3 million in ether for 75.2 bitcoin through THORChain on Monday, and the protocol refused to do anything about it.

CoinDesk dug through THORChain's public transaction records and found 27 successful swaps moving roughly 2,390 ETH into BTC, all paid out to a single bitcoin address. Four more swaps covering 400 ETH were still pending. The orders came in between about 03:55 and 06:23 UTC, mostly in batches of around 100 ETH, roughly $265,000 a pop. The Ethereum wallet was flagged by blockchain tracker Lookonchain as part of the attacker's activity.

## The context

Bitget lost about $388 million in a breach on September 24. The exchange asked THORChain to block the publicly identified attacker addresses and put up a 5 percent bounty for freezing or recovering the stolen funds. THORChain said no. Its position: emergency controls can halt broader network activity, but the protocol cannot freeze an individual address or transaction.

## Why this matters

This is the decentralization promise meeting its least flattering use case. THORChain lets anyone swap assets across chains without an account, without a centralized exchange that could say no. Stolen ETH goes in, clean-ish BTC comes out the other side. No compliance desk in the middle.

I keep coming back to the tension here. Bitget's request is reasonable from a victim's standpoint. You lose $388 million, you want every door shut. But a protocol that can freeze one address on request can freeze any address on request, and that is exactly the property THORChain's users are paying to avoid. Selective blacklisting is just blacklisting with extra steps.

The one silver lining for investigators: the swaps are all publicly visible. The funds moved, but they moved in the open. Following 75.2 BTC across the bitcoin network is tedious, not impossible. Whether that trail leads anywhere before the coins get mixed, peeled, or parked is another question.

Nobody knows how this plays out. What we know is that $6.3 million of the haul is now bitcoin, sitting at one address, and the protocol that moved it has no intention of moving it back.

## Sources

- [CoinDesk: THORChain rejects Bitget request to block hacker as $6 million moves to bitcoin](https://www.coindesk.com/tech/2026/09/28/thorchain-rejects-bitget-request-to-block-hacker-as-usd6-million-moves-to-bitcoin)
