---
title: BTCPay Server tells users to shut down after reports of drained wallets
date: 2026-11-02
topic: bitcoin
story: btcpay-security-breach
score: 8
candidate_id: a52597637b4f2169
sources: ["https://www.coindesk.com/tech/2026/11/02/btcpay-a-bitcoin-payment-tool-tells-users-to-switch-off-their-servers-after-reports-of-drained-wallets"]
triage_reason: "Major security breach affecting a widely used open-source Bitcoin payment tool."
---

# BTCPay Server tells users to shut down after reports of drained wallets

*Date: November 1, 2026*  
*Source: [CoinDesk](https://www.coindesk.com/tech/2026/11/02/btcpay-a-bitcoin-payment-tool-tells-users-to-switch-off-their-servers-after-reports-of-drained-wallets)*

BTCPay Server, the free open‑source tool that enables businesses to accept Bitcoin without a custodial intermediary, issued an urgent advisory on Sunday urging operators to shut down their servers.

The warning follows reports that attackers have been draining "hot wallets" on some installations. The project is still investigating; it has not disclosed any loss figures nor announced a fix. According to BTCPay's founder, the incidents appear to involve versions older than 2.4.2, but investigators have not determined how the attackers obtained administrator access, nor have they confirmed that newer releases are safe.

## Why hot wallets are a risk

BTCPay's model relies on self‑custody: merchants run the software on their own servers and receive payments directly into wallets they control. In a hot‑wallet configuration the seed phrase, the secret needed to sign transactions, is stored on the server, which remains online continuously. The BTCPay documentation states that the server will *"automatically use the seed stored on a server to sign"* transactions. This convenience means that anyone who compromises the server can move funds without additional merchant approval.

The documentation flags this capability with a **DANGER** label and warns that it *"comes with security implications."* The advisory therefore emphasizes that a compromised hot wallet can lead to immediate loss of funds.

## Decentralized deployment adds complexity

Because each merchant hosts their own instance, there is no central operator that can push a patch to every deployment instantly. When a vulnerability is discovered, the response relies on public alerts and the ability of individual administrators to act quickly.

## Unknowns

- **Attack vector:** Still under investigation.
- **Total losses:** Not disclosed.
- **Safety of newer versions:** Not yet confirmed.

**Recommendation:** Operators of BTCPay Server should shut down their instances until the project provides further guidance.

---

**Sources**

- [CoinDesk: BTCPay, a bitcoin payment tool, tells users to switch off their servers after reports of drained wallets](https://www.coindesk.com/tech/2026/11/02/btcpay-a-bitcoin-payment-tool-tells-users-to-switch-off-their-servers-after-reports-of-drained-wallets)
