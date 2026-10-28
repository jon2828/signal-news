---
title: Google previews MPC security system for institutional crypto custody
date: 2026-10-28
topic: both
score: 7
candidate_id: 1786ba9e95a710fe
sources: ["https://www.coindesk.com/tech/2026/10/28/google-to-preview-crypto-custody-security-system-as-ai-threats-grow"]
triage_reason: "Google launching MPC-based crypto custody in private preview with major financial institutions testing is a significant infrastructure development."
---

Google is unveiling a security system for institutional crypto custody at its inaugural digital assets symposium in New York City on Wednesday, [CoinDesk reports](https://www.coindesk.com/tech/2026/10/28/google-to-preview-crypto-custody-security-system-as-ai-threats-grow). The product, called Google Multi-Party Compute (MPC), is in private preview. Several major financial institutions are testing it as design partners, Google told CoinDesk, though it won't name them. Commercial availability is planned for early 2027, and pricing hasn't been disclosed.

## How it works

MPC splits a private key into fragments and distributes them across separate environments. No single machine holds the whole key, so one compromised server doesn't mean drained wallets. Google's version adds a policy layer: institutional rules get checked before a transaction is signed, which is meant to block unauthorized transfers even after credentials have been stolen.

That focus is the actual story. The headline ties the launch to growing AI threats, but the protections Google describes target compromised credentials and unauthorized transactions, not anything AI-specific. The company points to billions of dollars in private-key-related thefts as the motivation. Fair enough. That's the attack vector that keeps burning people.

## Alphabet is a customer

The detail I keep coming back to: Alphabet has started using the system to secure its own digital assets on Ethereum and Solana. Google declined to say which assets or in what size.

Running your own keys through your own custody stack is a stronger endorsement than any slide deck. It's also a quiet confirmation that Alphabet holds digital assets on those chains, something the company hasn't exactly advertised. I find that more newsworthy than the product itself.

## The caveats

MPC is not new, and Google knows it. In 2023 the company published guidance for building MPC-based digital-asset systems on its Confidential Space infrastructure. This launch is that do-it-yourself approach turned into a managed service, which is a sensible business move and also an admission that most institutions were never going to build it themselves.

Google says the service can eventually support post-quantum cryptography. "Eventually" is doing a lot of work in that sentence. What ships in 2027 protects against stolen credentials, not quantum attacks, so file the quantum angle under roadmap, not product.

No pricing. No named partners. A preview now, a real product sometime next year. Whether banks will hand key material to Google is a genuine open question, and nobody outside the private preview knows how the testing is actually going.

## Sources

- [CoinDesk: Google to preview crypto custody security system as AI threats grow](https://www.coindesk.com/tech/2026/10/28/google-to-preview-crypto-custody-security-system-as-ai-threats-grow)
