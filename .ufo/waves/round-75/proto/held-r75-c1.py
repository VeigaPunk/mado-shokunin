#!/usr/bin/env python3
"""Pre-freeze do-nothing baseline for mado round 75 C1 (NOT a scored counter).

Builds the eleven frozen fixture lanes and runs ONLY the held round-72 harness on each, through
the actual harness pipeline. Its score is the ceiling a rule that skips the witness work can
reach; the round-75 target (11/11) must be above it.
"""
import json, os, runpy, sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality/counters/c1-r75-harness-witness.py")
CONTROLS = os.path.join(LANE, ".ufo/waves/round-75/controls/c1-harness-cases-r75.json")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/mado-r75/l1/baseline-c1"

m = runpy.run_path(COUNTER)
work = SCRATCH
import shutil
shutil.rmtree(work, ignore_errors=True)
os.makedirs(os.path.join(work, "home"), exist_ok=True)
env = m["git_env"](os.path.join(work, "home"))
repo = LANE
sha = m["resolve_rev"](repo, "master", env)
cases = json.load(open(CONTROLS))["cases"]
lane = {p: m["extract"](repo, sha, p, env)
        for p in (m["USEDBY"], m["LEDGER"], m["CITECHECK"], m["R72"])}
print("PROTO held-r75-c1 rev=%s cases=%d base_harness=%s" % (sha, len(cases), m["BASE"]))
correct = 0
for case in cases:
    fixture = m["make_fixture"](work, case, lane, env)
    r = m["harness_run"](os.path.join(LANE, m["BASE"]), fixture,
                         os.path.join(work, "base", case["name"]), env)
    out = m["dec"](r.stdout) + m["dec"](r.stderr)
    decision = m["parse_decision"](out, m["BASE_RE"])
    want = "pass" if case["expect_kill"] else "fail"
    ok = decision == want
    correct += int(ok)
    print("PROTO case=%-20s expect=%-4s held=%-6s correct=%s"
          % (case["name"], want, decision or "absent", "yes" if ok else "no"))
print("PROTO do-nothing control: correct=%d/%d (target must be 11/11); its source is the frozen"
      " round-72 harness, which cannot echo the per-run challenge" % (correct, len(cases)))
print("PROTO verdict do_nothing=TARGET_MISSED" if correct < len(cases) else
      "PROTO verdict do_nothing=MEETS_TARGET (the target or counter is wrong)")
