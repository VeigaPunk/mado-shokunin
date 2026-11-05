# round-86 instrument repairs — pre-verdict, disclosed

The round-86 counters were authored by the attempt-1 L1, which died on a provider failure before any
measurement. Attempt 1's bytes were preserved at `f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7`. This file
records every repair attempt 2 made to them, in order, with the receipt each run produced. No repair
changes the declaration's target sentence, its numbers or its kill rule: each corrects the counter so
that it measures the sentence it prints, and the run at the committed bytes produced **no verdict**.

## C2 — four runs: one setup error, one self-contradiction, one dead mutation path

| run | instrument bytes | result | receipt |
|---|---|---|---|
| 1 | as committed at `f72bba01` | `ERROR (stage=setup mutant regex-anchor-dropped anchor occurs 0 times, not once)` — exit 2, **never a verdict** | this file, transcript below |
| 2 | repair 1 | `matched=34/37 clauses_observed=34/37 mutants=37 killed=37 verdict=TARGET_MISSED` | `receipts/c2-anchor-only-r86.txt` |
| 3 | repairs 1–2 | `matched=37/37 clauses_observed=37/37 mutants=37 killed=35 verdict=TARGET_MISSED` | `receipts/c2-live-observation-r86.txt` |
| 4 | repairs 1–3 | `matched=37/37 shapes=27/27 anchors=37/37 clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET` | `receipts/c2-repaired-r86.txt` |

### Repair 1 — stale mutation anchor (run 1 → run 2)

`MUTATIONS` entry `regex-anchor-dropped` still carried the pre-observation anchor
`if anchor == "line":\n    return line_anchored(value, text)`. The round-86 observation line had been
inserted inside that branch, so the anchor matched nothing and the whole run exited 2. Repaired by
anchoring on the branch body that now exists (`OBS["anchors"] += 1` plus the return) and replacing the
rule with `re.search`, so the mutant drops the anchor rule while keeping the observation.

### Repair 2 — the anchor-observation conjunct contradicted the printed target (run 2 → run 3)

`case_correct` required `OBS["anchors"] == 1 + len(samples) + len(negatives)`, while the counter's own
`declared` tuple and the declaration's sentence say the declared anchor population is **1** (one
judgement of the row's live output). A negative refused by the producer-status gate never reaches the
anchor branch, so the two clauses disagreed and the three anchored cases (`version`,
`omarchy-version`, `border-size-int`) could never pass. Repaired by snapshotting the live call's
anchor count (`LIVE["anchors"]`) and comparing the declared population against that snapshot; the full
`OBS` counters are retained unchanged (the selftest still asserts `anchors: 3` over a live call plus
one sample and one negative).

### Repair 3 — two mutations pointed at a function on no scoring path (run 3 → run 4)

`samples-skipped` and `negatives-skipped` anchored on `for sample in case.get("samples", []):`, which
after the `case_correct` refactor exists only in `held_case_correct` (the control). Both mutants
therefore changed the held rule, stayed at 37/37 and survived. Repaired by anchoring on the scoring
loops in `case_correct` (`for sample in samples:` / `for sample in negatives:`).

Every repair is proven able to fail: each run above is a receipt, and run 2 / run 3 are the failing
states of the repairs that follow them.

## C1 — no repair

`c1-r86-refusal-records.py` ran first time at the committed bytes and reports `verdict=TARGET_MET`
with `flooding=48/75`, `held_flooding=75/75` and `carried=72/72` (`receipts/c1-r86.txt`). Its
`base_correct=75/75` is the declaration's third control: the round-85 tool scores full marks under the
new rule, so the increment is the rule, not the tool.

## Run-1 transcript (verbatim tail of the committed instrument)

```text
MADO_R86_MUTANT: name=signal-as-exit matched=33/37 killed=yes
MADO_R86_RUNBOOK: ERROR (stage=setup mutant regex-anchor-dropped anchor occurs 0 times, not once)
```

rc 2. Exit 2 is the instruments' setup class: it is never a verdict, so nothing in this round treats it
as a score.
