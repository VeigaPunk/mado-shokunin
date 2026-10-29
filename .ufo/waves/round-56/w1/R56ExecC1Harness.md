# R56ExecC1Harness — C1 control harness (round 56, wave w1)

## Deliverables (all under `.ufo/waves/round-56/w1/R56ExecC1Harness/`)
- `r56_ctl_c1.py` — the harness module; `run(argv)->int`, also runnable as `python3 -I r56_ctl_c1.py --repo R --rev REV --work DIR [--counter PATH] [--claim c1]`.
- `witness/build_witness.py` — builds the witness tree (frozen tables + pins + README row + registry rows S383-S390 + generated entry) as a one-commit git repo.
- `witness/ref_counter.py` — witness reference counter (registration §C1 legs; NOT the real counter, see A1 for its one declared choice).
- `witness/stub_green.py`, `witness/stub_reject_min.py`, `witness/stub_reject_shotgun.py` — always-green, reject-everything (one fixed leg), reject-everything (names every leg).
- `witness/test_matrix.py` — mutation-scope check + 9 leg-disabled variants + protocol-defect variants.
- `witness/entry-witness.md` — the generated witness entry; `receipts/{four-counters,matrix,edge-runs,witness-commit-stat}.txt`.

## What the harness does
1. Resolves `--rev`, reads `frozen-tables.json` from the blob at `--rev`, and checks its sha256 against the embedded `d50d2b7b…f9af` (mismatch or absence = setup error, exit 2, nothing on stdout).
2. `git archive` of `entry`, tables, `fetch/` pin dir, `corpus/README.md`, `corpus/SOURCES.md` at `--rev`, extracted with `tar -x` (symlinks/modes kept) into `<work>/c1h-*/good-tree`. Counter = `--counter PATH` or `quality/counters/c1-r56-autoreload-entry.py` exported at `--rev` (absent → good=bad, 0/10, exit 1).
3. Per run (good + 10 controls): `D=$(mktemp -d -p <work>/…)`, `git -C D init`, asserts `rev-parse --show-toplevel == D`, copies the good tree, applies ONE mutation, commits as `-c user.name=ctl -c user.email=ctl@ctl`, runs `python3 -I counter --repo D --rev <sha> --work <w>` with cwd=`<w>`, env scrubbed to PATH/HOME=work/TMPDIR=work/LC_ALL/GIT_CONFIG_* (no inherited `GIT_*`; caller `GIT_DIR=/nonexistent` verified harmless, edge run G), 120 s timeout.
4. Anti-sniffing (the counter must know nothing about controls): scratch dir names, commit message and work-dir names are neutral (`scratch-*`, `ctl scratch commit`, `cwork-*`), controls run in random order (`SystemRandom`), the log is printed in canonical order.
5. Pass rules. `good=ok` iff counter prints exactly one parsable line, `rev=<scratch sha>`, `rows=30 hosts=3 sources=30 scope=30 content=33 new_rows=8`, `TARGET_MET`, `missed=none`, exit 0. A control passes iff exit 1, exactly one parsable line, `verdict=TARGET_MISSED` (never TARGET_MET), every `missed` item inside the registered leg grammar, and the required leg present. Control 2 needs ≥1 `tok:<id>` leg AND `content=e/33` with e<33. Denominator is the literal 10 (a dropped control cannot pass). stdout is the single line; per-control detail and non-binding "collateral legs" notes go to stderr; exit 0 only if `good=ok` and k=10, 1 on FAIL, 2 on setup error.

Mutations (each edits exactly the files listed; verified by `diff -rq` against the good commit, `receipts/matrix.txt`):
| # | name | edit | required leg | files changed |
|---|---|---|---|---|
|1|entry-absent|delete entry|`entry_absent`|entry|
|2|junk-placeholders|every K/H proposition cell replaced by the frozen placeholder texts|`tok:*` + content<33|entry|
|3|false-number|K04 proposition `+ " The value is capped at 200 by this call."`|`num:K04`|entry|
|4|cross-pin-source|K10 src S383→S385|`source_cell:K10`|entry|
|5|scope-swap|registry row S399 = copy of S383 row (same URL) with tier A, mined, 2026-10-28, used-by=entry, anchor `ConfigWatcher.cpp:1-10`, inserted after S383; K10 cites S399|`scope:K10`|entry + SOURCES.md|
|6|provenance-dangling|first `source:` line (first 30 lines) `+ ", S999"`|`prov`|entry|
|7|dropped-row|delete K17 row|`row:K17`|entry|
|8|edited-quote|last quoted char of K05's backticked quote cell → `.` (identifier tokens stay intact, so only the quote leg is hit)|`quote:K05`|entry|
|9|pin-byte|first byte of `fetch/Hyprland-ConfigWatcher.cpp` XOR 0x01 (line 1; no frozen row quotes line 1)|`pin_hash`|pin|
|10|new-row-missing|delete registry row S390|`new_rows`|SOURCES.md|
Row finding is fence/HTML-comment aware (``` / ~~~ with 0-3 leading spaces); a mutation that cannot be applied exactly once (missing/duplicated row, non-regular file) fails its control ("mutation not applicable").

## Results (witness tree, commit `66f19e4e`, built from lane `2aa347b1`; real commands in `receipts/`)
```
ref_counter            MADO_R56_CONTROLS: claim=c1 good=ok  controls=10/10 verdict=OK    rc=0
stub_green (always green)MADO_R56_CONTROLS: claim=c1 good=ok  controls=0/10  verdict=FAIL  rc=1   (each control: "verdict=TARGET_MET (mutant admitted)")
stub_reject_min        MADO_R56_CONTROLS: claim=c1 good=bad controls=0/10  verdict=FAIL  rc=1
stub_reject_shotgun    MADO_R56_CONTROLS: claim=c1 good=bad controls=10/10 verdict=FAIL  rc=1   (names every leg: passes the leg tests, good=bad still fails it)
```
Leg-disabled variants of the ref counter (one leg removed each): each loses exactly its control and keeps `good=ok` → 9/10 FAIL, rc 1: entry_absent→CTL-01, prov→06, num→03, source_cell→04, scope→05, quote→08, row→07, pin_hash→09, new_rows→10, tok+content→02. Protocol defects: exit 0 on miss → 0/10; MET with legs → 0/10; two stdout lines / crash rc2 / wrong `rev=` / leg outside the grammar → good=bad 0/10.
Edge runs (`receipts/edge-runs.txt`): lane rev without counter → `good=bad controls=0/10`; rev without tables, unknown rev, missing args → setup error rc 2, empty stdout; default counter exported from `--rev` works (witness copy with counter committed: 10/10 OK); no `--work` leftovers.

## Ambiguities / defects found in registration (registration.md wins; I followed it literally unless stated)
- **A1 `quote:` vs `row:` for control 8.** Leg table: `quote:<id>` = "the frozen quote is a substring of pin line"; row grammar says the quote cell *is* the frozen quote. Read literally, editing a char in the K05 quote cell surfaces only as `row:K05`, and `quote:K05` (the required leg) would never be emitted because the frozen quote still matches the pin. The counter author must emit `quote:K05` when the ROW's quote cell ≠ frozen quote or ≠ pin substring (as `host:` explicitly uses "the quote the ROW carries"). My witness counter does this; a literal-only counter would score 9/10 on this harness. Flag to the counter seat/L1.
- **A2 Control 2 "content shortfall".** `content` is not in the leg table; I read it as `content=e/33` with e<33 (plus ≥1 `tok:<id>` leg). In the witness the junk text shares `source` with K23's quote, so tok:K23 passes (32 tok legs + e=1 survive); that is why the check is "≥1 tok leg", not "all".
- **A3 Control 5/10 parentheticals.** "(and `source_cell:K10`)" / "(and `source_cell:` of the K rows citing S390)" are not enforced (registration: pass = required leg only); they are reported as non-binding notes. Observed in the witness: ctl 4 → also `scope:K10`; ctl 5 → `source_cell:K10`, `scope:K10`, `prov` (see A4); ctl 10 → `prov` (S390 stays on the `source:` line but is no longer a registry row), `source_cell:K29/K30`, `scope:K29/K30`, `new_rows`.
- **A4 `prov` in control 5.** K10 now cites S399, which is not on the entry's `source:` line, so a faithful counter also names `prov` ("source: set contains every S-id cited by a K row"). Harmless for pass, but the control is not a pure `scope`-only mutation.
- **A5 Archive scope.** Spec says archive "the good tree"; I archive only the five path groups the counter is registered to read (entry, tables, `fetch/`, README, SOURCES.md) — the lane tree is 389 MB. A counter reading any other path at `--rev` would get good=bad here.
- **A6 Control 9 line.** XOR on byte 0 of the pin; if that byte is ≥0x80 or becomes `\n`/`\r` the control reports "mutation not applicable" (not the case for the real pin: first byte flips cleanly in the witness run).

## Not verified / limits
- The real entry, real counter and real registry rows S383-S390 do not exist yet; everything above ran on the generated witness (lexical filler propositions, synthetic registry rows with the grammar-required URL/anchor/used-by shape) and on my own reference counter. The harness has NOT been run against the real counter.
- A counter that sniffs its environment beyond what is hidden (e.g. compares the tree to the frozen tables to infer mutations) can still pass (declared round-55 limit).
- No hold-out files for C2 were looked for or touched. No tools installed; no host, lane tracked file, git or jj state mutated; scratch `/fast/scratch/hyaku/mado-r56/R56ExecC1Harness/` removed.
- Re-run recipe: `python3 -I witness/build_witness.py --repo <lane> --src-rev 2aa347b1 --out <scratch>/w` then `python3 -I r56_ctl_c1.py --repo <scratch>/w --rev HEAD --work <scratch>/hw --counter witness/ref_counter.py`.
