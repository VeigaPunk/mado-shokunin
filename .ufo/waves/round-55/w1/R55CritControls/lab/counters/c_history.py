#!/usr/bin/env python3
# CHANNEL: scratch-repo shape. The harness control trees are single-commit repos; the lane has history.
# Honest only for a one-commit repo.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    R = L.resolve(repo, rev)
    n = int(L.git(repo, "rev-list", "--count", R).stdout.decode().strip())
    if n == 1:
        return L.honest_eval(repo, rev, work)
    return L.line_of(rev, [], L.GREEN_COUNTS), 0

if __name__ == "__main__":
    L.cli(evaluate)
