---
title: Chinese hackers used AI agents to spy on 2,250 organizations after breaching ConnectWise
date: 2026-10-22
topic: ai
score: 7
candidate_id: 93c844a35d415e95
sources: ["https://techcrunch.com/2026/10/22/chinese-hackers-spied-on-thousands-of-companies-after-breaching-it-giant-connectwise/"]
triage_reason: "Breach of a major IT provider affecting thousands of companies with named Microsoft attribution and an AI-agent angle is clearly publishable security "
---

China state-aligned hackers broke into IT management giant ConnectWise and used the access to spy on roughly 2,250 organizations, [TechCrunch reports](https://techcrunch.com/2026/10/22/chinese-hackers-spied-on-thousands-of-companies-after-breaching-it-giant-connectwise/), citing security researchers at Microsoft.

The mechanics are ugly. The hackers got into ConnectWise's cloud backup service and stole application credentials, the ones used to establish data links between ConnectWise and its corporate customers, who rely on the service to back up company data. Those credentials are trusted by design. With them in hand, the attackers could log in to a customer's Microsoft-hosted environment as if they were an authorized user and read through emails and other files.

## The AI part is the speed

Mass credential theft is not new. The pace of this campaign is. Microsoft says the attackers used AI agents to hit those 2,250 organizations at almost 3,000 attempted sign-ins per minute, a tempo the company says gives defenders "little time to detect and respond."

The tool behind it has a name. ARTEX is an open source AI framework that works with AI models to stress-test cyber defenses. A defensive tool, in other words, until someone points it outward. The speed of the mass hacks was attributed directly to its use. The same software showed up in the recent compromise of South Korea's financial systems, many of which had weak security and lacked multi-factor authentication.

I keep coming back to the open source part. When the offensive capability ships as a framework anyone can download, the cost of running a campaign like this collapses. You do not need operators working in shifts. You need stolen credentials and someone else's code.

## One vendor, thousands of victims

The other story is the blast radius. ConnectWise is not a household name, but its software sits inside thousands of corporate environments. Breach one vendor like that and you inherit its customer list. The hackers did not pick 2,250 targets. They picked one.

I have read some version of this story every few months for years, and the math never changes. Defenders have to trust their vendors. Attackers only have to find the one vendor with a weak spot. Adding AI agents to the attacker's side of that equation makes the tempo worse without making the defense any faster.

ConnectWise says it has paused access to its cloud backup system and is investigating the breach. As of Thursday, the company said it was working on restoring the service.

## What to watch

Two things. First, what ConnectWise's investigation turns up about how the hackers got in, because that tells you whether this was a sophisticated operation or an unlocked door. Second, whether ARTEX keeps showing up in incident reports. One campaign is an event. Two, counting South Korea, starts to look like a pattern.

Nobody knows how far this kind of automated attack scales from here. But 3,000 sign-in attempts a minute is not something you answer with humans staring at dashboards.

## Sources

- [TechCrunch: Chinese hackers spied on thousands of companies after breaching IT giant ConnectWise](https://techcrunch.com/2026/10/22/chinese-hackers-spied-on-thousands-of-companies-after-breaching-it-giant-connectwise/)
