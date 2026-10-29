# R56ScribeEntryC — C1 knowledge entry draft (wave w1)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD at read time `2aa347b1175cded6628465acf335f9232183d40c` (freeze `3423ae28`). Scope: draft the complete C1 entry per `registration.md` §C1 and report. Leaf seat, no subagents, no lane edits, no git mutation, no host mutation.

## 1. Deliverables

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeEntryC/`:

- `entry.md` — the entry (199 lines). Title line 1; provenance trio at lines 3-5 (`source:` S383-S390, `verified-at: 2026-10-28`, `recheck: on-release`); Scope; Chain (12 steps); Host join; Rows (33 counted K/H rows, generated); Extra rows E01-E18 (not counted); Limits; How to verify (fenced, read-only).
- `template.md` — the prose with `@@ROWS:…@@` placeholders. I wrote all prose here.
- `props.json` — the proposition cell for each K/H row and the text of each E row, plus the E-row pin/line/source. Only the proposition cells and the E-row choice of line are authored here.
- `gen-entry.py` — builds `entry.md`. Reads `frozen-tables.json` (sha256 checked against `d50d2b7b…edf9af`), the pins under `fetch/`, `props.json`, `template.md`. K/H rows take pin, line, quote and `sid` from the frozen table; E rows take their quote from the pinned line itself. No quote is typed by hand.
- `selfcheck.py` — a local re-implementation of the §C1 legs (`prov`, `row:`, `quote:`, `host:`, `tok:`, `num:`, `len`, unique propositions, `cites_new_rows`, and optionally `source_cell:`/`scope:`/`new_rows` against a registry file). It is not the counter. It does not run the harness.
- `receipts/`: `rows.json` (every row, as generated), `selfcheck-local.txt`, `controls-local.txt`, `run-controls.py` (my mutation driver), `anchors-sim-registry.md` (see §5), `howto-run.txt` (the How-to block run as written), `freeze-verify-run.txt`, `lane-head.txt`.

## 2. What I did (in order)

1. Read `claims-frozen.md`, `registration.md` (§C1, §C2, §C3, seat boundaries) and `frozen-tables.json` (`c1.k`, `c1.h`, `pin_suffix`, `rev_rule`, `new_row_ids`). Read every pin window the chain uses: ConfigWatcher.cpp (whole, 1-111), PropRefresher.cpp (whole), EventLoopManager.cpp (1-282, whole), ConfigValues.cpp 477-508, legacy ConfigManager.cpp 726-752, 764-788, 970-1098, 1049-1095 (callback), 1799-1858 (`handleSource`), 1077-1087 (`init`), 2133-2139 (`getConfigPaths`), MiscFunctions.cpp 54-105 (`absolutePath`), HyprCtl.cpp 1159-1293 (`dispatchKeyword`, `reloadRequest`), man7 html 178-193 and 254-269. Grep over the eight pins for the chain identifiers (`reload`, `postConfigReload`, `REFRESH_*`, `doLater`, `getConfigPaths`, `reloadRequest`, `m_configPaths`).
2. Verified the frozen state: `python3 -I .ufo/waves/round-56/freeze-verify.py` (run from the lane root; read-only) → `FREEZE_VERIFY: bad=0 frozen-tables.sha256=d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af OK`; `fixture commitment ok files=119`.
3. Wrote `props.json` (33 K/H propositions, 18 E rows), `template.md`, then `gen-entry.py` and `selfcheck.py`.
4. Generated the entry; ran the local self-check; ran four mutations of the entry and three scratch registries (controls, §5).
5. Ran the How-to block from `entry.md` as written (read-only). Ran the host reads (§4).

## 3. Commands and decisive output

```
$ python3 -I gen-entry.py --lane <lane> --seat <seat> --out <seat>/entry.md
gen-entry: wrote …/entry.md counted=33 extra=18 lines=200        (rc 0)
$ python3 -I selfcheck.py --lane <lane> --entry <seat>/entry.md
SELFCHECK_C1 (local, not the counter): rows=30/30 hosts=3/3 content=33/33 registry=not_evaluated missed=none
cites=S383,S384,S385,S386,S387,S388,S389,S390
props_lengths={'min_K': 98, 'min_H': 107}
```

Controls on the entry (no registry), each a one-mutation copy in scratch, `selfcheck.py` run on it:

```
junk-placeholders   rc=1 missed=tok:H01,…,tok:K30 (content 1/33)
false-number        rc=1 missed=num:K04            (appended " The value is capped at 200 by this call." to the K04 proposition)
edited-quote        rc=1 missed=quote:K05,row:K05  (one character changed inside the K05 quote)
dropped-row         rc=1 missed=len:K17,quote:K17,row:K17,row_grammar,tok:K17
provenance-order    rc=1 missed=prov               (verified-at and recheck lines swapped)
```

Controls with scratch registries (my simulation: one row per S383-S390, anchors = exactly the lines the entry cites for that pin, all other fields as §C1 requires; `anchors-sim-registry.md`):

```
registry-good       rc=0 missed=none
registry-no105      rc=1 missed=scope:K12          (line 105 removed from the S383 anchor)
registry-no390      rc=1 missed=new_rows,scope:K29,scope:K30,source_cell:K29,source_cell:K30   (S390 row removed)
```

The registry-good result is my own simulation, not evidence about the sibling rows (§5).

How-to block (extracted from `entry.md` and run with `bash`, output in `receipts/howto-run.txt`, rc 0): freeze-verify → `OK`; pins sha256 listed; `sed -n '128p'` and `sed -n '3p'` return the pinned lines; the grep call sites return; the counter step prints `counter not present at 2aa347b1…` (the counter is absent at HEAD); the host block prints the captured values (below).

## 4. Host reads (read-only)

```
$ hyprctl getoption misc:disable_autoreload -j
{"option": "misc:disable_autoreload", "int": 0, "set": false }
$ hyprctl version -j | grep '"commit"'
    "commit": "efb50993780079460b0cbed1363e2166a2de1d9f",
$ diff <(grep '^source' ~/.config/hypr/hyprland.conf) fetch/host-sources.txt && echo "SOURCES SAME"
SOURCES SAME
$ grep -rln 'disable_autoreload' ~/.config/hypr ~/.config/omarchy ~/.local/share/omarchy ~/.local/state/omarchy
(no output) → "no host config names disable_autoreload"
$ python3 (lstat over the 40 regular-file lines of host-watched-lstat.txt, host paths expanded)
40 of 40 regular
```

Also read: `stat -c '%F|%n|%Y' ~/.config/hypr/hyprland.conf` → `regular file|…|1792267376`. No `hyprctl keyword`, `dispatch` or `reload`; no write under `~/.config` or `~/.local`.

`hyprctl version -j` agrees with H03 (commit) and `getoption` agrees with H01 (int 0). The `^source` lines of the live main config equal `host-sources.txt` (18 lines), agreeing with H02. Under the §C2 join rule (`config` = 0 with no `misc:disable_autoreload` line in the files, live int 0) the join reads AGREE; I did not run the C2 tool (not in the lane).

## 5. Defects, ambiguities and contract notes

Contract (registration vs claims-frozen vs frozen tables):

- No disagreement found between `claims-frozen.md` §C1 and `registration.md` §C1: the entry path, `prov` order, row grammar, legs, `content=33/33`, `new_rows=8/8`, the controls and the kill rules match. `frozen-tables.json` K/H rows match the grammar of §C1 (every quote is a single-line pipe-free substring; `freeze-verify` confirms).
- Ambiguity A1 (E rows vs row detection): §C1 defines a row as a line whose first cell is an id `K01..K30` or `H01..H03`. My E01-E18 rows share the table grammar (`| E01 | … | S### | pin:line | `quote` |`). The contract says the counter ignores them; if the counter's row detector is looser than the K/H id set, E rows would show as malformed. Worth a check at integration (if they do, delete the E table; nothing in the chain cites an E row only for a counted fact).
- Ambiguity A2 (`new_rows` vs `source_cell`): `source_cell` includes "the S-id equals the frozen sid of that K row"; for `new_rows` the rows S383..S390 are each cited by K or E rows, so the clause is satisfiable, but the wording does not say which K row is meant for E-only sids. Not triggered by the current entry (every new sid has K rows: S383 K03..K12, S384 K01-K02, S385 K15-K16, S386 K13-K14, S387 K17-K24, S388 K25-K26, S389 K27-K28, S390 K29-K30).
- Ambiguity A3 (`prov` and the title line): §C1 says "first 30 lines … in that order". I placed a title at line 1 (the corpus convention) and the trio at lines 3-5. If "first" means literally first line, the trio must move to lines 1-3; the leg as written is satisfied.
- Ambiguity A4 (`tok`/`num` on H rows): §C1 applies `tok`/`num` to K and H rows (`e` = 33). All H propositions satisfy both.

Source-level facts that look wrong or surprising (reported as observed, not fixed; the entry states them):

- D1 `ConfigWatcher.cpp:33` reads `misc:disable_autoreload` through `CConfigValue<Config::INTEGER>`, while `ConfigValues.cpp:492` declares it `MS<Bool>`. The entry does not rely on the accessor beyond the 0/non-zero test.
- D2 `ConfigWatcher.cpp:59-62`: the `wd` returned by `inotify_add_watch` is stored without a check, so a missing path leaves a record with `wd` -1 (the entry labels the consequence as an inference).
- D3 `ConfigWatcher.cpp:100-107` (`onInotifyEvent`): no mask or name filter; every event whose `wd` is registered calls the callback, so one buffer can call `reload()` several times (E09, E10, K12).
- D4 `MiscFunctions.cpp:73` and `:75`: the replace length is `2 + currentPath.empty()` / `1 + currentPath.empty()`. The bool term is a quirk; it only matters when the current path is empty, which the main path never is. Recorded as E18.
- D5 `handleSource` (legacy 1802-1855): recursion (E17) with no depth test in the read lines; the §C2 watch-list rule adds a depth cap of 16 as a declared divergence. The entry says the absence is for those lines only.
- D6 `ConfigWatcher.cpp:70`: the canonical watch record carries the link path as `file`, so a write through the target is reported under the link path (stated in the entry as a source fact plus an inference about the kernel).
- D7 `REFRESH_ALL` and `REFRESH_CONFIG_WATCHER` values are not pinned (`PropRefresher.hpp` is not in `fetch/`). Whether `scheduleRefresh(REFRESH_ALL)` reaches the watcher branch (K15/K16) is therefore UNKNOWN in the entry (chain step 8); this is the one link in the reload path that is not closed by the pins.

Scope/integration legs I could not evaluate:

- Registry: `corpus/SOURCES.md` at HEAD has 319 rows and none of S383-S390 (`grep -n 'S38[3-9]\|S390' corpus/SOURCES.md` → nothing; the working copy has no such rows either). So `source_cell:<id>`, `scope:<id>`, `new_rows` and the `prov` dangling check are not evaluated here. Anchors the sibling rows must cover (`receipts/anchors-sim-registry.md` is my simulation, which passes the legs): ConfigWatcher.cpp:22,33,34,46,54,55,56,59,60,67,69,80,100,105; ConfigValues.cpp:492; PropRefresher.cpp:29,33,34,148,149; EventLoopManager.cpp:71,127,128,215; legacy ConfigManager.cpp:726,776,970,1070,1079,1080,1081,1816,1835,1836,1839,1844,2133; MiscFunctions.cpp:65,68,73; HyprCtl.cpp:1190,1223,1262,1276,2028; man7-inotify.7.html:186,262. The K lines are what `scope:` tests; the E lines back the chain's citations.
- Index: `corpus/README.md` row for the entry is not written by me (R56ScribeIndex). The entry is in the w1 directory only; nothing is placed under `corpus/knowledge/`.
- Counter: `quality/counters/c1-r56-autoreload-entry.py` and `quality/check-r56-controls.py` are absent at HEAD. My `selfcheck.py` implements the legs but is not the counter; its verdict is not the predicate's.
- Hold-out: I did not look for and did not use any `fixtures/c2-holdout` or sealed H01-H08 path. I encountered none.

## 6. Scope of verification

Ran: freeze-verify (pass), gen-entry (pass), selfcheck on the entry (pass, all counted legs I can evaluate without a registry), the five entry mutations and three registry scenarios (outcomes as in §3), the How-to block (rc 0), and the host reads in §4.

Not run: the counter and its harness (absent at HEAD); `hyprctl keyword`, `hyprctl dispatch`, `hyprctl reload` and any filesystem event (not part of the seat; the entry does not claim them); the C2 tool; any builds or tests.

Not verified: that a proposition follows from its quote beyond lexical grounding (§C1 declares this as the wave-2 sentence audit, not counted); the values of `REFRESH_ALL`/`REFRESH_CONFIG_WATCHER`; live inotify behaviour and reload behaviour on the host; editor save methods; the producer of `host-watched-lstat.txt` (no producer recorded; the live re-lstat agrees 40/40 and the entry uses it for no counted row).

## 7. Tooling and host state

- No tools installed or upgraded. (pacman is paused host-wide; nothing was installed through any channel.)
- No host state changed. Scratch: `/fast/scratch/hyaku/mado-r56/R56ScribeEntryC/` (removed at the end of this seat, see below); two empty `c1-verify-*` directories created by my How-to test runs were removed.
- Scratch removal: the scratch tree (controls, mutated entries, simulated registries) is removed before yield; the copies the report needs are in `receipts/`.
