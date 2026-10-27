#!/usr/bin/env python3
"""check-quotes.py - verify every quote/locator cited by the seat report
against the pinned files in this seat dir (and the host files named in the
report).  Prints `PASS <file>:<line> <quote>` / `FAIL ...`; exit 1 on any FAIL.

Usage: python3 check-quotes.py > receipts/quote-check.txt
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CHECKS = [
    # parse semantics (findings F1/F2/F3)
    ("xkbcommon-symbols.c", 842, "/* Drop trailing NoSymbol */"),
    ("xkbcommon-symbols.c", 846, "if (nonEmptyLevels < nLevels)"),
    ("xkbcommon-symbols.c", 1782, "darray_resize0(groupi->levels, type->num_levels);"),
    ("xkbcommon-symbols.c", 1594, "FindAutomaticType(struct xkb_context *ctx, GroupInfo *groupi)"),
    ("xkbcommon-types.c", 323, "if (new->level >= type->num_levels)"),
    ("xkbcommon-types.c", 638, ".num_levels = 1,"),
    ("xkbcommon-keymap.c", 535, "empty_mapped = true;"),
    ("xkbcommon-keymap.c", 538, "if (!empty_mapped && count < masks_size) {"),
    ("xkbcommon-keymap.h", 678, "return entry->mods.mods == 0 || entry->mods.mask != 0;"),
    ("xkbcommon-keymap-dump.c", 345, "if (entry->level == 0 && entry->preserve.mods == 0)"),
    ("xkbcommon-keymap-dump.c", 346, "continue;"),
    ("xkbcommon-keysym.c", 438, "return keysym >= XKB_KEY_KP_Space && keysym <= XKB_KEY_KP_Equal;"),
    ("xkbcommon-keysym.c", 66,
     'return snprintf(buffer, size, "U%04"PRIX32, ks & UINT32_C(0xffffff));'),
    ("xkbcommon-tools-how-to-type.c", 697,
     "const size_t num_masks = xkb_keymap_key_get_mods_for_level("),
    # serializer emission (census constructs)
    ("xkbcommon-keymap-dump.c", 266, 'xkb_keycodes \\"%s\\" {'),
    ("xkbcommon-keymap-dump.c", 316, 'xkb_types \\"%s\\" {'),
    ("xkbcommon-keymap-dump.c", 329, 'copy_to_buf(buf, "\\ttype ");'),
    ("xkbcommon-keymap-dump.c", 684, 'xkb_compatibility \\"%s\\" {'),
    ("xkbcommon-keymap-dump.c", 710, "interpret %s+%s(%s) {"),
    ("xkbcommon-keymap-dump.c", 754, "action= {"),
    ("xkbcommon-keymap-dump.c", 789, "write_keysyms(struct xkb_keymap *keymap"),
    ("xkbcommon-keymap-dump.c", 971, 'actions[%"PRIu32"]= [ '),
    ("xkbcommon-keymap-dump.c", 990, 'xkb_symbols \\"%s\\" {'),
    # host type that produces the F2 corpus case
    ("/usr/share/xkeyboard-config-2/types/numpad", 17, "map[None] = Level2;"),
]


def main():
    bad = 0
    for path, line, quote in CHECKS:
        full = path if path.startswith("/") else os.path.join(HERE, path)
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                text = f.read().splitlines()
        except OSError as exc:
            print("ERROR %s: %s" % (full, exc))
            bad += 1
            continue
        if line < 1 or line > len(text):
            print("FAIL %s:%d out of range" % (full, line))
            bad += 1
            continue
        got = text[line - 1]
        if quote in got:
            print("PASS %s:%d %s" % (path, line, quote))
        else:
            print("FAIL %s:%d %r not in %r" % (path, line, quote, got.strip()))
            bad += 1
    print("QUOTE-CHECK %d/%d passed" % (len(CHECKS) - bad, len(CHECKS)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
