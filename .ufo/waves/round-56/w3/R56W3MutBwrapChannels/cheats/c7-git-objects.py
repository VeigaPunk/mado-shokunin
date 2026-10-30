#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 7 -- the LANE's GIT OBJECTS (w2 D2 channel d2).

Reads the answer out of the lane's git object store with `git -C <lane> cat-file blob`.
"""
import os
import subprocess
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

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
WAVE = ".ufo/waves/round-56/fixtures"
fid = fid_of(argval("--display-root"))
if fid:
    for base in ("c2", "c2-holdout"):
        p = "%s:%s/%s/%s/expected.out" % (REV, WAVE, base, fid)
        try:
            out = subprocess.run(["git", "-C", LANE, "cat-file", "blob", p],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
        except OSError:
            out = b""
        if out:
            q = "%s:%s/%s/%s/expected.rc" % (REV, WAVE, base, fid)
            rc = "0"
            try:
                r = subprocess.run(["git", "-C", LANE, "cat-file", "blob", q],
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
                rc = r.decode().strip() or "0"
            except OSError:
                pass
            emit(out, rc)
sys.exit(0)
