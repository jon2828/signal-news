#!/usr/bin/env python3
"""Verify nothing renders raw markdown on the built site.

Checks every generated page for literal '#' headings, '*Date*' lines,
unconverted markdown links, and stray list bullets, printing the offending
snippet so a failure is actionable.
"""
import re
import sys
from pathlib import Path

dist = Path("site/dist")
pages = sorted(list(dist.glob("*.html")) + list((dist / "posts").glob("*.html")))
pages += [dist / "feed.xml"] if (dist / "feed.xml").is_file() else []
assert pages, "no built pages found - run scripts/build.py first"

LEAKS = (
    (re.compile(r"<p>\s*#{1,6}\s"), "raw heading in a paragraph"),
    (re.compile(r"<p>\s*\*{0,2}Date:\s*\d{4}"), "raw *Date* line"),
    (re.compile(r"\[[^\]]+\]\s*\(https?://"), "unconverted markdown link"),
    (re.compile(r"<p>\s*[-*]\s+"), "raw bullet in a paragraph"),
    (re.compile(r"<li>\s*[-*]\s+"), "double bullet"),
)

bad = []
for page in pages:
    body = page.read_text()
    for pattern, why in LEAKS:
        m = pattern.search(body)
        if m:
            snippet = re.sub(r"\s+", " ", body[max(0, m.start() - 60):m.end() + 80])
            bad.append(f"{page.relative_to(dist)}: {why} -> ...{snippet}...")

print(f"checked {len(pages)} pages")
if bad:
    print("LEAKS:")
    for b in bad:
        print("  " + b)
    sys.exit(1)
print("no raw markdown on any page")
