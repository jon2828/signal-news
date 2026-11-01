---
title: Chainalysis says AI-assisted hacker accessed customer names and emails
date: 2026-10-31
topic: both
story: chainalysis-breach
score: 7
candidate_id: 92484b73101f6f77
sources: ["https://www.theblock.co/news/business/2026-10-31-chainalysis-says-hacker-using-offensive-agentic-techniques-accessed-its-customers-names-and-emails-432244"]
triage_reason: "A security breach at a major crypto-analytics firm with named sourcing and new detail on attacker techniques."
---

Chainalysis, the blockchain analytics firm that tracks crypto hackers for a living, says a hacker using AI broke into its own systems this month.

In a notice sent to affected customers and published in a blog post Friday evening, the company said an unidentified attacker used "offensive agentic techniques" to access its systems and internal tools. The data taken was what Chainalysis calls non-sensitive: user IDs, full names, email addresses, and organization role labels for users on its platform. The company said it will follow up with each client detailing exactly what was accessed.

It also said it has found no indication the attacker reached investigation content like graphs, notes, or cases, nor transaction or query results, cleartext passwords, MFA secrets, or session tokens.

## What Chainalysis is not saying

The notice leaves out a lot. Chainalysis did not say when it detected the intrusion, how many customers were affected, which vulnerabilities were exploited, or what role AI agents actually played. The breach was first flagged by International Cyber Digest, and Chainalysis declined to answer The Block's follow-up questions.

I keep coming back to that phrase, "offensive agentic techniques." If an AI agent genuinely ran this intrusion, that is a milestone, and the company best positioned to describe it in detail is Chainalysis. If the phrase is vaguer than the reality behind it, that is worth knowing too. Right now we have the label and nothing underneath it.

The company said it has brought in third-party cybersecurity experts and is using large language models to support a security review of its platform. AI on both sides, then. It advised customers to turn on two-factor authentication and to watch for unexpected password reset requests or authentication prompts.

## The Binance backdrop

Chainalysis stressed the breach is "not related" to the recent crypto theft at Binance, and there is no reason to doubt that. But the timing is something. Chainalysis, Elliptic, and TRM have each attributed the roughly $6.3 billion Binance hack to North Korean groups (Chainalysis puts the figure at $6.4 billion). Binance says the attackers compromised an engineer's laptop and reached a service container, though co-CEO Richard Teng has said the breach was more complex than one employee's permissions.

On Ethereum, the attacker used EIP-7702 to turn a Binance hot wallet into a sweeper. The contract was only around 130 lines, according to Immunefi vice president Simone Imbrescia, who noted that very simple code can become devastating once an attacker has access to a powerful enough system.

Chainalysis is still tracking the stolen funds and says it is seeing "never-seen-before laundering patterns." Thousands of transactions in a short period suggest the attackers are using automation to obscure the trail. Rather than forwarding funds to fresh addresses, they circulate the crypto among addresses repeatedly, sometimes sending it back to addresses used earlier in the sequence. The attackers are also routing funds through DeFi protocols on Tron to dodge stablecoin freezes.

Two automation stories in one week. One attacker used AI to get into the company that tracks attackers. Another is using automation to launder billions while that same company watches. The defenders, for their part, are now running LLMs over their own infrastructure. Nobody knows how this plays out, but the loop is getting faster on both sides.

## Sources

- [The Block: Chainalysis says hacker using 'offensive agentic techniques' accessed its customers' names and emails](https://www.theblock.co/news/business/2026-10-31-chainalysis-says-hacker-using-offensive-agentic-techniques-accessed-its-customers-names-and-emails-432244)
