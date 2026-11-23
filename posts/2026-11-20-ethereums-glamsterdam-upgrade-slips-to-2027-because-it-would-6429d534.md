---
title: Ethereum's Glamsterdam upgrade slips to 2027 because it would break thousands of apps
date: 2026-11-20
topic: bitcoin
story: ethereum-glamsterdam-delay
score: 8
candidate_id: 6429d534ac2dde1f
sources: ["https://www.coindesk.com/tech/2026/11/20/ethereum-s-next-big-upgrade-is-pushed-into-2027-by-apps-it-would-break"]
triage_reason: "Protocol upgrade delay to 2027 is a major infrastructure change affecting Ethereum's roadmap and developer expectations."
---

Ethereum's next big upgrade, Glamsterdam, will not go live before mid-January at the earliest, and the reason is simple: in its current form it would break a lot of software already running on the network.

The upgrade was originally targeted for December. Now, [CoinDesk reports](https://www.coindesk.com/tech/2026/11/20/ethereum-s-next-big-upgrade-is-pushed-into-2027-by-apps-it-would-break), core developers say late January or early February is the realistic window. At their weekly meeting, which CoinDesk attended, the Ethereum Foundation and outside security researchers said they had contacted more than 50 companies whose apps would be affected. Most of those companies said they could patch their code by mid-January, as long as the upgrade's rules stay as written.

## What Glamsterdam changes

The point of the upgrade is capacity. Glamsterdam is meant to let Ethereum handle more activity at once, so existing apps like onchain trading platforms and lending services can scale their features.

The problem sits in one specific change. The base charge for deploying a new smart contract would rise from 32,000 to 183,600 units of gas, Ethereum's measure of computing work, with separate charges for storing the code on top. That is close to six times the current cost. An Ethereum Foundation developer estimates as many as 15,000 programs could fail under the new rules.

## My take

I keep coming back to that 15,000 number. This is not an edge case. It is a meaningful chunk of the ecosystem waking up to find that the ground under their contracts is about to move.

To the developers' credit, they seem to be handling it the right way. They contacted affected companies directly instead of just shipping and letting things break. A tentative test is scheduled for the week of Dec. 14, and app fixes are due by mid-December or Jan. 10, depending on urgency. Most core software teams want to keep the proposed rules rather than water them down, which tells you they think the capacity gains are worth the pain.

Still, there is a real tension here. Ethereum is asking thousands of teams to spend the next several weeks patching code so the base layer can change its pricing. Some of those contracts belong to small teams. Some might be unmaintained entirely, and the reporting does not say what happens to a program nobody is left to fix. I do not know either.

This is the part of permissionless infrastructure that gets glossed over. The chain itself may be neutral, but upgrades like this create a soft coordination requirement. If you built on Ethereum, you now have homework, assigned by people you did not choose, on a timeline you did not set.

That is not an argument against the upgrade. Raising capacity matters, and repricing gas is a legitimate tool for doing it. It is a reminder that "immutable" infrastructure rests on a very mutable set of assumptions, and every so often the bill comes due.

If the fixes land on time, late January looks realistic. If they do not, this slips again, and nobody should be surprised.

## Sources

- [CoinDesk: Ethereum's next big upgrade is pushed into 2027 by apps it would break](https://www.coindesk.com/tech/2026/11/20/ethereum-s-next-big-upgrade-is-pushed-into-2027-by-apps-it-would-break)
