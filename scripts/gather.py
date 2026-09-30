#!/usr/bin/env python3
"""Job 1: gather. Pull all feeds, keep new items only.

Reads config/feeds.json, fetches enabled feeds, normalizes items,
dedupes against state/seen.json, writes state/pending.json for the
dedupe step and updates state/seen.json. Feed failures are logged to
state/decisions.jsonl; the pipeline runs on what is left.
"""
import datetime
import hashlib
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, config, guarded_exit, kill_switch, log_decision  # noqa: E402

RSS_TITLE = ["title", "link", "description", "pubDate", "updated", "published", "summary", "content"]


def fetch(url: str, cfg: dict) -> bytes:
    timeout = cfg.get("fetch", {}).get("timeout_seconds", 20)
    ua = cfg.get("fetch", {}).get("user_agent", "Mozilla/5.0 (compatible; UnspentThoughtsBot/1.0)")
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(cfg.get("fetch", {}).get("max_bytes_per_feed", 300000))


def strip_tag(el) -> str:
    if el is None:
        return ""
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def parse_feed(xml_bytes: bytes, source: dict) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "item":  # RSS
            get = lambda name: strip_tag(el.find(name))
            items.append({
                "title": get("title"),
                "url": get("link") or strip_tag(el.find("atom:link")),
                "summary": get("description")[:600],
                "published": get("pubDate"),
                "source": source["name"],
                "topic": source["topic"],
            })
        elif tag == "entry":  # Atom
            get = lambda name: strip_tag(el.find(name))
            link = ""
            lel = el.find("atom:link")
            if lel is not None:
                link = lel.get("href", "")
            items.append({
                "title": get("title"),
                "url": link or get("atom:id"),
                "summary": get("summary") or get("content")[:600],
                "published": get("published") or get("updated"),
                "source": source["name"],
                "topic": source["topic"],
            })
    return [i for i in items if i["url"] and i["title"]]


def item_id(url: str) -> str:
    return hashlib.sha1(url.strip().lower().encode()).hexdigest()[:16]


def main() -> int:
    if kill_switch():
        return guarded_exit("gather")
    cfg = config()
    feeds = json.loads((ROOT / "config" / "feeds.json").read_text())["feeds"]
    seen_path = ROOT / "state" / "seen.json"
    pending_path = ROOT / "state" / "pending.json"
    seen = json.loads(seen_path.read_text()) if seen_path.exists() else {}
    pending = json.loads(pending_path.read_text()) if pending_path.exists() else []

    new_items, failed = [], []
    for src in feeds:
        if not src.get("enabled"):
            continue
        try:
            items = parse_feed(fetch(src["url"], cfg), src)
        except Exception as e:
            failed.append({"feed": src["name"], "error": f"{type(e).__name__}: {e}"[:120]})
            continue
        for it in items:
            iid = item_id(it["url"])
            if iid not in seen:
                it["id"] = iid
                seen[iid] = {"url": it["url"], "title": it["title"][:200],
                             "first_seen": datetime.datetime.now(datetime.UTC).isoformat()}
                new_items.append(it)

    pending.extend(new_items)
    STATE = ROOT / "state"
    STATE.mkdir(exist_ok=True)
    seen_path.write_text(json.dumps(seen, indent=1))
    pending_path.write_text(json.dumps(pending, indent=1))

    for f in failed:
        log_decision("feed_failed", json.dumps(f))
    n_enabled = len([f for f in feeds if f.get("enabled")])
    print(f"[gather] {len(new_items)} new items from {n_enabled} enabled feeds "
          f"({len(failed)} failed), {len(pending)} pending total")
    if failed:
        for f in failed:
            print(f"  - FAILED {f['feed']}: {f['error']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
