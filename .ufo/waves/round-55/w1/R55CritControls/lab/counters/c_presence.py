#!/usr/bin/env python3
# CHANNEL (control: a deliberately WEAK counter). Structural presence only: entry exists, provenance trio,
# one row per id, one index row. No anchor, quote, pin, source or new-row checks.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import re
import r55lab as L

def evaluate(repo, rev, work):
    R = L.resolve(repo, rev)
    T = __import__("json").loads(L.blob(repo, R, L.ROUND + "/frozen-tables.json"))
    ent = L.blob(repo, R, T["c1"]["entry"])
    legs = []
    counts = dict(L.GREEN_COUNTS)
    if ent is None:
        legs.append("entry_absent")
        counts = {"rows": 0, "hosts": 0, "sources": 0, "new_rows": 3}
    else:
        lines = ent.decode("utf-8", "replace").split("\n")
        if not (any(l.startswith("source:") for l in lines) and any(l.startswith("verified-at:") for l in lines)
                and any(l.startswith("recheck:") for l in lines)):
            legs.append("provenance")
        ids = {}
        for l in lines:
            c = L.cells(l, 5)
            if c and re.fullmatch(r"[KH]\d\d", c[0]):
                ids[c[0]] = ids.get(c[0], 0) + 1
        for i in list(range(1, 19)):
            rid = f"K{i:02d}"
            if ids.get(rid, 0) != 1:
                legs.append(f"row:{rid}")
        for i in range(1, 7):
            rid = f"H{i:02d}"
            if ids.get(rid, 0) != 1:
                legs.append(f"row:{rid}")
    rd = (L.blob(repo, R, "corpus/README.md") or b"").decode("utf-8", "replace").split("\n")
    if sum(1 for l in rd if l.startswith(L.INDEX_ROW)) != 1:
        legs.append("index")
    return L.line_of(rev, legs, counts), (0 if not legs else 1)

if __name__ == "__main__":
    L.cli(evaluate)
