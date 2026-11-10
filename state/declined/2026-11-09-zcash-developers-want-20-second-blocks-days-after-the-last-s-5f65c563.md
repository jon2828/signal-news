---
title: Zcash developers want 20-second blocks days after the last speedup
date: 2026-11-09
topic: bitcoin
story: zcash-block-time
score: 7
candidate_id: 5f65c5631083bb10
sources: ["https://www.coindesk.com/tech/2026/11/09/zcash-developers-want-20-second-blocks-just-days-after-major-speed-upgrade"]
triage_reason: "Significant protocol change proposal for a major PoW coin, backed by early performance data."
---

Zcash developers are pushing to cut the network's block time to 20 seconds, days after an upgrade that already has blocks arriving three times faster than before, [CoinDesk reports](https://www.coindesk.com/tech/2026/11/09/zcash-developers-want-20-second-blocks-just-days-after-major-speed-upgrade).

The case for moving again so quickly comes from the data since that upgrade. Early numbers show Zcash's orphan-block rate holding close to pre-upgrade levels, even with blocks coming three times as often. Orphan blocks are valid blocks that lose the race to join the main chain, and they're the usual price of faster block times: the quicker blocks arrive, the more often two miners produce competing blocks at the same height. If the orphan rate barely moves after a 3x speedup, the network probably has headroom. That's the developers' read, and it's a reasonable one.

## The part I like

This is how protocol changes should go. Ship, measure, then push further if the numbers hold. No manifesto. No year-long governance fight. The last upgrade went out, the orphan rate stayed flat, and the response is: again.

## The part I'd watch

"Early data" is doing real work in that summary. A few days of blocks is a small sample, and network conditions aren't static. An orphan rate that looks calm this week can look different when usage spikes or a large miner has a bad peering day. The honest position is that the first upgrade looks safe so far, not that it's proven safe.

There's also a gap in what's public. The summary gives the target, 20 seconds, and the speedup so far, three times, but not the current block time itself. Without the pre-upgrade number I can't tell you how aggressive this next cut actually is. Going from 60 seconds to 20 is a bigger leap than going from 25 to 20, and the risk profile isn't the same.

Faster blocks are mostly a user experience play. Quicker first confirmations, less staring at a pending transaction. The cost shows up in orphans and reorgs, which is exactly the metric the developers are watching, so at least the right dial is on the dashboard.

If the rate holds at 20 seconds, expect someone to propose going lower. Whether that's good engineering or a network easing toward its breaking point is the part nobody knows yet.

## Sources

- [CoinDesk: Zcash developers want 20-second blocks just days after major speed upgrade](https://www.coindesk.com/tech/2026/11/09/zcash-developers-want-20-second-blocks-just-days-after-major-speed-upgrade)
