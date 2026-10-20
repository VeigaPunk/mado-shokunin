# RevHarmWatchLimits — Two revision-binding gaps undermine round-20 admission evidence

Axes reviewed: revision identity, evidence integrity, and minimality. Read-only review; no edits or harness executions.

## Findings

### High — `harm-watch.sh` can report a worktree SCORECARD result as evidence for `REV`

The navigation section extracts `### Counting command` from `$ROOT/SCORECARD.md` in the worktree (`.ufo/waves/round-19/harm-watch.sh:359-367`). It hashes the worktree file and extracted block, then compares the *whole-file* worktree digest with `git show "$REV_SHA:SCORECARD.md"` (`:369-377`). If they differ, the script only appends a note that the worktree block will be read; it still executes the already-extracted worktree block and records the result by its exit code (`:378-386`). Unlike `run_pinned`, this path does not skip/fail on a pin mismatch (`:119-133`). Thus an `OK` result can be attributed to `REV` while being produced by a different worktree block. The current SCORECARD counting command itself accepts `REV` and reads revisioned corpus/index files (`SCORECARD.md:63-90`), but that does not bind the command text to that revision.

This is directly relevant to round-20 C2 criterion 30, which requires a stated count to be re-derived at the measured revision (`SCORECARD.md:1263-1273`); the round-20 plan explicitly routes the “harm-watch worktree block” issue (`SCORECARD.md:1213-1216`). The source limit is also stated at `corpus/lessons/round-19.md:110-116`.

**Minimal fix:** read `REV:SCORECARD.md` with `git show`, extract and hash the counting block from those exact bytes, and execute that block with `REV=$REV_SHA` from the lane root. Fail closed if the committed file/block cannot be read. Alternatively, refuse to run when the worktree file differs from `REV`; a mismatch note followed by an `OK` is insufficient. Record the committed SCORECARD and block digests with the receipt.

Evidence: `harm-watch.sh:359-386`; source SHA-256 `077e1b4d05be67aca0587b240122f05eb2d4bb4f5955d93f368d46b0ae09238a`.

### High — `supersede-sweep.py` combines a revisioned corpus with a worktree ledger

`DEFAULT_LEDGER` is constructed from the executing script's directory (`.ufo/waves/round-19/supersede-sweep.py:43-44`). `main()` loads that ledger before resolving the requested revision (`:128-153`); the later corpus tree and file reads use the resolved commit (`:151-187`). The optional `--ledger` flag accepts an arbitrary path, but neither default nor override is verified against the requested commit. The result therefore has no source-level guarantee that its supersession rules belong to the same revision as the scanned corpus. **[INFERENCE]** If the worktree ledger differs from the ledger at `REV`, the sweep can report a clean or stale result for a mixed-input state, not the measured revision. The round-19 lesson records this as open, and round-20 explicitly routes the “supersede-sweep worktree ledger” issue (`corpus/lessons/round-19.md:110-116`; `SCORECARD.md:1213-1216`).

**Minimal fix:** resolve `REV` first, obtain `.ufo/waves/round-19/supersessions.json` from that commit (e.g. `git show "$commit:.ufo/waves/round-19/supersessions.json"`), and parse those bytes. If retaining path-based loading, require the ledger digest to equal the revision's git-object bytes and fail closed otherwise. Include the ledger path, commit, and digest in the sweep evidence.

Evidence: `supersede-sweep.py:43-44,128-187`; current ledger SHA-256 `a0e6cfbe2f096602ce8f85132cefe37b0fdb9ddbd2f1172e46a65236d9cfb636`; script SHA-256 `fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4`.

## Admission relevance and residual risk

These are input-provenance gaps, not evidence that a particular round-20 count is wrong. A round-20 result relying on either check is not revision-bound until its source input is pinned or a mismatch aborts before execution. Round-20's own claim text makes measured-revision counting an admission condition (`SCORECARD.md:1263-1273`). The round-19 limits paragraph also lists distinct open items: the `measure-mutants.py --out` guard, malformed-receipt behavior in `anchor-durability.py`, and `frozen-repin.py` receipts without `measured_commit` (`corpus/lessons/round-19.md:110-116`). They are not fixed by the two source-binding changes above and were not audited here.

The source digests were captured with `sha256sum`; relevant output included:

```text
077e1b4d05be67aca0587b240122f05eb2d4bb4f5955d93f368d46b0ae09238a  .../.ufo/waves/round-19/harm-watch.sh
fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4  .../.ufo/waves/round-19/supersede-sweep.py
0139a1a403d4a0e431106e9d7fe70009daa86b7016e7dbbc81292d4593e62914  .../SCORECARD.md
```

## Limits

Static source inspection only; neither script was run. The LSP device was unavailable (`read xd://lsp` returned “No such tool”), so no LSP status/references/definitions/diagnostics were available. No text grep was used as semantic proof. I did not inspect or validate the other open limits listed above, nor verify any round-20 generated receipt.

## Installs

None.
