#!/usr/bin/env python3
"""Job 5: edit. Independent fact-check pass with a different model.

Every draft goes to the edit model with its source articles. Verdicts:
publish -> straight to posts/, rewrite -> re-check the revised post
(word count + lint) then publish or drop, drop -> archived to
state/declined/ with the reason logged. This is the difference between
a news site and slop.
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ROOT, chat_with_fallback, config, extract_article,  # noqa: E402
                     guarded_exit, kill_switch, log_decision, normalize_text,
                     provider_client, slugify)
from lint import lint  # noqa: E402

MAX_SOURCES_PER_POST = 3


def front_meta(text: str) -> dict:
    meta = {}
    if text.startswith("---"):
        try:
            fm = text[3:].split("---", 1)[0]
            for line in fm.splitlines():
                if line.startswith("sources:"):
                    try:
                        meta["sources"] = json.loads(line.split(":", 1)[1].strip().replace("'", '"'))
                    except Exception:
                        meta["sources"] = []
                elif line.startswith("candidate_id:"):
                    meta["candidate_id"] = line.split(":", 1)[1].strip()
                elif line.startswith("title:"):
                    meta["title"] = line.split(":", 1)[1].strip()
        except ValueError:
            pass
    return meta


def _requeue_by_candidate_id(candidate_id: str) -> None:
    """Edit-stage drop with unverifiable sources: put the candidate back in
    the queue using the entry this run's triage left in approved.json."""
    import json as _json
    try:
        approved = _json.loads((ROOT / "state" / "approved.json").read_text())
        cand = next((e for e in approved if e.get("id") == candidate_id), None)
        if cand:
            from _common import _return_to_queue
            _return_to_queue({"id": cand["id"], "title": cand["title"], "topic": cand.get("topic", "both"),
                              "source_count": len(cand.get("sources", [])), "sources": cand.get("sources", [])})
    except Exception:
        pass


def main() -> int:
    if kill_switch():
        return guarded_exit("edit")
    cfg = config()
    prov, base_url, api_key = provider_client(cfg)
    if not prov:
        log_decision("edit_skipped", "no API key in provider chain")
        print("[edit] no API key available. Drafts stay in state/drafts/.")
        return 0

    drafts = sorted((ROOT / "state" / "drafts").glob("*.md")) if (ROOT / "state" / "drafts").exists() else []
    if not drafts:
        print("[edit] no drafts to check.")
        return 0

    posts_dir = ROOT / "posts"
    declined_dir = ROOT / "state" / "declined"
    posts_dir.mkdir(exist_ok=True)
    declined_dir.mkdir(parents=True, exist_ok=True)
    prompt_tpl = (ROOT / cfg["edit"]["prompt_file"]).read_text()
    write_model = cfg["models"]["write"][prov]
    edit_model = cfg["models"]["edit"][prov]
    max_words = cfg["caps"].get("max_words_per_post", 1000)
    max_hits = cfg["lint"].get("max_hits_per_post", 2)

    published = 0
    for draft in drafts:
        text = draft.read_text()
        meta = front_meta(text)
        articles = []
        for url in (meta.get("sources") or [])[:MAX_SOURCES_PER_POST]:
            try:
                t = extract_article(url, cfg)
                if len(t) > 200:
                    articles.append(f"## Source: {url}\n\n{t}")
            except Exception as e:
                log_decision("fetch_failed", json.dumps({"url": url, "error": f"{type(e).__name__}: {e}"[:120]}))
        if not articles:
            log_decision("edit_dropped", json.dumps({"file": draft.name, "reason": "sources unreachable, cannot verify"}))
            _requeue_by_candidate_id(meta.get("candidate_id", ""))
            shutil.move(str(draft), str(declined_dir / draft.name))
            continue

        prompt = (prompt_tpl.replace("<<ARTICLES>>", "\n\n".join(articles))
                  .replace("<<POST>>", text))
        try:
            raw, prov_used = chat_with_fallback(cfg, "edit", prompt, max_tokens=8000, timeout=420)
        except Exception as e:
            log_decision("edit_failed", json.dumps({"file": draft.name, "error": str(e)[:200]}))
            continue  # keep draft for next run

        try:
            from _common import parse_json_blob
            verdict = parse_json_blob(raw)
        except Exception:
            log_decision("edit_failed", json.dumps({"file": draft.name, "error": "unparseable verdict; kept for next run"}))
            continue

        v = str(verdict.get("verdict", "")).lower()
        reason = str(verdict.get("reason", ""))[:250]

        if v == "publish":
            (posts_dir / draft.name).write_text(text)
            draft.unlink()
            published += 1
            log_decision("published", json.dumps({"file": draft.name, "verdict": "publish", "reason": reason}))
        elif v == "rewrite" and verdict.get("revised_post"):
            revised = normalize_text(str(verdict["revised_post"]).strip())
            hits = lint(revised)
            total_hits = sum(h[1] for h in hits)
            # word count on body only
            body = revised
            if revised.startswith("---"):
                try:
                    body = "---".join(revised[3:].split("---")[1:])
                except IndexError:
                    pass
            words = len(body.split())
            if words <= max_words and total_hits <= max_hits:
                (posts_dir / draft.name).write_text(revised + "\n")
                draft.unlink()
                published += 1
                log_decision("published", json.dumps({"file": draft.name, "verdict": "rewrite", "reason": reason}))
            else:
                log_decision("edit_dropped", json.dumps({"file": draft.name, "reason": f"rewrite failed checks: words={words}, lint={total_hits}"}))
                shutil.move(str(draft), str(declined_dir / draft.name))
        else:
            log_decision("edit_dropped", json.dumps({"file": draft.name, "verdict": v or "unknown", "reason": reason}))
            shutil.move(str(draft), str(declined_dir / draft.name))

    print(f"[edit] {published}/{len(drafts)} drafts published, rest verified-or-dropped. "
          f"Every decision in state/decisions.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
