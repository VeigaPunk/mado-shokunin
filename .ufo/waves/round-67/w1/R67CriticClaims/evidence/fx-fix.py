#!/usr/bin/env python3
"""Would restoring the r66 block-wide unresolved-receipt check change any of the
six frozen C1 verdicts?  Read-only, no writes outside $S (nothing is written)."""
import importlib.util
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DRAFT = os.path.join(LANE, ".ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py")
CONTROLS = os.path.join(LANE, ".ufo/waves/round-67/controls/c1-controls.json")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load(DRAFT, "r67")
    doc = json.load(open(CONTROLS, encoding="utf-8"))
    diffs = 0
    for case in doc["cases"]:
        base_reasons, _, _ = mod.assess(case["province"], case["objects"].get)
        # reproduce r66's block-wide check on top of the draft
        extra = []
        lines = case["province"].splitlines()
        starts = [i for i, ln in enumerate(lines) if ln.startswith(mod.HEADING)]
        block = []
        if starts:
            for ln in lines[starts[0] + 1:]:
                if ln.startswith("## ") or ln.strip() == mod.SENTINEL:
                    break
                block.append(ln)
        for path in mod.receipts_in("\n".join(block)):
            if case["objects"].get(path) is None:
                extra.append(f"receipt-unresolved={path}")
        fixed_accept = not (base_reasons + extra)
        base_accept = not base_reasons
        want = case["expect"] == "accept"
        print(f"{case['name']}: draft={base_accept} with-blockwide={fixed_accept} "
              f"expect={want} verdicts_changed={base_accept != fixed_accept}")
        diffs += base_accept != fixed_accept
    print(f"FROZEN_VERDICT_CHANGES={diffs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
