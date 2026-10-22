#!/usr/bin/env python3
"""Round-23 C2 counter: sourced route rows for the foot, kitty and ghostty trees.

Usage: python3 -I count.py REV   (reads committed bytes only, via git show)

A terminal counts when corpus/knowledge/terminal-trees-r23.md at REV holds a
Markdown table row whose first cell names the terminal and whose cells cite an
S### token that resolves to a corpus/SOURCES.md registry row with status
`mined`, opened `2026-10-22`, and a source cell naming the same terminal.
Prints JSON; exit 0 when 3/3, 1 otherwise, 2 on usage or git error.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[4]
NOTE = "corpus/knowledge/terminal-trees-r23.md"
TERMINALS = ("foot", "kitty", "ghostty")


def show(rev, path):
    proc = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    rev = argv[1]
    sources = show(rev, "corpus/SOURCES.md")
    if sources is None:
        print(json.dumps({"error": "SOURCES.md unreadable at " + rev}))
        return 2
    registry = {}
    for line in sources.splitlines():
        if re.match(r"^\| S\d{3} \|", line):
            row = cells(line)
            if len(row) == 11:
                registry[row[0]] = {"source": row[1].lower(), "status": row[7], "opened": row[8]}
    note = show(rev, NOTE)
    result = {"rev": rev, "note_present": note is not None, "terminals": {}}
    for term in TERMINALS:
        ok = []
        for line in (note or "").splitlines():
            if not line.startswith("|"):
                continue
            row = cells(line)
            if not row or not re.fullmatch(rf"`?{term}`?", row[0].lower()):
                continue
            for sid in re.findall(r"S\d{3}", line):
                src = registry.get(sid)
                if src and src["status"] == "mined" and src["opened"] == "2026-10-22" \
                        and term in src["source"]:
                    ok.append(sid)
        result["terminals"][term] = sorted(set(ok))
    count = sum(1 for v in result["terminals"].values() if v)
    result["count"] = f"{count}/{len(TERMINALS)}"
    print(json.dumps(result, indent=1))
    return 0 if count == len(TERMINALS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
