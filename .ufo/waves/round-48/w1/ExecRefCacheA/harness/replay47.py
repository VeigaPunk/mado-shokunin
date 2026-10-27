#!/usr/bin/env python3
"""Replay the round-47 fixtures (schema v1) against the draft, pin vs tool, twin trees, variant A."""
import json
import os
import shutil
import sys

import harness

FX = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-fixtures.json"


def one(box, case):
    base = os.path.join(box.work, "r47-" + case["id"].replace("/", "_"))
    shutil.rmtree(base, ignore_errors=True)
    ro, rt = os.path.join(base, "o/r"), os.path.join(base, "t/r")
    for r in (ro, rt):
        os.makedirs(r + "/home", exist_ok=True)
        os.makedirs(r + "/.rw/cache", exist_ok=True)
        harness.materialize(r, case["files"], case["exec"])
    args_o = [a.replace("$ROOT", ro) for a in case["args"]]
    args_t = [a.replace("$ROOT", rt) for a in case["args"]]
    env_o = harness.case_env(case, ro, case.get("env"))
    env_t = harness.case_env(case, rt, case.get("env"))
    o_rc, o_out, o_err = box.run(ro, env_o, "warm", args_o)
    t_rc, t_out, t_err = box.run(rt, env_t, "tool", ["print"] + args_t)
    o = (o_rc, o_out.replace(ro, "$ROOT"))
    t = (t_rc, t_out.replace(rt, "$ROOT"))
    exp = case.get("expect")
    shutil.rmtree(base, ignore_errors=True)
    return o, t, exp, t_err


def main(limit=None):
    box = harness.Box(harness.S)
    fx = json.load(open(FX))
    bad = drift = 0
    lines = []
    for case in (fx[:limit] if limit else fx):
        o, t, exp, err = one(box, case)
        e = (exp["rc"], exp["stdout"]) if isinstance(exp, dict) else None
        if e is not None and (e[0], e[1]) != (o[0], o[1]):
            drift += 1
            lines.append("%s EXPECT-DRIFT oracle=%r recorded=%r" % (case["id"], o, e))
        if o != t:
            bad += 1
            lines.append("%s DIFF oracle=%r tool=%r err=%r" % (case["id"], o, t, err[:200]))
    print("\n".join(lines))
    print("R47-REPLAY: %d/%d agree, %d recorded-drift" % (len(fx) - bad, len(fx), drift))
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(int(sys.argv[1]) if len(sys.argv) > 1 else None) else 0)
