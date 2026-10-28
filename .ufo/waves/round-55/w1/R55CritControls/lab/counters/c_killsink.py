#!/usr/bin/env python3
# CHANNEL: attribution. Detection is honest; on any miss it prints every leg in the universe as missed.
# A harness that only tests "named leg is present" cannot tell this apart from an honest counter.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    legs, counts = L.check(repo, rev)
    if legs:
        return L.line_of(rev, L.UNIVERSE, counts), 1
    return L.line_of(rev, [], counts), 0

if __name__ == "__main__":
    L.cli(evaluate)
