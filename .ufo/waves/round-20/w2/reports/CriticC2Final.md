# CriticC2Final — partly falsified: 22/30 is literal-real but conditional; R19-V1-conservative reading is 21/29 target-missed, and criterion 30′ is admitted while its own third leg is unlanded

Attacked claim: `SCORECARD.md:1331` — C2 `python3 .ufo/waves/round-17/measure.py REV` key `c1`, 20/28 → 22/30, "improved as registered after the pre-measurement correction; if the closure rules 30′ a swap, the reading is 21/29". Question put to me: is 20/28 → 22/30 discernment or count inflation after the pre-measurement swap, and what would a non-author closure write?

## Reproduced measurements (all in `/tmp/mado-r20w2-CriticC2Final` clone)

| Command | Output |
|---|---|
| `python3 .ufo/waves/round-17/measure.py 1f7f995` (also `e629f73`, `f3da504`, `28c6837`) | `{"criteria": 28, "lesson_cited": 20, "score": 7.1429}` |
| `python3 .ufo/waves/round-17/measure.py 4362219` (also `a4046a8`) | `{"criteria": 30, "lesson_cited": 22, "score": 7.3333}` |
| `python3 .ufo/waves/round-17/measure.py 9c54c56` | `{"criteria": 26, "lesson_cited": 18, "score": 6.9231}` |
| `bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh` | `FAIL_CLOSED` all six modes + `POSITIVE_CONTROL_OK`, exit 0 |
| `bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/evidence/inns-r19-shape.sh` | `COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)`, exit 2 |
| `python3 -I .ufo/waves/round-20/tally-check.py --set red --rev a4046a8216080d4004de3f268c62cf142095ac07 tally-claims.json` | `TALLY_SUMMARY: set=red n=5 match=0 mismatch=5 error=0`, `EXPECT_SUMMARY: 5/5`, exit 1 |
| `... --set green --rev a4046a8...` | `set=green n=4 match=4 mismatch=0 error=0`, `EXPECT_SUMMARY: 4/4`, exit 0 |
| `python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995` | `score 1.6571`, families `P 7/66, S 2/17, W 4/22, H 15/52, L 1/18` |
| `python3 -I .ufo/waves/round-20/tw-precision.py a4046a8` | `score 9.8286`, `P 66/66, S 17/17, W 21/22, H 51/52, L 17/18`; three named fails as claimed |

The count itself is not regex-gamed at tip: exactly 30 `^[0-9]+\. ` lines exist (`corpus/QUALITY.md`), criteria 29 and 30 each carry `lessons/` on their own numbered lines (`QUALITY.md:232`, `:249`), and both anchors resolve to real rows at tip — M1 = "precision-for-recall trade" (`corpus/lessons/round-20.md:15` → 30′), M2 = "fail-open isolation" (`round-20.md:16` → 29). The wave-1 wrong-anchor warning (CriticC2Inflation §3) was repaired: draft M2/M3 misassignment did not land. Commit order confirms the correction was genuinely *pre*-measurement: `e629f73` pre-reg (20/28) → `f3da504` append-only correction (still 20/28) → `28c6837` tool (still 20/28) → `4362219` QUALITY 29/30′ (22/30). Receipt `evidence/measure-before.txt` pins before=`1f7f995` 20/28.

## Finding 1 — the swap is disclosed but it is still score-preserving substitution, and the honest floor is 21/29

Counterexample for "discernment, full stop": the pre-registered target `22/30` is goal-seeked by construction (measure.py:92-93 is a line regex; ScribeQuality's own placement note documents score-by-construction — `.ufo/waves/round-20/w1/reports/CriticC2Inflation.md:37-41`, independently confirmed). Wave-1 advisers showed registered-30 restated criterion 10 (`QUALITY.md:16`; RevCriterion30, CriticC2Inflation, ConnCriteriaFleet all concur). The correction withdrew it and substituted 30′ — a *different* norm — while keeping the numeric target. R19-V1 (`corpus/lessons/round-19-verifier-spotcheck.md:149`) demands "Do not add a duplicate criterion or retroactively redefine the target." Withdrawing the duplicate satisfies the first half; keeping `22/30` while replacing the content that produces the numerator is a defensible but not innocent reading of the second half — the author concedes this by flagging 30′ "a possible target-preserving swap" (`SCORECARD.md:1300`) and registering the 21/29 = 7.2414 fallback.

My own duplication screen of 30′ against criteria 1–28 (direct read of `corpus/QUALITY.md` at `a4046a8`): the nearest hit is criterion **25** (`QUALITY.md:138`) — an instrument change credited for *tightening* needs a committed mutant receipt; 30′ asks a change credited for *recall* to carry precision negatives + corpus diff + lead markers. Same domain (detector evidence), opposite direction, different evidence class; distinctness is arguable either way and was never independently screened — the pre-measurement correction screens nothing, it registers. 30′ is also a specialization of criterion 2's "every claim carries a source," but precedent (23 specializing 9, stated in-corpus at `QUALITY.md:118-119`) tolerates that shape.

**Impacted axes:** calibration honesty (down — numerator preserved by substitution); non-duplication (contested — 30′≈25 dual); process integrity (up — disclosed, append-only, fallback pre-registered).

## Finding 2 — criterion 30′ is credited while its own third admission leg is unlanded (premature saturation)

The strongest counterexample. `QUALITY.md:249` admits a recall-credited detector change *only beside* three evidence legs: (a) committed negatives read at both tools, (b) "a whole-corpus diff against the pre-change tool that lists every added and relabelled row," (c) the `evidence: lead` marker. Legs (a) and (c) exist (`tw-precision.py` red/green above; marker verified in emitted rows). Leg (b) is explicitly **pending**: `SCORECARD.md:1330` — "whole-corpus diff vs `9c54c56`: pending (wave 2)". The C2 row (`:1331`) reports 30′'s green — "red P 7/66, L 1/18 → green 66/66, 17/18" — with no condition on that pending leg. Under the criterion's own text, the change it retroactively gates is *not yet admitted*: if `corpus-diff.py` (`.ufo/waves/round-20/corpus-diff.py`, `--base 9c54c56 --new <tip>`) lands with any unclassed added row or a lost finding, the 30′ green inverts and the honest C2 reading drops to 21/29 retroactively. A green entered before the criterion's own admission clause is satisfied is the premature-saturation defect this seat exists to flag.

Sub-point: the L family is 17/18, not 18/18 — `L-AdoptW2-AdvHelperFn-b14` wants a `lead` row for a parameter callee inside a never-called def; the tool emits nothing. Leg (c) of 30′ is therefore satisfied at 17/18 by the author's own counter, a residual the SCORECARD names but the "admitted" framing does not carry.

## Finding 3 — corroborated defect: criterion 29's red is not runnable at tip without a mode fix

`git ls-tree a4046a8 .ufo/waves/round-20/evidence/inns-r19-shape.sh` → `100644` (flipped from `100755` in `4362219`, same commit that landed the receipts). `isolation-check.sh:11-13` requires `-x`, so the criterion's documented runnable check at tip returns `COULD_NOT_EVALUATE … (not executable)`, exit 2 — not `FAIL_OPEN`, exit 1. Already reported as P2 by sibling `w2/reports/RerunIsolation.md` and worked around by `MutIsolationCheck.md`; corroborated here byte-identical (`harness_sha256=8bd507f0…` matches the receipt). The receipt is revision-bound to `28c6837` where the mode was 755, so the *claim's* evidence is sound; the *criterion's* "runnable check" promise is impaired at tip. Smallest safe correction: keep 0644 (the fixture really calls `unshare`/`mount` — execute bit off is defensible) and amend the criterion-29 runnable-check line or the checker's harness handling to state "copy to /tmp, chmod +x" — or restore +x with a header noting the fixture is checked, not run by hand. Fixable; not grounds to reject 29.

## What a non-author closure should write (R19-V1 shape)

Suggested verdict text:

> **R20-Vx (C2).** Literal `measure.py` reading reproduced: 20/28 = 7.1429 → 22/30 = 7.3333 — *improved*. The pre-registered target "22/30" is **met only under a qualified reading**: criterion 29 stands (new norm, real red, green 6/6); criterion 30′ is the flagged target-preserving replacement of a withdrawn duplicate. This closure rules 30′ **distinct-but-incomplete**: not a restatement of 6/10 (different obligation) and arguably not of 25 (opposite direction, different evidence class), but its green is not independent of C1 — the author's own note — and its admission is conditional on its own whole-corpus-diff leg, recorded pending. Record C2 as **21/29 = 7.2414 achieved unconditionally; 22/30 = 7.3333 achievable only if (a) the corpus-diff receipt lands classed-complete and (b) this closure's distinctness ruling on 30′ stands**. Round 19's ≥21/29 miss stays a miss; this round's floor is the same number the target was built to avoid, reached honestly rather than by restatement. Do not stamp "target met" while the diff leg is pending.

That wording preserves the real improvement, honors R19-V1's no-redefinition rule by holding both readings, and makes the residual conditions explicit instead of laundering them into a met target.

## Limits

- Did not run `corpus-diff.py` (assigned to CorpusDiffV2/CorpusDiffIndependent, still running); finding 2 stands on the claim's own "pending" marker.
- The 30′-vs-25 distinctness call is a direct-read judgment, not an exhaustively screened one — other criteria pairs were checked by reading, not a mechanical rubric.
- `tw-precision.py` runs used the tip counter on revisions `1f7f995`/`a4046a8`; case-level rows only spot-checked (the closure frozenset case `P-CasePureBuiltins-frozenset-closure` does emit an ordinary `package_query`/`observed` row at `1f7f995` — red confirmed).
- The inns fixture's 644 mode may be intentional hazard-reduction [INFERENCE]; the defect is the undocumented check regression, not the mode choice itself.
- Green `isolate.sh` run was in my /tmp clone with /tmp canary payloads only; no host probe, no sudo, no pacman, no live gate.

## Installs

none
