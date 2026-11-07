# R97MExecC2 — C2 self-invocation mode for the two round-96 counters

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/build/c1-r96-magictext-selftest.py`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.py`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/selftest-fixtures/` (8 committed fixture files)

Each counter file is a copy of the base revision file plus an additive block only.
The block is delimited by the marker pair
`# === MADO-COUNTER-SELFTEST-BEGIN` / `# === MADO-COUNTER-SELFTEST-END ===`.
Stripping that block (and the small `--selftest`/`--fixture-dir` dispatch inside `main()`)
leaves the production path byte-identical to `quality/counters/<name>.py`.

## Byte-identity proof

Method: `python3` script read both base and draft, removed the marker block, then
diffed against `quality/counters/*.py`.

- `c1-r96-magictext-selftest.py`: **14 added / 0 removed** lines outside the marker block
  (argparse `--selftest`, `--fixture-dir`, pre-`parse_args` dispatch).
- `c2-r96-selftest-kills-selftest.py`: **14 added / 0 removed** lines outside the marker block.

The two added lines inside `main()` are the `--selftest` flag registration and the
`a = ap.parse_args()`-adjacent dispatch, plus the pre-parse `sys.argv` check that makes
bare `python3 -I <counter> --selftest` work without all required production args.

## Fixture inventory

Directory: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/selftest-fixtures/`

| File | Purpose |
|------|---------|
| `dummy-tool.py` | Pinned dummy tool: selftest prints `MADO_MIMETEXT_SELFTEST: checks=50 failed=0`; `--json` prints a shape-valid answer. |
| `c1-cases.json` | Two-case file, envelope `version=2`, `oracle_src_sha256=0*64`, `glib2=2.90.1-1`, 16 frozen classes, `inputs`/`labels` schema-valid. |
| `c1-mutants.json` | Two mutants with `id`, `find`, `replace`, `class`, `expect`; `find` occurs once in `dummy-tool.py` source. |
| `host-list.txt` | Three absolute host paths. |
| `panel.json` | `{"hand":[], "neutral":[]}` empty panel (shape-valid). |
| `control-kills.json` | Copy of `quality/selftest-kills/check-receipt-presence.json`. |
| `c2-kills.json` | Two-kill file with `tool`, `tool_sha256`, `selftest_argv`, `fail_line_prefix`, `result_line_prefix`, `selftest_checks`, `kills`. |
| `r90-argv.json` | `{"base_rev","argv":["--repo",".","--rev","@REV@","--base","@BASE_REV@","--scratch-root","@SCRATCH@"]}`. |

## Selftest transcripts (green)

### C1 counter

```
$ python3 -I .ufo/waves/round-97/build/c1-r96-magictext-selftest.py --selftest
MADO_COUNTER_SELFTEST: checks=7 failed=0
rc=0
```

Check ids (stable strings):
- `C1-green-target-met`
- `C1-missing-cases`
- `C1-wrong-rev-pin`
- `C1-mutant-mismatch`
- `C1-result-format`
- `C1-no-scratch-left`
- `C1-fixture-parses`

### C2 counter

```
$ python3 -I .ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.py --selftest
MADO_COUNTER_SELFTEST: checks=7 failed=0
rc=0
```

Check ids:
- `C2-green-target-met`
- `C2-missing-panel`
- `C2-wrong-rev-pin`
- `C2-mutant-mismatch`
- `C2-result-format`
- `C2-no-scratch-left`
- `C2-fixture-parses`

### Temp-copy isolation (mirrors C2 counter's `run_counter()`)

Copying each counter to a fresh `mktemp -d` and running `python3 -I <copy> --selftest`
with `cwd` set to the temp dir still resolves the committed fixture directory
because the fallback path is the absolute
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/selftest-fixtures`.
Both return `checks=7 failed=0`, `rc=0`.

## Red runs (deliberately broken fixtures)

### RED 1 — corrupt C1 cases fixture

Copy fixtures, replace `c1-cases.json` with `not json`:

```
$ python3 -I .ufo/waves/round-97/build/c1-r96-magictext-selftest.py --fixture-dir <broken>
MADO_COUNTER_SELFTEST_FAIL: C1-green-target-met
MADO_COUNTER_SELFTEST_FAIL: C1-fixture-parses
MADO_COUNTER_SELFTEST: checks=7 failed=2
rc=1
```

### RED 2 — corrupt C2 panel fixture

Copy fixtures, replace `panel.json` with `{}`:

```
$ python3 -I .ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.py --fixture-dir <broken>
MADO_COUNTER_SELFTEST_FAIL: C2-green-target-met
MADO_COUNTER_SELFTEST: checks=7 failed=1
rc=1
```

### RED 3 — could-not-evaluate

Point `--fixture-dir` at a nonexistent path:

```
$ python3 -I .ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.py --fixture-dir /nonexistent
MADO_COUNTER_SELFTEST: checks=7 failed=0
rc=2
```

## Notes for R97MMutC2 / R97MMutC2b

- Both counters accept `--selftest` and `--fixture-dir` in any order; bare `--selftest`
  alone dispatches before `argparse` enforces required production args.
- Fixture resolution order: `--fixture-dir` > `--repo`-derived `.ufo/waves/round-97/selftest-fixtures`
  > absolute committed path > `__file__`-relative sibling.
- Each check is a stable string id; a `find`/`replace` pair that changes the check body will
  make that specific check return `False` and print `MADO_COUNTER_SELFTEST_FAIL: <id>`.
- The counters keep their production `main()` exit codes: `TARGET_MET=0`, `TARGET_MISSED=1`,
  `SETUP_ERROR=2`, `DRAFT=3`.
- `quality/check-receipt-presence.py` is not ASCII-clean; the C2 selftest block opens it with
  `encoding="utf-8"` and the selftest fixtures are ASCII.


## Post-review fixes (R97MReviewC2)

- Could-not-evaluate now prints `MADO_COUNTER_SELFTEST_FAIL: <id>-fixture-could-not-evaluate` and
  `MADO_COUNTER_SELFTEST: checks=0 failed=1`, rc 2 — no green spelling on a failed evaluation.
- Hardcoded lane root removed from both selftest blocks. Fixture resolution order is now:
  `MADO_SELFTEST_FIXTURE_DIR` env > `--fixture-dir` > `--repo`-derived > walk-up from `__file__`
  > walk-up from `cwd` > `__file__` sibling. The C2 counter's runner must set the env var or pass
  `--fixture-dir` for isolated temp copies; bare `--selftest` works from the lane root.
- New draft sha256: c1 `66b4979c502b8ae278b0c8ec816d50b6a196cd3f4f0f9baa72fee469b547e23d`,
  c2 `dafb7a8b545de79b871bc6aff32ec08bd444c9358ceafe15fbc97e14d0565610`.


## Post-review fixes round 2 (R97MMutC2b blocker)

- Restored absolute committed fixture path as final fallback in both counters, so a lone
  temp copy with no env/`--fixture-dir` still resolves fixtures. Resolution order is now:
  `MADO_SELFTEST_FIXTURE_DIR` env > `--fixture-dir` > `--repo`-derived > walk-up from
  `__file__` > walk-up from `cwd` > absolute committed path > `__file__` sibling.
- C2's `REPO` derivation now works in the runner's hermetic layout: `REPO` is derived from
  `FIX` (`../../../..`), and when `FIX` is the runner's temp `.ufo` path the checks that need
  repo files (`check-selftest-strength.py`, `check-receipt-presence.py`) are resolved relative
  to `REPO`; the runner must place those files under `<root>/quality/` or the checks will
  correctly report could-not-evaluate.
- Verified: lone temp copy `python3 -I <copy> --selftest` -> `checks=7 failed=0` rc=0 for both
  counters; simulated runner layout (counter under `<root>/quality/counters/`, fixtures under
  `<root>/.ufo/waves/round-97/selftest-fixtures/`, cwd=`<root>`) -> green for both.
- New draft sha256: c1 `cc39301e67845723058cc478b7eb90d35be5c094d804a64dc1a13783509528aa`,
  c2 `c5aadb87b1edbe6ca7be09c1b6dec7dfcb2a383bd0165296a1923e1a5eba4109`.


## Post-review fixes round 3 (R97MReviewC2 blocker)

- Both selftest blocks rewritten fixture-only: no repository file is read. C2's four
  repo-dependent checks now assert over fixture JSON shapes only; `REPO` is gone.
- `--fixture-dir` now outranks `MADO_SELFTEST_FIXTURE_DIR` (explicit flag wins).
- Absolute committed path kept as last-resort fallback so lone temp copies stay green.
- Mutant checks strengthened: empty `mutants`/`kills` lists now FAIL the check.
- Verified: in-place green, lone temp copy green (no env), simulated runner layout
  (counter + fixtures only, no quality/ files) green for both counters.
- New draft sha256: c1 `377a34fe822bb567717f28a51d48db3fdcd3978714bafa5c6dd100c4cc15aeb9`,
  c2 `861883b3a823106377fb76f9dd1e8a5b184c1843361de244c4730b29c3dcb9ae`.
- Byte-identity still added=14 removed=0 outside the marker block.


## Post-review fixes round 4 (R97MReviewC2 F4)

- `*-result-format` now bites: asserts the emit statement
  `print("MADO_COUNTER_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))`
  occurs exactly twice in the file (once inside the check's needle literal, once at the
  emit site). Mutating the emit line was measured to print the declared FAIL id with rc 1.
- `*-green-target-met` remains a fixture-shape assertion (documented limit: it proves
  fixture wiring, not the oracle; the production green leg belongs to the L1's counter).
- New draft sha256: c1 `3cb53f2c31d2e22a017d4319061bd1dd2a3407919e686dee4c42412f6a95762c`,
  c2 `5bb32d0a2c0f8b8be7950c3927abe8892d900cea1a50353aba2e63a00efbdd20`.
- Byte-identity still added=14 removed=0 outside the marker block.


## Post-review fixes round 5 (R97MReviewC2 F8 ruling)

- Dropped the absolute committed fixture fallback per reviewer ruling: no
  `/home/vgpnk/...` literal remains in either draft (grep count 0). Resolution order is
  now `--fixture-dir` > `MADO_SELFTEST_FIXTURE_DIR` > `--repo`-derived > walk-up from
  `__file__` > walk-up from `cwd` > `__file__` sibling. A lone temp copy with no flag/env
  now correctly prints could-not-evaluate rc 2 instead of silently reading the lane tree.
- Verified: in-place green, runner-layout green (with and without --fixture-dir — the
  walk-up from `__file__` finds `.ufo/waves/round-97/selftest-fixtures` under the layout
  root), lone temp copy rc 2 could-not-evaluate.
- New draft sha256: c1 `dd9b5a0ba09dc490e286522e9d4d55d60f04dec4274bf456c0a891fa630f61d6`,
  c2 `d4689f5a43b3bc38ef45a1eca354169cf5de4b91846bed336b8d15c0ae79f7a3`.
