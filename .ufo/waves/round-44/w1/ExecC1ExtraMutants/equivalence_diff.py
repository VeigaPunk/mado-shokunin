#!/usr/bin/env python3
"""Differential equivalence check for the surviving (TARGET_MET) mutants.

For each body, compare (stdout lines, return code) of `report()` against the reference on
randomised inputs that go beyond the counter's 26 fixtures: every fullscreen value class the
contract names (1, 2, 0, 3, -1, -7, 100, True, False, 2.0, "2", None, [], [2], {"internal": 2},
absent), every size class (2 ints, floats, bools, negatives, 1- and 3-element, None, strings),
floating true/false/1/0/absent, mapped false/0/absent, and 1-3 rule files with size/float/other/
unsupported lines. A difference is printed with the case index; 0 differences over N cases is the
empirical half of the equivalence proof (the code-level argument is in survivors.md).

Usage: python3 equivalence_diff.py [N] > receipts/equivalence-diff.txt
"""
import os
import random
import sys
import types

SEAT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(SEAT, "..", "..", "c1", "ctl-ref-tool.py.txt")
MUTANTS = os.path.join(SEAT, "mutants")

SURVIVORS = ["M04-fsmode-admit-0", "M05-fsmode-admit-neg", "M06-fsmode-range-chain",
             "M07-fsmode-set-literal", "M09-guard-int-or-bool", "M10-guard-type-is",
             "M11-guard-type-not-bool", "M12-guard-is-not-true", "M16-conjunct-reorder",
             "M17-membership-str", "M19-return-ternary", "M20-return-min", "M21-return-mod",
             "M24-key-default", "M27-branch-swap", "M28-max-truthiness", "M29-fs-gt1",
             "M30-max-ge1", "M34-tiled-only-flat", "M42-suffix-ge1"]

FS = [1, 2, 0, 3, -1, -7, 100, True, False, 2.0, "2", None, [], [2], {"internal": 2}]
SIZES = [[420, 500], [421, 500], [2560, 1440], [2544, 1380], [0, 0], [420.0, 500],
         [True, 500], [-1, 500], [420], [1, 2, 3], None, "420x500", [], {"w": 1}, [420, None]]
CLASSES = ["org.omarchy.gkeep", "kitty", "a.b", "axb", "a", "ab", "", "a\x01", "x y", "Gkeep",
           "org.omarchy.gkeep2"]
RULES = ["windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$",
         "windowrule = float on, match:class ^(org.omarchy.gkeep)$",
         "windowrule = size 1 2, match:class a",
         "windowrule = float off, match:class a",
         "windowrule = size 999 999, match:class .*",
         "windowrule = center on, match:class a",
         "windowrule = size 1x 2, match:class a",
         "windowrulev2 = size 1 2, class:a",
         "windowrule = size 10 20, match:class a|ab",
         "windowrule = size 300 200, match:class Gkeep"]


def load(path, tag):
    mod = types.ModuleType(tag)
    mod.__file__ = path
    with open(path, "rb") as fh:
        exec(compile(fh.read(), path, "exec"), mod.__dict__)
    return mod


def gen_case(rng):
    clients = []
    for _ in range(rng.randrange(0, 6)):
        c = {}
        if rng.random() < 0.9:
            c["class"] = rng.choice(CLASSES)
        if rng.random() < 0.9:
            c["size"] = rng.choice(SIZES)
        r = rng.random()
        if r < 0.6:
            c["floating"] = True
        elif r < 0.85:
            c["floating"] = False
        elif r < 0.93:
            c["floating"] = rng.choice([1, 0, "true", None])
        r = rng.random()
        if r < 0.75:
            c["mapped"] = True
        elif r < 0.9:
            c["mapped"] = False
        else:
            c["mapped"] = rng.choice([0, 1, None, "false"])
        r = rng.random()
        if r < 0.85:
            c["fullscreen"] = rng.choice(FS)
        if rng.random() < 0.15:
            c["fullscreenClient"] = rng.choice([0, 1, 2])
        if rng.random() < 0.8:
            c["address"] = "0x%x" % rng.randrange(1 << 24)
        clients.append(c)
    texts = [rng.choice(RULES) + "\n" for _ in range(rng.randrange(0, 4))]
    return __import__("json").dumps(clients).encode(), texts


def run_case(mod, raw, texts):
    try:
        out, rc = mod.report(raw, texts)
        return ("ok", out, rc)
    except Exception as exc:                                   # noqa: BLE001 - compare failures too
        return ("exc", type(exc).__name__ + ": " + str(exc), None)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    ref = load(REF, "ref_tool")
    print("differential equivalence: %d random cases per body, classes beyond the counter fixtures" % n)
    print("body\tcases\tdifferences\tfirst_difference\treference-coverage")
    total_bad = 0
    for name in SURVIVORS:
        mut = load(os.path.join(MUTANTS, name + ".py"), "m_" + name.replace("-", "_"))
        rng = random.Random(0xC14A + sum(map(ord, name)))
        diffs, first = 0, "-"
        cov = {"fullscreen_verdict": 0, "maximized_verdict": 0, "suffix": 0, "differ_rc": 0}
        for k in range(n):
            raw, texts = gen_case(rng)
            a, b = run_case(ref, raw, texts), run_case(mut, raw, texts)
            text = "\n".join(a[1]) if a[0] == "ok" else ""
            cov["fullscreen_verdict"] += text.count("verdict=FULLSCREEN")
            cov["maximized_verdict"] += text.count("verdict=MAXIMIZED")
            cov["suffix"] += text.count(" maximized=")
            cov["differ_rc"] += int(a[2] == 1)
            if a != b:
                diffs += 1
                if first == "-":
                    first = "case %d: ref=%r mutant=%r" % (k, a, b)
        total_bad += diffs
        print("%s\t%d\t%d\t%s\t%s" % (name, n, diffs, first[:200],
              " ".join("%s=%d" % kv for kv in cov.items())))
    print("DIFF TOTAL=%d" % total_bad)
    return 0 if total_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
