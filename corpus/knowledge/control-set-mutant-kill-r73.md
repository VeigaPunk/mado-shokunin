---
source: own-work — `.ufo/waves/round-73/{claims-declaration-r73.md,controls/c1-outcomes-r73.json,control-baseline-r73.txt,measurement-c1-r73.txt}` plus the round-72 mutation battery `.ufo/waves/round-72/w1/R72MutBattery.md`; held rows S441 (the exit-status vocabulary) and S444 (the result object's pass/fail read) stand behind the outcome rule itself
verified-at: `1459cca11fb5d3956a6e9a128217852dd0c28cb9` (round-73 instruments; measurement in `.ufo/waves/round-73/measurement-c1-r73.txt`)
recheck: `python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev <rev> --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json --scratch-root DIR` — `killed=4 base_killed=2 verdict=TARGET_MET`
---

# A control set is an instrument: the outcome set's discriminating power (round 73, C1)

## 1. The gap this round closes

The lane's landing instrument decides a contract outcome from the subject's own summary. Round
72 froze an eight-case set to protect that rule and declared, in its own erratum, two shapes it
did not cover: the successor's `n > 0` guard (no zero-denominator case) and the repaired
last-parsed-summary scan (the F1 repair was covered by the harness selftest only, not by the
frozen cases). The round-72 mutation battery proved the consequence — a rule with the `n > 0`
guard deleted scored `8/8` on the frozen set and printed `TARGET_MET`.

The lesson is not "add a case". It is that **a frozen control set has its own measurable
property: how many named mutations of the rule it certifies it can separate.** Round 72 measured
the rule and left the set unmeasured; round 73 measures the set.

## 2. The measurement

| quantity | command | round-72 set | round-73 set |
|---|---|---|---|
| cases | `jq '.cases\|length' <file>` | 8 | 10 |
| named mutations separating | `python3 -I quality/counters/c1-r73-summary-mutants.py …` | 2/4 (`base_killed=2`) | 4/4 (`killed=4`) |

The ten-case set is the round-72 eight carried byte-identically (the counter hash-checks
`.ufo/waves/round-72/controls/c2-controls-r72.json`, sha256 `640fb44f…`, and compares every
carried case field by field) plus two cases:

| new case | gate output | expected | what it exists for |
|---|---|---|---|
| `zero-denominator` | `MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed` | `TARGET_MISSED` | a run that asserted nothing is not green; a rule without the `n > 0` guard greens it |
| `valid-then-garbled` | a green `12/12` summary followed by `MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete` | `TARGET_MET` | a malformed trailing marker is not a summary and must not suppress the last parsed one; the pre-repair prefix-match scan returns the marker and reds it |

## 3. The four named mutations

Each is a literal substitution of the committed round-72 rule
(`quality/counters/c1-r72-landing-controls.py`, sha256 `b6108c86…` at the measurement), applied
exactly once and asserted to be the only delta.

| id | delta | rule broken | separated by |
|---|---|---|---|
| N1 | `return total > 0 and passed == total` → `return passed == total` | the zero-denominator guard (r72 battery GAP-1) | `zero-denominator` |
| N2 | `last_parsed_summary` → the pre-repair last-prefix-match scan | "the last **parsed** summary" (r72 erratum §1) | `valid-then-garbled` |
| N3 | `passed == total` → `passed <= total` | equality on a green summary (the M2 family) | `failing-summary-exit0`, `failing-summary-exit2` |
| N4 | `outcome_verdict` → the kill count alone | the summary gate itself (r72 battery M4) | six cases, both directions |

N1 and N2 are the important rows: each is separated by exactly one of the two new cases, and by
nothing in the eight-case set. That is the property the round buys — the two disclosed blind
spots are now load-bearing cases, and a future edit that re-opens either one cannot pass the set.

## 4. Why the held leg is the right do-nothing control

The counter's `base_killed` leg scores the same four mutations on the held eight-case set in the
same run. It is the cheapest control that skips the round's work: keep the round-72 denominator,
change nothing else, and the set separates 2/4. It therefore **cannot** reach the target
(`base_killed == 2` is a frozen required value, not an observation), and a counter whose base leg
reached 4 would be proof the target was mis-specified.

## 5. Bounds

- Four named mutations of one rule family are not fault coverage. A rule that is wrong in a way
  none of N1–N4 encodes passes the set.
- The mutations are syntactic substitutions of the committed source, not arbitrary program
  mutations; a mutation that changes behaviour only outside these ten cases is not counted.
- The counter scores the committed decision functions in-process; it does not execute a harness
  run, and it says nothing about the fixture lane.
- The set protects the outcome rule only; the kill-credit rule (`credit()`) keeps its own eight
  fixture modes and its own counter (`c1-r72-summary-credit.py`), untouched this round.

## 6. Reuse

A lane adding or editing a decision rule should, in the same round:

1. freeze the case set **before** the rule exists (as round 72 did), and
2. measure the set's discriminating power by mutating the rule it certifies (as this round does),
   with the held denominator as the do-nothing leg.

A set whose mutant-kill fraction is below its mutation count is a set with a named blind spot, and
the blind spot belongs in the declaration, not in a footnote.
