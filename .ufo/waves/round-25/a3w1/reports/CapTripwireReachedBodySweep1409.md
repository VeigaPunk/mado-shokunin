# CapTripwireReachedBodySweep1409 — C2 row re-run, SCORECARD.md:1409 at 41cc04c8

Item: executor (C2 row contract). Capability: `tripwire reached-body sweep`.
Lane base: `41cc04c8d593837a0d5078bffaacdaa163d12897`. Sandbox clone:
`/fast/scratch/hyaku/mado-r25a3/c2/CapTripwireReachedBodySweep1409` (detached at 41cc04c8, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset), deleted after the runs and before returning (see Cleanup).
No tool was installed or upgraded; no package transaction was attempted; no git/jj write was made in the lane or the fleet repo.

## The row

`SCORECARD.md:1409`, under `### Capabilities (round 20, attempt 2; append-only)` (heading at :1406, section `## Round 20 — attempt-2 results…` at :1380):

> **tripwire reached-body sweep** — "Report every visible body the executed text reaches but the call path does not follow (thread targets, callbacks, decorators, closures, dunders, scheduled coroutines, recursion, past-depth helpers) as a `lead` row instead of dropping it" — evidence pointer: `python3 .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca` (`recall_lost` 0; 52 at `28c6837`) — first-working round 20.

Stated capability: a `lead` row for every reachable-but-unfollowed body; the meter named in the row is `recall_lost` from the round-20 a2 guard counter over a population frozen at `6a7d9ca`. The evidence pointer is the command itself (the frozen receipts are `.ufo/waves/round-20/a2/evidence/guards-after-a8960de655e6ea8c0a3bf74f5542041d9fe25b39.txt` and `guards-before-28c6837.txt`; the counter script at base is sha256 `414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`, the same bytes the round-20 receipt records).

## Command run (as written, plus the contract's bounds)

Runnable as written: yes — one positional revision, one `--fixtures-rev` pin, repo root derived from the script's own path, so it needs the lane repo (present in the clone) and nothing else. Run from the clone root:

```
timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca
```

exit=0 in 119.32 s (wall measured by the shell). Two further runs used the same form with `REV` = `28c6837` (the row's before-number) and `41cc04c8` (the present tool at base, sha256 `cd9da20c…`), each exit=0.

## Ledger line

| SCORECARD.md:1409 | tripwire reached-body sweep | Unfollowed reachable bodies (threads, callbacks, decorators, closures, dunders) reported as lead rows, not dropped | works at 41cc04c8: exit 0, recall_lost 0, crash_flip 0, pure_rows 0 with the present tool cd9da20c; at the row's own revision a8960de recall_lost 0 (exit 0) but crash_flip 1 — internal MemoryError on huge_many_stmts.jsonl under the contract's 4 GB cap, where the frozen round-20 receipt at the same tool sha256 a57d4fe9 records crash_flip 0 and rev_exit2 3 (mine: 4) | python3 .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca (contract form: timeout 600 prlimit --as=4000000000 python3 … ) | SCORECARD.md:1584 (round-24 status table supersedes the implied works of earlier rows; re-affirms works, recall_lost 0, at 8e5d9369) and `.ufo/waves/round-24/c2/manifest.json` entry "tripwire reached-body sweep" (frozen regex `"recall_lost": 0` plus the `"rev"` line); partial contradiction: SCORECARD.md:1412-1420 §Final residual-review disposition records C1 harmed at a8960de with misses that this row's frozen population does not contain (no imaplib fixture in the 81-file recall set at 6a7d9ca) |

## Verbatim output — primary run (a8960de, exit=0), sha256 08e09f9b411ff989c09d76b7def33176980ed1a092d4ea74ba8793b6701c401c

```
{
 "a2_mismatch": 0,
 "a2_mismatch_files": [],
 "a2_seconds": {
  "dotted-rebind-sp.jsonl": 0.057,
  "hang-fanout-12x4.jsonl": 0.364,
  "hang-mutual-24.jsonl": 0.079,
  "hang-selfrec-40.jsonl": 0.056,
  "importlib-alias.jsonl": 0.05,
  "jj-R-bookmark-collision.jsonl": 0.055,
  "jj-R-git-collision.jsonl": 0.054,
  "pure-heapq-nlargest.jsonl": 0.057,
  "pure-vars-print.jsonl": 0.054
 },
 "crash_flip": 1,
 "crash_flip_files": [
  ".ufo/waves/round-20/w2/AdvCrash/fixtures/huge_many_stmts.jsonl"
 ],
 "dup_row_sites": [],
 "dup_rows": 0,
 "fixtures_rev": "6a7d9ca0d2124a4077074b800c94a9bc1184441c",
 "populations": {
  "a2": 9,
  "crash": 172,
  "pure": 24,
  "recall": 81,
  "vcs": 74
 },
 "pure_rows": 0,
 "pure_rows_files": [],
 "recall_excluded": {
  ".ufo/waves/round-20/w2/AdvRecallShapes/fixtures/gap04-lambda-argv-lead.jsonl": "old false positive (AdvRecallShapes)"
 },
 "recall_lost": 0,
 "recall_lost_files": [],
 "rev": "a8960de655e6ea8c0a3bf74f5542041d9fe25b39",
 "rev_exit2": 4,
 "schema": "mado-r20-a2-guards-v1",
 "slowest": {
  "file": ".ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl",
  "seconds": 107.998
 },
 "timeouts": [],
 "tool_sha256": {
  "harmed": "367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d",
  "pre_harm": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
  "rev": "a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458"
 },
 "vcs_fn": 0,
 "vcs_fn_files": [],
 "vcs_fp": 20,
 "vcs_fp_files": [
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/eval-list-jj-root.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add--dry-run-eq-false.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add--dry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add-dd-n.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-checkout-n.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-dry-run-eq-false.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-porcel.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-dash-n-add.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-push--dry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-push-dry-run-eq-false.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-push-repo-dry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-config-list.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-describe-dry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-git--dry-run-push.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-git-fetch-dry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-git-push-dd-iwc.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-root.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-util-config-schema.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-util-exec-git-status.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-util-exec-true.jsonl"
 ]
}
```

## Before-leg replay (28c6837, exit=0) — verbatim key lines

The same command with `28c6837` reproduces the row's stated 52 and the frozen `guards-before-28c6837.txt` receipt exactly (recall_lost 52, crash_flip 13, pure_rows 24, vcs_fp 31, a2_mismatch 6, rev_exit2 24):

```
 "a2_mismatch": 6,
 "crash_flip": 13,
 "dup_rows": 0,
 "pure_rows": 24,
 "recall_lost": 52,
 "rev": "28c68378eccbd5f227cdc28a62406ff390e3540a",
 "rev_exit2": 24,
  "rev": "9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c"
 "vcs_fn": 0,
 "vcs_fp": 31,
```

## Present-tense re-run at base (41cc04c8, exit=0) — verbatim key lines

`rev` here is the tool the lane ships at base, sha256 `cd9da20c…`; recall_lost 0 holds with it, crash_flip 0, and vcs_fp moves 20 (a8960de) → 26 (present):

```
 "a2_mismatch": 0,
 "crash_flip": 0,
 "dup_rows": 0,
 "pure_rows": 0,
 "recall_lost": 0,
 "rev": "41cc04c8d593837a0d5078bffaacdaa163d12897",
 "rev_exit2": 3,
  "rev": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"
 "vcs_fn": 0,
 "vcs_fp": 26,
```

## What the run shows

1. **The row's meter reproduces.** `recall_lost` 0 at `a8960de` and 52 at `28c6837` — both legs match the row and the frozen round-20 receipts. All other guard metrics also match the frozen after-receipt (pure_rows 0, vcs_fn 0, vcs_fp 20, a2_mismatch 0, dup_rows 0, timeouts none, populations 81/172/24/74/9, tool sha256 a57d4fe9/harmed 367be947/pre_harm c1ae45a7, fixtures pin 6a7d9ca).
2. **One metric diverged, and it is resource-bound, not recall-bound.** At `a8960de` my run reports `crash_flip: 1` on `.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_many_stmts.jsonl` (a single JSONL line of 777,986 bytes, one `message`). Isolated: the `a8960de` tool exits 2 printing `{"error": "internal MemoryError", "exit": 2}` under `prlimit --as=4000000000` (3.6 s) and under `--as=8000000000` (7.3 s), while the `1f7f995` baseline tool exits 0 on the same fixture (1.7 s). The frozen round-20 receipt has `rev_exit2` 3 and `crash_flip` 0 for the same tool bytes, so the flip is today's host/limit outcome on that one 778 KB cell, consistent with the round-20 disposition's ReviewRuntimeV3 finding (>1,800 MiB on large assignment-only cells). It does not touch `recall_lost`.
3. **The capability's shape is directly visible.** On `.ufo/waves/round-20/w2/AdvRecallShapes/fixtures/ar05-create-task-inside-main.jsonl` the base tool prints one finding with `"evidence": "lead"`, `lead_findings` 1, `observed_findings` 0 (the `asyncio.create_task` body is not followed) — a `lead` row rather than a drop.
4. **The row's word "every" is population-bounded.** The round-20 disposition (:1412-1420) names a missed `imaplib.IMAP4_stream` process and recursive shell-string/callback-literal misses at `a8960de`; `git grep -i imaplib` over the recall population at `6a7d9ca` returns nothing, so `recall_lost 0` and those misses are compatible. The row is true of its frozen 81-file recall set, not of all bodies.
5. **Supersession.** The only later SCORECARD text about this capability is the round-24 status table entry at `:1584` (`works`, `recall_lost` 0 at `8e5d9369`), which the wave-2 scope note at `:1589-1591` counts inside the 12 heading-scoped capability rows. Round 24 also froze the same rule in `.ufo/waves/round-24/c2/manifest.json`. Nothing later marks it stale or failing; SCORECARD.md:1554's restoration of `tools/mado-tripwire.py` to `cd9da20c…` explains why the present-tense tool differs from the row's measured revision.

## Risks, blockers, cleanup

- Risk (row-reading): citing this row as "no reachable body is ever dropped" overstates it — its meter is `recall_lost` over 81 frozen files, and the round-20 disposition lists misses outside that set. A `crash_flip` difference also depends on host memory, so the sibling row `:1410`'s crash-flip 0 is host-contingent at `a8960de`.
- Risk (reproduction): the primary run's `crash_flip 1` is stable today at 4 GB and 8 GB caps; an unbounded run of the same fixture was killed (exit 143) after 39 s with no output. I did not re-run the counter unbounded, so no unbounded comparison is claimed.
- Blockers: none.
- Cleanup: sandbox clone deleted (`/fast/scratch/hyaku/mado-r25a3/c2/CapTripwireReachedBodySweep1409` — see `ls` below); scratch fixture copies live only under `/tmp/cap1409diag` (777 KB + tool copies); no process started by this item is left running (each python run was under `timeout`, and the counter's own scans are child processes of it).
- Installs: none.
