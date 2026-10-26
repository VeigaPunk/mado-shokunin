#!/usr/bin/env python3
"""Parse the per-mutant PRED-C1-r44 logs into one table (name | rc | verdict | failing fixtures | clauses)."""
import glob
import os
import re
import sys

LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts", "logs")

rows = []
for p in sorted(glob.glob(os.path.join(LOGS, "*.log"))):
    name = os.path.basename(p)[:-4]
    text = open(p, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    last = next((l for l in reversed(lines) if l.startswith("PRED-C1-r44: fixtures=")), "")
    m = re.search(r"fixtures=(\d+)/(\d+) tool=(\w+) verdict=(\w+)", last)
    cl = next((l for l in lines if " clauses=" in l), "")
    selt = next((re.search(r"selftest=(\d+)/(\d+)", l) for l in lines
                 if "clause=b rc=" in l), None)
    b4 = next((re.search(r"clause=b4 sites=(\d+) killed=(\d+) need=(\d+)", l) for l in lines
               if "clause=b4 sites=" in l and "killed=" in l), None)
    fails = [re.search(r"fixture=(\S+) ok=0", l).group(1) for l in lines
             if re.search(r"fixture=(\S+) ok=0", l)]
    clauses = cl.split("clauses=")[-1] if "clauses=" in cl else ""
    rows.append({"name": name, "verdict": m.group(4) if m else "?", "fx": m.group(1) if m else "?",
                 "selftest": ("%s/%s" % (selt.group(1), selt.group(2))) if selt else "-",
                 "b4": ("%s/%s/%s" % (b4.group(2), b4.group(1), b4.group(3))) if b4 else "-",
                 "clauses": clauses, "fails": fails})

print("name\tverdict\tfixtures\tselftest\tb4:killed/sites/need\tfailing_fixtures")
for r in rows:
    print("%s\t%s\t%s\t%s\t%s\t%s" % (r["name"], r["verdict"], r["fx"], r["selftest"], r["b4"],
                                     ",".join(r["fails"]) or "-"))
print("TOTAL=%d MET=%d MISSED=%d" % (len(rows), sum(r["verdict"] == "TARGET_MET" for r in rows),
                                     sum(r["verdict"] == "TARGET_MISSED" for r in rows)))
