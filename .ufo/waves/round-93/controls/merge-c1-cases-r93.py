#!/usr/bin/env python3
"""Round-93 C1 (L1): merge the frozen case set.

portal-cases-r93.json = the 229 labelled round-90 cases + each labelled byte-class file given with --labelled
(written by controls/portal-oracle-r93.py from controls/portal-bytes-cases-r93-unlabelled.json and
controls/portal-review-cases-r93-unlabelled.json).  Every labelled file must carry the same oracle_binary_sha256 and
host_tail_sha256 as the round-90 file; ids must be unique.
Usage: merge-c1-cases-r93.py --r90 portal-cases-r90.json --labelled A.json --labelled B.json --out portal-cases-r93.json
"""
import argparse
import json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--r90", required=True)
    ap.add_argument("--labelled", action="append", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    r90 = json.load(open(a.r90, encoding="utf-8"))
    out = {"cases": list(r90["cases"]), "host_tail_sha256": r90["host_tail_sha256"],
           "oracle_binary_sha256": r90["oracle_binary_sha256"]}
    for p in a.labelled:
        d = json.load(open(p, encoding="utf-8"))
        for k in ("host_tail_sha256", "oracle_binary_sha256"):
            if d.get(k) != out[k]:
                raise SystemExit(f"{p}: {k} {d.get(k)} != {out[k]}")
        if any("oracle" not in c or "oracle_reason" not in c or "class" not in c for c in d["cases"]):
            raise SystemExit(f"{p}: unlabelled or unclassed case")
        out["cases"] += d["cases"]
    ids = [c["id"] for c in out["cases"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate case id")
    with open(a.out, "w", encoding="ascii") as fh:
        json.dump(out, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    by = {}
    for c in out["cases"]:
        by[c.get("class")] = by.get(c.get("class"), 0) + 1
    print("MERGE cases=%d %s" % (len(ids), " ".join(f"{k}={v}" for k, v in sorted(by.items(), key=str))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
