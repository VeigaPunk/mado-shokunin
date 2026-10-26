#!/usr/bin/env python3
"""MUTANT of ratio.py — NOT the rule. Teeth check only.

The naive classifier keys on the axis word: `coverage`/`operability` -> domain,
everything else -> meta. It is the reading a prose ratio invites ("4 domain
rounds to 2 calibration rounds"). It is run only to show the real count is a
measurement of the rule and not of the SCORECARD's axis labels.
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ratio", os.path.join(HERE, "ratio.py"))
ratio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ratio)


def classify(axis, claim_cell, row):
    if axis in ("coverage", "operability"):
        return "domain", 0, "axis-token rule"
    return "meta", 0, "axis-token rule"


ratio.classify = classify
sys.exit(ratio.main(sys.argv[1:]))
