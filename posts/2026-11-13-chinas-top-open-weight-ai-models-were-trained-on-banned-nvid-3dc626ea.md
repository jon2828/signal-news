---
title: China's top open-weight AI models were trained on banned Nvidia chips
date: 2026-11-13
topic: ai
story: china-nvidia-chips
score: 7
candidate_id: 3dc626ea28ff3a7d
sources: ["https://techcrunch.com/2026/11/13/export-banned-nvidia-chips-are-behind-chinas-most-powerful-ai-models-uh-oh-jensen/"]
triage_reason: "Reveals potential failure of US export controls, a critical geopolitical and regulatory issue for AI."
---

China's leading open-weight AI models were trained on Nvidia chips the US government banned from export to China, according to new research reported by TechCrunch.

Will DePue, a former OpenAI researcher who leads the nonprofit Unemployment Labs, analyzed the weights of models released by DeepSeek, Moonshot AI, MiniMax, and Ant Group. Model weights retain traces of the hardware used to train them, and DePue says he found compelling evidence that Moonshot's Kimi K3 releases and DeepSeek's V4 models bear fingerprints from training on Blackwell GPUs. Blackwell is banned from export to China or Chinese-owned firms.

The claim matches what the White House has been saying. Technology adviser Michael Kratsios said earlier this year that Moonshot had used export-banned Nvidia chips, citing US intelligence sources.

## The Jensen Huang angle

The timing is something. Nvidia parted ways with CEO Jensen Huang this week after he admitted to an affair with Alice Huang, an executive at Megaspeed, a company implicated in smuggling Nvidia chips into China. Alice Huang has also been alleged to be an agent of China's intelligence service. Bloomberg reported Friday that a company linked to her was involved in moving banned chips to a data center in Shanghai.

TechCrunch notes that Nvidia's potential corporate liability for export control violations likely factored into the split. That tracks. Nvidia and Jensen Huang both vouched for Megaspeed's data centers, saying company officials had visited and confirmed they were legitimate. If investigators confirm smuggling took place and he knew about it, that vouching turns into a serious problem.

## The scale of the leak

Epoch AI, a nonprofit research organization, estimates about two million advanced chips entered China in 2024 and 2025 through schemes designed to hide their final destination.

There is a legal gray zone worth naming. These models were not necessarily trained on chips sitting inside China, and export laws were not necessarily broken. Renting compute in offshore data centers has become a popular way for Chinese firms to access US silicon, and it has driven an industrial buildout in Malaysia. Epoch estimates 275,000 Nvidia AI accelerators were imported to Malaysia in 2024 and 2025.

Sam Bresnick, a researcher at Georgetown's Center for Security and Emerging Technology, told TechCrunch it makes no sense to him that Chinese companies are blocked from chips in mainland China, Hong Kong, and Macau, but can "just go over to Malaysia" and do whatever they want. He is right, and the DePue research is what that loophole looks like in practice.

## The part nobody can explain

Then there is the mystery of the H200, the less powerful chip the Trump administration lets Nvidia export provided shipments take a circuitous route so the US can claim a 25% tariff. Some 600,000 H200 chips are reportedly stockpiled in Hong Kong, awaiting shipment into China, and nobody agrees on why Beijing has not cleared them. Theories include preparation for a trade deal and concerns about surveillance technology in the chips. Graham Webster, a Stanford research scholar focused on US-China tech policy, says he does not buy the idea that holding the chips back would drive domestic production, since demand is so large.

## My take

The export control regime had one job: keep China's frontier labs off the best American silicon. By the evidence in this research, it failed at that job. The chips got through, or the compute did, and the models got trained anyway. What the controls actually produced was a smuggling economy and a data center boom in Malaysia. Plus, apparently, the end of Jensen Huang's run at Nvidia.

The Culper detail is the kicker. The short-selling firm that flagged Nvidia's "China problem" back in May was not betting on a US crackdown. It was betting that Beijing would respond to the bans by recommitting to its own chip industry, and that billions in Chinese demand for Nvidia would dry up. If that happens, Nvidia loses the market either way. The only question is whether the chips keep leaking in the meantime.

Commerce Secretary Howard Lutnick, whose agencies license chip exports, could reportedly lose his job over investigators who were too cozy with Nvidia. Nobody knows how this plays out. But "the bans are working" is a hard case to make this week.

## Sources

- [TechCrunch: Export-banned Nvidia chips are behind China's most powerful AI models](https://techcrunch.com/2026/11/13/export-banned-nvidia-chips-are-behind-chinas-most-powerful-ai-models-uh-oh-jensen/)
