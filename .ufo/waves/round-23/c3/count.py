#!/usr/bin/env python3
"""Round-23 C3 counter: SHONEN self-assessment versus observed repo state.

Usage: python3 -I count.py REV   (reads committed bytes only, via git)

SHONEN.md box 4 is the lane's self-assessment "No cross-domain bleed
(PROVINCE.md still accurate)". Observed repo state: the tracked lane tools
(every tools/**.py and tools/**.sh at REV). While box 4 is asserted ([~] or
[x]), each tracked tool that PROVINCE.md does not account for is one mismatch
between that self-assessment row and the repo.

A tool is accounted for only by a Markdown table row in PROVINCE.md whose
first cell names the tool's repo path in backticks and which has at least four
non-empty cells (tool, what it reads, what it writes, owner and adjacent
lanes). A bare mention in prose does not count. The pre-existing gate
`tools/mado-verify.sh` is held to the same rule.

Exit 0 at 0 mismatches, 1 above 0, 2 when the counter cannot evaluate (git
error, box 4 absent, or box 4 unticked so nothing is asserted).
Version 2 (tightened before any after-measurement; v1 is in lane history at
a28e4815 and counted bare filename mentions).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[4]


def git(*args):
    proc = subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        print(json.dumps({"error": "git " + " ".join(args) + " failed"}))
        raise SystemExit(2)
    return proc.stdout


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    rev = argv[1]
    shonen = git("show", f"{rev}:SHONEN.md")
    box = [line for line in shonen.splitlines()
           if re.match(r"^- \[[ x~]\] ", line) and "PROVINCE.md still accurate" in line]
    if len(box) != 1:
        print(json.dumps({"rev": rev, "error": "SHONEN box 4 self-assessment not found"}))
        return 2
    if box[0].startswith("- [ ]"):
        print(json.dumps({"rev": rev, "error": "SHONEN box 4 is unticked; nothing asserted"}))
        return 2
    province = git("show", f"{rev}:PROVINCE.md")
    accounted = set()
    for line in province.splitlines():
        if not line.startswith("|"):
            continue
        row = cells(line)
        if len(row) >= 4 and all(row[:4]):
            match = re.fullmatch(r"`(tools/[^`]+)`", row[0])
            if match:
                accounted.add(match.group(1))
    tools = sorted(p for p in git("ls-tree", "-r", "--name-only", rev, "tools/").split()
                   if re.search(r"\.(py|sh)$", p))
    mismatches = [p for p in tools if p not in accounted]
    print(json.dumps({"rev": rev, "counter_version": 2, "self_assessment": box[0],
                      "tracked_tools": tools, "accounted_rows": sorted(accounted),
                      "mismatches": mismatches, "count": len(mismatches)}, indent=1))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
