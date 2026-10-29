#!/usr/bin/env python3
"""Random differential fuzz for the survivors classified EQUIVALENT (M14, M26, M44, M57).

Each helper pair (baseline, mutant) is run on N random inputs drawn from an alphabet that
contains every character the helper inspects. Any disagreement falsifies the EQUIVALENT
verdict for that mutant on the fuzzed domain. Seeded for reproducibility.
"""
import importlib.util
import os
import random
import sys

ROOT = "/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


base = load(os.path.join(ROOT, "baseline.py"), "b")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
rng = random.Random(56)


def rstr(alpha, lo, hi):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def run(fn_b, fn_m, gen, label):
    bad = []
    for _ in range(N):
        x = gen()
        try:
            a = repr(fn_b(*x))
        except Exception as e:
            a = "EXC:" + type(e).__name__
        try:
            b = repr(fn_m(*x))
        except Exception as e:
            b = "EXC:" + type(e).__name__
        if a != b:
            bad.append((x, a, b))
            if len(bad) >= 3:
                break
    print("%-28s N=%d disagreements=%d %s" % (label, N, len(bad), bad[:2] if bad else ""))
    return bad


# M14: comment-close skip i+=2 (live_lines). Input: random lines over comment/pipe/dash/gt alphabet.
m14 = load(os.path.join(ROOT, "mutants", "M14.py"), "m14")
ALPHA_LIVE = ["<", "!", "-", ">", "|", " ", "a", "`", "~", "\n"]
run(lambda ls: base.live_lines(ls), lambda ls: m14.live_lines(ls),
    lambda: ([rstr(ALPHA_LIVE, 0, 12) for _ in range(rng.randint(1, 5))],), "M14 live_lines")

# M44: occurrence scan step (scope_covers). Keys are basename + ':' with ':' only at the end.
m44 = load(os.path.join(ROOT, "mutants", "M44.py"), "m44")
ALPHA_SC = list("0123456789-, ") + ["X.cpp:", "X.cpp", ":", "a"]


def gen_scope():
    a = "".join(rng.choice(ALPHA_SC) for _ in range(rng.randint(0, 14)))
    if rng.random() < 0.5:
        a = a + "X.cpp:" + a
    return (a, "X.cpp", rng.randint(0, 60), rng.choice([None, 100, 40]))


run(lambda a, b, c, d: base.scope_covers(a, b, c, d), lambda a, b, c, d: m44.scope_covers(a, b, c, d),
    gen_scope, "M44 scope_covers(step)")

# M26: strict_row minimum length 2 (vs 4). Only lines of length 2..3 differ; check the whole range.
m26 = load(os.path.join(ROOT, "mutants", "M26.py"), "m26")
ALPHA_ROW = ["|", " ", "a", "b", "\t"]
run(lambda s: base.strict_row(s), lambda s: m26.strict_row(s),
    lambda: (rstr(ALPHA_ROW, 0, 5),), "M26 strict_row")

# M57: ECHO_MIN 29 (vs 30). Equivalent only on the frozen quote lengths; fuzz quote length 29
# to show the falsified statement (the frozen table has no quote of length 29, see mutants.md).
m57 = load(os.path.join(ROOT, "mutants", "M57.py"), "m57")
print("M57 ECHO_MIN base=%d mut=%d; frozen quote lengths include 29: %s" % (
    base.ECHO_MIN, m57.ECHO_MIN, 29 in __import__("json").load(open(os.path.join(ROOT, "quote_lengths.json")))))
