#!/usr/bin/env python3
"""Locate every quote used by report.md at its source file:line and assert the report carries it.

Read-only. Run from this seat directory:
  python3 -I quote-check.py            # prints one PASS/FAIL line per quote, summary last
Exit 0 only when every quote is found both at the source line and in report.md.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = f"{LANE}/.ufo/waves/round-46/fetch"
DRAFT = f"{LANE}/.ufo/waves/round-46/l1-draft"

# (source path, 1-based line, exact quote) - locators were produced by grep -n, not typed
QUOTES = [
    (f"{DRAFT}/entry.md", 68, "The XKB compile itself is not reproduced"),
    (f"{DRAFT}/entry.md", 24, "the compile failure itself is not observed here"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 87, "if (!m_xkbFilePath.empty()) {"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 98, "if (!m_xkbKeymap)"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 101, "if (!m_xkbKeymap) {"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 107, "memset(&XKBRULES, 0, sizeof(XKBRULES));"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 113, 'm_currentRules.layout  = "us";'),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 61, "if (m_keymapOverridden) {"),
    (f"{FETCH}/Hyprland-IKeyboard.cpp", 313, "const auto LAYOUTNAME = xkb_keymap_layout_get_name(KEYMAP, i);"),
    (f"{FETCH}/Hyprland-HyprCtl.cpp", 783, "const auto KM        = k->getActiveLayout();"),
    (f"{FETCH}/Hyprland-HyprCtl.cpp", 794, '"active_keymap": "{}",'),
    (f"{FETCH}/Hyprland-VirtualKeyboard.cpp", 41, "m_keymapOverridden = true;"),
]

WORDS = re.compile(r"\S+")


def main():
    report = open("report.md", encoding="utf-8").read()
    bad = 0
    for path, line, quote in QUOTES:
        try:
            lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
        except OSError as e:
            print(f"QUOTE: FAIL {os.path.basename(path)}:{line} unreadable ({e.__class__.__name__})")
            bad += 1
            continue
        at_source = 0 <= line - 1 < len(lines) and quote in lines[line - 1]
        in_report = quote in report
        nwords = len(WORDS.findall(quote))
        ok = at_source and in_report and nwords <= 25
        bad += 0 if ok else 1
        print(
            f"QUOTE: {'PASS' if ok else 'FAIL'} {os.path.basename(path)}:{line} words={nwords} "
            f"at_source={at_source} in_report={in_report} :: {quote}"
        )
    print(f"QUOTE: quotes={len(QUOTES)} failures={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
