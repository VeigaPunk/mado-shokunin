#!/usr/bin/env python3
"""Verify every quote in quotes.json against its cited source lines (locators computed, never typed).

For each quote: read the named file, keep the cited line range, normalise whitespace, require the quote text to be a
substring, and require <= 25 words. Last line `QUOTES: N/N ok`; exit 0 iff all pass.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    quotes = json.load(open(os.path.join(HERE, "quotes.json")))
    ok = 0
    for q in quotes:
        try:
            lines = open(q["file"], encoding="utf-8", errors="surrogateescape").read().splitlines()
        except OSError as e:
            print("%s FAIL unreadable %s (%s)" % (q["id"], q["file"], e))
            continue
        parts = q["lines"].split("-")
        lo = int(parts[0])
        hi = int(parts[1]) if len(parts) > 1 else lo
        span = norm(" ".join(lines[lo - 1:hi]))
        text = norm(q["text"])
        words = len(text.split())
        if text not in span:
            print("%s FAIL not at %s:%s -- span=%r" % (q["id"], os.path.basename(q["file"]), q["lines"], span[:120]))
            continue
        if words > 25:
            print("%s FAIL %d words (>25)" % (q["id"], words))
            continue
        ok += 1
        print("%s ok %s:%s words=%d" % (q["id"], os.path.basename(q["file"]), q["lines"], words))
    print("QUOTES: %d/%d ok" % (ok, len(quotes)))
    return 0 if ok == len(quotes) else 1


if __name__ == "__main__":
    sys.exit(main())
