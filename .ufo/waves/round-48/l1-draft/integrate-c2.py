#!/usr/bin/env python3
"""L1-only C2 integration helper, run once after the pre-data freeze: append rows, entry, README and Frontier update.
All sources/pins/receipts have already been opened/measured this round; this script only integrates the reviewed bytes."""
import os

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = L + "/.ufo/waves/round-48"
ENTRY = "xkb-keymap-compile-r48.md"

# Append only the newly opened rows immediately after S339; do not rewrite held rows.
p = L + "/corpus/SOURCES.md"
s = open(p).read().splitlines()
if not any(x.startswith("| S340 |") for x in s):
    i = max(i for i, x in enumerate(s) if x.startswith("| S339 |"))
    s[i + 1:i + 1] = open(W + "/l1-draft/rows-c2.md").read().rstrip("\n").splitlines()
    open(p, "w").write("\n".join(s) + "\n")

# Land entry and README index row.
import shutil
shutil.copyfile(W + "/l1-draft/" + ENTRY, L + "/corpus/knowledge/" + ENTRY)
p = L + "/corpus/README.md"
s = open(p).read().splitlines()
if not any("knowledge/" + ENTRY in x for x in s):
    i = max(i for i, x in enumerate(s) if x.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
    s.insert(i + 1, open(W + "/l1-draft/readme-row.md").read().rstrip("\n"))
open(p, "w").write("\n".join(s) + "\n")

# Append this round's frontier observation immediately after the r47 row; prior observations stay historical.
p = L + "/corpus/README.md"
s = open(p).read().splitlines()
line = ("- Round 48 moves the input-device XKB **compile** itself onto sourced ground ([XKB keymap compile](knowledge/" + ENTRY + "), "
        "rows S340-S350): libxkbcommon 1.13.2 and xkeyboard-config 2.48 rule resolution, include order, failure versus dropped names, "
        "and this host's `br` + `compose:caps` compile. It cites the held S318/S319 Hyprland fallback without re-claiming it. "
        "The compositor's live context/environment and `kb_file` remain outside this measurement.")
if line not in s:
    i = max(i for i, x in enumerate(s) if x.startswith("- Round 47 moves the P4 terminal-selection route"))
    s.insert(i + 1, line)
open(p, "w").write("\n".join(s) + "\n")
print("C2 integrated: entry, 11 rows, README index + Frontier")
