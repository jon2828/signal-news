---
title: Electrum bug let rogue servers steal bitcoin when users bumped fees
date: 2026-10-26
topic: bitcoin
score: 7
candidate_id: 128bbb42a21b9700
sources: ["https://www.coindesk.com/tech/2026/10/26/bitcoin-wallet-bug-let-rogue-servers-steal-funds-when-users-tried-to-speed-up-payments"]
triage_reason: "Concrete wallet security flaw with real losses and a developer patch is a publishable security story."
---

A bug in Electrum, one of Bitcoin's oldest software wallets, let malicious servers trick users into signing payments straight to attackers, and at least one person lost bitcoin before developers shipped a fix, CoinDesk reported.

Electrum disclosed the vulnerability on Saturday and said some servers were already exploiting it. The team received two reports in October, including one from a user who lost funds after approving what looked like a routine transaction‑fee increase.

## How the attack worked

Electrum is a light wallet. It doesn't run a full Bitcoin node, so it relies on outside servers to fetch transaction history and broadcast payments. Before the patch, the wallet trusted those servers to report pending transactions without verifying their signatures.

That trust was the opening. An attacker running a server could intercept a payment before it reached the network and swap a fake transaction into the wallet's history. The fake spent the user's coins to an attacker‑controlled address, carrying invalid signatures that Electrum didn't check.

The wallet then showed the fake payment as pending. When the user tried to speed it up with Replace‑by‑Fee, Bitcoin's mechanism for rebroadcasting a stuck transaction with a higher fee, Electrum signed a valid replacement of the fraudulent transaction. The coins went to the attacker, signed by the victim's own keys.

In one reported case the malicious transaction carried no fee at all, so it looked stuck and practically begged for a fee bump. Attackers also generated receiving addresses whose last four characters matched the legitimate destination, making the substitution harder to spot during a quick check. Many users verify an address by its tail, which the attackers exploited.

## Two reports, one confirmed theft

The first report came in on Oct. 11 from a user with a two‑of‑three multisignature wallet backed by two Trezor hardware devices. They had verified the legitimate payment on both devices, then later noticed a different outgoing transaction in their history. That user did not report losing funds.

The second report, on Oct. 18, came from a user who raised the fee on a substituted transaction and lost money. Developers haven't disclosed the amount stolen or identified the malicious servers.

## The fix

Electrum released version 4.8.3 on Oct. 24, six days after the reported theft. It adds signature checks for unconfirmed transactions that spend coins from the user's own wallet. Earlier versions remain vulnerable when connected to a malicious server, so upgrading is essential. Users who only connect to servers they trust, including their own, were never exposed.

The developers' advice beyond upgrading: check receiving addresses and amounts before signing. Given the address‑matching trick, it's safest to verify the entire address, not just the last four characters.

The episode underscores the trade‑off of light wallets. They exist because running a full node is a hassle, but that convenience can expose users to server‑side attacks. Even hardware‑wallet users can be affected when the software they rely on presents a forged transaction.

## Sources

- [CoinDesk: Bitcoin wallet bug let rogue servers steal funds when users tried to speed up payments](https://www.coindesk.com/tech/2026/10/26/bitcoin-wallet-bug-let-rogue-servers-steal-funds-when-users-tried-to-speed-up-payments)
