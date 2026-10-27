# RevC1CounterRev — C1 reviewer attack

Axes: **coverage + operability**.

## Deliverables
- `.ufo/waves/round-51/w2/RevC1CounterRev/c1-counter-replay.md` — exact commands/output, receipt comparison, selftest, selected-revision assessment.

## Findings
- **PASS — PRED-C1-r51 replay.** Freeze revision `56026fcb9800370ae04bc65952a6567181c398d0` returned exact final line with population/ledger_rows 82, all required zero counts, `selftest=ok`, and `TARGET_MET`; exit 0. The checker reported selftest 50/50 and ledger revision equal to freeze. Base `6ca8c559a4a3d6d361101592116eea2bc7452437` returned `TARGET_MISSED ledger=absent population=79`; exit 1. Both match the frozen claim/registration and cited base receipt.
- **PASS — worktree/revision disagreement.** Although invoked via the later current worktree, counter logic assesses a revision-specific clone and reads tracked inputs through `git ls-tree`/`git show` at the resolved revision. It reports the exact revision and assessed 82/79 populations. No actionable discrepancy found.

## Residual risk and verification gaps
Registration explicitly preserves C1 literal-pass limitations: comment-only pointer evidence and repeated generic descriptions. This replay does not re-test those known limits. No tracked lane code was edited.
