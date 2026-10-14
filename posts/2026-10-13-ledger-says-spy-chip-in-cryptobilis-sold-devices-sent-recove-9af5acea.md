---
title: Ledger says spy chip in CryptoBilis-sold devices sent recovery phrases over LTE
date: 2026-10-13
topic: bitcoin
score: 8
candidate_id: 9af5acea5c334ce7
sources: ["https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network"]
triage_reason: "Confirmed spy chip transmitting wallet keys is a major security breach with a named company, corroborated by retailer pullout coverage elsewhere."
---

# Ledger says spy chip in CryptoBilis‑sold devices sent recovery phrases over LTE

**Date:** October 13, 2026

Ledger says a covert chip implanted in some of its hardware wallets sold by Southeast Asian reseller **CryptoBilis** read users' 24‑word recovery phrases from the device screen and transmitted them to an attacker over a mobile phone network.

The company laid out the mechanism in an investigation update on X on Tuesday, per CoinDesk. When a user set up the device and the screen displayed the recovery phrase, the implant's microcontroller recognized and decoded the words, then sent them out over LTE using an eSIM. The chip sat inside the device enclosure.

This is the first public explanation of how the CryptoBilis‑linked thefts actually worked. The recovery phrase is the master key to a wallet; anyone who has it can recreate the wallet anywhere and move the funds without needing the physical Ledger device.

## What the chip did **not** touch

Ledger's account is clear on one point: the implant did **not** modify the Secure Element, the chip designed to protect private keys, and it did **not** alter the operating system, transactions, or signatures. The company is calling this a physical supply‑chain attack, not a breach of its software or internal systems.

## How it surfaced

Ledger also announced that retailer **MediaMarkt Saturn** stopped selling the devices after a customer in Germany reported a "spy" implant in a signer. Ledger said the investigation will continue until it determines who tampered with the devices.

Its advice to CryptoBilis customers is straightforward:

* **Do not** initialize unused devices.
* If you have already used one, transfer your assets to a new device with a freshly generated recovery phrase.

## The uncomfortable part

Hardware wallets are sold on a simple promise: your keys never touch an internet‑connected machine. This attack didn't break that promise; it simply bypassed it by reading the recovery phrase the moment it appeared on the screen. An implant with LTE and an eSIM is far from a garage‑level hack, someone invested real money and effort to get modified devices into a reseller's stock.

## What we still don't know

Ledger has not disclosed where in the supply chain the tampering occurred, how many devices are affected, or who is behind it. Public reporting so far provides no concrete numbers on the thefts.

If you bought a Ledger from CryptoBilis, the remedy is simple: obtain a new device, generate a fresh recovery phrase, and move your funds.

---

**Sources**

- [CoinDesk: Ledger says 'spy' chip inside CryptoBilis Ledger devices transmitted wallet keys over mobile network](https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network)
