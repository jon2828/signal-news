#!/usr/bin/env python3
"""Anti-AI tell checker for Signal posts.

Usage: python3 lint.py <post.md> [--max-hits N]
Prints every hit with a count and pattern name. Exits 1 when total hits
exceed --max-hits (default from config/pipeline.json, fallback 2), which
fails the pipeline step and drops the post from publishing.

The pattern list mirrors voice/bible.md. Keep them in sync.
"""
import json
import re
import sys
from pathlib import Path

# (name, compiled regex). Word-boundary aware. Case-sensitive where the
# lowercase form is the tell (headings are checked separately).
PATTERNS = [
    ("delve", re.compile(r"\bdelve[sd]?\b|\bdelving\b", re.I)),
    ("landscape-abstract", re.compile(r"\b(?:the\s+\w+\s+)?landscape\b", re.I)),
    ("tapestry", re.compile(r"\btapestry\b", re.I)),
    ("testament", re.compile(r"\btestament\b|\ba testament to\b", re.I)),
    ("pivotal", re.compile(r"\bpivotal\b", re.I)),
    ("crucial", re.compile(r"\bcrucial\b", re.I)),
    ("underscore", re.compile(r"\bunderscor(?:e|es|ing)\b", re.I)),
    ("highlight-verb", re.compile(r"\bhighlights?\b|\bhighlighting\b", re.I)),
    ("showcase", re.compile(r"\bshowcas(?:e|es|ing|ed)\b", re.I)),
    ("boasts", re.compile(r"\bboasts?\b|\bboasting\b", re.I)),
    ("vibrant", re.compile(r"\bvibrant\b", re.I)),
    ("garner", re.compile(r"\bgarner(?:s|ed|ing)?\b", re.I)),
    ("fostering", re.compile(r"\bfoster(?:s|ed|ing)?\b", re.I)),
    ("leveraging", re.compile(r"\bleverag(?:e|es|ed|ing)\b", re.I)),
    ("seamless", re.compile(r"\bseamless(?:ly)?\b", re.I)),
    ("game-changer", re.compile(r"\bgame-?changer\b", re.I)),
    ("cutting-edge", re.compile(r"\bcutting-?edge\b", re.I)),
    ("not-just-parallelism", re.compile(r"\bit'?s not just\b|\bnot only\b", re.I)),
    ("weasel-attribution", re.compile(r"\bindustry reports?\b|\bexperts (?:argue|say|say)\b|\bobservers (?:note|have noted|cited)\b|\bsome critics\b", re.I)),
    ("em-dash", re.compile(r"\u2014|\u2013(?!\d)")),
    ("curly-quotes", re.compile(r"[\u201c\u201d\u2018\u2019]")),
    ("emoji", re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", re.I)),
    ("generic-conclusion", re.compile(r"\bin conclusion\b|\bthe future looks bright\b|\bexciting times\b|\bmoving forward\b", re.I)),
    ("signoff", re.compile(r"\blet me know\b|\bi hope this helps\b|\bhere'?s what you need to know\b|\bwithout further ado\b", re.I)),
    ("rhetorical-question", re.compile(r"\bwhat if\b.*\?|\bever wondered\b|\bthe question is\b|\bthink about it\b", re.I)),
    ("so-opener", re.compile(r"^\s*(?:So|Look),", re.I | re.M)),
    ("adverb-opener", re.compile(r"^\s*(?:Interestingly|Importantly|Notably|Crucially|Essentially|Ultimately|Additionally|Furthermore),", re.I | re.M)),
    ("knowledge-cutoff", re.compile(r"\bas of (?:my|our) last\b|\bup to my last training\b|\bbased on available information\b", re.I)),
    ("stands-as", re.compile(r"\bstands as\b|\bserves as\b", re.I)),
    ("rule-of-three", re.compile(r"\b\w[\w-]*,\s+\w[\w-]*,?\s+and\s+\w[\w-]*\b")),
]

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
CODE_RE = re.compile(r"```.*?```", re.S)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def load_max_hits() -> int:
    cfg = Path(__file__).resolve().parent.parent / "config" / "pipeline.json"
    try:
        return int(json.loads(cfg.read_text())["lint"]["max_hits_per_post"])
    except Exception:
        return 2


def lint(text: str) -> list[tuple[str, int, list[str]]]:
    # Strip frontmatter (dates/sources are fine), code blocks, and link URLs
    # so we only judge the prose. Link text stays.
    body = FRONTMATTER_RE.sub("", text)
    body = CODE_RE.sub("", body)
    body = LINK_RE.sub(r"\1", body)
    hits = []
    for name, rx in PATTERNS:
        matches = rx.findall(body)
        if matches:
            hits.append((name, len(matches), [str(m)[:40] for m in matches[:3]]))
    return hits


def main() -> int:
    args = sys.argv[1:]
    max_hits = load_max_hits()
    if "--max-hits" in args:
        i = args.index("--max-hits")
        max_hits = int(args[i + 1])
        del args[i : i + 2]
    if not args:
        print("usage: lint.py <post.md> [--max-hits N]")
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"lint: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    words = len(re.findall(r"\S+", FRONTMATTER_RE.sub("", text)))
    hits = lint(text)
    total = sum(h[1] for h in hits)
    status = "FAIL" if total > max_hits else "PASS"
    print(f"lint: {status}  words={words}  hits={total} (max {max_hits})")
    for name, count, examples in hits:
        print(f"  - {name}: {count}  e.g. {'; '.join(examples)}")
    if words > 1000:
        print(f"  - WORD COUNT OVER LIMIT: {words} > 1000")
        return 1
    return 1 if total > max_hits else 0


if __name__ == "__main__":
    sys.exit(main())
