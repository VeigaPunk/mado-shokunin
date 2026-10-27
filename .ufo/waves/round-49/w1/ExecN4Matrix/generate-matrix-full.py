#!/usr/bin/env python3
"""N4: regenerate the complete 98-row text matrix of the round-48 C2 v2 counter from its committed summary.

Why this exists
---------------
The frozen stdout receipt `.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-matrix.txt` carries 96 of the 98
rows that `c2v2-revc2counter-summary.json` records. The generator
`.ufo/waves/round-48/l1-draft/v2/c2v2-harness-revc2counter.py` prints one line for `pos` (line 412) and one line
per mutated variant (line 429, `last` truncated to 96 chars); the two base-scoring rows are only handed to
`record()` (lines 415 and 417) and are never printed. This script re-derives the text matrix from summary.json
alone, so the two rows are restored without touching any frozen file.

Inputs are read-only. Output defaults to `c2v2-matrix-full.txt` beside this script.

Row format is the harness's own (line 429), with `last` NOT truncated:
    "%-28s %s rc=%d %s" % (name, declared, rc, last)
Row order follows summary.json order (pos, the two base rows, then the 95 mutated variants).
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROW = re.compile(r"^(\S+)\s+(\S+)\s+rc=(\d+)\s+(.*)$")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def row_line(r):
    return "%-28s %s rc=%d %s" % (r["name"], r["declared"], r["rc"], r["last"])


def frozen_rows(path):
    """Names the frozen text matrix actually carries (same shape as row_line, plus the `pos` line)."""
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
    ap.add_argument("--summary", default=os.path.join(HERE, "source-summary.json"),
                    help="c2v2-revc2counter-summary.json (default: the byte snapshot in this seat dir)")
    ap.add_argument("--frozen", default="",
                    help="optional frozen matrix.txt, to record which rows it is missing")
    ap.add_argument("--out", default=os.path.join(HERE, "c2v2-matrix-full.txt"))
    a = ap.parse_args()

    with open(a.summary, encoding="utf-8") as f:
        rows = json.load(f)
    names = [r["name"] for r in rows]
    dupes = sorted({n for n in names if names.count(n) > 1})

    out = []
    out.append("# c2v2-matrix-full.txt - complete text matrix of the round-48 C2 v2 counter (N4).")
    out.append("# Derived from the committed summary only; no frozen file was read for row values.")
    out.append("# summary: %s sha256=%s rows=%d" % (os.path.basename(a.summary), sha256(a.summary), len(rows)))
    out.append("# derived by: .ufo/waves/round-49/w1/ExecN4Matrix/generate-matrix-full.py sha256=%s"
               % sha256(os.path.abspath(__file__)))
    out.append("# generator that wrote the frozen receipt: "
               ".ufo/waves/round-48/l1-draft/v2/c2v2-harness-revc2counter.py")
    out.append("# row shape: \"%-28s %s rc=%d %s\" (harness line 429), last untruncated")
    out.append("# duplicate names: %s" % (dupes or "none"))
    if a.frozen:
        fz = frozen_rows(a.frozen)
        missing = [n for n in names if n not in set(fz)]
        out.append("# frozen text: %s sha256=%s rows=%d missing=%s"
                   % (os.path.basename(a.frozen), sha256(a.frozen), len(fz), ",".join(missing) or "none"))
    out.append("#")
    for r in rows:
        out.append(row_line(r))
    out.append("rows %d" % len(rows))
    out.append("#")
    out.append("# Recovered rows (present in summary.json, absent from the frozen text; the harness never")
    out.append("# printed them - record() only, lines 415 and 417 of the generator):")
    if a.frozen:
        pos_frozen = ""
        with open(a.frozen, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("pos rc "):
                    pos_frozen = line.rstrip("\n")
        out.append("# Frozen `pos` line (harness line 412 prints the clauses field, a different projection from")
        out.append("# the row shape; this receipt normalizes every row onto summary.json `last`):")
        out.append("#   %s" % pos_frozen)
    recovered = []
    if a.frozen:
        present = set(frozen_rows(a.frozen))
        recovered = [r for r in rows if r["name"] not in present]
        for r in recovered:
            out.append("#   name=%s declared=%s rc=%d rev=%s note=%r fails=%d"
                       % (r["name"], r["declared"], r["rc"], r["rev"], r["note"], len(r["fails"])))
            out.append("#     last: %s" % r["last"])
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote %s rows=%d recovered=%s"
          % (a.out, len(rows), ",".join(r["name"] for r in recovered) or "n/a"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
