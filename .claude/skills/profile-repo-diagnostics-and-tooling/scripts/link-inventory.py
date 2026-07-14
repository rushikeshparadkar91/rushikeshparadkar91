#!/usr/bin/env python3
"""link-inventory.py — extract every URL and image reference from a markdown file.

Usage: ./link-inventory.py path/to/README.md [--check]

Default mode is OFFLINE: it only parses and prints a table
(KIND | LINE | URL) — one row per reference. KIND is one of:
  image-md     markdown image  ![alt](url)
  image-html   <img src="url">
  link-md      markdown link   [text](url)
  link-auto    bare/angle-bracket URL in prose
Duplicates are kept (each occurrence is a row) so line numbers stay useful.

--check adds a STATUS column by issuing an HTTP HEAD request (5s timeout,
python3 stdlib only) to each unique http(s) URL. NOTE: in Claude remote
sessions outbound network is policy-filtered (verified 2026-07-14:
docs.github.com → 403); a 403/connection error under --check may mean
sandbox policy, not a dead link. Re-run --check from an unrestricted
machine before declaring a link dead.

Exit codes: 0 = table printed (even if empty); 2 = usage/file error.
--check does not change the exit code; read the STATUS column instead.
"""
import re
import sys

MD_IMG = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)[^)]*\)")
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)[^)]*\)")
HTML_IMG = re.compile(r"<img[^>]*\ssrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
BARE_URL = re.compile(r"(?<![(\"'<\]])(https?://[^\s)\"'<>\]]+)")


def head(url: str) -> str:
    import urllib.request
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "link-inventory/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return str(resp.status)
    except Exception as e:  # noqa: BLE001 — report, don't crash
        return f"ERR:{type(e).__name__}:{e}"[:60]


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        return 2
    try:
        with open(args[0], encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except OSError as e:
        print(f"ERROR: cannot read {args[0]}: {e}")
        return 2

    rows = []
    for lineno, line in enumerate(lines, 1):
        seen_spans = []

        def add(kind, m, url):
            rows.append((kind, lineno, url))
            seen_spans.append(m.span(1))

        for m in MD_IMG.finditer(line):
            add("image-md", m, m.group(1))
        for m in HTML_IMG.finditer(line):
            add("image-html", m, m.group(1))
        for m in MD_LINK.finditer(line):
            add("link-md", m, m.group(1))
        for m in BARE_URL.finditer(line):
            if not any(s <= m.start(1) < e for s, e in seen_spans):
                rows.append(("link-auto", lineno, m.group(1)))

    header = ["KIND", "LINE", "URL"] + (["STATUS"] if check else [])
    print(" | ".join(header))
    print("-|-".join("-" * len(h) for h in header))
    status_cache = {}
    for kind, lineno, url in rows:
        row = [kind, str(lineno), url]
        if check:
            if url.startswith(("http://", "https://")):
                if url not in status_cache:
                    status_cache[url] = head(url)
                row.append(status_cache[url])
            else:
                row.append("skipped(non-http)")
        print(" | ".join(row))
    print(f"TOTAL: {len(rows)} reference(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
