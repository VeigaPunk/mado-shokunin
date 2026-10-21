# SourceGitCommit — pinned upstream source findings

## Axes
- **C1 operability / residual repair:** source-callsite evidence for `git commit --dry-run` index-refresh and tree-update behavior relevant to VCS-boundary reasoning.
- **C2 calibration / independent artifact integrity:** exact public source bytes, digest, access date, and located evidence retained independently of implementation measurements.

## Source receipt
- URL: https://raw.githubusercontent.com/git/git/v2.56.0/builtin/commit.c
- Version: Git v2.56.0 (tag in the requested raw URL).
- Access date: 2026-10-21.
- SHA-256: `e566f2092ed52b6a1afa87ed62cd5bed7d18dd9723a990fcca9265ad46a18025`.
- Fetched body: 62,305 bytes; 1,994 lines, saved at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c`.
- Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/receipt.json`.

Located quote (20 words), source lines 1840–1841:
> “Set up everything for writing the commit object. This includes running hooks, writing the trees, and interacting with the user.”

## Observed source facts

- At `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:1836–1838`, the `dry_run` branch returns through `dry_run_commit(...)` before the ordinary `prepare_index(..., 0)` and `prepare_to_commit(...)` path. The dry-run helper at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:1428–1438` calls `prepare_index(..., 1)`, calls `run_status(...)`, then calls `rollback_index_files()`.
- `prepare_index` uses `is_status` to add `REFRESH_UNMERGED` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:365–366`). The as-is preparation path calls `refresh_cache_or_die(...)` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:483–485`); that helper calls `refresh_index(...)` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:346–348`). Thus the dry-run path can perform index refresh work through `prepare_index`; the source does not establish that dry-run skips index refresh.
- `prepare_index` has `cache_tree_update(...)` callsites in its interactive, include/all, as-is, and partial-index paths (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:424`, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:464`, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:486–489`, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:535–539`). The dry-run helper calls this same function with status mode enabled, then rolls back index lock files. Separately, `prepare_to_commit` calls `cache_tree_update(the_repository->index, 0)` at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:1111`; the normal commit path invokes `prepare_to_commit` at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:1842`, after the early dry-run return.
- The source comment at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c:1840–1841` describes the ordinary commit preparation as including “writing the trees.” The callsites alone do **not** prove whether a given `cache_tree_update` creates new tree objects, reuses existing objects, or what ODB effects remain after index rollback. The implementation of `cache_tree_update` and rollback is outside this file; no runtime behavior was measured. Therefore this source is not evidence for a universal “dry-run writes nothing” or “dry-run definitely writes tree objects” claim.

## Existing S-row coverage

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:111` has S099 for the Git v2.56.0 `git-commit.adoc` documentation and its dry-run-versus-write semantics. S100 at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:112` is the `git-add` dry-run documentation. These rows cover related documented behavior, but not the implementation-level refresh and `cache_tree_update` callsites in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c`. No SOURCES row was added; L1 reserves S116 onward.

## Limits

Only the requested raw source at https://raw.githubusercontent.com/git/git/v2.56.0/builtin/commit.c (saved at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitCommit/git-v2.56.0-builtin-commit.c`) was fetched and inspected. No companion helper source, tag-signature verification, Git host-version check, or runtime/host probe was performed. The exposed tool inventory has no LSP device; these are line-located source observations, not LSP definition/reference results. No package or tool was installed.

Report: .ufo/waves/round-21/w1/reports/SourceGitCommit.md
