#!/usr/bin/env python3
"""Verify every quotation lifted into the seat's report/fuzz.md: <= 25 words,
located (file:line), and present in the named source file (grep). Writes
quotes-receipt.txt."""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"

QUOTES = [
    ("a FIFO or any other non-regular",
     os.path.join(SEAT, "counter-v2.py"), 35, 39),
    ("the tool must return, never block on opening or reading",
     os.path.join(SEAT, "counter-v2.py"), 35, 39),
    ("A SESSION starts at an ADVERT when no session is open",
     os.path.join(SEAT, "counter-v2.py"), 50, 65),
    ("anything else at the data tip is a miss, reported as an honest stop; no narrowing",
     os.path.join(LANE, ".ufo/waves/round-41/registration-v2.md"), 40, 41),
    ("clause g is a heuristic over names; the sandbox is detectable",
     os.path.join(LANE, ".ufo/waves/round-41/registration-v2.md"), 55, 57),
]


def main():
    out = []
    ok_all = True
    for quote, path, lo, hi in QUOTES:
        words = len(quote.split())
        wok = words <= 25
        text = ""
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
            window = "\n".join(lines[lo - 1:hi])
            found = quote in window
        except OSError as exc:
            found, window = False, "ERR %s" % exc
        ok = wok and found
        ok_all &= ok
        out.append("%s | words=%d | found=%s | %s:%d-%d" % (
            "OK " if ok else "FAIL", words, found, os.path.basename(path),
            lo, hi))
        out.append("    quote: %s" % quote)
    with open(os.path.join(SEAT, "quotes-receipt.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
