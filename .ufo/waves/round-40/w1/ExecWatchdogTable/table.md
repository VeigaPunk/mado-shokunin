# Watchdog table — mado rounds 32–39: launch lines, dead attempts, completion, dirty closures

Read-only digest. Two sources only: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` and
`mado-shokunin/corpus/lessons/round-{32..39}-verifier-spotcheck.md`. Every number below carries the
`grep -c` (or the arithmetic) that reproduces it. No verdict is stated beyond "the spot-check does /
does not name leftover working-tree files" and the verbatim quotes; nothing is inferred from them.

## Pins

- Watchdog log: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`. First read (line numbers below are
  as of this state): `sha256 = 5827413166271e7edf2a364c121132f4a42995d918137db8d77a92e5400b4631`,
  `wc -l = 1418`, mtime `Oct 25 17:46`. Re-checked after the table was written:
  `sha256 = 784433719336f09798197a91832b8bbdfab0843105d72d09a4f987a02fd18e2b`, `wc -l = 1419`; the one
  appended line is `2026-10-25T17:49:56-03:00 launch kama round=42 pgid=2295067 driver=hyaku-inline attempt=1`
  (not a mado line), and the mado 32–39 counts re-ran identical (`20 / 10 / 2 / 8`). It is a live
  append-only file, so a later append can shift no line before 1419.
- Slice completeness: `grep -c -E 'mado round=3[2-9]' .ufo/watchdog.log` → `20`, and
  `grep -E 'mado round=3[2-9]' .ufo/watchdog.log | grep -vc -E ' launch | complete | lane-dead-no-report '`
  → `0`, so every mado 32–39 line is one of the three verbs counted below (10 launch + 2 dead + 8 complete = 20).
- Spot-checks: `ls corpus/lessons/round-{32..39}-verifier-spotcheck.md | wc -l` → `8` (all present).

## A. Watchdog counts per round

`NN` = the round number in the row; each cell shows the measured value and the exact command.

| round | launches | `lane-dead-no-report` | `complete` | completion time (verbatim) | elapsed first launch → complete |
|---|---|---|---|---|---|
| 32 | 1 — <code>grep -c ' launch mado round=32 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=32;'</code> | 1 — <code>grep -c ' complete mado round=32;'</code> | `2026-10-24T20:33:30-03:00` | 36m52s |
| 33 | 1 — <code>grep -c ' launch mado round=33 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=33;'</code> | 1 — <code>grep -c ' complete mado round=33;'</code> | `2026-10-24T21:30:29-03:00` | 32m18s |
| 34 | 1 — <code>grep -c ' launch mado round=34 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=34;'</code> | 1 — <code>grep -c ' complete mado round=34;'</code> | `2026-10-24T22:55:29-03:00` | 1h14m33s |
| 35 | 2 — <code>grep -c ' launch mado round=35 pgid='</code> | 1 — <code>grep -c ' lane-dead-no-report mado round=35;'</code> | 1 — <code>grep -c ' complete mado round=35;'</code> | `2026-10-25T03:53:57-03:00` | 4h39m19s |
| 36 | 1 — <code>grep -c ' launch mado round=36 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=36;'</code> | 1 — <code>grep -c ' complete mado round=36;'</code> | `2026-10-25T05:41:00-03:00` | 1h31m55s |
| 37 | 2 — <code>grep -c ' launch mado round=37 pgid='</code> | 1 — <code>grep -c ' lane-dead-no-report mado round=37;'</code> | 1 — <code>grep -c ' complete mado round=37;'</code> | `2026-10-25T09:35:45-03:00` | 3h30m06s |
| 38 | 1 — <code>grep -c ' launch mado round=38 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=38;'</code> | 1 — <code>grep -c ' complete mado round=38;'</code> | `2026-10-25T12:49:09-03:00` | 2h09m56s |
| 39 | 1 — <code>grep -c ' launch mado round=39 pgid='</code> | 0 — <code>grep -c ' lane-dead-no-report mado round=39;'</code> | 1 — <code>grep -c ' complete mado round=39;'</code> | `2026-10-25T17:15:05-03:00` | 1h18m49s |
| **32–39** | **10** — <code>grep -c -E ' launch mado round=3[2-9] pgid='</code> | **2** — <code>grep -c -E ' lane-dead-no-report mado round=3[2-9];'</code> | **8** — <code>grep -c -E ' complete mado round=3[2-9];'</code> | — | — |

All commands run with cwd `/home/vgpnk/Projects/shokunin`. Elapsed = `complete` timestamp minus the
**first** `launch` timestamp of the same round (both from the lines quoted in §D), computed by the
script in §F; it therefore includes any dead-attempt span.

### A2. Per-attempt spans for the two multi-attempt rounds (same script, §F)

| round | launch | → event | span |
|---|---|---|---|
| 35 | `2026-10-24T23:14:38-03:00` (attempt 1) | `lane-dead-no-report` `2026-10-25T03:23:08-03:00` | 4h08m30s |
| 35 | `2026-10-25T03:23:08-03:00` (dead) | launch attempt 2 `2026-10-25T03:23:38-03:00` | 30s |
| 35 | `2026-10-25T03:23:38-03:00` (attempt 2) | `complete` `2026-10-25T03:53:57-03:00` | 30m19s |
| 37 | `2026-10-25T06:05:39-03:00` (attempt 1) | `lane-dead-no-report` `2026-10-25T06:46:34-03:00` | 40m55s |
| 37 | `2026-10-25T06:46:34-03:00` (dead) | launch attempt 2 `2026-10-25T08:50:16-03:00` | 2h03m42s |
| 37 | `2026-10-25T08:50:16-03:00` (attempt 2) | `complete` `2026-10-25T09:35:45-03:00` | 45m29s |

## B. Does the round-N spot-check name leftover working-tree files?

Mention count (uniform regex, §E command `M`): `grep -c -E 'untracked=[1-9]|Uncommitted (paths|round work)|uncommitted round (work|artifact)|left uncommitted' corpus/lessons/round-NN-verifier-spotcheck.md`.
The count is a **phrase-mention** count, not a verdict: it also matches a line that says *no* such
work (r37, r39). The yes/no below is read off the quoted line; the fixed-string grep proves the
quoted line is present verbatim (`grep -F -c '<fragment>'` → 1 in all 8 rows).

| round | names leftover working-tree files? | mention count (cmd M) | quoted line (file:line) | decisive fragment — <code>grep -F -c</code> = 1 |
|---|---|---|---|---|
| 32 | **yes** — 5 paths, stated as round-30 leftovers | 2 | `corpus/lessons/round-32-verifier-spotcheck.md:18` (also `:84`) | `Five uncommitted round-30 leftovers in the lane repo at closure` |
| 33 | **yes** — `untracked=19` | 2 | `corpus/lessons/round-33-verifier-spotcheck.md:19` (also `:23`) | `## Uncommitted paths (19) — classified, not edited` |
| 34 | **no** — `untracked=0`, porcelain empty | 0 | `corpus/lessons/round-34-verifier-spotcheck.md:43` | `PASS on push and on leftovers.` |
| 35 | **yes** — `tracked=8 untracked=2` | 3 | `corpus/lessons/round-35-verifier-spotcheck.md:47` | `eight modified` |
| 36 | **yes** — 1 untracked seat report | 2 | `corpus/lessons/round-36-verifier-spotcheck.md:21` | `a round-36 seat report left uncommitted` |
| 37 | **no** — `untracked=0`, porcelain empty | 1 | `corpus/lessons/round-37-verifier-spotcheck.md:21` | `No uncommitted round work; pushed. OK.` |
| 38 | **yes** — 3 modified seat reports | 1 | `corpus/lessons/round-38-verifier-spotcheck.md:17` | `working tree carries 3 modified seat reports` |
| 39 | **no** — porcelain empty (a reviewer-created `tip:` file was removed, per the same line) | 1 | `corpus/lessons/round-39-verifier-spotcheck.md:17` | `empty at closure` |

### B2. Full quoted spot-check lines (verbatim, in a text block)

Format of each entry below: `- **rNN \`:line\`** — ` + the source line(s). The source line is
copied byte-for-byte between the outer backticks (a source line that itself starts with a backtick
therefore shows two in a row); multi-line quotes are joined with ` / ` and the `:L1-L2` label gives
the exact range. Nothing inside the block was reworded.

```text

- **r32 `:18`** — `- Uncommitted round work: `git status --porcelain` shows 5 paths, all round-30 leftovers (routed defect D7 below) — the driver's `WARN … 5 paths` reproduces. DEFECT (routed), status-neutral.`
- **r32 `:84`** — `7. **Five uncommitted round-30 leftovers in the lane repo at closure** (the driver's WARN, 5 paths): modified `.ufo/waves/round-30/w1/reports/RevRecordsChain.md`, `RevTrendExpansion.md`, `SentScope.md`; untracked `RevTrendDiscernment.md`, `SimplifierC2.md`. Uncommitted round work under the landed-means-committed rule — resolve (commit under the round's entry or revert) next round; not named in the round-32 report. Not touched by this closure.`
- **r33 `:19`** — `- Pushed: `jj-lane.sh state` → `branch=master local=69f72100bee31a60b811f8fbbe7796db883e17b3 remote=69f72100bee31a60b811f8fbbe7796db883e17b3 ahead=0 behind=0 head=detached tracked=0 untracked=19`. `git ls-remote origin refs/heads/master` → the same hash. PASS on push. Untracked leftovers are a conformance defect, classified below, not a push failure.`
- **r33 `:23`** — `## Uncommitted paths (19) — classified, not edited`
- **r34 `:41-43`** — `tracked=0 untracked=0`; `git ls-remote origin refs/heads/master` →` / ``dff394109f3cc3d851309ad7c67dd3b35b46adf2`; `git status --porcelain` is empty` / `and `untracked=0`. PASS on push and on leftovers.` (r34 `:207` names the r33 leftovers as a cross-reference: `The r33 closure named 19 untracked paths: 6 control fixture trees, 12 seat`.)
- **r35 `:46-48`** — ``branch=master local=7a068cbee3b0983230b8fb8467c02e12772832dd remote=7a068cbee3b0983230b8fb8467c02e12772832dd ahead=0 behind=0 head=detached tracked=8 untracked=2`;` / ``git ls-remote origin refs/heads/master` → `7a068cb…`. Push PASS. Cleanliness **FAIL**: eight` / `modified and two untracked round-35 paths stood in the tree at closure, with mtimes`
- **r35 `:217-220`** — `- **D2 — uncommitted round work at closure (durability debt).** `jj-lane.sh state` at closure →` / ``tracked=8 untracked=2`; eight modified `.ufo/waves/round-35/w2/reports/*` +` / ``scratch-evidence/RevEntryR12/evidence.txt` and two untracked` / ``.ufo/waves/round-35/scratch/RevQuoteS20{3,5}/count_probe.py`, mtimes `03:53:59`–`04:00:00` — seat`
- **r36 `:21`** — `| Lane pushed, no uncommitted round work | **partial** — `jj-lane.sh state` → `ahead=0 behind=0`, `ls-remote origin refs/heads/master` = `a5aaa09…`; but `git status --porcelain` → `?? .ufo/waves/round-36/w1/reports/DistillerFindings.md` (19,033 B, mtime 05:31), a round-36 seat report left uncommitted while the report's line 379 asserts "working tree clean". Defect R1 |`
- **r37 `:20-21`** — `behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; remote` / ``ls-remote origin refs/heads/master` = `6542248…`. No uncommitted round work; pushed. OK.`
- **r38 `:17`** — `| uncommitted round work | DEFECT — working tree carries 3 modified seat reports (`.ufo/waves/round-38/w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md`, +187/−7) at closure; next round must commit or revert |`
- **r39 `:17`** — `| uncommitted round work | PASS — `git status --porcelain` empty at closure. (Closure-side note: one of this reviewer's own `echo …->tip:` commands created a stray untracked file named `tip:` in the lane repo at 17:15; it was removed before anything was staged. Nothing was committed or moved.) |`

```

## D. Verbatim watchdog lines (the only mado 32–39 lines in the log)

```
1196: 2026-10-24T19:56:38-03:00 launch mado round=32 pgid=1636979 driver=hyaku-inline attempt=1
1203: 2026-10-24T20:33:30-03:00 complete mado round=32; hyaku-inline attempt=1
1210: 2026-10-24T20:58:11-03:00 launch mado round=33 pgid=2254139 driver=hyaku-inline attempt=1
1220: 2026-10-24T21:30:29-03:00 complete mado round=33; hyaku-inline attempt=1
1224: 2026-10-24T21:40:56-03:00 launch mado round=34 pgid=3166550 driver=hyaku-inline attempt=1
1233: 2026-10-24T22:55:29-03:00 complete mado round=34; hyaku-inline attempt=1
1239: 2026-10-24T23:14:38-03:00 launch mado round=35 pgid=29506 driver=hyaku-inline attempt=1
1245: 2026-10-25T03:23:08-03:00 lane-dead-no-report mado round=35; retry same round (hyaku-inline attempt=1: run-6: attempt-1 orphan — no report, session died 2026-10-24 ~23:30 -03)
1254: 2026-10-25T03:23:38-03:00 launch mado round=35 pgid=1756809 driver=hyaku-inline attempt=2
1266: 2026-10-25T03:53:57-03:00 complete mado round=35; hyaku-inline attempt=2
1274: 2026-10-25T04:09:05-03:00 launch mado round=36 pgid=3277229 driver=hyaku-inline attempt=1
1287: 2026-10-25T05:41:00-03:00 complete mado round=36; hyaku-inline attempt=1
1292: 2026-10-25T06:05:39-03:00 launch mado round=37 pgid=1729662 driver=hyaku-inline attempt=1
1303: 2026-10-25T06:46:34-03:00 lane-dead-no-report mado round=37; retry same round (hyaku-inline attempt=1: run-6: L1 returned after 40m with no commits and no report (abandoned mid-round; uncommitted work inherited by next attempt))
1334: 2026-10-25T08:50:16-03:00 launch mado round=37 pgid=819016 driver=hyaku-inline attempt=2
1341: 2026-10-25T09:35:45-03:00 complete mado round=37; hyaku-inline attempt=2
1358: 2026-10-25T10:39:13-03:00 launch mado round=38 pgid=2523589 driver=hyaku-inline attempt=1
1370: 2026-10-25T12:49:09-03:00 complete mado round=38; hyaku-inline attempt=1
1391: 2026-10-25T15:56:16-03:00 launch mado round=39 pgid=3182525 driver=hyaku-inline attempt=1
1404: 2026-10-25T17:15:05-03:00 complete mado round=39; hyaku-inline attempt=1
```

Reproduce with:
`grep -n -E ' launch mado round=3[2-9] | complete mado round=3[2-9];| lane-dead-no-report mado round=3[2-9];' .ufo/watchdog.log` (cwd `/home/vgpnk/Projects/shokunin`, 20 lines).

## E. Commands (all run from `/home/vgpnk/Projects/shokunin` unless noted)

```sh
# per-round watchdog counts (substitute NN = 32..39)
grep -c " launch mado round=NN pgid=" .ufo/watchdog.log
grep -c " lane-dead-no-report mado round=NN;" .ufo/watchdog.log
grep -c " complete mado round=NN;" .ufo/watchdog.log
# slice totals
grep -c -E ' launch mado round=3[2-9] pgid=' .ufo/watchdog.log        # 10
grep -c -E ' lane-dead-no-report mado round=3[2-9];' .ufo/watchdog.log # 2
grep -c -E ' complete mado round=3[2-9];' .ufo/watchdog.log            # 8
# slice completeness (no other verb)
grep -E 'mado round=3[2-9]' .ufo/watchdog.log | grep -vc -E ' launch | complete | lane-dead-no-report '  # 0
# M: spot-check mention count (cwd mado-shokunin, NN = 32..39)
grep -c -E 'untracked=[1-9]|Uncommitted (paths|round work)|uncommitted round (work|artifact)|left uncommitted' \
  corpus/lessons/round-NN-verifier-spotcheck.md
# fixed-string presence of the quoted decisive line (cwd mado-shokunin)
grep -F -c 'Five uncommitted round-30 leftovers in the lane repo at closure' corpus/lessons/round-32-verifier-spotcheck.md
grep -F -c '## Uncommitted paths (19) — classified, not edited'            corpus/lessons/round-33-verifier-spotcheck.md
grep -F -c 'PASS on push and on leftovers.'                                 corpus/lessons/round-34-verifier-spotcheck.md
grep -F -c 'eight modified'                                                 corpus/lessons/round-35-verifier-spotcheck.md
grep -F -c 'a round-36 seat report left uncommitted'                        corpus/lessons/round-36-verifier-spotcheck.md
grep -F -c 'No uncommitted round work; pushed. OK.'                         corpus/lessons/round-37-verifier-spotcheck.md
grep -F -c 'working tree carries 3 modified seat reports'                   corpus/lessons/round-38-verifier-spotcheck.md
grep -F -c 'empty at closure'                                               corpus/lessons/round-39-verifier-spotcheck.md
```

## F. Elapsed-time script (the source of every duration above)

```sh
cd /home/vgpnk/Projects/shokunin && python3 - <<'PY'
import re, datetime
pat = re.compile(r'^(\S+) (launch|complete|lane-dead-no-report) mado round=(\d+)')
ev = {}
for ln in open('.ufo/watchdog.log', encoding='utf-8'):
    m = pat.match(ln)
    if m and 32 <= int(m.group(3)) <= 39:
        ev.setdefault(int(m.group(3)), []).append((m.group(1), m.group(2)))
t = lambda s: datetime.datetime.fromisoformat(s)
for r in sorted(ev):
    rows = ev[r]
    lau = [x for x in rows if x[1] == 'launch']
    dead = [x for x in rows if x[1] == 'lane-dead-no-report']
    comp = [x for x in rows if x[1] == 'complete']
    print(f"r{r} launches={len(lau)} dead={len(dead)} complete={len(comp)} "
          f"first={lau[0][0]} complete_at={comp[-1][0]} elapsed={t(comp[-1][0]) - t(lau[0][0])}")
    for i in range(len(rows) - 1):
        print(f"   {rows[i][1]}@{rows[i][0]} -> {rows[i+1][1]}@{rows[i+1][0]} span={t(rows[i+1][0]) - t(rows[i][0])}")
PY
```

## G. Method notes (no interpretation added)

- All timestamps are verbatim `-03:00` offsets; durations are naive differences of two same-offset
  timestamps from §D, so the offset cancels.
- Rounds 35 and 37 are the only rows with `lane-dead-no-report`; their row elapsed (§A) spans the
  dead attempt plus the retry, and §A2 splits it per attempt from the same lines.
- The §B mention count and the yes/no are different measurements: the count is `grep -c` of a phrase
  regex over the whole spot-check file (so a negating line still counts); the yes/no is read off the
  quoted line and pinned by the fixed-string `grep -F -c` = 1. Both are given so neither is taken for
  the other.
- No claim, gate, counter or axis is referenced here; nothing in this table was scored.
