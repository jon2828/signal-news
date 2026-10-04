#!/usr/bin/env python3
"""Poll the live site until the markdown fix is deployed, then verify it."""
import re
import sys
import time
import urllib.request

BASE = "https://unspentthoughts.com"
LEAK_PATTERNS = ("<p># ", "<p>## ", "<p>*Date", "<p>**Date", "<p>### ", "](http", ">Date: 2026", ">Topic: ")


def fetch(path="/"):
    url = f"{BASE}{path}?cb=%d" % int(time.time())
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    return urllib.request.urlopen(req, timeout=25).read().decode()


for attempt in range(1, 13):
    try:
        home = fetch("/")
    except Exception as exc:
        print(f"check {attempt}: fetch failed ({type(exc).__name__})")
        time.sleep(30)
        continue
    leaks = [p for p in LEAK_PATTERNS if p in home]
    excerpts = home.count("…</p>")
    if not leaks and excerpts >= 16:
        print(f"check {attempt}: CLEAN — {excerpts} prose excerpts, no raw markdown")
        break
    print(f"check {attempt}: leaks={leaks} excerpts={excerpts}")
    time.sleep(30)
else:
    print("still stale after polling; Cloudflare build may be queued")
    sys.exit(1)

# Deeper check: every article page, plus the disclosure page.
from html.parser import HTMLParser  # noqa: E402


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


parser = Links()
parser.feed(home)
articles = sorted({u for u in parser.links if "/posts/" in u})
bad = []
for url in articles + [f"{BASE}/disclosure"]:
    body = fetch(url.replace(BASE, ""))
    hits = [p for p in LEAK_PATTERNS if p in body]
    if hits:
        bad.append((url.rsplit("/", 1)[-1][:50], hits))
print(f"checked {len(articles)} article pages + disclosure | leaks: {bad if bad else 'none'}")
