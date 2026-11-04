# D3 — round-76 declaration errata and the r76 counter's docstring text

Seat R77ExecRepairs, round 77, 2026-11-04. Lane HEAD `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.

## 1. `claims-declaration-r76.md:26` — the "fifteen-case" text

Line 26 (frozen historical text, never re-cut):

> against a frozen fifteen-case expectation, and separates four named mutations of the outcome
> rule at unique source anchors.

The frozen set, the contract line and the measurement are sixteen cases:
`controls/c1-outcome-cases-r76.json` (16 cases, sha256 `320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea`);
contract line `cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET` at
`3588a527eba555a94e497097b0467efc04274c6d`.

The append-only errata is already landed at `.ufo/waves/round-76/claims-declaration-r76.md:191`
(12 lines added by `3e35d0a9`; the predicate, labels, control set and kill rule are unchanged —
an errata, never a re-freeze):

```markdown
## Errata (round 77, append-only; never a re-freeze)

The round-76 declaration above says "a frozen fifteen-case expectation". The frozen set, the
counter's contract line and the measurement are sixteen cases
(`cases=16 correct=16 mutants=4 killed=4 base_killed=0` at `3588a527`); the word "fifteen" is a
stale draft label (round-76 closure D3). The predicate, labels, control set and kill rule are
unchanged. The pack's executable status is the counter's contract line, not this sentence; a
docstring-only correction to `quality/counters/c1-r76-outcome-field.py` (the printed example said
`cases=15`, the limits paragraph said "fifteen modes") lands in round 77 with the parity receipt
`.ufo/waves/round-77/receipts/parity-r76-docstring.txt` (identical counts before/after).
```

## 2. The counter docstring (`quality/counters/c1-r76-outcome-field.py`)

At HEAD the file is blob `d74c493a92e79d0df83515abd036277a41d97b14`, sha256
`e6ce2a4829d00f675c9845b806ab22d69f162ba61f4555eae7741d814bc7ac65`. The numeric text is already
fixed (landed by `3e35d0a9`, 2 insertions / 2 deletions versus `2308e12a`):

- line 38: `MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 …`
  (was `cases=15` at `2308e12a`);
- line 52: "sixteen modes are rule separators, not fault coverage" (was "fifteen modes").

**Still stale at HEAD:** docstring lines 26–29 list the *superseded* mutant class:

```
  outcome-term-dropped   the outcome ignores the challenge echo (round-75's surviving C1-M2)
  prefix-match           the echo comparison becomes a prefix test (needs the widened grammar)
  first-witness-wins     the first parsed echo wins instead of the last
  case-insensitive       the echo comparison folds case (needs the case-changing challenge)
```

The executable `MUTANTS` table (lines 64–77) holds the four frozen observable mutants:
`outcome-summary-only`, `outcome-killed-only`, `outcome-killed-any`, `outcome-killed-or`.

## 3. Proposed text-only fix (docstring lines 26–29; zero code lines)

Replace:

```
  outcome-term-dropped   the outcome ignores the challenge echo (round-75's surviving C1-M2)
  prefix-match           the echo comparison becomes a prefix test (needs the widened grammar)
  first-witness-wins     the first parsed echo wins instead of the last
  case-insensitive       the echo comparison folds case (needs the case-changing challenge)
```

With:

```
  outcome-summary-only   the outcome drops the `killed == 2` conjunct
  outcome-killed-only    the outcome drops the green conjunct
  outcome-killed-any     `killed >= 1` instead of `killed == 2`
  outcome-killed-or      green **or** killed 2
```

The frozen predicate, the `MUTANTS` anchors, the control set and the kill rule are untouched.

## 4. Parity (text-only proof)

`parity.txt` — the counter was run on a copy of the HEAD bytes before and after that four-line
substitution, against the frozen revs and control set:

    python3 -I <copy> --repo . --rev 3588a527eba555a94e497097b0467efc04274c6d \
      --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf \
      --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json --scratch-root <scratch>

- before: sha256 `e6ce2a4829d00f675c9845b806ab22d69f162ba61f4555eae7741d814bc7ac65`, rc 0;
- after: sha256 `5984477aa758d2fe562e50c2f8aba1825679448dd5587caac74464524a6a7086`, rc 0;
- both print the identical contract line
  `MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET rev=3588a527eba555a94e497097b0467efc04274c6d`.

## 5. Landing

Apply the four-line replacement above. The numeric-fix parity receipt stays as landed at
`.ufo/waves/round-77/receipts/parity-r76-docstring.txt`; land this receipt as
`.ufo/waves/round-77/receipts/parity-r76-docstring-mutants.txt` and cite it beside the errata.
