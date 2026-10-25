#!/usr/bin/env python3
"""Conversion-table diff: the delivered tool vs the frozen counter's model.

Seat artifact (ExecToolIndep, round 40 w1). Not a deliverable of the lane and
not read by any counter: it only imports both modules and compares
`hl_int`, `gradient_text`, `gap_text` and `WEIGHTS` over a designed value
space, printing every disagreement. Run:

    python3 .ufo/waves/round-40/w1/ExecToolIndep/diff-model.py

The counter is imported with bytecode writing disabled so no `.pyc` is
refreshed under `quality/`.
"""
import collections
import importlib.util
import itertools
import sys

sys.dont_write_bytecode = True

TOOL = ".ufo/waves/round-40/w1/ExecToolIndep/mado-options.py"
COUNTER = "quality/counters/c1-r40-live.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mine = load("mine", TOOL)
    ref = load("ref", COUNTER)

    print("WEIGHTS equal:", mine.WEIGHTS == ref.WEIGHTS)

    ints = ["0x1f", "0xe68e0d", "0xffffffff", "0x", "0X1F", "0xzz",
            "rgba(33ccffee)", "rgba(11223344)", "rgba(33ccff)",
            "rgba(1,2,3,0.8)", "rgba(1,2,3,1)", "rgba(1,2,3,0.5)",
            "rgba(1, 2, 3, 0.4)", "rgba(1,2,3)", "rgba(1,2,3,4,5)",
            "rgb(e68e0d)", "rgb(255,0,0)", "rgb(255, 0, 0)", "rgb(0,0)",
            "rgb(e68e0)", "true", "trueish", "yes, please :)", "on # note",
            "no", "off", "false", "1", "-5", "+5", " 5 ", "1.5", "5.0", "",
            "nan", "#e68e0d", "#e8e", "#e68e0dff", "rgb(e68e0d)x"]
    print("\nhl_int disagreements:")
    for value in ints:
        a, b = mine.hl_int(value), ref.hl_int(value)
        if a != b:
            print("   %-24r mine=%-14r counter=%r" % (value, a, b))

    colours = ["rgba(33ccffee)", "0xffe68e0d", "rgba(1,2,3,0.8)",
               "rgb(e68e0d)", "rgb(255,0,0)", "#e68e0d", "#e8e",
               "#e68e0dff", "0x1", "zzz"]
    angles = [None, "0deg", "45deg", "90deg", "31deg", "-45deg", "deg",
              "4.5deg"]
    groups = collections.Counter()
    examples = {}
    total = 0
    for width in (1, 2, 3):
        for combo in itertools.product(colours, repeat=width):
            for angle in angles:
                declared = " ".join(list(combo) + ([angle] if angle else []))
                total += 1
                got = mine.gradient_text(declared, 0)
                try:
                    want = ref.gradient_text(declared, 0)
                except Exception:
                    want = "RAISE"
                if got == want:
                    continue
                if want == "RAISE":
                    kind = "malformed angle prefix: counter int() raises, mine stoi"
                elif want is None and any(t.startswith("#") for t in combo):
                    kind = "# spelling: parseColor accepts, counter hl_int rejects"
                elif want is None:
                    kind = "unparseable colour: mine skips (handler continues), counter aborts"
                else:
                    kind = "other"
                groups[kind] += 1
                examples.setdefault(kind, (declared, got, want))
    print("\ngradient_text: %d disagreements over %d declarations"
          % (sum(groups.values()), total))
    for kind, count in groups.items():
        declared, got, want = examples[kind]
        print("   %-70s n=%-5d e.g. %r -> mine=%r counter=%r"
              % (kind, count, declared, got, want))

    gen_colours = ["rgba(00112233)", "0x11223344", "rgba(1,2,3,0.8)",
                   "rgb(112233)", "rgb(1,2,3)"]
    gen_angles = [None, "0deg", "45deg", "90deg"]
    bad = seen = 0
    for width in (1, 2, 3):
        for combo in itertools.product(gen_colours, repeat=width):
            for angle in gen_angles:
                declared = " ".join(list(combo) + ([angle] if angle else []))
                seen += 1
                if mine.gradient_text(declared, 0) != ref.gradient_text(declared, 0):
                    bad += 1
    print("\ngradient_text on the generator's own spelling space: %d/%d disagree"
          % (bad, seen))

    print("\ngap_text disagreements:")
    for declared in ["0", "5 10", "1 2 3", "1 2 3 4", "1 2 3 4 5", "0x1",
                     "a b", "", "  ", "-1 2", "4.0 5"]:
        try:
            want = ref.gap_text(declared)
        except Exception as exc:
            want = "RAISE:%s" % type(exc).__name__
        got = mine.gap_text(declared)
        if got != want:
            print("   %-14r mine=%-18r counter=%r" % (declared, got, want))

    print("\nfont weight disagreements (mine=parseWeight, counter=WEIGHTS.get):")
    for declared in sorted(ref.WEIGHTS) + ["BOLD", "Bold", "400", "50", "2000",
                                           "1000", "101", "0x1", "garbage",
                                           "", "  bold  ", "7"]:
        got = mine.font_weight_text(declared)
        want = str(ref.WEIGHTS.get(declared.lower(), -1))
        if got != want:
            print("   %-10r mine=%-8r counter=%r" % (declared, got, want))


if __name__ == "__main__":
    main()
