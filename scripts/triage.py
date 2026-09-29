#!/usr/bin/env python3
"""Job 3: triage. The decision step. Score candidates with an LLM.

Sends candidates in one batch to the triage model, applies the per-source
weight, keeps everything scoring >= min_triage_score, caps at
posts_per_run and the daily cap. Every score and rejection is logged so
the repo history shows why something ran or didn't.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ROOT, chat_with_fallback, config, guarded_exit,  # noqa: E402
                     kill_switch, log_decision, parse_json_blob, provider_client)


def posts_published_today() -> int:
    posts = ROOT / "posts"
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    n = 0
    if posts.exists():
        for p in posts.glob("*.md"):
            try:
                for line in p.read_text().splitlines()[:10]:
                    if line.startswith("date:"):
                        if line.split(":", 1)[1].strip() == today:
                            n += 1
                        break
            except Exception:
                continue
    return n


def main() -> int:
    if kill_switch():
        return guarded_exit("triage")
    cfg = config()
    prov, base_url, api_key = provider_client(cfg)
    if not prov:
        log_decision("triage_skipped", "no API key in provider chain")
        print("[triage] no API key available (set GROQ_API_KEY or OPENROUTER_API_KEY). Skipping this run.")
        return 0

    candidates = json.loads((ROOT / "state" / "candidates.json").read_text())
    if not candidates:
        print("[triage] no candidates. Nothing to score.")
        return 0

    caps = cfg["caps"]
    already = posts_published_today()
    room = caps["posts_per_day"] - already
    if room <= 0:
        log_decision("triage_skipped", f"daily cap reached ({already} posts today)")
        print(f"[triage] daily cap reached ({already}/{caps['posts_per_day']} posts today). Skipping.")
        return 0
    take = min(room, caps["posts_per_run"])

    feeds_cfg = {f["name"]: f for f in json.loads((ROOT / "config" / "feeds.json").read_text())["feeds"]}
    lines = []
    for c in candidates[:60]:  # batch cap
        weight = feeds_cfg.get(c["sources"][0]["source"], {}).get("weight", 1.0)
        src_names = ", ".join(s["source"] for s in c["sources"])
        summaries = " | ".join(s["summary"][:200] for s in c["sources"][:3])
        lines.append(f'id: {c["id"]}\ntitle: {c["title"]}\nsources: {src_names} ({c["source_count"]})\nsummaries: {summaries}')

    # Score in small batches: reasoning models stay inside their token budget
    # and JSON adherence holds. 20 candidates per call.
    prompt_tpl = (ROOT / cfg["triage"]["prompt_file"]).read_text()
    no_preamble = ("\nAdditional output rule: skip any preamble or planning text. "
                   "Your ENTIRE response is the JSON array, nothing else.")
    scores = []
    for i in range(0, len(lines), 20):
        chunk = "\n---\n".join(lines[i:i + 20])
        prompt = prompt_tpl.replace("<<CANDIDATES>>", chunk) + no_preamble
        try:
            raw, _ = chat_with_fallback(cfg, "triage", prompt, max_tokens=4000, temperature=0.0)
        except Exception as e:
            log_decision("triage_failed", json.dumps({"batch": i // 20, "error": str(e)[:200]}))
            print(f"[triage] batch {i // 20} failed (all providers). Logged; candidates kept for next run.")
            continue
        try:
            scores.extend(parse_json_blob(raw))
        except Exception as e:
            log_decision("triage_failed", json.dumps({"batch": i // 20, "error": f"unparseable: {str(e)[:150]}"}))
            print(f"[triage] batch {i // 20} unparseable. Logged.")
            continue

    approved, rejected = [], []
    by_id = {c["id"]: c for c in candidates}
    for s in scores:
        c = by_id.get(str(s.get("id")))
        if not c:
            continue
        weight = feeds_cfg.get(c["sources"][0]["source"], {}).get("weight", 1.0)
        effective = min(10, round(float(s["score"]) * weight))
        entry = {"id": c["id"], "title": c["title"], "topic": c["topic"],
                 "score": effective, "raw_score": s["score"], "weight": weight,
                 "reason": s.get("reason", ""), "sources": c["sources"]}
        (approved if effective >= caps["min_triage_score"] else rejected).append(entry)

    approved.sort(key=lambda e: -e["score"])
    overflow = approved[take:]
    approved = approved[:take]
    # Over-cap 7+ scorers keep their candidate (not removed below) so the next
    # run re-considers them; they get an explicit over_cap decision here.
    # Keep only unscored-and-not-over-cap candidates for future runs: re-scoring
    # final decisions every run wastes tokens.
    final_ids = {e["id"] for e in rejected} | {e["id"] for e in approved}
    unscored = [c for c in candidates if c["id"] not in final_ids and c["id"] not in {e["id"] for e in overflow}]
    (ROOT / "state" / "candidates.json").write_text(json.dumps(unscored, indent=1))
    (ROOT / "state" / "approved.json").write_text(json.dumps(approved, indent=1))

    for e in rejected:
        log_decision("rejected", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e.get("score"), "reason": e.get("reason", "")[:200]}))
    for e in overflow:
        log_decision("over_cap", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e["score"], "reason": e.get("reason", "")[:200]}))
    for e in approved:
        log_decision("approved", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e["score"], "reason": e.get("reason", "")[:200]}))
    print(f"[triage] {len(scores)} scored via {prov}: {len(approved)} approved "
          f"(cap {take}), {len(rejected)} rejected. Scores and reasons in state/decisions.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
