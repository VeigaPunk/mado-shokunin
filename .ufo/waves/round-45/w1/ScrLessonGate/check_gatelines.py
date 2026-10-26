#!/usr/bin/env python3
"""ScrLessonGate: rebuild the nine GATE lines from build-pos.py's own QUOTES/PINS
inputs (lane fetch bytes) and diff them against the draft's lines, so the draft's
Gate section is provably the generator's format. Read-only."""
import hashlib
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
F = ".ufo/waves/round-45/fetch/"
bp = open(os.path.join(LANE, ".ufo/waves/round-45/l1-draft/build-pos.py")).read()
import ast
QUOTES = ast.literal_eval(re.search(r"QUOTES = (\{.*?\n\})", bp, re.S).group(1))

exp = []
for rid in sorted(QUOTES):
    rname, quote = QUOTES[rid]
    blob = open(os.path.join(LANE, F + rname), "rb").read()
    exp.append('GATE %s receipt=%s%s sha256=%s quote="%s"'
               % (rid, F, rname, hashlib.sha256(blob).hexdigest(), quote))

draft = open(os.path.join(
    LANE, ".ufo/waves/round-45/w1/ScrLessonGate/round-45.md")).read()
got = [l for l in draft.splitlines() if l.startswith("GATE S")]
print("expected=%d draft=%d" % (len(exp), len(got)))
bad = 0
for e, g in zip(exp, got):
    same = e == g
    bad += not same
    print("%s %s" % ("MATCH" if same else "DIFF ", e[:96]))
print("GATE_LINES_IDENTICAL=%d" % int(len(exp) == len(got) and not bad))
raise SystemExit(0 if (len(exp) == len(got) and not bad) else 1)
