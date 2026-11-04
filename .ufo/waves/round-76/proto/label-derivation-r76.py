#!/usr/bin/env python3
"""Derive the round-76 C1 labels from the harness's own evidence lines.

For each frozen case, run the successor harness on the fixture and read only its
`MADO_R76_SELFTEST ... green=` and `MADO_R76_MUTANT M-Z ... killed=` evidence lines:

    expect_mz       <- the M-Z line's killed= field (the harness's own credit decision)
    expect_verdict  <- green=yes AND M-Z killed=yes AND M-R killed=yes (the harness's
                       outcome_exit sentence), never from the contract row

Then compare with the frozen control labels. Run from the lane root.
"""
import importlib.util, json, os, re, sys

LANE = os.getcwd()
spec = importlib.util.spec_from_file_location("c76", "quality/counters/c1-r76-outcome-field.py")
c76 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c76)
raw = sys.argv[1] if len(sys.argv) > 1 else ".ufo/waves/round-76/controls/c1-outcome-cases-r76.json"
sha = sys.argv[2] if len(sys.argv) > 2 else "755b339f1f6ec18f45b494d40515aecdbe9ceb73"
scratch = sys.argv[3] if len(sys.argv) > 3 else "/fast/scratch/hyaku/mado-r76/labels"
os.makedirs(os.path.join(scratch, "home"), exist_ok=True)
env = c76.git_env(os.path.join(scratch, "home"))
def show(p):
    return c76.git(LANE, ["show", "%s:%s" % (sha, p)], env).stdout
lane = {p: show(p) for p in (c76.USEDBY, c76.LEDGER, c76.CITECHECK, c76.R72)}
cand = show(c76.CAND)
hpath = os.path.join(scratch, "candidate.py"); open(hpath, "wb").write(cand)
work = os.path.join(scratch, "work"); os.makedirs(work, exist_ok=True)
cases = json.load(open(raw))["cases"]
GREEN = re.compile(r"MADO_R76_SELFTEST instrument=.* green=(yes|no)")
KILL = re.compile(r"MADO_R76_MUTANT (M-Z|M-R) .* killed=(yes|no)")
ok = True
print("case expect_mz expect_verdict derived_mz derived_verdict agree")
for case in cases:
    root = c76.make_fixture(work, case, lane, env)
    out = c76.harness_run(hpath, root, os.path.join(work, "derive", case["name"]), env).stdout.decode()
    green = "no"; kills = {}
    for line in out.splitlines():
        m = GREEN.search(line.strip())
        if m: green = m.group(1)
        m = KILL.search(line.strip())
        if m: kills[m.group(1)] = m.group(2)
    mz = "pass" if kills.get("M-Z") == "yes" else "fail"
    verdict = "pass" if (green == "yes" and kills.get("M-Z") == "yes" and kills.get("M-R") == "yes") else "fail"
    agree = (mz == case["expect_mz"] and verdict == case["expect_verdict"])
    ok = ok and agree
    print("%s %s %s %s %s %s" % (case["name"], case["expect_mz"], case["expect_verdict"], mz, verdict, "yes" if agree else "NO"))
print("DERIVATION: %s" % ("all labels re-derived" if ok else "MISMATCH"))
sys.exit(0 if ok else 1)
