# R56ScribeIndex — corpus/README.md integration drafts (L1 applies; drafts only)

Sources of truth: `.ufo/waves/round-56/claims-frozen.md` and `registration.md` (C1 entry, rows S383-S390, K01-K30, H01-H03).

## 1a. Coverage-map row (insert as the line directly after the round-55 row, `knowledge/hyprland-keyboard-repeat-numlock-r55.md`, README line 82; the row is the exact line in `02-index-row.txt`)

The row sits inside the `|Note|Holds|Sources|` table (the gate `quality/check-index-rows.py` requires that), with 3 non-empty cells, no `|` inside a cell, and only registry ids S383 and S390 as `S###` tokens.

## 1b. Frontier bullet (insert as the FIRST bullet under `## Frontier`, README line 117, above the round-55 bullet)

- Round 56 moves the Hyprland config auto-reload chain onto sourced ground ([config auto-reload](knowledge/hyprland-config-autoreload-r56.md), rows S383-S390 plus the host pins under `.ufo/waves/round-56/fetch/`): how `misc:disable_autoreload` reaches `CConfigWatcher`'s watch list (the main config and every regular file its `source =` lines reach, with glob and `~` rules), which inotify masks are registered for files, directories and symlink canonical targets, and how an event leads through `CConfigManager::reload` to `REFRESH_ALL` on Hyprland 0.56.2. A read-only join, `tools/mado-watchplan.py`, predicts the watch list from config bytes and joins the option to `hyprctl getoption -j`; constructs it does not model are reported `unsupported`, never guessed. Still open: no filesystem event was generated, no config file was saved and no reload was observed, so inotify delivery and the drawn effect of a reload stay unmeasured; the Lua config provider of later releases and runtime `hyprctl keyword misc:disable_autoreload` are outside this round.

## 1c. Gating (L1 must check before applying)

- Apply 1a and 1b only if `MADO_AUTORELOAD_ENTRY` reads `TARGET_MET` (C1) and, for the tool sentence in 1b, `MADO_R56_C2 ... verdict=TARGET_MET` (C2). If C2 is `TARGET_MISSED`, delete the `tools/mado-watchplan.py` clauses from 1a (Sources cell) and 1b before applying, or the index gate fails on a missing path.
- Re-read the landed entry: the Holds cell must share a 5-word sequence with the entry bytes (`check-index-rows.py` `holds-no-overlap` is a WARN; a WARN is a review item, not a block).
- Do not add the 1b bullet's "Still open" wording as a claim of coverage: it names what is NOT observed.
- Pre-existing table split (recommended, L1 decides): `corpus/README.md` line 79 is blank, so the coverage-map table ends at line 78 and the r52, r52-errata and r55 rows (lines 80-82) are `row-outside-map` for `quality/check-index-rows.py`; the base `3423ae28` already reports 3 such errors (`receipts/rows-A-base.txt`). Delete line 79 so the table is contiguous; with that deletion and the row, the new row's own errors are only the pending `S383`, `S390` and `tools/mado-watchplan.py` (`receipts/index-gates-dryrun.txt`).

## 1d. Existing rows this text must not contradict

- `corpus/README.md:8` — "A new index row does not close a behavioral gap."
- `corpus/README.md:98` (route table, *Hyprland config, binds, rules and display*) — limit "Parsed declarations do not prove dispatcher behavior, rule effects or exec-once results." The new row does not change that limit; it adds reload-mechanism sourcing only.
- `corpus/README.md:12` (`hyprland-config-plane.md`) — include order is precedence; "proven by `hyprctl getoption`". The new entry is a source-level reading of the watch list, not a precedence proof.
- `corpus/README.md:35` (`hyprland-config-era-r12.md`) — host 0.56.2 `configProvider: hyprlang`; upstream Lua-era claims stay `[INF-docs]`. The new Frontier wording keeps the Lua provider open, consistent with this.
- `corpus/README.md:131-134` — "Index completeness does not retire these unresolved surfaces."
- `corpus/README.md:82` (r55 row) and `:117` (r55 bullet) — the house form for "no key was pressed / no event observed" limits; 1a/1b follow it.
