# R56ScribeIndex — round 56, wave w1 — integration drafts report

Seat: R56ScribeIndex (scribe, leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `3423ae285676c2a10273000f4519163472b443db` (freeze), lane HEAD `2aa347b1` (wave spec). Drafts only; nothing in the lane's tracked files was edited, and no git/jj mutation was run.

## 1. What I did

1. Read the frozen contract: `claims-frozen.md`, `registration.md` (C1 §C1, C2 §C2, C3 §C3, seat boundaries). The frozen tables were not re-verified (not my seat).
2. Read `corpus/README.md` (full), `PROVINCE.md` (full), the relevant `SKILL.md` sections (lines 112, 197-199, 204-227, 477, and the round-45/46 join sections), `quality/check-index-rows.py`, `quality/check-index.py`.
3. Confirmed tool state at base: `tools/mado-watchplan.py` does **not** exist (`ls`; `git ls-tree 3423ae28` → no `watchplan` path). So the SKILL sample is `to be filled at integration`.
4. Host reads allowed by the brief (read-only, no compositor/config write):
   - `hyprctl version -j` → `"version": "0.56.2"`, `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"`, `"buildHyprlang": "0.6.8"` (matches the pinned commit).
   - `hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`.
   - `grep -rni disable_autoreload ~/.config/hypr ~/.local/share/omarchy/default/hypr ~/.local/state/omarchy/toggles/hypr ~/.config/omarchy` → no hits (the toggles dir holds `flags.conf`, `window-no-gaps.conf`).
   Copies: `receipts/hyprctl-version.json`, `receipts/getoption-disable_autoreload.json`.
5. Dry-run of the two README gates on a scratch tree (`git archive 3423ae28 corpus quality tools SKILL.md PROVINCE.md .ufo/waves/round-56/fetch`, plus a placeholder note; the placeholder is for the dry run only). Output (trimmed):
   - A-base (unmodified README): `MADO_INDEX_ROWS: rows=70 errors=28 warns=3`; `ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52.md at line 80` (also lines 81, 82).
   - B (base with blank line 79 removed): the three `row-outside-map` errors disappear; the rest is dry-run artifact (partial `.ufo` archive).
   - C (B + the exact row from `02-index-row.txt` after the r55 row): `rows=71 errors=31 warns=4`; diff against B, attributable to the new row only: `ERROR cited-path-missing: tools/mado-watchplan.py`, `ERROR cited-s-undefined: S383`, `ERROR cited-s-undefined: S390`, `WARN holds-no-overlap` (against the placeholder).
   - `quality/check-index.py` parity on C: `MADO_INDEX: indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, rc 0.
   Receipts: `receipts/index-gates-dryrun.txt`, `receipts/rows-A-base.txt`, `receipts/rows-B-base-noblank.txt`, `receipts/rows-C-with-row.txt`.
6. Wrote the drafts (below) and checked the SKILL row has 3 cells and no interior pipe.

## 2. Deliverables (drafts; the L1 applies)

Directory: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeIndex/`

- `01-corpus-README.md` — (1a) coverage-map row placement; (1b) Frontier bullet "Round 56 moves the Hyprland config auto-reload chain onto sourced ground…" to insert as the first bullet under `## Frontier` (README:117); (1c) gating conditions and the table-split fix; (1d) existing rows the text must not contradict.
- `02-index-row.txt` — the exact one-line index row (3 cells; Note / Holds / Sources), to insert after the r55 row (README:82):
  `| `knowledge/hyprland-config-autoreload-r56.md` (MADO-R56-1, round 56; config plane, Hyprland config auto-reload) | The Hyprland 0.56.2 (efb50993) chain … | `source:` S383-S390 (opened 2026-10-28) in [SOURCES](SOURCES.md); pins under `.ufo/waves/round-56/fetch/`; host pins …; watch-list predictor `tools/mado-watchplan.py` (round-56 C2, read-only). |`
  Full text is in the file.
- `03-PROVINCE-refinement.md` — (3a) "Round-56 refinement" paragraph, append-only at the end of PROVINCE.md, in the round-36/round-55 form. It names `tools/mado-watchplan.py` (reads the `--config` file, at most one `--getoption` file, the files its `source =` lines reach, and only `stat`/`lstat`/`realpath`/`glob`/`isdir`/`lexists`/`islink` on those paths; writes nothing, no process, no socket) and `quality/counters/c1-r56-autoreload-entry.py`, `quality/counters/c3-r56-used-by.py`, `quality/check-r56-controls.py`. (3b) an optional tool-table row for `tools/mado-watchplan.py` after PROVINCE:32. (3c) notes on the defects below.
- `04-SKILL-probe-row.md` — (4b) one row for the read-only probe `python3 -I tools/mado-watchplan.py --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <file>` (capture first with `hyprctl getoption misc:disable_autoreload -j > <file>`), appended to the "Read-only probes" table after SKILL:225; sample column `to be filled at integration`. (4d) the SKILL rows it must not contradict.
- `receipts/` — host captures and the gate dry-run outputs listed above.
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ScribeIndex.md`.

## 3. Which existing rows the text must not contradict

README: line 8 ("A new index row does not close a behavioral gap"); line 98 (route row *Hyprland config, binds, rules and display*, limit "Parsed declarations do not prove …"); line 12 (`hyprland-config-plane`); line 35 (`hyprland-config-era-r12`: host `configProvider: hyprlang`, upstream Lua claims `[INF-docs]`); lines 131–134 ("Index completeness does not retire these unresolved surfaces"); lines 82 and 117 (r55 house form for "no event observed" limits).

SKILL: line 112 ("auto-reloads on save (omarchy skill:145)" — a documentary claim; not to be promoted to observed); lines 197–199 (safe-probe discipline cites auto-reload as the reason for read-only strictness); lines 145–148 and 477 (omarchy's `hyprctl reload` + `configerrors` pair; mado runs only the `configerrors` read leg); line 204 (table header "all executed 2026-10-14 unless cited" — the new row is cited to the round-56 contract, not executed); PROVINCE lines 10–16 (config trees read-only; no compositor mutation).

## 4. Defects and ambiguities found (with the input that shows each)

D1 — **README coverage-map table is split by a blank line (pre-existing).** `corpus/README.md:79` is empty, so `quality/check-index-rows.py` reads the table as ending at line 78; rows r52 (line 80), r52-errata (81) and r55 (82) are `row-outside-map`. Shown by A-base (`rows-A-base.txt`): errors=28 at base. Fix: delete line 79 (drafted in 01 §1c; L1 decides). The new row inherits the problem if the blank line stays.

D2 — **PROVINCE tool table is not complete, though the round-23 correction says it is.** The round-23 wave-2 correction (`PROVINCE.md:34`) states the inventory "covers every tracked file under `tools/`". The table (`PROVINCE.md:24-32`) has 9 rows; `tools/` holds 18 files. No rows for `mado-devices.py`, `mado-eventq.py`, `mado-hostguard.py`, `mado-kbdopts.py`, `mado-keysym.py`, `mado-monitors.py`, `mado-options.py`, `mado-terminal.py`, `mado-wsrules.py`. Pre-existing; not created by round 56; not repaired by my drafts beyond the new watchplan row.

D3 — **SKILL has no entry for the round-55 tool.** `grep -n kbdopts SKILL.md` at `3423ae28` returns nothing, while `tools/mado-kbdopts.py` is tracked and listed in `quality/tool-ledger.md:128`. Pre-existing gap; the new row does not cover it.

D4 — **Index row depends on two artifacts not yet on the lane.** At base SOURCES.md's highest id is `S382` (no S383–S390 rows; `grep -c '^| S38[3-9]\|^| S390' corpus/SOURCES.md` → 0), and `tools/mado-watchplan.py` is absent. Under `check-index-rows.py` the row therefore fails `cited-s-undefined` (S383, S390) and `cited-path-missing` (`tools/mado-watchplan.py`) until SourcesB and C2 land (receipt C). Not a frozen C1 leg (the frozen `index` leg checks only the line's presence), but a gate failure at integration.

D5 — **"read git objects only" is true for the two counters, not for the harness.** The brief asks for that phrase for all three. `registration.md` says the counters "read ONLY git objects … the counter itself writes nothing"; `check-r56-controls.py` (per registration) exports the tool and fixtures, builds scratch repos, and runs the tool and counters as child processes, writing under `--work`. The 3a paragraph states the difference rather than repeating the brief's wording.

D6 — **Brief vs registration on the watchplan reads.** The brief lists config file(s), sourced files, and stat/lstat/realpath/glob. `registration.md` §C2 also reads the `--getoption` file and uses `isdir`, `lexists` and `islink`. 3a uses the registration's set.

D7 — **Quality ledger and tool-table need rows for four new files.** `PROVINCE.md:116-118` (round-51) says `quality/tool-ledger.md` names each tracked instrument under `tools/`, `quality/*.py` and `quality/counters/*.py`, and `check-tool-ledger.py` checks row coverage. The four round-56 files (`tools/mado-watchplan.py`, `quality/counters/c1-r56-autoreload-entry.py`, `quality/counters/c3-r56-used-by.py`, `quality/check-r56-controls.py`) have no ledger row yet. Not executed (see §5).

D8 — **Holds-cell overlap is unverified.** `holds-no-overlap` (WARN) compares the Holds cell with the landed entry's bytes; the entry is not on the base, and the dry run used a placeholder. Re-run against the landed entry.

D9 — **Frontier bullet and row assert coverage only conditionally.** The text describes the entry's content as frozen (K01–K30, H01–H03, S383–S390, pins). It must not be applied unless `MADO_AUTORELOAD_ENTRY … TARGET_MET` and, for the tool sentence, `MADO_R56_C2 … TARGET_MET` (both in 01 §1c). Per `claims-frozen.md`, the C2 capability row enters SCORECARD only on TARGET_MET.

D10 — **SKILL sample cannot be filled honestly yet.** The probe needs `tools/mado-watchplan.py` (absent). The only live input captured is the getoption reply above (`int 0, set false`). No sample line is invented.

## 5. Not verified / not run

- The landed entry, SOURCES rows S383–S390 and the C2 tool do not exist on the lane at this seat; the index-row and frontier text are checked against the frozen contract and the gate code, not against landed bytes.
- `quality/check-tool-ledger.py`, `quality/check-r56-controls.py`, the C1/C3 counters and the C2 harness were not run (they are other seats' or the L1's; the brief forbids running the harness mid-flight and no tool exists to run).
- No sentence-to-pin check of any proposition (declared limit in the contract).
- `hyprctl` was called only with the read verbs `version -j` and `getoption misc:disable_autoreload -j`; no `keyword`, `dispatch`, `reload` or `configerrors` was run.
- Hold-out: I did not look for or use any sealed hold-out fixture. None was encountered.

## 6. Tooling and installs

None. No tool was installed or upgraded; no pacman transaction; nothing written under `~/.local/bin` or `~/.config`.

## 7. Cleanup

The scratch dir `/fast/scratch/hyaku/mado-r56/R56ScribeIndex/` (git archive, scratch variants, dry-run outputs) is removed at the end of this seat; the receipts it produced were copied to `receipts/` first.
