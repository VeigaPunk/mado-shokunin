#!/usr/bin/env python3
"""RerunCensus — verify every quote used in the seat report.

Each item is (rev-path, line, exact substring).  The line number is the one the
report cites; the substring must occur on that line of the blob at the data
commit, and the report's locator is therefore computed-and-checked, not typed.
Read-only: `git show <rev>:<path>`.
"""
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "e46789213830597348fe96a351ae004d10587385"

ITEMS = [
    ("corpus/lessons/round-44.md", 24,
     "the registry tops at `S297` (234 rows at base)"),
    ("corpus/lessons/round-44.md", 80,
     "one item appended; cells 1-10"),
    ("SCORECARD.md", 2583,
     "Sources 234 -> 238 rows (S298-S301, tier A, `mined`, opened 2026-10-26)"),
    ("corpus/SOURCES.md", 248,
     "xdg-shell.xml:560-590 xdg_surface request ack_configure"),
    ("corpus/SOURCES.md", 249,
     "gdktoplevel-wayland.c:606-700 handle_configure"),
    ("corpus/README.md", 72,
     "S164, S298, S299, S300, S301"),
]


def blob(path):
    return subprocess.check_output(
        ["git", "-C", LANE, "show", f"{REV}:{path}"], text=True
    ).splitlines()


def main():
    fail = 0
    by_path = {}
    for path, line, frag in ITEMS:
        lines = by_path.setdefault(path, blob(path))
        n = len(frag.split())
        assert n <= 25, (path, line, n)
        if line > len(lines):
            print(f"FAIL {path}:{line} past EOF ({len(lines)} lines)")
            fail += 1
            continue
        if frag in lines[line - 1]:
            total = sum(frag in ln for ln in lines)
            print(f"PASS {path}:{line} words={n} occurrences_in_file={total} :: {frag}")
        else:
            print(f"FAIL {path}:{line} :: {frag}")
            fail += 1
    print(f"QUOTES: {'PASS' if fail == 0 else 'FAIL'} ({len(ITEMS) - fail} of {len(ITEMS)})")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
