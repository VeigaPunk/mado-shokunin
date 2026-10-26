#!/usr/bin/env python3
"""Bind every docstring quote in this seat's report to its computed location in the reference docstring.

The reference's code below the docstring is never read: only ast.get_docstring() is used. For each quote
(ellipses split it into fragments) the script normalizes whitespace, asserts each fragment occurs verbatim in
the docstring, asserts the whole quote is <= 25 words, computes the docstring file:line of the first
fragment, and asserts the quote also appears in the report (backtick/ellipsis-insensitive, fragment-wise).
"""
import ast
import re
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
REPORT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecIndepA.md"

QUOTES = [
    ("Q1 add-erases", "Adding a rule erases every earlier rule with the same selector and appends it."),
    ("Q2 transform-copies", "The first rule in the current list whose selector equals SEL is copied with that transform and the copy is added"),
    ("Q3 addreserved-noop", "If a rule with selector SEL exists nothing changes (the reserved area is not compared)"),
    ("Q4 rules-numbered", "Rules are numbered n=1.. in the final list."),
    ("Q5 transform-modifier-bad", "field 1 `transform`: field 2 must be one digit 0-7, else the line adds one to `badrules`."),
    ("Q6 value-outside-forms", "A MODE, POSITION, SCALE or transform VALUE outside these forms makes the line `unsupported` (not modelled)."),
    ("Q7 live-disabled", "live_disabled is `disabled` == JSON true"),
    ("Q8 booleans-never-numbers", "a string for mirrorOf; booleans are never numbers"),
    ("Q9 scale-correction", "else, with K = round-half-up(S*120), K/120 when it divides both; else the first of (K+i)/120, (K-i)/120 for i = 1..89"),
    ("Q10 scale-not-compared", "none found means the scale is not compared"),
    ("Q11 scale-32-bit", "S (a 32-bit float; S < 0.25 becomes 1.0, as Hyprland's parser does)"),
    ("Q12 two-token", "two-token form only; anything else is usage"),
    ("Q13 no-rules", "NO_RULES (exit 4, lines = 0 and v2 = 0)"),
    ("Q14 monitorv2-token", "A line whose first token (up to a space, tab, `=` or `{`) is `monitorv2` adds one to `v2`."),
    ("Q15 key-loop", "KEY VALUE pairs from field 4 while the key field is not"),
    ("Q16 field-past-end", 'field i is "" past the end'),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    src = open(REF, encoding="utf-8").read()
    tree = ast.parse(src)
    doc = ast.get_docstring(tree, clean=False)
    start = tree.body[0].lineno  # file line holding the opening quotes of the docstring
    rawlines = doc.split("\n")
    # concatenate the normalized lines, remembering the docstring-line of every character
    parts, owner = [], []
    for ln, raw in enumerate(rawlines):
        nraw = norm(raw)
        if not nraw:
            continue
        if parts:
            parts.append(" ")
            owner.append(ln)
        parts.append(nraw)
        owner.extend([ln] * len(nraw))
    ndoc = "".join(parts)
    report = norm(open(REPORT, encoding="utf-8").read().replace("`", "").replace("…", " "))
    bad = 0
    rows = []
    for label, quote in QUOTES:
        frags = [norm(f) for f in quote.split("…") if norm(f)]
        words = len(quote.split())
        idx = ndoc.find(frags[0])
        ok = idx >= 0 and all(norm(f).replace("`", "") in ndoc.replace("`", "") for f in frags)
        line = start + owner[idx] if idx >= 0 else -1
        in_report = all(norm(f).replace("`", "").replace('"', '"') in report for f in frags)
        ok = ok and words <= 25 and in_report
        bad += 0 if ok else 1
        rows.append("%-26s words=%2d ref:%d %-4s report=%s %s" % (
            label, words, line if line >= 0 else -1, "ok" if idx >= 0 else "MISS",
            "yes" if in_report else "NO", "" if ok else "<-- FAIL"))
    print("\n".join(rows))
    print("MADO_QUOTES: checked=%d bad=%d doc_lines=%d report=%s" % (
        len(QUOTES), bad, len(doc.split("\n")), REPORT.rsplit("/", 1)[-1]))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
