#!/usr/bin/env python3
"""Verify finding.md's quotes: every quotes.tsv row must (a) match the pinned file at its own line,
(b) appear in receipts/greps.txt, (c) be at most 25 words. Code-looking spans in finding.md that no
row covers are printed as warnings (not failures) so the uncovered surface is visible.

Usage: python3 -I verify-quotes.py            # from anywhere; paths are relative to the lane root
Exit 0 = all rows verified and no failure; 1 = at least one failure.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FINDING = os.path.join(HERE, "finding.md")
QUOTES = os.path.join(HERE, "quotes.tsv")
RECEIPT = os.path.join(HERE, "receipts", "greps.txt")
MAX_WORDS = 25


def norm(s):
    return re.sub(r"[ \t]+", " ", s).strip()


def main():
    fails = []
    receipt = norm(open(RECEIPT, encoding="utf-8", errors="replace").read())
    finding = open(FINDING, encoding="utf-8").read()
    rows = []
    for i, raw in enumerate(open(QUOTES, encoding="utf-8").read().splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) != 3:
            fails.append(f"quotes.tsv:{i}: need 3 tab-separated fields, got {len(parts)}")
            continue
        rel, line_s, needle = parts
        try:
            line = int(line_s)
        except ValueError:
            fails.append(f"quotes.tsv:{i}: line {line_s!r} is not an int")
            continue
        path = os.path.join(LANE, rel)
        if not os.path.isfile(path):
            fails.append(f"quotes.tsv:{i}: missing pin {rel}")
            continue
        src = open(path, encoding="utf-8", errors="replace").read().splitlines()
        if line > len(src):
            fails.append(f"quotes.tsv:{i}: {rel} has {len(src)} lines, row says {line}")
            continue
        if norm(needle) not in norm(src[line - 1]):
            fails.append(f"quotes.tsv:{i}: {rel}:{line} does not contain the needle")
        if norm(needle) not in receipt:
            fails.append(f"quotes.tsv:{i}: needle absent from receipts/greps.txt")
        words = len(needle.split())
        if words > MAX_WORDS:
            fails.append(f"quotes.tsv:{i}: needle is {words} words (> {MAX_WORDS})")
        rows.append(norm(needle))

    # uncovered code-looking spans in the finding: a span is covered when it is a substring of a
    # needle, or a needle is a substring of it (locator plus quote in one span)
    warn = []
    for span in re.findall(r"`([^`\n]+)`", finding):
        s = norm(span)
        if len(s) < 4 or s.startswith(("pins/", ".ufo/", "skill://", "agent://")):
            continue
        if not any(ch in s for ch in "()=;{}<>|&*+"):
            continue
        if any(s in r or r in s for r in rows):
            continue
        warn.append(s)

    for w in warn:
        print(f"WARN uncovered span: {w}")
    for f in fails:
        print(f"FAIL {f}")
    print(f"QUOTES: rows={len(rows)} fails={len(fails)} uncovered={len(warn)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
