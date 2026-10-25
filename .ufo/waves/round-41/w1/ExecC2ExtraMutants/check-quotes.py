#!/usr/bin/env python3
"""Verify every quoted counter line in survivors.md at its cited file:line.

A quote line has the form

    > "<quote, with \\" for a literal quote mark>" — <path>:<line>

The quote must (1) be <= 25 words and (2) occur verbatim in that line of that
file. Final line: `quote check: K/N`.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
DOC = os.path.join(HERE, "survivors.md")
PAT = re.compile(r'^> "(.*)" \u2014 (\S+):(\d+)$')


def unescape(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] in '\\"':
            out.append(s[i + 1])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def main():
    cache = {}
    ok = total = 0
    for line in open(DOC, encoding="utf-8").read().splitlines():
        m = PAT.match(line)
        if not m:
            continue
        total += 1
        quote, path, lineno = unescape(m.group(1)), m.group(2), int(m.group(3))
        words = len(quote.split())
        if path not in cache:
            with open(os.path.join(LANE, path), encoding="utf-8") as fh:
                cache[path] = fh.read().splitlines()
        lines = cache[path]
        hit = 0 < lineno <= len(lines) and quote in lines[lineno - 1]
        good = hit and words <= 25
        ok += good
        print("%s words=%d %s:%d %r" % (
            "OK  " if good else "FAIL", words, path, lineno, quote[:60]))
    print("quote check: %d/%d" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
