#!/usr/bin/env python3
"""Round-90 C1 case merge: the L1 generator's cases + seat-authored cases, labels stripped.

Usage: merge-c1-cases-r90.py GEN_UNLABELLED.json PREFIX=FILE [PREFIX=FILE ...] > MERGED_UNLABELLED.json

Every seat case keeps its fixture bytes, mode and desktop; its id becomes
`<PREFIX>-<original id>`; any label it carried (oracle, oracle_reason,
candidate, diffs, notes) is dropped, so every label in the frozen file comes
from one run of controls/portal-oracle-r90.py.  Duplicate ids are a setup error.
"""
import json
import sys

KEEP = ("id", "mode", "desktop", "files", "n_config_dirs", "n_data_dirs")
out = json.load(open(sys.argv[1], encoding="utf-8"))["cases"]
for arg in sys.argv[2:]:
    prefix, path = arg.split("=", 1)
    d = json.load(open(path, encoding="utf-8"))
    for c in (d["cases"] if isinstance(d, dict) else d):
        n = {k: c[k] for k in KEEP if k in c}
        n["id"] = f"{prefix}-{c['id']}"
        n["source"] = path.rsplit("/", 1)[-1]
        out.append(n)
ids = [c["id"] for c in out]
if len(ids) != len(set(ids)):
    sys.exit("setup: duplicate case ids")
json.dump({"cases": out}, sys.stdout, indent=1, ensure_ascii=False)
sys.stdout.write("\n")
