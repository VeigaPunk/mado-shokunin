#!/usr/bin/env python3
"""Verify every quote and evidence block of ../ExecIndepA.md against its receipt.

Rules checked:
  * `> quote  <-- draft:N`  : the quote (whitespace-normalised) occurs in
    receipts/contract-docstring.txt starting at line draft:N, and holds <= 25 words.
  * `<!-- evid PATH:LINE -->` followed by a fenced block : the block equals PATH's line LINE verbatim.
"""
import os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-46/w1/ExecIndepA")
REPORT = os.path.join(LANE, ".ufo/waves/round-46/w1/ExecIndepA.md")
CONTRACT = os.path.join(SEAT, "receipts/contract-docstring.txt")
QUOTE = re.compile(r"> (.+?)  <-- draft:(\d+)")
EVID = re.compile(r"^<!-- evid (.+?):(\d+) -->$")


def norm(text):
    return " ".join(text.split())


def unescape(text):
    """Markdown cannot carry a bare pipe inside a table cell, so the report escapes it as \\|."""
    return text.replace("\\|", "|")


contract = {}
for raw in open(CONTRACT, encoding="utf-8").read().split("\n"):
    m = re.match(r"^draft:(\d+): (.*)$", raw)
    if m:
        contract[int(m.group(1))] = m.group(2)

lines = open(REPORT, encoding="utf-8").read().split("\n")
fails, quotes, evids = [], 0, 0
i = 0
while i < len(lines):
    line = lines[i]
    m = QUOTE.search(line)
    if m:
        quotes += 1
        quote, number = unescape(m.group(1)), int(m.group(2))
        window = " ".join(contract.get(number + k, "") for k in range(4))
        words = len(quote.split())
        ok = norm(quote) in norm(window) and words <= 25
        if not ok:
            fails.append("quote draft:%d (%d words): %r" % (number, words, quote))
        i += 1
        continue
    m = EVID.match(line)
    if m:
        path, number = m.group(1), int(m.group(2))
        if i + 1 >= len(lines) or lines[i + 1].strip() != "```":
            fails.append("evid %s:%d: no fenced block" % (path, number))
            i += 1
            continue
        j = i + 2
        body = []
        while j < len(lines) and lines[j].strip() != "```":
            body.append(lines[j])
            j += 1
        evids += 1
        src = open(os.path.join(LANE, path), encoding="utf-8").read().split("\n")
        if number < 1 or number > len(src):
            fails.append("evid %s:%d: line out of range" % (path, number))
        elif "\n".join(body).rstrip() != src[number - 1].rstrip():
            fails.append("evid %s:%d: block does not match the receipt line" % (path, number))
        i = j + 1
        continue
    i += 1

for fail in fails:
    print("FAIL " + fail)
print("VERIFY: quotes=%d evids=%d failures=%d %s" % (quotes, evids, len(fails),
                                                     "PASS" if not fails else "FAIL"))
sys.exit(0 if not fails else 1)
