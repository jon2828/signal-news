---
title: Ledger says spy chip in CryptoBilis-sold wallets sent recovery phrases over LTE
date: 2026-10-13
topic: bitcoin
score: 8
candidate_id: 9af5acea5c334ce7
sources: ["https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network"]
triage_reason: "Confirmed spy chip transmitting wallet keys is a major security breach with a named company, corroborated by retailer pullout coverage elsewhere."
retracted: true
retracted_reason: "Duplicate: the same candidate was accidentally published twice in one day."
---

Ledger says a covert chip planted inside some of its hardware wallets sold by Southeast Asian reseller CryptoBilis read users' 24-word recovery phrases off the device screen and transmitted them to attackers over a mobile network. The company laid out the mechanism in an investigation update on X Tuesday, the first public explanation of how the CryptoBilis-linked thefts actually worked.

## How the implant worked

The details are grim, and kind of elegant. According to Ledger, the spy chip sat inside the device enclosure. When a user set up the wallet and the screen displayed the recovery phrase, the implant's microcontroller recognized and decoded the words, then sent them out over LTE using an eSIM, the same data technology cellphones use. From the victim's side, nothing looked unusual.

The recovery phrase is the master key to a wallet. Whoever has it can recreate the wallet anywhere and move the funds, no physical device needed.

Here is the part that should bother anyone who bought a Ledger for the security marketing. The implant did not touch the secure element, the chip that is supposed to protect the private keys. It did not modify the operating system, and it did not alter transactions or signatures. Ledger is framing this as a physical supply-chain attack rather than a breach of its software or internal systems, and on the facts given, that framing holds. But it also means the tamper resistance in the secure chip was irrelevant. The attackers just watched the screen.

## The losses

Ledger has not confirmed a victim count or a total figure. Onchain researchers estimate losses of up to $93.2 million across more than 300 wallets, and Tether froze $10 million in USDT tied to the theft.

Ledger says every confirmed loss in the Oct. 9 incident involved a device sold by CryptoBilis, and that it has not verified any theft from a signer bought elsewhere. One wrinkle: Mark Karpeles, the former Mt. Gox CEO, claimed he found a spy implant in a Ledger Flex purchased at Singapore Airport. Ledger says it is examining reports of implants in other devices and locations. If the Karpeles claim checks out, this stops being a one-reseller story.

## What Ledger is doing

CryptoBilis has stopped selling Ledger signers, according to Ledger. The company told customers who bought one from the reseller not to initialize it. Anyone who already did should move their assets to a new device with a freshly generated recovery phrase.

CTO Charles Guillemet said on X that "Ledger is reviewing its reseller controls and anti-tamper protections" and invited researchers and other vendors to work on tamper detection and chain-of-custody practices. CEO Pascal Gauthier said the company is "reviewing the controls that apply to our direct sales and to resellers, and we will share what we can," adding that the investigation is ongoing to determine who tampered with the devices and where in the distribution chain it happened.

## My read

The obvious takeaway is buy direct from the manufacturer, which is also the self-serving takeaway Ledger wants you to reach. Fair enough. The harder problem is that this attack bypassed every security feature Ledger advertises by simply not engaging with them. Detecting a second radio inside a sealed enclosure is not something a normal buyer can do, and "reviewing reseller controls" is what a company says before it knows what went wrong.

Nobody has named who built the implant or where it entered the chain. Until that gets answered, the $93.2 million question is whether CryptoBilis was the target or just the easiest door.

## Sources

- [CoinDesk: Ledger says 'spy' chip inside CryptoBilis Ledger devices transmitted wallet keys over mobile network](https://www.coindesk.com/tech/2026/10/13/ledger-says-spy-chip-inside-cryptobilis-ledger-devices-transmitted-wallet-keys-over-mobile-network)
