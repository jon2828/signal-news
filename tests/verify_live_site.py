#!/usr/bin/env python3
"""Wait for the feed fix to deploy, then verify the live site end to end."""
import concurrent.futures
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

BASE = "https://unspentthoughts.com"
PATTERNS = ("<p># ", "<p>## ", "<p>*Date", "](http", ">Date: 2026", ">Topic: ")


def get(path="/"):
    req = urllib.request.Request(f"{BASE}{path}?cb={int(time.time())}",
                                headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    r = urllib.request.urlopen(req, timeout=25)
    return r.status, r.read().decode()


for attempt in range(1, 13):
    try:
        _, feed = get("/feed.xml")
    except Exception as exc:
        print(f"check {attempt}: fetch failed ({type(exc).__name__})", flush=True)
        time.sleep(30)
        continue
    if "](http" not in feed and "<description>" in feed:
        print(f"check {attempt}: feed clean ({feed.count('<item>')} items, no markdown links)")
        break
    print(f"check {attempt}: feed still has markdown", flush=True)
    time.sleep(30)
else:
    sys.exit("feed fix did not deploy in time")


class L(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


_, home = get("/")
lp = L()
lp.feed(home)
arts = sorted({u for u in lp.links if "/posts/" in u})
paths = [a.replace(BASE, "") for a in arts] + [
    "/disclosure", "/feed.xml", "/sitemap.xml", "/robots.txt",
    "/posts/2025-10-13-openais-third-chip-deal-in-three-weeks-brings-the-total-to-2-96f43ed0.html",
]
with concurrent.futures.ThreadPoolExecutor(6) as ex:
    results = list(ex.map(lambda p: (p, *get(p)), paths))
bad = [(p, c) for p, c, _ in results if c != 200]
leaks = [(p, pat) for p, _, b in results for pat in PATTERNS if pat in b]
ret = next(b for p, _, b in results if "2025-10-13" in p)
sm = next(b for p, _, b in results if p == "/sitemap.xml")
fd = next(b for p, _, b in results if p == "/feed.xml")
print(f"pages checked: {len(paths)} | broken: {bad if bad else 'none'}")
print(f"markdown leaks: {leaks if leaks else 'none'}")
print(f"retraction banner: {'RETRACTED' in ret} | retracted excluded from listings: "
      f"{'2025-10-13' not in sm and '2025-10-13' not in fd}")
print(f"homepage: {len(arts)} posts | sitemap {sm.count('<loc>')} | feed {fd.count('<item>')}")
print("sample feed description:", re.search(r"<description>([^<]{40,120})", fd).group(1)[:110])
