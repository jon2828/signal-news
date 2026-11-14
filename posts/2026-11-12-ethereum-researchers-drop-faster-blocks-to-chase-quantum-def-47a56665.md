---
title: Ethereum researchers drop faster blocks to chase quantum defenses in 2027
date: 2026-11-12
topic: bitcoin
story: ethereum-quantum-defense
score: 7
candidate_id: 47a5666574edc89e
sources: ["https://www.coindesk.com/tech/2026/11/12/ethereum-researchers-drop-faster-blocks-to-race-toward-quantum-defenses-in-2027"]
triage_reason: "A concrete protocol research direction toward quantum-resistant accounts is an important infrastructure development."
---

Ethereum research group Ethlabs has withdrawn its own faster-block proposal from the planned 2027 Hegotá upgrade, urging core developers to push other features aside and lock in post-quantum security a year ahead of schedule, [CoinDesk reports](https://www.coindesk.com/tech/2026/11/12/ethereum-researchers-drop-faster-blocks-to-race-toward-quantum-defenses-in-2027).

## What Ethlabs is proposing

The group made the call in a Wednesday post on Ethereum Magicians, a forum for protocol improvement discussions. Instead of faster block times, Ethlabs wants Hegotá to prioritize Frame Transactions, a feature that would support quantum-resistant signatures. The current target for that work is 2028. Ethlabs wants 2027, shaving 12 months off the timeline.

Nothing is decided yet. The schedule overhaul remains a proposal and has not been adopted into Ethereum's roadmap.

The vulnerability at stake is basic. Ethereum wallets use private keys to sign transactions, and the public version of the key is readable in the blockchain record. A sufficiently powerful quantum computer could, in theory, work backward from the public key to the secret one and drain the account. That exposure covers anyone holding ether, stablecoins, or other tokens on the network.

The Ethereum Foundation's quantum research team says such a machine is "not imminent." But replacing the cryptography behind wallets, apps, and validator nodes takes years, which is the whole argument for starting now.

## The timeline is murky

One thing worth flagging: the dates in CoinDesk's report do not perfectly line up. The piece cites a current 2028 target for quantum defenses, and separately notes the foundation's protocol team set a December 2029 target in September. How those two figures relate is not spelled out. What Ethlabs is really asking for is a year shaved off whatever the real schedule is, and a public signal that quantum resistance outranks performance tweaks.

## The catch for holders

Even if Hegotá ships with Frame Transactions, nobody gets protected automatically. Wallet providers would need to update their software, and holders would need to switch signing methods themselves.

That last part is the real story. Getting millions of people to change how they sign transactions is a social problem, not a technical one. A quantum-resistant account type that nobody migrates to protects no one, and crypto's user base is not famous for moving quickly on opt-in security changes.

## My take

I keep coming back to the trade itself. Faster blocks are something users would feel immediately. Quantum resistance is insurance against a machine that does not exist yet and may not for years. Ethlabs looked at that exchange and picked the insurance. I think that is right, and it says something about how seriously the research crowd takes the tail risk, even when the foundation's own quantum team calls the threat distant.

The cost of being early is a slower roadmap for a year. The cost of being late is every exposed wallet on the chain. That math is not close. Whether holders actually switch signing methods once the option exists is a different question, and nobody knows how that plays out.

## Sources

- [CoinDesk: Ethereum researchers drop faster blocks to race toward quantum defenses in 2027](https://www.coindesk.com/tech/2026/11/12/ethereum-researchers-drop-faster-blocks-to-race-toward-quantum-defenses-in-2027)
