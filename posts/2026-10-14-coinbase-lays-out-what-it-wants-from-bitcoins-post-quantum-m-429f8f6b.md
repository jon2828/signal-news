---
title: Coinbase lays out what it wants from Bitcoin's post-quantum migration
date: 2026-10-14
topic: bitcoin
score: 7
candidate_id: 429f8f6be8883f62
sources: ["https://www.theblock.co/news/ecosystems/2026-10-13-coinbase-bitcoin-post-quantum-migration-418509"]
triage_reason: "A major exchange publicly shaping Bitcoin's post-quantum signature migration is a notable protocol-adjacent development with a named source."
---

# Coinbase lays out what it wants from Bitcoin's post‑quantum migration

*Date: 2026‑10‑14*

Coinbase has published a set of technical priorities for Bitcoin's post‑quantum transition, and the short version is simple: start now, because the work can take years.

The exchange, which says it holds **5 % of the total Bitcoin supply**, is already preparing its own systems for a post‑quantum future. Its argument is that protecting the network from quantum threats is a much bigger job than merely picking a quantum‑resistant signature scheme. An ideal approach, per Coinbase, would protect both exposed and newly created funds, fit within Bitcoin's limited block space, keep full‑node validation independent, work with institutional custody setups and ordinary wallets, and offer a credible path for coins that cannot or will not move.

> "We believe it is important to begin preparing well ahead of any CRQC (Cryptographically Relevant Quantum Computer) announcement," Coinbase said. "Bitcoin consensus changes and ecosystem migrations can take years, so it is important that we begin this work now."

---

## Flexibility first

Coinbase's headline preference is modularity. It wants post‑quantum output designs that separate the **"container"** from the signature scheme so that new schemes can be introduced, replaced, or supplemented without a complete redesign. The firm points to **P2MR (BIP‑360)** and **P2TRv2** as constructions that appear to offer this flexibility.

It also favors staged protection. Active wallets could move to a PQ‑capable or hybrid construction before a final policy on legacy signatures is settled. One option described is a **1‑of‑2** setup that gives the same funds two spending paths: one authorized by a classical ECDSA or Schnorr key, and one by a post‑quantum key.

> "When implemented effectively, MPC can provide strong protection against key theft, and it is an important layer of defense for large organizations that face constant attacks on their infrastructure," Coinbase said.

The exchange notes that any support for stateful signatures should also include a stateless option, because state‑mismanagement can lead to forgery. It also stresses the importance of **multiparty computation (MPC) friendliness** for institutional custody, and that at least one viable post‑quantum option should have promising MPC compatibility.

---

## The abandoned‑coins problem

Coinbase's position on lost or inaccessible coins is cautious: the questions are difficult, they deserve debate, and that debate can run in parallel with the technical work. The company does not propose a specific solution or timeline, but it encourages continued discussion.

---

## Why this carries weight

Few entities control a sizable share of Bitcoin's supply; Coinbase's custody of roughly 5 % gives its technical roadmap significant visibility. When an exchange of this size signals that it is preparing its own systems and publishes a wishlist, wallet developers and BIP authors are likely to take notice.

Whether the community ultimately converges on P2MR, P2TRv2, or another construction remains an open question. The timeline depends on hardware that does not yet exist, and any consensus change plus ecosystem‑wide migration is expected to be a multi‑year effort. Starting early is the one part that the community can control.

---

## Sources

- [The Block: Coinbase lays out flexible designs as key priority for Bitcoin's post‑quantum migration](https://www.theblock.co/news/ecosystems/2026-10-13-coinbase-bitcoin-post-quantum-migration-418509)
