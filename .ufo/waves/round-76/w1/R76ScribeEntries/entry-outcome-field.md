---
source: own-work — committed round-76 declaration, measurements and label derivation (locators below); predecessor corpus/knowledge/harness-witness-credit-r75.md
verified-at: cb713254ee9926e036e594312fdc61b57825526b (recorded measurement revision; not a new execution)
---

# Score the contract outcome separately from M-Z (round 76, C1)

## Evidence locators

All paths below are relative to the lane root; `D:50-55` means the committed path assigned to D, lines 50–55.

| Alias | Committed path |
|---|---|
| D | `.ufo/waves/round-76/claims-declaration-r76.md` |
| M | `.ufo/waves/round-76/measurement-c1-r76.txt` |
| L | `.ufo/waves/round-76/receipts/label-derivation-r76.txt` |
| H | `quality/counters/c1-r76-landing-controls.py` |
| C | `quality/counters/c1-r76-outcome-field.py` |
| P | `corpus/knowledge/harness-witness-credit-r75.md` |

## The observable field, not a proxy

The predecessor scores only M-Z credit and explicitly does not certify the outcome clause (P:72-74). The successor scores both `mz=` and `verdict=`; its published contract is `MADO_R76_LANDING_CONTROLS: ... mz=... ... verdict=...`, where the outcome is `TARGET_MET` only when the extracted selftest is green, its witness equals the run challenge, and `killed == 2` (D:23-27; H:137-150,228-234).

[INF] Scoring M-Z alone cannot certify this additional conjunction: a mutation confined to the outcome helper leaves M-Z untouched. This inference is bounded by the declared mutation scope, and the measured held score is 16/16 on each mutated harness (D:82-87; M:19-22).

| Observable outcome mutation | Rule change | Declared separator | Measured two-field score; held mz-only score |
|---|---|---|---|
| `outcome-summary-only` | Drop `killed == 2` | `green-absent`: green, killed 1 | 15/16; 16/16 |
| `outcome-killed-only` | Drop green conjunct | `always-red`: red, killed 2 | 15/16; 16/16 |
| `outcome-killed-any` | Replace equality by `killed >= 1` | `green-mutant`: green, killed 1 | 15/16; 16/16 |
| `outcome-killed-or` | Replace conjunction by OR | `always-red` | 14/16; 16/16 |

Rule/separator provenance: D:57-65; replacement expressions: C:79-91; measured scores: M:19-22. A kill is implemented as `score < len(cases)`, with both fields required for a correct candidate case and only M-Z required for the held leg (C:383-399).

## Negative result: dropping the outcome echo is unobservable

The originally proposed echo-dropping outcome mutation cannot be separated through `verdict=`: the outcome already requires both kills, while the M-Z kill itself requires the echo. Removing the redundant outcome echo test therefore changes no reachable published field. This certificate covers the observable green and killed conjuncts, **not** independent enforcement of the echo conjunct (D:50-55,82-87; H:141-150).

## Frozen labels and deterministic uppercase separator

The final label set is v3, sixteen modes, sha256 `320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea`; the declaration discloses replacement of v1's summary-only outcome labels and v2's unobservable echo mutation before final scoring (D:39-48; M:1).

| Cases | Expected M-Z / outcome | Label evidence |
|---|---|---|
| `right`, `liar-success` | pass / pass | L:2-3; M:3-4 |
| `always-red` | pass / fail | L:4; M:5 |
| `absent-witness`, `overlong-witness`, `last-wins-wrong`, `uppercase-echo`, `stale-witness`, `wrong-witness` | fail / fail | L:5-10; M:6-11 |
| `green-mutant`, `green-absent`, `green-overlong`, `green-uppercase` | fail / fail | L:11-14; M:12-15 |
| `crash`, `zero-denominator`, `mismatch-detail` | fail / fail | L:15-17; M:16-18 |

The label receipt reports agreement for all sixteen labels; the declaration says they were re-derived from SELFTEST and M-Z/M-R evidence, not the contract row (L:1-18; D:45-48). The receipt itself contains the derived-label table, not the underlying raw harness transcripts (L:1-18).

G1 accepts sixteen **or more** hex characters, making an overlong echo a parsed mismatch rather than a prefix match. G2 rejection-samples `secrets.token_hex(8)` until at least one `a-f` letter occurs: uppercasing always changes the accepted challenge, unlike the predecessor's digits-only possibility (D:75-80; H:254-263; P:69-71). Deterministic here describes case change, not token generation (H:255-262).

## Measured result and limits

The recorded result is `cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET`, revision `cb713254ee9926e036e594312fdc61b57825526b` (M:23). This entry records that receipt; it does not rerun the counter.

- Only the outcome helper is mutated; the kill path remains correct by construction (D:82-85).
- Sixteen modes are rule separators, not fault coverage; the challenge authenticates the run's echo, not assertion truth (D:86-87).
- Provenance conflict retained: D:67-69 says “below fifteen”, whereas the final denominator and implementation are sixteen and `score < len(cases)` (D:71-73; C:393-394). The measured 15/16 mutants are reported killed (M:19-21); this entry does not silently repair the declaration.
