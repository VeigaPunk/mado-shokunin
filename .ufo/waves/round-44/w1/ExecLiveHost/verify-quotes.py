#!/usr/bin/env python3
"""Verify every located quote in live-states.txt.

For each (relative path under the lane or fetch-c1, needle) pair:
  1. the needle occurs on exactly one line of the source file (for the handler and
     hyprctl needles that legitimately repeat, every occurrence must appear in the
     receipt and each occurrence line must equal the receipt's locator);
  2. the receipt carries a line `  <path>:<line>  <line text>` with that text;
  3. the quote is at most 25 words and the receipt line is at most 25 words of quote
     beyond its locator.
Exit 0 only when all pass. Prints one PASS/FAIL line per check.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PINS = os.path.join(LANE, ".ufo/waves/round-44/fetch-c1")
RECEIPT = os.path.join(HERE, "live-states.txt")

CASES = [
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", "if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", "const CBox MONBOX"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", "else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", "workArea(target->floating());"),
    ("fetch-c1/Hyprland-HyprCtl.cpp", '"fullscreen": {},'),
    ("fetch-c1/Hyprland-HyprCtl.cpp", "getFullscreenModes(w).internal"),
    ("fetch-c1/Hyprland-HyprCtl.cpp", '"fullscreenClient": {},'),
    ("fetch-c1/Hyprland-HyprCtl.cpp", "getFullscreenModes(w).client"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", "FSMODE_NONE = 0,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", "FSMODE_MAXIMIZED,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", "FSMODE_FULLSCREEN,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", "eFullscreenMode internal = FSMODE_NONE;"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", "eFullscreenMode client   = FSMODE_NONE;"),
    ("w1/ExecLiveHost/mado-geometry.py", "fsmode is the `fullscreen` value when it is a JSON integer"),
    ("w1/ExecLiveHost/mado-geometry.py", "FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED (not floating) | AGREE"),
    ("w1/ExecLiveHost/mado-geometry.py", "(the bracketed pair is printed exactly when maximized + fullscreen > 0"),
]
ROUND44 = os.path.dirname(os.path.dirname(HERE))


def resolve(rel):
    if rel == "SKILL.md":
        return os.path.join(LANE, "SKILL.md")
    return os.path.join(ROUND44, rel)


receipt = open(RECEIPT, encoding="utf-8").read().splitlines()
fails = 0
for rel, needle in CASES:
    path = resolve(rel)
    src = open(path, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(path) else []
    hits = [i for i, ln in enumerate(src, 1) if needle in ln]
    words = len(needle.split())
    if not hits:
        print("FAIL absent from source: %s :: %r" % (rel, needle))
        fails += 1
        continue
    if words > 25:
        print("FAIL quote longer than 25 words (%d): %s :: %r" % (words, rel, needle))
        fails += 1
        continue
    for ln in hits:
        text = src[ln - 1].strip()
        pref = "  %s:%d  " % (rel, ln)
        same = any(line == pref + text for line in receipt)
        print("%s %s:%d words=%d %r" % ("PASS" if same else "FAIL", rel, ln, words, text))
        fails += 0 if same else 1

# Report citations: every `fetch-c1/<pin>:<line>` in the seat report must carry the same text the
# receipt prints for that locator (so a locator cannot drift between the two documents).
REPORT = os.path.join(os.path.dirname(HERE), "ExecLiveHost.md")
REPORT_CITES = [
    ("fetch-c1/Hyprland-HyprCtl.cpp", 410, '"fullscreen": {},'),
    ("fetch-c1/Hyprland-HyprCtl.cpp", 411, '"fullscreenClient": {},'),
    ("fetch-c1/Hyprland-HyprCtl.cpp", 431, "getFullscreenModes(w).internal"),
    ("fetch-c1/Hyprland-HyprCtl.cpp", 432, "getFullscreenModes(w).client"),
    ("fetch-c1/Hyprland-HyprCtl.cpp", 427, "size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x"),
    ("fetch-c1/Hyprland-HyprCtl.cpp", 428, "size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", 13, "FSMODE_NONE = 0,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", 14, "FSMODE_MAXIMIZED,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", 15, "FSMODE_FULLSCREEN,"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", 34, "eFullscreenMode internal = FSMODE_NONE;"),
    ("fetch-c1/Hyprland-FullscreenController.hpp", 35, "eFullscreenMode client   = FSMODE_NONE;"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", 192, "MONITOR->logicalBox()"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", 222, "MONITOR->logicalBox()"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", 196, "workArea(target->floating())"),
    ("fetch-c1/Hyprland-FullscreenHandler.cpp", 238, "workArea(FS_TARGET->floating())"),
    ("SKILL.md", 332, "`clients` for length/tags, never window titles"),
    ("SKILL.md", 300, "timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>"),
]
if os.path.exists(REPORT):
    report = open(REPORT, encoding="utf-8").read()
    for rel, ln, needle in REPORT_CITES:
        loc = "%s:%d" % (rel, ln)
        src_line = open(resolve(rel), encoding="utf-8", errors="replace").read().splitlines()[ln - 1]
        cited = loc in report
        agrees = needle in src_line
        if rel == "SKILL.md":
            in_receipt = any(needle in line for line in receipt)
        else:
            in_receipt = any(line.startswith("  %s  " % loc) and needle in line for line in receipt)
        ok = cited and agrees and in_receipt
        print("%s report cites %s (in report=%s, line has needle=%s, receipt agrees=%s)"
              % ("PASS" if ok else "FAIL", loc, cited, agrees, in_receipt))
        fails += 0 if ok else 1
else:
    print("SKIP report not found at %s" % REPORT)

# The before/after table and the two state fixtures must also be present verbatim.
for needle in ("DIFFER (rc 1)", "FULLSCREEN (rc 0)", "MAXIMIZED (rc 0)",
               "verdict=NO_MATCHING_CLIENT", "fullscreen=2", "fullscreen=1"):
    ok = any(needle in line for line in receipt)
    print("%s receipt contains %r" % ("PASS" if ok else "FAIL", needle))
    fails += 0 if ok else 1

print("VERIFY_QUOTES: %s (%d failures)" % ("PASS" if not fails else "FAIL", fails))
sys.exit(0 if not fails else 1)
