# R55W2RevC1Code — report

Scope: correctness review (not style) of `quality/counters/c1-r55-kbd-entry.py` and `quality/r55_ctl_c1.py` at
57584ed67716340b3d466fa04333ac0bab3fb79e. Full defect table with inputs, commands, observed and expected output:
`.ufo/waves/round-55/w2/R55W2RevC1Code/review.md`. Receipts: `.ufo/waves/round-55/w2/R55W2RevC1Code/receipts/`.
Fix diffs verified on copies: `.ufo/waves/round-55/w2/R55W2RevC1Code/fixes/`.

## Verdict summary

| Target | Verdict | Evidence |
|---|---|---|
| `--rev` as full hash, abbreviated hash, HEAD, branch, annotated tag, lightweight tag, `^{commit}` | SURVIVES | review.md "Counter --rev forms"; all rc 0, `TARGET_MET` |
| `--rev` as tree oid, blob oid, unknown hash, tree-tag, `rev:path`, unborn HEAD, empty, `-x` | SURVIVES | rc 2, stdout empty |
| `--work` honoured, nothing written to /tmp, no leftovers, file or unwritable path (counter) | SURVIVES | `find /tmp -newer` empty; setup error rc 2 |
| `--work` file or unwritable (harness) | BROKEN (D8) | traceback, rc 1, stdout empty |
| git env scrub (`GIT_DIR` and config injection) | SURVIVES | env replaced by `git_env`; verdict unchanged |
| git env scrub of replace refs and lazy fetch | BROKEN (D2, D9) | replace ref flips verdict; partial clone fetched 14 blobs into the scored repo |
| repo through symlink (root), trailing slash, relative `--repo`/`--work` | SURVIVES | TARGET_MET rc 0 |
| repo that is a subdirectory of a repo (direct or symlinked) | BROKEN (D1, High) | `TARGET_MET` rc 0 on a subtree with no corpus at the repo root |
| rc/stdout contract under uncaught exceptions (counter) | BROKEN (D5, D6) | RecursionError / embedded NUL: traceback, rc 1, stdout empty |
| rc/stdout contract (harness) | BROKEN (D5, D7, D8) | RecursionError, UnicodeDecodeError, FileNotFoundError: rc 1, stdout empty |
| fence closer with info string (counter) | BROKEN (D3, High) | K12 inside a CommonMark code block: `TARGET_MET` rc 0; `cmark` renders it in `<pre><code>` |
| `new_rows` used-by substring | BROKEN (D4, Medium) | used-by `…r55.md.orig` for S378–S380 gives `new_rows=3/3` rc 0 |
| HTML comment on one line before K12 | NOT-REPRODUCED | block-level CommonMark ends the block on the first line; counter agrees |
| `--selftest` at scored rev | SURVIVES as a self-check | 50/50 passed; output is 52 lines, contrary to the docstring (D10) |
| Harness `good`/controls at scored rev | SURVIVES on the scored tree | `good=ok controls=7/7 verdict=OK`; it also passes the D1 and D3 trees, so it cannot see the counter's false greens |

## What ran

- Counter at 57584ed (full, abbreviated, HEAD, branch, annotated and lightweight tags, `^{commit}`, tree/blob/unknown/tree-tag/`rev:path`, unborn HEAD, empty and `-x` revs, `--repo` as subdir, symlink, relative paths, nonexistent/file/empty repo, `--work` file/unwritable/absent/spaced).
- Counter `--selftest` at 57584ed: 50/50 passed (`receipts/selftest.out`).
- Harness `r55_ctl_c1.py` at 57584ed: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` (`receipts/harness.out`); harness with an unknown rev, `--counter` nonexistent, `--rev=--show-toplevel`.
- Scratch fixtures (git repos, toplevel asserted before commit): clone of the lane (replace refs on the entry blob, tags, branch); a repo whose `fake/` subtree is a full copy; deep-nested `frozen-tables-v2.json`; NUL pin key in `frozen-tables-v2.json`; non-UTF-8 file in the pin dir; fence-closer and HTML-comment entry variants; used-by variant of SOURCES.md; partial clone (`--filter=blob:none`, `uploadpack.allowFilter` set on the scratch clone only).
- Mutation copies `fixes/c1-fix-D1-D2-D3.py` and `fixes/c1-fix-D4-D5-D6.py` (copies under scratch, never the lane): each targeted fix was run on its own failing input and on the lane at 57584ed (`TARGET_MET` rc 0 retained), and selftest 50/50 retained.
- Mechanism checks with plain git on scratch repos: `GIT_NO_REPLACE_OBJECTS=1 git cat-file` shows the original blob; `GIT_NO_LAZY_FETCH=1 git cat-file` on a partial clone fails with rc 128.
- `cmark 0.31.2` (`/usr/bin/cmark`, pre-installed, read-only use) on the fence and comment fixtures.
- CommonMark spec text fetched read-only from raw.githubusercontent.com (`receipts/spec.txt`), sections on fenced code blocks and HTML blocks.

## What did not run / limits

- No tool was installed or upgraded. `pacman` is paused host-wide and no `uv tool` or `npm` install was needed.
- No `hyprctl` command was run (not needed for C1).
- The D2 and D9 fixes were verified by a copied counter, not by a patch to the lane. D1, D3, D4, D5, D6 fixes likewise.
- D7 and D8 (harness) are not fixed on a copy; the cause is identified from the traceback and code (`read_tree` strict decode; unguarded `work0.mkdir`).
- D11 (selftest cleanup on exception) is code reading only; it was not triggered.
- CommonMark behaviour was checked with one parser (cmark 0.31.2) and the spec text; no other parser.
- The harness's own control set was not re-derived; its verdict on the scored tree is reported as observed.
- Two early fixture runs were contaminated by a replace ref I had created in a scratch clone (the lane was never touched). Those outputs (non-UTF-8 counter line and a relative-path run on that clone) were discarded and the cases re-run on a clean fixture; the discarded outputs are not in receipts.

## Lane and scratch hygiene

- The lane was not written: no tracked file edited, no git mutation in the lane (only read commands: `rev-parse`, `cat-file`, `ls-tree`, `show`, `status`, `archive` to scratch).
- Every clone, fixture, copy and work dir lived under `/fast/scratch/hyaku/mado-r55/R55W2RevC1Code/`, removed before yield.
- Deliverables written only under `.ufo/waves/round-55/w2/R55W2RevC1Code/` and this report.
- No credentials were read or written.
