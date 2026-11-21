---
title: Judge acquits MIT brothers in $25 million Ethereum MEV case
date: 2026-11-18
topic: bitcoin
story: mit-brothers-acquittal
score: 8
candidate_id: 020a15a1edf23116
sources: ["https://www.coindesk.com/policy/2026/11/18/u-s-judge-says-ethereum-has-no-terms-of-use-clears-mit-brothers-of-usd25-million-fraud"]
triage_reason: "Federal acquittal in the first criminal MEV prosecution sets a meaningful legal precedent with named parties and a clear ruling."
---

A federal judge in Manhattan has acquitted Anton and James Peraire-Bueno, the MIT-educated brothers prosecutors accused of pulling $25 million out of Ethereum trading bots in 12 seconds, ruling that outsmarting bots on a blockchain is not wire fraud.

U.S. District Judge Jessica Clarke granted the judgment of acquittal on Nov. 16, throwing out charges of wire fraud, conspiracy to commit wire fraud, and conspiracy to commit money laundering, [CoinDesk reports](https://www.coindesk.com/policy/2026/11/18/u-s-judge-says-ethereum-has-no-terms-of-use-clears-mit-brothers-of-usd25-million-fraud). The ruling ends the U.S. government's first criminal case over MEV, and it directs the court clerk to close the case. It comes a year after a jury deadlocked and Clarke declared a mistrial in November 2025.

The line in her opinion that will get quoted for years is about Ethereum itself: "It is a trustless, highly adversarial environment with no terms of use."

## How the trade worked

Pending Ethereum transactions sit in a public queue called the mempool until a validator, the network participant chosen to add the next block, includes them. Trading bots watch that queue for maximal extractable value, or MEV, the profit available to whoever controls the sequence of transactions in a block.

The brothers' 2023 trade baited those bots and exploited a flaw in relay software to reorder transactions. The bots lost about $25 million. The brothers walked away with it.

## Why the fraud theory failed

Wire fraud requires a material misrepresentation, a lie that someone relied on. Clarke ruled prosecutors never established one. The trade involved no lie that anyone relied on, and her opinion stressed that objectionable conduct is not necessarily criminal.

That distinction matters beyond this case. Fraud law was built for a world of promises and counterparties. Ethereum's mempool offers neither. The bots that lost money were autonomous programs hunting the same edge the brothers found, inside a system whose whole pitch is that you never have to trust anyone in it.

## My take

I keep coming back to "no terms of use." Every other corner of finance runs on the opposite assumption: rules exist, written or not, and stepping far enough outside them gets you indicted. Clarke looked at Ethereum and concluded the network makes no such promise, so breaking an unwritten rule is not fraud. The code-is-law crowd will treat this as total vindication, and honestly, the logic is hard to argue with.

And yet $25 million left other people's positions in 12 seconds, taken from bots the brothers deliberately baited. If that sits wrong with you, the court's answer is that the fix is better bot design, not a prosecutor. Maybe that is correct for a network built to be adversarial. It also means the mempool stays a knife fight, and everyone now knows the courts will not break it up.

This was the government's first swing at criminalizing MEV, and it missed on the facts of the network itself. Whether prosecutors adjust their theory next time, nobody knows. Any future case starts from Clarke's premise: Ethereum has no terms of use, and trading against it as designed is not a lie.

## Sources

- [CoinDesk: U.S. judge says Ethereum has 'no terms of use,' clears MIT brothers of $25 million fraud](https://www.coindesk.com/policy/2026/11/18/u-s-judge-says-ethereum-has-no-terms-of-use-clears-mit-brothers-of-usd25-million-fraud)
