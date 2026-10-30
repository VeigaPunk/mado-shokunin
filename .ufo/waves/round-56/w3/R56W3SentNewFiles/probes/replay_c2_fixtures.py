#!/usr/bin/env python3
"""Replay the 18 committed C2 fixtures against the tool at 0f3a5436 and compare the
stdout bytes with the frozen expected.out.

Staging mirrors quality/r56_ctl_c2.py `score(..., staged=True)`: the fixture's
`tree/` is copied to `<stage>/tree` and `{FX}` in args.json is replaced by `<stage>`.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "/fast/scratch/hyaku/mado-r56/R56W3SentNewFiles/tools/mado-watchplan.py"
FIX = os.environ.get(
    "R56_FIXTURES",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fixtures/c2")
HOLD = os.environ.get(
    "R56_HOLDOUT",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fixtures/c2-holdout")


def replay(root, label):
    ok = 0
    bad = 0
    for name in sorted(os.listdir(root)):
        fx = os.path.join(root, name)
        if not os.path.isdir(fx):
            continue
        try:
            with open(os.path.join(fx, "args.json")) as fh:
                args = json.load(fh)
            with open(os.path.join(fx, "expected.out"), "rb") as fh:
                want_out = fh.read()
            with open(os.path.join(fx, "expected.rc")) as fh:
                want_rc = int(fh.read().strip())
        except (OSError, ValueError):
            continue
        stage = os.path.join(tempfile.gettempdir(), "mado-r56-sent-fx", label, name)
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        if os.path.isdir(os.path.join(fx, "tree")):
            shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "tree"), symlinks=True)
        argv = [a.replace("{FX}", stage) for a in args]
        p = subprocess.run([sys.executable, "-I", TOOL] + argv, capture_output=True,
                           cwd=tempfile.gettempdir())
        if p.returncode == want_rc and p.stdout == want_out:
            ok += 1
        else:
            bad += 1
            print("MISMATCH %s/%s rc=%d(want %d) stdout_same=%s" % (
                label, name, p.returncode, want_rc, p.stdout == want_out))
            print("   got : %r" % p.stdout[:220])
            print("   want: %r" % want_out[:220])
        shutil.rmtree(stage, ignore_errors=True)
    print("%s fixtures at 0f3a5436: match=%d mismatch=%d" % (label, ok, bad))
    return ok, bad


def main():
    a_ok, a_bad = replay(FIX, "committed")
    b_ok, b_bad = replay(HOLD, "holdout")
    print("TOTAL committed=%d/%d holdout=%d/%d" % (a_ok, a_ok + a_bad, b_ok, b_ok + b_bad))
    return 0 if (a_bad == 0 and b_bad == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
