#!/usr/bin/env python3
"""Job 6: build. posts/*.md -> static site (index.html, feed.xml, disclosure).

Plain stdlib, no framework. Output goes to site/dist/, which Cloudflare
Pages serves. Sort posts by date, newest first.
"""
import datetime
import html
import json
import re
import shutil
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
footer{font-size:12px;color:#888;padding-top:10px}.article{border:0}.article .post{border:0;margin:0;padding:0}.article-title{font-size:36px;font-weight:400;line-height:1.3;letter-spacing:-.7px;margin:0 0 22px}.article .post>p{color:#444;font-size:18px;margin:0 0 24px}.article h2,.article h3{font-weight:400;margin:32px 0 16px}.article li{margin:10px 0;color:#555}.article a{text-decoration:underline;text-underline-offset:3px;overflow-wrap:anywhere}.article blockquote{margin:24px 0;padding:0 0 0 18px;border-left:2px solid #ddd;color:#555}.article blockquote p{margin:0;color:#555}.disclosure p{margin:20px 0}.disclosure h1{font-size:30px;font-weight:400}
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
    (re.compile(r"\[\[([^\]]+)\]\]"), r"[\1]"),  # writer's '[[source]]' -> '[source]'
    (re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)"), r'<a href="\2">\1</a>'),
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
    text = re.sub(r"\[\[([^\]]+)\]\]", r"[\1]", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    return text


def md_blocks(md: str) -> list[tuple[str, str]]:
    """Split a post body into ('p' | 'hN' | 'li', text) blocks, line by line.

    The writer sometimes leaves its own '# Title' heading and a '*Date:*' line
    in the body, plus stray '### x' headings. The page renders the title and
    date itself, so those lines are dropped: no post should ever print a
    literal '#' or '*Date*' on the site. '> quote' lines become blockquotes.
    """
    blocks: list[tuple[str, str]] = []
    para: list[str] = []
    quote: list[str] = []
    seen_content = 0

    def flush() -> None:
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()
        if quote:
            blocks.append(("quote", " ".join(quote)))
            quote.clear()

    # Metadata the writer sometimes leaves at the top of a body: a bare
    # '*Date: ...*' line, or a 'Topic: AI / Score: 9' header block. Only the
    # opening lines are stripped, so a legitimate mid-article sentence that
    # happens to start with 'Score:' is never touched.
    meta_line = re.compile(
        r"^\*{0,2}(?:Date|Topic|Score|Sources?|Author|Published|Candidate_?id)\s*:?\*{0,2}\s*.{0,400}$", re.I)
    hr = re.compile(r"^-{3,}$")

    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        if re.match(r"^#\s+", line):
            flush()
            continue
        if hr.match(line):
            # The writer's own horizontal-rule separators (often doubled up
            # around its duplicated metadata block). The page provides its
            # own separators, and a bare '---' previously leaked as text.
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
        q = re.match(r"^>\s?(.*)$", line)
        if q:
            flush()
            seen_content += 1
            quote.append(q.group(1).strip())
            continue
        seen_content += 1
        para.append(line)
    flush()
    return blocks


def blocks_html(blocks: list[tuple[str, str]]) -> str:
    out: list[str] = []
    in_list = False
    for kind, text in blocks:
        if kind == "quote":
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<blockquote><p>{inline_md(text)}</p></blockquote>")
            continue
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


SITE_DESCRIPTION = ("AI and Bitcoin news that earned its place. Selected, written, and "
                    "fact-checked by software, with every decision logged.")
DISCLOSURE_DESCRIPTION = ("How Unspent Thoughts works: where the stories come from, how they "
                          "are selected and fact-checked, and what happens when one is wrong.")
MAX_DESCRIPTION = 158

# One site-wide social card, served from site/assets (a source directory) into
# the dist root by copy_assets(). Kept deliberately single: a per-post image
# would mean rendering a bitmap on every pipeline run.
OG_IMAGE_PATH = "/og-card.png"
OG_IMAGE_SIZE = (1200, 630)
OG_IMAGE_ALT = "Unspent Thoughts — AI and Bitcoin news that earned its place"
ASSET_SUFFIXES = (".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp")


def meta_description(text: str, limit: int = MAX_DESCRIPTION) -> str:
    """Trim a summary to search/social length on a word boundary.

    Search engines truncate around 160 characters, so the cut is made here and
    marked with an ellipsis; letting the consumer clip it would cut mid-word."""
    clean = " ".join(plain_md(text).split())
    if len(clean) <= limit:
        return clean
    cut = clean[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.—-")
    return (cut or clean[: limit - 1]).rstrip() + "…"


def head_meta(*, base_url: str, title: str, description: str, path: str = "",
              og_type: str = "website") -> str:
    """Description, canonical and Open Graph/Twitter tags for one page.

    ``path`` is site-relative ("" for the homepage) and must be the page's final
    URL so duplicate URLs collapse onto a single canonical. ``og_type`` is
    "article" for posts and "website" for standing pages.

    There is deliberately no per-page ``og:image``: one site-wide card is used
    for every page, because a per-post image would mean rendering a bitmap on
    every pipeline run. The card itself is copied into dist by ``copy_assets``.
    """
    canonical = f"{base_url}{path}" if base_url else (path or "/")
    image = f"{base_url}{OG_IMAGE_PATH}" if base_url else OG_IMAGE_PATH
    width, height = OG_IMAGE_SIZE
    twitter_card = "summary_large_image"
    return (
        f'<meta name="description" content="{esc(description)}">'
        f'<link rel="canonical" href="{esc(canonical)}">'
        f'<meta property="og:type" content="{og_type}">'
        f'<meta property="og:site_name" content="Unspent Thoughts">'
        f'<meta property="og:title" content="{esc(title)}">'
        f'<meta property="og:description" content="{esc(description)}">'
        f'<meta property="og:url" content="{esc(canonical)}">'
        f'<meta property="og:image" content="{esc(image)}">'
        f'<meta property="og:image:type" content="image/png">'
        f'<meta property="og:image:width" content="{width}">'
        f'<meta property="og:image:height" content="{height}">'
        f'<meta property="og:image:alt" content="{esc(OG_IMAGE_ALT)}">'
        f'<meta name="twitter:card" content="{twitter_card}">'
        f'<meta name="twitter:title" content="{esc(title)}">'
        f'<meta name="twitter:description" content="{esc(description)}">'
        f'<meta name="twitter:image" content="{esc(image)}">'
        f'<meta name="twitter:image:alt" content="{esc(OG_IMAGE_ALT)}">')


def render_post(meta: dict, base_url: str, full: bool, heading: bool = True) -> str:
    # The clean form: Cloudflare serves /posts/<stem> with 200 and 307s the
    # .html form, so linking .html would cost every in-site click a redirect.
    url = f"{base_url}/posts/{esc(meta['path'].stem)}"
    blocks = md_blocks(meta["body"])
    excerpt = esc(excerpt_of(meta))
    title_html = (f'<h2><a href="{url}">{esc(meta.get("title", "untitled"))}</a></h2>'
                  if heading else "")
    out = ['<div class="post">',
           f'<div class="meta">{esc(str(meta.get("topic", "?")).upper())} · score {esc(meta.get("score", "?"))}/10 · {esc(meta.get("date", ""))}</div>',
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


def copy_assets(dist: Path) -> int:
    """Copy static image assets from site/assets into the dist root.

    dist is wiped at the start of every build, so anything not generated here
    (the social card, and any favicon added later) has to be copied in. Only
    image suffixes are copied: site/assets also holds the card's source HTML,
    which must not be published."""
    src = ROOT / "site" / "assets"
    if not src.is_dir():
        return 0
    copied = 0
    for item in sorted(src.iterdir()):
        if item.is_file() and item.suffix.lower() in ASSET_SUFFIXES:
            shutil.copyfile(item, dist / item.name)
            copied += 1
    return copied


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

    # Source images (the social card) are not generated above, and the wipe has
    # just removed the previous build's copies, so re-copy them.
    copy_assets(dist)

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
             f'{head_meta(base_url=base_url, title="Unspent Thoughts — AI and Bitcoin news that earned its place", description=SITE_DESCRIPTION)}'
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
        raw_title = str(m.get("title", "untitled"))
        title = esc(raw_title)
        # Canonical must name the URL that actually serves 200. Cloudflare's
        # html_handling (auto-trailing-slash) serves /posts/<stem> and 307s the
        # .html form, so pointing canonical at .html would contradict the live
        # URL - the exact duplicate-content mismatch this tag exists to fix.
        post_path = f"/posts/{m['path'].stem}"
        page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{title} — Unspent Thoughts</title>'
                f'{head_meta(base_url=base_url, title=raw_title, description=meta_description(excerpt_of(m)), path=post_path, og_type="article")}'
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
                f'<title>Not found — Unspent Thoughts</title>'
                f'<meta name="robots" content="noindex">'
                f'<style>{SITE_CSS}</style></head>'
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
        f"{base_url}/posts/{esc(m['path'].stem)}" for m in live]
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
                       f'{head_meta(base_url=base_url, title="How this site works", description=DISCLOSURE_DESCRIPTION, path="/disclosure")}'
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
        link = f"{base_url}/posts/{esc(m['path'].stem)}" if base_url else f"/posts/{esc(m['path'].stem)}"
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
