# The landing harness's contract outcome field — what it certifies and what it cannot (round 76)

Lane: mado-shokunin. Round 76, claim C1 (calibration). Measured instrument:
`quality/counters/c1-r76-outcome-field.py`; measured content
`6806b4dc8b46fb07e8759983f323267f6b32b763`; base `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`.
Every number below is a line in `.ufo/waves/round-76/measurement-c1-r76.txt` (re-executed)
or `.ufo/waves/round-76/receipts/label-derivation-r76.txt` (evidence-verified labels).

## 1. Why the outcome field needed a counter of its own

The landing harness (`quality/counters/c1-r76-landing-controls.py`, wrapping the frozen
round-72 generation) prints two decisions on one row:

```
MADO_R76_LANDING_CONTROLS: selftest=<p/n|none> mz=<pass|fail> mr=<pass|fail> killed=<n>/2
                          baseline=0/2 witness=<ok|absent|mismatch>
                          verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

`mz=` is the M-Z kill decision (does the extracted instrument's red summary subtract exactly
its own failure lines, with the per-run challenge echoed). `verdict=` is the contract
outcome: green iff the extracted instrument is green **and** both baseline mutants were
killed (`killed == 2`). The held round-75 counter (`c1-r75-harness-witness.py`) parses `mz=`
only, so any rule change confined to the outcome clause is invisible to every denominator
the lane held before this round (`corpus/lessons/round-75.md`, planned item 1).

The successor counter runs sixteen real `bash` fixture lanes through the actual pipeline
(extraction, instrument selftest, M-Z zero-citation clause deletion, M-R replacement-ref
pair) and scores **both** fields per case. Receipt line:

```
MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET
```

The do-nothing control (the held `mz=`-only scoring rule, `control-baseline-r76-matched.txt`) scores
16/16 on `mz=` and kills 0/4 mutants: the control cannot reach the target. (The historical
`control-baseline-r76.txt` scored the v1/v2 fifteen-case set and is kept beside it, append-only.)

## 2. The negative result: an echo-dropping outcome mutation is unobservable

Round-75's planned item 1 asked for exactly one mutation class: drop the echo term from the
outcome clause (`green(out, nonce) := r72_green(out)`), and score it. That cannot be scored
through this field, and the reason is structural:

| case | unmutated summary | M-Z killed | `verdict=` |
|---|---|---|---|
| `right` | 2/2 green | yes | `TARGET_MET` |
| `green-absent` | 2/2 green | **no** | `TARGET_MISSED` |
| `always-red` | 1/2 red | yes | `TARGET_MISSED` |

The M-Z kill already requires the run's echo of the per-run challenge, and `verdict=` is
green only when `killed == 2`. So on every reachable case, `killed == 2` already implies the
echo matched, and dropping the echo from the outcome clause changes no published field.
Measured before the frozen set moved to the observable class: the echo-dropping mutation scored
16/16 and was not killed (round-76 declaration §C1 and `corpus/lessons/round-76.md` M76-2; the
v1/v2 run's own receipt is the historical `control-baseline-r76.txt`). This is a *negative
result*, recorded rather than papered over.

What remains observable is the published field's own conjuncts. Four named mutations, each
anchored once at `outcome_green`'s single return line:

| mutant | rule change | separator case | score |
|---|---|---|---|
| `outcome-summary-only` | drop `killed == 2` | `green-absent` (green, killed 1) | 15/16 |
| `outcome-killed-only` | drop the green conjunct | `always-red` (red, killed 2) | 15/16 |
| `outcome-killed-any` | `killed >= 1` | `green-mutant` (green, killed 1) | 15/16 |
| `outcome-killed-or` | green **or** killed 2 | `always-red` | 14/16 |

`always-red` is the shape that separates a rule ignoring the green conjunct: the unmutated
summary is red while the Z-clause-deleted run is still credited, so `killed=2` fires with a
red instrument. Without that case a "killed-only" rule and the correct rule are identical on
every other fixture.

## 3. Two mechanical fixes the round carries

- **Widened witness grammar (G1).** The witness regex is `[0-9a-fA-F]{16,}`, not exactly
  sixteen. An over-long echo is then a *parsed mismatch* rather than "no witness", which is
  what makes a prefix-matching implementation observable at all. Selftest asserts both the
  parse and the mismatch (`MADO_R76_HARNESS_SELFTEST: 23/23`).
- **Case-changing challenge (G2).** The per-run challenge is drawn by rejection sampling
  until it contains at least one `a-f` letter, so uppercasing it always changes its bytes.
  This closes round-75 M75-4's probabilistic oracle: the counter prints
  `MADO_R76_CHALLENGE ... has_letter=yes` per case and the selftest asserts 200 draws all
  carry a letter (`MADO_R76_OUTCOME_FIELD_SELFTEST: 19/19`).

## 4. Declared limits

- The mutants patch the outcome helper only; the kill path stays correct by construction,
  which is exactly why the held mz-only rule cannot see them.
- The echo term is **not** certified through `verdict=` (see §2); it is certified through
  `mz=`, which the held counter already scored.
- The fixture lanes are test doubles, not the production instrument; the sixteen cases are
  rule separators, not fault coverage.
- A challenge authenticates the run's echo, not the truth of the assertions: a child that
  echoes the challenge and reports arithmetic it did not perform still passes the harness's
  arithmetic check.

## 5. Recheck

Re-run the counting command in `.ufo/waves/round-76/claims-declaration-r76.md` § C1 against
`6806b4dc…`; exit 0 and the exact contract line above are the pass condition. The label set
is `controls/c1-outcome-cases-r76.json` (v3, sha256 `320f7e6b…`); a label may only be changed
through a new round's declaration, never in place.

Sources: S450 (the caller-supplied challenge token and the child's echo). S455 grounds the round's C2/D3 rule and is cited in `corpus/knowledge/interprocedural-del-r76.md`, not here.
