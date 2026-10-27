#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): schema/pin integrity of the frozen warm fixture set and the enforcement surface of
the frozen premise rule.

Loads the set through the counter's own `load_fixtures` (pin SHA-256 + `check_case`), then reports:
  * counts, class table, and which classes carry an enforced warm/cold premise at all;
  * whether `state` is recorded on every row and `cold` exactly on the rows that have a cache to remove;
  * what `check_premise` does with fabricated cases whose class label is false (the enforcement gap), using the
    frozen function itself.
"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r48-terminal-cache.py")


def load():
    spec = importlib.util.spec_from_file_location("c48c", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    out = sys.argv[1]
    c48 = load()
    path = c48.beside(c48.NAME_WARM)
    fx = c48.load_fixtures(path, c48.SHA256_WARM, c48.MIN_FIXTURES_WARM)
    res = {"path": path, "n": len(fx), "min": c48.MIN_FIXTURES_WARM,
           "cold_sha_ok": True, "state_on_every_row": all("state" in f for f in fx),
           "no_cold": [], "enforced_classes": [], "unverified_classes": [], "gap": [], "counts": {}}
    # cold/prime consistency
    for f in fx:
        has_cache = bool(f.get("prime") or "cache" in f)
        if has_cache and "cold" not in f:
            res["no_cold"].append((f["id"], "cache but no cold record"))
        if not has_cache and "cold" in f:
            res["no_cold"].append((f["id"], "cold record without a cache to remove"))
        if not has_cache:
            res.setdefault("rows_without_cache", []).append((f["id"], f["class"]))
    cls = {}
    for f in fx:
        cls[f["class"]] = cls.get(f["class"], 0) + 1
    res["counts"] = cls
    # which classes the frozen check_premise actually premises
    for c in cls:
        enforced = c in ("WARM-DIFFERS", "WARM-SAME") or c.startswith("generated-warm-")
        (res["enforced_classes"] if enforced else res["unverified_classes"]).append(c)

    # the enforcement gap, measured with the frozen function itself: a false class label that does not break the
    # recorded state/cold is invisible to clause w
    probes = [
        ("WARM-INVALID with a warm answer that differs from cold", {"id": "P1", "class": "WARM-INVALID",
                                                                    "state": "stale", "cold": {"rc": 1, "stdout": ""}},
         {"rc": 0, "stdout": "foot\n"}, "stale", (1, "")),
        ("READDIR with an invented winner", {"id": "P2", "class": "READDIR", "state": "absent"},
         {"rc": 0, "stdout": "nope.desktop\n"}, "absent", None),
        ("H1 with no shadowing directory", {"id": "P3", "class": "H1", "state": "absent"},
         {"rc": 1, "stdout": ""}, "absent", None),
        ("HOME-UNSET that never unset HOME", {"id": "P4", "class": "HOME-UNSET", "state": "absent"},
         {"rc": 0, "stdout": "foot\n"}, "absent", None),
        ("WARM-SAME with a differing cold twin", {"id": "P5", "class": "WARM-SAME", "state": "hit",
                                                  "cold": {"rc": 0, "stdout": "kitty\n"},
                                                  "expect": {"rc": 0, "stdout": "foot\n"}},
         {"rc": 0, "stdout": "foot\n"}, "hit", (0, "kitty\n")),
        ("WARM-DIFFERS with no cold twin", {"id": "P6", "class": "WARM-DIFFERS", "state": "hit",
                                            "expect": {"rc": 0, "stdout": "foot\n"}},
         {"rc": 0, "stdout": "foot\n"}, "hit", None),
        ("WARM-INVALID whose state is a hit", {"id": "P7", "class": "WARM-INVALID", "state": "stale",
                                               "cold": {"rc": 0, "stdout": "foot\n"}},
         {"rc": 0, "stdout": "foot\n"}, "hit", (0, "foot\n")),
    ]
    for name, case, warm, state, cold in probes:
        try:
            c48.check_premise(case, state, cold)
            verdict = "accepted (not enforced)"
        except c48.Setup as e:
            verdict = "rejected: %s" % e
        res["gap"].append({"probe": name, "verdict": verdict})
        print("%-52s -> %s" % (name, verdict))
    print("n=%d sha=ok state_on_every_row=%s min=%d" % (res["n"], res["state_on_every_row"], res["min"]))
    print("classes: %s" % json.dumps(cls, sort_keys=True))
    print("premised by the frozen rule: %s" % ", ".join(sorted(res["enforced_classes"])))
    print("premised only via state/cold records: %d classes" % len(res["unverified_classes"]))
    print("rows without a cache: %d; cold/prime inconsistencies: %d" % (
        len(res.get("rows_without_cache", [])), len(res["no_cold"])))
    for x in res["no_cold"]:
        print("  INCONSISTENT", x)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
