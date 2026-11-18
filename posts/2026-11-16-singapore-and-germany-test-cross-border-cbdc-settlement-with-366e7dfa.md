---
title: Singapore and Germany test cross-border CBDC settlement with zero-knowledge proofs
date: 2026-11-16
topic: bitcoin
story: singapore-germany-zk-payments
score: 7
candidate_id: 366e7dfafc88dc00
sources: ["https://www.coindesk.com/business/2026/11/16/singapore-germany-test-cross-border-payments-to-reduce-settlement-risk"]
triage_reason: "Named central-bank-adjacent cross-border settlement test using zero-knowledge proofs, a real infrastructure milestone."
---

The Monetary Authority of Singapore and Germany's Bundesbank say they've successfully tested a cross-border payment method that attacks settlement risk, the old problem where one side of a currency trade pays out and the other side never delivers.

The trial, called Project Simbolon, used wholesale central bank digital currencies to exchange euros and Singapore dollars. DBS and Deutsche Bank took part, with Partior as the technology provider, according to an MAS announcement reported by CoinDesk.

## The problem

Settlement risk is not a niche concern. According to the Bank for International Settlements, about 10% of daily foreign currency transactions, roughly $1.4 trillion, move through processes that leave banks exposed when one leg of a trade completes and the other doesn't.

A fix already exists for euro-Singapore dollar trades: a bank-owned system that settles both legs of a trade simultaneously. But it only works during the roughly five-hour window each day when both central bank payment systems are open. Outside that window, the risk comes back.

## How the test worked

Simbolon asked whether the two central banks' own tokenized ledgers could do the same job across different operating hours, with no shared platform between them.

The mechanism is the part I find genuinely interesting. The project used zero-knowledge proofs, a form of cryptography that lets one party verify information without seeing the underlying data. Each ledger could confirm the other leg of the trade was locked, so neither currency settled unless both did. No shared ledger. No trusted intermediary sitting in the middle.

If that sounds familiar, it should. This is the cryptographic toolbox the public blockchain world has been building for years, now showing up inside central bank infrastructure.

## My take

I'm of two minds on this. CBDC skepticism is well earned when the subject is retail versions and what they mean for financial privacy. But this is wholesale plumbing, bank-to-bank settlement, and the problem it targets is real and expensive. $1.4 trillion a day in exposed transactions is not a rounding error.

The ZK angle is the story for me. The central banks didn't adopt a public chain or a shared ledger. They took the cryptography and kept everything else permissioned and separate. That's probably how most of this tech gets absorbed by incumbents: piece by piece, stripped of the parts that threaten anyone.

Credit to the central banks for not declaring victory, at least. They say wider use still requires assessing legal, regulatory, operational, and governance requirements, and a full report is due Wednesday. Successful pilot announcements are cheap. Production systems that banks actually route trillions through are not. I'll read the report when it lands.

## Sources

- [CoinDesk: Singapore, Germany test cross-border payments to reduce settlement risk](https://www.coindesk.com/business/2026/11/16/singapore-germany-test-cross-border-payments-to-reduce-settlement-risk)
