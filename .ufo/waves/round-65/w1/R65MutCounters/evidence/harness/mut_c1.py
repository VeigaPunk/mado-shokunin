#!/usr/bin/env python3
"""C1 mutation battery: apply one change to a copy, run the fixture matrix.

Baseline expectations are measured from the pristine copy at run time; a mutant is
KILLED when any (fixture, verdict, rc) tuple moves away from that baseline.
"""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r65/w1/R65MutCounters"
SRC = S + "/targets/c1-r65-register.py"
OUT = S + "/c1-mut"
FIXTURES = ["pos", "pos-extra", "neg-dupgroup", "neg-droprow", "neg-gate-dirty",
            "neg-dangling", "neg-nearmiss", "neg-base", "neg-8r7g-gateok",
            "neg-sentinel-leak", "neg-wt-only"]

MUTANTS = [
    ("M1 rows>=9 (off-by-one up)", "len(rows) >= 8 and", "len(rows) >= 9 and"),
    ("M2 rows>=7 (off-by-one down)", "len(rows) >= 8 and", "len(rows) >= 7 and"),
    ("M3 groups>=7 (weaken required set)", "len(groups) == len(GROUPS)", "len(groups) >= 7"),
    ("M4 gate token weakened", 'GATE_TOKEN = "MADO_VERIFY: CLEAN"',
     'GATE_TOKEN = "MADO_VERIFY"'),
    ("M5 receipt resolution dropped",
     'and len(resolved) == len(receipts) and gate == "ok")',
     'and gate == "ok")'),
    ("M6 group first-cell substring",
     "groups = [name for name in GROUPS if name in first_cells]",
     "groups = [name for name in GROUPS if any(name in cell for cell in first_cells)]"),
    ("M7 worktree instead of rev",
     'province = git(repo, "show", "%s:%s" % (args.rev, PROVINCE_REL))',
     'province = open(os.path.join(repo, PROVINCE_REL), "rb").read()'),
    ("M8 always exit 0", "return 0 if met else 1", "return 0"),
    ("M10 required group dropped from GROUPS",
     '    "omarchy skill docs",\n    "windows desktop plane",\n)',
     '    "omarchy skill docs",\n)'),
    ("M9 sentinel ignored",
     'if cand.startswith("## ") or cand.strip() == SENTINEL:',
     'if cand.startswith("## "):'),
]


def run(script, name):
    repo = os.path.join(S, "fx", name)
    rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    p = subprocess.run([sys.executable, script, "--repo", repo, "--rev", rev],
                       capture_output=True, text=True, timeout=120)
    line = [l for l in p.stdout.splitlines() if l.startswith("MADO_R65_REGISTER:")]
    line = line[0] if line else "<no-verdict-line>"
    verdict = "MET" if "verdict=TARGET_MET" in line else (
        "MISSED" if "verdict=TARGET_MISSED" in line else "NONE")
    return p.returncode, verdict, line


def main():
    os.makedirs(OUT, exist_ok=True)
    src = open(SRC).read()
    base = {n: run(SRC, n) for n in FIXTURES}
    print("== BASELINE")
    for n in FIXTURES:
        print("  %-20s rc=%d %s" % (n, base[n][0], base[n][1]))
    rows = []
    for label, old, new in MUTANTS:
        mid = label.split()[0]
        cnt = src.count(old)
        if cnt != 1:
            print("!! %s: pattern occurs %d times, skipped" % (mid, cnt))
            rows.append((label, "N/A", "pattern count %d" % cnt, "n/a"))
            continue
        d = os.path.join(OUT, mid)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        path = os.path.join(d, "c1-r65-register.py")
        open(path, "w").write(src.replace(old, new))
        dev = []
        obs = []
        for n in FIXTURES:
            rc, verdict, line = run(path, n)
            was = base[n]
            same = (rc == was[0] and verdict == was[1])
            obs.append((n, rc, verdict, same))
            if not same:
                dev.append("%s: %s/rc%d -> %s/rc%d" % (n, was[1], was[0], verdict, rc))
        verdict = "KILLED" if dev else "SURVIVED"
        print("== %-38s %s" % (label, verdict))
        for dline in dev:
            print("     deviation: " + dline)
        rows.append((label, verdict, "; ".join(dev) or "no deviation", "%d fixtures" % len(FIXTURES)))
    with open(S + "/c1-mutants.json", "w") as f:
        json.dump({"baseline": {k: base[k] for k in FIXTURES}, "rows": rows}, f, indent=1)
    print("wrote", S + "/c1-mutants.json")


if __name__ == "__main__":
    main()
