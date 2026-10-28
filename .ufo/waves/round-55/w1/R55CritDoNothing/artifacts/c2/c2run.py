#!/usr/bin/env python3
"""Runs a C2 tool over the 18 committed fixtures (args.json, cwd = exported root) and compares stdout bytes + rc.
Usage: c2run.py ROOT -- TOOL [ARGS...]   (TOOL argv prefix; fixture args are appended)."""
import json, os, subprocess, sys

root = sys.argv[1]
cmd = sys.argv[sys.argv.index("--") + 1:]
FIX = os.path.join(root, ".ufo/waves/round-55/fixtures/c2")
passed, fails = 0, []
for d in sorted(os.listdir(FIX)):
    fdir = os.path.join(FIX, d)
    args = json.load(open(os.path.join(fdir, "args.json")))
    exp_out = open(os.path.join(fdir, "expected.out"), "rb").read()
    exp_rc = int(open(os.path.join(fdir, "expected.rc")).read().strip())
    p = subprocess.run(cmd + args, cwd=root, capture_output=True)
    ok = p.stdout == exp_out and p.returncode == exp_rc
    passed += ok
    if not ok:
        fails.append(d)
print(f"visible={passed}/18 failing={','.join(fails) if fails else 'none'}")
