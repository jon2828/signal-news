---
title: Keystone is destroying 18,835 unsold wallets after a breach leaked its authenticity key
date: 2026-10-27
topic: bitcoin
score: 7
candidate_id: b1b914e55cbbb869
sources: ["https://www.coindesk.com/business/2026/10/27/crypto-wallet-maker-keystone-to-destroy-almost-19-000-devices-after-security-breach"]
triage_reason: "Significant security breach at a major hardware wallet vendor with specific details on data exposure and policy failures."
---

# Keystone is destroying 18,835 unsold wallets after a breach leaked its authenticity key

**Date:** 2026-10-27

Keystone is destroying 18,835 unsold hardware wallets and suspending shipments after a breach of its website exposed customer data and, worse, a key that lets counterfeit devices pass the company's authenticity checks.

---

## What happened

An attacker got into Keystone's website on Oct. 20 through a flaw in a third‑party data‑monitoring tool, the company said in a post on X, per CoinDesk. The breach exposed **25,964 buyer records** from 2024 through 2026, including names, contact details, shipping addresses and order information. Another **12,873 unpaid checkout records** may also have been affected.

The customer data is bad. The key is worse. Keystone builds an authentication key into its devices during production, and it cannot be changed afterward. Whoever holds that key can make a fake wallet pass Keystone's online authenticity checks and look genuine. That creates a direct risk to users' funds, which is why nearly 19,000 unsold units are being destroyed rather than shipped.

Keystone says the breach did **not** expose recovery phrases, private keys or wallet credentials. Devices delivered before Oct. 20 remain safe to use if they pass authentication, and the company says users do **not** need to move funds because of the breach alone. It also warned users about fake recall or asset‑migration messages.

---

## The quieter failure

The detail I keep coming back to is not the key. It is the deletion tool. Some of the exposed records should have been erased under Keystone's 180‑day retention policy, but an automated deletion tool failed and nobody at the company noticed. As Keystone wrote:

> "We failed to fulfill our commitment to erase customer data on time, and we accept responsibility for this failure."

Credit for the plain apology. This is the second time in two days that a hardware‑wallet company has lost data it was not supposed to still have. **Foundation** disclosed its own breach a day before Keystone's update. Attackers sent more than **23,000 phishing emails** that appeared to come from Foundation's official domains. Foundation found no evidence that Passport devices or private keys were compromised, but it did find older database copies that its 60‑day deletion process had missed, containing about **5,600 mailing addresses** and **5,200 phone numbers**.

Both companies had retention policies, and both had automated processes that failed to carry them out. This highlights that deletion policies are only effective when the enforcement mechanisms are reliably monitored.

---

## The bigger pattern

CoinDesk notes that criminals fitted Ledger devices sold through resellers in Southeast Asia with hidden components that captured recovery phrases during setup. A flaw in Coldcard's seed‑generation software let attackers reconstruct private keys and drain wallets remotely. Keystone's authenticity key is now out in the wild, and Foundation's customers are getting phished from addresses that look official.

The common thread is that none of these attacks broke the underlying cryptography; they targeted the supply chain, websites, resellers, or customer databases. Many analysts consider the device itself a hard target, leading attackers to focus on those peripheral components.

Keystone says it will replace the authentication key in new devices, shift website sales to pre‑orders and cut customer data retention from 180 days to **90 days**. Destroying the unsold stock is expensive, and it appears to be the prudent response. The effectiveness of the remaining fixes will depend on internal monitoring, which is not publicly verifiable.

---

## Sources

- [CoinDesk: Crypto wallet maker Keystone to destroy almost 19,000 devices after security breach](https://www.coindesk.com/business/2026/10/27/crypto-wallet-maker-keystone-to-destroy-almost-19-000-devices-after-security-breach)
