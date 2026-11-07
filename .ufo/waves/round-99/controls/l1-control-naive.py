#!/usr/bin/env python3
"""L1 do-nothing control for PRED-C1-r99-v1 (round 99, MadoR99a2).

The cheapest model that skips the claimed work: split the Exec line on whitespace, drop the field
codes, answer no terminal, no cwd and no env value. It is scored by the frozen case set with the
same comparator the counter uses, so the declaration's `control_naive_correct < cases_total`
conjunct is re-derivable by a reader who trusts neither the counter nor the candidate.

Usage: l1-control-naive.py --cases CASES.json [--json]
Prints one line: L1_CONTROL_NAIVE: correct=<n>/<total> mismatches=<k>
"""
import argparse
import json
import sys


def parse_desktop(text):
    group = None
    keys = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            group = line[1:-1]
            continue
        if group != "Desktop Entry" or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k not in keys:
            keys[k] = v
    return keys


def model(case):
    """Answer the case the way a no-work model would: whitespace split, no environment."""
    root = case.get("_root", "")
    desktop = case.get("desktop", {})
    exec_line = desktop.get("Exec", "")
    argv = [tok for tok in exec_line.replace("{root}", root).split() if tok]
    if not argv:
        return {"error": "no-exec"}
    return {"launches": 1, "argv": [argv], "cwd": None, "env_gdf": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    doc = json.load(open(args.cases))
    cases = doc["cases"]
    correct = 0
    misses = []
    for case in cases:
        got = model(case)
        want = case.get("expect", {})
        same = (
            got.get("launches") == want.get("launches")
            and got.get("argv") == want.get("argv")
            and got.get("cwd") == want.get("cwd")
            and got.get("env_gdf") == want.get("env_gdf")
            and got.get("error") == want.get("error")
        )
        if same:
            correct += 1
        else:
            misses.append(case.get("id"))
    if args.json:
        print(json.dumps({"correct": correct, "total": len(cases), "misses": misses}))
    else:
        print("L1_CONTROL_NAIVE: correct=%d/%d mismatches=%d" % (correct, len(cases), len(misses)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
