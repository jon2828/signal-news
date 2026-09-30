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
body{max-width:720px;margin:0 auto;padding:2rem 1rem;font-family:Georgia,serif;line-height:1.6;color:#1a1a1a;background:#fafaf8}
a{color:#0a6e4f}
h1{font-size:1.9rem;line-height:1.25;margin-bottom:.3rem}
h2{font-size:1.25rem;margin-top:1.6rem}
.post{margin-bottom:2.5rem;padding-bottom:2rem;border-bottom:1px solid #ddd}
.meta{font-size:.85rem;color:#666;margin-bottom:.8rem}
.badge{display:inline-block;border:1px solid #ccc;border-radius:3px;padding:0 .4rem;margin-right:.5rem;font-size:.75rem}
footer{font-size:.85rem;color:#666;margin-top:3rem}
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


def render_post(meta: dict, base_url: str, full: bool) -> str:
    url = f"{base_url}/posts/{esc(meta['path'].stem)}.html"
    paras = [p.strip() for p in re.split(r"\n\s*\n", meta["body"]) if p.strip()]
    excerpt = esc(paras[0][:280]) if paras else ""
    out = [f'<div class="post">',
           f'<h2><a href="{url}">{esc(meta.get("title", "untitled"))}</a></h2>',
           f'<div class="meta"><span class="badge">score {meta.get("score", "?")}/10</span>'
           f'<span class="badge">{esc(meta.get("topic", "?"))}</span>{esc(meta.get("date", ""))}</div>']
    if full:
        out.append(meta["body"].replace("\n\n", "</p>\n<p>").join(["<p>", "</p>"]))
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

    dist = ROOT / "site" / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    # Optional privacy-first analytics: Cloudflare Web Analytics beacon.
    analytics = ""
    token = cfg.get("analytics_token", "")
    if token:
        analytics = (f"<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
                     f"data-cf-beacon='{json.dumps({'token': token})}'></script>")

    items = "\n\n".join(render_post(m, base_url, full=False) for m in posts)
    index = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>Unspent Thoughts — AI and Bitcoin news that earned its place</title>'
             f'<style>{SITE_CSS}</style>{analytics}</head><body>'
             f'<h1>Unspent Thoughts</h1><p>The AI and Bitcoin news that earned its place. '
             f'Selected, written, and checked by software. <a href="/disclosure">How it works</a>.</p>'
             f'{items}<footer><a href="/feed.xml">RSS</a> · '
             f'<a href="https://github.com/jon2828/signal-news">Open source: every decision logged</a></footer>'
             f'</body></html>')
    (dist / "index.html").write_text(index)

    # Per-post pages: the index links here, so they must exist.
    posts_dir_dist = dist / "posts"
    posts_dir_dist.mkdir(exist_ok=True)
    for m in posts:
        page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{esc(m.get("title"))} — Unspent Thoughts</title>'
                f'<style>{SITE_CSS}</style>{analytics}</head><body>'
                f'<p><a href="/">← Unspent Thoughts</a></p>'
                + render_post(m, base_url, full=True)
                + '</body></html>')
        (posts_dir_dist / f"{m['path'].stem}.html").write_text(page)

    notfound = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>Not found — Unspent Thoughts</title><style>{SITE_CSS}</style></head>'
                f'<body><h1>Not found</h1><p>The page you asked for does not exist. '
                f'<a href="/">Back to Unspent Thoughts</a>.</p></body></html>')
    (dist / "404.html").write_text(notfound)

    # Crawler files: robots.txt + sitemap.xml (regenerated every build, so
    # new posts are always discoverable).
    (dist / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n")
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    urls = [f"{base_url}/", f"{base_url}/disclosure"] + [
        f"{base_url}/posts/{esc(m['path'].stem)}.html" for m in posts]
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
                       f'<h1>How this site works</h1>'
                       + disclosure_md.replace("\n\n", "</p>\n<p>").join(["<p>", "</p>"])
                       + '<p><a href="/">← back</a></p></body></html>')
    (dist / "disclosure.html").write_text(disclosure_html)

    now = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    rss_items = []
    for m in posts[:30]:
        link = f"{base_url}/posts/{esc(m['path'].stem)}.html" if base_url else f"/posts/{esc(m['path'].stem)}.html"
        desc = [p.strip() for p in re.split(r"\n\s*\n", m["body"]) if p.strip()]
        rss_items.append(
            f"<item><title>{esc(m.get('title'))}</title>"
            f"<link>{link}</link>"
            f"<guid>{link}</guid>"
            f"<pubDate>{esc(m.get('date'))} 00:00:00 GMT</pubDate>"
            f"<description>{esc(desc[0][:300] if desc else '')}</description></item>")
    feed = (f'<?xml version="1.0"?><rss version="2.0"><channel>'
            f'<title>Unspent Thoughts</title><link>{base_url or "/"}</link>'
            f'<description>The AI and Bitcoin news that earned its place</description>'
            f'<lastBuildDate>{now}</lastBuildDate>{"".join(rss_items)}</channel></rss>')
    (dist / "feed.xml").write_text(feed)

    print(f"[build] {len(posts)} posts -> site/dist/ (index.html, disclosure.html, feed.xml)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
