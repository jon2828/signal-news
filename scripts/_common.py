#!/usr/bin/env python3
"""Shared helpers for the Unspent Thoughts pipeline scripts."""
import html.parser
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"

BASE_URLS = {
    "groq": "https://api.groq.com/openai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "nvidia": "https://integrate.api.nvidia.com/v1",
}


def config() -> dict:
    return json.loads((ROOT / "config" / "pipeline.json").read_text())


def kill_switch(cfg: dict | None = None) -> bool:
    """True when the pipeline must not run: config flag off, or env override."""
    cfg = cfg or config()
    if not cfg.get("pipeline_enabled", True):
        return True
    env = os.environ.get("PIPELINE_ENABLED")
    return env is not None and env.strip().lower() in ("0", "false", "off", "no")


def guarded_exit(script_name: str) -> int:
    print(f"[{script_name}] pipeline_enabled is off (kill switch). Exiting without posting.")
    return 0


def _return_to_queue(cand: dict) -> None:
    """A drop must not permanently lose a high scorer: put the candidate
    back so the next triage can reconsider it."""
    path = ROOT / "state" / "candidates.json"
    try:
        candidates = json.loads(path.read_text())
        if not any(c["id"] == cand["id"] for c in candidates):
            candidates.append(cand)
            path.write_text(json.dumps(candidates, indent=1))
    except Exception:
        pass


def provider_client(cfg: dict) -> tuple[str | None, str | None, str | None]:
    """First available (provider, base_url, api_key) from the configured chain."""
    for prov, base_url, key in provider_chain_clients(cfg):
        return prov, base_url, key
    return None, None, None


def provider_chain_clients(cfg: dict, order: list[str] | None = None):
    """Every available (provider, base_url, api_key), in the given order
    (default: the configured provider chain)."""
    keys = cfg.get("env_keys", {})
    for prov in (order or cfg.get("provider_chain", [])):
        key = os.environ.get(keys.get(prov, ""), "").strip()
        if not key:
            continue
        if prov == "cloudflare":
            acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
            if not acct:
                continue
            yield prov, f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/v1", key
        else:
            yield prov, BASE_URLS.get(prov, ""), key


def chat_with_fallback(cfg: dict, job: str, prompt: str, max_tokens: int = 4000,
                       temperature: float | None = None, timeout: int = 300):
    """Try each provider in the chain, in order. Returns (content, provider).

    A provider failure (HTTP error, rate limit, error payload, timeout) is
    logged and the next provider is tried. Raises RuntimeError when all fail.
    """
    temps = cfg.get("temperature", {})
    errors = []
    chain = cfg.get("job_chain", {}).get(job) or cfg.get("provider_chain", [])
    ordered = [p for p in chain if p in cfg.get("provider_chain", [])]
    for prov, base_url, api_key in provider_chain_clients(cfg, order=ordered):
        model = cfg.get("models", {}).get(job, {}).get(prov)
        if not model:
            continue
        try:
            content = chat(model, prompt, "", base_url, api_key,
                           temperature=temps.get(job, 0.0) if temperature is None else temperature,
                           max_tokens=max_tokens, timeout=timeout)
            return content, prov
        except Exception as e:
            detail = f"{prov}:{model}: {type(e).__name__}: {e}"[:160]
            errors.append(detail)
            log_decision(f"{job}_provider_failed", detail)
    raise RuntimeError("all providers failed: " + " | ".join(errors))


def chat(model: str, prompt: str, user_content: str, base_url: str,
         api_key: str, temperature: float = 0.0, max_tokens: int = 4000,
         timeout: int = 120) -> str:
    """OpenAI-compatible chat completion via urllib. Returns message content."""
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{user_content}"},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json",
                 # Groq (and other Cloudflare-fronted APIs) return error 1010
                 # for urllib's default Python UA. A normal UA passes.
                 "User-Agent": "UnspentThoughtsBot/1.0 (news pipeline; +https://github.com/jon/signal-news)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    if not isinstance(data, dict) or "choices" not in data:
        # Some free-tier providers return {"error": ...} with HTTP 200.
        err = data.get("error") if isinstance(data, dict) else data
        raise RuntimeError(f"no choices in response: {str(err)[:200]}")
    content = data["choices"][0]["message"].get("content") or ""
    if not content.strip():
        # Reasoning models can burn the whole token budget on reasoning_content
        # and return empty content. Treat as failure so fallback kicks in.
        raise RuntimeError("empty content in response (reasoning model spent the budget)")
    return content


def rewrite_for_lint(cfg: dict, body: str, hits: list, max_words: int, title: str = "") -> str | None:
    """One rewrite attempt to clear the anti-AI lint, preserving every fact.

    Jon's call: a story that scored well should not be thrown away over style.
    The writer model rephrases the flagged patterns; facts, numbers, quotes and
    source links must survive untouched. Returns the new body, or None when the
    attempt itself fails (the caller then publishes with a lint_flags note
    rather than dropping the story).
    """
    prompt_file = cfg.get("lint", {}).get("rewrite_prompt_file", "prompts/lint_rewrite.md")
    try:
        tpl = (ROOT / prompt_file).read_text()
    except OSError as e:
        log_decision("lint_rewrite_failed", json.dumps({"error": f"prompt missing: {e}"}[:160]))
        return None
    flagged = "\n".join(f"- {name} ({count}x): {'; '.join(examples)}" for name, count, examples in hits) or "- (word count only)"
    prompt = (tpl.replace("<<FLAGGED>>", flagged)
              .replace("<<MAX_WORDS>>", str(max_words))
              .replace("<<TITLE>>", title or "(untitled)")
              .replace("<<POST>>", body))
    try:
        raw, _prov = chat_with_fallback(cfg, "write", prompt, max_tokens=6000, timeout=420)
    except Exception as e:
        log_decision("lint_rewrite_failed", json.dumps({"error": f"{type(e).__name__}: {e}"[:160]}))
        return None
    text = re.sub(r"```[a-zA-Z]*", "", raw).strip()
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S).strip()
    if len(text) < 200:
        log_decision("lint_rewrite_failed", json.dumps({"error": f"rewrite too short ({len(text)} chars)"}))
        return None
    return text


def parse_json_blob(text: str):
    """Tolerant JSON extraction.

    Models emit reasoning prose, markdown fences, and JSON in varying shapes
    (bare array, single-key wrapper, verdict object). Instead of trusting the
    first brace in the text, scan every balanced top-level blob (ignoring
    braces inside strings) and return the most useful one: a dict carrying a
    'verdict' key if present, else the first array (unwrapping single-key
    objects whose value is a list), else the first object.
    """
    text = re.sub(r"```(?:json)?", "", text).strip().strip("`").strip()
    blobs: list = []
    stack: list[str] = []
    start = None
    in_str = False
    escaped = False
    for i, ch in enumerate(text):
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "[{":
            if not stack:
                start = i
            stack.append("]" if ch == "[" else "}")
        elif stack and ch == stack[-1]:
            stack.pop()
            if not stack and start is not None:
                try:
                    blobs.append(json.loads(text[start:i + 1]))
                except Exception:
                    pass
                start = None
    for blob in blobs:
        if isinstance(blob, dict) and "verdict" in blob:
            return blob
    for blob in blobs:
        if isinstance(blob, list):
            return blob
        if isinstance(blob, dict) and len(blob) == 1:
            only = next(iter(blob.values()))
            if isinstance(only, list):
                return only
    if blobs:
        return blobs[0]
    raise ValueError(f"no JSON found in model response: {text[:200]}")


def normalize_text(text: str) -> str:
    """Mechanical fixes the lint would otherwise reject a draft for:
    curly quotes -> straight, em-dash -> comma, en-dash -> hyphen.
    Deterministic and safe; editorial style is the lint's job after this."""
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u2014", ", ").replace("\u2013", "-")
    return re.sub(r"(, ){2,}", ", ", re.sub(r" ,", ",", text))


def slugify(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s-]+", "-", s)
    return s[:maxlen].strip("-") or "post"


class _TextExtractor(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript", "nav", "footer", "header", "aside"}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "br", "tr"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.parts.append(data)


def strip_html(html_text: str) -> str:
    ex = _TextExtractor()
    ex.feed(html_text)
    text = "".join(ex.parts)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()


def _jina_fetch(url: str, cfg: dict, max_chars: int = 8000) -> str:
    """Free fallback for JS-heavy pages: r.jina.ai renders the page as
    markdown, no API key needed at low volume."""
    timeout = cfg.get("fetch", {}).get("timeout_seconds", 20)
    req = urllib.request.Request(f"https://r.jina.ai/{url}",
                                 headers={"User-Agent": "Mozilla/5.0 (compatible; UnspentThoughtsBot/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout + 40) as r:
        text = r.read(200000).decode("utf-8", "replace")
    marker = "Markdown Content:"
    if marker in text:
        text = text.split(marker, 1)[1]
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            lines.append("")
            continue
        clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # drop link syntax, keep text
        if clean.strip():
            lines.append(clean)
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()[:max_chars]


def extract_article(url: str, cfg: dict, max_chars: int = 6000) -> str:
    """Fetch a full article: direct (trafilatura) first, r.jina.ai fallback
    for pages that render empty without a browser."""
    timeout = cfg.get("fetch", {}).get("timeout_seconds", 20)
    ua = cfg.get("fetch", {}).get("user_agent", "Mozilla/5.0 (compatible; UnspentThoughtsBot/1.0)")
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    text = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(400000).decode("utf-8", "replace")
        try:
            import trafilatura  # type: ignore
            text = trafilatura.extract(raw) or strip_html(raw)
        except Exception:
            text = strip_html(raw)
    except Exception:
        text = ""
    if len(text) < 200:
        try:
            text = _jina_fetch(url, cfg)
        except Exception:
            pass
    return text[:max_chars]


def append_jsonl(path: Path, obj: dict) -> None:
    import datetime
    obj = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), **obj}
    with path.open("a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def log_decision(action: str, detail: str) -> None:
    STATE.mkdir(exist_ok=True)
    append_jsonl(STATE / "decisions.jsonl", {"action": action, "detail": detail})
