#!/usr/bin/env python3
"""Verify the quotes the ExecControlsC1 report lifts from the counter draft: each must be a verbatim substring of the
line it is cited at, and at most 25 words.

Usage: check-quotes.py > receipts/quotes.txt
"""
import os
import sys

DRAFT = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecCounterC1/c1-r49-keysym.py")
QUOTES = [
    (DRAFT, 87, "clause g is what that tool fails"),
    (DRAFT, 49, "readonly=ok iff trips=0 over all runs"),
]


def main():
    bad = 0
    print("# quote verification (grep of the cited line; words <= 25)")
    print("# script: .ufo/waves/round-49/w1/ExecControlsC1/check-quotes.py")
    for path, line_no, quote in QUOTES:
        words = len(quote.split())
        with open(path, encoding="utf-8") as fh:
            line = fh.read().splitlines()[line_no - 1]
        ok = quote in line and words <= 25
        bad += 0 if ok else 1
        print("%s %s:%d words=%d quote=%r" % ("OK  " if ok else "FAIL", os.path.basename(path), line_no, words, quote))
    print("quotes=%d failed=%d" % (len(QUOTES), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
