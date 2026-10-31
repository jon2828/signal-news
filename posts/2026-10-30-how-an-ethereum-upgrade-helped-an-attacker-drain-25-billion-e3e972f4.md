---
title: How an Ethereum upgrade helped an attacker drain $2.5 billion from Binance
date: 2026-10-30
topic: bitcoin
score: 7
candidate_id: e3e972f430cf9f17
sources: ["https://www.coindesk.com/tech/2026/10/30/here-s-how-one-ethereum-permission-let-an-attacker-drain-usd2-5-billion-from-binance"]
triage_reason: "Adds genuinely new facts on the hack mechanism via an Ethereum upgrade, a material development beyond the initial breach report."
---

# How an Ethereum upgrade helped an attacker drain $2.5 billion from Binance

**Date:** 2026‑10‑30

Binance says an attacker stole roughly **$6.3 billion** from its wallets across several blockchains on Thursday. The largest single chunk - about **$2.5 billion** in ether and tokens - left one Ethereum wallet in under four minutes. According to CoinDesk's reconstruction of the on‑chain data, the attack was enabled by a newly‑added Ethereum feature, **EIP‑7702**.

---

## What is EIP‑7702?

EIP‑7702, which went live in May 2025 as part of the **Pectra** upgrade, allows an ordinary wallet (controlled by a private key) to **borrow** the code of a smart contract. The wallet signs a short message - an *authorization* - that points to a contract; once the authorization is submitted, the network treats the contract's code as if it were part of the wallet itself. The authorization remains in effect until it is replaced or cancelled on‑chain.

The feature was intended for legitimate use cases such as batching payments or letting a third party pay transaction fees. However, within weeks of launch, market‑maker **Wintermute** observed that many EIP‑7702 delegations referenced copy‑pasted "sweeper" scripts - code that automatically forwards a wallet's funds to an attacker once the wallet's key is compromised.

---

## The attack in detail

* **Funding the attacker's wallet** - The attacker's main wallet (0x7C86…5CA0) received small withdrawals from the mixing service **Tornado Cash** starting Wednesday, as reconstructed by CoinDesk.
* **Rehearsal and deployment** - On Thursday, the attacker rehearsed the attack on their own wallets and, at about **16:00 UTC**, deployed a sweeper contract (0x63e8…6fAe) that could only be operated by the attacker's address.
* **Fifty authorizations** - At **20:20:59 UTC**, a single transaction containing **50 authorizations** was submitted. Each authorization was signed by the wallet labeled "Binance 14" on Etherscan and pointed to the sweeper contract. Because Binance 14's nonce was rapidly increasing, the attacker prepared authorizations for consecutive nonces **18,914,775 - 18,914,824**. The network accepted the one with nonce **18,914,809** and ignored the remaining 49.
* **First sweep** - At **20:24:23 UTC**, the sweeper was triggered. In that transaction the attacker moved roughly **167,464 ETH** and **63 tokens**, including about **1.6 billion USDT**, to their own address.
* **Continued theft** - Binance's internal systems continued routing customer deposits to Binance 14. The attacker swept additional funds out at **21:04 UTC** and **21:44 UTC**. Using the same borrowed code, the attacker also issued commands to a separate Binance smart wallet, **Hot Wallet 34**, extracting **823 million USDC** (as reported by TRM Labs).
* **Delegation duration** - The malicious delegation remained active for nearly **four hours** before Binance revoked the permission at **00:10:35 UTC** on Friday.

---

## The broader theft

Beyond Ethereum, the attacker moved **18,270 BTC**, hundreds of millions of **XRP**, and funds on **Solana**, **Tron**, and other networks, according to TRM Labs. Those blockchains do not support EIP‑7702, so the transfers were ordinary signed transactions.

All of the on‑chain moves were signed by Binance‑controlled wallets, indicating that the attacker obtained a large number of valid signatures rather than exploiting a single leaked key. How the attacker acquired this authority across multiple blockchains is still under investigation.

---

## Binance's response

Binance's co‑CEO **Richard Teng** said on Friday that preliminary findings point to a **compromised DevOps engineer**. Binance has pledged to cover the full **$6.3 billion** loss.

---

## Takeaway

EIP‑7702 was designed to add flexibility for ordinary wallets, but its early misuse for "sweeper" scripts created a powerful tool for attackers once they obtained the necessary signatures. The incident underscores the importance of protecting signing keys and monitoring delegated permissions.

---

### Sources
- [CoinDesk: Here's how one Ethereum permission let an attacker drain part of Binance's $6 billion loss](https://www.coindesk.com/tech/2026/10/30/here-s-how-one-ethereum-permission-let-an-attacker-drain-usd2-5-billion-from-binance)
