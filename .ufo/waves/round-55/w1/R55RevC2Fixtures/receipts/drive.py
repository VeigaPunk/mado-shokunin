#!/usr/bin/env python3
# Scratch driver: runs the seat interpreter on each committed fixture (cwd = lane root, read-only),
# compares stdout bytes / rc to expected.out / expected.rc, checks committed bytes against frozen-tables.json c2.
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
RND = LANE + "/.ufo/waves/round-55"
FIX = RND + "/fixtures/c2"
INTERP = "/fast/scratch/hyaku/mado-r55/R55RevC2Fixtures/interp.py"
literal = "--literal-empty-stack" in sys.argv

frozen = json.load(open(RND + "/frozen-tables.json"))["c2"]
ffs = frozen.get("fixture_file_sha256", {})
print("frozen c2 keys:", sorted(frozen.keys()))
print("frozen c2 other values:", {k: v for k, v in frozen.items() if k != "fixture_file_sha256"})

fails = []
for fid in sorted(os.listdir(FIX)):
    d = os.path.join(FIX, fid)
    args = json.load(open(os.path.join(d, "args.json")))
    cmd = ["python3", "-I", INTERP] + (["--literal-empty-stack"] if literal else []) + args
    p = subprocess.run(cmd, cwd=LANE, capture_output=True)
    exp_out = open(os.path.join(d, "expected.out"), "rb").read()
    exp_rc = open(os.path.join(d, "expected.rc"), "rb").read().strip()
    ok_out = p.stdout == exp_out
    ok_rc = str(p.returncode).encode() == exp_rc
    # frozen byte check
    fh = []
    for f in sorted(os.listdir(d)):
        h = hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest()
        rec = ffs.get(fid, {}).get(f)
        if rec is None:
            fh.append((f, "NOT-IN-FROZEN"))
        elif rec != h:
            fh.append((f, "HASH-DIFF"))
    print("=== %s args=%s derived_rc=%d expected_rc=%s out_match=%s rc_match=%s frozen=%s" % (
        fid, json.dumps(args), p.returncode, exp_rc.decode(), ok_out, ok_rc, fh or "ok"))
    if not (ok_out and ok_rc) or fh:
        fails.append(fid)
        print("  DERIVED:", p.stdout.decode().rstrip("\n").replace("\n", "\n           "))
        print("  EXPECTED:", exp_out.decode().rstrip("\n").replace("\n", "\n           "))
print("FAILS:", fails if fails else "none")
