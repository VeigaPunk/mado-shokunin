# ExecSelftest — runner pass at tip (round 30, w1)

Item: runner only — no writes beyond this report. Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`. All commands run from that
root; nothing in the lane repo, fleet repo, git index or jj state was
mutated (this report file excepted).

## Verdict: PASS on all three assigned checks

| Check | Result |
|---|---|
| `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed`, **exit 0** (wall 15.74 s) |
| `git diff --stat 8f51071b master -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md` | **empty**, exit 0 — at both tips measured (see tip movement) |
| `git status --porcelain` | 0 rows before wave reports landed; then 1 untracked row (`?? .ufo/waves/round-30/w1/`); a tracked modification ` M quality/q36-successor-receipts.txt` appeared at 07:06:46Z from a sibling's r28-leg run — path-only diff, §3a |

## 1. Hermetic suite

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
bash tools/mado-verify.sh --selftest          # stdout captured, 1 line
EXIT=0
MADO_SELFTEST: 460/460 assertions passed
Wall time: 15.74 seconds
```

- 460/460 matches the registration's harm-watch base value (N/N unchanged);
  no `FAIL`/`not ok`/`ERROR` lines in the output (grep count 0).
- Run at worktree HEAD `92d3c86` (the tip at run time). `ScoutAxisScores`
  independently ran the base-extracted copy at `8f51071b` and also got
  460/460 exit 0, so the suite is green at base and at tip.
- Script blob pinned: `tools/mado-verify.sh` = `9113c7c05e586328f44ed6822a3d12ff34c47a36`
  at base and at tip (identical), so tip-run and base-run exercise the same
  suite bytes.

## 2. Scoped byte-identity (expected empty)

Run twice, because the lane tip advanced during the wave:

| Pass | UTC | `master` | scoped diff | exit | name-status rows |
|---|---|---|---|---|---|
| A | 2026-10-24T07:03:42Z | `92d3c86` | empty | 0 | 0 |
| B | 2026-10-24T07:04:07Z | `d72243e` | empty | 0 | 0 |

Blob-level pins, base `8f51071b` vs tip `d72243e` — all SAME:

| Path | Blob |
|---|---|
| `tools/mado-verify.sh` | `9113c7c05e586328f44ed6822a3d12ff34c47a36` |
| `SKILL.md` | `a6a68dd5c13cebfeccaf37278b87c82751efb613` |
| `PROVINCE.md` | `80079c8ca52053853744b3875593c8453c51cac5` |
| `corpus/knowledge` (tree) | `0d93899cd0b93e03949bc89d6215ca2b6bc3e00e` |

`corpus/knowledge` file count is 43 at base and 43 at tip (the C1 fence's
denominator; not a re-measurement of the fence itself, which is C1's item).

Tip movement observed: `master` went `92d3c86` → `d72243e` ("round-30
verifier spot-check (integrator, hyaku): non-author admit/reject") between
passes. That commit touches exactly one path,
`corpus/lessons/round-30-verifier-spotcheck.md` (+109, 0 deletions) — outside
the scoped set, which is why the second pass is still empty. `446dc39`
(the C1/C2 data commit) is an ancestor of both tips.

## 3. `git status --porcelain` — every row seen

| Snapshot | UTC | Rows |
|---|---|---|
| before peer wave reports existed | 2026-10-24T07:03:42Z | (none) |
| after scouts wrote reports | 2026-10-24T07:03:56Z | `?? .ufo/waves/round-30/w1/` |
| re-check at new tip | 2026-10-24T07:04:07Z | `?? .ufo/waves/round-30/w1/` |
| after report write | 2026-10-24T07:04:25Z | `?? .ufo/waves/round-30/w1/` |
| later, tracked change appears | 2026-10-24T07:07:32Z | ` M quality/q36-successor-receipts.txt`, `?? .ufo/waves/round-30/w1/` |
| restored by a sibling seat | 2026-10-24T07:08:21Z | `?? .ufo/waves/round-30/w1/` (tracked row gone) |

The untracked row is the wave-1 scratch directory holding peer reports
(`ScoutAxisScores.md`, `ScoutIndexHistory.md`, `ScoutW04.md`,
`CritSourcedClaim.md`, `ExecC1Rerun.md`, …) plus this file, so it adds no
row of its own. Until 07:04:25Z nothing tracked was modified or staged.

### 3a. Late tracked modification (outside this item's write scope)

At 07:06:46Z (mtime, -0300 04:06:46) `quality/q36-successor-receipts.txt`
— committed evidence, not an assigned wave path — was rewritten in the
worktree. First observed by this item at 07:07:32Z; `RevC1Fence` and
`SentScope` independently report the same file.

Diff is provenance-only, verdict-neutral:

- 19 lines on both sides; `git diff --numstat` = `4 4`.
- 4 raw differing lines, **0** after normalizing `/tmp/...` and
  `/fast/scratch/.../run.XXXXXXXX` tokens.
- `rc=`/`expected=`/`PASS` token count 6/6 identical; the PASS/FAIL verdict
  sequence is identical.

Cause (verified in source): `quality/q36-successor-run.sh:7` sets
`RECEIPTS="$ROOT/quality/q36-successor-receipts.txt"` and line 21 truncates
it (`: > "$RECEIPTS"`) before appending rows; run directories come from
`mktemp -d "$SCRATCH_ROOT/run.XXXXXXXX"` (line 15). A sibling seat re-ran
the r28 q36-witness leg during the wave. This seat did not: its only
execution was `tools/mado-verify.sh --selftest` at 07:03:42Z, and
`tools/mado-verify.sh` contains zero `q36` references (grep count 0).

Consequence worth the L1's attention: that lane gate is **non-idempotent**
— every run rewrites a tracked evidence file with fresh ephemeral paths, so
a "clean `git status`" harm-watch assertion cannot coexist with re-running
the r28 leg unless the receipt is restored or the script writes outside the
tree. Not restored and not remediated here: outside this item's write
scope, and remediation is L1-owned.

Resolution at 07:08:21Z: the tracked row is gone. Worktree sha256
`667bee37062141a20de2533f72201ca9eb19c8dbcf8f39724c169885493d0721` equals
the `HEAD:` blob hash, mtime 07:08:10Z — a sibling seat restored the
committed bytes, so the final tree state is clean apart from the untracked
`w1/` row. The non-idempotence finding stands independently of the restore.

Scoped predicate re-checked at 07:07:32Z: `git diff --stat 8f51071b
<master> -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md` still empty,
exit 0. No deletions exist anywhere in the r30 range
(`8f51071b..92d3c86` full stat was 22 files, 1388 insertions, 0 deletions).

## Risks / limits

- `--selftest` was run against the worktree at tip, not a base-extracted
  copy (base coverage comes from the peer's independent run); script blob
  identity makes the two runs comparable.
- `git status` rows are point-in-time while sibling seats are still writing
  reports, so later rows are expected and not attributable to this item.
- New capability `quality/check-index.py` sits outside the assigned path
  set, so this pass says nothing about C3's gate; C3 has its own items.
- The suite's 460/460 is a count only — this item did not audit assertion
  quality.

## Lane bounds / tooling

No subagent dispatch (this seat has no task/spawn tool on this host
surface; the "single labrat" allowance was unused). No git/jj mutation, no
compositor or config touch, no pacman transaction, no installs performed.

## Blockers

None.
