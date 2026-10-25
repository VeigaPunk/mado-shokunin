#!/usr/bin/env python3
"""Verify every quote printed in quarantine-verdicts.md against the fetched source bytes.

The verdicts file carries machine-checkable lines of the form

    QUOTE-CHECK|<label>|expect=<present|absent>|src=<html|abs|tex>|<quote>

This script normalizes each source (HTML tags stripped, entities unescaped, TeX
`\\%` -> `%`, whitespace collapsed) and checks the quote's presence/absence.
Exit 0 only when every line matches its expectation.

Sources (fetched 2026-10-25 by this seat, bytes kept beside this script):
    sources/arxiv-html-2604.18860.html    https://arxiv.org/html/2604.18860v1
    sources/arxiv-abs-2604.18860.html     https://arxiv.org/abs/2604.18860
    tex                                   /home/vgpnk/Projects/shokuknow/lanes/mado/round8/fetch/arXiv-2604.18860.txt
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERDICTS = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation/quarantine-verdicts.md")
TEX = Path("/home/vgpnk/Projects/shokuknow/lanes/mado/round8/fetch/arXiv-2604.18860.txt")

SRC = {
    "html": HERE / "sources" / "arxiv-html-2604.18860.html",
    "abs": HERE / "sources" / "arxiv-abs-2604.18860.html",
    "tex": TEX,
}


def norm(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".html":
        raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    raw = raw.replace("\\%", "%").replace("\\_", "_")
    return re.sub(r"\s+", " ", raw)


def main() -> int:
    text = VERDICTS.read_text(encoding="utf-8")
    rows = [l.split("|") for l in text.splitlines() if l.startswith("QUOTE-CHECK|")]
    if not rows:
        print("FAIL: no QUOTE-CHECK lines in", VERDICTS)
        return 1
    cache: dict[str, str] = {}
    bad = 0
    for parts in rows:
        label, exp, src, quote = parts[1], parts[2], parts[3], "|".join(parts[4:]).strip()
        want = exp.split("=", 1)[1]
        key = src.split("=", 1)[1]
        body = cache.setdefault(key, norm(SRC[key]))
        found = re.sub(r"\s+", " ", quote) in body
        ok = found if want == "present" else not found
        bad += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {label:<4} {want:<7} src={key:<4} found={str(found):<5} {quote[:72]}")
    print(f"QUOTE-CHECK checked={len(rows)} failed={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
