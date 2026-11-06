#!/usr/bin/env python3
"""Round-90 M90-1 check: no fixture config line carries two keys.

A config fixture assembled by concatenating a host file that lacks a final
newline merges the host's last line with the appended key
(`default=hyprland;gtkorg.freedesktop.impl.portal.FileChooser=kde`).  This
check reads a case file and flags any *portals.conf line whose value contains
`org.freedesktop.impl.portal.` followed by `=` — a second key inside one value.
Usage: check-fixture-lines-r90.py CASES.json ; exit 0 clean, 1 merged lines found.
"""
import json, re, sys
MERGED = re.compile(r"^[^=]+=.*org\.freedesktop\.impl\.portal\.[A-Za-z]+=")
bad = 0
for c in json.load(open(sys.argv[1]))["cases"]:
    for path, text in c["files"].items():
        if not path.endswith("portals.conf"):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if MERGED.match(line):
                bad += 1
                print(f"merged {c['id']} {path}:{n} {line}")
print(f"FIXTURE_LINES: cases={len(json.load(open(sys.argv[1]))['cases'])} merged={bad} verdict={'CLEAN' if bad == 0 else 'MERGED'}")
sys.exit(1 if bad else 0)
