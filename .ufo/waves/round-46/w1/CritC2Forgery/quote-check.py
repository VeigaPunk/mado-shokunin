#!/usr/bin/env python3
"""Verify every quote used in the CritC2Forgery report: the quote occurs in the named file (whitespace
collapsed, so a wrapped sentence still counts), it is <= 25 words, and its locator is computed here."""
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin/"
Q = [
    ("quality/counters/c2-r46-input-device-entry.py", "a true quote at a true locator can stand beside a claim it does not support"),
    ("quality/counters/c2-r46-input-device-entry.py", "a decision table naming no id is not bound"),
    ("quality/counters/c2-r46-input-device-entry.py", "a census value contradicted in words rather than tokens is not caught"),
    ("quality/counters/c2-r46-input-device-entry.py", "finds each of its tokens in the first cited receipt at REV"),
    ("quality/counters/c2-r46-input-device-entry.py", "a fenced block may only carry text that occurs verbatim in a pinned receipt"),
    ("quality/counters/c2-r46-input-device-entry.py", "j  surface coverage: for each SURFACES item"),
    (".ufo/waves/round-46/registration.md", "claim-to-quote binding, word-form census contradictions and registry prose cells are the non-author reading"),
    ("quality/counters/c2-r46-input-device-entry.py", "registry cells 3-6 of a new row are not read except the scope cell"),
]


def collapse(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


bad = 0
for path, q in Q:
    text = open(LANE + path, encoding="utf-8", errors="replace").read()
    flat, lines = collapse(text)
    nq = re.sub(r"\s+", " ", q).strip()
    k = flat.find(nq)
    words = len(nq.split())
    ok = k >= 0 and words <= 25
    bad += not ok
    print("%s:%s lines=%d words=%d %s" % (path, lines[k] if k >= 0 else "-", lines[k] if k >= 0 else 0,
                                          words, "OK" if ok else "FAIL"))
sys.exit(1 if bad else 0)
