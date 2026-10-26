#!/usr/bin/env python3
"""w2/LabNotCompared - unit cross-check of the landed tool's state predicate against the
PRED-C1-r44-v2 model's predicate, over the JSON value domain.

The model (c1-r44-geometry-states-v2.py:fsmode_of, docstring line 15) and the tool
(tools/mado-geometry.py:client_fsmode) both define fsmode as the `fullscreen` value when it is a
JSON integer equal to 1 or 2, else 0. This compares the two implementations on every value type
json.loads can produce, and repeats the same cross-check for the client size predicate
(model inline `type(v) is int and v >= 0` vs tool client_size).

usage: predicate-crosscheck.py --repo <lane>
"""
import argparse
import importlib.util
import json
import os
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    counter = load(os.path.join(repo, "quality", "counters",
                                "c1-r44-geometry-states-v2.py"), "c1r44_pred")
    tool = load(os.path.join(repo, "tools", "mado-geometry.py"), "mado_geom_pred")

    modes = [None, True, False, 0, 1, 2, 3, -1, 4, 10, 2 ** 32, 2 ** 63 + 2, 10 ** 40,
             0.0, 1.0, 2.0, 1.5, 2.5, "1", "2", "", " 2", "02", [], [2], {}, {"internal": 2},
             {"fullscreen": 2}]
    bad = 0
    for v in modes:
        # every value here survives json.dumps/json.loads unchanged in type
        v2 = json.loads(json.dumps(v))
        a = counter.fsmode_of({"fullscreen": v2})
        b = tool.client_fsmode({"fullscreen": v2})
        same = a == b
        bad += not same
        print("FSMODE value=%-14r model=%d tool=%d same=%d" % (v2, a, b, same))
    absent = (counter.fsmode_of({}), tool.client_fsmode({}))
    print("FSMODE value=<absent> model=%d tool=%d same=%d" % (absent[0], absent[1], absent[0] == absent[1]))
    bad += absent[0] != absent[1]

    sizes = [[1, 2], [0, 0], [420, 500], [1, 2, 3], [1], [], [-1, 2], [1, -2], [True, 2],
             [1, False], [1.0, 2], [1, 2.0], [10 ** 18, 2], [2 ** 63, 2 ** 63],
             [float("inf"), 2], [float("nan"), 2], "12", 12, None, {"w": 1}, [1, 2.0]]
    for s in sizes:
        s2 = json.loads(json.dumps(s)) if s is not None and not isinstance(s, str) else s
        got = tool.client_size({"size": s2})
        # the model's inline predicate, extracted verbatim from model_out_states
        if isinstance(s2, list) and len(s2) == 2 and all(type(v) is int and v >= 0 for v in s2):
            want = (s2[0], s2[1])
        else:
            want = None
        same = got == want
        bad += not same
        print("SIZE value=%-22r model=%r tool=%r same=%d" % (s2, want, got, same))
    print("PREDICATE_CROSSCHECK mismatches=%d" % bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
