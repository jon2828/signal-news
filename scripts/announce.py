#!/usr/bin/env python3
"""Job 7 (optional): announce. Post each newly published article to X.

Reads posts/*.md, skips anything already announced (state/announced.json),
composes a post under 280 chars (title + link), signs with OAuth 1.0a
(pure stdlib, tokens never expire), and posts to the X API v2.

Secrets (env): X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.
If any are missing, this job exits 0 without posting — the pipeline works
without X entirely.
"""
import base64
import hashlib
import hmac
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, config, guarded_exit, kill_switch, log_decision  # noqa: E402

API = "https://api.x.com/2/tweets.json"


def oauth1_header(method: str, url: str, creds: dict) -> str:
    params = {
        "oauth_consumer_key": creds["api_key"],
        "oauth_nonce": base64.b64encode(hashlib.sha256(
            (creds["access_token"] + str(__import__("time").time_ns())).encode()).digest()).decode()[:32],
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_timestamp": str(int(__import__("time").time())),
        "oauth_token": creds["access_token"],
        "oauth_version": "1.0",
    }
    base_items = sorted(params.items())
    param_str = "&".join(f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
                         for k, v in base_items)
    base_url = url.split("?")[0]
    base_str = "&".join([method.upper(), urllib.parse.quote(base_url, safe=""),
                         urllib.parse.quote(param_str, safe="")])
    key = "&".join([urllib.parse.quote(creds["api_secret"], safe=""),
                    urllib.parse.quote(creds["access_secret"], safe="")])
    sig = base64.b64encode(hmac.new(key.encode(), base_str.encode(), hashlib.sha256).digest()).decode()
    params["oauth_signature"] = sig
    return "OAuth " + ", ".join(f'{urllib.parse.quote(k, safe="")}="{urllib.parse.quote(v, safe="")}"'
                                for k, v in sorted(params.items()))


def post_to_x(text: str, creds: dict) -> dict:
    body = json.dumps({"text": text}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": oauth1_header("POST", API, creds),
        "Content-Type": "application/json",
        "User-Agent": "SignalBot/1.0",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main() -> int:
    if kill_switch():
        return guarded_exit("announce")
    cfg = config()
    creds = {k: os.environ.get(v, "").strip() for k, v in [
        ("api_key", "X_API_KEY"), ("api_secret", "X_API_SECRET"),
        ("access_token", "X_ACCESS_TOKEN"), ("access_secret", "X_ACCESS_SECRET")]}
    if not all(creds.values()):
        print("[announce] X secrets not set; skipping (pipeline works without X).")
        return 0

    base_url = cfg.get("site_base_url", "").rstrip("/")
    if not base_url:
        print("[announce] site_base_url not set; cannot build links. Skipping.")
        return 0

    announced_path = ROOT / "state" / "announced.json"
    announced = set(json.loads(announced_path.read_text())) if announced_path.exists() else set()

    posted = 0
    for p in sorted((ROOT / "posts").glob("*.md")):
        stem = p.stem
        if stem in announced:
            continue
        text_src = p.read_text()
        title = ""
        for line in text_src.splitlines()[:6]:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
                break
        if not title:
            log_decision("announce_failed", json.dumps({"file": stem, "error": "no title found"}))
            continue
        link = f"{base_url}/posts/{stem}.html"
        # 280-char limit: trim the title to leave room for " — " + link + margin.
        room = 280 - len(link) - 3
        text = f"{title[:room]} — {link}"
        try:
            resp = post_to_x(text, creds)
            post_id = resp.get("data", {}).get("id", "?")
            announced.add(stem)
            announced_path.write_text(json.dumps(sorted(announced), indent=1))
            posted += 1
            log_decision("announced", json.dumps({"file": stem, "post_id": post_id, "text": text[:120]}))
            print(f"[announce] posted: {text[:70]}... (id {post_id})")
        except Exception as e:
            log_decision("announce_failed", json.dumps({"file": stem, "error": f"{type(e).__name__}: {e}"[:150]}))
            print(f"[announce] FAILED for {stem}: {type(e).__name__}: {str(e)[:100]}")

    print(f"[announce] {posted} new post(s) announced to X")
    return 0


if __name__ == "__main__":
    import os
    sys.exit(main())
