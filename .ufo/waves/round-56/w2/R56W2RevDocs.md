# R56W2RevDocs — accuracy review of round-56 text in corpus/README.md, PROVINCE.md, SKILL.md, quality/tool-ledger.md

Reviewed tree: lane commit `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` vs base `13f0acbe3a15da2d9c08357a576d91dcadc85273`.
Diff scope: `git -C <lane> diff 13f0acbe… 28fc86ac… -- corpus/README.md PROVINCE.md SKILL.md quality/tool-ledger.md`
(13 added sentences: PROVINCE tool row + Round-56 refinement paragraph; SKILL probe row; README index row + Frontier
bullet; 7 tool-ledger rows). Lane working tree was never modified; every check read committed state via
`git show`/`--rev`/`git archive`. Scratch: `/fast/scratch/hyaku/mado-r56/R56W2RevDocs/` (removed before yield;
receipts copied to `.ufo/waves/round-56/w2/R56W2RevDocs/receipts/`).

Tooling: no tool was installed or upgraded (none needed); Python 3.14 stdlib only, `hyprctl` read verbs
`getoption` per the seat's read list.

Receipts (all under `.ufo/waves/round-56/w2/R56W2RevDocs/receipts/`):
`01-docs-diff.txt`, `02-added-lines.txt`, `03-index-rows-target.txt`, `04-index-rows-base.txt`,
`05-tool-ledger.txt`, `06-c1-counter.txt`, `07-c3-counter.txt`, `08-registry-vs-readme.txt`,
`09-live-rerun.txt`, `10-receipt-diff.txt`, `11-blankline-experiment.txt`, `12-selftest-writes.txt`,
`13-pyc-write.txt`, `14-contrasts.txt`.

---

## Verified checks (passing / null results)

- **The SKILL sample line is the real tool output.** Re-ran the committed `tools/mado-watchplan.py`
  bytes at `28fc86ac` against this host's live `~/.config/hypr/hyprland.conf` with a fresh
  `hyprctl getoption misc:disable_autoreload -j` capture: output byte-identical to the cited
  `receipts/live-watchplan.txt` (43 lines, `diff` clean — `10-receipt-diff.txt`: "FULL RECEIPT
  IDENTICAL"), and the receipt is unchanged at the rev. The two lines quoted in SKILL.md
  (`MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE`,
  `MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE`) match the receipt verbatim.
- **README coverage-map row obeys `quality/check-index-rows.py`.** At `28fc86ac`:
  `MADO_INDEX_ROWS … rows=71 errors=0` (exit 0); the 3 warns are pre-existing round-12/24 glob
  warns, none about the r56 row (`03-index-rows-target.txt`).
- **No contradiction with SKILL.md:112 / 197-199.** Those lines assert "auto-reloads on save
  (omarchy skill:145)"; the added sentences only report non-observation ("no reload was observed",
  "no filesystem event is generated and no reload is observed", the effect "stay[s] unmeasured").
  Observation-absence is not a denial; the Frontier bullet in fact corroborates the mechanism at
  source level. Residual: the entry's own Scope section marks "whether Hyprland reloads on this
  host after a save" UNKNOWN — an entry-vs-SKILL.md:112 tension the added rows neither create nor
  reconcile (see Residual).
- **The frozen predicates reproduce at the rev** (run for context): C1 counter line + C1 harness
  `controls=12/12`; C2 `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 TARGET_MET`;
  C3 counter `missing=0 … exempt=24 TARGET_MET` + C3 harness `controls=9/9` (`06/07-c*-counter.txt`,
  and the harness runs logged in the transcript). Ledger gate: `population=97 ledger_rows=97
  uncovered=0 bad_pointer=0` (`05-tool-ledger.txt`).
- **PROVINCE "three record instruments"** matches the round-55 convention (the `r56_ctl_c*.py`
  harness modules are counted as parts of the harness, exactly as `r55_ctl_c*.py` were in round 55);
  the ledger nonetheless lists all 7 new instruments and the gate shows `uncovered=0`.
- **"constructs it does not model are reported `unsupported`"** matches the round-55 house wording
  (values are counted `unsupported=<U>`, not named per-construct) — identical to the r55 Frontier
  bullet for kbdopts.
- **The value-grammar claim checks out at the true/on branch**: round-46 pin `hyprlang-config.cpp`
  `configStringToInt` has `starts_with("true")||("on")||("yes") → 1` / `false/off/no → 0`
  (`14-contrasts.txt`), matching the tool's `config_int`; the wider forms (0x, rgb/rgba) are the
  declared grammar-subset divergence, though PROVINCE's "the way hyprlang does" omits that
  qualifier (see F10).

---

## Findings

### F1 [weakens the claim] corpus/README.md index row (line 82), Sources cell: "`source:` S383-S390" — understates the entry's registry binding and its host pins; contradicts the same file's Frontier bullet

- The entry's `source:` line (line 1 of the note, same rev) names **S383–S391** (nine ids, ending
  "S391 (PropRefresher.hpp)") and **three** host captures ("host-getoption.json, host-version.json,
  host-sources.txt").
- The index row names **S383-S390** (eight) and **two** host pins (`host-version.json`,
  `host-getoption.json`).
- The same commit's Frontier bullet (line 117) says "**rows S383-S391** plus the host pins under
  `.ufo/waves/round-56/fetch/`" — so the two added README sentences contradict each other.
- S391 (Hyprland `PropRefresher.hpp`, tier A, opened 2026-10-28, used-by cell = this entry) is the
  only source of E08/E09 — the `REFRESH_CONFIG_WATCHER = (1 << 8)` / `REFRESH_ALL = max(uint16_t)`
  arithmetic that the index row's own "… leads through `CConfigManager::reload` to `REFRESH_ALL`"
  leans on. H02's pin is `host-sources.txt:10` — not named in the cell.
- Neither omission is gate-visible: `cited-s-undefined` only checks that named S-ids resolve
  (S383, S390 do) and `cited-path-missing` only that named paths exist — the gate shows errors=0.
- Root: `frozen-tables-v2.json` `c1.new_row_ids` = S383..S390 (8 ids, `new_rows_min` 8) — S391 is a
  **9th new registry row** opened this round that no C1 leg scores (the C3 counter does bind
  S391↔entry: `rows=328 missing=0`). The tool-ledger row for the C1 counter repeats
  "registry rows S383-S390" (accurate about the counter, short of the registry).
- Receipts: `08-registry-vs-readme.txt`, `03-index-rows-target.txt`.
- Fix: index-row cell → "`source:` S383-S391 (opened 2026-10-28)" + add `host-sources.txt`;
  ledger C1 row → "registry rows S383-S391 (counter scores the frozen S383-S390)".

### F2 [weakens the claim] corpus/README.md index row + Frontier bullet: "runtime `hyprctl keyword` are outside the entry" / "runtime `hyprctl keyword misc:disable_autoreload` are outside this round" — contradicted by the entry's own counted rows

- The entry contains **K27** (S389, `Hyprland-HyprCtl.cpp:1223`,
  `` if (COMMAND.contains("misc:disable_autoreload")) ``) and **K28** (:1276,
  `Config::mgr()->reload()`), plus E04 — counted upstream claims, byte-checked (content=33/33),
  and chain step 8 "A keyword that names `misc:disable_autoreload` calls `update()` at once".
- So the runtime-keyword path is *in* the entry at source level; what is outside is executing it.
  Read literally (parallel with "the Lua config provider", which genuinely is outside/UNKNOWN),
  the added sentences tell a reader the entry does not cover the keyword path.
- The entry's own Limits use the accurate boundary ("the watch-plan model's declared divergences …
  runtime keyword … are not facts of this entry"; "Not checked: the `full-reset` branch").
- Receipt: `08-registry-vs-readme.txt` (K27/K28 rows quoted).

### F3 [weakens the claim] SKILL.md probe row (line 226): the model's output is stated as "the inotify watch list Hyprland 0.56.2 registers for the config tree" — no prediction/model qualifier, no divergence list

- The tool's own docstring: "It is a model of a deliberate subset, not Hyprland", with the seven
  declared divergences of registration-v2 E8 (depth cap 16; bytewise glob order vs locale
  collation; the canonical watch prints the **realpath** while Hyprland records the **symlink
  path**; duplicate paths printed separately; `~user` forms; Lua provider; runtime keyword).
- The other three added texts hedge: PROVINCE tool row "static prediction of the inotify watch
  list"; PROVINCE refinement "From these it predicts the inotify watch list"; ledger "Read-only
  prediction"; README Frontier bullet "predicts the watch list from config bytes". SKILL.md — the
  operator-facing file, directly above a concrete sample count (`watches=40`) — is the only one
  that states the answer in the indicative as Hyprland's actual watch list.
- Secondary: the parenthetical "(main config plus its `source =` closure, **with symlink canonical
  watches**)" describes model capability, while the cited run produced 40 primary file watches and
  **zero** canonical watches; and "joined to the **live** `misc:disable_autoreload` value" is the
  tool's field name for a *captured* reply (the row does disclose the capture step, so this part
  is borderline).
- Fix: "a **prediction** of the inotify watch list Hyprland 0.56.2 registers … (model; the seven
  declared divergences are in the tool docstring / registration-v2 E8)".

### F4 [weakens the claim] PROVINCE.md tool row (Writes cell) + Round-56 refinement paragraph + tool-ledger rows: the write-surface sentences are false for `--selftest` and for the harness dispatcher

- PROVINCE tool row Writes cell: "nothing — stdout only (`MADO_WATCH:` and `MADO_WATCH_LIVE:`
  lines)"; refinement paragraph: "It starts no process, opens no socket and writes nothing";
  ledger row: "stdout only".
  But `mado-watchplan.py --selftest` **writes** a 65-file temp tree (dirs, config files, symlinks)
  before removing it, and prints `MADO_WATCH_SELFTEST: 82/82 assertions passed` — a third line
  kind the row's enumeration omits. Proof: ran the selftest with its `shutil.rmtree` disabled —
  65 files materialised (`12-selftest-writes.txt`); the tool's own docstring discloses it
  ("`--selftest` writes only under a private temporary directory that it removes").
- The house convention is to disclose exactly this: the sibling mado-globals row says "`--selftest`
  (63/63 …) writes only inside a private temporary directory it removes" and mado-geometry says
  "`--selftest` writes nothing". The direct template, round-55 `mado-kbdopts.py`, **truly** writes
  nothing in --selftest (verified: 0 files; no write calls) — so the copied claim is true for
  kbdopts and false for watchplan.
- PROVINCE refinement: "writing only under its `--work` directory; **it never writes the lane or
  the fleet repo**"; ledger rows for `quality/check-r56-controls.py` and `quality/r56_ctl_c*.py`:
  "writes only under `--work`". The dispatcher does `sys.path.insert(0, HERE)` +
  `importlib.import_module(...)`, which writes `quality/__pycache__/r56_ctl_c1.cpython-314.pyc`
  **inside the lane tree** (fresh clone: 0 pyc before → 1 after, `13-pyc-write.txt`; the real lane
  already carries `r55_ctl_c1..c3` and `r56_ctl_c1..c3` .pyc files dated 20:45–21:59).
  Mitigation: `__pycache__/` is gitignored, so no tracked file changes — but the sentences as
  written are false. The round-55 rows make the same claim, so this is a carried-over house
  pattern rather than a fresh regression; the round-56 refinement's "never writes the lane" is,
  however, a new absolute.
- Also dropped: the refinement's "The two counters read git objects only … and write nothing"
  omits the C1 counter's own documented exception ("The counter writes nothing except creating
  `--work`") and both counters' `--selftest` writes under `--work/selftest-*`.
- Fix: add the kbdopts/globals-style clause ("`--selftest` writes only inside a private temporary
  directory it removes" / "writes only under `--work` and its import cache") or set
  `sys.dont_write_bytecode` in the dispatcher.

### F5 [weakens the claim] PROVINCE.md tool row: read-surface cell narrower and wider than the tool as integrated

- "the bytes of the `--config` file **(a regular file)**" — the registered and observed behaviour
  is lenient: a missing/directory/unreadable `--config` is never a setup error, it is *listed*
  (registration §C2; verified: `--config <dir>` → `n=1 role=primary … type=dir … via=main`,
  exit 0 — `14-contrasts.txt`). The sibling mado-geometry row states its refusals explicitly; this
  row implies a regular-file requirement the tool does not enforce.
- The "**1 MiB cap**" is attached only to `--getoption`, but the tool applies it to **every** file
  read — config and sourced files too (verified: a 1048577-byte config →
  `MADO_WATCH: SETUP too_large`). The r55 kbdopts row attaches the cap to the config paths; the
  tool-ledger row for watchplan omits it entirely.
- "with `stat`, `lstat`, `realpath`, `glob`, `isdir`, `lexists` and `islink` **on those paths
  only**" — `os.path.realpath` is also applied to the `--display-root` argument (a caller path
  outside the enumerated set), and the row never names `--display-root` at all (the ledger row
  does). Also `os.lstat` is never called directly by the tool — it is reached only inside
  `os.path.islink`/`os.path.lexists` (matches registered §C2 wording; cosmetic).
- Fix: name `--display-root` and its realpath, move/extend the 1 MiB cap to the config and sourced
  files, and state the lenient `--config` acceptance.

### F6 [weakens the claim, mild] README index row / Frontier bullet: masks "with file, directory and symlink-canonical inotify masks" / "registered for files, directories and symlink canonical targets"

- The entry states `source =` lines pointing at directories are "warning, skipped, not added and so
  not watched" (K23) and "no parent directory is ever watched"; a directory therefore never enters
  `m_configPaths` and the directory mask is unreachable for a config tree. The integrated run shows
  40 watches, all `role=primary`, file mask; the tool emits `type=dir` only for a directory passed
  as `--config` itself.
- The Frontier wording "masks are **registered** for … directories" asserts a registration that
  never happens; the index row's compression drops the K23 caveat the entry carries. Fix: "file
  and symlink-canonical masks (the directory-mask branch is unreachable — `source =` directories
  are skipped)".

### F7 [cosmetic] quality/tool-ledger.md row for the C1 counter names "PRED-C1-r56"

- The operative frozen claim (claims-frozen-v2.md; "Where v2 and v1 disagree, v2 wins") is
  **PRED-C1-r56-v2** ("## C1 — coverage (sourced entry) — PRED-C1-r56-v2"), and the sibling C3 row
  correctly uses "PRED-C3-r56-v2". The counter's own docstring also points at "registration.md
  section C1" (v1) although its operative legs are §C1 + registration-v2 E1–E5. Traceability nit.

### F8 [cosmetic] corpus/README.md Frontier bullet: "the drawn effect of a reload"

- Garbled phrase ("… so inotify delivery and the drawn effect of a reload stay unmeasured");
  presumably "downstream effect". Prose nit in an otherwise careful bullet.

### F9 [cosmetic, verified] index row: "30 upstream claims (K01-K30) and 3 host claims (H01-H03); each quote is byte-checked at its pin line"

- The entry also carries **9 extra E-row propositions** (E01–E09, incl. E08/E09 anchored to S391)
  that the row's inventory omits; and while I verified **all 42** quotes byte-exact at their pin
  lines (independent script over the entry tables, 0 failures), **no lane instrument byte-checks
  the 9 E-row quotes** — every counter leg runs over the frozen K/H ids (`all_rows = c1["k"] +
  c1["h"]`; no E rows in the frozen tables). The sentence is factually true of the entry as
  integrated; the gap is that the round's counter proves it for 33 of the 42 quotes only.

---

## Answer to the two specific seat questions

- **Blank README line before the r52 row: not merely harmless — required, and it repairs a
  pre-existing failure.** At the base rev `13f0acbe`, `check-index-rows.py` fails with 3
  `row-outside-map` ERRORs (r52, r52-errata-r53, r55 — the blank line at README:79 ends the
  coverage-map block). At `28fc86ac` the blank line is deleted and the gate is clean
  (rows=71 errors=0). Re-inserting the blank line into the integrated tree reproduces **4**
  `row-outside-map` errors — including the **new r56 row itself** (full-archive `--root`
  experiment, `11-blankline-experiment.txt`). So the deletion is necessary for the round's own row
  to sit inside the map, and it incidentally clears the three pre-existing failures (those rows
  become in-map and pass all checks). It was wave-1-sanctioned (R56ScribeIndex D1: "Drafted fix:
  delete line 79") but none of the four added texts records the repair. It also fixes rendering:
  the r52/r53/r55 block was previously a headerless pipe block, not part of the table.
- **Contradiction with SKILL.md:112 / 197-199: none.** The added sentences report non-observation
  and keep the reload effect unmeasured; they never assert that Hyprland does not auto-reload, and
  the Frontier bullet's source-level chain corroborates the mechanism. Residual: the entry's own
  UNKNOWN ("whether Hyprland reloads on this host after a save") sits against the flat
  SKILL.md:112 claim; the added rows neither create nor reconcile that tension.

---

## Lane state during review

While this seat ran, the lane **working tree** gained uncommitted edits (not made by this seat —
every check above was read-only against committed state at `28fc86ac`): `corpus/SOURCES.md` gains
rows **S392–S395** (per-line anchors for the extra rows: E01→S393 `MiscFunctions.cpp:66`,
E03→S392 `ConfigWatcher.cpp:106`, E04→S394 `HyprCtl.cpp:1190`, E05–E07→S395
`ConfigManager.cpp:630/1838/2134`), and the entry's `source:` line is extended to
"… S391 (PropRefresher.hpp), **S392-S395 (extra-row anchors for E01, E03-E07)** …". Two
consequences once that edit lands:

1. Finding F1's understatement **deepens**: the entry will then cite S383–S395 (thirteen registry
   rows) while the index row still says "S383-S390" and the Frontier bullet says S383-S391.
2. It partially addresses F9's neighbourhood (the E rows get their own per-line anchors), but the
   counter still scores only the 33 frozen K/H rows, so "each quote is byte-checked" remains
   instrument-backed for 33 of what will then be 42+ rows.

---

## Not verified / out of seat

- Whether `watches=40` matches Hyprland's **actual** inotify state on this host — that is
  R56W2RevProcFdinfo's seat; I read no `/proc/<pid>/fdinfo`. The SKILL row's unqualified framing
  (F3) is the doc-side risk; the model/reality agreement itself is unmeasured here.
- The `.pyc`/`--selftest` writes (F4) are confined to gitignored scratch paths (`__pycache__/`,
  mkdtemp) — no tracked file and no repo state is affected; I did not audit whether the C2
  harness's optional `bwrap` path changes that.
