# CapDetectorRemovalSideGuard1410 — C2 row re-run (SCORECARD.md:1410, base 41cc04c8)

Seat `MadoR25A3.CapDetectorRemovalSideGuard1410`, wave `a3w1` (PRE-DATA). No lane file was edited except this
report; `tools/mado-binds.py` and the frozen C1 counter were not touched. Sandbox clone deleted before returning.

## Ledger line

| SCORECARD.md:1410 | detector removal-side guard | Counts findings a newer tripwire tool drops versus an older one, crash flips and pure-data rows over frozen populations | works at 41cc04c8: exit 0; recall_lost 0, crash_flip 0, pure_rows 0, vcs_fn 0, a2_mismatch 0, dup_rows 0, timeouts none, rev_exit2 3, measured tool sha256 cd9da20c…; vcs_fp 26 (outside this row's counters) | timeout 600 prlimit --as=4000000000 -- python3 -I .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca (cwd: sandbox clone checked out at 41cc04c8) | SCORECARD.md:1585 (round-24 status: works, all counters 0 at 8e5d9369); caveat SCORECARD.md:1458 (a1e1b608 zeros plus two logging false leads) |

## Row, section, and what its demonstration actually is

Row text at `41cc04c8:SCORECARD.md:1410`, under `### Capabilities (round 20, attempt 2; append-only)` (`:1405`):

```
| detector removal-side guard | Count, for a tripwire change, the findings an older tool reported that the new one drops, the crash flips and the pure-data rows, over frozen adversarial populations | `a2/evidence/guards-before-28c6837.txt` vs `guards-after-a8960de….txt` | 20 |
```

The row's third cell is **an evidence pointer, not a command**: two receipt files, the second truncated with an
ellipsis. Both exist at base and were inspected:

- `.ufo/waves/round-20/a2/evidence/guards-before-28c6837.txt` — `RECEIPT … measured_commit=28c68378eccbd5f227cdc28a62406ff390e3540a … argv=python3 .ufo/waves/round-20/a2/a2-guards.py 28c6837 --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c`; counters `recall_lost 52, crash_flip 13, pure_rows 24, vcs_fn 0, vcs_fp 31, a2_mismatch 6, dup_rows 0, rev_exit2 24, timeouts []`.
- `.ufo/waves/round-20/a2/evidence/guards-after-a8960de655e6ea8c0a3bf74f5542041d9fe25b39.txt` (the cell's `guards-after-a8960de….txt`) — same argv shape with `a8960de…`; counters `recall_lost 0, crash_flip 0, pure_rows 0, vcs_fn 0, vcs_fp 20, a2_mismatch 0, dup_rows 0, rev_exit2 3, timeouts []`, slowest `huge_bash_cmd.jsonl` 83.483 s.

Both receipts head with `tool=.ufo/waves/round-20/a2/a2-guards.py tool_sha256=414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`. The script at base has exactly that hash
(8,458 bytes, 188 lines), so the committed counter bytes are the bytes that produced the cited receipts.

Because the cell is not runnable as written, I used the nearest documented form:

1. `SCORECARD.md:1367` registers `python3 .ufo/waves/round-20/a2/a2-guards.py REV --fixtures-rev PIN`.
2. The round-24 C2 manifest (`.ufo/waves/round-24/c2/manifest.json` at base) has an entry named
   `detector removal-side guard` fixing argv `python3 {LANE}/.ufo/waves/round-20/a2/a2-guards.py {REV} --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c`,
   cwd `{LANE}`, `timeout_s` 600, `exit_ok` [0], and `regex_all` = `recall_lost`, `crash_flip`, `vcs_fn`,
   `a2_mismatch`, `dup_rows`, `pure_rows` all 0 plus `rev` = `{REV}`. Its own `why` says: "vcs_fp is a
   false-positive count outside this removal-side claim and is not asserted."

I substituted `{REV}` = 41cc04c8 and ran the script from the sandbox clone (the script derives its repo root from
its own `__file__`, so it read the clone's bytes, not the lane's).

## Sandbox and preflight

```sh
df -h /fast                                        # 804G size, 221G avail, 73% used
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapDetectorRemovalSideGuard1410
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapDetectorRemovalSideGuard1410 checkout -q --detach 41cc04c8
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapDetectorRemovalSideGuard1410 rev-parse HEAD
# 41cc04c8d593837a0d5078bffaacdaa163d12897
git -C <clone> cat-file -t 6a7d9ca     # commit (fixture pin present in clone)
git -C <clone> cat-file -t 28c6837     # commit
git -C <clone> cat-file -t a8960de     # commit
```

Counter bytes at base: sha256 `414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`, matches the
receipts' `tool_sha256`; fixture pin `6a7d9ca0d2124a4077074b800c94a9bc1184441c`.

## Demonstration command and result (the required re-run)

Command, run in the clone, per the C2 contract (`timeout 600`, `prlimit --as=4000000000`):

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapDetectorRemovalSideGuard1410
timeout 600 prlimit --as=4000000000 -- python3 -I .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca
```

Observed: **exit 0**, `real 2m9.456s  user 28m7.140s  sys 13m11.326s`, stderr empty, stdout 3,359 bytes / 78
lines. Every round-24 manifest regex for this row matched: `rev` = `41cc04c8d593837a0d5078bffaacdaa163d12897`,
`recall_lost 0`, `crash_flip 0`, `vcs_fn 0`, `a2_mismatch 0`, `dup_rows 0`, `pure_rows 0`. Also observed:
populations `recall 81, crash 172, pure 24, vcs 74, a2 9`; `timeouts []`; `rev_exit2 3`; `slowest
huge_bash_cmd.jsonl 109.459 s`; `vcs_fp 26`; measured tool sha256
`cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` (the same bytes as `8e5d9369:tools/mado-tripwire.py`,
verified by `git show 8e5d9369:tools/mado-tripwire.py | sha256sum`).

Status at 41cc04c8: **works**. The guard executes over the frozen populations and reports all three counters the
row names (dropped findings, crash flips, pure-data rows) as 0 for the present tool.

### Full stdout of the demonstration run (78 lines, verbatim)

```json
{
 "a2_mismatch": 0,
 "a2_mismatch_files": [],
 "a2_seconds": {
  "dotted-rebind-sp.jsonl": 0.064,
  "hang-fanout-12x4.jsonl": 0.534,
  "hang-mutual-24.jsonl": 0.27,
  "hang-selfrec-40.jsonl": 0.099,
  "importlib-alias.jsonl": 0.073,
  "jj-R-bookmark-collision.jsonl": 0.064,
  "jj-R-git-collision.jsonl": 0.072,
  "pure-heapq-nlargest.jsonl": 0.084,
  "pure-vars-print.jsonl": 0.068
 },
 "crash_flip": 0,
 "crash_flip_files": [],
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
 "rev": "41cc04c8d593837a0d5078bffaacdaa163d12897",
 "rev_exit2": 3,
 "schema": "mado-r20-a2-guards-v1",
 "slowest": {
  "file": ".ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl",
  "seconds": 109.459
 },
 "timeouts": [],
 "tool_sha256": {
  "harmed": "367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d",
  "pre_harm": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
  "rev": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"
 },
 "vcs_fn": 0,
 "vcs_fn_files": [],
 "vcs_fp": 26,
 "vcs_fp_files": [
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/eval-bang-commit-zn.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/eval-list-commit-porcelain-nodry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/eval-list-jj-root.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add--dry-run-eq-false.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add-Nn.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-add-dd-n.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-checkout-n.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-dry-run-eq-false.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-nodry-porcelain.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-porcel.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-porcelain-m.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-porcelain-nodry.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-z-m.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-commit-zn.jsonl",
  ".ufo/waves/round-20/w2/AdvVcsForms/fixtures/git-dash-n-add.jsonl",
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

Process exit code of the command: `exit=0`.

## Supporting replays of the cited receipts

Both extra runs are in the same clone, under the same `timeout 600` and `prlimit --as=4000000000`. They show the
counter is not a constant-zero stub and expose one replay hazard.

### `28c6837` (the pointer's "before") — reproduces exactly

```sh
timeout 600 prlimit --as=4000000000 -- python3 -I .ufo/waves/round-20/a2/a2-guards.py 28c6837 --fixtures-rev 6a7d9ca
```

exit 0, wall 117.69 s. Counters, verbatim from the JSON:

```text
 "recall_lost": 52,
 "crash_flip": 13,
 "pure_rows": 24,
 "vcs_fn": 0,
 "vcs_fp": 31,
 "a2_mismatch": 6,
 "dup_rows": 0,
 "rev_exit2": 24,
 "timeouts": [],
```

These equal the committed before receipt field for field (including `rev` sha and measured tool sha
`9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`), so the removal-side counter does detect the
older tool's 52 lost recalls, 13 crash flips and 24 pure-data rows on the frozen populations.

### `a8960de` (the pointer's "after") — does not reproduce under the mandated cap

```sh
timeout 600 prlimit --as=4000000000 -- python3 -I .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca
```

exit 0, wall 117.31 s, but `crash_flip` = 1 (`crash_flip_files` =
`.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_many_stmts.jsonl`) and `rev_exit2` = 4, against the receipt's
`crash_flip 0` / `rev_exit2 3`. The other counters match the receipt (`recall_lost 0, pure_rows 0, vcs_fn 0,
vcs_fp 20, a2_mismatch 0, dup_rows 0, timeouts []`).

Mechanism, measured directly: the `a8960de` tool on that one fixture exits 2 with
`{"exit": 2, "error": "internal MemoryError", …}` (`MADO_TRIPWIRE: could_not_evaluate`) at a 4,000,000,000-byte
address-space cap, and also at 8,000,000,000 and 12,000,000,000; the base tool `cd9da20c` scans the same fixture
under the same 4 GB cap with exit 0 and `MADO_TRIPWIRE: clean`. The committed `a8960de` receipt was produced by an
argv with no `prlimit` (its header: `argv=python3 .ufo/waves/round-20/a2/a2-guards.py a8960de… --fixtures-rev
6a7d9ca…`), so the divergence is consistent with the contract's address-space cap, not with drift in the base
status (the old receipt cannot be replayed capped on this host). The base-status run above is unaffected: the
present tool scans that fixture cleanly under the same cap, and its counters are 0.

One failed attempt, reported for completeness: `/usr/bin/time` is not installed (exit 127); timings were taken with
shell `time` and epoch-second deltas instead. No result depends on them.

## Supersession / contradiction grep over all of SCORECARD.md at 41cc04c8 (1,618 lines)

- `:1585` — `### Capability status (round 24 re-demonstration)` (`:1566`): `detector removal-side guard | works |
  same a2-guards.py run: removal, crash-flip and pure-row counters all 0, at 8e5d9369`. This **supersedes** the
  implied status of `:1410` and agrees with the base observation (the `8e5d9369` tool bytes are identical to
  `41cc04c8`'s). Its scope note says the frozen C2 population is the 12 rows under `Capabilities` headings; `:1410`
  is one of them.
- `:1458` — round-21 note: "The old A2 guard at a1e1b608 recorded recall_lost0/crash_flip0/vcs_fn0/a2_mismatch0/
  dup_rows0, plus two logging false leads". A caveat about that revision's tool output, not a contradiction of the
  guard; the guard still reports those zeros.
- `:1392` — registers the same counter with the `28c6837` → `a8960de` numbers (`recall_lost 52 → 0, crash_flip
  13 → 0, pure_rows 24 → 0`), consistent with the pointer.
- `:1393` is a different row (whole-corpus diff removal side, `corpus-diff-28c6837-vs-a8960de.json`), not a
  supersession. `:291` is an unrelated `gkeep.conf removal case`.
- No row or text marks `:1410` stale; nothing contradicts "works".

## Limits and risks

- The row has no literal runnable command; the nearest documented forms (`:1367`, round-24 manifest) were used and
  are named above. A reviewer requiring the literal cell would find only evidence files.
- `vcs_fp` moved 20 → 26 between `a8960de` and base. It is explicitly outside this row's removal-side claim (the
  round-24 manifest says it is not asserted) and is reported, not scored.
- The counter's per-fixture timeout is 120 s; `huge_bash_cmd.jsonl` needed 105.8–109.5 s on this shared host. A
  slower host would put it in `timeouts` (the process would still exit 0) and could perturb crash-flip/pure-row
  counts. One measurement run was taken; it is not repeated to steer a result.
- Replaying the old `a8960de` receipt under the mandated 4 GB cap is impossible (MemoryError, shown above); the
  pointer's after numbers were verified by reading its receipt file and by the exact before replay, not by a capped
  after replay.
- The guard's removal comparison uses fixed bases `9c54c56` / `1f7f995`; "an older tool" in the row means those
  pinned bases, not an arbitrary prior revision.

## Safety and maintenance

- Lane: read-only (`git show`, `git ls-tree`, `grep` on extracted text). No git/jj write, no commit, no checkout in
  the lane. No file written in the lane except this report. No changes to `tools/`, `.ufo/waves/round-25/c1/`, or
  `corpus/`.
- Clone under `/fast/scratch/hyaku/mado-r25a3/c2/CapDetectorRemovalSideGuard1410` was checked out at `41cc04c8`
  and **deleted** after the runs; `pgrep -fa 'a2-guards|tw-*'` after the runs found no remaining process (exit 1).
- No packages, services, home configuration, compositor state, or `hyprctl` calls; no nested Hyprland started; no
  network fetch. No builds, tests, linters, or formatters were run beyond the demonstration command itself.
- Kept receipts (scratch, outside the lane): `/fast/scratch/hyaku/mado-r25a3/c2/guards-41cc04c8.json` (base stdout,
  3,359 B), `guards-28c6837.json` (11,219 B), `guards-a8960de.json` (2,956 B), the `scan-*` memory-cap probes, and
  `SCORECARD-41cc04c8.md` (extracted base scorecard).
