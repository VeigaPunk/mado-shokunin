# The landing kill credit requires the run's own failure detail (round 72)

source: S442 (captured streams are the child's own report) + own-work instruments —
`quality/counters/c1-r72-landing-controls.py` (`credit`), `quality/counters/c1-r72-summary-credit.py`,
frozen declaration `.ufo/waves/round-72/claims-declaration-r72.md` § C1
verified-at: `9bcb4fd5b598844f168230dc05e441721d95b272` (2026-11-04; measured at that revision)
recheck: `python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev REV
--base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root DIR` — last line
`MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=<sha>`

## 1. The rule

A landing kill is credited only when the child's **last** parsed
`MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary reports `p < n` with
`n > 0` **and** the run's own `SELFTEST FAIL` lines number exactly `n − p`; both captured
streams are read. Implemented as `credit(out)` in `quality/counters/c1-r72-landing-controls.py`
(line `mz_killed = bool(credit(mz_out))` in `measure()`).

The arithmetic is the invariant the production instrument already keeps: `check()` prints one
`SELFTEST FAIL <i>: …` line per failing assertion and the summary prints the same `p/n`
(`quality/landing-counters.sh:18,216`). A summary that does not match its own failure lines was
not produced by this run's assertions.

## 2. Decision table

| last summary parses | `n > 0` | `p < n` | `SELFTEST FAIL` lines = `n − p` | credit |
|---|---|---|---|---|
| yes | yes | yes | yes | **killed** |
| yes | yes | yes | no | no credit (bare echo, mismatch, replayed line) |
| yes | yes | no | any | no credit (`p == n` is a green run) |
| yes | no (`0/0`) | — | any | no credit |
| no (crash/garbled/absent) | — | — | — | no credit |

The **last** summary wins: a failing block followed by a green summary is green (an earlier
summary cannot be resurrected), and a green line followed by a failing summary with its own
detail is credited.

## 3. Measured — eight real `bash` fixture modes

Scored by `quality/counters/c1-r72-summary-credit.py` at `9bcb4fd5…`, base harness
(`c1-r71-landing-controls.py`) at `976684a2…` as the do-nothing control
(`.ufo/waves/round-72/measurement-c1-r72.txt`):

| mode | shape | truth | held r71 | r72 |
|---|---|---|---|---|
| `liar-success` | genuine `1/2` + its fail line, exit 0 | pass | pass | pass |
| `stderr-genuine` | genuine `1/2` on stderr only, exit 1 | pass | pass | pass |
| `liar-kill` | `2/2`, unrelated exit 1 | fail | fail | fail |
| `crash-stderr` | exit 2, no summary | fail | fail | fail |
| `bare-failing` | `0/2` line, no fail line | fail | **pass** | fail |
| `mismatch-detail` | `0/2` beside three fail lines | fail | **pass** | fail |
| `last-wins-pass` | `1/2` block, then `2/2` last | fail | fail | fail |
| `last-wins-fail` | `2/2`, then one fail line and `1/2` last | pass | pass | pass |

`correct=8 base_correct=6 verdict=TARGET_MET` (bounded score 10.0000 vs the held 7.5000). The
held rule's two misses are exactly the summary-without-own-detail class: it credits a summary
line any wrapper can echo.

## 4. What the rule does not authenticate

A captured summary **replayed together with its matching detail lines** is byte-identical to a
genuine run; the rule bounds the summary to the run's own fail lines and their count, it does
not provenance-stamp them. The fixed `p < n` + `n > 0` guards keep a green summary, a `0/0`
summary, a crash and a garbled summary at no credit. This is a finite control set (eight
modes), not fault coverage; the fixture lane is the counter's own instrument, not the lane's
real landing instrument.

## 5. Provenance

- Frozen predicate and targets: `.ufo/waves/round-72/claims-declaration-r72.md` § C1 (frozen
  before the instrument existed; held baseline `control-baseline-c1-r72.txt` scored 6/8).
- Frozen mode labels: `.ufo/waves/round-72/controls/c1-modes-r72.json` (sha256
  `18144745d65a00e1d812c663dbace402a5714fde74506f54d9adabe858268c13`).
- Instruments: `quality/counters/c1-r72-landing-controls.py` (selftest 83/83) and
  `quality/counters/c1-r72-summary-credit.py` (selftest 33/33).
- Source ground: S442 (`subprocess.run` capture_output paragraphs) — the child's own captured
  streams are the report; the exit status is a one-bit non-carrier (held S435/S441).
