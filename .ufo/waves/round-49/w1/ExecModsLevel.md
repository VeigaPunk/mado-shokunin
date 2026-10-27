# ExecModsLevel — the MODIFIERS column (`xkb_keymap_key_get_mods_for_level` + how-to-type's mask printing)

Seat: mado round 49 w1 (BUILD), C1 component. Deliverable is a library module, not the
tool: `mods.py` here, plus the differential that proves it. Nothing outside this seat
directory was written; the tool at `tools/mado-keysym.py` and the C1 counter are other
seats' files and were not touched.

| file | role | sha256 |
|---|---|---|
| `mods.py` | the model (deliverable) | `5fa7a18944510e681eccef2eeec2f2bc67cc09d22d5a827627b7c4230a3fe1d6` |
| `diff_mods.py` | exhaustive differential vs the pinned library + end-to-end vs the judge binary | `f586182d0da0edd3cbd1ad4d5d2db5e6e67d1b5e9999bdd17b65377c29e11dfb` |
| `edge_cases.py` | probes the RMLVO corpus cannot reach | `ffdee95aa8b01748d7616a74049296895924fd054275c4db1e9e710cc04533d3` |
| `unit_checks.py` | unit checks for rules with no RMLVO witness | see `receipts/env-pins.txt` |
| `src/` | pinned libxkbcommon sources + `PINS.txt` + `SHA256SUMS` | `src/PINS.txt` |

Receipts: `receipts/mods-diff.txt`, `receipts/edge-cases.txt`,
`receipts/unit-checks.txt`, `receipts/source-loci.txt` (every `file:line` below is
computed by `grep -n`, not typed), `receipts/env-pins.txt`.

Library identity: the judge `/usr/lib/xkbcommon/xkbcli-how-to-type`
(`sha256 f6c0b122…`) is dynamically linked against `/usr/lib/libxkbcommon.so.0`
→ `libxkbcommon.so.0.13.2` (`sha256 e475adbf…`), the same shared object the harness
loads through `ctypes` (`ldd` output in `receipts/env-pins.txt`), so the exhaustive layer
compares my model against the exact functions the judge calls, and the end-to-end layer
compares against the judge's own stdout.

## The rule set

### R1 — which masks produce a level

`mods.mods_for_level(type, level, masks_size=100)` reproduces
`xkb_keymap_key_get_mods_for_level` (`src_keymap.c:494`):

* `level` out of `[0, type->num_levels)` → no masks (`src_keymap.c:512`).
* Level 0 is special-cased (`src_keymap.c:531-540`): an unmatched modifier set also
  selects level 0, so the empty mask `0` is emitted **first** — *unless the type already
  has an active entry whose mask is empty*, in which case it is not synthesised.
  The entry's own level is **not** consulted. Consequence, verified from the judge:
  a type with `map[none]= 3` produces **no row at all for Level 1** and one empty-mask row
  at Level 3 (`receipts/edge-cases.txt` probe C: judge `U1F702` → 0 rows, `U1F704` →
  `[ ]` at level 3).
* Then every **active** entry whose `level` matches is appended, in declaration order,
  duplicates included (a type cannot hold two entries with the same *named* mask, see R5,
  but two entries with different names can collapse to the same effective mask — both rows
  then print, e.g. `Mod1` and `Alt`/`Meta`, `receipts/mods-diff.txt` trace cells).
* The output is truncated at `masks_size`, which how-to-type sets to
  `MAX_TYPE_MAP_ENTRIES = 100` (`tools_how-to-type.c:27`, call at `:697`).

### R2 — which entries are active

An entry that names a virtual modifier with **no mapping** is deactivated at compile time:
its mask is zeroed and further processing is skipped (`src_xkbcomp_keymap.c:494-508`,
`has_unbound_vmods` at `:25`). `entry_is_active` then reports
`entry->mods.mods == 0 || entry->mods.mask != 0` (`src_keymap.h:676`), i.e. the deactivated
entry looks like "empty mask" only if you ignore that it named something. Deactivated
entries never contribute a mask. Witness: probe B, `virtual_modifiers TestVmod=none` with
`map[TestVmod]= 2` / `map[Shift+TestVmod]= 2` → only `[ Shift ]` survives at level 2.

### R3 — the effective mask of an entry

`mod_mask_get_effective` (`src_state.c:1614`) + `ComputeEffectiveMask`
(`src_xkbcomp_keymap.c:36`): real bits pass through, every named virtual bit is replaced by
that modifier's mapping, and bits past `num_mods` (numeric masks) are kept verbatim
(`unknown_mods`). Type `modifiers=`, entry `mods` and `preserve` all get this treatment
(`src_xkbcomp_keymap.c:509-510`). Preserve affects **nothing** in this column — it only
matters for level *selection* (`src/state.c`) — so it is carried in the model but unused by
`mods_for_level`.

### R4 — how a mask is printed (order, and which virtual modifiers are named)

`print_combo` (`tools_how-to-type.c:522-537`) is not "the type's `modifiers=` list":

* Every modifier **index** of the keymap is visited in index order:
  `0..7` are the always-present real modifiers `Shift Lock Control Mod1 Mod2 Mod3 Mod4
  Mod5` (`Shift` has bit 0, `Mod1` bit 3, …), then the virtual modifiers in keymap
  declaration order — which is the order of the serialized `virtual_modifiers` line,
  because `write_vmods` enumerates by index (`src_xkbcomp_keymap-dump.c:206-260`).
* A name is printed when **all bits of its canonical mapping are present**:
  `(mask & mapping) == mapping` (`src_keymap.c:369` `xkb_keymap_mod_get_mask2` gives the
  mapping). So the answer to "which virtual modifiers are named?" is neither "the type's
  vmods" nor "vmods whose mapping is a non-empty subset": **any** modifier whose mapping is
  contained in the mask, including virtual modifiers the type never mentions.
* `[ Lock Mod5 LevelThree ]` (host sample, `receipts/edge-cases.txt` probe D) is therefore
  the mask `Lock|Mod5 = 0x82` of `map[Lock+LevelThree]` in
  `FOUR_LEVEL_(SEMI)ALPHABETIC`: `Lock` and `Mod5` are real bits, `LevelThree` is the
  virtual modifier whose mapping *is* `Mod5`, so it satisfies the containment test and
  prints after the real names. `Mod1 Alt Meta` shows the same effect for a 3-way mapping
  (`Alt` and `Meta` both map to `Mod1`).
* A modifier whose mapping is `0` satisfies the test for **every** mask and is printed in
  every cell — reachable only with `virtual_modifiers M = none` (probe B: judge prints
  `[ TestVmod ]` for the empty mask).
* Formatting is `"[ "` + one `"<name> "` per printed modifier + `"]"`, i.e. an empty mask
  renders `[ ]` (one space), and names are space-separated with a trailing space before
  `]`.

### R5 — type-compilation rules that change the masks

From `src/xkbcomp/types.c` (the text the tool receives is a *serialized* keymap, so these
parse-time rules apply to it as well):

* `modifiers=` / `map[]` / `preserve[]` masks are clamped to the type's `modifiers=` mask
  **as seen at that point in the source** (`:361` for `map`, `:451` for `preserve`);
  a `preserve[]` value is further clamped to its entry's mask (`:475`).
  Probe C, `EDGE_clamp`: `modifiers= Shift` + `map[Shift+Control]= 2` becomes a second
  level-2 entry for `Shift` — judge prints `[ Shift ]` at level 2, never `[ Shift Control ]`.
* Duplicate entries with the same **named** mask are merged by `AddMapEntry`
  (`:299`, `FindMatchingMapEntry` at `:286`): the entry keeps the *position* of its first
  occurrence, a later `map[]` clobbers its level, a later `preserve[]` overrides its
  preserve (and `preserve[]` before `map[]` creates an entry at level 1, `:426`).
  Probe C, `EDGE_dup`: `map[none]= 1` twice → **one** row, not two (first harness run
  showed the bug, judge `U1F700` rows=1).
* `type->num_levels = def->num_levels` (`:813`), which is `1` or `max(entry level)+1` —
  **level names never extend it**. Probe C, `EDGE_names`: a type with four
  `level_name[]` entries and one level-2 entry has two levels; the key's 3rd/4th syms are
  dropped and the judge prints no rows for them (`U1F70B` → 0 rows).
* The serializer **drops level-1 entries without preserve**
  (`src_xkbcomp_keymap-dump.c:345`) and writes `map[]`/`preserve[]` from the *named* mask,
  so a deactivated entry still appears in the text (identical names → deactivated again on
  reparse). It never writes `type=` for an implicit type and pads each key's level list to
  the type's `num_levels` with `NoSymbol`; resolving the type back with
  `FindAutomaticType` (`src_xkbcomp_symbols.c:1594`) reproduces the original type for every
  key in the corpus (`nlevels_mismatch = 0` over 24 842 keys).

### R6 — where the mapping table comes from (and why the load format matters)

For each virtual modifier, in this order: an explicit `= <mask>` on the serialized
`virtual_modifiers` line; else the OR of the `modifier_map` real masks of the keys that
carry the vmod (compat `interpret … { virtualModifier= M; }`, `src_xkbcomp_keymap.c:447-453`);
else, when the keymap is loaded with format ≥ 2 — the judge's default
(`DEFAULT_INPUT_KEYMAP_FORMAT`; the judge's own `--help` says "The keymap format to use (default: '2')", captured in `receipts/env-pins.txt`) — the canonical
`1 << index` (`src_xkbcomp_keymap.c:466-480`); format 1 leaves it `0`.

Probe A measures exactly this: the same `--format 1` text gives
`Hyper=0, ScrollLock=0` when loaded as format 1 and `Hyper=16384, ScrollLock=32768` when
loaded as format 2, and the judge (format 2) matches the `fmt_v2=True` table. **The C1 tool
must implement the load-format-2 rule**, not the text-implied one; a tool that reads the
text literally will print `Hyper`/`ScrollLock` in every MODIFIERS cell of a format-1
fixture. Consequence for the freeze: `compile-keymap` default output (format 2) writes
those mappings explicitly, so RMLVO fixtures are unambiguous — but `--format 1` fixtures are
a cheap discriminator (see "notes for the freeze").

## Differential

`receipts/mods-diff.txt` — 51 keymaps (0 skipped), **36 533 (keycode, layout, level) rows**,
24 842 key rows (one per key per keymap, summed), 50 350 mask→cell renderings, **30 713 judge invocations** (120.0 s in the final run recorded in the receipt; 48-55 s
on an idle box):

* corpus: 51 RMLVO cases (rules `evdev`, model `pc105`) covering the host sample
  (`br compose:caps`), `us`/`us-intl`/`dvorak`/`colemak`/`altgr-intl`, `br`, `de`,
  `de nodeadkeys`, `de neo`, `fr`, `fr oss`, `ru`, multi-group `us,ru` / `fr,us` /
  `de,ru,us`, `ch fr`/`ch de`, `no dk fi se is gr tr pl cz hu ro hr si sk lt lv ee pt es
  latam it gb`, `ca fr`, `in jp kr bg`, and option sets `terminate:ctrl_alt_bksp`,
  `kpdl:dot`, `kpdl:comma`, `level3:ralt_switch`, `compose:caps`.
* type coverage actually used by keys: `ALPHABETIC, CTRL+ALT, EIGHT_LEVEL,
  EIGHT_LEVEL_ALPHABETIC_WITH_LEVEL5_LOCK, EIGHT_LEVEL_WITH_LEVEL5_LOCK, FOUR_LEVEL,
  FOUR_LEVEL_ALPHABETIC, FOUR_LEVEL_KEYPAD, FOUR_LEVEL_MIXED_KEYPAD, FOUR_LEVEL_PLUS_LOCK,
  FOUR_LEVEL_SEMIALPHABETIC, KEYPAD, ONE_LEVEL, PC_ALT_LEVEL2, PC_CONTROL_LEVEL2,
  PC_CONTROL_SUPER_LEVEL2, PC_SHIFT_SUPER_LEVEL2, TWO_LEVEL` — i.e. all the classes the
  assignment names (ONE_LEVEL, TWO_LEVEL, ALPHABETIC, the FOUR_LEVEL family, KEYPAD,
  PC_*, CTRL+ALT, multi-group) plus the eight-level Level5 family.
* layer 1 (exhaustive): model masks vs `xkb_keymap_key_get_mods_for_level` for **every**
  key/layout/level, model table vs `xkb_keymap_mod_get_name/mask2`, model `num_levels` vs
  `xkb_keymap_num_levels_for_key`. Counters all 0: `table_mismatch, cell_mismatch,
  mask_mismatch, nlevels_mismatch, layout_mismatch, missing_key`.
* layer 2 (end-to-end): for **every distinct single-keysym level of every keymap**, the
  judge was run and the printed rows compared as `(keycode, key name, layout#, level#,
  MODIFIERS cell)`; `judge_mismatch = 0`, `judge_rc = 0` over 30 713 runs. The layout
  *name* column is deliberately excluded (it is not this column's business).
* the model side is fed by `mods.py`'s own `parse_type_block`, not by a harness shortcut, so
  R5's clamping/merging rules are exercised on every type of every keymap.

## Edge probes (`receipts/edge-cases.txt`)

| probe | what it pins | result |
|---|---|---|
| A `--format 1` keymap | load-format rule for vmod mappings | library fmt1 vs fmt2 differ; judge (=fmt2) matches `fmt_v2=True`; 0 mismatches over 725 rows / 612 judge runs |
| B `virtual_modifiers TestVmod=none` | deactivation + mapping-0 printing | entries `[Shift active, TestVmod inactive, Shift+TestVmod inactive]`; level 1 `[ TestVmod ]`, level 2 `[ Shift TestVmod ]`; judge agrees; 0 mismatches |
| C synthetic types | duplicates, `map[none]= 3`, 100-mask cap, level names, clamping | `[0]` (1 row) for duplicate `map[none]`; **0 rows** at level 1 and `[ ]` at level 3 for `map[none]= 3`; 102 entries → **exactly 100** judge rows (`U1F706`); 4 level names with 1 entry → 2 levels; `map[Shift+Control]` clamped to `Shift`; 0 mismatches |
| D host sample | the C1 contract sample | judge `--keysym slash` → `AD01` L3 `[ Mod5 LevelThree ]`, L3 `[ Lock Mod5 LevelThree ]`, L4 `[ Shift Mod5 LevelThree ]`, L4 `[ Shift Lock Mod5 LevelThree ]`, `AB11` L1 `[ ]`; `Return` → `RTRN` L1 `[ ]`; `nosuchsym` → rc 2 + `ERROR: Failed to convert argument to keysym` |

`receipts/unit-checks.txt` — 16 unit checks for rules with no RMLVO witness: out-of-range
level, the cap at `masks_size=3`, unknown-bit passthrough in `effective_mask`, unmapped
virtual modifier named in every cell, deactivation, duplicate merge. All OK.

## Residual risks / what is *not* covered

* **Level selection** (which level a pressed modifier state maps to) is `src/state.c`, not
  this column; `mods.py` only answers "which masks reach level N". The `preserve` masks are
  modelled but unused here by design.
* **Numeric masks** (`map[0x4000]= 2`) are not emitted by the serializer and not exercised
  end-to-end; `effective_mask`'s unknown-bit branch is only unit-checked.
* 100-mask truncation and the `= none` form are only reachable with hand-authored keymaps,
  i.e. outside the C1 contract; both are pinned by probe B/C, not by RMLVO.
* The vmod mapping derivation (R6) is the *parser's* contract. The harness implements it
  text-only (interprets + `modifier_map` + `virtualMods=` + explicit `=`) and the derived
  table equals the library's on all 51 keymaps (`table_mismatch = 0`), which is evidence the
  derivation is text-computable — but the production parser is another seat's code.
* The harness sources the keysym *name → value* table from
  `/usr/include/xkbcommon/xkbcommon-keysyms.h` (2 638 defines) plus the `U<hex>` spelling
  that `KeysymText` emits for Unicode keysyms (`U0463` → `0x01000463`); the argument/header
  path is ExecKeysymNames' seat, and `FindAutomaticType` additionally needs
  `xkb_keysym_is_lower` / `is_upper_or_title` (case tables), which the harness obtains from
  the library's `xkb_keysym_to_lower/upper`. In the tool those must come from the header or
  an embedded table.

## Notes for the freeze (C1 contract / counter)

1. The deliverable's entry points are `mods.parse_type_block(text, name_to_index,
   mod_masks)` → type, then `mods.mods_for_level(type, level)` →
   `mods.format_modifiers(mask, mod_names, mod_masks)`; `mods.level_cells(...)` is the
   composed helper. `mods.mod_table(vmods)` builds the index-ordered
   `(names, masks)` pair with the 8 real modifiers first.
2. Fixtures must be the pinned `compile-keymap` output at its **default format** (2). If a
   clause ever uses `--format 1`, the tool must still apply the format-2 canonical-vmod
   rule (probe A) or every cell of that fixture will be wrong — a free, cheap falsifier.
3. The judge's MODIFIERS cell depends on the keymap's *whole* modifier list (real + virtual),
   so a tool that prints only the type's `modifiers=` names will fail on any key with
   `LevelThree` (`[ Mod5 LevelThree ]`) — this is the single most likely wrong
   implementation, and probe D pins it on the host sample.
4. `masks_size` is 100, not unbounded: `mods_for_level` defaults to it; do not "fix" the
   truncation.

## Hygiene

* Reads only: `/usr/lib/xkbcommon/*`, `/usr/lib/libxkbcommon.so.0.13.2`,
  `/usr/include/xkbcommon/xkbcommon-keysyms.h`, `/usr/share/X11/xkb/**` (grep only).
  `xkbcli` was used only as `compile-keymap`, `how-to-type`, `list`; never `interactive-*`,
  `dump-keymap*`. No `hyprctl`, no compositor or service call, no GUI, no pacman (no
  package was installed: the harness uses Python 3.14.8 + ctypes from the stdlib).
* Every compile/judge run used `env -i PATH=/usr/bin:/usr/lib/xkbcommon` with `HOME` and
  `XDG_CONFIG_HOME` inside `/fast/scratch/hyaku/mado-r49/ExecModsLevel`; no home state was
  written. Scratch was bounded (`ulimit -f 65536`, ~12 MB peak) and deleted before this
  report was finalised, so no scratch path is cited as evidence: every receipt above lives
  in `receipts/`.
* Git: none. No commit, no branch, no fixture repo. Nothing in the lane's index was touched.
