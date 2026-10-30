---
title: Quantum model cuts the hardware needed to break bitcoin keys by 17 times
date: 2026-10-29
topic: bitcoin
score: 8
candidate_id: 046f5ffccb1df51e
sources: ["https://www.coindesk.com/tech/2026/10/29/new-quantum-model-slashes-hardware-needed-to-break-bitcoin-keys-by-17-times"]
triage_reason: "A 17x reduction in hardware needed to break bitcoin keys materially advances a credible threat to Bitcoin security and raises urgency for quantum-resi"
---

A machine with about 30,000 physical qubits could break the cryptography protecting bitcoin wallets in just over an hour. That is the new estimate from researchers at quantum computing firm Alice & Bob, [reported by CoinDesk](https://www.coindesk.com/tech/2026/10/29/new-quantum-model-slashes-hardware-needed-to-break-bitcoin-keys-by-17-times).

The number is a jolt because of where estimates stood a few months ago. Google said in March that a future quantum computer would need fewer than 500,000 physical qubits to crack Bitcoin's cryptography, and that was already down from earlier estimates in the millions. Alice & Bob's figure, 29,588 qubits, is roughly 17 times lower than Google's.

Hold the panic, though. The two studies use different hardware designs and assumptions, so this is not a clean comparison. The findings are theoretical, and nobody has built anything close to the machine described. What I find hard to wave off is the direction. Every big estimate of the hardware needed to threaten Bitcoin keeps moving the same way: down.

## Six million coins with their keys half out

The attack Alice & Bob modeled would take about 62 minutes. That is too slow to reliably target a transaction before it confirms, so the day-to-day payment flow is not the soft spot.

The soft spot is old coins. More than six million bitcoins sit at addresses whose public keys are already exposed, per the CoinDesk report. A public key lets the network verify transactions without revealing the private key that authorizes spending. A powerful enough quantum computer could work backwards from the public key, recover the private key, and steal the coins. No race against confirmation times required. With BTC trading around $76,800 when the story ran, six million coins is a target measured in the hundreds of billions of dollars.

I keep coming back to this group of coins. A lot of them are early coins, dormant for years, possibly lost. Their owners may never move them and may never know they should. If a machine like this ever exists, that stash is the buffet line.

## The migration problem

The Alice & Bob researchers urge Bitcoin's developers to start moving to quantum-resistant security now. Their warning: upgrades could take years, while the hardware that matters keeps advancing toward the early 2030s.

That timeline is the whole story for me. Bitcoin changes slowly, and anyone who has watched even minor upgrades grind through years of debate knows a cryptography swap will not be quick. If the hardware estimates keep shrinking at this rate, "we have a decade" stops being a comfort and starts being a schedule.

Nobody knows when a machine like this gets built, or whether Alice & Bob's assumptions hold up better than Google's. What we know is that the estimate was in the millions, then under 500,000, and now 29,588. The coins with exposed keys are not getting any less exposed while the numbers fall.

## Sources

- [CoinDesk: New quantum model slashes hardware needed to break bitcoin keys by 17 times](https://www.coindesk.com/tech/2026/10/29/new-quantum-model-slashes-hardware-needed-to-break-bitcoin-keys-by-17-times)
