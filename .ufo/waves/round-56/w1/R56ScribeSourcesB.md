# R56ScribeSourcesB — SOURCES.md rows S383–S390 (round 56, wave w1)

Scope: draft the eight registry rows for the C1 autoreload entry (`corpus/knowledge/hyprland-config-autoreload-r56.md`), with the gate and the registry-shape check. Nothing in the lane was edited; `corpus/SOURCES.md` was not touched (rows are in `rows.md` for the integrator).

## Deliverables

- Rows: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeSourcesB/rows.md` (8 lines, 11 cells each, no `|` or backslash inside cells, no line wrap).
- Gate: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeSourcesB/gate.md` (URL, access date 2026-10-28, located quote with pin line, sha256, bytes, locators, K-row coverage per row).
- Generator (the locators, sha256, sizes and quote checks are computed, not typed): `.../R56ScribeSourcesB/mkrows.py`.
- Receipts (copied before scratch removal): `.../R56ScribeSourcesB/receipts/validate-exact-cmd.txt`, `.../receipts/validate-tree.tsv`, `.../receipts/harm-watch-validate-root-mado.txt`; duplicates of the first two at `.../R56ScribeSourcesB/validate-exact-cmd.txt` and `validate-tree.tsv`.
- Scratch `/fast/scratch/hyaku/mado-r56/R56ScribeSourcesB/` removed.

## What I did

1. Read `registration.md` (§C1, §C3, seat boundaries) and `claims-frozen.md` (C1, harm watch, causal separability). Loaded `frozen-tables.json` (sha256 `d50d2b7b…edf9af` checked against the frozen value) and listed the 30 K rows and their `sid`.
2. Verified the eight pins against the tables and the disk. Output (trimmed): every pin `True` for sha256; sizes `Hyprland-ConfigWatcher.cpp 4046`, `ConfigValues 59222`, `PropRefresher 5139`, `EventLoopManager 9073`, `legacy ConfigManager 90963`, `MiscFunctions 29785`, `HyprCtl 97582`, `man7-inotify.7.html 44066`. Every K quote is a substring of its stated line (30/30).
3. Read the pinned lines (the read tool, ranges around each K line) to write the teaches cells and to choose the gate quotes. I did not use any other seat's output.
4. Ran `mkrows.py` (python3 -I). It derives locators from the K rows (adjacent lines merge into `N-M`), asserts each K row line is inside a locator, asserts each pin sha256, asserts each quote at its line, asserts the 11-cell shape and no `|`/`\`, and asserts each gate quote is at most 25 words. All assertions passed; the script printed the eight rows and the gate.

Row locators (K rows covered per pin; the anchor cell carries the same list):

| row | pin (basename used in anchor) | locators | K rows |
|---|---|---|---|
| S383 | Hyprland-ConfigWatcher.cpp (`ConfigWatcher.cpp:`) | 33-34,46,54-56,60,67,69,105 | K03–K12 (10) |
| S384 | Hyprland-ConfigValues.cpp (`ConfigValues.cpp:`) | 492 | K01–K02 |
| S385 | Hyprland-PropRefresher.cpp (`PropRefresher.cpp:`) | 148-149 | K15–K16 |
| S386 | Hyprland-EventLoopManager.cpp (`EventLoopManager.cpp:`) | 71,128 | K13–K14 |
| S387 | Hyprland-legacy-ConfigManager.cpp (`ConfigManager.cpp:`) | 776,1070,1079-1080,1816,1835-1836,1844 | K17–K24 (8) |
| S388 | Hyprland-MiscFunctions.cpp (`MiscFunctions.cpp:`) | 65,68 | K25–K26 |
| S389 | Hyprland-HyprCtl.cpp (`HyprCtl.cpp:`) | 1223,1276 | K27–K28 |
| S390 | man7-inotify.7.html (`inotify.7.html:`) | 186,262 | K29–K30 |

Total 30/30 K rows covered. Anchors carry `@ efb50993780079460b0cbed1363e2166a2de1d9f; <bytes> B sha256 <hex>; pin .ufo/waves/round-56/fetch/<pin>` (S390: `@ man-pages 6.19 (footer 2026-02-14)`, see ambiguity 4).

Teaches are one sentence each (word counts 39, 18, 10, 18, 32, 23, 21, 18); none quotes a fragment.

5. Registry-shape check, exactly as requested. Copy of `corpus/SOURCES.md` with the eight rows inserted after the S382 row (line 332, last row of `## Registry`), then:

```
$ sources-census.sh validate --file <scratch>/SOURCES-scratch.md
exit=1
    365 E11
      1 W01   (S277, pre-existing)
     32 W04
E11 naming S383–S390: 8     E11 naming pre-existing rows: 357
```

The exit is 1, not the required 0. Cause: `--file` resolves each `used-by` path against the parent of the copy's directory (`$dir/$path`, `sources-census.sh` around line 560), so from a `/fast/scratch` copy every `used-by` path is "missing", including 357 pre-existing rows. Plus, the entry file does not exist in the lane yet, so the eight new rows also fail E11 (ambiguity 1 and 2).

To get a faithful run I built a scratch tree: `git -C <lane> archive 3423ae285676c2a10273000f4519163472b443db | tar -x -C <scratch>/tree` (read-only archive at the freeze commit), the scratch copy as `tree/corpus/SOURCES.md`, and a placeholder file `tree/corpus/knowledge/hyprland-config-autoreload-r56.md` containing one line "placeholder entry for registry-shape check only; not a deliverable". Result:

```
$ sources-census.sh validate --file <scratch>/tree/corpus/SOURCES.md --today 2026-10-28
EXIT=0
      1 ok
      1 W01   file W01 S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
     32 W04
E-lines: 0
```

W04 lines naming the new rows (warnings, do not change status):
- `W04 S384 duplicate url …/src/config/values/ConfigValues.cpp across scopes` (matches S318)
- `W04 S387 duplicate url …/src/config/legacy/ConfigManager.cpp across scopes` (matches S303, S317, S353, S368)
- `W04 S388 duplicate url …/src/helpers/MiscFunctions.cpp across scopes` (matches S321)
- `W04 S389 duplicate url …/src/debug/HyprCtl.cpp across scopes` (matches S307, S320, S366)

No W04 for S383, S385, S386, S390. No E04 (duplicate URL+scope) fired, because the scopes differ.

6. Frozen harm watch (`claims-frozen.md` § Harm watch: `validate --root /home/vgpnk/Projects/shokunin mado` must stay exit 0), run read-only on the lane's current registry (new rows not yet present):

```
$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
EXIT=0   1 ok, 1 W01 (S277), 28 W04
```

Host: no `hyprctl`, no config reads, no installs. Tools installed: none.

## Defects and ambiguities

1. **`validate --file` cannot exit 0 from a copy outside the lane.** Input: the exact command in the seat spec, run on a copy under `/fast/scratch/...`, exits 1 with 365 E11 (357 pre-existing rows). The script resolves `used-by` relative to the copy's parent (`sources-census.sh` ~line 560). The frozen harm watch uses `--root` instead; the spec's `--file` form is not the frozen command. I reported the `--file` result verbatim and used the scratch tree above for the exit-0 check.
2. **Entry not on disk yet.** `corpus/knowledge/hyprland-config-autoreload-r56.md` does not exist in the lane. Every new row's `used-by` therefore fails E11 until the entry lands. This is not my deliverable; the entry seat or the integrator must create it before the rows can validate in the lane. Note the frozen C1 `new_rows` leg checks `source_cell`, which does not test file existence, so this is a registry-tool concern, not a C1 counter failure.
3. **Locator grammar (registration §C1 `scope`).** The text says a comma-separated list of `N` or `N-M` locators must contain "a range that includes the row's line". I wrote single lines as bare `N` (e.g. `492`, `71,128`). I read `N` as `N-N`. If the counter requires the `N-M` form, the anchors need `492-492` and the like. Not verified (the counter is not in this lane yet; no counter run by me).
4. **S390 anchor revision marker.** The seat spec says to add `@ efb50993780079460b0cbed1363e2166a2de1d9f` for each pin, but S390's pin is man7, not a Hyprland commit. I used `@ man-pages 6.19 (footer 2026-02-14)`. The registration's `rev_rule` for man7 is the URL token (`man7.org/linux/man-pages/man7/inotify.7.html`), and that token is in the URL, so the counter's `source_cell` should still hold. The footer confirms the version: `Linux man-pages 6.19 2026-02-14 inotify(7)` (pin line 811).
5. **Byte sizes.** `frozen-tables.json` carries sha256 but no sizes. I took sizes from the pin files; they match `wc -c` (listed above).
6. **Pin path naming.** The spec's pin map uses the pin file names. In the anchor the basename is the last component of `pin_suffix` (`ConfigWatcher.cpp`, not `Hyprland-ConfigWatcher.cpp`), as registration §C1 requires; the pin path in the anchor is the full `.ufo/waves/round-56/fetch/<pin>`.
7. **Lane status read.** One `git -C <lane> status --porcelain` (read-only in intent; may refresh the index stat cache) to see whether the lane had changed. It shows untracked sibling-seat directories (`w1.ready`, `w1.ready.dispatched`, `w1/R56ExecC1Harness/`, `w1/R56ExecC3CounterA/`, `w1/R56ExecC3CounterB.md`) and nothing from this seat except my own directory, which I created. I did not look inside sibling directories.

## Not verified / not run

- The C1 counter (`quality/counters/c1-r56-autoreload-entry.py`) and the controls harness are not in this lane yet at my read; I did not run them. My check covers only the registry shape (the census script) and my own asserts. Entailment of teaches to pins is my reading, not an audit.
- The seat's row shape check is on the census script's reading. The `source_cell` URL-suffix rule was checked by my own assert (`URL endswith /<pin_suffix>`) and by reading, not by the counter.
- Hold-out fixtures (H01–H08) were not touched or looked for. No hold-out path was encountered.
- No pacman, no installs, no hyprctl, no writes outside the seat directory and my scratch (scratch removed).
