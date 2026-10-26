#!/usr/bin/env python3
"""Seat MutC1Fixtures: run the proposed kill-fixtures through verify.py for every
surviving mutant. Prints VERIFY-VERDICT per case + writes receipts."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fixtures-proposed")
PAIRS = [
    ("k-readsplit-appid.json", "I-READSPLIT-APPID"),
    ("k-tok-quoted-esc-nonspecial.json", "I-TOK-QUOTED-ESC-NONSPECIAL"),
    ("k-tryexec-abs-cwd.json", "I-TRYEXEC-ABS-CWD"),
    ("k-test-with-print.json", "I-TEST-WITH-PRINT"),
    ("k-printcmd-empty-delim.json", "I-PRINTCMD-EMPTY-DELIM"),
    ("k-commandv-functions.json", "I-COMMANDV-FUNCTIONS"),
    ("k-tok-squote-in-dquote.json", "I-TOK-SQUOTE-IN-DQUOTE"),
    ("k-execarg-eq-only.json", "I-EXECARG-EQ-ONLY"),
]

for case, mid in PAIRS:
    p = subprocess.run(["python3", "-I", "verify.py", os.path.join(F, case), mid,
                        "--label", case[:-5]], capture_output=True, text=True,
                       cwd=HERE)
    print(p.stdout.strip())
    if p.stderr.strip():
        print("STDERR:", p.stderr.strip()[:300], file=sys.stderr)
