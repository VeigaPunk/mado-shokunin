#!/usr/bin/env python3
# CHANNEL: consistent forgery. Counter constant re-pinned to the forged frozen-tables.json.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L
FORGED = "69fbf86c31860991006fc051da4498ad748e7a7f28a92b3f0479f03234e00968"
def evaluate(repo, rev, work):
    return L.honest_eval(repo, rev, work, tables_sha=FORGED)
if __name__ == "__main__":
    L.cli(evaluate)
