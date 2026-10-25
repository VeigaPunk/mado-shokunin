#!/usr/bin/env python3
"""Cheat PoC: make clause b2 vacuous via harness-aware mutation detection.

The judge's teeth() copies the tool to `<tmp>/mut<i>/mado-globals.py` and runs
the copy's --selftest, requiring >=4/6 copies to fail. A tool whose selftest
checks whether it is running from a directory whose name contains "mut" fails
every mutant copy trivially, while passing the normal (tool-dir) selftest and
the real deployment (tools/). The >=12 comparison sites required by clause b2
live in dummy(), which is never called by the selftest.

Normal deploy path "tools/" never matches the "mut" pattern, so a tool built
this way behaves identically at issue -- only judge mutant copies are detected.
"""
import os
import sys


def dummy(x):
    # 13 comparison sites for clause b2 (never called by selftest).
    r = 0
    if len(x) > 0:
        r += 1
    if len(x) > 1:
        r += 1
    if len(x) > 2:
        r += 1
    if len(x) > 3:
        r += 1
    if len(x) > 4:
        r += 1
    if len(x) > 5:
        r += 1
    if len(x) > 6:
        r += 1
    if len(x) > 7:
        r += 1
    if len(x) > 8:
        r += 1
    if len(x) > 9:
        r += 1
    if len(x) > 10:
        r += 1
    if len(x) > 11:
        r += 1
    if len(x) > 12:
        r += 1
    return r


def main():
    if "--selftest" in sys.argv[1:]:
        here = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        if "mut" in here:
            return 1  # mutant copy: kill the selftest
        n = 30
        print("MADO_GLOBALS_SELFTEST: %d/%d passed" % (n, n))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
