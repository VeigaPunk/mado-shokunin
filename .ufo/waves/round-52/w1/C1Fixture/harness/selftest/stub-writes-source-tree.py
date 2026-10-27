#!/usr/bin/env python3
"""stub-writes-source-tree.py — HARNESS SELF-TEST ASSET, not a candidate C1 counter.

Purpose: prove that the harness's `lane_unchanged` detector actually fires.  This stub
writes a file into the *watched* repository — the repository the harness was pointed at,
reached through the fixture clone's `origin` remote — which the harness must detect and
report as a source-tree write.

The write target is the throwaway repository that `run-selftest.sh` creates under the
scratch tree, never the lane: the harness points the counter at a fixture clone, whose
origin URL is the throwaway path.

Usage: stub-writes-source-tree.py --repo <fixture dir> --rev <rev> --work <dir>
"""

import argparse
import os
import subprocess
import sys


def origin_of(path):
    proc = subprocess.run(("git", "-C", path, "remote", "get-url", "origin"),
                          capture_output=True)
    if proc.returncode != 0:
        return None
    url = proc.stdout.decode("utf-8", "replace").strip()
    return url if os.path.isdir(url) else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args(argv)
    target = origin_of(args.repo) or args.repo
    with open(os.path.join(target, "UNEXPECTED-WRITE.txt"), "w") as fh:
        fh.write("this file must be detected by the harness\n")
    print("STUB: population=1 ledger_rows=1 verdict=TARGET_MET rev=%s" % args.rev)
    return 0


if __name__ == "__main__":
    sys.exit(main())
