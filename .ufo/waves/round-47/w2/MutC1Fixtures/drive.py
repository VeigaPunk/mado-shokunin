#!/usr/bin/env python3
"""Seat MutC1Fixtures driver: score the reference and each one-rule mutant with the frozen
C1 counter at a fixed nonce, in a --shared scratch clone of the freeze.

Usage: python3 -I drive.py [--nonce 47] [--only SUBSTR] [--jobs 2]
Results are keyed by name@nonce. Writes receipts/mut-<id>@<nonce>.txt and results.json.
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import shutil
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FREEZE = "d7527d608ad2b2e3cc398fdde34db7947b254a1a"
SCRATCH = "/fast/scratch/hyaku/mado-r47/MutC1Fixtures"
CLONE = os.path.join(SCRATCH, "clone")
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")
REFPATH = os.path.join(LANE, ".ufo", "waves", "round-47", "l1-draft", "mado-terminal.py")

sys.path.insert(0, HERE)
from mutants import MUTANTS

REF = open(REFPATH).read()
REC = os.path.join(HERE, "receipts")
os.makedirs(REC, exist_ok=True)
GITLOCK = threading.Lock()


def ensure_clone():
    if not os.path.isdir(os.path.join(CLONE, ".git")):
        shutil.rmtree(CLONE, ignore_errors=True)
        subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, CLONE], check=True)
    top = subprocess.run(["git", "-C", CLONE, "rev-parse", "--show-toplevel"],
                         capture_output=True).stdout.decode().strip()
    assert top == CLONE, "clone toplevel %r != %r" % (top, CLONE)
    lock = os.path.join(CLONE, ".git", "index.lock")
    if os.path.exists(lock):
        os.unlink(lock)
    subprocess.run(["git", "-C", CLONE, "checkout", "-q", "--detach", FREEZE], check=True)


def build(name, old, new):
    assert REF.count(old) == 1, "%s: old matches %d times" % (name, REF.count(old))
    return REF.replace(old, new, 1)


def score(name, src, nonce):
    with GITLOCK:
        ensure_clone()
        os.makedirs(os.path.join(CLONE, "tools"), exist_ok=True)
        with open(os.path.join(CLONE, "tools", "mado-terminal.py"), "w") as fh:
            fh.write(src)
        subprocess.run(["git", "-C", CLONE, "add", "tools/mado-terminal.py"], check=True)
        subprocess.run(["git", "-C", CLONE, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
                        "commit", "-q", "-m", "cand %s" % name], check=True)
    w = tempfile.mkdtemp(dir=SCRATCH, prefix="w-")
    env = dict(os.environ)
    env["TMPDIR"] = w
    try:
        p = subprocess.run(["python3", "-I", COUNTER, "--repo", CLONE, "--rev", "HEAD",
                            "--work", w, "--nonce", str(nonce)], capture_output=True, text=True,
                           timeout=1200, env=env)
        out = p.stdout
        rc = p.returncode
    except subprocess.TimeoutExpired:
        out, rc = "TIMEOUT", 124
    finally:
        shutil.rmtree(w, ignore_errors=True)
    lines = out.splitlines()
    tail = lines[-8:] if len(lines) >= 8 else lines
    fails = [l for l in lines if "FAIL" in l][:3]
    with open(os.path.join(REC, "mut-%s@%d.txt" % (name, nonce)), "w") as fh:
        fh.write("\n".join(tail + fails) + "\nrc=%d\n" % rc)
    final = [l for l in lines if l.startswith("PRED-C1-r47: ")]
    summ = final[-1] if final else (lines[-1] if lines else "<no output>")
    return name, rc, summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nonce", type=int, default=47)
    ap.add_argument("--only", default=None)
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    results_path = os.path.join(HERE, "results.json")
    results = json.load(open(results_path)) if os.path.exists(results_path) else {}
    jobs = [("REF-baseline", None)]
    for (name, old, new) in MUTANTS:
        if a.only and a.only not in name:
            continue
        jobs.append((name, build(name, old, new)))
    jobs = [j for j in jobs if "%s@%d" % (j[0], a.nonce) not in results]

    def run(job):
        name, src = job
        return score(name, src if src is not None else REF, a.nonce)

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for f in concurrent.futures.as_completed(futs):
            name, rc, summ = f.result()
            results["%s@%d" % (name, a.nonce)] = {"rc": rc, "final": summ}
            with open(results_path, "w") as fh:
                json.dump(results, fh, indent=1, sort_keys=True)
            print("MUT %s@%d rc=%d %s" % (name, a.nonce, rc, summ.split("verdict=")[-1].split(" rev=")[0]),
                  flush=True)
    print("DRIVE done %d results" % len(results))


if __name__ == "__main__":
    sys.exit(main())
