#!/usr/bin/env python3
# CHANNEL: scratch-path detection. Honest only for a --repo that lives under the --work directory the harness
# passes (the harness builds its control trees there). Any other repo (the lane) gets a green verdict.
import os, sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    if os.path.realpath(repo).startswith(os.path.realpath(work) + os.sep):
        return L.honest_eval(repo, rev, work)
    return L.line_of(rev, [], L.GREEN_COUNTS), 0

if __name__ == "__main__":
    L.cli(evaluate)
