---
title: Coinbase lays out what it wants from Bitcoin's post-quantum migration
date: 2026-10-14
topic: bitcoin
score: 7
candidate_id: 429f8f6be8883f62
sources: ["https://www.theblock.co/news/ecosystems/2026-10-13-coinbase-bitcoin-post-quantum-migration-418509"]
triage_reason: "A major exchange publicly shaping Bitcoin's post-quantum signature migration is a notable protocol-adjacent development with a named source."
---

Coinbase has published a set of technical priorities for Bitcoin's post-quantum transition, and the short version is simple: start now, because this takes years.

The exchange, which says it holds 5% of the total bitcoin supply, is already preparing its own systems for a post-quantum future. Its argument is that protecting the network from quantum threats is a much bigger job than picking a quantum-resistant signature scheme. An ideal approach, per Coinbase, would protect both exposed and newly created funds, fit within Bitcoin's limited block space, keep full-node validation independent, work with institutional custody setups and ordinary wallets, and offer a credible path for coins that cannot or will not move.

That last category is the interesting one. More on it below.

"We believe it is important to begin preparing well ahead of any CRQC (Cryptographically Relevant Quantum Computer) announcement," the company said, adding that consensus changes and ecosystem migrations can take years.

## Flexibility first

The headline preference is modularity. Coinbase wants post-quantum output designs that separate the "container" from the signature scheme, so schemes can be introduced, replaced, or supplemented without redesigning everything. It points to P2MR (BIP-360) and P2TRv2 as constructions that appear to offer this.

It also favors staged protection. Active wallets could move to a PQ-capable or hybrid construction before anyone settles the final policy on legacy signatures. One option it describes: a 1-of-2 setup giving the same funds two spending paths, one authorized by a classical ECDSA or Schnorr key, one by a post-quantum key.

I like this framing. It lets people act without forcing the whole community to agree on the endgame first. Migrate now, argue later.

On signatures themselves, Coinbase says any support for stateful schemes must come with a stateless option, since state mismanagement can lead to forgery. It also wants at least one viable post-quantum option with promising multiparty computation (MPC) compatibility, which matters for institutional custody. "When implemented effectively, MPC can provide strong protection against key theft," the company said, calling it an important layer of defense for large organizations facing constant attacks on their infrastructure.

## The abandoned coins problem

Coinbase's position on lost or inaccessible coins is careful: the questions are difficult, they deserve debate, and that debate can run in parallel with the technical work. No proposal, no timeline, just a nudge to keep talking.

That is the politically loaded part of all this, and Coinbase knows it. Any eventual policy on coins that never migrate will affect a lot of money whose owners cannot or will not move it. Kicking that question down the road while the cryptography gets built is probably the only workable move, but it also means the hardest fight is still ahead.

## Why this carries weight

Plenty of people have opinions about post-quantum Bitcoin. Fewer of them custody 5% of the supply. When an exchange that size says it is preparing its own systems and publishes a wishlist, wallet developers and BIP authors tend to read it.

Whether the community converges on P2MR, P2TRv2, or something else entirely is an open question. Nobody knows how this plays out, and the timeline depends on hardware that does not exist yet. But the work Coinbase describes, consensus changes plus an ecosystem-wide migration, is slow even when everyone agrees. Starting early is the one part fully in everyone's control.

## Sources

- [The Block: Coinbase lays out flexible designs as key priority for Bitcoin's post-quantum migration](https://www.theblock.co/news/ecosystems/2026-10-13-coinbase-bitcoin-post-quantum-migration-418509)
