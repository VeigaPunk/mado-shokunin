#!/usr/bin/env python3
"""Round-23 C2 counter: sourced route rows for the foot, kitty and ghostty trees.

Usage: python3 -I count.py REV   (reads committed bytes only, via git show)

A terminal T counts when corpus/knowledge/terminal-trees-r23.md at REV holds a
Markdown table row whose first cell is exactly T (optionally in backticks),
which contains a cell naming the host tree `~/.config/T/`, and which cites an
S### token that resolves to a corpus/SOURCES.md registry row (11 cells) with:
status `mined`; opened `2026-10-22`; a source cell that names T as a whole
word, names no other of the three terminals, and points at T's upstream
(foot: codeberg.org/dnkl/foot; kitty: github.com/kovidgoyal/kitty or
sw.kovidgoyal.net/kitty; ghostty: ghostty.org or github.com/ghostty-org/ghostty);
and a used-by cell naming corpus/knowledge/terminal-trees-r23.md.
Prints JSON; exit 0 when 3/3, 1 otherwise, 2 on usage or git error.
Version 2 (tightened before any after-measurement; v1 is in lane history at
6b383c46 and accepted substring matches such as 'Footnotes').
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[4]
NOTE = "corpus/knowledge/terminal-trees-r23.md"
TERMINALS = ("foot", "kitty", "ghostty")
UPSTREAM = {
    "foot": ("codeberg.org/dnkl/foot",),
    "kitty": ("github.com/kovidgoyal/kitty", "sw.kovidgoyal.net/kitty"),
    "ghostty": ("ghostty.org", "github.com/ghostty-org/ghostty"),
}


def show(rev, path, required=False):
    proc = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        if required:
            print(json.dumps({"error": f"{path} unreadable at {rev}"}))
            raise SystemExit(2)
        return None
    return proc.stdout


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def names(text, term):
    return re.search(rf"(?<![a-z0-9]){term}(?![a-z0-9])", text) is not None


def source_ok(src, term):
    text = src["source"].lower()
    return (src["status"] == "mined" and src["opened"] == "2026-10-22"
            and names(text, term)
            and not any(names(text, other) for other in TERMINALS if other != term)
            and any(u in text for u in UPSTREAM[term])
            and NOTE in src["used_by"])


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    rev = argv[1]
    sources = show(rev, "corpus/SOURCES.md", required=True)
    registry = {}
    for line in sources.splitlines():
        if re.match(r"^\| S\d{3} \|", line):
            row = cells(line)
            if len(row) == 11:
                registry[row[0]] = {"source": row[1], "status": row[7],
                                    "opened": row[8], "used_by": row[10]}
    note = show(rev, NOTE)
    result = {"rev": rev, "counter_version": 2, "note_present": note is not None,
              "terminals": {}}
    for term in TERMINALS:
        ok = []
        for line in (note or "").splitlines():
            if not line.startswith("|"):
                continue
            row = cells(line)
            if not row or not re.fullmatch(rf"`?{term}`?", row[0].lower()):
                continue
            if not any(f"~/.config/{term}/" in cell for cell in row[1:]):
                continue
            for sid in re.findall(r"S\d{3}", line):
                src = registry.get(sid)
                if src and source_ok(src, term):
                    ok.append(sid)
        result["terminals"][term] = sorted(set(ok))
    count = sum(1 for v in result["terminals"].values() if v)
    result["count"] = f"{count}/{len(TERMINALS)}"
    print(json.dumps(result, indent=1))
    return 0 if count == len(TERMINALS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
