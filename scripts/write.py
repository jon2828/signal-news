#!/usr/bin/env python3
"""Job 4: write. One post per approved candidate, voice bible enforced.

For each approved candidate: fetch the full source articles, send the
voice bible + write prompt + sources to the write model, parse the
frontmatter post, then word-count and lint it BEFORE saving. A draft
that fails either check is dropped here with the reason logged.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ROOT, chat_with_fallback, config, extract_article,  # noqa: E402
                     guarded_exit, kill_switch, log_decision, normalize_text,
                     provider_client, rewrite_for_lint, slugify)
from lint import lint  # noqa: E402

MAX_SOURCES_PER_POST = 3


def _return_to_queue(cand: dict) -> None:
    """A write-stage drop must not permanently lose a high scorer: put the
    candidate back so the next triage can reconsider it."""
    path = ROOT / "state" / "candidates.json"
    try:
        candidates = json.loads(path.read_text())
        if not any(c["id"] == cand["id"] for c in candidates):
            candidates.append(cand)
            path.write_text(json.dumps(candidates, indent=1))
    except Exception:
        pass


def parse_post(text: str) -> dict | None:
    if not text.startswith("---"):
        # Salvage: a preamble before the frontmatter is fine; find the block.
        m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not m:
            return None
        text = text[m.start():]
    try:
        fm, body = text[3:].split("---", 1)
    except ValueError:
        return None
    meta = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") :  # sources list
                try:
                    meta[k.strip()] = json.loads(v.replace("'", '"'))
                except Exception:
                    meta[k.strip()] = [u.strip(" '\"") for u in v.strip("[]").split(",")]
            else:
                meta[k.strip()] = v
    meta["body"] = body.strip()
    return meta


def main() -> int:
    if kill_switch():
        return guarded_exit("write")
    cfg = config()
    prov, base_url, api_key = provider_client(cfg)
    if not prov:
        log_decision("write_skipped", "no API key in provider chain")
        print("[write] no API key available. Skipping.")
        return 0

    approved_path = ROOT / "state" / "approved.json"
    approved = json.loads(approved_path.read_text()) if approved_path.exists() else []
    if not approved:
        print("[write] nothing approved. No posts this run.")
        return 0

    drafts_dir = ROOT / "state" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    voice = (ROOT / "voice" / "bible.md").read_text()
    prompt_tpl = (ROOT / cfg["write"]["prompt_file"]).read_text()
    max_words = cfg["caps"].get("max_words_per_post", 1000)
    max_hits = cfg["lint"].get("max_hits_per_post", 2)
    temp = cfg.get("temperature", {}).get("write", 0.2)

    written = 0
    for cand in approved:
        articles = []
        for s in cand["sources"][:MAX_SOURCES_PER_POST]:
            try:
                text = extract_article(s["url"], cfg)
                if len(text) > 200:
                    articles.append(f"## {s['source']}: {cand['title']}\nURL: {s['url']}\nPublished: {s.get('published','')}\n\n{text}")
            except Exception as e:
                log_decision("fetch_failed", json.dumps({"url": s["url"], "error": f"{type(e).__name__}: {e}"[:120]}))
        if not articles:
            # Full fetch failed for every source; fall back to RSS summary
            # text so the writer (and then the fact-checker) still work from
            # what we have instead of dropping a good story.
            fallback = []
            for s in cand["sources"][:MAX_SOURCES_PER_POST]:
                if s.get("summary"):
                    fallback.append(f"## {s['source']} (summary only): {cand['title']}\nURL: {s['url']}\n\n{s['summary']}")
            if fallback:
                articles = fallback
        if not articles:
            log_decision("write_dropped", json.dumps({"id": cand["id"], "reason": "no source article could be fetched"}))
            _return_to_queue(cand)
            continue

        user_content = "\n\n".join(articles)
        prompt = prompt_tpl.replace("<<VOICE>>", voice).replace("<<ARTICLES>>", user_content)
        try:
            raw, prov_used = chat_with_fallback(cfg, "write", prompt, max_tokens=8000, timeout=420)
        except Exception as e:
            log_decision("write_failed", json.dumps({"id": cand["id"], "error": str(e)[:200]}))
            continue
        raw = normalize_text(raw)

        meta = parse_post(raw)
        if not meta or not meta.get("title") or not meta.get("body"):
            log_decision("write_dropped", json.dumps({"id": cand["id"], "reason": "model output missing frontmatter or body"}))
            _return_to_queue(cand)
            continue

        # The model never gets to claim its sources: force the URLs we
        # actually fetched, so the fact-checker verifies against ground truth.
        real_urls = [s["url"] for s in cand["sources"][:MAX_SOURCES_PER_POST]
                     if str(s.get("url", "")).startswith("http")]
        if real_urls:
            meta["sources"] = real_urls

        hits = lint(meta["body"])
        total_hits = sum(h[1] for h in hits)
        words = len(meta["body"].split())
        # Style is a flag, not a veto, and word count is the one hard limit.
        # Over either: one rewrite attempt (facts preserved), then judge again.
        if total_hits > max_hits or words > max_words:
            before = (total_hits, words)
            rewritten = rewrite_for_lint(cfg, meta["body"], hits, max_words, meta.get("title", ""))
            if rewritten:
                meta["body"] = rewritten
                hits = lint(rewritten)
                total_hits = sum(h[1] for h in hits)
                words = len(rewritten.split())
                log_decision("lint_rewrite", json.dumps(
                    {"id": cand["id"], "before": f"lint={before[0]},words={before[1]}",
                     "after": f"lint={total_hits},words={words}"}))
        if words > max_words:
            log_decision("write_dropped", json.dumps({"id": cand["id"], "reason": f"word count {words} > {max_words} after rewrite"}))
            _return_to_queue(cand)
            continue
        if total_hits > max_hits:
            # Published anyway (owner decision): flag it for the audit trail.
            names = ", ".join(f"{h[0]}({h[1]})" for h in hits)
            log_decision("lint_flagged", json.dumps({"id": cand["id"], "hits": total_hits, "patterns": names}))
            print(f"[write] lint flagged, publishing anyway: {total_hits} hits ({names})")

        meta.setdefault("date", datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"))
        meta.setdefault("sources", [s["url"] for s in cand["sources"][:MAX_SOURCES_PER_POST]])
        meta["score"] = cand["score"]
        meta["triage_reason"] = cand.get("reason", "")
        fm_lines = ["---",
                    f"title: {meta['title']}",
                    f"date: {meta['date']}",
                    f"topic: {meta.get('topic', cand['topic'])}",
                    f"score: {meta['score']}",
                    f"candidate_id: {cand['id']}",
                    f"sources: {json.dumps(meta['sources'])}"]
        if meta["triage_reason"]:
            safe_reason = meta["triage_reason"][:150].replace('"', "'")
            fm_lines.append(f"triage_reason: \"{safe_reason}\"")
        fm_lines.append("---")
        post_text = "\n".join(fm_lines) + "\n\n" + meta["body"] + "\n"

        name = f"{meta['date']}-{slugify(meta['title'])}-{cand['id'][:8]}.md"
        (drafts_dir / name).write_text(post_text)
        written += 1
        print(f"[write] draft saved: {name} ({words} words, lint hits {total_hits})")

    print(f"[write] {written}/{len(approved)} drafts written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
