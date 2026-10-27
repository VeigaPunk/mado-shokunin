#!/usr/bin/env python3
"""N4 check: the full text matrix must carry exactly one row per variant recorded in summary.json.

Assertions (every one is fatal, all failures are printed):
  1. row count is 98 and equals len(summary)
  2. the row-name set equals the summary name set, with no duplicate names
  3. every row's declared / rc / last equals the summary record for that name
  4. row order equals summary.json order
  5. the footer says `rows 98`
  6. the two rows the frozen text dropped (a-rev-base-direct, a-entry-at-base) are present
  7. with --frozen: the frozen text has 96 rows and its missing set is exactly those two names

Read-only; nothing is written. Exit 0 = all assertions hold, 1 = at least one failed.
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROW = re.compile(r"^(\S+)\s+(\S+)\s+rc=(\d+)\s+(.*)$")
RECOVERED = ("a-rev-base-direct", "a-entry-at-base")
EXPECT = 98


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_rows(path):
    rows, footer = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#"):
                continue
            m = ROW.match(line)
            if m and not line.startswith("rows "):
                rows.append({"name": m.group(1), "declared": m.group(2),
                             "rc": int(m.group(3)), "last": m.group(4)})
            elif line.startswith("rows "):
                footer = line
    return rows, footer


def frozen_names(path):
    names = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("pos rc "):
                names.append("pos")
                continue
            m = ROW.match(line.rstrip("\n"))
            if m:
                names.append(m.group(1))
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--matrix", default=os.path.join(HERE, "c2v2-matrix-full.txt"))
    ap.add_argument("--summary", default=os.path.join(HERE, "source-summary.json"))
    ap.add_argument("--frozen", default="",
                    help="frozen round-48 matrix.txt, to re-assert the 96-of-98 claim")
    a = ap.parse_args()

    with open(a.summary, encoding="utf-8") as f:
        summ = json.load(f)
    want = {r["name"]: r for r in summ}
    rows, footer = parse_rows(a.matrix)
    fails = []

    def check(label, ok, detail=""):
        print("%-34s %s%s" % (label, "PASS" if ok else "FAIL", (" " + detail) if detail else ""))
        if not ok:
            fails.append(label)

    print("matrix  %s sha256=%s" % (os.path.basename(a.matrix), sha256(a.matrix)))
    print("summary %s sha256=%s" % (os.path.basename(a.summary), sha256(a.summary)))
    check("row_count_98", len(rows) == EXPECT == len(summ), "rows=%d summary=%d" % (len(rows), len(summ)))

    got = [r["name"] for r in rows]
    dupes = sorted({n for n in got if got.count(n) > 1})
    check("set_equality_summary", set(got) == set(want), "matrix=%d summary=%d" % (len(set(got)), len(want)))
    check("no_duplicate_names", not dupes, ",".join(dupes) or "none")
    check("order_equals_summary", got == [r["name"] for r in summ])
    check("footer_rows_98", footer == "rows %d" % EXPECT, repr(footer))
    check("recovered_present", all(n in want and n in set(got) for n in RECOVERED),
          ",".join(n for n in RECOVERED if n in set(got)))

    bad = []
    for r in rows:
        s = want.get(r["name"])
        if s is None:
            bad.append("%s:not_in_summary" % r["name"])
            continue
        if r["declared"] != s["declared"]:
            bad.append("%s:declared %r!=%r" % (r["name"], r["declared"], s["declared"]))
        if r["rc"] != s["rc"]:
            bad.append("%s:rc %r!=%r" % (r["name"], r["rc"], s["rc"]))
        if r["last"] != s["last"]:
            bad.append("%s:last differs" % r["name"])
    check("row_values_match_summary", not bad, "; ".join(bad[:4]) + (" ..." if len(bad) > 4 else ""))

    if a.frozen:
        fz = frozen_names(a.frozen)
        missing = [n for n in want if n not in set(fz)]
        check("frozen_96_rows", len(fz) == 96 and len(set(fz)) == 96, "rows=%d" % len(fz))
        check("frozen_missing_two", sorted(missing) == sorted(RECOVERED), ",".join(sorted(missing)))
        pos_frozen = ""
        with open(a.frozen, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("pos rc "):
                    pos_frozen = line.rstrip("\n")
        check("frozen_pos_is_clauses",
              pos_frozen == "pos rc 0 " + want["pos"]["clauses"],
              "frozen pos line = print site 412, the clauses projection")
        print("frozen_sha256                    %s" % sha256(a.frozen))

    print("RESULT %s failures=%d" % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
