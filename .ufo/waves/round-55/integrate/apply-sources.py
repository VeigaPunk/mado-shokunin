#!/usr/bin/env python3
"""L1 integration (round 55): append rows S378-S380 (from the R55ScribeSources draft, each quote re-opened by the L1 against
the committed pins), add the entry to the used-by cell of S052/S316/S317/S318/S319, append the round-55 search-log note.
Prints every in-place change old->new for the lesson. Run from the lane root."""
import re
P = "corpus/SOURCES.md"
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
lines = open(P).read().split("\n")
rows = [l for l in open(".ufo/waves/round-55/w1/R55ScribeSources/rows.md").read().split("\n") if re.match(r"\| S3[78]\d \|", l)]
assert len(rows) == 3 and all(len(r.strip().strip("|").split("|")) == 11 for r in rows), rows
i = max(n for n, l in enumerate(lines) if re.match(r"\| S377 \|", l))
lines[i + 1:i + 1] = rows
for n, l in enumerate(lines):
    m = re.match(r"\| (S052|S316|S317|S318|S319) \|", l)
    if m:
        cells = l.split("|")  # ['', id, ..., usedby, '']
        old = cells[-2].strip()
        if ENTRY not in old:
            cells[-2] = " " + (old + ", " + ENTRY if old and old != "—" else ENTRY) + " "
            lines[n] = "|".join(cells)
            print("used-by %s: %s -> %s" % (m.group(1), old, cells[-2].strip()))
log = open(".ufo/waves/round-55/w1/R55ScribeSources/search-log.md").read().strip()
txt = "\n".join(lines).rstrip("\n") + "\n\n" + log + "\n"
open(P, "w").write(txt)
