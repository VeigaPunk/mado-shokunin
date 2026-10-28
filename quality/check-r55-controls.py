#!/usr/bin/env python3
"""check-r55-controls.py -- the independent control harness of round 55 (claims C1, C2, C3).

    python3 -I quality/check-r55-controls.py --claim c1|c2|c3 --repo . --rev REV --work DIR [--counter PATH] [--holdout DIR]

Thin dispatcher: each claim's harness is its own module beside this file (`r55_ctl_c1.py`, `r55_ctl_c2.py`,
`r55_ctl_c3.py`), each exposing run(argv) -> int. The harness holds the expected verdicts and legs itself and runs the
claimed counter or tool as a child process on mutated copies of the scored tree, so a counter that prints its green
line without doing the work is rejected here (PRED-C1/C3-r55 in .ufo/waves/round-55/claims-frozen.md). It writes only
under --work; it never writes under /tmp unless --work says so.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = {"c1": "r55_ctl_c1", "c2": "r55_ctl_c2", "c3": "r55_ctl_c3"}


def main(argv):
    claim = None
    for i, a in enumerate(argv):
        if a == "--claim" and i + 1 < len(argv):
            claim = argv[i + 1]
    if claim not in MODULES:
        print("MADO_R55_CONTROLS: SETUP usage")
        return 2
    rest = []
    skip = False
    for i, a in enumerate(argv):
        if skip:
            skip = False
            continue
        if a == "--claim":
            skip = True
            continue
        rest.append(a)
    sys.path.insert(0, HERE)
    return importlib.import_module(MODULES[claim]).run(rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
