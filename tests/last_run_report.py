#!/usr/bin/env python3
"""What did the newest pipeline run decide? Focus: the new lint policy."""
import collections
import json
from pathlib import Path

ROOT = Path("/home/jarvis/ai-bitcoin-news")
rows = [json.loads(l) for l in (ROOT / "state" / "decisions.jsonl").read_text().splitlines() if l.strip()]
recent = [r for r in rows if r["ts"] >= "2026-10-04T17:50"]
print("decisions since the lint change:", dict(collections.Counter(r["action"] for r in recent)))
print()
for r in recent:
    if r["action"] in ("lint_rewrite", "lint_flagged", "lint_rewrite_failed", "published",
                       "announced", "write_dropped", "edit_dropped", "over_cap", "rejected",
                       "stale_rejected", "catchup_allowance"):
        detail = r["detail"]
        if r["action"] in ("rejected", "stale_rejected") and len(detail) > 70:
            continue
        print(f"  {r['ts'][11:19]} {r['action']}: {detail[:150]}")
print()
posts = sorted(p.name for p in (ROOT / "posts").glob("*.md"))
drafts = sorted(p.name for p in (ROOT / "state" / "drafts").glob("*.md"))
print("posts:", len(posts), "| drafts pending:", len(drafts))
for d in drafts:
    print("   pending:", d[:75])
print("newest posts:")
for p in posts[-3:]:
    print("   ", p[:75])
