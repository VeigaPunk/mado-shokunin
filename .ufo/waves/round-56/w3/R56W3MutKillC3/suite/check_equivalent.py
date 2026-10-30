#!/usr/bin/env python3
"""check_equivalent.py -- re-verify at the lane tip that the survivors wave 2 classified as EQUIVALENT really are
behaviour-preserving: the mutant harness must print byte-identical stdout AND stderr against the real counter.

Input : the 54-mutant table (mutants_w2.py) and the tip harness quality/r56_ctl_c3.py.
Output: equivalent.json -- one row per survivor: stdout_identical, stderr_identical, the diff (if any).
"""
import difflib
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location("mutants_w2", os.path.join(S, "mutants_w2.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
MUTANTS = {m[0]: m for m in _mod.MUTANTS}

MINI = os.path.join(S, "mini")
TREE = os.path.join(S, "src")
HARNESS = os.path.join(TREE, "quality_r56_ctl_c3.py")
DRIVER = os.path.join(TREE, "quality_check-r56-controls.py")
COUNTER = os.path.join(TREE, "quality_counters_c3-r56-used-by.py")
# the eleven survivors wave 2 argued are behaviour-preserving
EQUIV = ["M10", "M12", "M23", "M31", "M33", "M35", "M41", "M43", "M47", "M49", "M50"]


def mini_sha():
    return open(os.path.join(S, "mini_sha.txt")).read().strip()


def run_harness(module_path):
    d = tempfile.mkdtemp(prefix="eq.", dir=os.path.join(S, "work"))
    try:
        shutil.copyfile(DRIVER, os.path.join(d, "check-r56-controls.py"))
        shutil.copyfile(module_path, os.path.join(d, "r56_ctl_c3.py"))
        w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "work"))
        try:
            cmd = [sys.executable, "-I", os.path.join(d, "check-r56-controls.py"), "--claim", "c3",
                   "--repo", MINI, "--rev", mini_sha(), "--work", w, "--counter", COUNTER]
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w, timeout=900)
            return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
        finally:
            shutil.rmtree(w, ignore_errors=True)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    os.makedirs(os.path.join(S, "work"), exist_ok=True)
    rows = []
    rc0, out0, err0 = run_harness(HARNESS)
    print("reference: rc=%d stdout=%r" % (rc0, out0.strip()))
    for mid in EQUIV:
        rec = MUTANTS[mid]
        src = open(HARNESS, "rb").read()
        assert src.count(rec[2].encode()) == 1, mid
        mut = src.replace(rec[2].encode(), rec[3].encode(), 1)
        d = tempfile.mkdtemp(prefix="eqm.", dir=os.path.join(S, "work"))
        try:
            p = os.path.join(d, "r56_ctl_c3.py")
            with open(p, "wb") as fh:
                fh.write(mut)
            rc, out, err = run_harness(p)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        same_out = (out == out0)
        same_err = (err == err0)
        diff = []
        if not same_err:
            diff = [l for l in difflib.unified_diff(err0.split("\n"), err.split("\n"), "reference", mid, n=0)
                    if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))][:8]
        rows.append({"id": mid, "operator": rec[1], "note": rec[4], "rc": rc,
                     "stdout_identical": same_out, "stderr_identical": same_err, "stderr_diff": diff,
                     "mutant_sha256": hashlib.sha256(mut).hexdigest()})
        print("%-5s stdout_same=%-5s stderr_same=%-5s rc=%d %s" % (mid, same_out, same_err, rc, diff[:2]))
    out = os.path.join(S, "equivalent.json")
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    bad = [r["id"] for r in rows if not (r["stdout_identical"] and r["stderr_identical"])]
    print("\nequivalent-bytes-check: %d/%d identical; divergent: %s" % (len(rows) - len(bad), len(rows), bad or "none"))
    print("-> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
