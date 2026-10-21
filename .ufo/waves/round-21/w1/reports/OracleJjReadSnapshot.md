# OracleJjReadSnapshot

## C1 — operability / VCS write boundary

**Expectation:** retain the proposed positive `vcs_write` class for the inert shell shape `jj log`, with the condition that the working-copy tree has changed in a writable workspace. A clean working copy can make snapshotting a no-op; the oracle records the command's write-capable semantics rather than claiming every invocation mutates state.

**Grounding:** the tagged `v0.45.1` `log.rs` implementation calls `command.workspace_helper(ui)` at line 139. In `cli_util.rs`, `workspace_helper` is documented as loading and snapshotting the working copy if allowed, and calls `workspace_helper_with_stats` (lines 461–500). The tagged `snapshot_working_copy` implementation compares the observed working-copy tree with the stored commit; when they differ it writes a rewritten/new commit, sets the workspace's working-copy commit, and commits the `snapshot working copy` transaction (lines 2088–2225). The tagged working-copy documentation says most `jj` commands commit changed working-copy contents (lines 9–12). This establishes repository-object/operation/workspace writes, not only ref changes. Round-20 `ReviewVcsV3.md` records the measured host version as jj 0.45.1 (lines 43–45), which aligns the public-source tag used here.

**Limits:** no `jj` command, fixture transcript, scanner/classifier, or runtime was executed or consulted. The expectation is sourced from the tagged implementation and is conditional on a changed working copy and writable snapshot path. No tool was installed or updated.

Report: .ufo/waves/round-21/w1/reports/OracleJjReadSnapshot.md
