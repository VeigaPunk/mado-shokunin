# README draft — index row and Frontier bullet for `knowledge/hyprland-input-devices-r46.md`

Seat ScrReadme, round 46 wave w1. Anchors below are computed with `grep -n` against the lane at freeze
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec` (`corpus/README.md`, 323 lines); none of them is typed from memory.
Nothing in the lane was edited: this file is the draft the L1 applies.

## 1. Index row (verbatim, one line, insert as `corpus/README.md:74`)

```text
| `knowledge/hyprland-input-devices-r46.md` (MADO-R46-1, round 46; input-device plane, runtime state agreement) | How `input { kb_* }` and a keyed `device { name = X ... }` block become what `hyprctl devices -j` prints on Hyprland 0.56.2 (efb50993) with hyprlang 0.6.8: the six XKB names a keyboard stores, five of them printed by the dump, each taken from the device block value when the block sets it, else the global `input:kb_*`, else the `us` and empty defaults; the `STRVAL_EMPTY` marker read as the empty string; the `us` fallback after a keymap that does not compile; a pointer's `scrollFactor` as the device block's `scroll_factor` clamped 0..100 only when explicitly set and `-1` otherwise, with the global `input:scroll_factor` never reaching the field; `hl-virtual-keyboard*` naming with an overridden keymap that `setKeymap` skips; and device-name normalization (lower-case, space/newline/comma to `-`, `-1`/`-2` duplicates); join tool `tools/mado-devices.py` (per keyboard AGREE/DIFFER/FALLBACK/VIRTUAL, per mouse AGREE/DIFFER, per block MATCHED/NO_SUCH_DEVICE, verdict OK/DIFFER/NO_KEYBOARDS/STALE_BLOCK/NOT_COMPARED); live census 10 keyboards (9 AGREE, 1 VIRTUAL) and 4 pointers AGREE at -1.00, verdict OK | S316-S325 |
```

Placement: the table's last row is the round-45 row, `corpus/README.md:73`
(`grep -n '^| `knowledge/hyprland-monitor-rule-r45.md`' corpus/README.md` → `73:`). Insert directly after it, with no
blank line, so the new row becomes line 74 and the table stays contiguous. `build-pos.py:103` inserts a placeholder row
with the same path and third cell but `draft` in the Holds cell; that placeholder must be replaced by this row, not kept
alongside it (two column-0 rows for the entry fail the counter's single-row rule).

## 2. Frontier bullet (verbatim, insert as `corpus/README.md:108`, first bullet under `## Frontier`)

```text
- Round 46 moves the input-device plane onto sourced ground ([input devices](knowledge/hyprland-input-devices-r46.md), rows S316-S325): how `input { kb_* }` and a keyed `device { name = X ... }` block become the per-keyboard XKB names and the per-pointer `scrollFactor` that `hyprctl devices -j` prints, with a read-only join (`tools/mado-devices.py`). Still open: the XKB compile itself (whether a layout/variant pair exists in xkeyboard-config), the per-device settings the dump never prints (`repeat_rate`, `repeat_delay`, `numlock_by_default`, `enabled`, `keybinds`, `sensitivity`, `accel_profile` and the libinput knobs), hyprlang variables and `{{ }}` expressions, and the Lua config of later releases.
```

Placement: `## Frontier` is `corpus/README.md:106` (`grep -n '^## Frontier'` → `106:`); its first bullet is
`corpus/README.md:108` (round 45). Newest-first order, so the round-46 bullet goes above it, followed by a blank line
like every other bullet in that list. Do not touch the `Index completeness does not retire these unresolved surfaces:`
list below the bullets — the round-46 item is a movement, not a retirement.

## 3. What the row and bullet claim, and where each clause comes from

Every clause in the Holds cell is the entry's own sentence, not new measurement:

| clause | entry location |
|---|---|
| six XKB names read per keyboard, five of them printed by the dump | entry step 3 (chain), pin `Hyprland-InputManager.cpp:1213-1238` (six `getDeviceString` calls at `:1225-1230`); dump fields `Hyprland-HyprCtl.cpp:785-802` |
| block value counts only when the user set it | step 3, `Hyprland-ConfigManager.cpp:1115-1123` |
| `STRVAL_EMPTY` read as the empty string | step 3, `Hyprland-ConfigManager.cpp:1156-1168` (read at `:1163`) |
| `us` fallback after a keymap that does not compile | step 4, `Hyprland-IKeyboard.cpp:101-116` |
| `scrollFactor` clamped 0..100 only when explicitly set, else `-1` | step 5, `Hyprland-InputManager.cpp:1376-1383` |
| global `input:scroll_factor` never reaches the field | step 5, `Hyprland-ConfigValues.cpp:290-300` |
| `hl-virtual-keyboard*`, overridden keymap, `setKeymap` early return | step 6, `Hyprland-protocols-VirtualKeyboard.cpp:11-30`, `Hyprland-VirtualKeyboard.cpp:36-44`, `Hyprland-IKeyboard.cpp:60-64` |
| name normalization and duplicate suffixes | step 7, `Hyprland-MiscFunctions.cpp:777-789`, `Hyprland-InputManager.cpp:2119-2131` |
| live 9 AGREE / 1 VIRTUAL / 4 pointers at -1.00 / OK | entry "Live host run", receipt `.ufo/waves/round-46/receipts/live-devices-host-l1.txt` |

The four open items in the bullet are the entry's `## Limits` list (XKB compile; `repeat_rate`/`repeat_delay`/
`numlock_by_default`/`enabled`/`keybinds`/`sensitivity`/`accel_profile`/libinput; variables, `{{ }}`, directives;
Lua config), each kept in the entry's own words.

## 4. Checks run on this draft

1. Cell arithmetic (the counter's own clause-f test, `quality/counters/c2-r46-input-device-entry.py:652-663`):
   the row is column 0, matches `^\| \`knowledge/hyprland-input-devices-r46.md\``, splits to exactly three cells after
   `strip("|").split("|")`, and the third cell's `S316-S325` expands to `S316`…`S325` — the ten cited ids and nothing
   else. No cell contains a `|`, so the split cannot over-count.
2. Shape against the round-45 row (`corpus/README.md:73`): same three cells, same `S###-S###` third cell, `(MADO-R46-N,
   round 46; <surface>)` label form, single line, no trailing spaces.
3. Row and bullet reuse only entry facts (table in §3) plus the tool name the C1 claim installs at
   `tools/mado-devices.py`; no live value, count or verdict is invented here.
4. Scope: the round-45 closure item D1 (re-running the round-45 w2 falsification) is routed non-claim work
   (registration § Routed non-claim work). It is deliberately absent from this row and bullet: the Frontier entry
   describes this entry's movement, and no round-45 re-run result is claimed anywhere in this draft.

## 4b. Pin checks behind the row (run this seat, read-only)

Each locator the Holds cell leans on was re-read in `.ufo/waves/round-46/fetch/` and the anchor is present in the named
line range: `Hyprland-InputManager.cpp:1213-1238` (`applyConfigToKeyboard`, six `getDeviceString` calls at `:1225-1230`),
`:1376-1383` (`deviceConfigExplicitlySet(devname, "scroll_factor")` at `:1377`, `std::clamp(..., 0.F, 100.F)` at `:1378`,
`std::nullopt` at `:1382`), `:2119-2131` (`getNameForNewDevice`); `Hyprland-ConfigManager.cpp:1115-1123`
(`m_bSetByUser` fallback), `:1156-1168` (`getDeviceString`, `STRVAL_EMPTY` read at `:1163`);
`Hyprland-ConfigValues.cpp:290-300` (`input:scroll_factor`); `Hyprland-IKeyboard.cpp:60-64` (overridden early return),
`:101-116` (`m_currentRules.layout  = "us";` at `:113`); `Hyprland-MiscFunctions.cpp:777-789`
(`deviceNameToInternalString`, `case ',': return '-';` at `:782`); `Hyprland-protocols-VirtualKeyboard.cpp:11-30`
(`hl-virtual-keyboard` at `:12`); `Hyprland-VirtualKeyboard.cpp:36-44` (`m_keymapOverridden = true;` at `:41`).

Two wording consequences, both applied to the row above:

1. The entry says "a stored `[[EMPTY]]`". The literal `[[EMPTY]]` does not occur in the hyprlang pin
   (`.ufo/waves/round-46/fetch/hyprlang-config.cpp`) nor in `/usr/include/hyprlang.hpp`; what the pinned Hyprland
   source carries is the symbol `STRVAL_EMPTY` (`Hyprland-ConfigManager.cpp:520-547` defaults, `:1163` the read). The
   row therefore names `STRVAL_EMPTY`, not the literal string. This is a row-wording choice, not an entry defect — the
   entry's own parenthetical already says "STRVAL_EMPTY marker".
2. The entry's "six keymap names" is six *read* (`kb_file` included) but the dump prints five (rules, model, layout,
   variant, options — `Hyprland-HyprCtl.cpp:785-802`), so the row says "six … five of them printed by the dump".

The verdict ladder in the row (`OK`/`DIFFER`/`NO_KEYBOARDS`/`STALE_BLOCK`/`NOT_COMPARED`, in that test order) is the
reference's own docstring (`.ufo/waves/round-46/l1-draft/mado-devices.py:87-89`), not a round result.

## 5. Limits of this seat

- No counter was run against the lane (clause f needs the entry to exist at REV, which only the L1 commit supplies);
  check 1 is the clause's own regex logic applied to the draft text, not the counter's verdict.
- The Holds cell is deliberately long because the index's round-45 and round-43 rows are equally long; shortening it
  would drop a clause the entry's step list names.
- No U-number is attached (round 45 carried `U5`): the round-46 registration names the surface "the input-device
  plane" without a U token, and the entry's `ground:` line uses the same wording. If the L1 wants a U token, U6 is the
  input surface the round-15 entry covered, but the registration does not claim it — so this draft does not either.
- Nothing was installed, upgraded or fetched for this seat; no compositor call, no git mutation, no scratch tree was
  needed (the check runs in memory over the lane's read-only README bytes).
