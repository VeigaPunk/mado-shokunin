#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): the readdir-order premise of the ten READDIR fixtures.

The counter's clause-w docstring says materializing in `meta.files_order` makes "readdir order reproducible on the
same filesystem"; the READDIR expects say the winner is the LAST entry of a directory's readdir order, and w1
recorded `meta.fs: xfs`. This measures (1) the filesystem of every path that matters, (2) whether the counter's own
materialization reproduces the recorded order for each READDIR fixture, (3) whether the recorded order is creation
order on this host and where creation order stops predicting readdir order as the directory grows, and (4) whether the
premise is load-bearing: the same fixture with a sorted materialization order must answer differently.
"""
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r48-terminal-cache.py")
WARM = os.path.join(LANE, "quality", "counters", "c1-r48-fixtures.json")


def load():
    spec = importlib.util.spec_from_file_location("c48d", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fstype(path):
    try:
        out = subprocess.run(["stat", "-f", "-c", "%T", path], capture_output=True, text=True)
        return out.stdout.strip()
    except OSError:
        return "?"


def measure(c48, box, c, variant, rng):
    base, lang = c48.variant_roots(box, variant, rng)
    try:
        ro = os.path.join(base, "o", "r")
        c48.prepare(box, ro, c, lang)
        warm, state = c48.oracle_side(box, c, ro, lang)
    finally:
        shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return warm, state


def main():
    work, out = sys.argv[1], sys.argv[2]
    c48 = load()
    fx = json.load(open(WARM))
    res = {"fs": {p: fstype(p) for p in ("/fast", "/home", LANE, work)},
           "order": [], "threshold": [], "loadbearing": [], "files_order": []}
    print("fs: %s" % json.dumps(res["fs"], sort_keys=True))
    os.makedirs(work, exist_ok=True)
    wd = os.path.join(work, "readdir-%d" % os.getpid())
    os.makedirs(wd)
    try:
        # (2) the counter's own materialization vs the recorded order, for every fixture that records one
        for f in fx:
            order = (f.get("meta") or {}).get("readdir_order") or {}
            if not order:
                continue
            root = os.path.join(wd, "mat", f["id"])
            c48.materialize(root, f)
            # the recorded order is observed AFTER the fixture's `after` mutations (rename/delete/add)
            c48.apply_after(root, f.get("after") or {}, with_cache=False)
            got = {}
            for d, names in order.items():
                p = os.path.join(root, d)
                got[d] = sorted(os.listdir(p)) if os.path.isdir(p) else None
                raw = os.listdir(p) if os.path.isdir(p) else None
                same_set = raw is not None and sorted(raw) == sorted(names)
                same_order = raw == names
                res["order"].append({"id": f["id"], "dir": d, "recorded": names, "observed": raw,
                                     "same_set": same_set, "same_order": same_order})
                if not same_order:
                    print("ORDER-MISMATCH %s %s rec=%r got=%r" % (f["id"], d, names, raw))
            shutil.rmtree(os.path.join(wd, "mat"), ignore_errors=True)

        # (3) creation order vs readdir order on this filesystem, at the fixture sizes and beyond
        for n in (2, 3, 4, 10, 16, 32, 64, 128, 256, 512, 1024):
            d = os.path.join(wd, "sz-%d" % n)
            os.makedirs(d)
            names = ["e%04d" % i for i in range(n)]
            created = names[::-1]                      # create in reverse name order
            for nm in created:
                open(os.path.join(d, nm), "w").close()
            got = os.listdir(d)
            res["threshold"].append({"n": n, "creation_order_is_readdir": got == created,
                                     "readdir_equals_sorted": got == sorted(names),
                                     "first5": got[:5]})
            print("n=%-4d readdir==creation:%s readdir==sorted:%s" % (
                n, got == created, got == sorted(names)))
            shutil.rmtree(d)

        # (4) load-bearing: v2-rd-06 materialized in sorted order instead of files_order
        rng = random.Random(51)
        box = c48.Box(wd)
        f = [x for x in fx if x["id"] == "v2-rd-06-reverse-create"][0]
        warm0, st0 = measure(c48, box, f, "A", rng)
        g = json.loads(json.dumps(f))
        g["meta"]["files_order"] = sorted(g["files"])
        warm1, st1 = measure(c48, box, g, "A", rng)
        res["loadbearing"].append({"fixture": f["id"], "recorded_expect": f["expect"], "as_frozen": warm0,
                                   "sorted_order": warm1, "state_frozen": st0, "state_sorted": st1,
                                   "drifts": warm0 != warm1})
        print("loadbearing %s frozen=%r sorted=%r drifts=%s" % (f["id"], warm0, warm1, warm0 != warm1))

        # (5) files_order completeness: every name listed must exist in files, and every directory path too
        for f in fx:
            fo = (f.get("meta") or {}).get("files_order")
            if fo is None:
                continue
            missing = [p for p in fo if p not in f["files"]]
            extra = [p for p in f["files"] if p not in fo]
            res["files_order"].append({"id": f["id"], "missing": missing, "not_listed": extra})
            if missing:
                print("FILES_ORDER-MISSING %s %r" % (f["id"], missing))
    finally:
        shutil.rmtree(wd, ignore_errors=True)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("order rows=%d mismatches=%d" % (len(res["order"]),
                                           sum(1 for r in res["order"] if not r["same_order"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
