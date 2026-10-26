# ExecHarmBase — harm-watch baseline, round 45 w1

**Deliverable:** `.ufo/waves/round-45/w1/ExecHarmBase/baseline.md` (+ 53 receipts in
`.ufo/waves/round-45/w1/ExecHarmBase/gates/`, 324 KB). Round-45 `w2` compares its tip against this, not against memory.

**Method.** Two `git clone --shared` copies of the lane under `/fast/scratch/hyaku/mado-r45/ExecHarmBase/`,
detached at `0c89478af821a6424c9ac922eafe02e39630cf4f` (base) and
`22a8dedd02f507689c567777e0f20b5e645c8ce0` (freeze), each verified with
`git -C <clone> rev-parse --show-toplevel == <clone>` and `rev-parse HEAD` before any gate. Every run's argv,
full output and exit code are in `gates/<gate>-{base,freeze}.txt`. Read-only against the lane: no file of the
lane was written, no mutating git/jj ran in the lane or the fleet, no compositor call (`hyprctl` unused), no
package transaction, no host config touched. No tool was installed.

## Result — 19 gates green at both revs, 3 red at both revs (pre-existing)

Green, base and freeze, byte-equal after masking scratch paths/revs/seeds/nonces
(`gates/normalized-diff.txt`: 21/21 `SAME (modulo masks)`, 0 `DIFFERS`):

| gate | line |
|---|---|
| `quality/check-axis-scores.py --rev … --repo …` (lane bytes **and** rev-committed bytes) | `MADO_AXIS: checked=3 mismatched=0`; navigation 61/61, calibration 71/71, operability 12/12, all `verdict=MATCH` |
| `quality/check-index.py --rev … --repo …` (both byte forms) | `indexed=61/61 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| `quality/counters/c1-r44-geometry-states-v2.py --repo … --rev … --work …` | `fixtures=26/26 tool=present verdict=TARGET_MET`; `clause=b rc=0 selftest=94/94`; `b4 sites=16 killed=16 need=12`; inner r42 `fixtures=37/37 … TARGET_MET` |
| `quality/counters/c2-r44-gkeep-size-request-v2.py --repo … --rev …` | `admitted=1/1 verdict=TARGET_MET`, `clauses=a:1 … j:1` |
| `tools/mado-geometry.py --selftest` | `MADO_GEOMETRY_SELFTEST: 94/94 passed` |
| `tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` |
| census `sources-census.sh validate --root … mado` (current tree) | 7 × `W04`, 1 × `W01`, `ok …/corpus/SOURCES.md`, exit 0 — its payload lines are identical to the freeze's `receipts/census-before.txt` |
| `check-evidence-pointers` | `TARGET_MET`, `dangling_r36=0`, `scratch_tracked=124`, `tip_axis_transcript=1` |
| `check-index-rows` / `--selftest` | `rows=61 errors=0 warns=3` / `10/10` |
| `check-locators --selftest` | `cases=18 passed=18`, `SELFTEST: PASS` |
| `ratio-domain-meta --from 44 --to 44` | `DOMAIN_META: domain=2 meta=0` |
| `counter-selftest` (r26 counters, `--scratch` in scratch) | `SELFTEST pass=59 total=59` |
| `check-counter-discrimination --profile r36` | `controls=25 correct=25/25` |
| `check-r38-discrimination` | `controls=19 correct=19/19` |
| `check-axis-scores --selftest` / `check-index --selftest` | `18/18` / `12/12` |

**Round-45 counters, pre-data (frozen "before"):** at the freeze, `c1-r45-monitors.py` prints
`fixtures=0/49 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` (exit 1) and
`c2-r45-monitor-entry.py` prints `admitted=0/1 verdict=TARGET_MISSED` (exit 1); neither counter exists at the
base (`git ls-tree` empty), matching the committed before-receipts. Counter blobs at the freeze are pinned in
`baseline.md` §2 (`6642ebf…`, `61bd4be…`) so w2 can prove a data commit did not edit them.

**Red at both revs — pre-existing, not round-45 damage** (must stay red identically; a changed failure set is
a finding):

1. `quality/population-suite.py --checker quality/check-population.py` → `SUITE verdict=FAIL fixtures=46 failed=9`
   (whitespace around `cases_pass =`, and the suite's allowed-leg set, disagree with the checker). exit 1 both revs.
2. `quality/check-control-receipts.py --round 44 …` → `verdict=FAIL reason=no-receipt-under-.ufo/waves/round-44/controls/`:
   the gate is per-round over `.ufo/waves/round-N/controls/`, a layout the lane stopped using after round 36
   (round 44 keeps `ctl/` + `receipts/`).
3. same gate `--round 35` (the last round with that layout) → `receipts=100`, `order=ok gap_s=65`, but
   `CONTROL_RECEIPTS verdict=FAIL` because the default shape list is unmet. exit 1 both revs.

## What w2 must hold invariant at the tip (baseline.md §5)

`MADO_AXIS…mismatched=0` with all rows `MATCH`; `MADO_INDEX…missing=0 dangling=0 duplicates=0 coverage=10.0000/10`
with `indexed=N/N` for N = notes at the tip; r44 counters `TARGET_MET` at their frozen counts; `94/94` and
`460/460` unless the tip legitimately edits `tools/mado-verify.sh`; `check-evidence-pointers` `TARGET_MET` with
`dangling_r36=0 inherited_dirty=0`; `check-index-rows errors=0`; the three instrument selftest counts; the same
nine population-suite failures; the r45 counter blobs; and an empty
`git status --porcelain -- quality tools corpus SCORECARD.md LOG.md`.

Expected movement, by registration: `indexed=61/61 → 62/62` (+ one `corpus/README.md` row), axis
`operability 12/12 → 13/13` (and possibly navigation re-derives), `check-index-rows rows=61 → 62` (+ at most
one warn for the new note), census `W04 7 → 9` where the only new `W04`s may be S303 (S162's
`ConfigManager.cpp` URL) and S307 (S158's `HyprCtl.cpp` URL). Any other new `W04`, or a `W01` count above 1,
is a finding.

## Evidence index (all under `.ufo/waves/round-45/w1/ExecHarmBase/`)

`baseline.md` (the baseline, 7 sections) · `gates/axis*.txt`, `gates/index*.txt`, `gates/c1r44-*.txt`,
`gates/c2r44-*.txt`, `gates/geometry-selftest-*.txt`, `gates/verify-selftest-*.txt`, `gates/census.txt`,
`gates/{evidence-pointers,index-rows,locators-selftest,ratio-domain,counter-selftest,counter-discrimination,r38-discrimination}-*.txt`,
`gates/{population-suite,control-receipts,control-receipts-r35}-*.txt` (the reds),
`gates/r45-c1-freeze.txt`, `gates/r45-c2-freeze.txt`, `gates/r45-c{1,2}-base-absent.txt`,
`gates/blobs-{base,freeze}.txt`, `gates/blobs-r45.txt`, `gates/lane-status.txt`,
`gates/normalized-diff.txt`, `gates/quote-check.txt`.

Quote audit: `quote-audit.py` (re-runnable from the seat dir) greps every backticked span of `baseline.md`
against the receipts and writes `gates/quote-check.txt`: `spans=215 found=128 no-receipt-line=87
over-25-words=0`. The 87 are paths, commands, blob ids and placeholders; every quoted metric line resolves
to a `receipt:line` (locators computed by `grep -n`, never typed).

## Risks / residuals

- The baseline records gate **verdicts**, not teeth. That a gate fails on what it names is measured by the
  round-38/44 controls, which are themselves gates here (rows 5, 6, 16, 17) and are green.
- Three reds above are stable at both revs but are real instrument mismatch; w2 should not "fix" them in a
  harm check, and no data seat should derive a claim from them.
- `tools/mado-verify.sh --selftest` hardcodes `/tmp/w5-mado-m52-*` for its fixtures (script-internal, small,
  self-deleted); `TMPDIR` was pointed into scratch for the gates that honour it. No `/tmp` path is cited.
- `check-control-receipts.py` is invocation-sensitive (per-round paths, default shape list); its verdict is
  recorded with the exact argv used, and both invocations agree at base and freeze.
- Scratch (`/fast/scratch/hyaku/mado-r45/ExecHarmBase/`) held only the two clones, scripts and gate work dirs;
  it was deleted after the receipts were copied into this seat directory.

Report: .ufo/waves/round-45/w1/ExecHarmBase.md
