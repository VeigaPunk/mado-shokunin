# ReviewC2Predicate — attack report on `.ufo/waves/round-33/c2/count.py`

Date: 2026-10-24. Lane: mado-shokunin, round 33, w1. Scope: read-only attack of the
PRED-C2-r33-v1 counter via scratch scorecards under
`.ufo/waves/round-33/scratch/ReviewC2Predicate/`. `SCORECARD.md` untouched
(`git status --porcelain -- SCORECARD.md` → empty).

## Axes attacked

- **A — claim parsing**: mandated cited/verdict/absence cases; anchoring; charset.
- **B — frozen-rev measurement**: wrong rev where measurement coincides, so only the
  `rev == FROZEN_REV` literal check can reject.
- **C — precedence**: which of several matching lines decides (doc says "last").
- **D — normalization/boundaries**: leading-zero N, uppercase verdict, hash length/case.

Ground truth measured first: `measured=7` on frozen rev `d9ed3816…` (probe card), and
`measured=7` on HEAD `9a46ccf3…` — identical, which makes case 2 below the strongest
possible rev test.

## Mandated cases — all hold

```
=== case1-cited7-targetmet.card   (cited_entries=7, verdict=target-met, rev=frozen)
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=7 measured=7 verdict_word=target-met rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MISSED
exit=1
=== case2-wrongrev.card           (cited_entries=7, verdict=honest-stop, rev=HEAD 9a46ccf3…)
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=7 measured=7 verdict_word=honest-stop rev=9a46ccf3282117f960b8d53cd71599a91f388ee3 verdict=TARGET_MISSED
exit=1
=== case3-absent.card             (no claim line; prose + prefixed decoy line)
PRED-C2-r33-v1 claim_mismatch=1 reason=absent verdict=TARGET_MISSED
exit=1
```

Case 2 is decisive: published == measured == 7 and verdict is right, so **only** the
`rev == d9ed3816…` identity check rejects it. It holds.

## Control — the counter can pass (harness validity)

```
=== control-pass.card   (cited_entries=7, honest-stop, frozen rev)
PRED-C2-r33-v1 claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET
exit=0
```

## Additional attacks — all behave

```
=== case-anchor-lead.card   (leading space)        → claim_mismatch=1 reason=absent verdict=TARGET_MISSED exit=1
=== case-anchor-trail.card  (trailing space)       → claim_mismatch=1 reason=absent verdict=TARGET_MISSED exit=1
=== case-upperrev.card      (uppercase 40-hex)     → claim_mismatch=1 reason=absent verdict=TARGET_MISSED exit=1
=== case-badhash.card       (39-hex)               → claim_mismatch=1 reason=absent verdict=TARGET_MISSED exit=1
=== case-verdict-upper.card (verdict=HONEST-STOP)
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=7 measured=7 verdict_word=HONEST-STOP rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MISSED
exit=1
=== case-lastline-mismatch.card (match first, mismatch last)
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=8 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MISSED
exit=1
=== case-lastline-match.card    (mismatch first, match last)
PRED-C2-r33-v1 claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET
exit=0
```

Last-line-wins confirmed in both directions; anchoring (`^…$` via `match` on
`splitlines()`) rejects padded lines; verdict comparison is case-sensitive; regex
rejects non-lowercase and wrong-length hashes without invoking git (no archive call,
no option injection — `rev` reaching `git archive` is always 40 lowercase hex).

## Observations (contract-defensible, recorded for the digest)

1. **Leading-zero normalization**: `cited_entries=07` with honest-stop/frozen →
   `claim_mismatch=0 … verdict=TARGET_MET exit=0`. `int()` treats `07` as 7. The
   predicate says "N equal to", which an integer reading satisfies; no fix demanded.
2. **Fake-rev path is a hard error, not a miss**: well-formed but nonexistent
   `rev=0000…0000` → `PRED-C2-r33-v1 error=archive-failed`, exit 2. Consumers must
   treat any exit != 0 as not TARGET_MET; a raw "exit 1 = miss" reading is wrong for
   this tool.
3. **Measurement cannot currently distinguish revs**: `measured=7` on both the frozen
   rev and HEAD. The rev-identity literal is the only discriminator today. Correct
   behavior now; becomes load-bearing if corpus citation counts drift between revs.

## Verdict

PRED-C2-r33-v1 survives all three mandated attacks plus 10 additional probes with no
false PASS. Weak points are cosmetic (zero-padded N) or consumer-side (exit-2 on fake
revs). No changes proposed to `count.py`; `SCORECARD.md` not modified.
