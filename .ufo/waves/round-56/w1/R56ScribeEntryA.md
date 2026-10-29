# R56ScribeEntryA — C1 knowledge entry draft (round 56, wave w1)

Seat role: scribe, leaf (no subagents, no lane edits, no git mutations). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; freeze commit `3423ae285676c2a10273000f4519163472b443db`.

## Deliverables

- Entry draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeEntryA/entry.md` (165 lines, 23569 bytes, sha256 `aab7978fe198495894a5f4b584e3226e9c47acb1a6e4c44ca14b2329a3893462`). Target path in the lane is `corpus/knowledge/hyprland-config-autoreload-r56.md`; it is NOT placed there (C1 integration does that).
- Generator (receipt): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeEntryA/gen-entry.py`. K/H pin cells and quote cells are read from `frozen-tables.json` and the pins; only proposition text and E-row selections are authored in the script.
- Self-check output (receipt): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeEntryA/legs.txt`.

## What I did

1. Read `registration.md` §C1–§C3, `claims-frozen.md`, `frozen-tables.json` (sha256 verified `d50d2b7b…f9af`, working tree and freeze blob both).
2. Opened every pin and read the surrounding function for each K/H row: ConfigWatcher.cpp 1–111 (whole), ConfigValues.cpp 479–503, PropRefresher.cpp 26–36 and 135–160, EventLoopManager.cpp 59–138, legacy ConfigManager.cpp 769–788, 970–1093 (1059–1093 read), 1799–1858, MiscFunctions.cpp 54–93, HyprCtl.cpp 1214–1289, man7 inotify 179–193, 196–240, 254–271. Lines 2133–2134 (`getConfigPaths`), legacy 485/614/731 and HyprCtl 2028 were located by grep and read as single lines. Greps across the pinned set for `watcher()`, `REFRESH_CONFIG_WATCHER`, `REFRESH_ALL`, `getConfigPaths`, `scheduleRefresh`, `registerCommand`, `registerHandler`, `"reload"`.
3. Wrote `gen-entry.py` (`python3 -I`): verifies the frozen tables sha, all 12 pin sha256 against the working tree AND the git blob at the freeze commit (`git cat-file blob`), quote-at-pin-line for all 33 frozen rows, and the sid→pin mapping; authors the 33 propositions; runs a local replica of the row legs (row/len/dup/cells/tok/num); validates 20 extra E rows; renders the entry; re-parses the rendered file for row grammar, provenance order and quote identity.
4. Ran it. Final run output:

```
pins=ok(12)
local_k_h_failed=none
rendered_rows=33/33 provenance_order=ok
cited_S_ids=['S383', 'S384', 'S385', 'S386', 'S387', 'S388', 'S389', 'S390']
wrote .../w1/R56ScribeEntryA/entry.md (23569 bytes, 165 lines)
rc=0
```

5. Read-only host checks (allowed by the seat spec; nothing changed):

```
$ hyprctl getoption misc:disable_autoreload -j
{"option": "misc:disable_autoreload", "int": 0, "set": false }        -> matches H01 (host-getoption.json:1)
$ hyprctl version -j   -> branch v0.56.2, commit efb50993780079460b0cbed1363e2166a2de1d9f, tag v0.56.2, dirty False, version 0.56.2   -> matches H03
$ stat -c '%F|%n|%U' ~/.config/hypr/hyprland.conf  -> regular file|/home/vgpnk/.config/hypr/hyprland.conf|vgpnk
$ readlink -f ~/.config/hypr/hyprland.conf         -> /home/vgpnk/.config/hypr/hyprland.conf (not a symlink)
```

6. Counts in the entry: `grep -c '^| [KH][0-9][0-9] | '` → 33; `grep -c '^| E[0-9][0-9] | '` → 20.

## Entry structure (as written)

- Lines 1–3: `source:` (S383–S390, the only S-ids in the file), `verified-at: 2026-10-28`, `recheck: on-release`, in that order.
- Scope (settled at source level vs UNKNOWN), Chain (9 numbered steps labelled [OBS]/[INF]/[UNKNOWN]), Host reads, Rows (K01–K30 in 5 tables, H01–H03, E01–E20), Limits, How to verify (read-only fenced block).
- Only S383–S390 are cited anywhere in the file (C3 `CITE` set = the 8 new ids).

## Anchor locators the registry rows must carry (for `scope:` and C3 integration)

Derived from the frozen K lines. The registry seat must write these into the `anchor` cell (the `basename:` locator list is what `scope` reads):

```
S383 ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105
S384 ConfigValues.cpp:492
S385 PropRefresher.cpp:148-149
S386 EventLoopManager.cpp:71,128
S387 ConfigManager.cpp:776,1070,1079-1080,1816,1835-1836,1844
S388 MiscFunctions.cpp:65,68
S389 HyprCtl.cpp:1223,1276
S390 inotify.7.html:186,262
```

Registry state at the freeze commit: `corpus/SOURCES.md` has 319 registry rows and **0** rows S383–S390 (`git show 3423ae28:corpus/SOURCES.md`). The `prov`, `source_cell` and `new_rows` legs cannot hold until those rows exist; this is integration work, not done here.

## Defects, ambiguities and disagreements found

1. **Counter and harness absent at the freeze commit.** `git ls-tree 3423ae28 quality/` shows `check-r55-controls.py` and no `c1-r56-autoreload-entry.py` nor `check-r56-controls.py`. The C1 predicate cannot be run as frozen. My local replica covers only the K/H row legs (row, len, dup, cells, tok, num) and the quote identity; it does NOT cover `prov`, `index`, `source_cell`, `scope`, `new_rows`, `pin_hash` or the 10 controls. Those are unverified.
2. **Chain prose in claims-frozen vs the pins.** `claims-frozen.md` §C1 chain says `REFRESH_ALL → hyprctl reload / keyword paths`. The pins show: `hyprctl reload` → `reloadRequest` → `Config::mgr()->reload()` (HyprCtl.cpp:1276, no watcher call); the keyword path calls `Config::watcher()->update()` directly (HyprCtl.cpp:1223–1224). `REFRESH_ALL` reaches `update()` only if its bits include `REFRESH_CONFIG_WATCHER`, and that definition is not in any pin. The entry states this as [UNKNOWN] rather than as the claims chain.
3. **Provider path ambiguity.** `registration.md` §C2 describes "hyprlang era, configProvider hyprlang"; the C1 pins are `src/config/legacy/ConfigManager.cpp`. The legacy file registers its `source` handler on the Hyprlang config (legacy ConfigManager.cpp:614), which suggests the legacy manager is used by the hyprlang provider, but no pin states which provider the 0.56.2 build selects. Recorded as [UNKNOWN] in the entry's Limits.
4. **K07 quote is a prefix of its line.** `fileMask      = IN_CLOSE_WRITE` is a true substring of ConfigWatcher.cpp:55, whose full text ORs `IN_DONT_FOLLOW`. The K07 proposition states both parts; a reader of the quote alone would not see the second.
5. **Host file set.** `host-watched-lstat.txt` lists 40 paths, including `~/.config/omarchy/current/theme/gum.env.conf` and `~/.local/state/omarchy/toggles/hypr/flags.conf`. Neither is named by a line in `host-sources.txt` (18 lines); the nested `source` chain that reaches them is not pinned. Not claimed in the entry.
6. **Behaviour the frozen claims do not settle (carried as UNKNOWN in the entry).** (a) whether a reload rebuilds the watch list; (b) where the `refresh` flag trips on parse (ConfigValue headers not pinned); (c) whether anything calls `update()` at startup (no call in any pinned file other than PropRefresher.cpp:149 and HyprCtl.cpp:1224); (d) editor save behaviour — the file-mask watch has no parent-directory watch, so a rename-into-place save is [INF] unobserved.
7. **`inotify_add_watch` return value unchecked.** ConfigWatcher.cpp:59–62 stores `.wd = inotify_add_watch(...)` with no check; a failed add stays in `m_watches` with the failure value. No pinned log line for it. Recorded as [INF].
8. **Symlink watch semantics rest on C++ and man-page rules not in the pins.** `std::filesystem::status` following links (used at legacy:1828) and `is_symlink` not following (ConfigWatcher.cpp:66) are C++ standard behaviour, cited as [INF]. The `IN_DONT_FOLLOW` reading is from the man page (K30), with the consequence [INF].
9. **C3 interaction.** The 8 new ids are cited by this entry. Unless the registry `used-by` cells of S383–S390 name `corpus/knowledge/hyprland-config-autoreload-r56.md`, C3's `missing` rises by 8 pairs from this entry alone. Integration must add that path to those 8 cells (logged old→new per CORPUS rule 2).

## Not verified / not run

- The frozen counter, the controls harness, `freeze-verify.py`, and the `scope`/`prov`/`index`/`source_cell`/`new_rows` legs: not run (see defect 1).
- Entailment of any proposition by its quote (declared limit; sentence-to-pin audit and non-author closure).
- Live behaviour: no inotify event, reload, editor save or watch-set read was made. No `hyprctl` keyword, dispatch or reload was run.
- Upstream identity of the pinned files beyond the frozen sha256 (not re-fetched).
- The C2 hold-out fixtures (H01–H08) were not looked for or used. No hold-out path was encountered.

## Tooling

No tools installed, upgraded or removed. No pacman, no service change, no ~/.config or ~/.local writes.

## Scratch

`/fast/scratch/hyaku/mado-r56/R56ScribeEntryA/` held the generator and legs; receipts were copied to the deliverable directory before the scratch was removed.
