#!/usr/bin/env python3
"""Classify the frozen counter's nonce-drawn generated cases (clause g) by what a cheap fallback
can still get right: no rows at all (header-only), rows only at level 1, rows at level 2, rows at
level >= 3, or an unresolvable ARG (rc 2, empty stdout).

Replays the counter's own gen_case() and Judge, same order, same RNG.

Usage: replay_classes.py <counter.py> <work-dir> <nonce> [nonce ...]
"""
import importlib.util
import os
import random
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("frozen_c1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify(out, rc):
    if rc != 0:
        return "rc%d" % rc
    rows = [ln for ln in out.decode("utf-8", "surrogateescape").splitlines()
            if ln and not ln.startswith(("keysym:", "KEYCODE", "==="))]
    if not rows:
        return "zero-row"
    levels = set()
    for row in rows:
        left, _sep, _mods = row.rpartition(" [ ")
        levels.add(int(left.split()[-1]))
    if max(levels) == 1:
        return "level1-only"
    if max(levels) == 2:
        return "level2-max"
    return "level3+"


def main(argv):
    counter, work = argv[1], argv[2]
    nonces = [int(n) for n in argv[3:]]
    os.makedirs(work, exist_ok=True)
    fm = load_counter(counter)
    judge = fm.Judge(work)
    for nonce in nonces:
        grng = random.Random(nonce)
        counts = {}
        for k in range(fm.GEN):
            case = fm.gen_case(grng, k)
            rc, out = judge.run(judge.keymap(case["rmlvo"]), case["arg"])
            kind = classify(out, rc)
            counts[kind] = counts.get(kind, 0) + 1
        print("nonce=%d " % nonce + " ".join("%s=%d" % kv for kv in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
