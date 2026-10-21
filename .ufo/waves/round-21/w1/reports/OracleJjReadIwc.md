# JjReadIwc — C1 VCS/runner oracle

## Finding

**Proposed `clean` expectation is too broad; recommend `vcs_write` for `jj --ignore-working-copy log`.** The finding is conditional on repository state; this is not a claim that every invocation writes.

In jj v0.45.1 (`7c41cdeb16b6b321c64e789a966b6adf723816a5`), `cmd_log` calls `workspace_helper`. `--ignore-working-copy` prevents the ordinary working-copy snapshot path: `workspace_helper_with_stats` returns before `snapshot_impl` when the working copy is not writable. It does not make repository loading a no-write operation. `load_from_workspace` resolves and loads the operation, and `RepoLoader::finish_load` calls `index_store.get_index_at_op`.

The tagged `DefaultIndexStore::get_index_at_op` rebuilds when the operation index association is missing, and reinitializes/rebuilds when the index is corrupt or not found. `build_index_at_operation` saves the resulting index; `save_mutable_index` writes commit and changed-path index segments and associates them with the operation. These are repository index writes, explicitly within this assignment's write boundary. Thus a command shape without a guarantee that the repository index is present and valid cannot be treated as universally clean.

There is a second conditional write path: default operation resolution handles multiple operation heads by invoking `merge_operations`; `Transaction::write` writes the operation and index. This too is independent of working-copy snapshotting. A normal repository with one operation head and a valid index may take neither path.

## Evidence and limits

- Tagged source: jj v0.45.1 commit `7c41cdeb16b6b321c64e789a966b6adf723816a5`; `cli/src/commands/log.rs:133-140`, `cli/src/cli_util.rs:474-490,532-565,801-833`, `lib/src/repo.rs:899-916`, `lib/src/default_index/store.rs:342-343,457-478,519-559`, `lib/src/transaction.rs:135-171`, and `lib/src/op_heads_store.rs:96-109,146-160`.
- `corpus/SOURCES.md` S103 records `cli_util.rs` at 185,869 bytes with SHA-256 `ee1eb31d16c0b5a920ea80ad2f73ff4183b83450013f63dacb8402f2f77f1e2d`; the fetched tagged file matched that digest exactly.
- Committed round-20 `ReviewVcsV3.md` documents measured repository writes for other jj mutating commands despite `--ignore-working-copy` (remote config, bookmark, workspace). It does not directly measure `jj --ignore-working-copy log`; the specific log expectation above is source-grounded, not a runtime observation.
- No VCS command, classifier, installer, transcript, or tool measurement was executed. No tools/packages were installed.

## Oracle

Recorded in `.ufo/waves/round-21/w1/oracles/JjReadIwc.json` as a `vcs_write` expectation, with the conditional nature of the source paths stated explicitly.
