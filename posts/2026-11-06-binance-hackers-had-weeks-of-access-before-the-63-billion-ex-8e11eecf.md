---
title: Binance hackers had weeks of access before the $6.3 billion exploit
date: 2026-11-06
topic: both
story: binance-hack
score: 8
candidate_id: 8e11eecf60a88eb1
sources: ["https://cointelegraph.com/news/binance-hackers-8-weeks-access-63b-exploit-security-alliance?utm_source=rss_feed&utm_medium=rss&utm_campaign=rss_partner_inbound"]
triage_reason: "Major security breach details revealing 8 weeks of access, significantly impacting trust in exchange security."
---

# Binance hackers had weeks of access before the $6.3 billion exploit

**Date:** 2023-11-06

The hackers behind Binance's $6.3 billion exploit maintained a foothold inside the exchange for weeks before the funds were moved on Oct. 29. Security Alliance (SEAL), a nonprofit cybersecurity group, estimates that a Binance employee's device was compromised about eight weeks earlier - in September - through a fake‑recruitment scheme, according to [Cointelegraph's report](https://cointelegraph.com/news/binance-hackers-8-weeks-access-63b-exploit-security-alliance).

Binance disputes the framing. A spokesperson told Cointelegraph that the initial device compromises occurred in June and September, but that the attackers **"did not gain the access needed to reach wallet operations until October 20, when they used that foothold to move laterally and obtain access to additional devices and credentials."**

Both accounts can be true. SEAL measures the full intrusion window, while Binance draws a line between merely being inside the network and having access to the wallet infrastructure. The distinction is technically accurate, even if it presents a more favorable narrative for Binance.

---

## How they got in

### First entry point - June
An employee downloaded a tampered Homebrew installer while trying to install an AI coding tool. Binance says it detected the incident, replaced the device and rotated the related credentials. By that time, the attackers had already gathered information about employees working on the wallet infrastructure, as noted in a Tuesday X post.

### Second entry point - September
A software engineer fell victim to a fake‑recruitment campaign. SEAL identified at least four front‑company domains linked to TraderTraitor's 2026 recruitment lures: `citalab.net`, `citalab.com`, `bitfit.io` and `oddium.io`.

### Final move - Oct. 20
Using the compromised engineer's machine and an internal AI tool, the attackers took control of two wallet‑infrastructure engineers' devices, discovered a deployment‑permission token and later leveraged it in the Oct. 29 exploit that drained $6.3 billion.

---

## The AI angle

Both entry points were ordinary: a developer installing an AI‑assisted coding tool and an engineer responding to a recruiter. The lateral movement also exploited an internal AI tool, highlighting how AI can expand the attack surface, first as bait, then as a pathway with broad system access.

---

## Long dwell times are the pattern

SEAL's broader analysis shows similar multi‑stage intrusion patterns in other high‑profile hacks:
- ~6 weeks of access before the $388 million Bitget hack
- ~6 weeks of access to LayerZero before the $293 million Kelp DAO exploit
- ~3 weeks before the $24 million AFX exploit

SEAL wrote that threat actors can operate with a **"high degree of stealth over prolonged periods"**, and the timelines support that claim.

These prolonged dwell times should alarm every exchange. Even though Binance detected the June compromise, the attackers had already mapped the internal org chart and identified the critical wallets, rendering the early detection insufficient.

---

## Attribution

The U.S. Federal Bureau of Investigation attributed the attack to North Korea's TraderTraitor in a Saturday report. Kim Yo Jong, sister of Kim Jong Un, dismissed the accusations.

---

## Sources

- [Cointelegraph: Binance hackers had 8 weeks of access before $6.3 B exploit, Security Alliance estimates](https://cointelegraph.com/news/binance-hackers-8-weeks-access-63b-exploit-security-alliance)
