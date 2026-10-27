# C1 comment-only pointer falsification

## Finding: this attempted forgery is rejected, TARGET_MISSED

The specified change was applied in an isolated private git fixture: change the `tools/mado-hostguard.py` row's pointer to `quality/comment-pointer-target.md`, whose only mention of `mado-hostguard.py` is `<!-- mado-hostguard.py -->`. The fixture retained all rows and descriptions. The frozen counter reports `uncovered=1 dangling=1`, checker failure, and `verdict=TARGET_MISSED` (exit 1), not TARGET_MET.

Exact probe command:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py \
  --repo /fast/scratch/hyaku/mado-r51/CritC1CommentPointer/fixture \
  --rev 127c090022e461ecb31951f07df6c9af8b14ab6d \
  --work /fast/scratch/hyaku/mado-r51/CritC1CommentPointer/work
```

Observed final line (counter stdout):

```text
C1_R51: population=82 ledger_rows=82 uncovered=1 dangling=1 bad_pointer=0 empty_desc=0 selftest=ok checker=failed verdict=TARGET_MISSED rev=127c090022e461ecb31951f07df6c9af8b14ab6d
```

The target file was created only in the working fixture after archiving frozen revision `56026fcb9800370ae04bc65952a6567181c398d0`; it was not committed as a lane change. The exact reason is that the ledger pointer must name an existing repo file *at the tested revision*. Since the target file was untracked at frozen revision `56026...`, the counter's tracked-file listing does not include it. The checker independently flags the dangling row and absent hostguard row. The output is preserved at `/fast/scratch/hyaku/mado-r51/CritC1CommentPointer/output.txt`; fixture commit is `127c090022e461ecb31951f07df6c9af8b14ab6d`.

**Interpretation:** The literal predicate does not require pointer target content to be outside comments, so the comment-only basename would satisfy the basename-content subcondition if the target were an existing tracked repo file at `<rev>`. The particular requested fixture did not establish that prerequisite, and under the frozen checker/counter it is a concrete MISS. The prior ledger-wide forgery record (`.ufo/waves/round-51/w1/CritLedgerForgery/forgery-c1.md`, especially its comments on basename containment) identifies the broader residual. This attack does not falsify C1's current mechanical predicate; it confirms a residual, conditional on a tracked target file.

- **Axes:** operability is affected if a comment-only artifact is accepted as accountability; coverage is not undermined by this probe, because the mechanism retained row count but caused target-file existence/row coverage to fail.
- **Smallest safe correction:** no frozen-rule change. For a future amendment only, test comment stripping or require a meaningful tool-specific accountability location, while retaining the frozen controls. To reproduce a MET version, the comment-only target must be part of the tested revision and the row retained exactly once; do not reinterpret the observed MISS as MET.
