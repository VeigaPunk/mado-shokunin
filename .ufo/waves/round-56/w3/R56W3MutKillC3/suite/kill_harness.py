#!/usr/bin/env python3
"""kill_harness.py -- apply each materialized kill fixture to the PRISTINE harness (must pass) and to the
MUTANT harness (must fail -> the mutant is killed).

Input : the 54-mutant table of .ufo/waves/round-56/w2/R56W2MutC3Harness/mutants.py, rebuilt against the lane
        tip harness quality/r56_ctl_c3.py at 0f3a54361a9824484d0801679ceb1fd8ac7c32e1, and the survivor set
        re-measured by sweep.py.
Output: kill_harness.json  -- one row per survivor: fixture, reference result, mutant result, verdict.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import harness_killers as HK  # noqa: E402

_spec = importlib.util.spec_from_file_location("mutants_w2", os.path.join(S, "mutants_w2.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
MUTANTS = _mod.MUTANTS

SWEEP = json.load(open(os.path.join(S, "sweep.json")))
SURVIVORS = [r["id"] for r in SWEEP if r["status"] == "SURVIVED"]
HARNESS_SRC = os.path.join(S, "src", "quality_r56_ctl_c3.py")


def mutant_source(mid):
    for rec in MUTANTS:
        if rec[0] == mid:
            src = open(HARNESS_SRC, "rb").read()
            assert src.count(rec[2].encode()) == 1, mid
            return src.replace(rec[2].encode(), rec[3].encode(), 1)
    raise KeyError(mid)


def apply_killer(mid, module_path, source_path):
    fn, arity = HK.KILLERS[mid]
    if arity == 1:
        mod = HK.load_module(module_path, "k_" + mid)
        return fn(mod)
    return fn(mod=None, path=source_path)


def main():
    os.makedirs(os.path.join(S, "work"), exist_ok=True)
    rows = []
    for mid in SURVIVORS:
        if mid not in HK.KILLERS:
            rows.append({"id": mid, "verdict": "NO_KILLER_PROPOSED",
                         "note": "wave-2 classified this survivor as behaviour-preserving (EQUIVALENT)"})
            print("%-5s NO_KILLER_PROPOSED" % mid, flush=True)
            continue
        d = tempfile.mkdtemp(prefix="kill.%s." % mid, dir=os.path.join(S, "work"))
        try:
            src = mutant_source(mid)
            mpath = os.path.join(d, "r56_ctl_c3.py")
            with open(mpath, "wb") as fh:
                fh.write(src)
            ref_ok, ref_detail = apply_killer(mid, HARNESS_SRC, HARNESS_SRC)
            mut_ok, mut_detail = apply_killer(mid, mpath, mpath)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        verdict = "KILLED" if (ref_ok and not mut_ok) else "NOT_KILLED"
        rows.append({"id": mid, "fixture": HK.KILLERS[mid][0].__name__, "fixture_argc": HK.KILLERS[mid][1],
                     "reference_passes": bool(ref_ok), "mutant_passes": bool(mut_ok),
                     "reference_detail": ref_detail, "mutant_detail": mut_detail, "verdict": verdict,
                     "mutant_sha256": hashlib.sha256(mutant_source(mid)).hexdigest()})
        print("%-5s %-12s ref=%-5s mutant=%-5s  %s" % (mid, verdict, bool(ref_ok), bool(mut_ok),
                                                       str(mut_detail)[:90]), flush=True)
    out = os.path.join(S, "kill_harness.json")
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    killed = [r for r in rows if r.get("verdict") == "KILLED"]
    nk = [r for r in rows if r.get("verdict") == "NOT_KILLED"]
    no = [r for r in rows if r.get("verdict") == "NO_KILLER_PROPOSED"]
    print("\nsurvivors=%d killed_by_fixture=%d not_killed=%d no_killer=%d" % (len(rows), len(killed), len(nk), len(no)))
    print("-> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
