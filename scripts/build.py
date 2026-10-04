#!/usr/bin/env python3
"""Job 6: build. posts/*.md -> static site (index.html, feed.xml, disclosure).

Plain stdlib, no framework. Output goes to site/dist/, which Cloudflare
Pages serves. Sort posts by date, newest first.
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, guarded_exit, kill_switch  # noqa: E402

SITE_CSS = """
:root{--bg:#0a0a0a;--panel:#141414;--text:#e8e6e3;--muted:#9a958e;--accent:#f59e0b;--accent-dim:#b97a2a;--line:#26241f}
*{box-sizing:border-box}
body{max-width:680px;margin:0 auto;padding:0 1.2rem 3rem;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.65;color:var(--text);background:var(--bg)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
header.site{padding:2.2rem 0 1.4rem;border-bottom:1px solid var(--line);margin-bottom:1.8rem}
.logo{display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:var(--panel);border:1px solid var(--line);font-family:Georgia,serif;font-size:1.7rem;color:var(--text);margin-bottom:1rem}
.logo span{color:var(--accent);font-size:1.9rem;line-height:0}
h1{font-size:1.55rem;font-weight:700;letter-spacing:-.02em;margin:0 0 .4rem}
h1 a{color:var(--text)}
.tagline{font-size:1.02rem;color:var(--muted);margin:0 0 1rem;max-width:34ch}
nav{display:flex;gap:1.1rem;font-size:.88rem}
nav a{color:var(--muted)}
nav a:hover{color:var(--accent);text-decoration:none}
h2{font-size:1.05rem;margin:0 0 .5rem;font-weight:600}
.post{margin:0 0 1.4rem;padding:1.2rem 1.3rem;background:var(--panel);border:1px solid var(--line);border-radius:14px}
.post h2 a{color:var(--text)}
.post h2 a:hover{color:var(--accent)}
.meta{font-size:.78rem;color:var(--muted);margin-bottom:.65rem;display:flex;gap:.45rem;align-items:center;flex-wrap:wrap}
.badge{border:1px solid var(--line);border-radius:99px;padding:.1rem .55rem;font-size:.72rem}
.badge.score{color:var(--accent);border-color:var(--accent-dim)}
.excerpt{color:var(--muted);font-size:.93rem;margin:0}
.article h2{margin-top:1.8rem}
.article p{margin:0 0 1.1rem}
.article .meta{margin-bottom:1.4rem}
.back{display:inline-block;margin:1.4rem 0;font-size:.88rem;color:var(--muted)}
h1.article-title{font-size:1.6rem;line-height:1.3;margin:.8rem 0 .6rem}
.disclosure h1{margin-bottom:1.2rem}
footer{font-size:.82rem;color:var(--muted);margin-top:2.6rem;padding-top:1.4rem;border-top:1px solid var(--line)}
hr{border:none;border-top:1px solid var(--line);margin:2rem 0}
ul{padding-left:1.2rem}
/* Simple editorial layout: original rhythm, profile palette, sans-serif. */
:root{--bg:#0a0b0d;--panel:#111216;--text:#e8e6e3;--muted:#a5a29d;--accent:#eea02b;--line:#303033}
body{max-width:720px;padding:2rem 1rem;line-height:1.6}
header.site{padding:0 0 1rem;border-bottom:0;margin-bottom:2rem}
h1{font-size:1.9rem;line-height:1.25;margin-bottom:.3rem}
.tagline{max-width:none;font-size:1rem}
nav{flex-wrap:wrap;gap:.3rem 1.1rem}
nav a{display:inline-flex;align-items:center;min-height:44px}
h2{font-size:1.25rem;line-height:1.35;margin:0 0 .7rem}
.post{margin:0 0 2.5rem;padding:0 0 2rem;background:transparent;border:0;border-bottom:1px solid var(--line);border-radius:0}
.post h2 a{color:var(--accent)}
.meta{font-size:.85rem;margin-bottom:.8rem;gap:.5rem}
.badge{border-radius:3px;padding:0 .4rem;font-size:.75rem}
.badge.score{color:var(--muted);border-color:var(--line)}
.article>.post,.disclosure{border-bottom:0;margin-bottom:0;padding-bottom:0}
footer{font-size:.85rem;margin-top:3rem;padding-top:0;border-top:0}
a:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
@media(max-width:480px){body{padding:1.5rem 1rem}h1{font-size:1.65rem}}
"""


def parse_post(path: Path) -> dict | None:
    text = path.read_text()
    if not text.startswith("---"):
        return None
    try:
        fm, body = text[3:].split("---", 1)
    except ValueError:
        return None
    meta = {"path": path, "body": body.strip()}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "sources":
                try:
                    meta[k] = json.loads(v.replace("'", '"'))
                except Exception:
                    meta[k] = []
            elif k == "score":
                try:
                    meta[k] = int(v)
                except ValueError:
                    meta[k] = 0
            else:
                meta[k] = v
    return meta


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def is_retracted(meta: dict) -> bool:
    """A withdrawn post stays online, marked, but leaves the index/feed/sitemap.
    Deleting it would break the link already announced on X and erase the
    record of the correction."""
    return str(meta.get("retracted", "")).strip().lower() in ("true", "1", "yes")


INLINE_MD = (
    (re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"`([^`\n]+)`"), r"<code>\1</code>"),
)


def inline_md(text: str) -> str:
    out = esc(text)
    for pat, rep in INLINE_MD:
        out = pat.sub(rep, out)
    return out


def plain_md(text: str) -> str:
    """Markdown stripped to readable text, for excerpts: '[a](u)' -> 'a'."""
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    return text


def md_blocks(md: str) -> list[tuple[str, str]]:
    """Split a post body into ('p' | 'hN' | 'li', text) blocks, line by line.

    The writer sometimes leaves its own '# Title' heading and a '*Date:*' line
    in the body, plus stray '### x' headings. The page renders the title and
    date itself, so those lines are dropped: no post should ever print a
    literal '#' or '*Date*' on the site.
    """
    blocks: list[tuple[str, str]] = []
    para: list[str] = []
    seen_content = 0

    def flush() -> None:
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    # Metadata the writer sometimes leaves at the top of a body: a bare
    # '*Date: ...*' line, or a 'Topic: AI / Score: 9' header block. Only the
    # opening lines are stripped, so a legitimate mid-article sentence that
    # happens to start with 'Score:' is never touched.
    meta_line = re.compile(
        r"^\*{0,2}(?:Date|Topic|Score|Sources?|Author|Published)\s*:\s*.{0,60}\*{0,2}$", re.I)

    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        if re.match(r"^#\s+", line):
            flush()
            continue
        if seen_content < 4 and meta_line.match(line):
            flush()
            continue
        if re.match(r"^\*{0,2}Date:\s*\d{4}\D\d{1,2}\D\d{1,2}\*{0,2}$", line, re.I):
            flush()
            continue
        h = re.match(r"^(#{2,6})\s+(.+)$", line)
        if h:
            flush()
            seen_content += 1
            blocks.append((f"h{min(6, len(h.group(1)))}", h.group(2).strip()))
            continue
        if re.match(r"^[-*]\s+", line):
            flush()
            seen_content += 1
            blocks.append(("li", re.sub(r"^[-*]\s+", "", line)))
            continue
        seen_content += 1
        para.append(line)
    flush()
    return blocks


def blocks_html(blocks: list[tuple[str, str]]) -> str:
    out: list[str] = []
    in_list = False
    for kind, text in blocks:
        if kind == "li":
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(text)}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if kind.startswith("h"):
            lvl = kind[1]
            out.append(f"<h{lvl}>{inline_md(text)}</h{lvl}>")
        else:
            out.append(f"<p>{inline_md(text)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def excerpt_of(meta: dict) -> str:
    """Plain-text summary of a post: first paragraph of real prose, markdown
    stripped. Used by the index cards AND the RSS descriptions, so neither can
    leak '[text](url)' syntax into a reader."""
    paras = [t for kind, t in md_blocks(meta["body"]) if kind == "p"]
    first = next((t for t in paras if len(t) >= 70), paras[0] if paras else "")
    return plain_md(first)[:280]


def render_post(meta: dict, base_url: str, full: bool, heading: bool = True) -> str:
    url = f"{base_url}/posts/{esc(meta['path'].stem)}.html"
    blocks = md_blocks(meta["body"])
    excerpt = esc(excerpt_of(meta))
    title_html = (f'<h2><a href="{url}">{esc(meta.get("title", "untitled"))}</a></h2>'
                  if heading else "")
    out = ['<div class="post">',
           title_html,
           f'<div class="meta"><span class="badge score">score {meta.get("score", "?")}/10</span>'
           f'<span class="badge">{esc(meta.get("topic", "?"))}</span>{esc(meta.get("date", ""))}</div>']
    if full:
        out.append(blocks_html(blocks))
        srcs = meta.get("sources") or []
        if srcs:
            out.append("<h2>Sources</h2><ul>" + "".join(
                f'<li><a href="{esc(s)}">{esc(s)}</a></li>' for s in srcs) + "</ul>")
    elif excerpt:
        out.append(f"<p>{excerpt}…</p>")
    out.append("</div>")
    return "\n".join(out)


def main() -> int:
    if kill_switch():
        return guarded_exit("build")
    cfg = json.loads((ROOT / "config" / "pipeline.json").read_text())
    base_url = cfg.get("site_base_url", "").rstrip("/") or ""
    posts = [m for p in (ROOT / "posts").glob("*.md") if (m := parse_post(p))]
    posts.sort(key=lambda m: (m.get("date", ""), m.get("score", 0)), reverse=True)
    # Withdrawn posts keep their page (the X link stays alive) but drop out of
    # the index, feed, and sitemap so they are not presented as news.
    live = [m for m in posts if not is_retracted(m)]

    dist = ROOT / "site" / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    # Wipe first: dist is fully generated, and stale files from earlier builds
    # (renamed or retracted posts) would otherwise keep shipping to production.
    for old in dist.rglob("*"):
        if old.is_file():
            old.unlink()

    # Optional privacy-first analytics: Cloudflare Web Analytics beacon.
    analytics = ""
    token = cfg.get("analytics_token", "")
    if token:
        analytics = (f"<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
                     f"data-cf-beacon='{json.dumps({'token': token})}'></script>")

    items = "\n\n".join(render_post(m, base_url, full=False) for m in live)
    index = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>Unspent Thoughts — AI and Bitcoin news that earned its place</title>'
             f'<style>{SITE_CSS}</style>{analytics}</head><body>'
             f'<header class="site">'
             f'<div class="logo">U<span>.</span></div>'
             f'<h1><a href="/">Unspent Thoughts</a></h1>'
             f'<p class="tagline">Bitcoin is scarce. Intelligence is becoming abundant. Time remains finite.</p>'
             f'<nav><a href="/">Posts</a><a href="/disclosure">How it works</a><a href="/feed.xml">RSS</a>'
             f'<a href="https://x.com/UnspentThoughts">𝕏</a></nav>'
             f'</header>'
             f'{items}'
             f'<footer>Selected, written, and checked by software. '
             f'<a href="https://github.com/jon2828/signal-news">Every decision logged</a>.</footer>'
             f'</body></html>')
    (dist / "index.html").write_text(index)

    # Per-post pages: the index links here, so they must exist.
    posts_dir_dist = dist / "posts"
    posts_dir_dist.mkdir(exist_ok=True)
    for m in posts:
        title = esc(m.get("title"))
        page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{title} — Unspent Thoughts</title>'
                f'<style>{SITE_CSS}</style>{analytics}</head><body>'
                f'<header class="site">'
                f'<div class="logo">U<span>.</span></div>'
                f'<h1><a href="/">Unspent Thoughts</a></h1>'
                f'<nav><a href="/">← All posts</a><a href="/disclosure">How it works</a></nav>'
                f'</header>'
                f'<article class="post article">'
                + ('<p style="display:inline-block;border:1px solid var(--accent);color:var(--accent);'
                   'border-radius:3px;padding:0 .5rem;font-size:.75rem;margin:0 0 .8rem">RETRACTED</p>'
                   '<p><em>This post was withdrawn. Its source material was a year old when it was '
                   'published, so it was not news. It stays online, marked, rather than deleted, because '
                   'the mistake and the correction are part of the record.</em></p>'
                   if is_retracted(m) else '')
                + f'<h1 class="article-title">{title}</h1>'
                + render_post(m, base_url, full=True, heading=False)
                + '</article>'
                + '</body></html>')
        (posts_dir_dist / f"{m['path'].stem}.html").write_text(page)

    notfound = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>Not found — Unspent Thoughts</title><style>{SITE_CSS}</style></head>'
                f'<body><header class="site"><div class="logo">U<span>.</span></div>'
                f'<h1>Not found</h1></header>'
                f'<p>The page you asked for does not exist. '
                f'<a href="/">Back to Unspent Thoughts</a>.</p></body></html>')
    (dist / "404.html").write_text(notfound)

    # Crawler files: robots.txt + sitemap.xml (regenerated every build, so
    # new posts are always discoverable).
    (dist / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n")
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    urls = [f"{base_url}/", f"{base_url}/disclosure"] + [
        f"{base_url}/posts/{esc(m['path'].stem)}.html" for m in live]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(
                   f"  <url><loc>{esc(u)}</loc><changefreq>daily</changefreq></url>"
                   for u in urls)
               + "\n</urlset>\n")
    (dist / "sitemap.xml").write_text(sitemap)

    disclosure_md = (ROOT / "site" / "pages" / "disclosure.md").read_text()
    disclosure_html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                       f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                       f'<title>How this site works — Unspent Thoughts</title>'
                       f'<style>{SITE_CSS}</style>{analytics}</head><body>'
                       f'<header class="site">'
                       f'<div class="logo">U<span>.</span></div>'
                       f'<h1><a href="/">Unspent Thoughts</a></h1>'
                       f'<nav><a href="/">← All posts</a></nav>'
                       f'</header>'
                       f'<div class="post disclosure">'
                       f'<h1 class="article-title">How this site works</h1>'
                       + blocks_html(md_blocks(disclosure_md))
                       + '</div></body></html>')
    (dist / "disclosure.html").write_text(disclosure_html)

    now = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    rss_items = []
    for m in live[:30]:
        link = f"{base_url}/posts/{esc(m['path'].stem)}.html" if base_url else f"/posts/{esc(m['path'].stem)}.html"
        rss_items.append(
            f"<item><title>{esc(m.get('title'))}</title>"
            f"<link>{link}</link>"
            f"<guid>{link}</guid>"
            f"<pubDate>{esc(m.get('date'))} 00:00:00 GMT</pubDate>"
            f"<description>{esc(excerpt_of(m))}</description></item>")
    feed = (f'<?xml version="1.0"?><rss version="2.0"><channel>'
            f'<title>Unspent Thoughts</title><link>{base_url or "/"}</link>'
            f'<description>The AI and Bitcoin news that earned its place</description>'
            f'<lastBuildDate>{now}</lastBuildDate>{"".join(rss_items)}</channel></rss>')
    (dist / "feed.xml").write_text(feed)

    print(f"[build] {len(live)} live posts ({len(posts) - len(live)} retracted) "
          f"-> site/dist/ (index.html, disclosure.html, feed.xml)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
