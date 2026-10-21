---
title: Solana's Alpenglow goes live Wednesday with a 150-millisecond finality target
date: 2026-10-21
topic: bitcoin
score: 8
candidate_id: d08f987d6839db67
sources: ["https://www.coindesk.com/tech/2026/10/21/solana-s-alpenglow-its-biggest-network-overhaul-since-2020-goes-live-wednesday"]
triage_reason: "Solana's Alpenglow upgrade is a major protocol change targeting 150ms finality, representing a significant infrastructure shift for a top-tier L1."
---

Solana switches on its Alpenglow upgrade Wednesday, the biggest overhaul of how the network reaches agreement since 2020, and the headline number is hard to argue with: transaction finality of roughly 150 milliseconds, down from about six seconds today.

## What actually changes

Right now, every Solana validator writes its votes directly onto the blockchain, and a transaction is not locked in until enough of those votes pile up. That takes around six seconds. Alpenglow pulls voting off-chain and bundles votes into certificates that can settle a transaction in one or two rounds. If the target holds on mainnet, a payment becomes irreversible faster than a blink.

Six seconds was already quick. For comparison, Ethereum takes roughly 13 minutes to reach full finality. But 150 milliseconds is a different category of fast, the kind that makes a trade or a payment feel like it happened on a centralized exchange. That is presumably the point.

## Validators get a cheaper bill

The economics shift too. Validators currently burn about 2 SOL a day on vote fees, a cost that doubled after Solana cut slot times to around 200 milliseconds. Alpenglow scraps those fees for a flat charge called a validator admission ticket: 0.8 SOL per epoch, a period of about 24 hours. That works out to roughly 60% cheaper.

The timing matters, because Solana's validator set is shrinking. Active validators fell to 659 at the end of September, down from 696 three months earlier and about 30% below a year ago, according to Bitwise's latest staking report. Bitwise points to operating costs. Lower fees could keep smaller operators in the game, though hardware, bandwidth and hosting bills remain.

## The part I keep coming back to

Stake is concentrating while the network gets faster. Data from Solana Compass shows the smallest group of validators controlling more than a third of staked SOL fell to 18 from 20 over the past year, and the ten largest validators now hold 24.5% of stake, up from 22.2%. With 69% of SOL's supply staked, that concentration covers most of the network's weight.

Faster finality does not fix any of that. The fee cut pushes in the right direction for small operators, but if the performance bar keeps rising, the validators with the best hardware and the best location keep pulling ahead. I don't know which force wins, and I don't think anyone else does either.

The road here was not clean, either. The test network was wiped and restarted six times since early May, and one migration attempt failed network-wide and had to be rolled back, according to Galaxy Digital, one of roughly 100 validator operators on the testnet. A later migration went through. None of it put real money at risk, which is what testnets are for, but six restarts and a failed migration tell you this is not a simple thing to do to a live network.

Expect one weird side effect this week: Solana's transaction count will drop, because validator votes were most of what got counted and those are off-chain now. Robin Nordnes, CEO of Raiku, which builds trading infrastructure on Solana, put it plainly: "Most of what got counted before was validators voting, and that's off-chain now. The trading's all still there."

His second point is the one worth sitting with. "For desks, faster finality is nice, but it was never the bottleneck. Being close to where the block is built still is." The headline is speed. The edge, according to someone who builds the trading plumbing, is still location.

The switch flips at the start of epoch 1064, at slot 459,653,000, after a 5,000-slot transition. Whether 150 milliseconds holds up under real mainnet load is the actual test, and nobody knows the answer until Wednesday.

## Sources

- [CoinDesk: Solana's Alpenglow, its biggest network overhaul since 2020, goes live Wednesday](https://www.coindesk.com/tech/2026/10/21/solana-s-alpenglow-its-biggest-network-overhaul-since-2020-goes-live-wednesday)
