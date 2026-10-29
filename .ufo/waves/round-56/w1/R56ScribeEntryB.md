# R56ScribeEntryB — C1 entry draft (wave w1, round 56)

Scope: draft the complete C1 knowledge entry per `registration.md` §C1, with the path-list half emphasised. Leaf seat; no subagents; no lane file edited; no git/jj mutation; no registry row written (the S383-S390 rows belong to the sources seat).

## Deliverables

- Entry draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeEntryB/entry.md` (164 lines; sha256 `469219666aafc567123670f4c17d640e2388d9c43dc131b586b7dc6cd3b196ff`). Integration target per registration: `corpus/knowledge/hyprland-config-autoreload-r56.md` (not written here).
- Generator: `.../R56ScribeEntryB/gen-entry.py` (reads `frozen-tables.json` and the fetch pins; writes only the proposition cells; rows K01-K30, H01-H03 and extra E01-E07 are emitted from the frozen quotes and pinned lines, never retyped).
- Template (prose): `.../R56ScribeEntryB/entry.tmpl.md`.
- Seat-side checker: `.../R56ScribeEntryB/check-entry.py` (replicates the row, quote, tok, num, prov legs; scope and source_cell only as requirements, see below).
- Receipt: `.../R56ScribeEntryB/receipts/gen-and-check.txt` (generator and checker output, sha256 of the four files).

## What I did

1. Read `claims-frozen.md`, `registration.md` (§C1, §C2, §C3, seat boundaries), `frozen-tables.json` (sha256 `d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af`, verified), and the pins. Pin sha256 values match `c1.pin_sha256` and `c1.host_pin_sha256` (`PINS_OK`, `HOSTPINS_OK`).
2. Opened each pin and read the surrounding function for every K row: ConfigWatcher.cpp 20-112 (whole watch path), ConfigValues.cpp 479-503, PropRefresher.cpp 130-159, EventLoopManager.cpp 51-138, legacy ConfigManager.cpp 355-381, 475-503, 630, 719-762, 764-786, 1050-1098, 1089-1113, 1794-1863, 2132-2147, MiscFunctions.cpp 54-105, HyprCtl.cpp 1159-1258 and 1260-1289, man7-inotify 169-274, host-getoption/-sources/-version/-watched-lstat.
3. Propositions written by hand for K01-K30 and H01-H03 (each reuses an identifier of its own quote, uses no number outside the quote, its own line, another row's line of the same pin, or 0-3). Generator emits the rows; self-check passed.
4. Host reads, all read-only: `hyprctl getoption misc:disable_autoreload -j`, `hyprctl version -j`, `stat -c '%F %n' ~/.config/hypr/hyprland.conf`, `readlink -f`, `grep -c '^source'` and `grep -n source` on `~/.config/hypr/hyprland.conf` and on `~/.config/omarchy/current/theme/hyprland.conf`, `grep -rn 'gum.env'` over `~/.local/share/omarchy/default/hypr`, `~/.config/hypr`, `~/.config/omarchy/current`, `stat` on `gum.env.conf` and the theme file. No `hyprctl` keyword, dispatch or reload; no write under `~/.config` or `~/.local`.

## Commands and decisive output

```
$ python3 -I .../R56ScribeEntryB/gen-entry.py
WROTE .../R56ScribeEntryB/entry.md K=30 H=3 E=7          rc=0

$ python3 -I .../R56ScribeEntryB/check-entry.py .../R56ScribeEntryB/entry.md
CHECK prov_src=[S383..S390] cited_by_entry=[S383..S390]
CHECK rows_ok K=30/30 H=3/3 quote_ok K=30/30 H=3/3
CHECK tok_num_content=33/33
CHECK missed=none                                          rc=0

$ awk 'NR<=30 && /^(source|verified-at|recheck):/' entry.md
1: source: S383 (...) ... S390 (inotify(7) man page); host captures ...
2: verified-at: 2026-10-28
3: recheck: on-release

$ hyprctl getoption misc:disable_autoreload -j
{"option": "misc:disable_autoreload", "int": 0, "set": false }
$ hyprctl version -j | sed -n 3p        -> "commit": "efb50993780079460b0cbed1363e2166a2de1d9f"
$ stat -c '%F %n' ~/.config/hypr/hyprland.conf   -> regular file /home/vgpnk/.config/hypr/hyprland.conf
$ grep -c '^source' ~/.config/hypr/hyprland.conf  -> 18
$ grep -rn gum.env ~/.local/share/omarchy/default/hypr  -> envs.conf:3:source = ~/.config/omarchy/current/theme/gum.env.conf
$ stat -c '%F %n' ~/.config/omarchy/current/theme/gum.env.conf -> regular file
$ git -C <lane> show 13f0acbe...:corpus/SOURCES.md | grep -cE '^\| S38[3-9] |^\| S390 '  -> 0   (same at HEAD 2aa347b1)
$ git -C <lane> cat-file -t 3423ae285676c2a10273000f4519163472b443db  -> commit
$ git -C <lane> ls-tree --name-only HEAD .ufo/waves/round-56/fetch/ | wc -l  -> 12
$ git -C <lane> cat-file -e HEAD:quality/counters/c1-r56-autoreload-entry.py -> absent (fatal: path does not exist)
```

Required anchors the registry rows must cover for `scope:<id>` (computed from the frozen K lines; the registry basename is the last path component of `pin_suffix`, so the anchor must say `ConfigWatcher.cpp:`, not `Hyprland-ConfigWatcher.cpp:`):

- S383 `ConfigWatcher.cpp`: 33, 34, 46, 54, 55, 56, 60, 67, 69, 105
- S384 `ConfigValues.cpp`: 492
- S385 `PropRefresher.cpp`: 148, 149
- S386 `EventLoopManager.cpp`: 71, 128
- S387 `ConfigManager.cpp` (pin `Hyprland-legacy-ConfigManager.cpp`): 776, 1070, 1079, 1080, 1816, 1835, 1836, 1844 (a single range such as `1070-1844` does not contain 776)
- S388 `MiscFunctions.cpp`: 65, 68
- S389 `HyprCtl.cpp`: 1223, 1276
- S390 `inotify.7.html`: 186, 262

Note on S387: the pin is `Hyprland-legacy-ConfigManager.cpp`, mapped to `pin_suffix` `src/config/legacy/ConfigManager.cpp`; its basename is `ConfigManager.cpp`. S390 maps to `man7/inotify.7.html`, basename `inotify.7.html`. The `Hyprland-` prefix is a seat-local pin name and is not part of the registry basename.

## Entry content (summary)

- Provenance trio first (lines 1-3). Scope (what is settled at source level; what stays UNKNOWN: no filesystem event, reload, save or editor write observed; `REFRESH_ALL` membership open).
- Chain (9 steps): declaration → `update()` → `setWatchList` masks → event-loop callback → `onInotifyEvent` → init callback → `reload()` → refresh → other entry points and inotify(7) semantics.
- Path list: `resetHLConfig` clears (776) and re-adds the main path (779) on construction (630), reload (731) and verify (755); `handleSource` steps (bogus; glob with `GLOB_TILDE` and error return; match status and "inaccessible" early return; regular file pushed before its nested parse; directory and non-regular skipped); pre-order depth-first recursion; no dedupe; no visited set; missing targets never listed; `absolutePath` cases (`~`, `~user`, `/`, `./`, `../`, other `.`-leading, bare names); resolution base for the main file, for nested files (`m_configCurrentPath` set to the nested `value`), and for symlinked nested files (link directory, not target).
- Rows: K01-K30, H01-H03 as frozen; E01-E07 extra (uncounted).
- Limits and How-to-verify (read-only commands; the counter line is present but marked as runnable only once the wave's counter lands at `REV`).

## Defects, ambiguities, and gaps found

1. **Watch-list rebuild after a reload is not pinned.** `Hyprland-legacy-ConfigManager.cpp:1070` schedules `REFRESH_ALL`; `Hyprland-PropRefresher.cpp:148-149` calls `Config::watcher()->update()` only when `REFRESH_CONFIG_WATCHER` is set. No pin shows `REFRESH_ALL` (grep over all pins finds it only at 1070). `claims-frozen.md` line 25 presents the chain as ending in `REFRESH_ALL`; the entry states this as UNKNOWN rather than closing it. Input: `grep -n REFRESH_ALL fetch/*` → one hit.
2. **Declared divergence wording vs the code (registration §C2).** The divergence list names "GLOB_TILDE `~user` forms". In Hyprland 0.56.2 the leading `~` is replaced by `absolutePath` (`Hyprland-MiscFunctions.cpp:64-66`) before `glob` is called (`legacy:1816`), so `GLOB_TILDE` never acts on a leading tilde, and `~user/x` becomes `$HOME` followed by `user/x` (no lookup, no slash). The watch-plan model's `~` branch (`--home` + RAW[1:]) reproduces that concatenation, so it does not diverge there; the listed divergence is at best a mis-description. The entry records the actual behaviour (E01, K25 and the path-resolution section).
3. **Registry rows absent.** `corpus/SOURCES.md` at base `13f0acbe` and at HEAD `2aa347b1` contains no S383-S390 row (count 0). The `source_cell`, `scope`, and `new_rows` legs cannot be evaluated by me; the required anchors are listed above for the sources seat.
4. **Counter and harness absent at HEAD.** `quality/counters/c1-r56-autoreload-entry.py` and `quality/check-r56-controls.py` are not in the lane HEAD tree. `MADO_AUTORELOAD_ENTRY` and `MADO_R56_CONTROLS` could not be run. The frozen commit `3423ae28…` exists (`cat-file -t` → commit).
5. **Source-level unknown in the frozen anchors.** `inotify_add_watch` return value is unchecked (`Hyprland-ConfigWatcher.cpp:60`, E02); `inotify_init1` failure leaves the watcher without a descriptor (21-26; event loop 127). Neither is modelled by the watch-plan tool, which the registration does not list as a divergence. Declared as a limit in the entry.
6. **`hyprctl keyword source` watch gap (inference).** The `source` keyword appends to `m_configPaths` through `handleSource` (1836) and the dispatcher's `source` branch (`Hyprland-HyprCtl.cpp:1194-1208`) does not call `update()`. The entry labels this as inference: the handler being invoked by `parseDynamic` is not in the pins. Not in the frozen claims; reported only.
7. **Cycle behaviour.** No visited set or depth limit appears in `handleSource` (1802-1855); the watch-plan tool's cap of 16 is a declared divergence. The entry labels unbounded recursion on a self-sourcing file as inference.
8. **`HOME` unset.** `absolutePath` calls `std::string(getenv("HOME"))` (`MiscFunctions.cpp:65-66`) without a null check: undefined behaviour if unset. Source reading, not exercised; in Limits.

## Propositions: checks against the legs

- `row`, `quote`, `tok`, `num`, prop length (>=40 K / >=20 H), no `|`, no backslash, no backtick, no duplicate proposition: all 33 pass in `check-entry.py` and in the generator's self-check. `quote` is the frozen string, read from the tables, never typed.
- `prov`: `source:` line lists S383-S390; `verified-at: 2026-10-28` once; `recheck: on-release`; order holds within the first 30 lines.
- `content`: 33/33 by my replica of tok and num. The counter's own regexes are the same as in registration §C1; I did not run the counter.

## Not verified

- The counter, harness, controls and the freeze commit's file set (absent at HEAD). Entailment: the propositions are bounded readings checked lexically; no sentence-to-pin audit was run (that is the wave-2 and non-author closure, per registration).
- Any filesystem event, save, editor write, reload, or `hyprctl` keyword effect: none observed; all such statements are UNKNOWN or labelled inference in the entry.
- `REFRESH_ALL` membership, `m_configPaths` declaration, `getMainConfigPath`, hyprlang `parseFile`/`source` pre-processing, and the glob collation: not in the pins.
- The H02 host listing is a captured line; the live file line 13 holds the same text (checked by `grep -n`), but the capture itself was not regenerated.

## Hold-out

Not touched. I did not look for or read any `fixtures/c2-holdout` or other sealed path.

## Installs and tooling

None. No pacman, uv, npm or cargo installs were made; the only tool used was the host's `python3 -I`, `git`, `sha256sum`, `stat`, `grep`, `sed`, `awk`. `hyprctl` was used only in its read-only `getoption` and `version` forms.

## Scratch and cleanup

Scratch dir `/fast/scratch/hyaku/mado-r56/R56ScribeEntryB/` was created empty and is removed before yield. The generator and checker write only inside the seat directory; no `/tmp` file was written.
