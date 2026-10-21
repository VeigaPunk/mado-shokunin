# GitCommitZn oracle review

## C1 — operability residual repair

Recommendation: retain the proposed `write` expectation for the exact Bash command `git commit -zn`. The committed round-20 `ReviewVcsV3` records an observed run in a fresh Git 2.56.0 repository with a staged tracked-file modification: command exit 0, HEAD unchanged, `.git/index` changed, and an unreferenced tree object created. The index and object-database writes satisfy the registered write boundary; an updated ref is not required. The artifact cites `.ufo/waves/round-20/a2/review/ReviewVcsV3.md:22-29,59`.

The oracle's `evidence: "observed"` is supported by this committed evidence, not by an execution in this assignment. No VCS command, classifier, installer, or transcript was executed; no tools were installed or updated. This is an advisory oracle contribution, not an admission judgment.

## C2 — calibration

Not evaluated by this scoped C1 oracle assignment.
