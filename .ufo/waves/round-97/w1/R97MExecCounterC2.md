# R97MExecCounterC2 — C2 counter-selftest draft

**Status note (post-yield update, same file):** the draft gained three fixes after the first
dry run — (1) the broken-mode leg now writes this counter's own bytes
(`open(os.path.abspath(__file__),"rb").read()`) into the run dir for all three modes
(R97MMutC2 finding: the c1 counter's argparse rejected the runner's flags, so the modes
passed for the wrong reason); (2) fixture resolution — every counter `--selftest` run
gets `MADO_SELFTEST_FIXTURE_DIR` in its child env, pointing at a materialisation of the
committed `.ufo/waves/round-97/selftest-fixtures*` tree at `--rev` (materialised from
git, never the working tree; a `-v2` tree wins when both exist; rc 2 SETUP_ERROR when no
fixture tree exists at `--rev`); (3) the always-OK control (R97MMutC2 F4) — the plain
always-OK stub was unsatisfiable (`stub_flagged` could never be true, so
`always_ok_flagged` reached panel_total while TARGET_MET requires 0). It is now the v2
echo stub + anchored credit rule: the stub prints the result line AND every panel id as
FAIL lines at exit 1 without work; a neutralisation credits the stub only when the
judged instrument's own bytes carry the row's find anchor exactly once — the stub's
bytes carry no anchor, so `always_ok_flagged=0` and `stub_uncredited=panel/panel`; a
runner that credits bare rc+id output would credit the stub on every row and fail the
control. Result line gains `stub_uncredited=<n>/<panel>`. Current sha256:
`bf5352dc23c0aa57c69b3239d30affcf3ecd375150be3e051526dd477fb62521`.

## What was built

The PRED-C2-r97-v1 counter draft at `.ufo/waves/round-97/build/c2-r97-counter-selftest.py`, Python stdlib only, ASCII only.

CLI (exact flag spelling from the seat spec):

```
python3 -I c2-r97-counter-selftest.py --repo . --rev <rev> --panel <json>
  --expect-panel-sha256 <sha> --expect-c1-sha256 <sha> --expect-c2-sha256 <sha>
  --expect-registry-sha256 <sha> --expect-ledger-sha256 <sha> --scratch-root <dir>
  [--timeout SEC]
```

Behaviour: (a) materialises both counters at `--rev` with `git show` into `--scratch-root` and pins their sha256 (`counter_pin=ok,ok`); (b) runs each `--selftest` and parses `MADO_COUNTER_SELFTEST: checks=N failed=0` (green, checks>=6 each); (c) applies every panel neutralisation (`find` exactly once in the counter's bytes, replace, rerun `--selftest`) and requires the declared finding id in the output and exit 1 (`negative_ids == panel`); a neutralisation that still passes is printed as `SURVIVED`; (d) runs every broken mode (missing panel file, fictitious `0`*40 `--rev`, pin mismatch on tampered counter bytes) requiring the declared exit code and `expect_line` substring (`broken_modes == broken`); (e) controls: the base-revision counters (no `--selftest`) must refuse with rc 2 and 0/2 green (`base_refuse`); an always-OK stub (prints the green result line without running checks) must be flagged on every neutralisation — `always_ok_flagged` counts neutralisations the stub is NOT flagged on, so 0 is the declared pass value; (f) counts the registry rows for the four named artifacts in `SKILL.md` at `--rev` (0 at base, 4 after) and runs the materialised `quality/check-tool-ledger.py --repo . --rev <rev>` requiring `uncovered=0` with both counters in the population.

Result line (one per run, stdout):

```
MADO_COUNTER_SELFTEST_COUNT: <TARGET_MET|TARGET_MISSED> pred=PRED-C2-r97-v1 rev=<rev> counter_pin=ok,ok selftest_green=<n>/2 checks=<n>,<n> negative_ids=<n>/<n> broken_modes=<n>/<n> base_refuse=<ok|FAIL> always_ok_flagged=<n> registry_rows=<n>/4 ledger_uncovered_ok=<bool> counters_in_pop=<bool>
```

`MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=PRED-C2-r97-v1 <reason>` (rc 2) on any missing/unreadable input, sha pin mismatch, bad rev, malformed panel, or absent counter/registry/ledger at `--rev`. rc 0 TARGET_MET / 1 TARGET_MISSED / 2 SETUP_ERROR.

Panel schema accepted: `{"counters":[{"path","checks":[{"id","find","replace"}]}],"broken":[{"id","mode","expect_exit","expect_line"}]}` with modes `missing-input|wrong-rev|mutated-tool`. `path` must be exactly `quality/counters/c1-r96-magictext.py` or `quality/counters/c2-r96-selftest-kills.py` (one entry per counter). Broken modes are built by this runner from the `mode` field (no flags in the panel): missing-input runs this counter with `--panel` pointing at a nonexistent path; wrong-rev runs with `--rev 0...0` (40 zeros); mutated-tool runs with `--expect-c1-sha256` set to the sha of the c1 counter bytes plus `# mutated`. All three write this counter's own bytes (`open(os.path.abspath(__file__),"rb").read()`) into the run dir — this was a falsifier finding by R97MMutC2 and is fixed; the modes genuinely exercise this counter's own setup paths.

## Evidence

Real-bytes verification (scratch repo holding the actual `build/c1-r96-magictext-selftest.py` /
`build/c2-r96-selftest-kills-selftest.py` bytes at a scratch rev, the working fixture tree, base
SKILL.md + ledger): full dry run printed `MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED ... 
counter_pin=ok,ok selftest_green=2/2 checks=7,7 negative_ids=0/16 broken_modes=3/3 base_refuse=ok 
always_ok_flagged=16 registry_rows=1/4 ledger_uncovered_ok=True counters_in_pop=True` (rc 1).
- `selftest_green=2/2 checks=7,7`: both real counters green through the fixture materialisation +
  `MADO_SELFTEST_FIXTURE_DIR` env var — the R97MMutC2 incompatibility is fixed and matches their
  independent measurement.
- `negative_ids=0/16` with `SURVIVED` lines: my dry-run panels weaken docstring lines, which cannot
  change the counters' behavioural checks, so survivors are the correct reading; R97MMutC2 measured
  16/16 killed on the same bytes with real find anchors, so the flagged path itself is proven by
  their run plus this runner's credit rule (rc 1 + declared id in output).
- `broken_modes=3/3`: all three modes run this counter's own bytes and genuinely print
  `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR` at rc 2.
- `registry_rows=1/4` is the base SKILL.md (only the mado-mimetext row exists); the 0 -> 4 move is
  the claim's after-state.

Red dry-run: `--panel <missing file>` prints `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=PRED-C2-r97-v1 panel ... missing`, rc 2. A panel with <6 checks per counter or a `0`*40 rev is also SETUP_ERROR rc 2.

Final confirmation on the CURRENT frozen counter bytes (c1 `dd9b5a0b…`, c2 `d4689f5a…` at a
scratch rev holding them plus the committed fixture tree): `MADO_COUNTER_SELFTEST_COUNT:
TARGET_MISSED ... counter_pin=ok,ok selftest_green=2/2 checks=7,7 negative_ids=2/12
broken_modes=3/3 base_refuse=ok always_ok_flagged=0 stub_uncredited=12/12 registry_rows=1/4
ledger_uncovered_ok=True counters_in_pop=True` (rc 1). The 2 credited kills are real
production-path rows (appending a failing check entry to each counter's checks list emits the
declared `C1/C2-fake` FAIL id at rc 1); the echo-stub control is now satisfiable: anchor=0 on
every row, `always_ok_flagged=0`, `stub_uncredited=12/12`. The remaining survivors are the
docstring/no-op rows of my synthetic dry-run panel (their `find` strings are not kill anchors;
R97MMutC2's 16/16 on real anchors covers the kill path independently).

Frozen-panel receipt (R97MMutC2 final pass): `.ufo/waves/round-97/controls/counter-selftest-panel-r97.json`
(sha256 `f380e7efb7e654ca63b97cbcaaaf02a432f8543b220ad7f1b2899a456301d9f5`, contract-3 shape,
2 counters x 8 checks = 16 neutralisations + 3 broken rows) verified against THIS draft
(`bf5352dc…`) plus the frozen counter bytes: 16/16 killed with declared ids, 0 survivors, both
baselines green, 3/3 broken rows, do-nothing control behind (base rc 2, 0/2 green), echo-stub
control `always_ok_flagged=0` / `stub_uncredited=16/16`. Their coverage findings F1-F3 (12/16
rows are check-body edits; check names overstate behaviour) are limits of the counters' own
selftest design, not panel or runner defects; F6 confirms the `MADO_SELFTEST_FIXTURE_DIR` hook
is load-bearing (fix (2) above).

## Notes / risks

- **Finding against R97MExecC2's drafts — WITHDRAWN, stale revision.** I measured
  `C1/C2-result-format` FAIL (`checks=7 failed=1`) on copies taken before their F4 fix; the current
  frozen bytes (c1 `dd9b5a0ba09dc490e286522e9d4d55d60f04dec4274bf456c0a891fa630f61d6`, c2
  `d4689f5a43b3bc38ef45a1eca354169cf5de4b91846bed336b8d15c0ae79f7a3`) assert `src.count(needle)==2`
  (the literal self-references) and measure green (`checks=7 failed=0`, rc 0) — re-verified here on
  the current bytes. The earlier `selftest_green=2/2 checks=7,7` leg above ran against my scratch
  dedup of the older revision; with the current bytes the green leg needs no patch at all.
- **v2 draft exists** (`build/c2-r97-counter-selftest.v2.py`, review-hardened: per-counter broken
  rows with a `counter` field, fixture-scene construction, echo-stub credit rule, base-vs-rev
  registry delta 1 -> 3). It is the stronger instrument; the L1 should freeze one. My file is the
  contract-3 fallback. R97MMutC2 was told both schemas.
- The ledger leg's `counters_in_pop` checks the absence of uncovered rows for the two counter paths
  plus a `population=` summary line; the ledger gate does not print its population list, so this is
  the derivable form of "both counters in the population".
- No tools were installed; no pacman/uv/npx activity this seat.

No other files written. Scratch deleted before yield.
