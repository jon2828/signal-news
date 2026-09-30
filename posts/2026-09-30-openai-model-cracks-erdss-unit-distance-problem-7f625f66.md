---
title: OpenAI model cracks Erdős's unit distance problem
date: 2026-09-30
topic: ai
score: 9
candidate_id: 7f625f66633806e0
sources: ["https://openai.com/index/model-disproves-discrete-geometry-conjecture"]
triage_reason: "Disproving an 80-year-old mathematical conjecture is a frontier-shifting milestone for AI capabilities."
---

OpenAI announced that one of its general‑purpose reasoning models has produced a proof that disproves a long‑standing conjecture about the planar unit distance problem.  

The conjecture dates back to 1946, when Paul Erdős asked how many pairs of points at distance 1 can appear among n points in the plane.  Mathematicians have spent almost eight decades tightening the bounds, but the best known lower bound grew only a hair faster than linear.  The prevailing belief was that a rescaled square‑grid construction was essentially optimal, giving about \(n^{1 + C/\log\log n}\) unit‑distance pairs for some constant C.

The OpenAI model generated an infinite family of point sets that achieve at least \(n^{1+\delta}\) unit‑distance pairs for infinitely many n, with \(\delta>0\).  The original proof did not spell out a concrete \(\delta\), but a refinement by Princeton professor Will Sawin shows that \(\delta\) can be taken as 0.014.  That pushes the growth rate well beyond the square‑grid bound and directly contradicts Erdős's conjectured upper limit of \(n^{1+o(1)}\).

The proof was not the product of a system trained specifically for geometry.  According to OpenAI, the model is a general‑purpose reasoning engine that was asked to tackle a suite of Erdős problems.  It arrived at the unit‑distance result on its own, then external mathematicians checked the argument and wrote a companion paper that explains the construction in detail.  The paper is linked from the OpenAI announcement.

Fields medalist Tim Gowers called the result "a milestone in AI mathematics" in the companion paper.  Number theorist Arul Shankar added, "In my opinion this paper demonstrates that current AI models go beyond just helpers to human mathematicians - they are capable of having original ingenious ideas, and then carrying them out to fruition."  Both comments underline how unexpected the breakthrough feels to the community.

Why does this matter beyond the narrow question?  First, the unit‑distance problem sits at the intersection of combinatorial geometry and number theory.  The new construction pulls ideas from algebraic number theory, something most geometers would not have tried on their own.  Second, the proof shows that a language model can navigate a deep, multi‑step argument without any problem‑specific prompting.  Mathematics offers a clean test: statements are precise, proofs can be verified line by line, and any mistake is fatal.  If an AI can produce a correct proof in a field it has never seen, the bar for machine reasoning has moved up dramatically.

That said, I remain cautious.  The result still depends on human verification, and the model's chain of thought is only partially disclosed.  We do not yet know how robust the approach is across other open problems, or whether the same model could discover a proof that truly outpaces human intuition without any human scaffolding.  The community will need more examples before we can say AI is a reliable research partner rather than a clever assistant.

Nobody knows how quickly this line of work will translate into practical tools for mathematicians.  For now, the headline is clear: an AI system has solved a problem that has resisted attack for almost a century, and it did so by bringing algebraic number theory into a geometric setting that most researchers would not have considered.

**Sources**

- OpenAI, "An OpenAI model has disproved a central conjecture in discrete geometry," May 20 2026, https://openai.com/index/model-disproves-discrete-geometry-conjecture.
