---
title: Ledger says spy chip in CryptoBilis-sold devices sent recovery phrases over LTE
date: 2026-10-13
topic: bitcoin
score: 8
candidate_id: 9af5acea5c334ce7
sources: ["https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network"]
triage_reason: "Confirmed spy chip transmitting wallet keys is a major security breach with a named company, corroborated by retailer pullout coverage elsewhere."
---

Ledger says a covert chip implanted in some of its hardware wallets sold by Southeast Asian reseller CryptoBilis read users' 24-word recovery phrases off the device screen and transmitted them to an attacker over a mobile phone network.

The company laid out the mechanism in an investigation update on X Tuesday, per CoinDesk. When a user set up the device and the screen displayed the recovery phrase, the implant's microcontroller recognized and decoded the words, then sent them out over LTE using an eSIM. The chip sat inside the device enclosure.

This is the first public explanation of how the CryptoBilis-linked thefts actually worked. And it is a nasty one. The recovery phrase is the master key to a wallet. Whoever holds it can recreate the wallet anywhere and move the funds, no physical device required.

## What the chip did not touch

Ledger's account is careful on one point. The implant did not modify the Secure Element, the chip built to protect private keys, and it did not touch the operating system. It did not alter transactions or signatures. The company is calling this a physical supply-chain attack, not a breach of its software or internal systems.

The distinction matters, and I think it is less comforting than Ledger would like. The Secure Element apparently did its job. The attacker just went around it, reading the words at the one moment they appear on the screen during setup. You do not need to break the vault if you can watch the combination being read aloud.

## How it surfaced

Ledger also announced that retailer MediaMarket Saturn stopped selling the devices after a customer in Germany found a corrupted signer. The company says the investigation will continue until it determines who tampered with the devices.

Its advice to CryptoBilis customers is blunt. Do not initialize unused devices. If you already used one, transfer your assets to a new device with a newly generated recovery phrase.

## The uncomfortable part

Hardware wallets are sold on a simple promise: your keys never touch an internet-connected machine. This attack did not break that promise so much as route around it, using hardware sophisticated enough to carry its own cellular radio. An implant with LTE and an eSIM is not a garage operation. Someone spent real money and real effort getting modified devices into a reseller's stock.

What we do not know is the part that matters most. Ledger has not said where in the supply chain the tampering happened, how many devices are affected, or who is behind it. The reporting so far puts no number on the thefts either. Until Ledger answers the where and the who, every third-party seller of hardware wallets carries more suspicion than it did last week.

If you bought a Ledger from CryptoBilis, the move is simple. New device with a fresh recovery phrase, then move your funds. Do it before whoever holds your phrase decides to.

## Sources

- [CoinDesk: Ledger says 'spy' chip inside CryptoBilis Ledger devices transmitted wallet keys over mobile network](https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network)
