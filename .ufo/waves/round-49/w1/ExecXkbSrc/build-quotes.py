#!/usr/bin/env python3
"""Generate quotes.md for seat ExecXkbSrc with COMPUTED locators.

Every quote is an exact substring of the pinned file; the line number is found by
an exact substring search at generation time, never typed by hand.  Word counts
are computed so the <=25-word rule is checkable.  No process, socket or network.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FETCH = HERE / "fetch"
OUT = HERE / "quotes.md"

# (id, file, exact substring, why-it-matters note)
QUOTES = [
    # ---- keysym.c ----
    ("K1", "keysym.c", "bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);",
     "from_name(): the only meaningful flag; `if (flags & ~XKB_KEYSYM_CASE_INSENSITIVE) return XKB_KEY_NoSymbol;` right after makes any other flag fatal."),
    ("K2", "keysym.c", "We need to !icase case to be fast, for e.g. Compose file parsing.",
     "Case-sensitive lookup is the fast path and is a perfect hash plus exact strcmp, not a linear scan."),
    ("K3", "keysym.c", "size_t pos = keysym_name_perfect_hash(name);",
     "The case-sensitive path is a generated perfect hash, so name acceptance is table-driven."),
    ("K4", "keysym.c", "if (strcmp(name, s) == 0)",
     "Exact byte comparison: names differing only in case do NOT match without the flag (measured: `--keysym SLASH` rc 2)."),
    ("K5", "keysym.c", "The name_to_keysym table is sorted by istrcmp(). So the binary",
     "Case-insensitive path is a binary search over an istrcmp-sorted table."),
    ("K6", "keysym.c", "The \"best\" case-insensitive match is the lower-case keysym name.",
     "Documents the tie-break: lower-case name wins among case-only duplicates."),
    ("K7", "keysym.c", "return snprintf(buffer, size, \"%s\", get_name(&keysym_to_name[index]));",
     "get_name() canonical choice: one canonical name per keysym value, from the keysym_to_name table."),
    ("K8", "keysym.c", "return snprintf(buffer, size, \"U%04\"PRIX32, ks & UINT32_C(0xffffff));",
     "Unicode fallback naming: `U%04X` of the low 24 bits (measured: 0x01000100 -> U0100)."),
    ("K9", "keysym.c", "return snprintf(buffer, size, \"0x%08x\", ks);",
     "Last-resort naming for unnamed non-Unicode keysyms (measured: 0x200000 -> `0x00200000`)."),
    ("K10", "keysym.c", "if (ks > XKB_KEYSYM_MAX) {",
     "get_name() refuses values above XKB_KEYSYM_MAX with \"Invalid\" and -1."),
    ("K11", "keysym.c", "if (ks >= XKB_KEYSYM_UNICODE_MIN && ks <= XKB_KEYSYM_UNICODE_MAX)",
     "The Unicode-name window is [UNICODE_MIN, UNICODE_MAX]; below UNICODE_MIN the 0x%08x branch is used."),
    ("K12", "how-to-type.c", "*keysym = xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS);",
     "how-to-type itself never sets CASE_INSENSITIVE: the ARG name lookup is case-SENSITIVE."),

    # ---- keysym.h (private, generated) ----
    ("KH1", "keysym.h", "#define XKB_KEYSYM_NAME_MAX_SIZE  31",
     "Name buffer size how-to-type allocates; the printf `%-*s` width is NAME_MAX_SIZE-1 = 30."),
    ("KH2", "keysym.h", "#define XKB_KEYSYM_COUNT_EXPLICIT 2505",
     "Library-declared number of explicitly named keysyms; measured header value count is also 2505."),
    ("KH3", "keysym.h", "#define XKB_KEYSYM_UNICODE_MIN    0x01000100",
     "Lower bound of the Unicode keysym window."),
    ("KH5", "keysym.h", "This file has been generated automatically by",
     "The header and the library tables are generated from one source, which is why header line order and the canonical name agree."),
    ("KH4", "keysym.h", "Maximum keysym canonical name length, plus terminating NULL byte",
     "Why 30-char canonical names fit `%-9s`/`%-*s` widths without truncation."),

    # ---- keymap.c : xkb_keymap_key_get_mods_for_level ----
    ("M1", "keymap.c", "layout = XkbWrapGroupIntoRange((int32_t) layout, key->num_groups,",
     "Out-of-range layout is wrapped, not rejected - how-to-type therefore always asks layout == key layout."),
    ("M2", "keymap.c", "if (level >= XkbKeyNumLevels(key, layout))",
     "A level past the key's level count yields zero masks, hence zero printed rows."),
    ("M3", "keymap.c", "If the active set of modifiers doesn't match any explicit entry of",
     "The key-type fallback rule: no explicit entry matches -> level 0 (Level 1)."),
    ("M4", "keymap.c", "What we do instead, is special case the empty set of modifiers for",
     "Level 1 gets the empty mask offered when no entry maps empty->level 0 (the `[ ]` row)."),
    ("M5", "keymap.c", "Now search explicit mappings.",
     "After the level-0 special case, masks come only from explicit type entries."),
    ("M6", "keymap.c", "for (darray_size_t i = 0; i < type->num_entries && count < masks_size; i++)",
     "Both loops are bounded by masks_size; appending stops rather than overflowing."),
    ("M6b", "how-to-type.c", "keymap, keycode, layout, level, masks, ARRAY_SIZE(masks)",
     "how-to-type passes MAX_TYPE_MAP_ENTRIES as masks_size, so truncation cannot silently drop rows."),
    ("M7", "keymap.c", "type->entries[i].level == level",
     "One output row per active type entry whose level equals the requested level."),

    # ---- how-to-type.c ----
    ("T1", "how-to-type.c", "printf(\"keysym: %s (%#06\"PRIx32\")\\n\\n\", name, keysym);",
     "Line 1 of stdout: `%#06x` = at least 4 hex digits, wider for XF86 values."),
    ("T2", "how-to-type.c", "printf(\"=== Direct access ===\\n\\n\");",
     "Line 3-4 of stdout, always printed even with --disable-compose."),
    ("T3", "how-to-type.c", "\"KEYCODE\", \"KEY NAME\", \"LAYOUT\", \"LAYOUT NAME\", \"LEVEL#\", \"MODIFIERS\"",
     "The column header text; layout/level are 1-based."),
    ("T4", "how-to-type.c", "printf(\"%-8u %-9s %-8u %-20s %-7u [ \",",
     "Row format: keycode, key name, layout+1, layout name, level+1, then `[ `."),
    ("T5", "how-to-type.c", "const xkb_mod_mask_t mod_mask = xkb_keymap_mod_get_mask2(keymap, mod);",
     "Modifier column: a name is printed when its mask bits are all contained in the row mask."),
    ("T6", "how-to-type.c", "printf(\"%s \", xkb_keymap_mod_get_name(keymap, mod));",
     "Each matching modifier name is printed with a trailing space, then `]` - e.g. `[ Mod5 LevelThree ]`."),
    ("T7", "how-to-type.c", "for (xkb_keycode_t keycode = min_keycode; keycode <= max_keycode; keycode++) {",
     "The scan is over every keycode present in the keymap that has a key name."),
    ("T8", "how-to-type.c", "const char* const key_name = xkb_keymap_key_get_name(keymap, keycode);",
     "Keys without a name are skipped entirely (no row)."),
    ("T9", "how-to-type.c", "xkb_keymap_num_levels_for_key(keymap, keycode, layout);",
     "Levels come from the keymap, not from a fixed 4-level model."),
    ("T10", "how-to-type.c", "We only deal with levels with exactly one keysym",
     "Multi-keysym levels are skipped, so a level with two syms never produces a row."),
    ("T11", "how-to-type.c", "if (syms[0] != keysym) {",
     "Row matching is exact keysym equality - no keysym normalization or case folding."),
    ("T12", "how-to-type.c", "/* Found our keysym: print the combo that generates it */",
     "On a match, every mask from mods_for_level is printed as its own row."),
    ("T13", "how-to-type.c", "const size_t num_masks = xkb_keymap_key_get_mods_for_level(",
     "The only source of the MODIFIERS column values."),
    ("T14", "how-to-type.c", "if (!key_name)",
     "Guards the NULL key name before a layout loop."),
    ("T15", "how-to-type.c", "layout_name = \"?\";",
     "Unnamed layouts print `?` in LAYOUT NAME."),
    ("T16", "how-to-type.c", "if (use_compose) {",
     "The Compose section (and its header row) is entirely inside this guard, so --disable-compose output ends after the last Direct-access row."),
    ("T17", "how-to-type.c", "ERROR: Failed to convert argument to keysym",
     "The stderr line and rc 2 that the tool must reproduce for a bad ARG."),
    ("T18", "how-to-type.c", "const long int val = strtol(argv[optind], &endp, 10);",
     "Decimal fallback is base-10 only and rejects trailing bytes."),

    # ---- xkbcommon.h ----
    ("H1", "xkbcommon.h", "this function will accept any name returned by that function.",
     "Every canonical name printed by get_name must be accepted by from_name - the round-trip the tool must preserve."),
    ("H2", "xkbcommon.h", "If you use the `::XKB_KEYSYM_CASE_INSENSITIVE` flag and two keysym names",
     "The documented tie-break for the case-insensitive flag (not used by how-to-type)."),
    ("H3", "xkbcommon.h", "Case folding is done according to the C locale; the current locale is not",
     "Locale-independent: the tool needs no locale tables."),
    ("H4", "xkbcommon.h", "the string is truncated",
     "Buffer-too-small behaviour, relevant when the tool formats a 30-char canonical name."),
    ("H5", "xkbcommon.h", "The number of bytes in the name, excluding the `NULL` byte. If",
     "Return value contract: -1 for invalid keysyms (how-to-type turns that into 'Failed to get name')."),
    ("H6", "xkbcommon.h", "If the key is not in the keymap or if the specified shift level cannot",
     "mods_for_level returns 0 for unreachable levels - no row, not an error."),
    ("H7", "xkbcommon.h", "This API is useful for inverse key transformation; i.e. finding out",
     "Names the API's purpose: which modifiers reach a given key/layout/level."),
    ("H8", "xkbcommon.h", "In X11 terminology it corresponds to the mapping to the *[real modifiers]*.",
     "mask2/mask map modifier names to real (X11) modifier bits in 1.13."),

    # ---- xkbcommon-keysyms.h ----
    ("X1", "xkbcommon-keysyms.h", "#define XKB_KEY_slash                         0x002f",
     "The canonical name of 0x002f is lower-case `slash`; there is no XKB_KEY_SLASH define."),
    ("X2", "xkbcommon-keysyms.h", "/* deprecated alias for Prior */",
     "Aliases are marked in comments only; canonicality is not machine-readable as a flag."),
    ("X3", "xkbcommon-keysyms.h", "#define XKB_KEY_Prior                         0xff55",
     "For alias groups the canonical name is the FIRST define of that value in the header (measured on all 120 alias groups)."),
    ("X4", "xkbcommon-keysyms.h", "#define XKB_KEY_SunPrint_Screen           0x0000ff61",
     "Sun* names use a 7-digit value; numeric normalization is required before ordering aliases."),
]


def wordcount(s: str) -> int:
    return len(s.split())


def main() -> int:
    rows = []
    failures = []
    for qid, fname, needle, note in QUOTES:
        path = FETCH / fname
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [i + 1 for i, line in enumerate(lines) if needle in line]
        if not hits:
            failures.append(f"{qid}: NOT FOUND in {fname}: {needle!r}")
            continue
        wc = wordcount(needle)
        if wc > 25:
            failures.append(f"{qid}: {wc} words > 25")
            continue
        loc = ",".join(str(h) for h in hits)
        rows.append((qid, f"{fname}:{loc}", wc, needle, note))
    if failures:
        print("GENERATION FAILED", file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        return 1
    with OUT.open("w", encoding="utf-8") as fh:
        fh.write("# ExecXkbSrc — located quotes (libxkbcommon 1.13.2, pinned)\n\n")
        fh.write("Locators are **computed** by `build-quotes.py` (exact substring search over `fetch/`),\n")
        fh.write("never typed. Every quote is <= 25 words (word count computed below) and is re-verified\n")
        fh.write("independently by `verify-quotes.py`, whose output is `verify-quotes.out`.\n\n")
        fh.write("| id | locator | words | quote | what it establishes |\n")
        fh.write("|---|---|---|---|---|\n")
        for qid, loc, wc, needle, note in rows:
            esc = needle.replace("|", "\\|").replace("`", "\\`")
            fh.write(f"| {qid} | `{loc}` | {wc} | `{esc}` | {note} |\n")
        fh.write(f"\nTotal quotes: {len(rows)}. All <= 25 words.\n")
    print(f"wrote {OUT} with {len(rows)} quotes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
