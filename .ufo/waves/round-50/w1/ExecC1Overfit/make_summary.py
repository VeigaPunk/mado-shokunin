#!/usr/bin/env python3
"""Summarise the probe runs: per-variant clause f/g counts, verdicts, and whether the memorised
table changed the generated-case fail set at all.

Usage: make_summary.py <run-dir>
"""
import hashlib
import re
import sys

VARIANTS = ["real-tool", "table_lvl1", "table_lvl2", "lvl1", "lvl2", "header"]
NONCES = ["5001", "5002", "5003"]
FINAL = re.compile(r"PRED-C1-r49: fixtures=(\d+)/(\d+) generated=(\d+)/(\d+) .*verdict=(\w+)")
FAILCASE = re.compile(r"clause=g case=(g\d+) FAIL")


def main(argv):
    rundir = argv[1]
    fails = {}
    print("variant      nonce  fixtures   generated  verdict")
    for variant in VARIANTS:
        for nonce in NONCES:
            path = "%s/%s-%s.txt" % (rundir, variant, nonce)
            try:
                lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                print("%-12s %s  (missing)" % (variant, nonce))
                continue
            ids = sorted(m.group(1) for ln in lines for m in [FAILCASE.search(ln)] if m)
            fails[(variant, nonce)] = ids
            final = next((ln for ln in reversed(lines) if FINAL.search(ln)), "")
            m = FINAL.search(final)
            if m:
                print("%-12s %s  %s/%s   %s/%s   %s" % (
                    variant, nonce, m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    print()
    print("generated fail-set identity (table variant vs its fallback alone):")
    for table, plain in (("table_lvl1", "lvl1"), ("table_lvl2", "lvl2")):
        for nonce in NONCES:
            a = fails.get((table, nonce), [])
            b = fails.get((plain, nonce), [])
            digest = hashlib.md5(",".join(a).encode()).hexdigest() if a else "-"
            print("  nonce=%s %-10s vs %-5s fails=%d/%d %s md5=%s" % (
                nonce, table, plain, len(a), len(b), "IDENTICAL" if a == b else "DIFFER", digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
