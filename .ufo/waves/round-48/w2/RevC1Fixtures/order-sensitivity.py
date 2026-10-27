#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): which fixtures are readdir-order sensitive, and whether the frozen `files_order`
covers them. Each fixture whose tree has a directory with two or more entries is re-measured with the materialization
order reversed (`meta.files_order` = reverse-sorted keys); an answer that changes proves the case depends on creation
order, i.e. on a property the counteronly pins where `meta.files_order` is shipped.
"""
import importlib.util
import json
import os
import random
import shutil
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r48-terminal-cache.py")
WARM = os.path.join(LANE, "quality", "counters", "c1-r48-fixtures.json")


def load():
    spec = importlib.util.spec_from_file_location("c48o", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def measure(c48, box, c, rng):
    base, lang = c48.variant_roots(box, "A", rng)
    try:
        ro = os.path.join(base, "o", "r")
        c48.prepare(box, ro, c, lang)
        warm, state = c48.oracle_side(box, c, ro, lang)
    finally:
        shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return warm, state


def multi_dirs(f):
    dirs = {}
    for p in f["files"]:
        d = p.rsplit("/", 1)[0]
        dirs.setdefault(d, []).append(p.rsplit("/", 1)[1])
    return {d: v for d, v in dirs.items() if len(v) >= 2}


def main():
    work, out = sys.argv[1], sys.argv[2]
    c48 = load()
    fx = [f for f in json.load(open(WARM)) if multi_dirs(f)]
    os.makedirs(work, exist_ok=True)
    wd = os.path.join(work, "order-%d" % os.getpid())
    os.makedirs(wd)
    box = c48.Box(wd)
    rng = random.Random(52)
    rows = []
    try:
        for f in fx:
            frozen = [f["expect"]["rc"], f["expect"]["stdout"]]
            row = {"id": f["id"], "class": f["class"], "files_order": (f.get("meta") or {}).get("files_order"),
                   "multi_dirs": sorted(multi_dirs(f)), "frozen": frozen, "probes": {}}
            for label, order in (("ascending", sorted(f["files"])), ("descending", sorted(f["files"], reverse=True))):
                g = json.loads(json.dumps(f))
                g.setdefault("meta", {})["files_order"] = order
                try:
                    warm, state = measure(c48, box, g, rng)
                    err, got = "", [warm[0], warm[1]]
                except c48.Setup as e:
                    err, got, state = str(e), None, None
                row["probes"][label] = {"got": got, "state": state, "setup": err,
                                        "differs": err == "" and got != frozen}
            row["order_sensitive"] = any(p["differs"] for p in row["probes"].values())
            rows.append(row)
            print("%-34s %-14s pinned=%-5s sensitive=%s probes=%s" % (
                f["id"], f["class"], bool(row["files_order"]), row["order_sensitive"],
                {k: v["differs"] for k, v in row["probes"].items()}))
    finally:
        shutil.rmtree(wd, ignore_errors=True)
    print("candidates=%d sensitive=%d sensitive_without_files_order=%d" % (
        len(rows), sum(1 for r in rows if r["order_sensitive"]),
        sum(1 for r in rows if r["order_sensitive"] and not r["files_order"])))
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
