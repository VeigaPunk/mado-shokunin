# The landing outcome verdict reads the gate's own summary, not its exit status (round 72)

source: S444 (the result object carries the pass/fail fact) + S445 (the official runner derives
its exit from `result.wasSuccessful()`) + own-work instruments —
`quality/counters/c1-r72-landing-controls.py` (`summary_green`, `outcome_verdict`) and
`quality/counters/c2-r72-outcome.py`; frozen declaration
`.ufo/waves/round-72/claims-declaration-r72.md` § C2
verified-at: `9bcb4fd5b598844f168230dc05e441721d95b272` (2026-11-04; measured at that revision)
recheck: `python3 -I quality/counters/c2-r72-outcome.py --repo . --rev REV
--base-rev 976684a27e99c2508037a60eec415f550f53d70e
--controls .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root DIR` — last line
`MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=<sha>`

## 1. The rule

The landing harness's contract verdict greens a run only when the kill count is `2/2` **and**
the extracted instrument's **last** parsed
`MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary has `n > 0` and `p == n`;
a missing or garbled summary earns no green. The child's exit status is printed as evidence and
does not gate the outcome. Implemented as `summary_green(out)` / `outcome_verdict(selftest_out,
killed)` in `quality/counters/c1-r72-landing-controls.py`.

Why this is the doctrine and not a preference: the official unittest runner reports pass/fail
through the result object and derives the process status from it in one line
(`Lib/unittest/main.py:271-275`, S445), and `TestResult.wasSuccessful()` is the documented read
(S444). A status is therefore a projection: one bit, many causes behind it (held S435/S441). A
summary that enumerates the shortfall is the finer record, so a summary/status contradiction is
scored by the summary.

## 2. Decision table

| last summary | `n > 0` | `p == n` | killed | verdict |
|---|---|---|---|---|
| parses, green | yes | yes | 2/2 | `TARGET_MET` (whatever the exit status) |
| parses, failing | yes | no | any | `TARGET_MISSED` (whatever the exit status) |
| `0/0` | no | — | any | `TARGET_MISSED` |
| absent / garbled | — | — | any | `TARGET_MISSED` |
| any | — | — | < 2 | `TARGET_MISSED` |

## 3. Measured — eight frozen `(gate_out, gate_rc, killed)` cases

Scored by `quality/counters/c2-r72-outcome.py` at `9bcb4fd5…` against the held round-71
`outcome_verdict(selftest_rc, killed)` at `976684a2…` as the do-nothing control
(`.ufo/waves/round-72/measurement-c2-r72.txt`):

| case | summary | rc | killed | truth | held r71 | r72 |
|---|---|---|---|---|---|---|
| `green-summary-exit0` | `12/12` | 0 | 2 | MET | MET | MET |
| `failing-summary-exit0` | `3/12` | 0 | 2 | MISSED | **MET** | MISSED |
| `green-summary-exit2` | `12/12` | 2 | 2 | MET | **MISSED** | MET |
| `no-summary-exit0` | none | 0 | 2 | MISSED | **MET** | MISSED |
| `garbled-summary-exit0` | `twelve/twelve` | 0 | 2 | MISSED | **MET** | MISSED |
| `failing-summary-exit2` | `11/12` | 2 | 2 | MISSED | MISSED | MISSED |
| `no-summary-exit2` | none | 2 | 2 | MISSED | MISSED | MISSED |
| `green-summary-killed1` | `12/12` | 0 | 1 | MISSED | MISSED | MISSED |

`correct=8 base_correct=4 verdict=TARGET_MET` (bounded score 10.0000 vs the held 5.0000). The
held rule's four misses are one defect: it reads the exit status in both directions — a failing
summary at exit 0 is green, and a fully green summary at exit 2 is red.

## 4. What this does not establish

- The eight cases are a finite grammar sample, not proof that every instrument prints a summary.
- The counter scores the committed decision functions, not an end-to-end harness execution.
- A summary/status contradiction is resolved by the summary **by design**; a reader who wants
  contradiction itself to be an error is asking for a different contract (r66's `marker_valid`
  leg contract), not this one.
- A green summary printed by a crashing gate after its assertions passed is `TARGET_MET`; the
  crash is visible only in the recorded rc, not in the verdict.

## 5. Provenance

- Frozen predicate, targets and limits: `.ufo/waves/round-72/claims-declaration-r72.md` § C2;
  held baseline `control-baseline-c2-r72.txt` scored 4/8.
- Frozen cases: `.ufo/waves/round-72/controls/c2-controls-r72.json` (sha256
  `640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`).
- Instruments: `quality/counters/c1-r72-landing-controls.py` (selftest 83/83),
  `quality/counters/c2-r72-outcome.py` (selftest 24/24).
- Sources: S444 (`unittest.rst` § `TestResult` `wasSuccessful`), S445 (`Lib/unittest/main.py`
  exit derivation), held S442 (captured streams), held S435/S441 (exit-status vocabulary).
