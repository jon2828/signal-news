---
title: Arbitrum's council rewrote a contract to move $30 million from the Binance hacker's address
date: 2026-11-03
topic: bitcoin
story: arbitrum-hack-funds
score: 8
candidate_id: f85746de9c57932a
sources: ["https://www.coindesk.com/tech/2026/11/03/arbitrum-s-council-moved-usd30-million-of-binance-hack-funds-without-the-hacker-s-key"]
triage_reason: "Reveals a controversial and unprecedented governance action by Arbitrum to move hack funds, raising serious security and centralization concerns."
---

Arbitrum's Security Council moved about $30 million out of an address tied to the Binance exploit last Friday, and it did it without the hacker's signature, [CoinDesk reports](https://www.coindesk.com/tech/2026/11/03/arbitrum-s-council-moved-usd30-million-of-binance-hack-funds-without-the-hacker-s-key). No private key, no approval from the wallet's owner. Nine people agreed, and the money moved.

The haul was more than 8,425 ETH and 74 million ARB. Real money, though a rounding error next to the roughly $6.3 billion taken from Binance in the original hack.

## How they did it

The mechanics are worth understanding, because they are the whole story.

Arbitrum runs on top of Ethereum to make transactions cheaper, and it holds billions of dollars in user deposits. Its Security Council is a 12-member group elected by ARB token holders, with emergency powers to upgrade the network's contracts if nine members sign off.

On Friday the council's shared wallet sent a single Ethereum transaction that temporarily swapped out the code of the Inbox, the contract that carries messages from Ethereum into Arbitrum. The replacement code added a function called `_sendUnsignedTransactionOverride_`, which let the council send transactions that Arbitrum treated as coming from the exploiter's address. The council moved the funds, then put the original code back.

Read that again. The network's rules were rewritten once, for one purpose, by a committee, then restored. Everything worked as designed. That is the part I keep coming back to.

## Where the money sits now

The recovered assets are in a holding address. They can move again only through an ArbitrumDAO governance vote, and that process has a track record: a similar recovery in April ran into legal delays. This is the second time this year the council has used these powers.

The hacker no longer controls the funds, but nobody else really does either. Getting the money out of the attacker's wallet turned out to be the easy, technical part. Getting it back to wherever it is supposed to go is a governance and legal problem, and those move slowly.

## The uncomfortable part

I want to be fair here. Recovering stolen funds is good. Most ARB holders will read this and shrug, because the council used its powers against a thief, in the open, with everything on chain for anyone to inspect.

But the power itself does not care who the target is. The entire pitch of a blockchain is that funds move only when the private key signs. Friday demonstrated, on a live network holding billions in deposits, that nine of twelve people can rewrite a core contract and spend from any address. Today that address belonged to a hacker. The mechanism would work identically on yours.

This is not a hidden backdoor. The council is elected, the nine-of-twelve threshold is public, and the transaction is right there on chain. Plenty of networks would kill for that kind of transparency. Still, if your mental model of Arbitrum is "Ethereum with cheaper fees," update it. It is Ethereum with cheaper fees and a twelve-person override switch.

How the DAO vote goes, and whether the legal delays from April repeat, nobody knows yet.

## Sources

- [Arbitrum's council moved $30 million of Binance hack funds without the hacker's key (CoinDesk)](https://www.coindesk.com/tech/2026/11/03/arbitrum-s-council-moved-usd30-million-of-binance-hack-funds-without-the-hacker-s-key)
