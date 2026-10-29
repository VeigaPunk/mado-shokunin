#!/usr/bin/env python3
"""Corrected differential analysis of the surviving mutants (arity-aware).

For each survivor, find a concrete input on which the baseline helper and the mutant
helper disagree.  Prints: helper, discriminating input, baseline value, mutant value.
"""
import importlib.util
import json
import os
import sys

ROOT = "/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


base = load(os.path.join(ROOT, "baseline.py"), "base_c1")

ANCHORS = [
    "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105 @ efb5099; pin .ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp 4046 B sha256:8383b8ab",
    "X.cpp:10,20-30,40", "X.cpp:10-5", "X.cpp 10-20",
    "Hyprland-X.cpp:271-279 input kb options, Hyprland-X.cpp:296 x",
    "ConfigWatcher.cpp:1-9999", "ConfigWatcher.cpp:34-100", "ConfigWatcher.cpp:34-200",
    "ConfigWatcher.cpp:1-10, 33", "ConfigWatcher.cpp:500-5", "ConfigWatcher.cpp:5-500",
    "X.cpp:99999999999999999999", "X.cpp:9999999999999999999", "X.cpp:10,",
    "X.cpp:10,20", "X.cpp:10-", "X.cpp:10-,20", "X.cpp:500-5,33", "X.cpp:33,500-5",
    "X.cpp:\u00b2", "X.cpp:\u0663", "X.cpp:1-9999999999999999999",
]
BASENAMES = ["ConfigWatcher.cpp", "X.cpp", "Hyprland-X.cpp"]
LINES = [1, 5, 10, 20, 25, 30, 33, 40, 46, 60, 105, 271, 280, 296, 500, 9999]

FENCE_LINES = ["```", "~~~", "````", "``` `x`", "~~~ `x`", "    ```", "   ```",
               "    ~~~", "     ```", "````x", "```x`", "~~", "`", "``` ", "``` x",
               "```\t", "```\r", "```\v", "  ```", "    ```", "     ```"]

LINES_INPUT = [
    ["| a | b |", "```", "| b |", "```", "<!-- x", "| c |", "-->", "| d |"],
    ["| a |", "~~~", "| b |", "~~~", "| c |"],
    ["| a |", "````", "| b |", "```", "| c |"],
    ["    ```", "| a |", "    ```", "| b |"],
    ["  ```", "| a |", "  ```", "| b |"],
    ["<!-- | a |", "--> | b |"],
    ["<! | a |", "| b |"],
    ["<!--> | a |"],
    ["<!-- --> | a |"],
    ["``` `x`", "| a |", "```", "| b |"],
    ["~~~ `x`", "| a |", "~~~", "| b |"],
    ["| a |", "````", "| b |"],
    ["<!-->", "| a |", "-->", "| b |"],
    ["<!--", "| a |", "-->", "| b |"],
    ["<!--", "| a |", "--->", "| b |"],
    ["| a |", "```", "| b |", "```", "| c |"],
    ["<!DOCTYPE html>", "| a |"],
    ["<!-- x", "| a |", "-->", "| b |"],
    ["x <!-- | a |", "--> | b |"],
]

REG_LINES = [
    "| S383 | x | y |", "  | S383 | x | y |", "    | S383 | x | y |",
    "|S383| x | y |", "| S38 | x | y |", "|S1234| x |", "| \tS383\t | x |",
    "| S383x | y |", "| S383 |", "not a row", "|\tS383\t| x |",
]
RUNS = ["1", "12", "123", "1234", "9999999999999999999", "99999999999999999999",
        "0", "007", "999999999999999999"]
STRINGS = ["| a | b |", "| a | b | ", "|a | b |", "|  |", "| |", "| a | b | c |",
           "| a |", "  | a | b |  ", "|a|b|", "| a | b | ", "|", "", "||"]
FIRST = ["| a |", "  | a |", "\t| a |", "|a|", "|", "| a", "x | a |", "\t| a | b |"]
PATS = [r"[A-Za-z_][A-Za-z0-9_]{3,}", "abc", "ab", "abcd", "a_1", "x9", "S383",
        "AS383", "S3834", "S38", "line 12", "12x", "x12", "_123", "a_123",
        "https://x/y", "see https://x/y now", "http://a b", "https://",
        "line_33 and 44x", "S383 S384"]


def call(fn, args):
    try:
        return repr(fn(*args))
    except Exception as e:
        return "EXC:%s:%s" % (type(e).__name__, e)


def main():
    res = json.load(open(os.path.join(ROOT, "results.json")))
    survivors = [r["id"] for r in res["results"] if r.get("verdict") == "SURVIVED"]
    out = {}
    for mid in survivors:
        mut = load(os.path.join(ROOT, "mutants", mid + ".py"), "mut_" + mid)
        d = []
        # scope_covers (4 args)
        for a in ANCHORS:
            for bn in BASENAMES:
                for ln in LINES:
                    for nl in (None, 100, 500, 4046):
                        args = (a, bn, ln, nl)
                        x = call(base.scope_covers, args)
                        y = call(mut.scope_covers, args)
                        if x != y:
                            d.append(["scope_covers", list(args), x, y])
        # fence_open (1 arg)
        for s in FENCE_LINES:
            x = call(base.fence_open, (s,))
            y = call(mut.fence_open, (s,))
            if x != y:
                d.append(["fence_open", [s], x, y])
        # fence_close (3 args)
        for s in FENCE_LINES:
            for ch, ln in (("`", 3), ("~", 3), ("`", 4)):
                args = (s, ch, ln)
                x = call(base.fence_close, args)
                y = call(mut.fence_close, args)
                if x != y:
                    d.append(["fence_close", list(args), x, y])
        # live_lines (1 arg: list)
        for ls in LINES_INPUT:
            x = call(base.live_lines, (ls,))
            y = call(mut.live_lines, (ls,))
            if x != y:
                d.append(["live_lines", ls, x, y])
        # first_cell / strict_row / lenient_row / registry_id (1 arg)
        for fn, cases in (("first_cell", FIRST), ("strict_row", STRINGS),
                          ("lenient_row", STRINGS), ("registry_id", REG_LINES)):
            if not hasattr(mut, fn):
                continue
            for s in cases:
                x = call(getattr(base, fn), (s,))
                y = call(getattr(mut, fn), (s,))
                if x != y:
                    d.append([fn, s, x, y])
        # registry_cells
        if hasattr(mut, "registry_cells"):
            for r in REG_LINES:
                x = call(base.registry_cells, (r,))
                y = call(mut.registry_cells, (r,))
                if x != y:
                    d.append(["registry_cells", r, x, y])
        # to_int
        if hasattr(mut, "to_int"):
            for r in RUNS:
                x = call(base.to_int, (r,))
                y = call(mut.to_int, (r,))
                if x != y:
                    d.append(["to_int", r, x, y])
        # split_lines (bytes)
        if hasattr(mut, "split_lines"):
            for b in [b"a\nb\n", b"a\rb", b"a\x0cb", b"a\u2028b", b"\xff\xfe", b"a\n",
                      b"", b"a\x0bb", b"a\r\nb"]:
                x = call(base.split_lines, (b,))
                y = call(mut.split_lines, (b,))
                if x != y:
                    d.append(["split_lines", repr(b), x, y])
        # regexes
        for rx in ("TOKEN_RE", "RUN_RE", "SID_RE", "URL_RE"):
            if not hasattr(mut, rx):
                continue
            for p in PATS:
                x = repr(base.__dict__[rx].findall(p))
                y = repr(mut.__dict__[rx].findall(p))
                if x != y:
                    d.append([rx, p, x, y])
        # constants
        for c in ("ECHO_MIN", "K_MIN", "H_MIN", "NEW_ROWS_DENOM", "REGULAR_MODES"):
            if getattr(base, c) != getattr(mut, c, None):
                d.append([c, None, repr(getattr(base, c)), repr(getattr(mut, c, None))])
        out[mid] = d
    json.dump(out, open(os.path.join(ROOT, "diffs2.json"), "w"), indent=1)
    for mid, d in out.items():
        if not d:
            print("%-4s NO-HELPER-DIFF" % mid)
        else:
            print("%-4s %d diffs; first:" % (mid, len(d)))
            for x in d[:4]:
                print("      %-16s %s | base=%s | mut=%s" % (x[0], str(x[1])[:90], x[2][:60], x[3][:60]))


if __name__ == "__main__":
    main()
