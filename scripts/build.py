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
:root{--accent:#333;--line:#ececec}
*{box-sizing:border-box}
body{margin:0 auto;max-width:920px;padding:68px 40px 48px;background:#fff;color:#262626;font-family:Arial,Helvetica,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}a:hover{color:#111;text-decoration:underline;text-underline-offset:5px}a:focus-visible{outline:2px solid #555;outline-offset:5px}
header.site{margin-bottom:60px}header h1{font-size:25px;font-weight:400;letter-spacing:-.5px;margin:0 0 10px}.tagline{font-size:15px;color:#777;max-width:530px;margin:0 0 22px}nav{display:flex;gap:25px;flex-wrap:wrap;font-size:13px;color:#777}nav a{padding:8px 0}
.post{padding:0 0 48px;margin:0 0 48px;border-bottom:1px solid var(--line)}.meta{font-size:13px;color:#777;margin-bottom:16px}.post h2{font-size:26px;line-height:1.35;font-weight:400;letter-spacing:-.4px;margin:0 0 14px}.post>p{font-size:18px;color:#777;line-height:1.65;margin:0;max-width:760px}
footer{font-size:12px;color:#888;padding-top:10px}.article{border:0}.article .post{border:0;margin:0;padding:0}.article-title{font-size:36px;font-weight:400;line-height:1.3;letter-spacing:-.7px;margin:0 0 22px}.article .post>p{color:#444;font-size:18px;margin:0 0 24px}.article h2,.article h3{font-weight:400;margin:32px 0 16px}.article li{margin:10px 0;color:#555}.article a{text-decoration:underline;text-underline-offset:3px;overflow-wrap:anywhere}.disclosure p{margin:20px 0}.disclosure h1{font-size:30px;font-weight:400}
@media(max-width:600px){body{padding:34px 24px}header.site{margin-bottom:46px}header h1{font-size:23px}.post{padding-bottom:34px;margin-bottom:34px}.post h2{font-size:23px}.post>p{font-size:16px}.article-title{font-size:29px}.article .post>p{font-size:17px}nav{gap:22px}}
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
           f'<div class="meta">{esc(meta.get("topic", "?"))} · {esc(meta.get("date", ""))}</div>',
           title_html]
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
             f'<h1><a href="/">Unspent Thoughts</a></h1>'
             f'<p class="tagline">Bitcoin is scarce. Intelligence is becoming abundant. Time remains finite.</p>'
             f'<nav><a href="/">Posts</a><a href="/disclosure">How it works</a><a href="/feed.xml">RSS</a>'
             f'<a href="https://x.com/UnspentThoughts">X</a></nav>'
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
                f'<body><header class="site">'
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
