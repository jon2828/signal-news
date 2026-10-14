---
title: Ledger confirms LTE implant in reseller units that steals recovery phrases
date: 2026-10-13
topic: bitcoin
score: 8
candidate_id: ed42c98438541b9f
sources: ["https://www.theblock.co/news/business/2026-10-13-ledger-confirms-hardware-implant-cryptobilis-reseller-units-mediamarkt-suspends-sales-europe-418442"]
triage_reason: "Ledger's confirmed hardware implant stealing recovery phrases is a major supply-chain security breach with named confirmation and concrete consequence"
---

Ledger has confirmed that hardware signers sold by Southeast Asian reseller CryptoBilis contained an implant that reads the 24-word recovery phrase off the screen during setup and transmits it over LTE using a provisioned eSIM.

The finding comes from Ledger's Donjon security team, which posted the update on X Tuesday. According to The Block's report, the implant does not touch the Secure Element or Ledger's operating system, and it does not alter transactions or signatures. It watches the screen at the one moment that matters, the moment the seed words appear, and phones home.

That detail is what makes this nasty. The whole pitch of a hardware wallet is that the seed never leaves the device. This attack does not break that cryptography. It sidesteps it entirely, with a cellular radio hidden inside the unit somewhere between the factory and the buyer.

## The losses, still unverified

Ledger said last week it was investigating fund losses from users who bought through CryptoBilis. Onchain researchers have estimated losses at more than $86 million across Bitcoin, Ethereum and Tron, but Ledger says that figure and the number of affected users remain unverified.

"Figures circulating online come from third parties and Ledger has not fully verified them," the company's post read. It also advised anyone who lost funds to "coordinate with law enforcement before opening the signer," which is good advice and a sign of how physical this investigation has become.

Ledger says it has no indication its own infrastructure or services were compromised, and it has asked CryptoBilis to pause all sales and shipments while recovered hardware is examined.

## MediaMarkt pulls Ledger from shelves

The fallout is no longer confined to one reseller. MediaMarkt Saturn stopped selling Ledger devices in stores and online as of Oct. 13 after a customer in Germany reported an implant. No funds were lost in that case, according to Ledger.

A MediaMarkt Saturn spokesperson told The Block the company takes "this incident very seriously" and has removed all of the manufacturer's affected products while staying in contact with Ledger.

Two other claims are floating around, and neither is confirmed. An X user named Johannes said Friday he bought two Ledger devices from separate MediaMarkt stores and found unauthorized cables and cellular modules inside both. Former Mt. Gox CEO Mark Karpelès said Tuesday that a Ledger Flex bought at Singapore's airport contained a spy implant. Ledger pointed people back to its CryptoBilis update without confirming the Singapore device is connected.

## Trezor and OneKey move to lock down resellers

Competitors are treating this as a channel problem, which it is. Trezor says it has no reports of tampered devices from CryptoBilis and no evidence its products were affected, but it removed the reseller anyway and is shrinking its wider reseller network. In a letter to partners, Chief Commercial Officer Danny Sanders said notified resellers lose authorization on Jan. 1, 2027, and will get no new stock, though they can sell remaining inventory until then.

"There is not a single piece of evidence that Trezor devices have been compromised," Sanders wrote. "This is a preventive step, taken out of an abundance of caution."

OneKey reported no customer fund losses, revoked CryptoBilis' authorization, and said sellers operating under questionable legal entities will lose authorization as it reviews its own network. It is offering free replacements for OneKey devices bought through the reseller.

## What I keep coming back to

Every hardware wallet warning for years has ended with the same line: buy direct from the manufacturer. Most people nod and then buy from whoever has stock, because airports and electronics chains are convenient. This is what that convenience can cost.

The uncomfortable part is that nothing here was a software failure. Ledger's firmware did what it was supposed to do. The attack lived in the physical supply chain, in units that passed through a reseller's hands, and the only defense was never being in that pipeline at all. If the $86 million figure holds up, this will be one of the most expensive supply chain attacks crypto has seen. If it does not, the confirmed implant is bad enough on its own.

## Sources

- [The Block: Ledger confirms hardware implant in CryptoBilis reseller units as MediaMarkt suspends sales in Europe](https://www.theblock.co/news/business/2026-10-13-ledger-confirms-hardware-implant-cryptobilis-reseller-units-mediamarkt-suspends-sales-europe-418442)
