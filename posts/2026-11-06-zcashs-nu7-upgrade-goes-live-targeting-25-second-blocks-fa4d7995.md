---
title: Zcash's NU7 upgrade goes live, targeting 25-second blocks
date: 2026-11-06
topic: bitcoin
story: zcash-nu7-upgrade
score: 10
candidate_id: fa4d7995ada11919
sources: ["https://www.coindesk.com/tech/2026/11/06/zcash-s-landmark-nu7-upgrade-goes-live-speeding-up-private-payments"]
triage_reason: "Zcash implements the NU7 upgrade, significantly speeding up private payments and reducing work."
---

Zcash activated its NU7 upgrade early Friday, cutting the target time between blocks from 75 seconds to 25 and setting up private payments to confirm three times faster, CoinDesk reported.

The upgrade went live at block 3,543,405, mined at 02:34 UTC. The detail I find more honest than the headline: the network is not actually hitting 25 seconds yet. By 04:59 UTC, Zcash had produced another 225 blocks at an average of about 39 seconds apart, according to ZecStats data cited by CoinDesk. Mining difficulty was still adjusting to the faster pace. That is normal for a block-time change, but it is worth saying out loud before anyone promises merchants instant private payments.

## What faster blocks actually buy you

Zcash hides the sender, recipient and amount on a transaction. That privacy has always come with a usability tax, and slow confirmations were part of it. NU7 takes a real bite out of the tax. A merchant could see a first confirmation in about 25 seconds on average, per CoinDesk. An exchange requiring three confirmations could cut its expected wait from nearly four minutes to about 75 seconds.

There is a catch, and CoinDesk flags it: each service sets its own confirmation requirements. If your exchange wants ten confirmations, your wait is whatever that works out to. The protocol sets the floor, not the ceiling.

## The wallet problem

The upgrade does more than change the clock. NU7 limits private transaction activity per block, which cuts how much data wallets must download to find their payments. That is the unglamorous part of privacy tech that decides whether normal people can use it. A wallet that takes forever to sync is a wallet nobody opens.

The tradeoff is a cap on per-block private activity, but CoinDesk reports the change could still more than double capacity for simple private payments, to over six per second. Six per second is not Visa. For a privacy chain, it is a real step.

## Fees and a quiet burn

Two more changes deserve attention. NU7 redirects 60 percent of transaction fees toward future mining rewards, setting aside fee income for the miners who will keep the chain running down the road. And the upgrade retires Sprout, Zcash's original privacy pool.

That retirement has a cost. About 12,224 ZEC still sitting in Sprout becomes unspendable, and no recovery plan has been approved. I keep coming back to that number. Upgrades usually get sold as pure progress. This one ships with a small, permanent graveyard attached, and nobody seems too bothered about it.

## My read

This is a solid, workmanlike upgrade. Faster blocks and lighter wallets, plus a fee change that pays miners into the future. Nothing flashy, all useful. The gap between the 25-second target and the 39-second reality will probably close as difficulty adjusts, but I will believe the marketing when the chain holds that pace for a week.

The Sprout burn is the part that lingers. Over twelve thousand coins, locked by design, with no agreed way back. Maybe that is fine. Maybe some of those keys were lost long ago. But it is a reminder that every big upgrade writes something off, and it is worth asking who got written off this time.

## Sources

- [CoinDesk: Zcash's landmark NU7 upgrade goes live, speeding up private payments](https://www.coindesk.com/tech/2026/11/06/zcash-s-landmark-nu7-upgrade-goes-live-speeding-up-private-payments)
