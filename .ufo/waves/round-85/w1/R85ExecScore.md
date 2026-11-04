# R85ExecScore — independent re-execution of round-85 measurements

Receipt: `.ufo/waves/round-85/receipts/independent-score-r85.txt` (verbatim contract lines, exit codes, input sha256).

## Results

| Measurement | Revision | Exit | Contract | Verdict |
|---|---|---|---|---|
| C1 identity causes | 3905311c (frozen rev) | 0 (twice) | `MADO_R85_IDENTITY: cases=72 correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61 tool_selftest=152/152 verdict=TARGET_MET` | TARGET_MET, equals declared target |
| C2 runbook status classes | 3905311c | 2 | `MADO_R85_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)` | setup refusal, retained as the frozen failure |
| C2 runbook status classes | d7c40e6d (successor, master) | 1 | `MADO_R85_RUNBOOK: cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 … mutants=37 killed=33 verdict=TARGET_MISSED rev=d7c40e6d… tree=bound` | TARGET_MISSED (33/37) |
| C2 replay, clean clone of d7c40e6d | d7c40e6d | 1 | identical contract line; identical four survivors | reproduced |

## C1 — met as declared
- 72/72 case lines `correct=yes`; 51/51 mutant lines `killed=yes`; base control 62/72; carried 61/61; stderr empty.
- Reproduced twice with identical output.

## C2 — not met at the successor
- All 36 rows execute and match (36/36, shapes 26/26, anchors 36/36, rows 36/36) and the tree binds.
- 33 of 37 declared mutants die. These four **survive**, each still matching 36/36 live rows:
  - `regex-anchor-dropped`
  - `line-anchor-prefix`
  - `negatives-skipped`
  - `samples-skipped`
- Interpretation: the kill rule only fires when a mutant exits nonzero or fails to match a live row. Mutants that disable the churn-sample or negative-sample checks, or that loosen the line anchor, do not change the live result, so the live rows cannot kill them. This is a real gap in the counter's kill predicate, not a counting error. I did not edit the counter.
- This matches the 33/37 prediction in L1's successor message. I report the measured result, not a pass.

## Frozen-rev C2 failure, retained
- At 3905311c the rev blob of SKILL.md still has the round-84 33-row section; the round-85 rows existed only uncommitted. The counter's tree-binding refused before executing any row (rc 2). Per the instruction, this failure is retained and not replaced.

## Revision handling
- REV for C1 = 3905311c. REV for C2 = d7c40e6d, the newer commit that already contains the 36-row section (descendant of 3905311c, verified by blob read). This exception was taken per the spec and is stated in the receipt.

## Drift and the clean clone
- After my successor run, the lane's `tools/mado-barfoot.py` changed (sha `62626fce…` vs the d7c blob `d2eb4547…`). The lane also has many unrelated dirty files and the rows marker was never written.
- To keep a drift-proof result I cloned the lane into scratch, checked out d7c40e6d (status clean), and re-ran C2 there with absolute lane control paths. The replay reproduced the successor result exactly.
- The lane was not written by me. No git mutating command was run in the lane; the clone was a read-only `git clone` from the lane into scratch.

## Not done / limits
- The rows poll was stopped once d7c40e6d carried the rows (verified by blob read, not by marker).
- C2 probes run against the live host; live outputs can drift between runs. The result is host-state-dependent, though all 36 rows matched.
- I did not verify C2 counter instrument identity at the frozen rev; the counter sha changed during the session (`e689438…` at 3905311c, `b4bde359…` at d7c40e6d). The successor run used the committed `b4bde359…`.
- No edits to any counter, tool, control, fixture or SKILL.md. No commit or push.

## Tooling
- No tools installed or updated. No pacman use.
