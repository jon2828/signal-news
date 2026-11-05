---
title: OpenAI's kernel pipeline turned 2,308 candidates into 948 root exploits
date: 2026-11-04
topic: ai
story: openai-linux-vulns
score: 8
candidate_id: a4f4c423c5426033
sources: ["https://openai.com/index/a-thousand-fewer-paths-to-root", "https://openai.com/index/a-thousand-fewer-paths-to-root/"]
triage_reason: "Autonomous AI pipeline finding and patching 948 Linux kernel privilege-escalation vulnerabilities is a major AI capability result with security implic"
---

# OpenAI's kernel pipeline turned 2,308 candidates into 948 root exploits

*Date: 2026-11-04*

OpenAI says a prototype pipeline built on an upcoming cyber model scanned the Linux kernel and produced 948 local privilege escalation (LPE) exploits, the kind that turn an unprivileged local user into root.

The numbers, from OpenAI's own write‑up, are:

- **2,308** candidate findings
- **1,724** dynamically reproduced vulnerabilities
- **948** working LPE exploits

Human researchers reviewed the outputs, then reported the vulnerabilities to kernel maintainers with candidate patches attached, starting with the critical issues in line with the Linux kernel community's guidance. The effort is part of OpenAI's *Patch the Planet* initiative, which in June highlighted that GPT‑5.5 Cyber had identified Linux kernel bugs and built **24** LPE exploits to validate and report them. The current work expands that into a full pipeline.

---

## How the pipeline works

The system consists of five stages, all driven by an upcoming cyber model:

1. **Vulnerability discovery** - Scout agents scan the repository and select high‑value audit targets.
2. **Dynamic validation** - Triage agents attempt to reproduce each candidate in an isolated VM with Kernel Address Sanitizer (KASAN).
3. **Exploitability assessment** - The agents test whether a validated vulnerability can lead to information disclosure or privilege escalation.
4. **Patch generation** - Candidate patches are produced for each confirmed issue.
5. **Human review** - Security researchers evaluate the exploit, patch, and severity before reporting to maintainers.

### Scout agents

Scout agents identified **5,034** audit targets, covering about **2.8 million** lines of code - roughly **7 %** of the Linux kernel's ~40 million lines. This focused effort reduced the audit surface and cost. The stage cost **$3,426** in API credits.

### Analyst agents

Analyst agents examined the audit targets and, after deduplication, produced **2,308** candidate findings within **12 hours**. This stage cost **$316,549** in API credits.

### Validation and beyond

For each candidate, a triage agent generated a proof‑of‑concept, ran it in an isolated VM with KASAN, observed the output and console, and iteratively refined the test. Only findings that were reachable by a low‑privileged user, required no special capabilities, and showed measurable memory corruption progressed to the next stages.

The pipeline then assessed exploitability, generated patches, and bundled a root‑cause analysis, minimal crashing PoC, candidate patch, and full exploit for human review.

---

## The bill

OpenAI published per‑stage API costs, which are useful but sizable:

- **Scout stage:** $3,426
- **Analyst stage:** $316,549

OpenAI notes these figures are **upper bounds**; better harness engineering could reduce them substantially.

---

## A cautious perspective

The post is both a research report and a product announcement. The central model is described only as *"an upcoming cyber model,"* and all performance numbers are self‑reported. There is no independent verification of the **948** exploits, nor a third‑party assessment of how many would succeed against a current kernel.

Coordinated disclosure with patches attached and a focus on critical issues aligns with responsible practice. However, the same pipeline could, in theory, be turned into an offensive tool if used without a Patch the Planet partner.

The asymmetry is worth noting: OpenAI's team could not manually triage the volume of candidates, prompting automation of both discovery and validation. The remaining bottlenecks are human reviewer capacity and maintainer bandwidth. Publicly, the kernel maintainers have not indicated a request for a flood of such reports, suggesting they are managing the intake cautiously.

If the cost of mass‑producing root exploits drops dramatically, defenders benefit, but well‑funded attackers could also leverage the same methodology. The ultimate impact will depend on how quickly patches are integrated and how the community balances disclosure speed with review capacity.

---

## Sources

- [A thousand fewer paths to root](https://openai.com/index/a-thousand-fewer-paths-to-root)
