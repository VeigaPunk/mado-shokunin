#!/usr/bin/env python3
"""run_mutants.py -- mutation driver for seat R56W2MutC3Harness.

Target   : quality/r56_ctl_c3.py (round-56 C3 control harness) as of lane commit 28fc86ac...
Oracle   : the UNCHANGED harness driver quality/check-r56-controls.py --claim c3, run three times per mutant:
             A) --counter <the real counter quality/counters/c3-r56-used-by.py>  -> must print exactly
                "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK" and exit 0
             B) --counter <stub_green.py>   (always prints TARGET_MET, exit 0)  -> must score FAIL (exit != 0)
             C) --counter <stub_legs.py>    (prints every leg missed, exit 1)    -> must score FAIL (exit != 0)
A mutant is KILLED when one of A/B/C deviates from the expectation above; SURVIVED when all three hold.
The lane is never touched: the harness runs against a reduced scratch repo (same blobs as the lane commit) whose
object store borrows the lane's, and every mutation is applied to a COPY of the harness source.
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
sys.path.insert(0, HERE)
from mutants import MUTANTS, TARGET  # noqa: E402

S = os.environ.get("SCRATCH", "/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness")
TREE = os.path.join(S, "tree")            # git archive of the lane at 28fc86ac
MINI = os.path.join(S, "mini")            # reduced scratch repo (same content blobs)
DRIVER = os.path.join(TREE, "quality", "check-r56-controls.py")
REAL_COUNTER = os.path.join(TREE, "quality", "counters", "c3-r56-used-by.py")
STUB_GREEN = os.path.join(S, "stubs", "stub_green.py")
STUB_LEGS = os.path.join(S, "stubs", "stub_legs.py")
WORKERS = int(os.environ.get("WORKERS", "4"))

EXPECT_A = "MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK\n"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def mini_sha():
    if os.environ.get("REV"):
        return os.environ["REV"]
    with open(os.path.join(S, "mini_sha.txt")) as fh:
        return fh.read().strip()


def repo():
    return os.environ.get("REPO", MINI)


def run_check(mdir, counter, work, label):
    """-> (ok, detail) for one oracle check."""
    cmd = [sys.executable, "-I", os.path.join(mdir, "check-r56-controls.py"), "--claim", "c3",
           "--repo", repo(), "--rev", mini_sha(), "--work", work, "--counter", counter]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work, timeout=900)
    out = p.stdout.decode("utf-8", "replace")
    if label == "A":
        ok = (p.returncode == 0 and out == EXPECT_A)
        detail = "rc=%d stdout=%r" % (p.returncode, out.strip())
    else:
        ok = (p.returncode != 0 and out.startswith("MADO_R56_CONTROLS: claim=c3") and "verdict=FAIL" in out)
        detail = "rc=%d stdout=%r" % (p.returncode, out.strip())
    return ok, detail, p.stderr.decode("utf-8", "replace")


def one_mutant(rec):
    mid, op, old, new, note = rec
    src = open(os.path.join(TREE, TARGET), "rb").read()
    n = src.count(old.encode())
    if n != 1:
        return {"id": mid, "status": "INVALID", "detail": "old fragment occurs %d times" % n,
                "operator": op, "note": note}
    mutated = src.replace(old.encode(), new.encode(), 1)
    mdir = tempfile.mkdtemp(prefix="mut.%s." % mid, dir=os.path.join(S, "mut"))
    try:
        shutil.copyfile(DRIVER, os.path.join(mdir, "check-r56-controls.py"))
        with open(os.path.join(mdir, "r56_ctl_c3.py"), "wb") as fh:
            fh.write(mutated)
        res = {"id": mid, "status": "?", "operator": op, "note": note, "old": old, "new": new,
               "mutant_sha256": sha(mutated), "target_sha256": sha(src)}
        checks = []
        for label, counter in (("A", REAL_COUNTER), ("B", STUB_GREEN), ("C", STUB_LEGS)):
            w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
            try:
                ok, detail, errtxt = run_check(mdir, counter, w, label)
            except subprocess.TimeoutExpired:
                ok, detail, errtxt = False, "timeout", ""
            finally:
                shutil.rmtree(w, ignore_errors=True)
            checks.append({"check": label, "ok": ok, "detail": detail})
            if not ok:
                res.setdefault("stderr", {})[label] = errtxt.strip()[-800:]
        res["checks"] = checks
        res["status"] = "KILLED" if (not checks[0]["ok"] or not checks[1]["ok"] or not checks[2]["ok"]) else "SURVIVED"
        return res
    finally:
        shutil.rmtree(mdir, ignore_errors=True)


def main():
    os.makedirs(os.path.join(S, "mut"), exist_ok=True)
    only = [x for x in os.environ.get("ONLY", "").split(",") if x]
    todo = [m for m in MUTANTS if not only or m[0] in only]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for r in ex.map(one_mutant, todo):
            results.append(r)
            print("%-4s %-9s %s" % (r["id"], r["status"], r["operator"]), flush=True)
    results.sort(key=lambda r: r["id"])
    out = os.path.join(S, os.environ.get("RESULTS", "results.json"))
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1)
    killed = [r for r in results if r["status"] == "KILLED"]
    survived = [r for r in results if r["status"] == "SURVIVED"]
    invalid = [r for r in results if r["status"] == "INVALID"]
    print("\nmutants=%d killed=%d survived=%d invalid=%d" % (len(results), len(killed), len(survived), len(invalid)))
    print("kill rate = %d/%d = %.1f%%" % (len(killed), len(results), 100.0 * len(killed) / max(1, len(results))))
    print("results -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
