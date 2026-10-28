# R55W2ScoutCallers — seat report (wave w2, falsify)

Re-issue of the w1 callers item that died on a provider limit. Read-only research; complete.

## What was attacked

The C1 entry's reapplication story: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` says (chain step 3, E08) that applyConfigToKeyboard is called from setupKeyboard, and says nothing else about when `input:repeat_rate`, `input:repeat_delay`, `input:numlock_by_default` are re-applied. The question: is that right, and what is missing?

## Method

Fetched the Hyprland tarball at the pinned commit efb50993780079460b0cbed1363e2166a2de1d9f (one codeload.github.com read) into scratch, grepped the single-commit tree, and byte-compared it against the lane pins: `cmp` IDENTICAL for `Hyprland-InputManager.cpp`, `Hyprland-ConfigValues.cpp`, `Hyprland-legacy-ConfigManager.cpp` in `.ufo/waves/round-55/fetch/`, so all cited line numbers sit on the same bytes the entry pins. No C++ LSP server/device was available in this session; text grep over the pinned tree with cross-checked anchors is the method used, and its unavailability is recorded in the deliverable. No new tools installed (operator tooling rule: nothing needed beyond curl/grep). No host state changed; `hyprctl keyword` was deliberately NOT run (host guard forbids state changes), so all findings are source-level.

## Decisive evidence (full map in .ufo/waves/round-55/w2/R55W2ScoutCallers/callers.md)

- `applyConfigToKeyboard` — def InputManager.cpp:1213, exactly TWO callers: setupKeyboard (:1195, def :1135) and the setKeyboardLayout loop (:1208, def :1206). setupKeyboard is reached from physical (Compositor.cpp:474), virtual-protocol (InputManager.cpp:89-90 → :1130) and pre-built (:1114) keyboard constructors.
- `setKeyboardLayout` — exactly FIVE callers: legacy config reload (postConfigReload :977, guarded `!m_isFirstLaunch`, from reload() :750; reload runs on file change via watcher :1079-1081 and on `hyprctl reload` via reloadRequest :1274), compositor start once (Executor.cpp:49), `hyprctl keyword` (HyprCtl.cpp:1204 — legacy parser only, guard :1162; triggers on any command whose name CONTAINS "input" or "device", after parseKeyword :1190 stores the value), `hyprctl -r` force flag (HyprCtl.cpp:2130 under `if (reloadAll)` :2126), and the PropRefresher (PropRefresher.cpp:60).
- `REFRESH_INPUT_DEVICES` (PropRefresher.hpp:11) — one handler: PropRefresher.cpp:59-60 inside refreshProp (:55), run via doLater from scheduleRefresh (:29-38). Producers: lua `hl.device` always (LuaBindingsConfigRules.cpp:1098); lua `hl.config` per-key dynamic sets schedule the option's own refreshBits (:1008) — `numlock_by_default` (:277) and `repeat_rate` (:279) carry the flag, **`repeat_delay` does not (ConfigValues.cpp:280)**; full reloads schedule the superset REFRESH_ALL (legacy :1070, lua :850).

## Verdicts

- E08 / chain step 3 ("applyConfigToKeyboard is called from setupKeyboard", InputManager.cpp:1195): **SURVIVES** — quote, line and enclosing function all confirmed; the "one of the callers" phrasing is exact (the other caller is the :1208 loop).
- Entry reapplication coverage: **INCOMPLETE — no falsifiable claim present beyond device setup**. Precise greps of the entry for `reload`, `refresh`, `keyword`, `setKeyboardLayout`, `dispatch`, `REFRESH_INPUT` all return no matches, so nothing the entry asserts is contradicted; the WHEN map (§4 of callers.md: 7 routes) is new material the entry could absorb. NOT-REPRODUCED as a falsification; recorded as a coverage gap.
- New adjacent fact: the `repeat_delay` refresh-flag asymmetry — under the dynamic/lua path it is the only one of the three keys not re-applied until a full reload (declarations observed; runtime consequence [INFERENCE], not exercised).

## Not verified / limits

- Source-level only, pinned commit; no running-compositor behaviour was exercised (QUALITY 104 holds: no keypress, no client, no keyword dispatch).
- `newKeyboard(SP<IKeyboard>)` overload has no in-tree caller; plugin use UNVERIFIED (no plugin tree fetched).
- The legacy reload double-apply (direct :977 + REFRESH_ALL :1070) is expected to short-circuit per keyboard at the entry's K07 gate; expected, not exercised.

## Hygiene

Lane untouched (no tracked-file edits, no git/jj commands against lane or fleet repo, no mutation tests — research seat, nothing to restore). Scratch /fast/scratch/hyaku/mado-r55/R55W2ScoutCallers removed after receipts were copied. Receipts: line-numbered excerpts of every quote, sha256 of every cited file, fetch provenance.

Report: .ufo/waves/round-55/w2/R55W2ScoutCallers.md
Deliverable: .ufo/waves/round-55/w2/R55W2ScoutCallers/callers.md
Receipts: .ufo/waves/round-55/w2/R55W2ScoutCallers/receipts/
