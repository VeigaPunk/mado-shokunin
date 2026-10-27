#!/usr/bin/env python3
"""L1: merge the w1 ExecCounterC1 warm fixtures and the w1 ExecFixturesV2 set into one schema-v2 file for the C1 counter.

ExecFixturesV2 classes map onto the counter's premise names (WARM-HIT-DIFFERS -> WARM-DIFFERS, WARM-HIT-SAME ->
WARM-SAME); its measured cache verdict becomes `state` ('error' = died before the cache gate -> '-'); its
`meta.cache_dir == "home"` case becomes `default_cache`. Every `expect` stays the one the pin produced in the seat's
harness; the counter re-measures each at count time and stops (setup error) on any drift.
Usage: merge-fixtures.py OUT
"""
import json
import os
import sys

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(W, "w1", "ExecCounterC1", "c1-r48-fixtures.json")
B = os.path.join(W, "w1", "ExecFixturesV2", "fixtures-v2.json")
CLS = {"WARM-HIT-DIFFERS": "WARM-DIFFERS", "WARM-HIT-SAME": "WARM-SAME"}


def conv(c):
    c = dict(c)
    meta = c.get("meta") or {}
    c["class"] = CLS.get(c["class"], c["class"])
    st = meta.get("cache_state")
    if st:
        c["state"] = "-" if st == "error" else st
    if meta.get("cache_dir") == "home":
        c["default_cache"] = True
        c["unset"] = [k for k in c.get("unset") or [] if k != "XDG_CACHE_HOME"]
        if not c["unset"]:
            del c["unset"]
    if c.get("cold") is None:
        c.pop("cold", None)
    if c.get("cache") is None:
        c.pop("cache", None)
    if not c.get("prime"):
        c.pop("prime", None)
    return c


def main():
    a = json.load(open(A))
    for x in a:
        if x["class"] == "EDGE-HOMEUNSET" and x.get("state") == "absent":
            x["state"] = "-"      # the resolver died before the cache gate (no `paths:` debug line): unreached

    b = [conv(x) for x in json.load(open(B))]
    ids = [x["id"] for x in a + b]
    assert len(ids) == len(set(ids)), "duplicate ids"
    out = a + b
    with open(sys.argv[1], "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print("merged %d (+%d counter seat, +%d fixtures seat)" % (len(out), len(a), len(b)))


main()
