# R55 w1 — seat R55ExecC1Harness (C1 control harness draft)

Draft only; the L1 integrates. No tracked file, git/jj state of the lane or host state was touched; no subagent, no background job, no pacman/tool install. Scratch `/fast/scratch/hyaku/mado-r55/R55ExecC1Harness/` removed (transcript copied first).

## Deliverables (all under `.ufo/waves/round-55/w1/R55ExecC1Harness/`)
- `r55_ctl_c1.py` — module exposing `run(argv)->int` (also `python3 -I r55_ctl_c1.py ...`). Args `--repo --rev --work [--counter PATH]` (a `--claim c1` is tolerated for a wrapper; `c3`/others are a usage error).
- `transcript.txt` — full output of `tests/run_tests.sh` (cases a–i).
- `tests/` — `gen_synth.py` (synthetic good tree from `frozen-tables.json`: entry, README row, SOURCES rows S052/S316-S319/S378-S380, real pins copied from `fetch/`), `counter_ref.py` (minimal correct counter, test-only; embeds sha256 `bf46c889…9490` of the frozen `frozen-tables.json`), stubs `stub_green|red|silent|noisy.py`, `run_tests.sh`.

## How the harness works
1. Resolves `--rev`, reads `frozen-tables.json` from it (git objects only; ls-tree + cat-file blob), takes `entry`, `pin_dir`, `pin_sha256` from it.
2. Needed paths only: entry, `corpus/README.md`, `corpus/SOURCES.md`, `frozen-tables.json`, whole `pin_dir`. Counter: `--counter PATH`, else `quality/counters/c1-r55-kbd-entry.py` at `--rev` (absent ⇒ `good=bad controls=0/7 FAIL`, exit 1, not a crash).
3. For good + each control: `mkdtemp` under `--work`, `git init`, asserts `rev-parse --show-toplevel` == dir, writes files, `-c user.name=ctl -c user.email=ctl@ctl commit`, all via `git -C`. Git env: `GIT_CONFIG_GLOBAL=/dev/null`, `HOME`/`TMPDIR`=work.
4. Runs `python3 -I <counter> --repo <scratch> --rev <scratch-commit-sha> --work <w>` (cwd = w, 120 s timeout).
5. Expected verdicts/legs are held in the harness: good needs `TARGET_MET missed=none rows=18/18 hosts=6/6 sources=n/n new_rows=3/3`, rev echoed, rc 0. A control needs `TARGET_MISSED`, rc 1, the required leg (`entry_absent`, `quote:K04`, `anchor:K01`, `source_cell:K10`, `row:K17`, `host:H02`, `pin_hash`). Extra strictness beyond the registration text (shotgun guard, M54-6 spirit): stdout must be exactly ONE non-empty line (frozen sentence "prints one line"); for CTL-2..7 `entry_absent` and any id-leg naming a row the mutation did not touch fail the control (owned ids: K04; K01; K10; K17; H02; K08,K09 for the IKeyboard.cpp pin). A counter that always prints every leg therefore fails.
6. stdout is exactly `MADO_R55_CONTROLS: claim=c1 good=<ok|bad> controls=<k>/7 verdict=<OK|FAIL>`; per-control detail on stderr; exit 0 OK / 1 FAIL / 2 setup error (bad args, unresolvable rev, unreadable `--counter`, no tables). Work subdir removed in `finally` (0 leftovers shown).
7. Mutations are exact: CTL-2 `std::max(0, REPEATRATE);`→`… ;` in the K04 row; CTL-3 K01 anchor cell `:1220`→`:1219`; CTL-4 K10 S-id cell→`S316`; CTL-5 delete K17 line; CTL-6 `repeat_delay = 250`→`300` in H02 row; CTL-7 first nibble of the IKeyboard.cpp sha in the tree's `frozen-tables.json` AND one space appended to its pin. A mutation that cannot apply (row missing/duplicated, string absent, no-op) fails that control with the reason.

## Results (decisive lines; full text in `transcript.txt`)
```
(a+b) synthetic tree + minimal correct counter : MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK     rc=0
      per control: absent→entry_absent; spliced→quote:K04; anchor→anchor:K01; source→source_cell:K10; dropped→row:K17; host→quote:H02,host:H02; pin→tables_sha,pin_hash
(c) always-green stub                          : MADO_R55_CONTROLS: claim=c1 good=ok controls=0/7 verdict=FAIL   rc=1
(d) always-red stub (all legs, every run)      : MADO_R55_CONTROLS: claim=c1 good=bad controls=1/7 verdict=FAIL   rc=1
extra: noisy (correct counter + 1 extra line)  : good=bad controls=0/7 FAIL
extra: silent stub (no output)                 : good=bad controls=0/7 FAIL
extra: anchor-blind counter (one leg removed)  : good=ok controls=6/7 FAIL
(h) no --counter, counter committed at --rev   : good=ok controls=7/7 OK  rc=0
(i) bad rev / missing --counter                : setup error, rc=2
real lane HEAD (counter not yet committed)     : good=bad controls=0/7 FAIL rc=1 (counter absent at dbc2eefe)
```
M54-6 satisfied: the always-green stub scores 0/7 and FAIL.

## Defects / ambiguities found
1. **K16 frozen quote contains `||`** (`if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`, `frozen-tables.json` c1.k K16), while registration §C1 says "no `|` inside a cell". The row is a valid markdown row only if the quote is written raw; any counter that does `line.split("|")` will mis-split K16 (my first `counter_ref` did: `good=bad missed=row:K16`). The scribe/counter must parse the quote as the backticked tail. The harness's own row edits touch only K01/K04/K10/K17/H02, none with pipes, so it is unaffected.
2. **`source_cell:K17`**: rule says the URL must "contain the frozen commit", but the K17 pin is wayland and S052's URL (`…/-/raw/1.26.0/protocol/wayland.xml`) carries tag 1.26.0, not `efb50993…`. A literal counter fails good on K17. `counter_ref` exempts wayland from the commit test; the real counter needs the same ruling (or a different S-id mapping).
3. **CTL-6 collateral leg**: forging the H02 quote cell makes both `quote:H02` (cell ≠ frozen) and `host:H02` (cell not in pin line) true; the harness requires `host:H02` and tolerates `quote:H02` (same id). A counter using only the frozen quote for `host:` would never fire it — registration reads "a H row whose quote is not a substring", i.e. the row's quote.
4. **CTL-7 collateral**: a counter naturally also prints `tables_sha` (tables hash differs from the embedded constant); allowed. K08/K09 legs are also allowed (their pin changed).
5. `rev=` echo: the harness passes the scratch commit sha (not the caller's `--rev`) to the counter and requires that exact value echoed. If L1 wants the counter's printed rev to be the caller's rev, say so; not covered by the frozen text.
6. Sources counts `sources=<n>/<n>` are only checked as n==n, n≥1 (the frozen text does not say what n counts).

## Not verified
- Not run against the real counter/entry (neither existed at lane HEAD `dbc2eefe`); only the synthetic tree + test counter.
- `check-r55-controls.py` (the L1's wrapper with `--claim`) was not seen; `run(argv)` takes no `--claim` requirement.
- No build/lint/test suite of the lane was run. Hold-out: none seen. Host: no hyprctl or config read was needed.
