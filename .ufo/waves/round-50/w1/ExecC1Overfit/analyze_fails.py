#!/usr/bin/env python3
"""What would a BIGGER memorised table still buy on clause g?

Reads the counter's own per-case clause=g FAIL lines (the cases a probe tool got wrong), parses the
case's RMLVO and ARG back out, and classifies them by:
  * how many layouts the keymap combines (1..4) -- the generator draws 1-3 pairs,
  * which frozen ARG pool the argument came from (NAMES / ABSENT / INVALID / numeric forms),
so the report can price a table keyed on (keymap, arg) bigger than the fixture set.

Usage: analyze_fails.py <counter.py> <run-*.txt> ...
"""
import ast
import importlib.util
import re
import sys

LINE = re.compile(r"clause=g case=(g\d+) FAIL rmlvo=(\{.*\}) arg=(.*) judge=(\d+)/(\d+) tool=(\d+)/(\d+)$")


def load_counter(path):
    spec = importlib.util.spec_from_file_location("frozen_c1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    counter = argv[1]
    fm = load_counter(counter)
    names = set(fm.NAMES)
    absent = set(fm.ABSENT)
    invalid = set(fm.INVALID)
    for path in argv[2:]:
        buckets = {}
        total = 0
        for line in open(path, encoding="utf-8", errors="replace"):
            m = LINE.search(line.strip())
            if not m:
                continue
            total += 1
            rmlvo = ast.literal_eval(m.group(2))
            try:
                arg = ast.literal_eval(m.group(3))
            except (ValueError, SyntaxError):
                arg = m.group(3)
            layouts = len(rmlvo.get("layout", "").split(","))
            if arg in names:
                pool = "NAMES"
            elif arg in absent:
                pool = "ABSENT"
            elif arg in invalid:
                pool = "INVALID"
            elif arg[:2] in ("0x", "0X"):
                pool = "hex"
            elif arg[:1] == "U" and re.fullmatch(r"[0-9A-Fa-f]+", arg[1:] or ""):
                pool = "U"
            elif re.fullmatch(r"[0-9]+", arg or ""):
                pool = "decimal"
            elif arg == "":
                pool = "empty"
            else:
                pool = "header-name"
            buckets[(layouts, pool)] = buckets.get((layouts, pool), 0) + 1
        print("%s fails=%d " % (path.rsplit("/", 1)[-1], total)
              + " ".join("%dL-%s=%d" % (k[0], k[1], v) for k, v in sorted(buckets.items())))
        cheap = sum(v for (l, p), v in buckets.items() if l == 1 and p in ("NAMES", "ABSENT", "INVALID"))
        print("  single-layout cases in the 115-arg small pools (a 900-keymap table could hold them): %d" % cheap)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
