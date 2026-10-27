#!/usr/bin/env python3
"""Score every ExecControlsC1 control with ExecCounterC1's own draft (c1-r49-keysym.py), at a throwaway commit each.

The draft reads the tool as a git blob at REV (`git show REV:tools/mado-keysym.py`), so a control cannot be scored
from a loose file. This driver builds a scratch clone of the lane, commits one control per revision as
tools/mado-keysym.py, and runs the draft counter against that revision. Nothing outside the scratch clone is written;
the clone is only ever touched with `git -C "$D" ...`, and its toplevel is asserted before the first commit.

Usage: score-with-draft.py --counter <c1-r49-keysym.py> --controls DIR --clone D --work W [--nonce N] [--only NAME]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
GIT = ["git", "-c", "user.name=mado control fixture", "-c", "user.email=ctl@fixture.invalid",
       "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]


def sh(argv, cwd=None, check=True):
    p = subprocess.run(argv, cwd=cwd, capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit("failed: %s\n%s\n%s" % (" ".join(argv), p.stdout.decode()[-800:], p.stderr.decode()[-800:]))
    return p


def git(d, *args, check=True):
    return sh(GIT + ["-C", d] + list(args), check=check)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--controls", required=True)
    ap.add_argument("--clone", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=49)
    ap.add_argument("--only")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    for p in (a.clone, a.work):
        if os.path.abspath(p).startswith("/tmp"):
            raise SystemExit("refusing a /tmp path: %s" % p)
    if os.path.exists(a.clone):
        shutil.rmtree(a.clone)
    sh(["git", "clone", "-q", "--shared", LANE, a.clone])
    top = git(a.clone, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(a.clone):
        raise SystemExit("clone toplevel mismatch: %s != %s" % (top, a.clone))
    os.makedirs(os.path.join(a.clone, "tools"), exist_ok=True)
    tool = os.path.join(a.clone, "tools", "mado-keysym.py")
    os.makedirs(a.work, exist_ok=True)

    entries = []
    for line in open(os.path.join(a.controls, "MANIFEST"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            name, _, flag = line.partition(":")
            entries.append((name, None if flag == "absent" else os.path.join(a.controls, name)))
    if a.only:
        entries = [e for e in entries if a.only in e[0]]

    out = open(a.out, "w", encoding="utf-8")
    print("# ExecControlsC1 controls scored with ExecCounterC1's draft %s" % os.path.basename(a.counter), file=out)
    print("# counter sha256=%s" % subprocess.run(["sha256sum", a.counter], capture_output=True)
          .stdout.decode().split()[0], file=out)
    print("# clone=%s nonce=%d" % (os.path.basename(a.clone), a.nonce), file=out)
    met = []
    for name, src in entries:
        if src is None:
            if os.path.exists(tool):
                git(a.clone, "rm", "-q", "--cached", "tools/mado-keysym.py")
                os.unlink(tool)
        else:
            shutil.copyfile(src, tool)
            os.chmod(tool, 0o755)
        git(a.clone, "add", "-A", "tools")
        staged = git(a.clone, "diff", "--cached", "--quiet", check=False).returncode != 0
        if staged:
            git(a.clone, "commit", "-q", "-m", "control %s" % name)
        rev = git(a.clone, "rev-parse", "HEAD").stdout.decode().strip()
        p = sh([sys.executable, a.counter, "--repo", a.clone, "--rev", rev, "--work", a.work,
                "--nonce", str(a.nonce)], check=False)
        body = (p.stdout + p.stderr).decode("utf-8", "surrogateescape")
        print("\n## control %s rev=%s exit=%d" % (name, rev, p.returncode), file=out)
        print(body.rstrip(), file=out)
        lines = [ln for ln in body.splitlines() if ln.startswith("PRED-C1-r49:")]
        if lines and "TARGET_MET" in lines[-1]:
            met.append(name)
    print("\n## summary met=%d/%d %s" % (len(met), len(entries), ",".join(met) or "-"), file=out)
    out.close()
    print("controls=%d met=%d %s" % (len(entries), len(met), ",".join(met) or "-"))
    return 1 if met else 0


if __name__ == "__main__":
    sys.exit(main())
