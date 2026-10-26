#!/usr/bin/env python3
"""Score all generated mutants with PRED-C1-r41-v2, 6-way parallel.

Usage: python3 score_all.py [--batch N] [--only NAME]
Each mutant logs to logs/<NAME>.log; a summary line per mutant is appended to
logs/_summary.tsv (one file per run, truncated).
"""
import argparse
import concurrent.futures
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
COUNTER = os.path.join(LANE, "quality/counters/c1-r41-globals-v2.py")
SEAT = os.path.join(LANE, ".ufo/waves/round-41/w2/ExecMutDelivered")
MUT_DIR = os.path.join(SEAT, "mutants")
LOG_DIR = os.path.join(SEAT, "logs")
NONCE = "c1w2mut0001"


def score_one(name):
    tool = os.path.join(MUT_DIR, name + ".py")
    log = os.path.join(LOG_DIR, name + ".log")
    with open(log, "w") as fh:
        p = subprocess.run(
            ["python3", "-I", COUNTER, "--repo", LANE, "--rev", REV,
             "--tool", tool, "--nonce", NONCE],
            stdout=fh, stderr=subprocess.STDOUT, timeout=1200)
    last = ""
    with open(log) as fh:
        for line in fh:
            if "PRED-C1-r41-v2:" in line:
                last = line.rstrip("\n")
    return name, p.returncode, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=6)
    ap.add_argument("--only")
    args = ap.parse_args()
    names = sorted(f[:-3] for f in os.listdir(MUT_DIR) if f.endswith(".py"))
    if args.only:
        names = [n for n in names if n == args.only]
    os.makedirs(LOG_DIR, exist_ok=True)
    summary = os.path.join(LOG_DIR, "_summary.tsv")
    with open(summary, "w") as out:
        out.write("name\trc\tverdict\n")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.batch) as ex:
            futs = {ex.submit(score_one, n): n for n in names}
            for fut in concurrent.futures.as_completed(futs):
                name, rc, last = fut.result()
                out.write("%s\t%d\t%s\n" % (name, rc, last))
                out.flush()
                print("%-40s rc=%d %s" % (name, rc, last[-160:]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
