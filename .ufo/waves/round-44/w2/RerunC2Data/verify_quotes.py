#!/usr/bin/env python3
"""Verify every literal string quoted in RerunC2Data.md against the receipt copy.

Each check names (receipt file, computed line, needle). The receipt is grepped; the
check passes only if a line in that receipt starts with the computed line number and
contains the needle. Locators were produced by grep -n, never typed.
"""
import os
import sys

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts")
CHECKS = [
    ("locators.txt", 32, "a new id's receipt must be one of",
     "counter docstring clause-d claim (c2-r44-...-v2.py:32, continues on :33)"),
    ("locators.txt", 489, "pin_ok = PINS.get(os.path.basename(path)) in (None, digest)",
     "counter :489 pin_ok accepts a basename absent from PINS"),
    ("locators.txt", 646, "bad |= not set(PINS) <= used",
     "counter :646 the only PINS guard is collective coverage"),
    ("locators.txt", 31, 'GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp',
     "lesson GATE S164 line"),
    ("locators.txt", 35, 'GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py',
     "lesson GATE S301 line"),
    ("locators.txt", 28, "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);",
     "entry line 28 carries the S164 quote"),
    ("locators.txt", 32, "hyprland sendWindowSize xdg_setSize=1 x11_configure=1",
     "census line 32"),
    ("locators.txt", 58, "gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
     "census line 58"),
    ("locators.txt", 56, "window.set_decorated(False) window.set_default_size(420, 500)",
     "entry line 56 carries the S301 quote"),
    ("locators.txt", 247, "| S298 |", "registry row S298"),
    ("locators.txt", 250, "| S301 |", "registry row S301"),
    ("locators.txt", 72, "| `knowledge/hyprland-gkeep-size-request-r44.md`", "README index row"),
    ("run1.txt", 1, "clause=c id=S164 new=0 status=mined used=1 ok=1", "counter run1 S164 clause c"),
    ("run1.txt", 1, "PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET", "counter final line (run1)"),
    ("run2.txt", 1, "PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET", "counter final line (run2)"),
    ("rederive1.txt", 1, "- S164  word-bounded occurrences=1  substring occurrences=1  start_line=1687",
     "independent quote occurrence S164"),
    ("rederive1.txt", 1, "- S299  word-bounded occurrences=1  substring occurrences=1  start_line=1150",
     "independent quote occurrence S299"),
    ("rederive1.txt", 1, "gtk-constrain gdktoplevel-wayland.c anchor_line=525 cited_range=[(50, '523', '528')",
     "surface gtk-constrain cited range"),
    ("rederive2.txt", 1, "base cells=11 cells1-9 equal=True", "held S164 cells 1-9 unchanged"),
    ("fixture-unpinned.txt", 1, "clause=d id=S302 gates=1 bound=1", "fixture: unpinned receipt bound"),
    ("fixture-unpinned.txt", 1, "PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=84153f4b",
     "fixture admitted"),
    ("fixture-diff.txt", 1, ".ufo/waves/round-44/fetch/unpinned-receipt.txt",
     "fixture added an unpinned receipt under fetch/"),
]

bad = 0
for fn, ln, needle, why in CHECKS:
    path = os.path.join(W, fn)
    text = open(path, encoding="utf-8", errors="replace").read().split("\n")
    if fn == "locators.txt":
        # receipt format is "<computed line>:<text>"; the needle must sit on that
        # computed line, wherever the receipt itself stores it
        hits = [n + 1 for n, l in enumerate(text)
                if l.startswith("%d:" % ln) and needle in l]
        ok, where = bool(hits), (hits[0] if hits else None)
    else:        # transcripts: needle may sit on any line
        hits = [n + 1 for n, l in enumerate(text) if needle in l]
        ok, where = bool(hits), (hits[0] if hits else None)
    print("%s  %-22s line %s  %s" % ("PASS" if ok else "FAIL", fn,
                                    where if where else "-", why))
    bad += 0 if ok else 1
print("verify: %d/%d ok" % (len(CHECKS) - bad, len(CHECKS)))
sys.exit(0 if bad == 0 else 1)
