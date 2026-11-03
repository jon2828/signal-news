---
title: Liquid's LBTC is fully backed again, but who paid for it is still a secret
date: 2026-11-03
topic: bitcoin
story: liquid-exploit-resolution
score: 7
candidate_id: a7816c982d9cf172
sources: ["https://www.coindesk.com/markets/2026/11/03/liquid-s-bitcoin-ious-are-fully-backed-again-after-a-usd320-million-exploit"]
triage_reason: "Confirms the resolution of a significant security exploit, a key milestone for trust in the Liquid network."
---

Every LBTC on the Liquid Network is backed by a real bitcoin again, nearly two months after a software bug let an attacker drain almost the entire reserve, [CoinDesk reports](https://www.coindesk.com/markets/2026/11/03/liquid-s-bitcoin-ious-are-fully-backed-again-after-a-usd320-million-exploit).

A quick recap, because the September incident got less attention than it deserved. On Sept. 6, a flaw in Liquid's software let someone mint about 4,000 LBTC with nothing behind them and redeem them for actual bitcoin. The federation's reserve fell from roughly 4,205 BTC to 197, according to Blockstream's incident report at the time. The attacker, who claimed to be a white hat, returned 3,400 BTC the next day. That left a hole of about 600 BTC.

On Monday, the Liquid Federation said on X that reserves were "fully restored, reestablishing 1:1 BTC backing for all LBTC," after a final 250 BTC transfer. Anyone can verify the balance on the network's public dashboard.

## The part nobody is explaining

Here's what I keep coming back to. Somebody put up roughly 600 BTC to make users whole, and the federation won't say who.

The candidates are obvious. Blockstream, which leads the federation. The federation members themselves, splitting the bill. Maybe the attacker settled for less than the full amount. The federation isn't saying, and that silence matters, because Liquid's entire model runs on trust in this group. You lock your BTC with them, they hand you an IOU, and the system works because you believe the IOU is good. When the backing breaks and then gets fixed behind closed doors, "believe" is doing a lot of work.

To be fair, the transparency here beats most of crypto. The reserve is on-chain and publicly auditable. You don't have to take the federation's word that the bitcoin is there; you can look. That's more than you get from the average centralized exchange.

But the money that filled the gap came from somewhere. In any other corner of finance, an institution that had $320 million drained by a software bug, then quietly covered the shortfall, would be answering questions about it. In crypto, we get a tweet.

## Not quite back to normal

One more detail. Users can swap BTC and LBTC one-to-one through providers like SideSwap, but direct withdrawals from the federation remain under "enhanced controls," whatever that means in practice. The peg is restored, but the drawbridge is still half up.

The network survived a $320 million exploit and users were made whole. That's a better ending than most crypto hacks get. I'd just like to know who wrote the check.

## Sources

- [Liquid's bitcoin IOUs are fully backed again after a $320 million exploit (CoinDesk)](https://www.coindesk.com/markets/2026/11/03/liquid-s-bitcoin-ious-are-fully-backed-again-after-a-usd320-million-exploit)
