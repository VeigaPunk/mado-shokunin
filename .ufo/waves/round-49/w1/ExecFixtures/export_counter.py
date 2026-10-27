#!/usr/bin/env python3
"""Derive the C1 counter's fixture view from fixtures.json.

`fixtures.json` (the wave deliverable) keeps `expect = {stdout, rc}`. The C1
counter seat's `c1-r49-keysym.py` accepts an installed fixture file only with
the flat shape `{id, class, rmlvo, arg, rc, sha256}` and identical key sets, so
this emits that view: same pairs, same judge bytes, stdout folded to a digest.

Usage: export_counter.py --fixtures fixtures.json --out fixtures-counter.json
"""
import argparse
import hashlib
import json
import sys

KEYS = ["rules", "model", "layout", "variant", "options"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    src = json.load(open(a.fixtures, encoding="utf-8"))
    out = []
    for f in src:
        if set(f) != {"id", "class", "rmlvo", "arg", "expect"}:
            sys.exit("unexpected fixture keys: %r" % sorted(f))
        if set(f["rmlvo"]) != set(KEYS):
            sys.exit("%s: rmlvo keys %r" % (f["id"], sorted(f["rmlvo"])))
        blob = f["expect"]["stdout"].encode("utf-8")
        if f["expect"]["rc"] != 0 and blob:
            sys.exit("%s: non-zero rc with stdout" % f["id"])
        out.append({"id": f["id"], "class": f["class"], "rmlvo": f["rmlvo"],
                    "arg": f["arg"], "rc": f["expect"]["rc"],
                    "sha256": hashlib.sha256(blob).hexdigest()})
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("cases=%d sha256=%s" % (len(out), hashlib.sha256(open(a.out, "rb").read()).hexdigest()))


if __name__ == "__main__":
    main()
