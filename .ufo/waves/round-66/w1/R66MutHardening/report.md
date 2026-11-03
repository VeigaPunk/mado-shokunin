# R66MutHardening — seat report (mutation-tester, w1)

Full findings and per-mutant tables: `../R66MutHardening.md` (lane-relative
`.ufo/waves/round-66/w1/R66MutHardening.md`). Evidence bundle: `evidence/`.

## Tested bytes (final)

| target | sha256 | selftest |
|---|---|---|
| `.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py` | `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` | 15/15, rc 0 |
| `.ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh` | `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f` | 58/58, rc 0 |

Superseded bytes were re-tested at each revision: C1 `4e1b94ff…`; C2 `1671cebc…`, `f0c8d74f…`,
`f72e579d…`. Drafts were read-only; every mutant ran on a scratch copy; tested hashes were
unchanged before/after their batteries.

## Detectors and outcomes (final bytes)

- C1: five-revision fixture repo plus aux wrong-live-path and planted-`refs/replace` probes.
  Pristine 4/4 with both aux correct; r65 baseline 1/4. Five mutants: 4/5 killed by the published
  three controls + selftest; `c1-m5` (drop `GIT_NO_REPLACE_OBJECTS`) keeps 15/15 and 4/4 and is
  killed only by the replace-ref probe — coverage finding F9.
- C2: green-nav fixture plus marker-faithful stubs. Frozen a–d; extended green, cite-red,
  duplicate marker, zero-citation, `--round 65/64` path log, poisoned `GIT_*`, clean no-round,
  empty population, planted `refs/replace`. Pristine 13/13 + aux correct; old instrument frozen
  a–d 1/4. Ten mutants: 8/10 killed by published a–d + selftest; `c2-m9` (zero-citation) and
  `c2-m10` (replace isolation) survive it and are killed only by the seat probes (F7, F9).
- Earlier revisions: `f72e` 5/7 published (m5/m7 survivors, no (d) ERROR summary); `f0c8` 7/7
  after fixes; `1671` 8/9 (m9 survivor).
- Detector calibration: always-accept stub 1/4, always-reject stub 3/4 (two-sided).

## Commands and rcs (evidence copies named)

| command | rc |
|---|---|
| `python3 c1-r66-8ca.py --selftest` | 0 (`evidence/c1-8ca-selftest.txt`) |
| `bash landing-r66-e4767.sh --selftest --scratch-root …` | 0 (`evidence/c2-e4767-selftest.txt`) |
| `python3 fixture-c1.py --counter c1-r66-8ca.py …` | 0 (`evidence/c1-matrix-pristine-c1-8ca.json`) |
| `python3 fixture-c2.py --instrument landing-r66-e4767.sh …` | 0 (`evidence/c2-matrix-pristine-e4767.json`) |
| `python3 fixture-c1.py --counter quality/counters/c1-r65-register.py …` | 1 (`evidence/c1-baseline-matrix.txt`) |
| `python3 fixture-c2.py --instrument quality/landing-counters.sh … --no-round` | 1 (`evidence/c2-baseline-matrix.txt`) |
| `python3 run-mutants.py --target c1 --src c1-r66-8ca.py …` | 0; 5/5 killed (`evidence/mutants-c1-8ca.json`) |
| `python3 run-mutants.py --target c2 --src landing-r66-e4767.sh …` | 0; 10/10 killed (`evidence/mutants-c2-e4767.json`) |
| superseded records | `evidence/mutants-c1.json`, `evidence/mutants-c2.json`, `evidence/mutants-c2-f0c8.json`, `evidence/mutants-c2-1671.json` |

## Limitations

- Synthetic shape-faithful fixtures, not the official `check-controls.py` (absent at inspection).
  C1 state-cell truth is intentionally unmeasured.
- C2 children are stubs with the real anchored markers (`MADO_USED_BY:`, `LEDGER:`,
  `MADO_CITECHECK:`); the actual four-leg landing GREEN was not evaluated.
- One run per probe; finite kill denominator (5 + 10 mutants), not a correctness proof.
- Selftest checks 46/49 are not fully isolated (F4); zero-citation (F7) and replace-ref isolation
  (F9) sit outside the published denominator and are killed only by the seat probes.
- Six drafts were tested across the wave; verdicts apply to the final shas above.

## Changed drafts

None. No production, peer-draft, lane, fleet, git/jj, host-config or service change. Only this seat's
`report.md`, the sibling `R66MutHardening.md`, and `evidence/**` were written. Scratch
`/fast/scratch/hyaku/mado-r66/R66MutHardening/` was used for fixtures/mutants and removed after the
evidence copy.
