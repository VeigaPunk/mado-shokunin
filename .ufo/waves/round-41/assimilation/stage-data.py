#!/usr/bin/env python3
"""Stage the round-41 data files into a target tree (lane working tree or a scratch clone).
Usage: stage-data.py <target-root>"""
import os, re, shutil, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-41"
T = sys.argv[1]

def put(src, dst, mode=None):
    os.makedirs(os.path.dirname(os.path.join(T, dst)), exist_ok=True)
    shutil.copyfile(src, os.path.join(T, dst))
    if mode:
        os.chmod(os.path.join(T, dst), mode)

# 1. the tool (byte-identical to the v2 reference)
put(W + "/c1/ctl-ref-tool-v2.py.txt", "tools/mado-globals.py", 0o755)
# 2. the S037 receipt
put(W + "/w1/ScrEntryA/s037-installed-version.txt", ".ufo/waves/round-41/fetch/xdph-installed-version.txt")
# 3. the entry (draft A, one id per quote line fix)
e = open(W + "/w1/ScrEntryA/hyprland-focus-grab-r41.md").read()
old = "so S286's `v1.4.1` pin and the running unit are the same upstream release"
assert old in e
e = e.replace(old, "so the `v1.4.1` pin of the portal source row and the running unit are the same upstream release")
old2 = "which is exactly S284's `finish(true)` path"
assert old2 in e
e = e.replace(old2, "which is exactly the compositor's `finish(true)` path")
open(os.path.join(T, "corpus/knowledge/hyprland-focus-grab-r41.md"), "w").write(e)
# 4. the registry: rows S283-S289, S037 used-by
reg = os.path.join(T, "corpus/SOURCES.md")
lines = open(reg).read().split("\n")
rows = [l for l in open(W + "/w1/ScrRowsDraft/rows-block.txt").read().split("\n") if l.strip()]
rows = [r for r in rows if not r.startswith("| S290 ")]
assert len(rows) == 7, len(rows)
last = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", l))
for i, l in enumerate(lines):
    if re.match(r"^ {0,3}\|\s*S037\s*\|", l):
        cells = l.split("|")
        cur = cells[11].strip()
        ent = "corpus/knowledge/hyprland-focus-grab-r41.md"
        cells[11] = " " + (cur + ", " + ent if cur not in ("", "\u2014") else ent) + " "
        lines[i] = "|".join(cells)
lines[last + 1:last + 1] = rows
open(reg, "w").write("\n".join(lines))
# 5. README index row (after the r40 rows)
rd = os.path.join(T, "corpus/README.md")
r = open(rd).read().split("\n")
idx = max(i for i, l in enumerate(r) if l.startswith("| `knowledge/host-bar-producer-census-r40.md`"))
row = ("| `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1, round 41; assimilation of the focus-control theme, "
       "successor to the staged `focus-grab-protocol-live-on-host-r14` and the English-channel part of `focus-control-surfaces-r28`) "
       "| Focus as a protocol surface: the Hyprland focus-grab protocol (two interfaces, five requests, one `cleared` event), the "
       "compositor-side seat grab that enforces it, what this host advertised to its portal (63 globals in the latest portal session, "
       "one focus-grab manager advert, logged and not bound by the portal), one real client's grab lifecycle (quickshell), and the "
       "rule-level counterpart (issue 565); a decision table of what is observed, inferred and unknown. |")
r.insert(idx + 1, row)
open(rd, "w").write("\n".join(r))
# 6. the lesson
put(W + "/assimilation/round-41-lesson.md", "corpus/lessons/round-41.md")
print("staged into", T)
