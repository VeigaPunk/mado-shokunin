#!/usr/bin/env python3
"""ExecDoNothingV2 - dump each fixture's entry text and evaluate two rule matrices.

No scoring here. Importing harness.py runs its data preparation only (its main() is guarded), so
the control texts are the same ones the harness scored. D15's entry is RECONSTRUCTED from the
landed entry and d15-swaps.txt (the swap table the harness's own run printed into
run-harness.log); harness.py's alt-quote scan is reproducible but slow, and the reconstruction is
checked against the D15 run's clause-g locators by harness.py's alt_quote probe in this seat's
report. The R-series controls are rejected, so the distinguishability question does not need them.

Answers the report's question: is the landed entry's prose distinguishable from an ADMITTED
do-nothing control by a mechanical rule? M-rules and E-rules are the cheap candidates.
"""
import difflib
import importlib.util
import os
import re

SEAT = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = load(os.path.join(SEAT, "harness.py"), "dn_harness")
C, R = H.C, H.R
OUT = os.path.join(SEAT, "entries")
os.makedirs(OUT, exist_ok=True)


def d15_reconstructed():
    entry = H.ENTRY_TEXT
    swaps = []
    for row in open(os.path.join(SEAT, "d15-swaps.txt")):
        m = re.match(r"^(S\d{3}) (\S+) (\d+) (\d+) (\d+) (.*)$", row.strip())
        if not m:
            continue
        i, fn, old_line, new_line, dist, cand = m.groups()
        old = re.sub(r"\s+", " ", H.GATES[i][2])
        entry = entry.replace(old, cand)
        entry = entry.replace("%s:%s" % (fn, old_line), "%s:%s" % (fn, new_line))
        swaps.append((i, fn, int(new_line)))
    return entry


FIX = [("L0-landed-verbatim", H.ENTRY_TEXT), ("P-registered", R.admitted()[R.ENTRY])]
for name, expected, build in H.D:
    FIX.append((name, d15_reconstructed() if name.startswith("D15") else build()[R.ENTRY]))

for name, text in FIX:
    open(os.path.join(OUT, name + ".md"), "w").write(text)

# ---- extended rules ---------------------------------------------------------------
CENSUS = set(H.CENSUS)


def body(text):
    return C.unfenced(text)


def source_order(text):
    out = []
    for l in body(text):
        m = re.match(r"^source: (S\d{3,})\b", l)
        if m:
            out.append(m.group(1))
    return out


def quote_line_order(text):
    """Order in which cited ids first appear OUTSIDE the source lines (the quote-bearing body)."""
    out = []
    for l in body(text):
        if l.startswith("source:"):
            continue
        for i in re.findall(r"\bS\d{3,}\b", l):
            if i not in out:
                out.append(i)
    return out


def in_section_prose(text):
    n, inside = 0, False
    for l in body(text):
        if l.startswith("## "):
            inside = bool(re.match(r"^## §", l))
            continue
        if not inside:
            continue
        t = l.strip()
        if (not t or t in CENSUS or t.startswith(H.HEADER_PREFIX) or t.startswith("|")
                or re.search(r"\bS\d{3,}\b", t)):
            continue
        n += 1
    return n


def negmark(text):
    pat = re.compile(r"nothing else|not taken on this host|^\*\*(INF|UNK)\*\* False:|"
                     r"does not hold|the opposite holds", re.I)
    return sum(1 for l in body(text) if pat.search(l))


EXTRA = [
    ("E1_has_OBS_marker", lambda t: any(l.startswith("**OBS**") for l in body(t))),
    ("E2_quote_order_eq_source_order", lambda t: quote_line_order(t) == source_order(t)),
    ("E3_prose_inside_sections_ge1", lambda t: in_section_prose(t) >= 1),
    ("E4_FullMatch_outside_quotes",
     lambda t: any("FullMatch" in l and H.GATES["S290"][2] not in l for l in body(t))),
    ("E5_negation_marker_any", lambda t: negmark(t) > 0),
]

rows = ["EXTRA RULES " + " ".join(k for k, _ in EXTRA),
        "(E-rules are the candidates a re-registration could add; M-rules are rules-matrix.txt's)", ""]
for name, text in FIX:
    rows.append("%-32s %s  M=%s" % (name, "".join("%d" % int(bool(f(text))) for _, f in EXTRA),
                                    H.rule_row(text)))
open(os.path.join(SEAT, "rules-matrix-extended.txt"), "w").write("\n".join(rows) + "\n")
print("\n".join(rows))

land = H.ENTRY_TEXT.split("\n")
delta = ["control entry_lines lines_minus_landed edits_vs_landed identical_to_landed"]
for name, text in FIX:
    a = list(difflib.unified_diff(land, text.split("\n"), n=0, lineterm=""))
    plus = sum(1 for l in a if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in a if l.startswith("-") and not l.startswith("---"))
    delta.append("%-32s %3d %+d -%d/+%d %s"
                 % (name, len(text.split("\n")), len(text.split("\n")) - len(land),
                    minus, plus, "yes" if text == H.ENTRY_TEXT else "no"))
open(os.path.join(SEAT, "distance.txt"), "w").write("\n".join(delta) + "\n")
print()
print("\n".join(delta))
