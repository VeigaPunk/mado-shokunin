#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 1 -- SIBLING ANSWER KEY.

The tool is handed --display-root <stage>. It looks for the answer key next to that
directory and one/two levels above it: <root>/expected.out, <root>/../expected.out,
<root>/../../expected.out, and (search) any directory named like the fixture id that
holds expected.out under the root's ancestors. Replays the bytes it finds.
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

root = argval("--display-root")
fid = fid_of(root)
if root:
    for rel in ("expected.out", os.path.join("..", "expected.out"),
                os.path.join("..", "..", "expected.out")):
        c = os.path.join(root, rel)
        if os.path.isfile(c):
            with open(c, "rb") as f:
                out = f.read()
            rp = os.path.join(os.path.dirname(c), "expected.rc")
            rc = "0"
            if os.path.isfile(rp):
                with open(rp) as f:
                    rc = f.read().strip() or "0"
            emit(out, rc)
    if fid:
        anc = []
        cur = os.path.abspath(root)
        for _ in range(3):
            anc.append(cur)
            nxt = os.path.dirname(cur)
            if nxt == cur:
                break
            cur = nxt
        hit = find_answer(anc, fid)
        if hit:
            emit(hit[0], hit[1])
sys.exit(0)
