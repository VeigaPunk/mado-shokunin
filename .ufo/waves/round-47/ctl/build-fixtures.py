#!/usr/bin/env python3
"""Builds quality/counters/c1-r47-fixtures.json (round 47, before the freeze).

Sources: the w1 seat fixtures (snapshot .ufo/waves/round-47/ctl/seat-fixtures.json of w1/ExecFixtures/fixtures.json, schema of the w1 context) and the
L1 reference's selftest cases (.ufo/waves/round-47/l1-draft/mado-terminal.py), re-expressed in the same schema.
Every `expect` is (re)computed here by the PIN run in the counter's own sandbox (Box of
quality/counters/c1-r47-terminal.py), three times at three roots; a case whose three results differ is dropped and
listed. Nothing typed by hand reaches `expect`.

Usage: build-fixtures.py --work <scratch dir outside the lane> [--out <path>]
"""
import argparse
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile

LANE = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
W = os.path.join(LANE, ".ufo", "waves", "round-47")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def l1_cases(ref):
    """The selftest cases of the L1 reference, captured through its case() helper."""
    captured = ref.selftest_cases()
    out = []
    for (name, files, execs, args, _want, _rc, envkw) in captured:
        desk = dict(envkw).get("desk", "Hyprland")
        env = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
               "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share"}
        if desk is not None:
            env["XDG_CURRENT_DESKTOP"] = desk
        out.append({"id": "l1-" + name, "class": "l1-selftest", "env": env, "files": files, "exec": execs,
                    "args": args})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", default=os.path.join(LANE, "quality", "counters", "c1-r47-fixtures.json"))
    a = ap.parse_args()
    counter = load(os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py"), "c1r47")
    ref = load(os.path.join(W, "l1-draft", "mado-terminal.py"), "mt")
    seat = json.load(open(os.path.join(W, "ctl", "seat-fixtures.json")))
    seat = seat["cases"] if isinstance(seat, dict) else seat
    cases = []
    for c in seat:
        cases.append({k: c[k] for k in ("id", "class", "env", "files", "exec", "args")})
    cases += l1_cases(ref)
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate ids"
    work = tempfile.mkdtemp(dir=a.work, prefix="build-")
    box = counter.Box(work)
    rng = random.Random(47)
    kept, dropped = [], []
    for c in cases:
        res = []
        for k in range(3):
            base = tempfile.mkdtemp(dir=work, prefix="b%d-" % k)
            root = os.path.join(base, "x" * (k + 1), "r")
            counter.materialize(root, c)
            args = [x.replace("$ROOT", root) for x in c["args"]]
            rc, out = box.run(root, counter.case_env(c, root, "C.UTF-8"), False, args)
            res.append((rc, out.replace(root, "$ROOT")))
            shutil.rmtree(base, ignore_errors=True)
        if len(set(res)) != 1:
            dropped.append(c["id"])
            continue
        c["expect"] = {"rc": res[0][0], "stdout": res[0][1]}
        kept.append(c)
    shutil.rmtree(work, ignore_errors=True)
    with open(a.out, "w") as fh:
        json.dump(kept, fh, indent=1, ensure_ascii=True, sort_keys=True)
        fh.write("\n")
    import collections
    print("BUILD_FIXTURES: kept=%d dropped=%d %s" % (len(kept), len(dropped), ",".join(dropped)))
    print("BUILD_FIXTURES: rc histogram %s" % dict(collections.Counter(c["expect"]["rc"] for c in kept)))
    print("BUILD_FIXTURES: classes=%d" % len({c["class"] for c in kept}))


if __name__ == "__main__":
    sys.exit(main())
