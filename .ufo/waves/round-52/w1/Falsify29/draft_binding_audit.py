#!/usr/bin/env python3
"""Binding vs. entailment on the live C2 draft map (frozen snapshot).

Input: the seat's snapshot of `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv`
(sha256 447b84b4e448707b693b23f3eac5ef00bebf1fbeea52f6057c1f1889e52e48ce), so the audit does
not chase a file a peer is still editing.

Part 1: every row's quote — word count, verbatim at the stated anchor. This is the frozen
        machine-checkable binding; it must pass.
Part 2: for the rows whose proposition asserts a predicate: print the quote, then the source
        window around the anchor with quote-covered lines marked. Where the asserted predicate
        lives outside every marked line, the quote does not carry the proposition.
No entailment automation: the verdicts are read off printed bytes in the report.
"""
import csv
import os
import re
import sys

SCR = os.path.dirname(os.path.abspath(__file__))
TSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCR, "fixture/draft-proposition-map.snapshot.tsv")
FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/fetch"

# rows the report discusses: (prop, first_line, last_line) source window to print
WINDOWS = {
    "P03": (596, 606),
    "P15": (612, 624),
    "P16": (1601, 1617),
}


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return collapse(s).split()


rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
print("map: %s" % TSV)
print("%-4s %-6s %-7s %-8s %s" % ("prop", "row", "qwords", "verbatim", "anchor lines"))
bad = []
for r in rows:
    m = re.match(r"^(?P<path>.+?):(?P<first>\d+)(?:-(?P<last>\d+))?$", r["anchor"])
    if not m:
        bad.append(r["prop"])
        continue
    pin = os.path.join(FETCH, os.path.basename(m.group("path")))
    first, last = int(m.group("first")), int(m.group("last") or m.group("first"))
    lines = open(pin, encoding="utf-8", errors="replace").read().splitlines()
    span = lines[first - 1:min(last, len(lines))]
    hay = collapse("\n".join(span))
    q, wc = r["quote"], len(words(r["quote"]))
    verbatim = collapse(q) in hay
    print("%-4s %-6s %-7d %-8s %d-%d" % (r["prop"], r["row"], wc, "yes" if verbatim else "NO", first, last))
    if wc > 25 or not verbatim:
        bad.append(r["prop"])

print()
print("binding: %s" % ("all rows <=25 words and verbatim at their stated anchor"
                       if not bad else "FAIL " + ",".join(bad)))
print()
print("support check on the rows whose proposition carries an operative predicate")
print("(quote lines marked `*`, uncovered source lines marked `-`):")
for r in rows:
    if r["prop"] not in WINDOWS:
        continue
    m = re.match(r"^(?P<path>.+?):(?P<first>\d+)", r["anchor"])
    pin = os.path.join(FETCH, os.path.basename(m.group("path")))
    q = r["quote"]
    lo, hi = WINDOWS[r["prop"]]
    lines = open(pin, encoding="utf-8", errors="replace").read().splitlines()
    print()
    print("%s  proposition: %s" % (r["prop"], collapse(r["proposition"])))
    print("     quote      : %s" % q)
    print("     anchor     : %s" % r["anchor"])
    for n in range(lo, min(hi, len(lines)) + 1):
        text = lines[n - 1]
        if not text.strip():
            continue
        inside = collapse(text.strip()) and collapse(text.strip()) in collapse(q)
        print("     %s %d: %s" % ("*" if inside else "-", n, text.strip()))
