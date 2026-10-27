# libxkbcommon 1.13.2 `how-to-type` output contract

Source fetched from `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/tools/how-to-type.c`; 836 lines; SHA-256 `f774882e88f012cb18225db4232c8a8074f7c7a7371c789fca8c27f41c8515bc`. Host verification: `/usr/lib/xkbcommon/xkbcli-how-to-type` SHA-256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`, package libxkbcommon 1.13.2-1. The citations below are source file line numbers.

## Exact stdout with `--disable-compose`

On success (main:625-628), stdout begins exactly:

```
keysym: NAME (0xNNNN)\n
=== Direct access ===\n
KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n
```

The actual first-line value format is `printf("keysym: %s (%#06"PRIx32")\n\n", name, keysym)`: lowercase hex, `0x` prefix, minimum width 4 hex digits (not a maximum); `name` is `xkb_keysym_get_name` output (main:569-574, 625). The exact column-heading format is `%-8s %-9s %-8s %-20s %-7s %-s\n` with labels `KEYCODE`, `KEY NAME`, `LAYOUT`, `LAYOUT NAME`, `LEVEL#`, `MODIFIERS` (main:627-628). Each data line is `%-8u %-9s %-8u %-20s %-7u [ ` followed by modifier names in modifier-index order, each as `%s `, then `]\n` (print_combo:522-537). Thus numbers are 1-based for layout and level; keycode is unadjusted. `layout_name` falls back to `?` (main:644-647). Widths are minimum widths, not truncation limits.

With compose disabled, no compose heading or rows are printed (main:709-724 guarded by `if (use_compose)`; Compose table loading is similarly guarded at 599-623). After the column-header newline, zero matching positions means stdout ends there. There is no extra final blank line.

## Direct-access row selection and order

- Visit keycodes from `xkb_keymap_min_keycode` through `max_keycode`, ascending; skip missing key names (main:630-639). Host data accessors return the stored bounds/name (keymap.c:608-639).
- For each keycode, visit its layouts ascending from 0 to `num_layouts_for_key-1`, then levels ascending from 0 to `num_levels_for_key-1` (main:641-652).
- A level participates only if it has exactly one keysym; levels with 0 or multiple keysyms are skipped (main:652-660). Emit only when that one keysym equals the requested keysym (main:661-663, 693-704).
- For each match, emit every mask returned by `xkb_keymap_key_get_mods_for_level`, in returned order, without sorting/deduplication (main:695-704). The API implementation scans active type entries in their declaration order; at level 0 it may prepend mask 0 when no active explicit entry has mask 0 (keymap.c:517-551). It is capped at the passed output capacity, 100 (how-to-type.c:27, 696-699).
- Modifier rendering scans modifier indexes from 0 to `xkb_keymap_num_mods-1` (print_combo:530-535; keymap.c:323-338). Print a modifier iff `(mask & xkb_keymap_mod_get_mask2(index)) == that mapping`; names are keymap-defined. Real and virtual modifiers can both print for one real mask (e.g. host output `[ Mod5 LevelThree ]`). Zero mappings satisfy the subset test and therefore also print if present in the keymap's modifier list.
- The relevant keymap accessor source confirms modifier mappings are stored as vmod-to-real mappings (keymap.h:386-395) and `get_mask2` returns that mapping (keymap.c:366-374). `entry_is_active` is true when no virtual modifier is involved or the resolved mask is nonzero (keymap.h:670-678). The keymap parser/compiler's inferred key-type behavior is outside `how-to-type.c`; the serialized keymap output itself can omit per-key type annotations. The tool's contract depends on the compiled keymap API result, not merely its textual `symbols` arrays.

Host empirical confirmation (compiled `br`, `compose:caps` keymap, clean env): `slash` emitted AD01 keycode 24 levels 3/4 with masks including `[ Mod5 LevelThree ]` and `[ Shift Mod5 LevelThree ]`, plus Lock variants, then AB11 keycode 97 level 1 `[ ]`; `Return` emitted keycode 36 RTRN layout 1 level 1 `[ ]`.

## Keysym argument parsing (`--keysym`)

`--keysym` is a no-argument flag setting keysym-only mode (options table and switch:142-178, 188-196); the one positional argument remains mandatory (255-258). In keysym-only mode it skips character/codepoint parsing and calls `xkb_keysym_from_name(arg, XKB_KEYSYM_NO_FLAGS)` (269-286), so names are case-sensitive. If that yields `NoSymbol`, it tries base-10 `strtol`; decimal must consume the complete string, have no errno, and satisfy `0 < value <= XKB_KEYSYM_MAX`, else it emits the conversion error (287-297). Consequently decimal numeric keysyms are accepted as fallback, except zero. For example, host probe `47` resolved to slash; `0x2f` and `U002F` resolved to slash; `XF86_ScreenSaver` resolves through library's XF86 underscore fallback.

Library `src/keysym.c` lines 236-350 defines name parsing: exact case-sensitive table lookup first (251-258); `U` followed by 1–8 hex digits parses Unicode keysym notation, mapping values >0xff and <=0x10ffff to Unicode-offset keysyms and otherwise via `xkb_utf32_to_keysym` (305-324); `0x` lower-case prefix plus 1–8 hex digits parses a raw keysym up to `XKB_KEYSYM_MAX` (325-333); `XF86_` is retried with underscore removed (335-348). Other names fail. `xkb_utf32_to_keysym` in `src/keysym-utf.c:912-940` handles Latin-1, special control keysyms, rejects NUL/surrogates/out-of-range, otherwise direct Unicode encoding after table lookup.

The header's `XKB_KEY_` names alone are not a full name/value interpreter: parser additionally handles `U...`, `0x...`, decimal fallback, and XF86 underscore compatibility. Nor should canonical output names be derived by naïvely selecting any alias: generator `scripts/update-keysyms-names-handling.py:87-115, 207-224` sorts names for parsing and selects the first header-order definition per numeric value for canonical output. `xkb_keysym_get_name` source (`src/keysym.c:69-94`) returns that table name, unnamed Unicode as `U%04X`, unnamed non-Unicode as `0x%08x`, and `Invalid` for values above max. Header hash observed on host: `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3`, with 2659 `#define XKB_KEY_` lines.

## CLI parsing and errors

The actual option table declares `--keymap` an optional argument (how-to-type.c:164-177), so use `--keymap=FILE` to supply a file. A separated `--keymap FILE` leaves FILE positional and fails the exactly-one-positional check. `--keysym` likewise takes no argument; `--keysym=slash` is a getopt error. `--disable-compose` sets `use_compose=false` (195-196). The displayed usage says `--keymap=<file>` and describes `-`/missing as stdin (usage:72-133). The program's expected error return values: invalid usage `EXIT_INVALID_USAGE` = 2 (meson.build:166); runtime failure `EXIT_FAILURE` = 1; success 0. `-h/--help` prints usage to stdout and exits 0 (247-249). Usage errors print usage to stderr (311-314); usage includes `argv[0]` so stderr's Usage line depends on invocation path.

Relevant literal error strings and source locations:

- `ERROR: invalid --format "%s"\n` (207).
- `ERROR: missing positional parameter\n` (255-258).
- `ERROR: Failed to convert code point to keysym\n` (275-279; not reached in `--keysym` mode).
- `ERROR: Failed to convert argument to keysym\n` (293-295).
- `ERROR: --keymap is not compatible with --enable-environment-names\n` (302-305).
- `ERROR: Cannot use RMLVO options with keymap input\n` (307-309).
- Failed open: `ERROR: Failed to open keymap file "%s": %s\n`, name `stdin` if no path (331-334).
- Compose-only errors: `ERROR: cannot iterate Compose table\n` (357-359) and `Couldn't create compose from locale\n` (605-608); unreachable with compose disabled.
- Failed keysym name: `ERROR: Failed to get name of keysym\n` (571-575); runtime status 1.
- Context/keymap creation: `ERROR: Failed to create XKB context\n` (581-585), `ERROR: Failed to create XKB keymap\n` (590-593); status 1.

Option parser sends invalid options through usage path; getopt itself may emit its own diagnostic (default libc behavior), then `usage(stderr, argv[0])` runs (250-252, 311-314). `load_keymap` file parse diagnostics may additionally be emitted by libxkbcommon; source's own generic keymap error follows (load_keymap:321-340; main:590-593).

## Compose-only behavior to exclude under this contract

When enabled, locale `LC_CTYPE` supplies Compose table (main:599-614); it scans entries and matches either keysym or equivalent UTF-8 (lookup:350-385), then emits `=== Access via Compose sequences ===` and a second table (main:709-714), sorting each keysym's positions by layout, level, keycode (compare:402-421; qsort:716-723), enumerating Cartesian products with mixed-layout combinations discarded (main:725-823). With `--disable-compose`, all these output paths and Compose table errors are excluded.
