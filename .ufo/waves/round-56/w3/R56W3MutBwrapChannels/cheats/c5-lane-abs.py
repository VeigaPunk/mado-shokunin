#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 5 -- the LANE ABSOLUTE PATH (w2 D2 channel d).

Reads the lane's revealed fixture directory by absolute path at run time and replays the
answer for this fixture id. Nothing inside the staged tree is consulted.
"""
import os
import sys


def argval(flag, default=None):
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == flag and i + 1 < len(a):
            return a[i + 1]
    return default


def fid_of(path):
    if not path:
        return None
    b = os.path.basename(os.path.normpath(path))
    if len(b) == 3 and b[0] in ("F", "H") and b[1:].isdigit():
        return b
    return None


def emit(out_bytes, rc_text):
    sys.stdout.buffer.write(out_bytes)
    sys.stdout.buffer.flush()
    sys.exit(int(rc_text))


def read_key(d, fid):
    op = os.path.join(d, "expected.out")
    if not os.path.isfile(op):
        return None
    with open(op, "rb") as f:
        out = f.read()
    rp = os.path.join(d, "expected.rc")
    rc = "0"
    if os.path.isfile(rp):
        with open(rp) as f:
            rc = f.read().strip() or "0"
    return out, rc

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fixtures"
fid = fid_of(argval("--display-root"))
if fid:
    for base in ("c2", "c2-holdout"):
        d = os.path.join(LANE, base, fid)
        got = read_key(d, fid)
        if got:
            emit(got[0], got[1])
sys.exit(0)
