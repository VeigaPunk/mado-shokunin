#!/usr/bin/env python3
"""Verify every locator in quotes.txt: the quoted substring must appear on the cited line.

Run from anywhere:  python3 verify-quotes.py
Exit 0 = all quotes verified. Prints one PASS/FAIL line per quote.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"


def main() -> int:
    quotes = os.path.join(HERE, "quotes.txt")
    bad = 0
    total = 0
    for raw in open(quotes, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        loc, text = line.split("\t", 1)
        path, num = loc.rsplit(":", 1)
        full = path if os.path.isabs(path) else os.path.join(LANE, path)
        try:
            src = open(full, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as exc:
            print(f"FAIL missing source {full}: {exc}")
            bad += 1
            continue
        n = int(num)
        total += 1
        words = len(text.split())
        ok = 0 < n <= len(src) and text in src[n - 1]
        if ok and words > 25:
            print(f"FAIL too long ({words} words) {loc}: {text}")
            bad += 1
        elif ok:
            print(f"PASS {loc} ({words}w) {text}")
        else:
            near = src[n - 1] if 0 < n <= len(src) else "<out of range>"
            print(f"FAIL {loc}: not found. line reads: {near[:120]!r}")
            bad += 1
    print(f"\n{total - bad}/{total} verified")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
