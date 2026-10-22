#!/usr/bin/env python3
"""Round-23 C3 counter: SHONEN self-assessment versus observed repo state.

Usage: python3 -I count.py REV   (reads committed bytes only, via git)

SHONEN.md box 4 is the lane's self-assessment "No cross-domain bleed
(PROVINCE.md still accurate)". Observed repo state: the tracked lane tools
(tools/*.py and tools/*.sh at REV). Each tracked tool whose file name does not
appear in PROVINCE.md at REV is one mismatch between that self-assessment row
and the repo: the lane owns and runs a tool its province declaration does not
account for. If box 4 is absent or no longer asserts PROVINCE accuracy, the
counter cannot evaluate (exit 2). Prints JSON; exit 0 at 0 mismatches, 1 above.
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
        raise SystemExit(json.dumps({"error": "git " + " ".join(args) + " failed"}))
    return proc.stdout


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
    province = git("show", f"{rev}:PROVINCE.md")
    tools = sorted(p for p in git("ls-tree", "--name-only", rev, "tools/").split()
                   if re.search(r"\.(py|sh)$", p))
    mismatches = [p for p in tools if Path(p).name not in province]
    print(json.dumps({"rev": rev, "self_assessment": box[0], "tracked_tools": tools,
                      "mismatches": mismatches, "count": len(mismatches)}, indent=1))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
