# RevQuality30 — partly falsified: 30′ is a defensible swap but its committed green is premature — the corpus-diff leg is pending and, if it fails, C2 is 21/30 = 7.0000, a regression the scorecard's two-outcome framing omits

Attacked: QUALITY 30′ (`corpus/QUALITY.md:249-259`), the pre-measurement correction
that withdrew registered criterion 30 and swapped in 30′ (`SCORECARD.md:1285-1316`),
and the C2 honest-reading fallback 21/29 (`SCORECARD.md:1308,1331`). All commands run
in `/tmp/mado-r20w2-RevQuality30` (clone of lane tip `a4046a8`, origin removed); lane
checkout touched read-only.

## Finding 1 (primary): 30′'s green is asserted before its own admission bar is met

Criterion text (`corpus/QUALITY.md:249`) makes admission of the detector change
conditional on *three* legs: committed negatives read at both tools, **"a
whole-corpus diff against the pre-change tool that lists every added and relabelled
row"**, and the `evidence: lead` marker. At `a4046a8` the corpus-diff leg does not
exist:

- `SCORECARD.md:1330` (own row): "whole-corpus diff vs `9c54c56`: **pending (wave 2)**".
- No diff receipt in `.ufo/waves/round-20/evidence/` (only `precision-*`,
  `recall-*`, `crit29-*`, `isolation-check-run.txt`).
- `.ufo/waves/round-20/corpus-diff.py` is committed (`f3da504`) but was never run
  against the corpus before the green claim was written.

Yet `corpus/QUALITY.md:254-255` declares "Green at `28c6837` …: P 66/66, L 17/18" and
`SCORECARD.md:1331` reads the C2 cell as green on 30′. The counterexample is
concrete: the criterion's own runnable check — `tw-precision.py REV` read for
families P and L — **cannot express the corpus-diff leg at all** (the criterion says
so itself, :257-259: "the corpus diff is the out-of-suite evidence"). So a green
runnable check does not mean the criterion is satisfied; the criterion text asserts
green anyway. If the wave-2 whole-corpus diff finds one unexplained added or
relabelled row, 30′ flips red while staying numbered: semantic C2 becomes
21/30 = 7.0000, **below** the 20/28 = 7.1429 baseline — C2 a regression, not
"improved". `SCORECARD.md:1331` frames only two outcomes ("22/30 as registered … if
the closure rules 30′ a swap, 21/29"); the third outcome — swap accepted, 30′ red —
is not named anywhere.

Evidence (reproduced in clone):

```
python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995 → P 7/66, S 2/17, W 4/22, H 15/52, L 1/18   (red, matches receipt precision-1f7f995.txt)
python3 -I .ufo/waves/round-20/tw-precision.py 28c6837 → P 66/66, S 17/17, W 21/22, H 51/52, L 17/18 (green legs only)
```

Smallest safe correction: relabel 30′ "pending the corpus-diff leg" in
`QUALITY.md:255` and `SCORECARD.md:1331` (the lesson line at
`corpus/lessons/round-20.md` M1 row already hedges only the tally side), and add the
third outcome ("swap accepted but red → 21/30 = 7.0000") beside the two registered
readings.

## Finding 2: 30′'s red and green are the C1 counter's own numbers — independence is nil, and the only independent leg is the pending one

- Red: the criterion's named red artifact (`QUALITY.md:252-254`) is the closure's
  `BLOCK=frozenset([...])` case — which is literally C1 counter case
  `P-CasePureBuiltins-frozenset-closure`, first row of receipt
  `evidence/precision-1f7f995.txt` (`got exit=1, package_query, evidence:observed`,
  want `exit:0`). Reproduced above.
- Green: P/L families of the same `tw-precision.py` run that scores C1.
- Lead marker: same counter, family L (17/18; the one failure `L-…-b14` is a
  no-row, not a missing marker — disclosed at `SCORECARD.md:1329`).

So every landed leg of 30′ is a re-read of C1's measurement; the sole leg that
could make 30′ independently evidenced is the corpus diff — pending (Finding 1).
The authors disclose "not independent of C1" (`SCORECARD.md:1307,1331`,
`QUALITY.md:255-256`), so this is honestly labeled, but substantively 30′'s
numerator point double-counts C1's repair evidence. For a *calibration* axis that
is exactly the inflation shape R19-V1 was written against; whether the swap is
"target-preserving" therefore hinges on a leg that does not yet exist.

## Finding 3: the swap is number-preserving, not substance-preserving — defensible but narrower than claimed

- R19-V1 requires: no duplicate criterion, no retroactive target redefinition, and
  for any next calibration claim "a fresh pre-registration and grounded failure
  evidence" (`corpus/lessons/round-19-verifier-spotcheck.md:149`).
- Withdrawal is well-grounded: two independent wave-1 reports
  (`w1/reports/RevCriterion30.md`, `w1/reports/CriticC2Inflation.md`) showed
  registered-30's core restates criterion 10 (`QUALITY.md:16`); the pre-registration
  screened only 24/27/28 (`SCORECARD.md:1272-1273`). The criterion-10 application is
  append-only with no new number — the R18-V2-under-24 precedent (`QUALITY.md:262`).
- 30′ is not itself a duplicate: I read all 28 criterion texts; the nearest is 25
  (instrument tightening must reject committed mutants — a *recall/teeth*
  direction) versus 30′'s precision side (negatives, relabelled rows, lead markers).
  Distinct norm; the claim "no criterion 1–28 covers detector precision"
  (`SCORECARD.md:1305`) holds.
- Timing holds: the correction landed `f3da504` (17:09) before the tool repair
  `28c6837` (17:29) and before the measured receipts (20:29Z); "registered before
  any after-measurement" is accurate.
- But "target-preserving" is literally true only because the registered target was
  authored as a *count* ("two lesson-cited criteria", `SCORECARD.md:1265`), not by
  member identity. The target 22/30 survives the substitution of an unrelated norm
  for a void one — a number-preserving swap. CriticC2Inflation's wave-1 warning
  ("`22/30` is authored, not measured; score-by-construction") is answered in form
  (non-duplicate member, disclosed fallback) but not fully in substance (the
  substituting member is C1-dependent and not yet fully evidenced).

## Finding 4: 21/29 verified mechanically — the honest fallback reading is exact

`measure.py` c1 counts `^[0-9]+\.` lines and the subset containing `lessons/`.
Reproduced: `1f7f995` → 20/28 = 7.1429; `a4046a8` → 22/30 = 7.3333. Removing the
numbered `30.` line from `a4046a8`'s QUALITY (runnable-check lines are indented,
never numbered) gives 21 cited / 29 criteria = 7.2414 — exactly the disclosed
fallback. The withdrawn registered-30 never landed as a numbered line, so the
denominator at baseline was correctly 28, and "21/29" is not a retroactive
redefinition but the corrected registration. Literal-vs-semantic is reported
separately, satisfying criterion 22.

## Finding 5: criterion-10 application (tally-check) is sound; the advisers' false-red risk on S096 is answered

Ran both sets in the clone:

```
python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set red --expect   → 5/5 MISMATCH, exit 0
python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set green --rev a4046a8… → 4/4 MATCH, exit 0
```

The S096 entries re-derive under the claim's own stated rule ("name S096 **on the
crediting line**" → `first_line`) at the statement's own revision `1f7f995`,
yielding 6/13 — not the advisers' feared cross-rule `b435568` comparison. The
correction sentences name the original rule and revision explicitly
(`corpus/lessons/round-20.md:65`: "The '5/13' was RerunC2's cited-as-evidence
reading at `01b8094`, not a token count"). Residual nit: the registry flags a claim
that was *true at its own revision* as red; the entries' notes do record this
(staleness, not falsehood), so the MISMATCH is a staleness flag — accurate enough
for criterion 10 but worth a judge's eye.

## Confirmed, not falsified

- Precision counter before/after reproduced exactly (29/175 → 172/175 with the
  same three named failures: `W-CaseWrapperForms-class-method-instance`,
  `H-…-jj-var-verb-help`, `L-…-b14`).
- Held-out set: 0/12 pass at both `1f7f995` and `28c6837` — consistent with the
  disclosed "EDGE, red at 9c54c56 too" expectations (`precision-heldout/expected.json`);
  it demonstrates no regression but also provides no generalization evidence —
  the "same round, blind authors, one contract" limit (`QUALITY.md:257`) is real.
- Tool sha256 `9613f510…` confirmed unchanged at `a4046a8`.

## Limits

- Did not run `corpus-diff.py` — that is CorpusDiffV2/CorpusDiffIndependent's
  assigned item; Finding 1 asserts only that the green was committed before the
  leg exists.
- Did not re-verify the held-out "before: fail at 9c54c56" author annotations
  beyond reading `expected.json`; consistent with receipts.
- [INFERENCE] The 21/30-if-30′-red scenario assumes the closure reads numerator by
  satisfaction rather than by landed numbered lines (criterion-22 semantic
  reading); the literal `measure.py` output stays 22/30 regardless.
- Verified restatement of 30′ against criteria 1–28 by direct read of all
  criterion texts, not by a formal duplicate screen.

## Installs

none
