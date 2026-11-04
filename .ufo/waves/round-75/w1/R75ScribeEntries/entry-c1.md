---
source: own-work — `.ufo/waves/round-75/{claims-declaration-r75.md,controls/c1-harness-cases-r75.json,measurement-c1-r75.txt}`; `quality/counters/{c1-r75-landing-controls.py,c1-r75-harness-witness.py,c1-r72-landing-controls.py}`; external S-row citation reserved for the L1
verified-at: `def73656c94f0e88bd671cfb4a65124338261722` (freeze and instruments; the supplied measurement names this revision, not a commit containing the receipt)
recheck: `python3 -I quality/counters/c1-r75-harness-witness.py --repo . --rev <rev> --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root DIR` — `cases=11 correct=11 base_correct=6 verdict=TARGET_MET`
---

# Wiring witness credit into the landing harness (round 75, C1)

## 1. The closed gap

The round-74 witness rule explicitly left harness wiring open. The held round-72 harness
credits the M-Z zero-citation mutant on arithmetic alone: the last parsed selftest summary has
`n > 0`, `p < n`, and exactly `n - p` matching `SELFTEST FAIL` detail lines. A captured report
with matching detail lines therefore earns the same credit as a current report.

`quality/counters/c1-r75-landing-controls.py` adds a per-run challenge to that actual harness
pipeline. It loads the round-72 generation from the measured revision, refusing bytes whose
SHA-256 differs from `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d`.
The imported generation retains extraction, the instrument selftest, M-Z clause deletion and
the M-R replacement-ref leg; it is not rewritten.

## 2. The successor rule

One `secrets.token_hex(8)` challenge is generated per harness run and passed to the child in
`MADO_LANDING_NONCE`. M-Z credit requires both the held arithmetic and the child's **last parsed**
`MADO_LANDING_WITNESS: <16 hex>` echo to equal that challenge byte-exactly. The parser accepts
either hex case; equality does not normalise it. A malformed later marker does not replace a
parsed witness.

The contract outcome separately requires the held green summary (`n > 0`, `p == n`), the same
exact echo, and both mutants killed (`2/2`). Exit status alone cannot green the outcome. The
standing `quality/landing-counters.sh` echoes only a well-formed supplied challenge; absent
challenge adds no output for held callers.

## 3. Eleven frozen fixture modes

The frozen set is `.ufo/waves/round-75/controls/c1-harness-cases-r75.json`, SHA-256
`f1e851a9d6133b44f6d538e97c8448bbeb174dcb5ba0a6906fe962ed3e8a6c31`. Each mode runs through
real `bash` fixture children and the extraction/mutation harness pipeline. Here pass/fail is the
**M-Z credit decision**, not the overall harness exit or contract verdict.

| frozen case | expected credit | held round-72 | successor | separator |
|---|---|---|---|---|
| right | pass | pass | pass | matching arithmetic and exact echo |
| liar-success | pass | pass | pass | exit success does not override failing assertion arithmetic |
| uppercase-echo | fail | pass | fail | uppercased echo is not byte-exact |
| stale-witness | fail | pass | fail | captured old witness |
| absent-witness | fail | pass | fail | no parsed witness |
| wrong-witness | fail | pass | fail | wrong token |
| last-wins-wrong | fail | pass | fail | last parsed witness overrides the earlier exact echo |
| crash | fail | fail | fail | no summary |
| zero-denominator | fail | fail | fail | `0/0` is not a kill |
| mismatch-detail | fail | fail | fail | detail count does not equal the summary shortfall |
| green-mutant | fail | fail | fail | `2/2` reports no failed assertion |

The supplied `.ufo/waves/round-75/measurement-c1-r75.txt` names freeze revision
`def73656c94f0e88bd671cfb4a65124338261722` and reports:

```
MADO_R75_HARNESS_WITNESS: cases=11 correct=11 base_correct=6 verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722
```

The held leg misses exactly the five witness separators. `TARGET_MET` requires all three
counts (`11`, `11`, `6`); the counter returns 0 when met, 1 for measured misses, and 2 for
usage/setup errors without a contract line. This scribe did not rerun the measurement.

## 4. What the challenge does not authenticate

- It authenticates the run's echo, **not the truth of the assertions**. A child can echo the
  current challenge and invent matching detail lines; the arithmetic still accepts them.
- Eleven modes separate these rules; they are not fault coverage. Fixture lanes are test
  doubles, not the production landing instrument.
- The challenge is not proof that it was unseen in transit; replay of a live challenge is not
  excluded by equality alone.
- The frozen generation is imported, not edited. Its byte pin makes generation drift a setup
  error; this claim does not re-implement extraction or the M-R leg.

## Receipt provenance

The measurement names the freeze/instrument revision above; the receipt is committed with this
round's landing, rather than being part of that measured revision (landing status supplied by
the L1, not independently observed by this scribe). The L1 supplies the external S-row citation.
