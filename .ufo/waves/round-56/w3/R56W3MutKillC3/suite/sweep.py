#!/usr/bin/env python3
"""sweep.py -- rebuild the w2 C3-harness mutant table against the LANE TIP harness and re-run the
three-oracle sweep, so the survivor set is re-verified at the revision this wave scores.

Target   : quality/r56_ctl_c3.py as of lane tip 0f3a54361a9824484d0801679ceb1fd8ac7c32e1
Mutants  : the 54 one-line mutants of .ufo/waves/round-56/w2/R56W2MutC3Harness/mutants.py (unchanged)
Oracle   : the UNCHANGED driver check-r56-controls.py --claim c3, three times per mutant:
             A) --counter <the real counter>          -> must print exactly
                "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK" and exit 0
             B) --counter stub_green.py (always green) -> must score FAIL (exit != 0)
             C) --counter stub_legs.py  (every leg)    -> must score FAIL (exit != 0)
KILLED   : any of A/B/C deviates from its expectation.  SURVIVED : all three hold.

The lane is never touched: every mutant is a COPY of the harness source in the scratch dir; the harness runs
against the reduced scratch repo `mini` whose blobs are the lane blobs at the tip and whose object store
borrows the lane's read-only (so the frozen base revision 13f0acbe stays readable).
"""
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(S, "mutants_w2.py").replace(".py", "")) if False else None
sys.path.insert(0, HERE)

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("mutants_w2", os.path.join(S, "mutants_w2.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
MUTANTS = _mod.MUTANTS

MINI = os.path.join(S, "mini")
TREE = os.path.join(S, "src")
HARNESS = "quality_r56_ctl_c3.py"          # the tip harness copy in S/src
DRIVER = "quality_check-r56-controls.py"
REAL_COUNTER = os.path.join(TREE, "quality_counters_c3-r56-used-by.py")
STUB_GREEN = os.path.join(HERE, "fixtures", "stub_green.py")
STUB_LEGS = os.path.join(HERE, "fixtures", "stub_legs.py")
WORKERS = int(os.environ.get("WORKERS", "6"))
EXPECT_A = "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK\n"


def mini_sha():
    return open(os.path.join(S, "mini_sha.txt")).read().strip()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_check(mdir, counter, work, label):
    cmd = [sys.executable, "-I", os.path.join(mdir, "check-r56-controls.py"), "--claim", "c3",
           "--repo", MINI, "--rev", mini_sha(), "--work", work, "--counter", counter]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work, timeout=900)
    out = p.stdout.decode("utf-8", "replace")
    if label == "A":
        ok = (p.returncode == 0 and out == EXPECT_A)
    else:
        ok = (p.returncode != 0 and out.startswith("MADO_R56_CONTROLS: claim=c3") and "verdict=FAIL" in out)
    return ok, "rc=%d stdout=%r" % (p.returncode, out.strip()), p.stderr.decode("utf-8", "replace")


def one_mutant(rec):
    mid, op, old, new, note = rec
    src = open(os.path.join(TREE, HARNESS), "rb").read()
    n = src.count(old.encode())
    if n != 1:
        return {"id": mid, "status": "INVALID", "detail": "old fragment occurs %d times" % n,
                "operator": op, "note": note}
    mutated = src.replace(old.encode(), new.encode(), 1)
    mdir = tempfile.mkdtemp(prefix="mut.%s." % mid, dir=os.path.join(S, "work"))
    try:
        shutil.copyfile(os.path.join(TREE, DRIVER), os.path.join(mdir, "check-r56-controls.py"))
        with open(os.path.join(mdir, "r56_ctl_c3.py"), "wb") as fh:
            fh.write(mutated)
        res = {"id": mid, "status": "?", "operator": op, "note": note, "old": old, "new": new,
               "mutant_sha256": sha(mutated), "target_sha256": sha(src)}
        checks = []
        for label, counter in (("A", REAL_COUNTER), ("B", STUB_GREEN), ("C", STUB_LEGS)):
            w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "work"))
            try:
                ok, detail, errtxt = run_check(mdir, counter, w, label)
            except subprocess.TimeoutExpired:
                ok, detail, errtxt = False, "timeout", ""
            finally:
                shutil.rmtree(w, ignore_errors=True)
            checks.append({"check": label, "ok": ok, "detail": detail})
            if not ok:
                res.setdefault("stderr", {})[label] = errtxt.strip()[-600:]
        res["checks"] = checks
        res["status"] = "KILLED" if (not checks[0]["ok"] or not checks[1]["ok"] or not checks[2]["ok"]) else "SURVIVED"
        return res
    finally:
        shutil.rmtree(mdir, ignore_errors=True)


def main():
    os.makedirs(os.path.join(S, "work"), exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for r in ex.map(one_mutant, MUTANTS):
            results.append(r)
            print("%-4s %-9s %s" % (r["id"], r["status"], r["operator"]), flush=True)
    results.sort(key=lambda r: r["id"])
    out = os.path.join(S, "sweep.json")
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1)
    k = [r for r in results if r["status"] == "KILLED"]
    v = [r for r in results if r["status"] == "SURVIVED"]
    inv = [r for r in results if r["status"] not in ("KILLED", "SURVIVED")]
    print("\nmutants=%d killed=%d survived=%d invalid=%d" % (len(results), len(k), len(v), len(inv)))
    print("survivors(%d): %s" % (len(v), ",".join(r["id"] for r in v)))
    print("-> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
