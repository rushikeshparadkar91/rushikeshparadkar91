#!/usr/bin/env python3
"""readme-audit.py — static checks on a profile README markdown file.

Usage: ./readme-audit.py path/to/README.md

Checks (all offline, no network):
  1. File exists and is non-empty (an empty README does not render on the profile).
  2. Relative image references whose target file does not exist on disk
     (relative paths only resolve inside the repo; broken ones render as broken images).
  3. Bare http:// links (should be https://; GitHub camo may refuse plain http images).
  4. HTML tags outside a conservative GFM-safe allowlist.
     The allowlist below is Model knowledge (2026-07-14) — a conservative subset of
     what GitHub's sanitizer keeps; anything outside it is FLAGGED FOR REVIEW,
     not proven broken.
  5. Heading structure: warns if there is no H1/H2 at all, or heading levels jump
     by more than one (e.g. # straight to ###).

Exit codes: 0 = no findings; 1 = findings reported; 2 = usage/file error.
"""
import os
import re
import sys

# Model knowledge (2026-07-14): conservative subset of HTML tags GitHub's GFM
# sanitizer is known to keep in READMEs. Tags NOT listed are flagged for review.
GFM_SAFE_TAGS = {
    "a", "b", "blockquote", "br", "code", "dd", "del", "details", "div", "dl",
    "dt", "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "ins",
    "kbd", "li", "ol", "p", "picture", "pre", "q", "samp", "source", "strong",
    "sub", "summary", "sup", "table", "tbody", "td", "th", "thead", "tr", "ul",
}

IMG_MD = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)")
IMG_HTML = re.compile(r"<img[^>]*\ssrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
BARE_HTTP = re.compile(r"(?<![\w/])http://[^\s)\"'<>]+")
HTML_TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9-]*)")
HEADING = re.compile(r"^(#{1,6})\s+\S")
FENCE = re.compile(r"^\s*(```|~~~)")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"FINDING [missing]: {path} does not exist")
        return 1
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if not text.strip():
        print(f"FINDING [empty]: {path} exists but is empty/whitespace-only "
              "(an empty README does not render on the profile)")
        return 1

    findings = 0
    base = os.path.dirname(os.path.abspath(path))
    in_fence = False
    headings = []

    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue  # ignore code blocks

        # relative images with missing targets
        for m in IMG_MD.finditer(line) or []:
            targets = [m.group(1)]
            for t in targets + [g.group(1) for g in IMG_HTML.finditer(line)]:
                if t.startswith(("http://", "https://", "data:", "#", "mailto:")):
                    continue
                rel = t.split("#")[0].split("?")[0]
                if rel and not os.path.exists(os.path.join(base, rel)):
                    print(f"FINDING [broken-relative-image] line {lineno}: "
                          f"'{t}' not found relative to {base}")
                    findings += 1
        # html-only images on lines with no markdown image
        if not IMG_MD.search(line):
            for g in IMG_HTML.finditer(line):
                t = g.group(1)
                if not t.startswith(("http://", "https://", "data:")):
                    rel = t.split("#")[0].split("?")[0]
                    if rel and not os.path.exists(os.path.join(base, rel)):
                        print(f"FINDING [broken-relative-image] line {lineno}: "
                              f"'{t}' not found relative to {base}")
                        findings += 1

        for m in BARE_HTTP.finditer(line):
            print(f"FINDING [bare-http] line {lineno}: {m.group(0)} "
                  "(use https://)")
            findings += 1

        for m in HTML_TAG.finditer(line):
            tag = m.group(1).lower()
            if tag not in GFM_SAFE_TAGS:
                print(f"FINDING [html-outside-allowlist] line {lineno}: <{tag}> "
                      "— not in the conservative GFM-safe allowlist "
                      "(Model knowledge 2026-07-14); verify rendering manually")
                findings += 1

        h = HEADING.match(line)
        if h:
            headings.append((lineno, len(h.group(1))))

    if not headings:
        print("FINDING [no-headings]: no markdown headings found "
              "(profile READMEs usually open with an H1/H2)")
        findings += 1
    else:
        prev = headings[0][1]
        for lineno, level in headings[1:]:
            if level > prev + 1:
                print(f"FINDING [heading-jump] line {lineno}: "
                      f"H{prev} jumps to H{level} (skipped a level)")
                findings += 1
            prev = level

    if findings:
        print(f"RESULT: {findings} finding(s)")
        return 1
    print("RESULT: clean — no findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
