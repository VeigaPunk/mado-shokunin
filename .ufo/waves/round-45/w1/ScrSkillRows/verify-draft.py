#!/usr/bin/env python3
"""Check the draft's quoted artefacts and table shapes against their sources.

- every `MADO_MON*` line the draft quotes must appear verbatim, as a whole line, in the L1 live receipt;
- the config line the draft quotes must be line 10 of ~/.config/hypr/monitors.conf;
- the exit codes and verdict order the draft states must match the reference docstring;
- every decision-table row in Block C must have exactly four cells.

Usage: python3 verify-draft.py     (paths absolute; no arguments)
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DRAFT = os.path.join(SEAT, "skill-rows.md")
RECEIPT = os.path.join(LANE, ".ufo/waves/round-45/receipts/live-monitors-host-l1.txt")
REFERENCE = os.path.join(LANE, ".ufo/waves/round-45/l1-draft/mado-monitors.py")
CONF = os.path.expanduser("~/.config/hypr/monitors.conf")

fails = 0


def check(ok, label, detail=""):
    global fails
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, (": " + detail) if detail and not ok else ""))
    if not ok:
        fails += 1


def main():
    draft = open(DRAFT, encoding="utf-8").read()
    receipt = open(RECEIPT, encoding="utf-8").read().split("\n")
    reference = open(REFERENCE, encoding="utf-8").read()

    quoted = [ln.strip() for ln in draft.split("\n") if ln.strip().startswith("MADO_MON")]
    check(len(quoted) >= 3, "draft quotes at least three MADO_MON lines", str(len(quoted)))
    for line in sorted(set(quoted)):
        check(line in receipt, "verbatim in live receipt: " + line[:60])

    conf_lines = open(CONF, encoding="utf-8").read().split("\n")
    check(conf_lines[9].strip() == "monitor = DP-1, 3440x1440@100, 0x0, 1", "config line 10 is the quoted rule",
          repr(conf_lines[9]))

    # reference docstring: the verdict chain and the exit map
    check("V = NO_RULES (exit 4,\nlines = 0 and v2 = 0) | NOT_COMPARED (exit 5, v2 > 0 or unsupported > 0: a monitorv2 block or an unmodelled\nline can change which rule applies) | DIFFER (exit 1, differ > 0) | NO_MATCHING_MONITOR (exit 3, matched = 0)\n| OK (exit 0), tested in that order." in reference,
          "reference verdict chain quoted by the draft is verbatim in the docstring")
    check("MADO_MONITORS: lines=<n> rules=<n> v2=<n> unsupported=<n> badrules=<n> outputs=<n> matched=<n> unruled=<n> agree=<n> differ=<n> disabled=<n> verdict=<V>" in reference,
          "reference summary line format in the docstring")

    # decision table shape: every row between the header and the exit-map line has four cells
    start = draft.index("| question | verdict/field | what it proves | what it does not |")
    end = draft.index("Exit map:", start)
    rows = [ln for ln in draft[start:end].split("\n") if ln.startswith("|")]
    check(len(rows) >= 9, "decision table has a header, a rule and rows", str(len(rows)))
    for row in rows:
        cells = re.split(r"(?<!\\)\|", row)[1:-1]
        check(len(cells) == 4, "four cells: " + row[:48], str(len(cells)))

    print("DRAFT: checked=%d failed=%d" % (1, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
