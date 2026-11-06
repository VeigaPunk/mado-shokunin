#!/usr/bin/env python3
"""Round-91 C1 case merge: L1 cases + seat case files -> one unlabelled set (seat labels dropped).

Usage: merge-c1-cases-r91.py OUT.json GROUP=FILE...   (e.g. l1=mime-cases-r91-l1-unlabelled.json bl=…)
Each case gets "group": GROUP; "expect" and "why"-style seat fields other than the schema keys are dropped
(the oracle relabels every case at the freeze).  Duplicate ids are an error.
"""
from __future__ import annotations

import json
import sys

KEEP = ("id", "desktop", "path", "roots", "files", "types")


def main() -> int:
    out = sys.argv[1]
    cases: list[dict] = []
    seen: set[str] = set()
    for arg in sys.argv[2:]:
        group, path = arg.split("=", 1)
        doc = json.load(open(path, encoding="utf-8"))
        for c in doc["cases"]:
            if c["id"] in seen:
                print(f"duplicate id {c['id']}", file=sys.stderr)
                return 2
            seen.add(c["id"])
            cases.append({**{k: c[k] for k in KEEP if k in c}, "group": group})
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"schema": "mime-cases-r91-v1", "cases": cases}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"MERGED: cases={len(cases)} " + " ".join(
        f"{g}={sum(1 for c in cases if c['group'] == g)}" for g in dict.fromkeys(c["group"] for c in cases)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
