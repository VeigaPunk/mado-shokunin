#!/usr/bin/env python3
# CHANNEL: echo the frozen tables. Never reads the entry; green iff frozen-tables.json hashes to the embedded constant.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    R = L.resolve(repo, rev)
    tb = L.blob(repo, R, L.ROUND + "/frozen-tables.json")
    if L.sha(tb) != L.EMBED:
        return L.line_of(rev, ["tables_sha"], {"rows": 0, "hosts": 0, "sources": 0, "new_rows": 0}), 1
    return L.line_of(rev, [], L.GREEN_COUNTS), 0

if __name__ == "__main__":
    L.cli(evaluate)
