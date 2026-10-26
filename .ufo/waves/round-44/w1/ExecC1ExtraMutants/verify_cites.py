#!/usr/bin/env python3
"""Verify every source citation used by survivors.md / the seat report.

Each entry is (file, line, quoted substring): the quoted substring must occur on that exact line
(1-based). Writes a PASS/FAIL table; exit 1 if any citation fails. Quotes are kept short.
"""
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = ".ufo/waves/round-44/c1/ctl-ref-tool.py.txt"
CTR = "quality/counters/c1-r44-geometry-states.py"
OLD = "quality/counters/c1-r42-geometry.py"

CITES = [
    (REF, 195, "def client_fsmode(c):"),
    (REF, 197, "f in (1, 2)"),
    (REF, 199, "return 0"),
    (REF, 233, "elif fsmode == 2:"),
    (REF, 235, "elif fsmode == 1:"),
    (REF, 237, "elif not floating:"),
    (REF, 243, "tally[verdict.lower()] += 1"),
    (REF, 269, 'if t["maximized"] + t["fullscreen"] > 0:'),
    (REF, 270, 'states = " maximized=%d fullscreen=%d"'),
    (REF, 458, 'for v in (1, 2, 0, 3, True, 2.0, "1", None)], [1, 2, 0, 0, 0, 0, 0, 0])'),
    (CTR, 76, "MIN_STATE_SITES = 6"),
    (CTR, 77, "KILL_FRACTION = 0.75"),
    (CTR, 90, "type(f) is int and f in (1, 2)"),
    (CTR, 283, "len(node.ops) == 1"),
    (CTR, 294, "need = math.ceil(KILL_FRACTION * len(sites))"),
    (CTR, 356, 'if cl["b"]:'),
    (CTR, 357, 'cl["b4"] = int(state_teeth'),
    (OLD, 838, "FLIP = {ast.Eq: ast.NotEq"),
]

bad = 0
print("cite-check: file:line -> quoted substring must be on that line")
for rel, lineno, quote in CITES:
    path = os.path.join(LANE, rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    ok = 0 < lineno <= len(lines) and quote in lines[lineno - 1]
    bad += not ok
    print("%s %s:%d %r" % ("PASS" if ok else "FAIL", rel, lineno, quote))
print("CITE CHECK: %d/%d pass" % (len(CITES) - bad, len(CITES)))
sys.exit(1 if bad else 0)
