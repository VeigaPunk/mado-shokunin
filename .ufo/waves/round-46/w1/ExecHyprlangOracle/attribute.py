#!/usr/bin/env python3
"""Attribute every corpus divergence to one of the two mechanisms found, so the report's counts are computed.

B1 = stale currentSpecialKey retarget (a `names`/`kb_file` divergence, or a scroll divergence with no
     underflow-to-zero literal)
B2 = scroll_factor literal whose float32 is 0 while the double is not (std::stof throws out_of_range)
Usage: python3 attribute.py <scratch-dir> <oracle> <seed> <n_clean> <n_raw>
"""
import decimal
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    root, oracle, seed, nc, nr = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    sys.path.insert(0, HERE)
    import differ
    import gen

    ref = differ.load_ref()
    cases = gen.generate(seed=seed, n_clean=nc, n_raw=nr)
    os.makedirs(root, exist_ok=True)
    out = differ.run_oracle(root, oracle, cases)
    counts = {"B1": 0, "B2": 0, "both": 0, "unexplained": 0}
    details = {"B1": [], "B2": [], "both": [], "unexplained": []}
    for case in cases:
        refm = differ.ref_model(ref, case)
        if refm["unsupported"]:
            continue
        diffs = differ.compare(refm, out[case["id"]])
        if not diffs:
            continue
        kinds = {d[0] for d in diffs}
        text = "\n".join(case["files"])
        tiny = False
        for m in re.finditer(r"scroll_factor\s*=\s*([^\s#]+)", text):
            kind, v = ref.read_float(m.group(1))
            if kind == "ok" and v == 0.0:
                try:
                    literal = decimal.Decimal(ref.FLOAT_RE.match(m.group(1)).group(0))
                except (decimal.InvalidOperation, AttributeError):
                    continue
                if literal != 0:
                    tiny = True
        other = kinds - {"scroll"}
        if other:
            key = "B1" if not tiny else "both"
        elif tiny:
            key = "B2"
        else:
            key = "B1" if re.search(r"^\s*(unknown_key|nope)\s*=", text, re.M) else "unexplained"
        counts[key] += 1
        if len(details[key]) < 3:
            details[key].append({"id": case["id"], "kinds": sorted(kinds), "files": case["files"],
                                 "diff": [list(d) for d in diffs]})
    print("corpus seed=%d clean=%d raw=%d -> %s" % (seed, nc, nr, counts))
    for k, v in details.items():
        for it in v:
            print(" ", k, it["id"], it["kinds"], it["diff"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
