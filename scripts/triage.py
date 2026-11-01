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


def newest_source_age_days(cand: dict) -> int | None:
    """Age in days of the newest source timestamp, or None when no source
    carries a parseable date (treated as fresh, never dropped silently).
    Feeds use RFC-822 ('Thu, 12 Sep 2024 10:02:00 GMT') and ISO-8601."""
    import datetime as _dt
    import email.utils
    best = None
    for s in cand.get("sources", []):
        raw = (s.get("published") or "").strip()
        if not raw:
            continue
        stamp = None
        try:
            stamp = email.utils.parsedate_to_datetime(raw)
        except Exception:
            try:
                stamp = _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except Exception:
                stamp = None
        if stamp is None:
            continue
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=_dt.timezone.utc)
        if best is None or stamp > best:
            best = stamp
    if best is None:
        return None
    return (_dt.datetime.now(_dt.UTC) - best).days


def recent_post_titles(days: int = 3) -> list[str]:
    """Titles of posts published in the last `days` days. Used so the triage
    model can refuse to re-cover a story the site already published, and so
    near-identical resubmissions can be dropped deterministically."""
    import datetime as _dt
    cutoff = _dt.datetime.now(_dt.UTC) - _dt.timedelta(days=days)
    out = []
    posts = ROOT / "posts"
    if not posts.exists():
        return out
    for p in posts.glob("*.md"):
        try:
            title, date = "", ""
            for line in p.read_text().splitlines()[:10]:
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                elif line.startswith("date:"):
                    date = line.split(":", 1)[1].strip()
            if title and date:
                if _dt.datetime.fromisoformat(date).replace(tzinfo=_dt.timezone.utc) >= cutoff:
                    out.append(title)
        except Exception:
            continue
    return out


def _tokens(s: str) -> set[str]:
    import re as _re
    return {t for t in _re.findall(r"[a-z0-9]+", s.lower()) if len(t) > 2}


def title_overlap(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def _story_slug(raw: str) -> str:
    """Normalise a triage story label so trivial spelling drift cannot split one event."""
    import re as _re
    return _re.sub(r"[^a-z0-9]+", "-", str(raw or "").lower()).strip("-")


def recent_post_stories(days: int) -> list[tuple[str, str]]:
    """(story slug, title) for posts inside the window, newest data first.

    Posts written before the `story` field existed carry no label; they come
    back with an empty slug so the cap can still match them on title overlap
    rather than silently ignoring a week of unlabelled backlog.
    """
    import datetime as _dt
    cutoff = _dt.datetime.now(_dt.UTC) - _dt.timedelta(days=days)
    out: list[tuple[str, str]] = []
    posts = ROOT / "posts"
    if not posts.exists():
        return out
    for p in posts.glob("*.md"):
        try:
            title = date = story = ""
            for line in p.read_text().splitlines()[:16]:
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                elif line.startswith("date:"):
                    date = line.split(":", 1)[1].strip()
                elif line.startswith("story:"):
                    story = line.split(":", 1)[1].strip().strip("\"'")
            if not date:
                continue
            stamp = _dt.datetime.fromisoformat(date).replace(tzinfo=_dt.timezone.utc)
            if stamp < cutoff:
                continue
            out.append((_story_slug(story), title))
        except Exception:
            continue
    return out


def apply_story_cap(approved: list[dict], take: int, prior: list[tuple[str, str]],
                    cap: int, overlap: float = 0.5):
    """Fill `take` slots in score order, refusing a third post on one event.

    Jon's rule: two posts on a similar topic, then take the next candidate
    down the list. A story that keeps clearing the score gate still stops at
    `cap` inside the window, because repetition costs more reader trust than
    one skipped story costs coverage.

    Returns (picked, no_room, story_blocked) so the audit log can tell "the
    daily allowance was already full" apart from "this event had its turn".
    """
    counts: dict[str, int] = {}
    seen_titles = list(prior)
    for slug, _title in prior:
        if slug:
            counts[slug] = counts.get(slug, 0) + 1

    picked: list[dict] = []
    no_room: list[dict] = []
    story_blocked: list[dict] = []

    for entry in approved:
        if len(picked) >= take:
            no_room.append(entry)
            continue
        slug = _story_slug(entry.get("story", ""))
        if slug:
            if counts.get(slug, 0) >= cap:
                entry["story_blocked"] = slug
                entry["story_count"] = counts[slug]
                story_blocked.append(entry)
                continue
            counts[slug] = counts.get(slug, 0) + 1
            picked.append(entry)
            continue
        # No usable label: fall back to title overlap against what the window
        # already covered, so a missing slug cannot walk straight past the cap.
        hits = sum(1 for _s, t in seen_titles if title_overlap(entry["title"], t) >= overlap)
        if hits >= cap:
            entry["story_blocked"] = "unlabelled-overlap"
            entry["story_count"] = hits
            story_blocked.append(entry)
            continue
        seen_titles.append(("", entry["title"]))
        picked.append(entry)

    return picked, no_room, story_blocked


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

    # Freshness gate. A story the model scores highly is worthless if the
    # source published it years ago (an undated archive page scoring 9 got a
    # 356-day-old item published and announced as news). Reject candidates
    # whose newest source date is older than max_source_age_days. Undated
    # candidates are kept, so feeds that omit dates never lose real news.
    max_age = caps.get("max_source_age_days")
    if max_age:
        fresh, stale = [], []
        for c in candidates:
            age = newest_source_age_days(c)
            (stale if age is not None and age > max_age else fresh).append((c, age))
        for c, age in stale:
            log_decision("stale_rejected", json.dumps(
                {"id": c["id"], "age_days": age, "title": c["title"][:90]}))
        print(f"[triage] freshness gate: {len(stale)} stale rejected "
              f"(>{max_age}d), {len(fresh)} kept")
        candidates = [c for c, _ in fresh]
        if not candidates:
            print("[triage] nothing fresh to score this run.")
            return 0

    # Repeat-story gate. The Ledger implant story was published three times in
    # one day (and six times in five days) because dedupe only compared
    # candidates with each other, never with the site's own history. Two
    # layers: a deterministic near-identical-title check, and the recent
    # headlines injected into the triage prompt so paraphrased re-runs score low.
    recent = recent_post_titles(days=3)
    if recent:
        kept, dupes = [], []
        for c in candidates:
            hit = max(recent, key=lambda t: title_overlap(c["title"], t))
            if title_overlap(c["title"], hit) >= 0.7:
                dupes.append((c, hit))
            else:
                kept.append(c)
        for c, hit in dupes:
            log_decision("duplicate_rejected", json.dumps(
                {"id": c["id"], "title": c["title"][:90], "matches": hit[:90]}))
        if dupes:
            print(f"[triage] repeat gate: {len(dupes)} near-identical to a post "
                  f"from the last 3 days, {len(kept)} kept")
        candidates = kept
        if not candidates:
            print("[triage] nothing new to score this run.")
            return 0

    recent_block = "\n".join(f"- {t}" for t in recent[:30]) or "(none)"

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
        prompt = (prompt_tpl.replace("<<RECENT>>", recent_block)
                  .replace("<<CANDIDATES>>", chunk) + no_preamble)
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
                 "story": _story_slug(s.get("story", "")),
                 "score": effective, "raw_score": s["score"], "weight": weight,
                 "reason": s.get("reason", ""), "sources": c["sources"]}
        (approved if effective >= caps["min_triage_score"] else rejected).append(entry)

    approved.sort(key=lambda e: -e["score"])
    story_cap = int(caps.get("max_posts_per_story") or 0)
    if story_cap > 0:
        prior = recent_post_stories(int(caps.get("story_window_days") or 7))
        approved, overflow, story_blocked = apply_story_cap(approved, take, prior, story_cap)
    else:
        story_blocked = []
        overflow = approved[take:]
        approved = approved[:take]
    # Over-cap 7+ scorers keep their candidate (not removed below) so the next
    # run re-considers them; they get an explicit over_cap decision here.
    # Keep only unscored-and-not-over-cap candidates for future runs: re-scoring
    # final decisions every run wastes tokens.
    final_ids = {e["id"] for e in rejected} | {e["id"] for e in approved}
    blocked_ids = {e["id"] for e in overflow} | {e["id"] for e in story_blocked}
    unscored = [c for c in candidates if c["id"] not in final_ids and c["id"] not in blocked_ids]
    (ROOT / "state" / "candidates.json").write_text(json.dumps(unscored, indent=1))
    (ROOT / "state" / "approved.json").write_text(json.dumps(approved, indent=1))

    for e in rejected:
        log_decision("rejected", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e.get("score"), "reason": e.get("reason", "")[:200]}))
    for e in overflow:
        log_decision("over_cap", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e["score"], "reason": e.get("reason", "")[:200]}))
    for e in story_blocked:
        log_decision("story_capped", json.dumps(
            {"id": e["id"], "title": e["title"][:120], "score": e["score"],
             "story": e.get("story_blocked"), "already_published": e.get("story_count"),
             "reason": e.get("reason", "")[:160]}))
    for e in approved:
        log_decision("approved", json.dumps({"id": e["id"], "title": e["title"][:120],
                                             "score": e["score"], "reason": e.get("reason", "")[:200]}))
    print(f"[triage] {len(scores)} scored via {prov}: {len(approved)} approved "
          f"(cap {take}), {len(rejected)} rejected, {len(story_blocked)} held back "
          f"for story repetition. Scores and reasons in state/decisions.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
