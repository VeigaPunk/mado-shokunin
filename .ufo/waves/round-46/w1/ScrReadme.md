# Report — ScrReadme (round 46, w1): README index row + Frontier bullet

Status: **complete**. Draft delivered at `.ufo/waves/round-46/w1/ScrReadme/readme.md`; the L1 applies it. No lane file was
edited, no clone or scratch tree was created, no counter was run, nothing was installed.

## Deliverable

`.ufo/waves/round-46/w1/ScrReadme/readme.md` holds, verbatim and in application order:

1. The index row for `knowledge/hyprland-input-devices-r46.md` — one column-0 line, three cells
   (`` `knowledge/…` (MADO-R46-1, round 46; input-device plane, runtime state agreement) `` | Holds | `S316-S325`).
2. Its placement: after `corpus/README.md:73`, the round-45 row (computed:
   `grep -n '^| `knowledge/hyprland-monitor-rule-r45.md`' corpus/README.md` → `73:`), so the new row is line 74.
3. The `## Frontier` bullet — inserted above `corpus/README.md:108`, the round-45 bullet (`grep -n '^## Frontier'` →
   `106:`; `grep -n '^- Round 45 moves'` → `108:`), newest-first, followed by a blank line.
4. A clause-by-clause provenance table (§3) and the pin checks behind it (§4b).

## Findings

**F1 — the row satisfies the C2 counter's index-row test.** Simulated the counter's own logic
(`quality/counters/c2-r46-input-device-entry.py:652-663`) in memory over the lane README with the row inserted:
`pat.match` true, `strip("|").split("|")` → **3 cells**, third cell `S316-S325` expands to exactly `S316`…`S325` (the ten
cited ids), **1** column-0 row for the entry, inserted at line 74 between the round-45 row and the blank line after the
table. No cell contains a `|`, so the split cannot over-count. This is the clause's regex logic applied to the draft —
not the counter's verdict (clause f needs the entry at REV).

**F2 — `build-pos.py` leaves a placeholder that must be replaced, not kept.** `l1-draft/build-pos.py:103` inserts
`` | `knowledge/hyprland-input-devices-r46.md` (MADO-R46-1, round 46) | draft | S316-S325 | ``. That placeholder already
passes clause f, so the positive control P can stay green while the landed index row still reads `draft`; two column-0
rows for the entry would fail the single-row rule. The L1 must swap the placeholder for §1's row in the data commit.

**F3 — two wording consequences from re-reading the pins (both applied).**
(a) The entry says "a stored `[[EMPTY]]`", but the literal `[[EMPTY]]` occurs in neither the hyprlang pin
(`.ufo/waves/round-46/fetch/hyprlang-config.cpp`, `grep` exit 1) nor `/usr/include/hyprlang.hpp` (`grep` exit 1); the
pinned Hyprland source carries the symbol `STRVAL_EMPTY` (`Hyprland-ConfigManager.cpp:520-547` defaults, read at
`:1163`). The row therefore names `STRVAL_EMPTY` — the entry's own parenthetical already does, so this is row wording,
not an entry defect.
(b) The entry's "six keymap names" is six *read* (`kb_file` included, `Hyprland-InputManager.cpp:1225-1230`) but the
dump prints five (rules, model, layout, variant, options — `Hyprland-HyprCtl.cpp:785-802`); the row says "six … five of
them printed by the dump".

**F4 — no U-number in the row.** Round 45's row carries `U5`. The round-46 registration names the surface "the
input-device plane" with no U token, and the entry's `ground:` line uses the same wording, so the row carries none. U6 is
the input surface the round-15 entry covered, but the registration does not claim it — flagged for the L1, not decided
here.

**F5 — the round-45 closure item D1 stays out of this row and bullet.** It is routed non-claim work (registration
§ Routed non-claim work). The Frontier entry describes this entry's movement only; no round-45 re-run result is claimed.

## Evidence (commands and outputs)

- Anchors: `grep -n '^| `knowledge/hyprland-monitor-rule-r45.md`' corpus/README.md` → `73:`; `grep -n '^## Frontier'` →
  `106:`; `grep -n '^- Round 45 moves'` → `108:`; `wc -l` → `323`.
- Pin anchors re-read in `.ufo/waves/round-46/fetch/` (all present in the named range): `Hyprland-InputManager.cpp`
  `:1213-1238` (`applyConfigToKeyboard`), `:1226-1231` (`kb_layout` lookup), `:1376-1383`
  (`deviceConfigExplicitlySet(devname, "scroll_factor")` at `:1377`, `std::clamp(…, 0.F, 100.F)` at `:1378`,
  `std::nullopt` at `:1382`), `:2119-2131` (`getNameForNewDevice`); `Hyprland-ConfigManager.cpp` `:1115-1123`
  (`m_bSetByUser`), `:1156-1168` (`getDeviceString`, `STRVAL_EMPTY` at `:1163`); `Hyprland-ConfigValues.cpp` `:290-300`
  (`input:scroll_factor`); `Hyprland-IKeyboard.cpp` `:60-64` (overridden early return), `:101-116`
  (`m_currentRules.layout  = "us";` at `:113`); `Hyprland-MiscFunctions.cpp` `:777-789` (`deviceNameToInternalString`,
  `case ',': return '-';` at `:782`); `Hyprland-protocols-VirtualKeyboard.cpp` `:11-30` (`hl-virtual-keyboard` at
  `:12`); `Hyprland-VirtualKeyboard.cpp` `:36-44` (`m_keymapOverridden = true;` at `:41`).
- Verdict ladder `NOT_COMPARED 5 | DIFFER 1 | NO_KEYBOARDS 3 | STALE_BLOCK 4 | OK 0`: reference docstring
  `.ufo/waves/round-46/l1-draft/mado-devices.py:87-89`.
- Live census in the row (10 keyboards: 9 AGREE, 1 VIRTUAL; 4 pointers AGREE at -1.00; verdict OK): entry "Live host
  run" and `.ufo/waves/round-46/receipts/live-devices-host-l1.txt` — quoted from the entry, not re-run by this seat.

## Gates

- No build, lint, test, formatter or counter run: this is a docs seat and clause f is only decidable at the L1's data
  commit. The single executed check is the in-memory clause-f simulation (F1); it is not a counter receipt.
- Host guards held: no `hyprctl` call, no compositor mutation, no git/jj mutation, no package transaction, no scratch
  dir (nothing to clean up), no write outside the seat dir and this report.

## Touched surfaces

- `.ufo/waves/round-46/w1/ScrReadme/readme.md` (new, draft).
- `.ufo/waves/round-46/w1/ScrReadme.md` (this report).

Nothing else in the lane was created, edited or deleted; `corpus/README.md`, `corpus/SOURCES.md`, the entry, the lesson,
the counters, fixtures, pins, controls and the registration are untouched.

## Out of scope (for the L1)

Entry body, SOURCES rows S316-S325, the lesson `## Gate`, the tool `tools/mado-devices.py`, the counters and their
fixtures — none drafted or changed here. The row and bullet are the only two README edits this seat proposes.
