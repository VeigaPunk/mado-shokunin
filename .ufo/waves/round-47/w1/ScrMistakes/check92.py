#!/usr/bin/env python3
"""check92 — a seat directory's produced set and its committed set are compared, both named
(proposed criterion 92).

Walks DIR in the worktree, lists the paths committed at REV under DIR, and prints every worktree
regular file absent at REV with its size. Exit 0 = sets equal; 1 = DIFFER; 2 = setup error.
"""
import argparse
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    d = os.path.join(a.repo, a.dir)
    r = subprocess.run(["git", "-C", a.repo, "ls-tree", "-r", "--name-only", a.rev, "--", a.dir],
                       capture_output=True)
    if r.returncode != 0:
        print("CHECK92: verdict=SETUP_ERROR git ls-tree failed")
        return 2
    tracked = {p for p in r.stdout.decode().splitlines() if p}
    work = {}
    if os.path.isdir(d):
        for root, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x != ".git"]
            for f in files:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, a.repo)
                if os.path.islink(p) or not os.path.isfile(p):
                    continue
                work[rel] = os.path.getsize(p)
    missing = sorted(set(work) - tracked)
    for p in missing:
        print("UNCOMMITTED %d %s" % (work[p], p))
    for p in sorted(tracked - set(work)):
        print("ONLY_AT_REV %s" % p)
    ok = not missing and not (tracked - set(work))
    print("CHECK92: rev=%s dir=%s worktree=%d tracked=%d uncommitted=%d uncommitted_bytes=%d verdict=%s"
          % (a.rev[:12], a.dir, len(work), len(tracked), len(missing),
             sum(work[p] for p in missing), "OK" if ok else "DIFFER"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
