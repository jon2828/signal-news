---
title: Lighter returns $5 million after API key leak, but the full loss may be much bigger
date: 2026-11-17
topic: bitcoin
story: lighter-security-breach
score: 7
candidate_id: e192c503efb17e30
sources: ["https://www.theblock.co/news/defi/2026-11-17-lighter-reopens-withdrawals-after-traders-api-key-leak-returns-about-5-million-in-usdc-442113"]
triage_reason: "Security incident with a named exchange and specific financial impact ($5M), relevant to Bitcoin/crypto security readers."
---

# Lighter returns $5 million after API‑key leak; total loss may be larger

**Date:** 2026‑11‑17

Lighter announced that withdrawals have been reopened and that approximately $5 million in USDC has been returned to a trader whose API keys were compromised on Monday, according to the exchange's post‑mortem reported by *The Block*.

The Ethereum‑based perpetual futures platform initially reported a suspected compromise involving an external party and suspended withdrawals and pool creation as a precaution. Investigation later identified a leaked API key linked to a single trader's account. The incident triggered Lighter's smart‑contract Guardian, which temporarily paused withdrawals and allowed the Security Council to recover the funds. The exchange later stated:

> "Deposits and withdrawals are back to normal following the deactivation of Guardian Mode by the Lighter Security Council."

---

## Attack methodology

Lighter's post‑mortem describes the following steps:
1. The attacker opened a public pool using the compromised account.
2. From a separate account under the attacker's control, they minted shares in that pool.
3. The attacker transferred the trader's funds into the pool without minting additional shares, thereby increasing the value of the shares they already held.
4. The attacker redeemed those shares and withdrew the proceeds.

The API‑key leak resulted from the trader signing transactions with software outside Lighter's official SDKs. The software reused nonces, one‑time values required for each signature. When two public signatures are generated with the same nonce and key, the private key can be derived, allowing an attacker to sign transactions on the trader's behalf.

Lighter confirmed that its official SDKs, protocol, smart contracts, and infrastructure were not affected by the breach.

---

## Estimated total loss

Lighter did not disclose the overall amount stolen or the identity of the affected trader. On‑chain analysts Lookonchain and Onchain Lens estimated the loss at roughly $15.5 million and suggested that the compromised account may belong to Abraxas Capital.

If the analysts' estimate is accurate, the $5 million that has been returned represents about one‑third of the total loss.

---

## Mitigations introduced

Following the incident, Lighter implemented several security changes:
- An API key alone can no longer authorize a transfer to a public pool; a wallet signature is now required.
- API‑key signatures are no longer public.
- IP allow‑lists and per‑key permissions have been added, including market‑specific restrictions.

These measures are intended to prevent a similar exploitation of API keys in the future.

---

## Sources

- [The Block: Lighter reopens withdrawals after trader's API‑key leak, returns about $5 million in USDC](https://www.theblock.co/news/defi/2026-11-17-lighter-reopens-withdrawals-after-traders-api-key-leak-returns-about-5-million-in-usdc-442113)
