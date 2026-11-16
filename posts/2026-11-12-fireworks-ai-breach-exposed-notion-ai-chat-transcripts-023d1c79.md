---
title: Fireworks AI breach exposed Notion AI chat transcripts
date: 2026-11-12
topic: ai
story: fireworks-ai-breach
score: 7
candidate_id: 023d1c79ca20cb05
sources: ["https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/"]
triage_reason: "A security breach exposing customer data at a major AI inference provider is a significant trust and security event."
---

Hackers breached Fireworks AI and stole customer data, including chat transcripts from some Notion AI customers, TechCrunch reports.

Fireworks, a platform developers use to access open AI models, said the attacker got in through its cloud provider, reached a Fireworks development system, and from there accessed customer data. The company's security advisory says billing information and some datasets were taken. Fireworks says it has tens of thousands of customers, including legal tech company Harvey and AI coding company Cursor.

## What Notion lost

Notion is the one confirmed affected customer so far. The company says around 1% of its customers were hit, and that the stolen material includes chat transcripts from Notion AI users of its "Insights" feature. In Notion's words, the transcripts cover "any input to or output from the model" that was written to the chat.

One strange detail: Notion says much of the data was unattributable, meaning the company could not tell which customer it came from. That cuts both ways. It limits how targeted the exposure is, but it also means Notion cannot fully tell you whether your conversations are in the pile.

Notion says Fireworks alerted it to the incident, and on November 3 it disconnected its systems from Fireworks, deleted the data stored in its systems, and stopped all connectivity between the two companies.

## The motive, and the pattern

Fireworks says it believes the attackers are financially motivated and focused on selling tokens from breached access to large language models. The scheme: sell that access to unauthorized third parties, who then burn through AI model usage on someone else's resources.

This is also the second security incident affecting Fireworks in as many months, following one in October. Once is an incident. Twice in two months starts to look like a pattern, and if I were a Fireworks customer I would be asking hard questions right now.

## Why this matters beyond Fireworks

The bigger story is the dependency chain. As TechCrunch puts it, the breach shows how tech companies rely on other tech providers for their own offerings, and how attacks spill over into their customers. Notion users never chose Fireworks. Most have probably never heard of it. Their AI chat transcripts were exposed there anyway.

Notion's response looks reasonably fast, and 1% is a small slice of its customer base. But the transcripts were already gone by the time the cables got pulled. Disconnection is containment, not recovery.

Harvey and Cursor appear in the report as Fireworks customers, not as confirmed victims. Still, the list of affected companies may not be finished growing, and nobody outside Fireworks knows how wide this goes yet.

## Sources

- [TechCrunch: Cyberattack on Fireworks AI allowed hackers to access Notion customers' chat transcripts](https://techcrunch.com/2026/11/12/cyberattack-on-fireworks-ai-allowed-hackers-to-access-notion-customers-chat-transcripts/)
