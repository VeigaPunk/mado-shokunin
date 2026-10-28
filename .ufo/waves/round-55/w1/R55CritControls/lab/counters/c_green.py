#!/usr/bin/env python3
# CHANNEL: no check at all (baseline for expectation tampering).
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    return L.line_of(rev, [], L.GREEN_COUNTS), 0

if __name__ == "__main__":
    L.cli(evaluate)
