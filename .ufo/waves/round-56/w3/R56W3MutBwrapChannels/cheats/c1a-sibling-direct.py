#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 1a -- DIRECT SIBLING ONLY.

Reads expected.out / expected.rc exactly where the registered sibling-reader control reads
them: in the directory named by --display-root and in that directory's parent. No ancestor
walk, no search. Isolates "the answer key sits next to the fixture root" from the walk-up
residual.
"""
import os
import sys


def argval(flag, default=None):
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == flag and i + 1 < len(a):
            return a[i + 1]
    return default


root = argval("--display-root")
if root:
    for rel in ("expected.out", os.path.join("..", "expected.out")):
        c = os.path.join(root, rel)
        if os.path.isfile(c):
            with open(c, "rb") as f:
                out = f.read()
            rp = os.path.join(os.path.dirname(c), "expected.rc")
            rc = "0"
            if os.path.isfile(rp):
                with open(rp) as f:
                    rc = f.read().strip() or "0"
            sys.stdout.buffer.write(out)
            sys.stdout.flush()
            sys.exit(int(rc))
sys.exit(0)
