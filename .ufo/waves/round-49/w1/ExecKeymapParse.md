# ExecKeymapParse — serialized-keymap parser + syntax census (mado round 49, w1)

Seat `ExecKeymapParse` (leaf executor). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `03e4ae76`.
Nothing here is a scored claim; this feeds the C1 freeze (`tools/mado-keysym.py`, fixtures, counter). No host state was
written, no pacman, no compositor call, no terminal. Work dir was `/fast/scratch/hyaku/mado-r49/ExecKeymapParse`
(removed at the end; no scratch path is cited as evidence — receipts were copied into the seat first).

## Deliverables (`.ufo/waves/round-49/w1/ExecKeymapParse/`)

| file | what | evidence |
|---|---|---|
| `parse.py` | stdlib-only parser of the SERIALIZED keymap text (V2, pretty, keep-unused); derives the `(keycode, layout, level) -> keysym` table and the exact cell set `how-to-type` prints | `receipts/selftest.txt` `MADO_KEYMAP_PARSE_SELFTEST: 34/34 passed`, rc 0 |
| `census.py` | seeded RMLVO draw from `xkbcli list`, compile with the pinned `compile-keymap` (clean env, scratch HOME), census with `parse.py`, write the receipts | `receipts/census.txt`, `census-keymaps.tsv`, `compile-log.txt`, `manifest.json` |
| `verify.py` | differential: inverts `how-to-type` over every keysym spelling present in a keymap and requires identical `(KEYCODE, LAYOUT, LEVEL#)` rows | `receipts/verify.txt` (20 keymaps), `receipts/verify-all-240.txt` (all 240) |
| `check-quotes.py` | re-greps every source quote below at its cited line | `receipts/quote-check.txt`: `QUOTE-CHECK 24/24 passed` |
| `receipts/level0-shadowing.txt` | the F2 corpus case: keymap, serialized `KEYPAD`/`KP7`, both judge runs | `map[none]= 2` + no row for `KP_Home` |
| `receipts/unreachable-cells.txt` | all 36 F2 cells enumerated (keymap, keycode, key, layout, level, keysym, type) | `# total=36 keymaps=240` |
| `URLS`, `SHA256SUMS`, `receipts/pins.sha256` | pinned libxkbcommon 1.13.2 sources + host binaries/header | digests below |

`parse.py` does **not** print the MODIFIERS column; masks are `ExecModsLevel`'s contract. It does compute whether a
level has *any* mask, because the judge's row set depends on that (finding F2). Interface for the tool:
`Keymap.judge_cells()` = the occupied cells; feed each through the mask implementation, print one row per mask.

## What was run

- Compile: `/usr/lib/xkbcommon/xkbcli-compile-keymap` sha256 `43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250`;
  248 attempts → **240 rc=0**, 8 failures. Each run: `subprocess` with `env = {PATH=/usr/bin, HOME=<scratch>/home,
  XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME under scratch, LC_ALL=C}`, cwd = scratch.
- Judge: `/usr/lib/xkbcommon/xkbcli-how-to-type` sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`
  (the claim's pin), always `--keymap=FILE --disable-compose --keysym <spelling>`.
- Keysyms header `/usr/include/xkbcommon/xkbcommon-keysyms.h` sha256 `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3`
  (2,638 real `#define`s; the ticket's 2,659 counts 21 documentation lines inside comments).
- `xkbcli list` sha256 `2666867f599d0a0ca9c0047d011cc5f86012a66a4e141f59ca5b33a6bbe6c760`: 184 models, 598
  layout/variant pairs, **99 layout names**, 217 options.
- Draw (`--seed 49`, reproducible): rules evdev 4/6 · base 1/6 · xorg 1/6; model pc105 75 % else random; 1/2/3 layouts
  55/30/15 from *distinct layout names*, variant drawn from that layout's own variant list; 0-4 options 25/30/25/15/5.
- Corpus: 240 keymaps, 15,998,883 B total, 90,775 keys, 97,308 (key, group) slots, 159,857 level slots, 124,144 distinct
  keysym spellings. All 240 were accepted by `parse.py` with **zero** OutOfContract/ParseError.
- Tooling installs: none.

## Findings the freeze should use

### F1 — the serialized level list is *already* the post-trim, post-type level set

`symbols.c` drops `NoSymbol` inside a level and drops trailing empty levels when it parses the file
(`/* Drop trailing NoSymbol */` at `xkbcommon-symbols.c:842`, `if (nonEmptyLevels < nLevels)` at `:846`), then resizes
each group to its type's level count (`darray_resize0(groupi->levels, type->num_levels);` at `:1782`). The serializer
writes exactly `XkbKeyNumLevels(key, group)` syms per group (`write_keysyms()` at `xkbcommon-keymap-dump.c:789`,
`xkbcommon-symbols.c` type assignment at `:1738-1782`), so in serializer output **width == the group type's num_levels**. That is why
`num_levels = max(1, highest printed map[] level)` (`xkbcommon-types.c:323-332`, `:638`) is all a parser needs for level
counts, and why the automatic type *name* is irrelevant to the level count (`FindAutomaticType` at
`xkbcommon-symbols.c:1594` returns 1/2/4-level types per width).

The automatic type *name* does matter for F2's reachability, though. Corpus exercise: `level_trailing_trimmed=3340` in 122 of 240
keymaps, `level_nosymbol_dropped=4504`, `level_empty=1164`, multi-keysym levels `{a,b}` **0**.

### F2 — a cell with one keysym can still print **no row** (level-0 shadowing) — 36 cells, 3 keymaps

`xkb_keymap_key_get_mods_for_level` suppresses the implicit empty mask for level 0 when the key type has *any* active
entry with mask 0 (`empty_mapped = true;` at `xkbcommon-keymap.c:535`, then `if (!empty_mapped && count < masks_size) {`
at `:538`), and how-to-type prints one row per mask (`xkbcommon-tools-how-to-type.c:697-703`). Level-1 map entries are
normally omitted from the serialization (`if (entry->level == 0 && entry->preserve.mods == 0)` at
`xkbcommon-keymap-dump.c:345`, `continue;` at `:346`), so a level-0 cell is shadowed exactly when a **printed**
`map[none]= N` (N ≥ 2) exists. `numpad:mac` does this to `KEYPAD` (`map[None] = Level2;` at
`/usr/share/xkeyboard-config-2/types/numpad:17`); the serialized form, the `KP7` key and both judge runs are in
`receipts/level0-shadowing.txt`. With `key <KP7> { [ KP_Home, KP_7 ] }` the judge prints `KP_7` at level 2 and **nothing**
for `KP_Home` (level 1 has zero masks). Measured corpus effect: `judge_cell_reachable=155317`, `judge_cell_unreachable=36`,
`judge_unreachable_level0=36` in 3 keymaps, `judge_unreachable_levelN=0`, `type_none_entry=3`. The counter/tool must not
expect rows for those 36 cells; `parse.py`'s `judge_cells()` excludes them and `unreachable_cells()` names them.

### F3 — automatic type resolution only matters through the KEYPAD branch

Automatic types per width are `ONE_LEVEL` (≤1), `ALPHABETIC|KEYPAD|TWO_LEVEL` (2),
`FOUR_LEVEL_ALPHABETIC|FOUR_LEVEL_SEMIALPHABETIC|FOUR_LEVEL_KEYPAD|FOUR_LEVEL` (3-4). Reachability (F2) and level count
(F1) are identical across the non-KEYPAD candidates; only KEYPAD can carry a printed `map[none]`. The KEYPAD predicate is
`return keysym >= XKB_KEY_KP_Space && keysym <= XKB_KEY_KP_Equal;` (`xkbcommon-keysym.c:438`), decided here from the spelling: `KP_*` except `KP_BackTab`
(0x1000ff75, the only canonical KP_ name outside the range) plus a value check for `0x…`/`Uxxxx` spellings.
`census.py` verifies that classifier against every one of the 2,638 header defines:
`keysym_classifier {"defines": 2638, "kp_defines": 38, "mismatches": [], "mismatch_count": 0}`.

### F4 — constructs that do occur and the parser must accept

All counts are totals over 240 keymaps (`keymaps_with` in `receipts/census.txt`). Sections are always **quoted**
(`section_xkb_*_quoted=240`, bare `0`). `xkb_symbols` section names contain parentheses and `+`, type names contain `+`
(`CTRL+ALT`), so section/type names are strings, not identifiers.

| construct | total | note |
|---|---|---|
| `name[GroupN]` | 372 (240 km) | group names; one string is non-ASCII (`string_nonascii=1`) |
| key blocks: simple `[ … ]` / `symbols[GroupN]=` | 79,630 / 17,678 | 11,145 keys use the group form; 3,797 keys have 2 groups, 1,368 have 3 |
| `type= "…"` (default type for all groups) | 6,417 keys (240 km) | e.g. `CTRL+ALT`, `ALPHABETIC` |
| `type[GroupN]= "…"` (multi-type keys) | 1,170 groups in 59 km | explicit groups 8,095 of 97,308 |
| `repeat= Yes/No,` on a key | 6 (6 km) | |
| `virtualMods= …,` on a key | 5 (5 km) | |
| `actions[GroupN]= [ … ]` on a key | 6 (6 km) | e.g. `actions[1]= [ SetMods(modifiers=NumLock) ]` |
| `modifier_map` in symbols | 1,887 lines / 3,392 key names | |
| type definitions | 27 per keymap, 6,480 total | all kept (`KEEP_UNUSED`), incl. `EIGHT_LEVEL*` (8 levels) |
| `map[…]` / `preserve[…]` / `level_name[…]` | 44,640 / 10,338 / 26,877 | |
| `virtual_modifiers` (types and compat) | 240 / 240 | explicit mappings 952 (e.g. `Hyper=0x4000`) |
| compat `interpret` blocks | 29,784 | one `action=` each; `action= { … }` multi-action block **0** |
| compat block fields | `virtualModifier` 3,844, `useModMapMods` 1,681, `repeat` 12,720, `groups` 248, `modifiers` 956, `whichModState` 956, `controls` 240 | |
| `interpret.useModMapMods=` / `interpret.repeat=` globals | 240 each | dotted keywords |
| keycodes `<NAME> = N` / `alias` / `indicator` | 104,128 / 16,684 / 2,753 | key names include `VOL-`/`VOL+` (`[A-Za-z0-9_+-]`) |
| keysym spellings | named 147,363 · `Uxxxx` 7,778 (197 km) · `0x…` 212 (14 km) · `NoSymbol` 4,504 · decimal 0 | |
| string escapes | `\n` 0 · `\\` 0 · `\0ooo` 0 | no escapes in 240 keymaps; the parser still decodes all three |
| comments / `xkb_geometry` / `include` | 0 / 0 / 0 | rejected by the parser, so absence is enforced, not assumed |

`Uxxxx` spellings are `xkb_keysym_get_name`'s no-`+` form (`return snprintf(buffer, size, "U%04"PRIX32, ks & UINT32_C(0xffffff));`
at `xkbcommon-keysym.c:66`, applied at `:89-90`)
and are parsed back by `xkb_keysym_from_name`; every emitted spelling **is** the canonical name (`NAME_CANONICALISED 0` in
both differential receipts) and every named spelling exists in the header (`HEADER_MISSING_NAMES -`).

### F5 — 8 of 248 draws do not compile, all because `xkbcli list` offers `custom`

All 8 failures are rc 1 with XKB-338 `Couldn't find file "symbols/custom"` or `"types/custom"` (`receipts/compile-log.txt`,
full stderr class). `xkbcli list` advertises a **layout** `custom` (“A user-defined custom Layout”, list line 4138) and an
**option** `custom:types` (“Use user-defined custom XKB types”, line 5098), which only compile when the operator has
`~/.config/xkb` files — not on this host, and never in the counter's clean env. Fixtures/nonce generation must exclude the
`custom` layout name and `custom:*` options (or expect rc 1 for them). Excerpt: `receipts/xkbcli-list-custom.txt`.

## Constructs declared OUT of contract (parser refuses: `OutOfContract`, or `ParseError` for the action-field shape)

| rejected construct | why (serializer/source) | corpus |
|---|---|---|
| `include "…"` | the serializer writes the fully-included keymap; no include statement exists in `keymap-dump.c` | 0/240 |
| `default`/`partial`/`replace`/`augment`/`override` prefixes | dump writes bare `xkb_keycodes`/`type`/`key`/`interpret` (`keymap-dump.c:266,316,329,684,710,990`) | 0/240 |
| `xkb_geometry` section | `compile-keymap` output has 4 sections only | 0/240 |
| `#`, `//`, `/* */` comments | never emitted | 0/240 |
| string escapes other than `\n`, `\\`, `\0ooo` | `check_write_string_literal`, `xkbcommon-keymap-dump.c:136-190` | 0/240 |
| non-contiguous `symbols[GroupN]`/`type[GroupN]` (a gap) | dump writes every group 1..num_groups (`keymap-dump.c:963-978`) | 0/240 |
| `action= { … }` holding action *fields* | the block form only concatenates whole action calls (V2 multi-action levels, `keymap-dump.c:753-763`) | 0/240 |
| non-ASCII outside a string literal | not emitted; names are ASCII | 0/240 |

Accepted by the parser but never emitted by the 240 compiled keymaps (hence in contract but unproven by the corpus):
`groupsClamp` / `groupsRedirect=` on a key, bare (unquoted) section headers, the multi-action `action= { … }` block,
multi-keysym levels `{ a, b }` (`write_keysyms()` `xkbcommon-keymap-dump.c:824-846`), any string escape, decimal keysym
spellings, and the duplicate/undefined-name paths (`types_duplicate_name`, `kc_duplicate_name`, `symbols_key_duplicate`,
`symbols_key_unknown_in_keycodes`, `type_undefined_fallback`, `level_cleared_by_type`). `parse.py`'s selftest exercises
each of the syntax paths that the corpus leaves cold.

Model boundaries (not syntax): modifier **masks** are not computed (only reachability); `preserve[…]` values, compat
semantics and actions are parsed for shape but not interpreted; the parser targets output format V2 exactly as
`compile-keymap` defaults emit it (`--format`/`--no-pretty`/`--drop-unused` are outside the contract).

## Proof: parser table == judge's implied table

Method: for every keysym spelling in a keymap, `how-to-type` is run and its `=== Direct access ===` rows are compared with
`parse.judge_positions(spelling)` — same order, duplicate mask rows collapsed (masks are another seat's contract). The
`keysym: NAME (0x…)` header value is checked against the spelling's implied value (header define for names, `0x` parsed,
`0x01000000+cp` for `Uxxxx`). Two negatives per keymap: a keysym absent from the keymap and (when applicable) a keysym
present only in a multi-keysym level must print zero rows.

| run | keymaps | checks | agree | disagree | receipt |
|---|---|---|---|---|---|
| required 20-keymap proof (6 construct-class representatives, then 5 by groups, 5 by levels, 5 by spellings, 5 by cells) | 20 | 12,655 | 12,655 | **0** | `receipts/verify.txt` |
| whole census corpus | 240 | 124,624 | 124,624 | **0** | `receipts/verify-all-240.txt` |

The 20-keymap selection covers 1/2/3 groups, 5- and 8-level types, 271 `type[GroupN]` groups, key-level
`actions[GroupN]` (3), `virtualMods` (3), `repeat` (3), 94 `0x` spellings (18 in one keymap, 68 in another) and the one
non-ASCII group name. The 240-keymap run is the same comparison over
every compiled keymap (its per-keysym detail file stayed in scratch; the receipt keeps every `SUMMARY` line).
The first full-corpus run, before F2 was modelled, disagreed on exactly those 36 level-0 cells — the same 36 that
`receipts/unreachable-cells.txt` enumerates and the census predicts as unreachable; after the model was added the
240-keymap run is clean, i.e. F2 was the only systematic gap.

## Risks / open items for the L1

- **Masks** (values, order, `Shift Lock Mod5 LevelThree` sequences) are not implemented here; `judge_cells()` decides only
  *which cells print*. The C1 tool needs `ExecModsLevel.mods.py` for the column; the counter compares full stdout, so this
  is a real dependency, not a detail.
- Reachability for levels > 0 is modelled as “some printed `map[…]` targets the level”. A printed entry naming a virtual
  modifier that resolves to mask 0 would be inactive (`return entry->mods.mods == 0 || entry->mods.mask != 0;` at
  `xkbcommon-keymap.h:678`) and the model would over-predict. `judge_unreachable_levelN=0` and 0 disagreements over
  124,624 checks say this never happens in 240 keymaps from xkeyboard-config 2.48; a nonce RMLVO cannot introduce a new
  type (`custom:types` needs a user file the clean env does not have), so the risk is confined to a host with user type
  files.
- The parser is deliberately strict (F4/F5). If the frozen fixtures are compiled with `--no-pretty` or `--drop-unused`, or
  with a future libxkbcommon format, the parser must be re-derived, not loosened.
- `KP_*`-based keypad classification is verified against the pinned header (0 mismatches); if a fixture ever carries a
  non-canonical keysym spelling, that assumption is what to check first.
- `receipts/manifest.json` (847 KB) embeds per-keymap stats and paths under the scratch dir; only the `sha256` fields are
  durable. Keymaps themselves were not committed (15.99 MB); they are reproducible from
  `census.py --seed 49` (verified: recompiling km001 gives the same sha256).
