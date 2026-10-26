#!/usr/bin/env python3
"""ExecFixtureMap: every number the seat report cites, recomputed from the trace record.

Reads out/lines.json (map-fixtures.py) and prints: sweep sizes, drift, traced-line count,
per-case distribution, variant A vs B unions, per-function entered/reached/missed counts, and a
full per-line table (hits, cases, source text). Deterministic; no scratch, no writes.

Usage: stats.py --lines out/lines.json --script <pin>
"""
import argparse
import json
import re
import statistics
import sys

sys.dont_write_bytecode = True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", required=True)
    ap.add_argument("--script", required=True)
    a = ap.parse_args()
    rec = json.load(open(a.lines))
    counts = {int(k): v for k, v in rec["counts"].items()}
    per_case = rec["per_case"]
    src = open(a.script, encoding="utf-8", errors="surrogateescape").read().split("\n")
    txt = "\n".join(src)
    print("fixtures_sha256=%s" % rec["fixtures_sha256"])
    print("pin_sha256=%s" % rec["pin_sha256"])
    print("variants=%s cases=%d runs=%d" % ("".join(rec["variants"]), rec["n_cases"], len(per_case)))
    print("source_lines=%d traced_lines=%d (%.1f%%) never_traced=%d"
          % (len(src) - 1, len(counts), 100.0 * len(counts) / (len(src) - 1),
             len(src) - 1 - len(counts)))
    print("drift_against_recorded_expect=%r" % (rec["drift"],))
    n = [len(v["lines"]) for v in per_case.values()]
    print("per-run distinct lines: min=%d median=%d mean=%.1f max=%d"
          % (min(n), statistics.median(n), statistics.mean(n), max(n)))
    A = {k: v for k, v in per_case.items() if k.endswith("/A")}
    B = {k: v for k, v in per_case.items() if k.endswith("/B")}

    def union(x):
        s = set()
        for v in x.values():
            s |= set(v["lines"])
        return s
    ua, ub = union(A), union(B)
    print("union A=%d union B=%d A_only=%r B_only=%r"
          % (len(ua), len(ub), sorted(ua - ub), sorted(ub - ua)))
    print("lines traced in every one of the %d runs: %d"
          % (len(per_case), sum(1 for v in counts.values() if v == len(per_case))))
    print("lines traced in exactly one run: %r"
          % sorted(i for i, v in counts.items() if v == 1))
    print()
    fnl = [(txt[:m.start()].count("\n") + 1, m.group(1))
           for m in re.finditer(r"(?m)^([a-zA-Z_][a-zA-Z_0-9]*)\(\) \{", txt)]
    print("function                 range      stmt  seen  missed")
    for k, (ln, name) in enumerate(fnl):
        if k + 1 < len(fnl):
            end = fnl[k + 1][0] - 1
        else:
            end = next(i for i in range(ln + 1, len(src)) if src[i - 1] == "}")
        body = [i for i in range(ln + 1, end + 1)
                if src[i - 1].strip() and not src[i - 1].strip().startswith("#")]
        seen = [i for i in body if i in counts]
        print("%-22s %4d-%-4d %5d %5d %7d%s" % (name, ln, end, len(body), len(seen),
                                                len(body) - len(seen),
                                                "" if seen else "  NEVER-ENTERED"))
    top = [i for i in range(fnl[-1][0] + 1, len(src))
           if src[i - 1].strip() and not src[i - 1].strip().startswith("#")]
    seen = [i for i in top if i in counts]
    print("%-22s %4d-%-4d %5d %5d %7d" % ("<toplevel>", 1133, len(src) - 1, len(top),
                                          len(seen), len(top) - len(seen)))
    print()
    print("per-line table: line hits cases | text")
    for i in range(1, len(src)):
        print("%4d %5d %5d | %s" % (i, counts.get(i, 0),
                                    sum(1 for v in per_case.values() if i in v["lines"]),
                                    src[i - 1].rstrip()[:110]))


if __name__ == "__main__":
    main()
