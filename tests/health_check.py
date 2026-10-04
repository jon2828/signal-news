#!/usr/bin/env python3
"""Read-only health check for Unspent Thoughts: repo, pipeline, live site."""
import collections
import concurrent.futures
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("/home/jarvis/ai-bitcoin-news")
BASE = "https://unspentthoughts.com"

print("=== REPO STATE ===")
print("posts:", len(list((ROOT / "posts").glob("*.md"))))
drafts = sorted((ROOT / "state" / "drafts").glob("*.md")) if (ROOT / "state" / "drafts").exists() else []
print("drafts pending:", len(drafts))
for d in drafts:
    print("   -", d.name[:70])

print("=== LATEST DECISIONS (last 12) ===")
rows = [json.loads(l) for l in (ROOT / "state" / "decisions.jsonl").read_text().splitlines() if l.strip()]
for r in rows[-12:]:
    print(f"  {r['ts']} {r['action']}: {r['detail'][:90]}")
print("today's action counts:", dict(collections.Counter(r["action"] for r in rows if r["ts"].startswith("2026-10-04"))))

print("=== LIVE SITE ===")


def get(path):
    url = f"{BASE}{path}?cb=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=25)
        return path, r.status, r.read().decode()
    except Exception as e:
        return path, str(e), ""


_, code, home = get("/")
p = HTMLParser()


class L(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


lp = L()
lp.feed(home)
arts = sorted({u for u in lp.links if "/posts/" in u})
print(f"homepage HTTP {code} | posts listed {len(arts)} | retracted in index {'2025-10-13' in home}")
paths = [a.replace(BASE, "") for a in arts] + [
    "/disclosure", "/feed.xml", "/sitemap.xml", "/robots.txt",
    "/posts/2025-10-13-openais-third-chip-deal-in-three-weeks-brings-the-total-to-2-96f43ed0.html",
]
with concurrent.futures.ThreadPoolExecutor(6) as ex:
    results = list(ex.map(get, paths))
bad = [(pth, c) for pth, c, _ in results if c != 200]
print("broken links:", bad if bad else "none", f"| checked {len(paths)}")
ret = next(b for pth, c, b in results if "2025-10-13" in pth)
print("retraction banner live:", "RETRACTED" in ret)
leaks = []
for pth, c, b in results:
    for pat in ("<p># ", "<p>## ", "<p>*Date", "](http", ">Date: 2026", ">Topic: "):
        if pat in b:
            leaks.append((pth, pat))
print("raw markdown leaks:", leaks if leaks else "none")
sm = next(b for pth, c, b in results if pth == "/sitemap.xml")
fd = next(b for pth, c, b in results if pth == "/feed.xml")
print(f"sitemap urls {sm.count('<loc>')} | feed items {fd.count('<item>')} | retracted excluded: {'2025-10-13' not in sm and '2025-10-13' not in fd}")
titles = re.findall(r"<h2><a href=\"[^\"]+\">([^<]+)</a></h2>", home)[:3]
print("newest:", [re.sub(r"\s+", " ", t) for t in titles])
