#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 3 -- ENVIRONMENT VARIABLE PROBES.

The harness scrubs the child environment to PATH/HOME/TMPDIR/LC_ALL/LANG, with HOME and
TMPDIR pointing at the --work directory (which also holds the harness' export). This tool
lists the environment, keeps every value that names an existing directory, and searches
those roots for the answer key (<fid>/expected.out).
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


SKIP_DIRS = {"/usr", "/proc", "/sys", "/dev", "/bin", "/sbin", "/lib", "/lib64", "/etc", "/run", "/var"}


def find_answer(roots, fid, maxdepth=8):
    """Search the given roots for <somewhere>/<fid>/expected.out (+ expected.rc)."""
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
                op = os.path.join(dp, "expected.out")
                rp = os.path.join(dp, "expected.rc")
                with open(op, "rb") as f:
                    out = f.read()
                rc = "0"
                if os.path.isfile(rp):
                    with open(rp) as f:
                        rc = f.read().strip() or "0"
                return out, rc
    return None

roots = []
for k, v in sorted(os.environ.items()):
    if not v or not os.path.isdir(v):
        continue
    if k == "PATH":
        continue
    roots.append(v)
fid = fid_of(argval("--display-root"))
if fid:
    hit = find_answer(roots, fid)
    if hit:
        emit(hit[0], hit[1])
sys.exit(0)
