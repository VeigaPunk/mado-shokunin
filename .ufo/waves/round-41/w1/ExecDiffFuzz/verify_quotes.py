#!/usr/bin/env python3
"""Verify every quotation the seat report lifts from the frozen sources.

Each row: (file, first_line, last_line, quote). The quote must appear in that
line window (whitespace-collapsed) and be <= 25 words. Writes quotes-receipt.txt;
exits 1 if any row fails.

Usage: python3 -I verify_quotes.py
"""
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = "quality/counters/c1-r41-globals.py"
REF = ".ufo/waves/round-41/w1/ExecDiffFuzz/ref-tool.py"

ROWS = [
    (COUNTER, 19, 19, "Exactly one of --journal-file/--live"),
    (COUNTER, 20, 20, "a NAME must fully match [A-Za-z0-9_]{1,128}"),
    (COUNTER, 26, 26, 'Lines are split on "\\\\n"'),
    (COUNTER, 30, 31, "`\\\\d{1,6}`"),
    (COUNTER, 29, 29, "TS = `\\\\d{4}-\\\\d\\\\d-\\\\d\\\\dT"),
    (COUNTER, 31, 32, "bytes that are not UTF-8"),
    (COUNTER, 32, 32, "CR endings"),
    (COUNTER, 34, 34, "its PID differs from the open session's PID"),
    (COUNTER, 37, 37, "per distinct NAME: count and ver = the highest N seen"),
    (COUNTER, 42, 42,
     "MADO_GLOBAL: name=<name> ver=<max> count=<count> class=<class>"),
    (COUNTER, 48, 48, "Class decision table (name -> class"),
    (COUNTER, 62, 62, "journalctl_unusable"),
    (COUNTER, 68, 68, "more than 8 MiB of output is"),
    (REF, 104, 104, "ent[1] = max(ent[1], ver)"),
    (REF, 31, 33, "Got interface: ([A-Za-z0-9_]{1,128}) \\(ver (\\d{1,6})\\)"),
]


def collapse(s):
    return " ".join(s.split())


def main():
    out, bad = [], 0
    for path, first, last, quote in ROWS:
        full = os.path.join(LANE, path)
        lines = open(full, "r", encoding="utf-8").read().splitlines()
        window = collapse(" ".join(lines[first - 1:last]))
        q = collapse(quote)
        found = q in window
        words = len(q.split())
        ok = found and words <= 25
        bad += 0 if ok else 1
        out.append("%s %s:%d-%d words=%d found=%s %r"
                   % ("PASS" if ok else "FAIL", path, first, last, words,
                      found, q))
    text = "\n".join(out) + "\n"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "quotes-receipt.txt"), "w") as fh:
        fh.write(text)
    sys.stdout.write(text)
    print("verify_quotes: rows=%d failures=%d" % (len(ROWS), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
