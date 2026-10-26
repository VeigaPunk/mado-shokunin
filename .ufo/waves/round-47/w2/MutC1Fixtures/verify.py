#!/usr/bin/env python3
"""Seat MutC1Fixtures verification harness.

For a proposed fixture JSON (counter schema: id/class/env/files/exec/args) and a mutant id,
runs the pinned real resolver (oracle) and BOTH the mutated tool and the pristine reference in
the counter's own sandbox, on fresh materialized trees, and reports:
  oracle = (rc, normalized stdout)
  ref_ok  (reference agrees with oracle)
  mut_ok  (mutant agrees with oracle)
A sound kill-fixture has ref_ok=True and mut_ok=False.

Usage: python3 -I verify.py <case.json> <mutant-id> [--probe PATH=...] [--env-case JSON]
"""
import argparse
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r47/MutC1Fixtures"
REFPATH = os.path.join(LANE, ".ufo", "waves", "round-47", "l1-draft", "mado-terminal.py")
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")
REC = os.path.join(HERE, "receipts")
os.makedirs(REC, exist_ok=True)

sys.path.insert(0, HERE)
from mutants import MUTANTS

spec = importlib.util.spec_from_file_location("c1r47", COUNTER)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

REF = open(REFPATH).read()


def mutated(mid):
    for name, old, new in MUTANTS:
        if name == mid:
            assert REF.count(old) == 1
            return REF.replace(old, new, 1)
    raise SystemExit("unknown mutant " + mid)


def build_tool(src, tag):
    d = tempfile.mkdtemp(dir=SCRATCH, prefix="tool-")
    p = os.path.join(d, tag + ".py")
    open(p, "w").write(src)
    return p


def verdict(box, case, rng):
    ok, o_norm, why = C.run_case(box, case, "A", rng)
    return ok, o_norm, why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("mutant")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    case = json.load(open(a.case))
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="vf-")
    rng = random.Random(47)
    try:
        mp = build_tool(mutated(a.mutant), a.mutant)
        rp = build_tool(REF, "ref")
        box_m = C.Box(work, tool_path=mp)
        m_ok, m_oracle, m_why = verdict(box_m, case, rng)
        box_r = C.Box(work, tool_path=rp)
        r_ok, r_oracle, r_why = verdict(box_r, case, rng)
        print("VERIFY %s\n  oracle rc=%d stdout=%r\n  ref_ok=%s\n  mut_ok=%s\n  mut_why=%s"
              % (a.label or a.mutant, m_oracle[0], m_oracle[1][:200], r_ok, m_ok, m_why[:200]))
        with open(os.path.join(REC, "verify-%s.txt" % (a.label or a.mutant)), "w") as fh:
            fh.write("case=%s\noracle=(%d, %r)\nref_ok=%s\nmut_ok=%s\nmut_why=%s\n"
                     % (a.case, m_oracle[0], m_oracle[1][:400], r_ok, m_ok, m_why[:400]))
        if r_ok and not m_ok:
            print("VERIFY-VERDICT: KILLS")
        elif r_ok and m_ok:
            print("VERIFY-VERDICT: SURVIVES (mutant == oracle on this case)")
        else:
            print("VERIFY-VERDICT: INCONCLUSIVE (ref mismatch; oracle drift or bad case)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
