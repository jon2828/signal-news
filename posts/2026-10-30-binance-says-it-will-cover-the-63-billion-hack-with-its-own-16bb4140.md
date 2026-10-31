---
title: Binance says it will cover the $6.3 billion hack with its own money
date: 2026-10-30
topic: bitcoin
score: 7
candidate_id: 16bb4140c583528b
sources: ["https://www.coindesk.com/business/2026/10/30/binance-arranges-usd6-34-billion-to-cover-losses-from-record-crypto-hack", "https://www.theblock.co/news/business/2026-10-30-binance-hack-largest-crypto-hack-north-korea-432225"]
triage_reason: "Corroborated by two sources and adds genuinely new facts — Binance reserving $6.34B of its own funds and roughly $3B in frozen assets — beyond the ini"
---

Binance lost an estimated $6.3 billion to attackers on Thursday, the largest crypto theft in history, and the exchange says it will cover the whole thing with company money.

## What Binance is doing

Per CoinDesk, Binance set aside more than $6.34 billion for the incident. $5 billion of that is already held in the exact tokens that were stolen, and the exchange is buying the rest through public markets and OTC desks so user balances can be restored one-for-one. Partners separately froze roughly $3 billion of the stolen funds, and that frozen pile does not count toward the $6.34 billion.

Withdrawals are paused. Deposits are open. Co-CEO Richard Teng said in an X video Friday that he is "very hopeful" withdrawals resume before a Sunday deadline, "on track to be within 40 hours," with an initial proof-of-reserves report targeted for Monday. There is also the SAFU emergency fund, which has typically held around $1 billion in bitcoin, as a backstop.

I will believe the one-for-one part when the proof of reserves publishes. To Binance's credit, buying the actual tokens rather than handing users a dollar figure is the right way to do it. FTX this is not, at least not on the numbers we have so far.

## How the attackers got in

This is the part that should worry every exchange. Per The Block, Binance's initial investigation points to a compromised DevOps engineer's laptop and unauthorized access to a service container. No private-key leak has been identified, and Teng himself described the attack as more complex than one employee's permissions.

TRM Labs says the attacker staged for at least 36 hours, funding an operational wallet with small Tornado Cash withdrawals, then deploying and testing malicious code on three wallets. On Ethereum, the attacker used EIP-7702 to turn a Binance hot wallet into a sweeper they controlled, with 50 pre-signed authorizations prepared so at least one would still be valid at execution. Coordinated transfers across nine other blockchains point to a compromise of Binance's broader hot-wallet signing infrastructure, not a single wallet.

Simone Imbrescia, a vice president at Immunefi, made the observation I keep coming back to. The onchain sweeper contract was only around 130 lines of code. "The hard part sometimes is getting access to a system powerful enough to make very simple code devastating," she said. The attacker did not break cryptography. They got inside the machine that tells the keys what to sign.

## The laundering, and the freezes

Chainalysis, Elliptic, and TRM have all attributed the attack to North Korean groups. TRM explicitly ties it to the same group behind the $1.5 billion Bybit hack, and Chainalysis found onchain links to last month's Bitget exploit. Elliptic added a caveat worth keeping: the overlap with Bitget involved only a small slice of the Binance funds and does not conclusively prove the same attackers.

The thief clearly knew what could be frozen. Per The Block, they converted $325 million in stablecoins into $285 million of ETH in about 20 minutes, and Elliptic says they accepted losses of up to 26% swapping USDT for ETH through decentralized exchanges and market makers, purely to get into assets no issuer can freeze. They also parked $59.9 million in stolen USDT in Aave as collateral and borrowed 19,762 ETH against it. Aave said Friday its contracts were unaffected and all markets were unfrozen.

That $3 billion freeze is the detail I can't stop thinking about. It is the best possible advertisement for centralized stablecoins and the worst, depending on who you ask. The freeze worked this time. It also confirms the attacker understood the system better than most of its defenders.

## The bank robbery defense

TD Cowen analysts called this "a compromise of infrastructure at a centralized intermediary, rather than a failure of Bitcoin or its underlying network," adding that "we do not stop using dollars when a bank is robbed."

Fair enough, as far as it goes. But robbed banks make depositors whole through deposit insurance and a lender of last resort. Binance is making depositors whole out of its own treasury, which works right up until the hole is bigger than the treasury. This time, apparently, it is not. Whether the industry can keep absorbing North Korea's budget line is a question nobody has a good answer to.

## Sources

- [CoinDesk: Binance arranges $6.34 billion to cover losses from record crypto hack](https://www.coindesk.com/business/2026/10/30/binance-arranges-usd6-34-billion-to-cover-losses-from-record-crypto-hack)
- [The Block: Binance arranges $6.34 billion to cover losses from record crypto hack](https://www.theblock.co/news/business/2026-10-30-binance-hack-largest-crypto-hack-north-korea-432225)
