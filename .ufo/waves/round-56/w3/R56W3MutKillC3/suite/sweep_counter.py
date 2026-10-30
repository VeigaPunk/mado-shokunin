#!/usr/bin/env python3
"""sweep_counter.py -- mutation sweep of quality/counters/c3-r56-used-by.py at the lane tip.

Target : the C3 counter at lane tip 0f3a54361a9824484d0801679ceb1fd8ac7c32e1.
Mutants: suite/counter_mutants.py (30 one-line mutants; each `old` fragment occurs exactly once).
Oracle : the UNCHANGED harness quality/r56_ctl_c3.py, run as
         `check-r56-controls.py --claim c3 --repo mini --rev <tip> --work W --counter <mutant counter>`.
         The harness scores `good` (the counter must print TARGET_MET with all-zero counts on the good tree)
         and nine controls (the counter must exit 1 and name the control's leg in `missed` on the mutated
         trees).  A counter mutant is KILLED when the harness does NOT print
         "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK"; it SURVIVES when the harness still
         prints exactly that line -- i.e. the shipped oracle cannot tell the mutant from the real counter.

The lane is never touched: every mutant is a COPY of the counter source in the scratch dir.
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
sys.path.insert(0, HERE)

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("counter_mutants", os.path.join(HERE, "counter_mutants.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
MUTANTS = _mod.MUTANTS

MINI = os.path.join(S, "mini")
TREE = os.path.join(S, "src")
DRIVER = os.path.join(TREE, "quality_check-r56-controls.py")
COUNTER_SRC = os.path.join(TREE, "quality_counters_c3-r56-used-by.py")
WORKERS = int(os.environ.get("WORKERS", "6"))
EXPECT = "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK\n"


def mini_sha():
    return open(os.path.join(S, "mini_sha.txt")).read().strip()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_harness(counter_path):
    d = tempfile.mkdtemp(prefix="csweep.", dir=os.path.join(S, "work"))
    try:
        shutil.copyfile(DRIVER, os.path.join(d, "check-r56-controls.py"))
        shutil.copyfile(os.path.join(TREE, "quality_r56_ctl_c3.py"), os.path.join(d, "r56_ctl_c3.py"))
        w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "work"))
        try:
            cmd = [sys.executable, "-I", os.path.join(d, "check-r56-controls.py"), "--claim", "c3",
                   "--repo", MINI, "--rev", mini_sha(), "--work", w, "--counter", counter_path]
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w, timeout=900)
            return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
        finally:
            shutil.rmtree(w, ignore_errors=True)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def one(rec):
    mid, op, old, new, note = rec
    src = open(COUNTER_SRC, "rb").read()
    n = src.count(old.encode())
    if n != 1:
        return {"id": mid, "status": "INVALID", "detail": "old fragment occurs %d times" % n,
                "operator": op, "note": note}
    mutated = src.replace(old.encode(), new.encode(), 1)
    d = tempfile.mkdtemp(prefix="cmut.%s." % mid, dir=os.path.join(S, "work"))
    try:
        cpath = os.path.join(d, "c3-r56-used-by.py")
        with open(cpath, "wb") as fh:
            fh.write(mutated)
        rc, out, err = run_harness(cpath)
        same = (rc == 0 and out == EXPECT)
        res = {"id": mid, "status": "SURVIVED" if same else "KILLED", "operator": op, "note": note,
               "old": old, "new": new, "mutant_sha256": sha(mutated), "target_sha256": sha(src),
               "harness_rc": rc, "harness_stdout": out.strip()}
        if not same:
            res["harness_stderr_tail"] = err.strip()[-900:]
        return res
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    os.makedirs(os.path.join(S, "work"), exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for r in ex.map(one, MUTANTS):
            results.append(r)
            print("%-5s %-9s %s" % (r["id"], r["status"], r["operator"]), flush=True)
    results.sort(key=lambda r: r["id"])
    out = os.path.join(S, "sweep_counter.json")
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
