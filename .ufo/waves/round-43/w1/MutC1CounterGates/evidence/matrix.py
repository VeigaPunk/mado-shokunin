#!/usr/bin/env python3
"""Build matrix.md + classification from results.jsonl / results2.jsonl."""
import json, os, collections

SCRATCH = "/fast/scratch/hyaku/mado-r43/MutC1CounterGates"
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/MutC1CounterGates"
PANEL = ["M01-fifo-block", "M04-toolarge-ge", "M27-nomatch-rc", "K1-zero-test-selftest",
         "K3-exec-model", "K4-child-interpreter", "K5-getattr", "D1-constant"]

rows = []
for f in ("results.jsonl", "results2.jsonl"):
    p = os.path.join(SCRATCH, f)
    if os.path.exists(p):
        rows += [json.loads(l) for l in open(p) if l.strip()]

pris = [r for r in rows if r["counter"] == "counter-orig.py"]
mut = [r for r in rows if r["counter"] not in ("counter-orig.py",)]
by = collections.defaultdict(dict)
for r in mut:
    by[r["counter"]][r["target"]] = r
pb = {}
for r in pris:
    pb[r["target"]] = r

def state(r):
    if r is None:
        return "no-run"
    if not r["final"].startswith("PRED"):
        return "CRASH(rc=%s)" % r["rc"]
    return "MET" if r["met"] else "MISSED"

print("== pristine anchors ==")
for t in ["REF", "BASE-absent"] + PANEL:
    r = pb.get(t)
    print("%-14s %-10s rc=%s clauses=%s failed=%s" % (t, state(r), r["rc"], r["clauses"], ",".join(r["failed"]) or "-"))

print("\n== mutant matrix ==")
lines = []
flips = collections.defaultdict(list)
for name in sorted(by):
    d = by[name]
    ref = d.get("REF")
    ctl = {c: d.get(c) for c in PANEL}
    refst = state(ref)
    flipped = [c for c in PANEL if ctl[c] and state(ctl[c]) == "MET" and state(pb.get(c)) != "MET"]
    worst = "MET" if flipped else ("MISSED" if all(ctl[c] and state(ctl[c]) != "MET" for c in PANEL) else "?")
    if flipped:
        cls = "GATE-BROKEN missed-defect: " + ",".join(flipped)
        for c in flipped:
            flips[c].append(name)
    elif refst not in ("MET",):
        cls = "OVER-STRICT (reference %s)" % refst
    else:
        cls = "SURVIVOR"
    row = "%-22s ref=%-12s worst=%-7s %s" % (name, refst, worst, cls)
    lines.append(row)
    print(row)
    for c in PANEL:
        if ctl[c] and state(ctl[c]) == "MET" and state(pb.get(c)) != "MET":
            print("    flip detail %s: rc=%s clauses=%s failed=%s" % (c, ctl[c]["rc"], ctl[c]["clauses"], ",".join(ctl[c]["failed"]) or "-"))

print("\n== control -> flipping mutants ==")
for c in PANEL:
    print("%-24s <- %s" % (c, ",".join(flips[c]) or "(none)"))
os.makedirs(SEAT, exist_ok=True)
open(os.path.join(SCRATCH, "matrix-raw.txt"), "w").write("\n".join(lines) + "\n")
