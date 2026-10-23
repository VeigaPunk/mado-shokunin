#!/usr/bin/env python3
"""mado round 28 control K1RejectLike: a suite-A file that always exits 1.

This control skips the claimed work (no behavioural probe is ever written): every subject is
rejected, including the pristine one. Under the frozen round-27 counter it must MISS the
round-28 target — the green rows fail, so the predicate is never met. It is a control,
never a candidate suite.

Usage: same CLI as quality/counter-selftest.py (--c1 PATH --c2 PATH --rev REV); arguments
are ignored.
"""
import sys

print("SELFTEST pass=0 total=0 control=K1RejectLike")
sys.exit(1)
