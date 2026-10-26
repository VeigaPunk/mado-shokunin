#!/usr/bin/env python3
"""Run the frozen C1 counter on each selftest-survivor; summarize kills."""
import json
import os
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
OUT = "/fast/scratch/hyaku/mado-r43/MutRefSelftest/mut"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r43/MutRefSelftest"
COUNTER = LANE + "/quality/counters/c1-r42-geometry.py"
REV = "b2e2efd6e268920d31f3c32cf52dc097dd6e1d22"

results = json.load(open(os.path.join(OUT, "results.json")))
survivors = sorted(m for m in results if results[m]["selftest_pass"])
summary = {}
for mid in survivors:
    mpath = os.path.join(OUT, "mut_%s.py" % mid)
    log = os.path.join(OUT, "counter_%s.txt" % mid)
    env = dict(os.environ, C1R42_TMP=SCRATCH)
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", LANE, "--rev", REV,
                        "--tool", mpath], capture_output=True, env=env, timeout=280,
                       cwd=LANE)
    text = (p.stdout + p.stderr).decode("utf-8", "replace")
    open(log, "w").write(text)
    fails = [l.split("fixture=")[1].split(" ")[0] for l in text.splitlines()
             if "fixture=" in l and " ok=0 " in l]
    final = [l for l in text.splitlines() if l.startswith("PRED-C1-r42: fixtures=")]
    clauses = [l for l in text.splitlines() if " clauses=" in l]
    setup = [l for l in text.splitlines() if "SETUP" in l and "clause" not in l]
    summary[mid] = {"rc": p.returncode, "final": final[-1] if final else "",
                    "clauses": clauses[-1] if clauses else "", "fixture_fails": fails,
                    "setup": setup[0] if setup else ""}
    print("%-4s rc=%d %s | fails=%s" % (mid, p.returncode,
          summary[mid]["final"].split("verdict=")[-1].split(" rev=")[0], ",".join(fails) or "-"))
    print("     %s" % summary[mid]["clauses"])
json.dump(summary, open(os.path.join(OUT, "counter-summary.json"), "w"), indent=1)
