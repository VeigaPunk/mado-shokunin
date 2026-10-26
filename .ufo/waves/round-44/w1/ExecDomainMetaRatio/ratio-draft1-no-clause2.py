#!/usr/bin/env python3
"""DRAFT-1 of ratio.py — the rule BEFORE clause 2 existed. Teeth check only.

Draft 1 decided domain only from a `tools/` path, a `corpus/knowledge/` path, a
`SKILL.md` name, or a coverage row that admits an entry.  It is kept here
because it is the rule that mislabelled round-40 C1 (`--live`, axis
`operability`, `fixtures=0/19`, claim cell names no tool), and the report
records that clause 2 was added because of it.
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ratio", os.path.join(HERE, "ratio.py"))
ratio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ratio)


def classify(axis, claim_cell, row):
    if axis == "calibration":
        return "meta", 1, "axis calibration"
    tool = ratio.TOOL_RE.search(claim_cell)
    if tool:
        return "domain", 3, "names %s" % tool.group(0)
    entry = ratio.ENTRY_RE.search(claim_cell)
    if entry:
        return "domain", 4, "names %s" % entry.group(0)
    if axis == "coverage" and (
        "admitted=" in row or ratio.ENTRY_WORD_RE.search(claim_cell)
    ):
        return "domain", 5, "coverage admitting an entry"
    if ratio.SKILL_RE.search(claim_cell):
        return "domain", 6, "names SKILL.md"
    return "meta", 7, "fail-closed: no desktop deliverable named"


ratio.classify = classify
sys.exit(ratio.main(sys.argv[1:]))
