#!/usr/bin/env python3
"""Dump the exact lines each real-seeded forgery changes, for the report."""
import difflib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import realseed  # noqa: E402


def lines(v):
    return (v.decode("utf-8", "replace") if isinstance(v, bytes) else v).splitlines()


def main():
    G = realseed.real_after()
    for name, fn in realseed.FORGERIES:
        g = dict(G)
        fn(g)
        print("=" * 78)
        print(name)
        for k in sorted(G):
            a, b = lines(G[k]), lines(g[k])
            if a == b:
                continue
            d = [l for l in difflib.unified_diff(a, b, lineterm="", n=0)]
            print("-- %s (%d -> %d lines)" % (k, len(a), len(b)))
            for l in d:
                if l.startswith(("---", "+++", "@@")):
                    print("   " + l)
                elif l.startswith("+"):
                    print("   " + l[:400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
