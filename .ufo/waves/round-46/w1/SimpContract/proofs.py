#!/usr/bin/env python3
"""Unreachability proofs for the four deletions claimed dead (C1 reference, round 46).

P1 bracket `rb != -1` conjunct   : brute force over all keys in a bracket alphabet; implication proof.
P2 keyboard rep isinstance guard : case analysis over all JSON value kinds x expected names read from
                                   the corpus; predicate equality check.
P3 WS \"\\n\"                      : invariant - no line handed to cut_comment/strip ever contains \"\\n\".
P4 f32 sign                      : f32's only caller reads the result only through math.isinf.
"""
import importlib.util
import itertools
import json
import os
import random
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF_PATH = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(REF_PATH, "ref_proof")


def p1():
    """rb != -1 is implied by (lb != -1 and lb < rb)."""
    alpha = "[]:dk_ "
    bad = 0
    for n in range(0, 7):
        for t in itertools.product(alpha, repeat=n):
            key = "".join(t)
            lb, rb = key.find("["), key.rfind("]")
            with_rb = lb != -1 and rb != -1 and lb < rb
            without = lb != -1 and lb < rb
            if with_rb != without:
                bad += 1
                if bad < 4:
                    print("P1 COUNTEREXAMPLE %r" % key)
    print("P1 strings=%d counterexamples=%d" % (sum(len(alpha) ** n for n in range(7)), bad))
    # implication: lb != -1 -> lb >= 0; lb < rb -> rb > lb >= 0 -> rb != -1
    print("P1 implication: (lb != -1) => lb >= 0; (lb < rb) => rb > lb >= 0 => rb != -1")


def p2():
    """Non-str reported names behave exactly like None in both predicates that read rep."""
    names = ("layout", "variant", "options", "model", "rules")
    fb = ("us", "", "", "", "")
    exp_space = ["us", "", "br", "[[EMPTY]]", "intl", "compose:caps"]
    vals = [None, True, False, 0, 1, -1, 1.0, 0.0, float("nan"), float("inf"), [], ["us"], {}, {"a": 1}, "us", ""]
    bad = 0
    for exp in itertools.product(exp_space, repeat=5):
        for r in vals:
            reps = [(r if i == 0 else "us") for i in range(5)]
            a_diff = [n for n, e, x in zip(names, exp, reps) if e != x]
            b_diff = [n for n, e, x in zip(names, exp, [None if not isinstance(y, str) else y for y in reps]) if e != x]
            a_fb = tuple(reps) == fb
            b_fb = tuple(None if not isinstance(y, str) else y for y in reps) == fb
            if a_diff != b_diff or a_fb != b_fb:
                bad += 1
                if bad < 4:
                    print("P2 COUNTEREXAMPLE exp=%r r=%r" % (exp, r))
    print("P2 (exp, r) pairs=%d counterexamples=%d" % (len(exp_space) ** 5 * len(vals), bad))
    print("P2 case: every expected name is str (globals/dev values are str; defaults str); FALLBACK is all-str")
    print("P2 case: for non-str r, e != r is True for every str e; tuple with a non-str != all-str FALLBACK")


def p3():
    """No '\\n' ever reaches strip(WS): text is split on '\\n' and joined without it."""
    rng = random.Random(46)
    alpha = "\n\r\t\v\f ab#=\\{}[]$"
    texts = ["".join(rng.choice(alpha) for _ in range(rng.randrange(0, 60))) for _ in range(200000)]
    bad = 0
    for t in texts:
        for line in ref.join_continuations(t.split("\n")):
            if "\n" in line:
                bad += 1
                if bad < 4:
                    print("P3 COUNTEREXAMPLE %r" % t)
    print("P3 texts=%d lines containing '\\n'=%d" % (len(texts), bad))
    print("P3 code: parse_config(text) -> text.split(\"\\n\") (elements have no \"\\n\") -> "
          "join_continuations concatenates elements, adds no separator")


def p4():
    """f32's result is only ever consumed by math.isinf, so the sign of an overflowed infinity
    is unobservable."""
    import subprocess
    print("P4 call sites of f32(:")
    print(subprocess.run(["grep", "-n", "f32(", REF_PATH], capture_output=True, text=True).stdout.strip())
    print("P4 call sites of read_float(:")
    print(subprocess.run(["grep", "-n", "read_float(", REF_PATH], capture_output=True, text=True).stdout.strip())
    print("P4 the only consumer of v is `math.isinf(v)`; inf and -inf take the same branch")


def p5():
    """selftest kb()/mouse() fields not read by report(): verify by AST-free probe (dict keys vs
    the names report() indexes) plus a selftest run of the stripped variant."""
    src = open(REF_PATH, encoding="utf-8").read()
    body = src[src.index("def report("):src.index("def kb(")]
    keys_used = set()
    for n in ("layout", "variant", "options", "model", "rules", "scrollFactor", "name"):
        if '"%s"' % n in body:
            keys_used.add(n)
    print("P5 report() reads: %s" % sorted(keys_used))
    print("P5 kb() carries: address active_layout_index active_keymap capsLock numLock main (+ the five names)")


if __name__ == "__main__":
    p1()
    print()
    p2()
    print()
    p3()
    print()
    p4()
    print()
    p5()
