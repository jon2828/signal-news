#!/usr/bin/env python3
"""Job 2: dedupe. Cluster pending items into story candidates. No LLM.

Exact URL-hash matches merge first, then title similarity: token-set
overlap above a threshold merges two items into one candidate with
combined sources. Multiple sources on one candidate is a credibility
signal the triage step will use, not spam.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, config, guarded_exit, kill_switch, log_decision  # noqa: E402

STOP = {"the", "a", "an", "of", "in", "to", "for", "on", "and", "is", "at", "as",
        "with", "over", "after", "from", "by", "new", "how", "what", "why"}


def tokens(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9$]+", title.lower())
    return {w for w in words if w not in STOP and len(w) > 2}


def similarity(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def main() -> int:
    if kill_switch():
        return guarded_exit("dedupe")
    cfg = config()
    pending_path = ROOT / "state" / "pending.json"
    candidates_path = ROOT / "state" / "candidates.json"
    pending = json.loads(pending_path.read_text()) if pending_path.exists() else []
    existing = json.loads(candidates_path.read_text()) if candidates_path.exists() else []
    # Cleaned candidates are stored without _tokens; recompute from the title.
    for c in existing:
        c.setdefault("_tokens", tokens(c["title"]))

    clusters: list[dict] = list(existing)
    for item in pending:
        toks = tokens(item["title"])
        merged = False
        for c in clusters:
            if similarity(toks, c["_tokens"]) >= 0.6:
                c["sources"].append({"source": item["source"], "url": item["url"],
                                     "summary": item["summary"], "published": item["published"]})
                c["_tokens"] |= toks
                merged = True
                break
        if not merged:
            clusters.append({
                "id": item["id"],
                "title": item["title"],
                "topic": item["topic"],
                "sources": [{"source": item["source"], "url": item["url"],
                             "summary": item["summary"], "published": item["published"]}],
                "_tokens": toks,
            })

    out = []
    for c in clusters:
        urls = {s["url"] for s in c["sources"]}
        seen_urls, srcs = set(), []
        for s in c["sources"]:
            if s["url"] not in seen_urls:
                seen_urls.add(s["url"])
                srcs.append(s)
        out.append({"id": c["id"], "title": c["title"], "topic": c["topic"],
                    "source_count": len(srcs), "sources": srcs})

    candidates_path.write_text(json.dumps(out, indent=1))
    pending_path.write_text("[]")
    n_multi = len([c for c in out if c["source_count"] > 1])
    print(f"[dedupe] {len(pending)} items -> {len(out)} candidates ({n_multi} multi-source), "
          f"{len(existing)} carried over from previous runs")
    log_decision("dedupe", f"{len(pending)} items -> {len(out)} candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
