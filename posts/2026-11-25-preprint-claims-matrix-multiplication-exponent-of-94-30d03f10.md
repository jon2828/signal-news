---
title: Preprint claims matrix multiplication exponent of 9/4
date: 2026-11-25
topic: ai
story: matrix-multiplication-breakthrough
score: 7
candidate_id: 30d03f10571df261
sources: ["https://github.com/openai/math/blob/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/paper.pdf"]
triage_reason: "Frontier AI research result from OpenAI that could significantly impact computational efficiency."
---

A preprint in the **openai/math** repository on GitHub claims that matrix multiplication can be done in \(O(n^{2.25})\) time. The paper lives in a folder called `The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026`, and the PDF (1.03 MB) was added to the repo on November 24, 2026.

## What we actually know

* The PDF's title is *"The matrix multiplication exponent is nine fourths"* and the abstract (where present) states an exponent of \(9/4 = 2.25\).
* The file size shown on GitHub is 1.03 MB.
* The repository does not contain a separate blog post, press release, or other explanatory material.
* The PDF does not prominently display an author list on its first page; the authors, if any, are only mentioned in the internal metadata.

## Why I am not excited yet

A claim of this magnitude needs more than a single file in a repo. Independent verification, ideally through peer‑reviewed publication or at least a community‑wide audit, is required before the result can be taken as established. The lack of a clear author attribution and the absence of any accompanying discussion mean that the community has not yet had the opportunity to scrutinize the proof.

Preprints are the usual venue for bold theoretical claims, and many such claims are later refuted. That fact alone does not invalidate this work, but it does mean we should treat the result cautiously until experts have had a chance to examine it.

If the proof holds, the impact would be far‑reaching: textbooks on algorithms would need updating, and the cost of training large AI models, whose workloads are dominated by matrix multiplication, could drop substantially. Conversely, if the proof contains a flaw, the claim will likely be dismissed once the community reviews it.

## Sources

- [Matrix Multiplication is \(O(n^{2.25})\) [pdf] (openai/math on GitHub)](https://github.com/openai/math/blob/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/paper.pdf)
