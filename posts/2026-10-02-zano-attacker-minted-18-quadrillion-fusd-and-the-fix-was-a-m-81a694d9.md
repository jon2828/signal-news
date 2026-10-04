---
title: Zano attacker minted 1.8 quadrillion fUSD, and the fix was a month-long rollback
date: 2026-10-02
topic: bitcoin
score: 7
candidate_id: 81a694d98b01dd31
sources: ["https://cointelegraph.com/news/zano-exploiter-created-369m-unauthorized-zano-before-blockchain-rollback?utm_source=rss_feed&utm_medium=rss&utm_campaign=rss_partner_inbound"]
triage_reason: "A quadrillion-token mint followed by a blockchain rollback is a major security breach and protocol-level event, though single-source coverage keeps it"
---

# Zano attacker minted 1.8 quadrillion fUSD, and the fix was a month-long rollback

*Date: 2026-10-02*

Zano's attacker created 36.9 million unauthorized ZANO and roughly 1.8 quadrillion Freedom Dollar (fUSD) tokens before the team decided to roll the blockchain back by a full month, according to a post‑mortem published Thursday and reported by Cointelegraph.

The numbers explain the rollback. I had wondered why any team would torch a month of legitimate transactions, and now we know: the fake coins were indistinguishable from real ones.

---

## How the exploit worked

The attacker registered a Gateway Address on Aug. 28, paid a 100 ZANO registration fee (about $553 at the time), tested a fabricated asset, and minted approximately 18.4 million ZANO in a single transaction the next day. That first mint went unnoticed for nearly a month. On Sept. 25, the attacker did it again, another 18.4 million ZANO, then used the same method to create about 1.8 quadrillion fUSD.

> "These coins functioned as authentic ZANO and could be spent normally," the team wrote in its post‑mortem.

Zano's head of marketing and growth, Quinten van Welzen, told Cointelegraph that only a small fraction of the unauthorized coins reached the market, limited by the liquidity available on exchanges. Small comfort, but it tracks: dumping tens of millions of coins into thin order books would have moved the price against the attacker long before most of it could be sold.

---

## The trust math

The team acknowledged the rollback would hurt trust but argued it was necessary. I think they are right on the narrow technical point and wrong to expect this to blow over. A chain that can be rewound a month by its own team is making a very specific promise about finality, and that promise is now broken in public.

According to Zano, exchanges and payment services that processed Zano transactions in September will need to replay withdrawals reversed by the rollback, meaning their records may be invalidated after the fact.

Also worth noting: Zano said the bug slipped past AI‑assisted testing, internal audits, and bug bounties. The exploit was ultimately flagged by internal staff after the second mint, weeks later. Teams are leaning on these tools as a layer of security review, and here is a case where the tool missed a bug that let someone print a quadrillion tokens for a $553 entry fee.

---

## The cleanup

Zano said Wednesday it is working to restore affected balances using its developer fund, team members' personal funds, and committed contributions. Recovery will run primarily through exchanges and payment services, with exchanges replaying withdrawals reversed by the rollback and the team crediting the affected deposits.

Whether that makes users whole is an open question. Nobody outside the team knows the full list of affected transactions, and "committed contributions" is doing a lot of work in that sentence.

---

## Sources

- [Cointelegraph: Zano exploiter minted more than a quadrillion fUSD before blockchain rollback](https://cointelegraph.com/news/zano-exploiter-created-369m-unauthorized-zano-before-blockchain-rollback)
