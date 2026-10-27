#!/usr/bin/env python3
"""Verify every quote cited in .ufo/waves/round-49/w1/ExecKeysymNames.md.

Each entry is (pinned file in this seat dir, computed locator line, quote).
The script greps the file for the quote and requires a literal match within
+-2 lines of the locator; it prints the line it actually matched. Locators are
therefore checked against the file, not trusted.

Usage: python3 receipts/verify-quotes.py > receipts/quotes-verified.txt
"""

import os
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecKeysymNames"

QUOTES = [
    ("tools_how-to-type.c", 286, "*keysym = xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS);"),
    ("tools_how-to-type.c", 287, "if (*keysym == XKB_KEY_NoSymbol) {"),
    ("tools_how-to-type.c", 291, "const long int val = strtol(argv[optind], &endp, 10);"),
    ("tools_how-to-type.c", 292, "if (errno != 0 || !isempty(endp) || val <= 0 || val > XKB_KEYSYM_MAX) {"),
    ("tools_how-to-type.c", 293, '"ERROR: Failed to convert argument to keysym\\n"'),
    ("tools_how-to-type.c", 171, '{"keymap",               optional_argument,      0, OPT_KEYMAP},'),
    ("tools_how-to-type.c", 570, "ret = xkb_keysym_get_name(keysym, name, sizeof(name));"),
    ("tools_how-to-type.c", 625, 'printf("keysym: %s (%#06"PRIx32")\\n\\n", name, keysym);'),
    ("src_keysym.c", 70, "xkb_keysym_get_name(xkb_keysym_t ks, char *buffer, size_t size)"),
    ("src_keysym.c", 66, 'return snprintf(buffer, size, "U%04"PRIX32, ks & UINT32_C(0xffffff));'),
    ("src_keysym.c", 90, "return get_unicode_name(ks, buffer, size);"),
    ("src_keysym.c", 93, 'return snprintf(buffer, size, "0x%08x", ks);'),
    ("src_keysym.c", 233, "return (count > 0 && s[count] == '\\0');"),
    ("src_keysym.c", 237, "xkb_keysym_from_name(const char *name, enum xkb_keysym_flags flags)"),
    ("src_keysym.c", 305, "if (*name == 'U' || (icase && *name == 'u')) {"),
    ("src_keysym.c", 309, "return (val > 0xff && val <= 0x10ffff)"),
    ("src_keysym.c", 330, "if (!parse_keysym_hex(&name[2], &val) || val > XKB_KEYSYM_MAX)"),
    ("src_keysym.c", 338, 'if (strncmp(name, "XF86_", 5) == 0 ||'),
    ("src_keysym-utf.c", 922, "return ucs | 0xff00;"),
    ("src_keysym-utf.c", 932, "if (unlikely(ucs == 0 || is_surrogate(ucs) || ucs > 0x10ffff))"),
    ("src_keysym.h", 43, "XKB_KEYSYM_UNICODE_OFFSET 0x01000000"),
    ("src_keysym.h", 45, "XKB_KEYSYM_UNICODE_MIN    0x01000100"),
    ("src_keysym.h", 51, "XKB_KEYSYM_UNICODE_MAX    0x0110ffff"),
    ("src_keysym.h", 55, "XKB_KEYSYM_NAME_MAX_SIZE  31"),
    ("include_xkbcommon.h", 280, "XKB_KEYSYM_MAX      0x1fffffff"),
    ("src_utils-numbers.h", 88, "parse_hex_to_##type(const char *s, size_t len, type (*out))"),
    ("scripts_update-keysyms-derived-headers.py", 47, "if value not in canonical_names:"),
    ("scripts_update-keysyms-derived-headers.py", 48, "canonical_names[value] = name"),
]


def main():
    bad = 0
    for name, loc, quote in QUOTES:
        path = os.path.join(SEAT, name)
        with open(path, "rt", encoding="utf-8", errors="replace") as fd:
            lines = fd.read().splitlines()
        hits = [i + 1 for i, line in enumerate(lines) if quote in line]
        near = [h for h in hits if abs(h - loc) <= 2]
        ok = bool(near)
        bad += 0 if ok else 1
        print("%s %s:%d -> matched lines %s %s"
              % ("OK" if ok else "FAIL", name, loc, nearby_str(hits, loc), quote[:60]))
    print("quotes=%d fail=%d" % (len(QUOTES), bad))
    return 1 if bad else 0


def nearby_str(hits, loc):
    if not hits:
        return "[]"
    near = [h for h in hits if abs(h - loc) <= 2]
    return str(near if near else hits)


if __name__ == "__main__":
    sys.exit(main())
