#!/usr/bin/env python3
"""Verify the one quoted source sentence in this seat's report.

The report quotes the frozen gate's R3 rule description. This script extracts
that sentence from the report itself, normalises backticks and whitespace on
both sides, and proves the same words occupy docstring lines 26-28 of the
frozen file (which this seat did not modify: sha256 889f8f05…).
"""
import hashlib
import re
import sys

GATE = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py"
REPORT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecSerialRule.md"
LINES = (26, 28)
ANCHOR = "a JSON object with a non-empty"


def norm(text):
    return re.sub(r"\s+", " ", text.replace("`", "")).strip()


source = open(GATE, encoding="utf-8").read().splitlines()
window = norm("\n".join(source[LINES[0] - 1:LINES[1]]))
report = [norm(line) for line in open(REPORT, encoding="utf-8")]
quote = next((line.strip('"') for line in report if ANCHOR in line), "")
print("GATE_SHA256 %s" % hashlib.sha256(open(GATE, "rb").read()).hexdigest())
print("QUOTE_LINES %d-%d" % LINES)
print("QUOTE_WORDS %d" % len(quote.split()))
print("QUOTE_IN_SOURCE %s" % (bool(quote) and quote in window))
sys.exit(0 if quote and quote in window else 1)
