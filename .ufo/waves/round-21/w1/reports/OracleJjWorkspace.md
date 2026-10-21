# JjWorkspace oracle — C1 VCS write boundary

**Decision:** `jj --ignore-working-copy workspace add new-workspace` expects `vcs_write` (`evidence: observed`).

**Grounding:** committed `.ufo/waves/round-20/a2/review/ReviewVcsV3.md:14-20` records a measured `jj -R ws --ignore-working-copy workspace add workspace-added`: it exited 1 because workspace-add required working-copy access, yet created the destination and registered `workspace-added`. This is a workspace-state mutation, so it is a write even without a ref change; the failure does not erase the observed side effect. The oracle command has the same workspace-add operation and `--ignore-working-copy` option, with only the repository selector and destination name differing.

The requested JSON is at `.ufo/waves/round-21/w1/oracles/JjWorkspace.json`. No VCS command, transcript, classifier, or tool behavior was executed or queried; classification is grounded in the committed ReviewVcsV3 measurement only. No tool installations.
