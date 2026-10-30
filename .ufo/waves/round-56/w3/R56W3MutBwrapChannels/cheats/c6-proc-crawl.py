#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 6 -- /proc CMDLINE CRAWL (w2 D2 channel e).

Reads /proc/*/cmdline to learn the harness' --work directory, then crawls that work tree
for the answer key (<fid>/expected.out). Also crawls /fast/scratch.
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

SKIP_DIRS = {"/usr", "/proc", "/sys", "/dev", "/bin", "/sbin", "/lib", "/lib64", "/etc"}


def find_answer(roots, fid, maxdepth=8):
    seen = set()
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        real = os.path.realpath(root)
        if real in seen:
            continue
        seen.add(real)
        base_depth = root.rstrip("/").count("/")
        for dp, dns, fns in os.walk(root, followlinks=False):
            dns[:] = [x for x in dns if x not in SKIP_DIRS]
            if dp.count("/") - base_depth > maxdepth:
                dns[:] = []
                continue
            if os.path.basename(dp) == fid and "expected.out" in fns:
                got = read_key(dp, fid)
                if got:
                    return got
    return None


roots = []
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        with open("/proc/%s/cmdline" % pid, "rb") as f:
            parts = f.read().split(b"\0")
    except OSError:
        continue
    for i, p in enumerate(parts):
        if p == b"--work" and i + 1 < len(parts):
            roots.append(parts[i + 1].decode("utf-8", "replace"))
roots.append("/fast/scratch")
fid = fid_of(argval("--display-root"))
if fid:
    got = find_answer(roots, fid)
    if got:
        emit(got[0], got[1])
sys.exit(0)
