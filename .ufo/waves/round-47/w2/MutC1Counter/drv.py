#!/usr/bin/env python3
"""MutC1Counter driver: score selected control/probe tools with a chosen counter variant.

Usage: drv.py --counter <counter.py> --names REF,EXIT1,... [--base <rev>] [--nonce 4747]
             [--jobs 2] [--logdir <dir>]
Names: REF | control names of run-c1-controls.py | P-* probe sources in tools/.
Prints `MUT <name> <verdict> <summary>` and writes each run's full counter output to the logdir.
"""
import argparse
import concurrent.futures
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ROOT = "/fast/scratch/hyaku/mado-r47/MutC1Counter"
BASE = "d7527d608ad2b2e3cc398fdde34db7947b254a1a"

spec = importlib.util.spec_from_file_location("ctl", LANE + "/.ufo/waves/round-47/ctl/run-c1-controls.py")
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)


def score(label, src, counter, a, logdir):
    d = tempfile.mkdtemp(dir=a.work, prefix="mut-%s-" % re.sub(r"[^A-Za-z0-9._-]", "_", label))
    D = os.path.join(d, "repo")
    run = lambda *c: subprocess.run(c, capture_output=True, check=True)
    run("git", "clone", "-q", "--shared", "--no-checkout", LANE, D)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == D, top
    run("git", "-C", D, "checkout", "-q", "--detach", a.base)
    if src is not None:
        os.makedirs(os.path.join(D, "tools"), exist_ok=True)
        with open(os.path.join(D, "tools", "mado-terminal.py"), "w") as fh:
            fh.write(src)
        run("git", "-C", D, "add", "tools/mado-terminal.py")
        run("git", "-C", D, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", label)
    wd = os.path.join(d, "w")
    os.makedirs(wd)
    try:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", D, "--rev", "HEAD", "--work", wd,
                            "--nonce", str(a.nonce)], capture_output=True, text=True, timeout=3600)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "TIMEOUT", -1
    last = [l for l in out.splitlines() if l.startswith("PRED-C1-r47:")]
    summ = last[-1] if last else "NO-SUMMARY rc=%d %s" % (rc, err[-200:])
    if logdir:
        with open(os.path.join(logdir, label + ".log"), "w") as fh:
            fh.write("counter=%s\nrc=%d\n--- stdout ---\n%s\n--- stderr ---\n%s"
                     % (counter, rc, out[-200000:], err[-20000:]))
    subprocess.run(["rm", "-rf", "--", d])
    if "verdict=TARGET_MET" in summ:
        verdict = "TARGET_MET"
    elif "verdict=TARGET_MISSED" in summ:
        verdict = "TARGET_MISSED"
    elif "SETUP" in summ:
        verdict = "SETUP"
    else:
        verdict = "ERROR"
    summ = re.sub(r" rev=\S+", "", summ.replace("PRED-C1-r47: ", ""))
    return label, verdict, summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--names", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--nonce", type=int, default=4747)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--work", default=ROOT + "/w")
    ap.add_argument("--logdir", default="")
    a = ap.parse_args()
    jobs = []
    for n in a.names.split(","):
        n = n.strip()
        if n == "REF":
            src = ctl.REF
        elif n.startswith("P-"):
            src = open(os.path.join(ROOT, "tools", n + ".py")).read()
        else:
            src = ctl.CONTROLS[n]
        jobs.append((n, src))
    logdir = a.logdir
    if logdir:
        os.makedirs(logdir, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(min(a.jobs, len(jobs))) as ex:
        futs = [ex.submit(score, label, src, a.counter, a, logdir) for label, src in jobs]
        for f in futs:
            label, verdict, summ = f.result()
            print("MUT %-22s %-13s %s" % (label, verdict, summ), flush=True)


if __name__ == "__main__":
    sys.exit(main())
