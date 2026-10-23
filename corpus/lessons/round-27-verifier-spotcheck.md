author: hyaku closure (non-author integrator, @m_flash)

# mado round 27 — non-author verifier spot-check (hyaku run-5 closure)

Round: mado lane-round 27, attempt 2. Lane base `543f0445e9d60bdfa026c54772d29e8b96bc844b`; lane tip at
closure `767b12db62ceb3ad38d24a13e4c693b4375ceb5a` (branch `master`). Report
`.ufo/reports/round-27/mado.md`, fleet commit `9f966367582294f8037be224810a3935f58ff954`, author
`mado-shokunin <mado@shokunin.local>`. This file is the outside discernment check required by
`LEARNING.md`; the lane authored neither the round nor this file. Verified 2026-10-23 (closure pass).

Driver digest this closure rests on (from `.ufo/watchdog.log`, mutable; lines 914/931/943 still carry the
first three at closure):

```
2026-10-23T07:15:52-03:00 launch mado round=27 pgid=4176664 driver=hyaku-inline attempt=1
2026-10-23T15:03:19-03:00 lane-dead-no-report mado round=27; retry same round (attempt=1: superseded ... fresh attempt)
2026-10-23T15:10:22-03:00 launch mado round=27 pgid=92816 driver=hyaku-inline attempt=2
2026-10-23T19:05Z complete mado round=27 (attempt 2, in-session L1); lane HEAD 767b12db..., report commit 9f966367...
```
Note: the live log carried no `complete mado round=27` line at closure (only the launch and lane-dead
lines); the orchestration digest above is the completion record, and the landed report is the completion
evidence.

## 1. Step-1 conformance

| item | command | observed | verdict |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-27/mado.md` (fleet) | `mado-shokunin 9f966367582294f8037be224810a3935f58ff954`; ancestor of pushed fleet HEAD `0fdce71a` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` | 4 lines, `[~]` each, one per `SHONEN.md` box; no `[x]` | pass |
| cited lane commits exist and are ancestors | `git merge-base --is-ancestor <h> master` over `767b12db 20022a65 0b53bd86 48b9434a 5c1d495 86f7355 0be82d62 43fdd7e6 cb7c38f0 98ebd5b0 b6650d5` | 11/11 `OK` | pass |
| no uncommitted round work | `git -C mado-shokunin status --porcelain` | empty | pass |
| pushed | `scripts/hyaku/jj-lane.sh state mado-shokunin` | `branch=master local=767b12db remote=767b12db ahead=0 behind=0 tracked=0 untracked=0` | pass |
| prompt carries the template contract | `.ufo/prompts/mado-round-27.md` §1–§5 | round-level (i) MISSION/AXES §1, (ii) L2 floor ≥8 one batched call §3, (iii) commit-then-push §5, (iv) push scope §5, (v) L0 §5; child-lane report path §4, commit-before-report §5, `SHONEN` heading §4, hash-citation rule §5, write scope §3. No L2 route map is quoted, so the route-map check is vacuous | pass |
| report is real, not a marker | checkable commit + evidence pointers + required sections | real report → lane-round status `ok`; defects below are status-neutral | pass |

Conformance defects recorded in this round's notes (none changes `ok`):

1. `SKILL.md:630-635` — the three r27 gate registry rows are stale draft placeholders: `mado-r27-… — lands
   this round, pending`, "Pending implementation pins", "R27 suite source and results are not present in the
   draft-time quality directory". The suites landed at `5c1d495` and the repair at `0b53bd86`; the rows were
   never finalised (`86f7355` committed them as-is). Gate standard §Delivery: r27 gates are not
   registry-conformant.
2. `corpus/lessons/round-27.md:14` (M27-2) — dead evidence pointer and stale claim: `corpus/SOURCES.md:195-199`
   holds the Paths section at every committed revision; no commit carried the malformed two-cell rows
   (`awk … NF!=13` = 0 at `5c1d495`, `b6650d5`, `86f7355`, `0be82d6`, `767b12db`). The fix cell still says
   "the current registry snapshot still contains them … removal and green revalidation remain pending L1",
   false at its own commit and at tip (census clean, rows valid). Needs an appended correction in r28.
3. Red-before receipt missing for the E01 fix. `evidence/sources-start.txt` is a clean 177-row run (`ok`,
   exit 0); the described E01/E11 failure was observed over attempt-1's uncommitted worktree and never
   committed. `CORPUS.md` "A fix is shown able to fail before it counts" is therefore unsatisfied for this fix.
4. Report dead pointer: `quality/q36-successor-receipts.txt` does not resolve; the file is
   `.ufo/waves/round-27/quality/q36-successor-receipts.txt` (`ls quality/` holds only the three scripts).
5. Report harm-watch absence claim is false: `git diff --stat 543f0445 -- tools/` also touches
   `tools/mado-binds.py` (docstring-only, +6 lines, `b6650d5`), not only the new `tools/mado-wsrules.py`.
6. Report says "the tool's docstring and the knowledge entry cite them [S178–S182]": the docstring cites the
   upstream source files (`WorkspaceRuleManager.cpp`, `ParserUtils.cpp`, …), not `S###` ids; only the knowledge
   entry cites the rows (frontmatter `source:` list).
7. Registration says "one measurement" / "the single C2 measurement" (`.ufo/waves/round-27/registration.md:50,72`)
   and contains no repair-flow section, but the round ran two C2 measurements (miss at `48b9434a`, repair at
   `0b53bd86`). The repair used the pre-declared first-returned data rule and the same frozen counter/predicate,
   so the claim is not a rule change — but the flow must be registered before data next time.
8. Round shape says w3 was 8 seats; 7 w3 seat reports are committed (`CritC1Claim, CritC2Claim, ExecWsToolC,
   MutWsTool, RevProvenance, RevSourcesFinal, RevSpotcheckDebt`) and 7 names appear in the report. The eighth
   seat or its death is unnamed.
9. Report cites `SKILL.md:631-636`; the six rows sit at `630-635` at tip (pointer drift).

## 2. Per-claim re-check (C1, C2)

Reported values were re-derived from committed bytes; where a claim rests on a lane-owned gate/counter, its
committed receipt was verified (counter/tool/subject digests, revision, verdict line, exit code) and the gate
itself was **not** executed, per PROTOCOL §Gate standard. No `/fast/scratch` input was opened; the sealed H
directory was not read.

### C1 — coverage (sourced): workspace-rule table from config bytes

| check | command | observed |
|---|---|---|
| tool absent at base | `git cat-file -e 543f0445:tools/mado-wsrules.py` | fatal, path not in `543f0445` (absent) |
| tool bytes at after-rev | `git show 20022a65:tools/mado-wsrules.py \| sha256sum` | `dcf5c8c05b2d5b68ef967df339f7539a762e56c8a3811d7fbef33db9936ca389` = receipt `tool=…@20022a652d20 sha256:` |
| counter pin | `sha256sum .ufo/waves/round-27/c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` = registration §v4 pin = receipt header |
| before receipt | `evidence/c1v4-before-543f0445.txt` | 41 `CASE` lines, 41 `FAIL`, `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED`, `exit=1`, seed `c5e1bb78d20a58eb` |
| after receipt | `evidence/c1-after-20022a65.txt` | 41 `CASE` lines, 41 ` PASS `, `PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET`, `exit=0`, seed `4cfdf858277ad362`, `HOST_SAFETY … delta=0` |
| controls | `controls/v4/*.txt` | 13 shapes × 2 seeds (+3 L1 pilots) = 29 receipts, all under counter v4 pin; best `K1FileScope-seed2` 32/41 < 41 |
| unmoved demonstration | receipt pairs | base rows read `tool absent`; control shapes miss 9–32 of 41 |
| sourced | `corpus/knowledge/workspace-rules-r27.md` frontmatter | `source: S178 S179 S180 S181 S182 S158 S162`; `verified-at: 20022a65`; SOURCES rows `mined`, used-by paths exist |
| report value | 41/41, seed, exit 0, measured commit | matches |

Verdict: **verified**. (Evidence-verified gate run; counts re-derived line-by-line from the committed
receipt. The report's "start exit 1" belongs to the frontier census, not C1, and is covered in §1 defect 3.)

### C2 — operability: the two offline gates fail when their subjects are broken

| check | command | observed |
|---|---|---|
| suites absent at base | `git cat-file -e 543f0445:quality/{counter-selftest,population-suite}.py` | both absent |
| suite bytes at measurement 1 | `git show 48b9434a:quality/… \| sha256sum` | A `7fd94b04…`, B `99e7d876…` = `c2-after-48b9434a.txt` header |
| suite bytes at measurement 2 | `git show 0b53bd86:quality/counter-selftest.py \| sha256sum`; tip `sha256sum` | A `aa0e14d1…` = ExecRepairA2 candidate sha (landed unmodified); B `99e7d876…` unchanged; no quality/ change after `0b53bd86` |
| subject pins | `git show 0b53bd86:.ufo/waves/round-26/{c1/count-v2.py,c2/count.py,quality/check-population.py} \| sha256sum` | `4ed70b54…`, `b92c32da…`, `803e0096…` = receipt `SUBJECT` lines |
| seal | `c2/heldout-seal.txt` vs receipt `HELDOUT_FILE` lines | 6/6 digests equal, every line `seal=match` |
| measurement 1 | `evidence/c2-after-48b9434a.txt` | 17 `GREEN … PASS`, 15 `W … KILLED`, 12 `H … KILLED` / 3 `SURVIVED`; `PRED-C2-r27-v2 … h_killed=12/18 h_need=14 … verdict=TARGET_MISSED`, `exit=1` |
| measurement 2 | `evidence/c2-after-0b53bd86.txt` | 17 `GREEN … PASS`, 15 `W … KILLED`, 15 `H … KILLED` / 3 `SURVIVED`; `PRED-C2-r27-v2 green=17/17 b_valid=9 w_killed=15/15 h_killed=15/18 h_need=14 h_valid=18 … invalid=0 verdict=TARGET_MET`, `exit=0` |
| repair provenance | `w4/reports/{ExecRepairA2,RevRepair,MutSuiteB}.md` | A2 candidate sha = landed file; RevRepair: sealed dir never read, both candidates pass required axes; MutSuiteB: 3 fresh suite-B mutants killed, 46/46 greens |
| report values | 15/15 W, 15/18 H ≥ 14, exit 0 | matches |

Verdict: **verified**, with the registry defect §1.1 (the two new gates declare no self-test mode / stable
finding id; their red/green is external through `c2/count-v2.py`). Gate-standard conformance is routed, not
granted.

## 3. No-harm check and per-axis verdicts

Base→tip lane surfaces: `M LOG.md`, `M PROVINCE.md` (+9 append-only correction), `M SCORECARD.md` (+24/−1:
one r26 citation fix + the r27 section), `M SKILL.md` (+6 registry rows), `M corpus/SOURCES.md` (+5 rows,
used-by), `A` knowledge note, lesson, `tools/mado-wsrules.py`, `quality/{counter-selftest,population-suite,
check-control-receipts}.py`; `M tools/mado-binds.py` is a docstring-only environment-limit note. `git diff
--name-status` contains no `D` records. Own census: rows 177→182, malformed 0, duplicate ids none, enum
violations none, mined used-by paths all exist. No owned axis is harmed.

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | new measured surface with a running tool (41/41 at `20022a65`) on ground that held only verb mentions at base; 5 new A-tier rows, all `mined`; 13 controls best 32/41 |
| operability | improved | two gates land and demonstrate red on broken subjects: 15/15 W and 15/18 H killed (need 14) at `0b53bd86`, green 17/17; registry rows not yet conformant (§1.1) |
| depth | unchanged | no depth claim this round; the note's schema section serves C1, not a separate move |
| freshness | unchanged | sources opened/rechecked 2026-10-23; no stale-claim repair claimed beyond r26 debt |
| calibration | unchanged | SHONEN stays 4×`[~]`; report overstatements §1.4–1.6 are recorded, not counted as a move |
| adjacency | unchanged | no cross-domain absorption; no contested scope reported |

## 4. Discernment spot-check (outside, non-author)

The lesson's `## Gate` records five admits and **no source-level reject** (its sweep says no candidate was
rejected as a duplicate). The reject sample is therefore drawn from the round's rule-retirement gate decisions,
which are the round's other gate decisions with committed receipts.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S178 Hyprland wiki Workspace-Rules | admit (A) | `raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md` re-fetched 2026-10-23: 4786 B, sha256 `486143a0…ab62` = row digest; quote `workspace selectors can only match _existing_ workspaces.` at line 47 (7 words) | agree | quote verbatim at the anchored line, digest matches the row, A-tier for the documented selector scope |
| S179 WorkspaceRuleManager.cpp | admit (A) | re-fetched at `efb50993`: 2672 B, sha256 `06e8dcba…2d10`; `mergedRule.mergeLeft(*rule);` at line 45 | agree | located quote inside the anchored range `:34-52`, digest matches, primary source |
| S180/S181/S182 (CCssGapData / parseInt / MiscFunctions) | admit (A) | re-fetched all three: 6116/5902/29785 B with row digests; quotes at lines 84/138/506 inside the anchored ranges | agree | all three quotes ≤10 words, verbatim, digests match |
| C1 counter v1 retired | reject (rule) | `controls/K1FlatScan-v1-seed{1,2}.txt` | agree | both seeds `PRED-C1-r27 cases_pass=41/41 verdict=TARGET_MET`, exit 0 — a partial reader met v1 before data, so retirement was forced |
| C1 counter v2 retired | reject (rule) | `controls/v2/K1PrefixKeyed-seed{1,2}.txt` | agree | both seeds `PRED-C1-r27-v2 cases_pass=41/41`, exit 0; label-keyed shortcut met v2 |
| C1 counter v3 retired | reject (rule) | `controls/v3/K1{GlobalOnce,FileScope}-seed{1,2}.txt` | agree | four receipts all `PRED-C1-r27-v3 cases_pass=41/41`, exit 0; label-free partial readers met v3 |
| E01 malformed S178–S182 rows | reject (gate) | my own census run + `awk NF!=13` over `5c1d495…767b12db` | agree with the rejection, **disagree with its evidence** | the rows were worktree-only (no commit contains them), so the rejection was right but its red-before output was never committed (§1.2–1.3) |

Census re-run (the round's end value): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin mado` → seven `W04` duplicate-url warnings (the same set as
`evidence/sources-end.txt`) then `mado ok …/corpus/SOURCES.md`, `exit=0`.

## 5. Trend verdicts

- **expansion — improved.** 177→182 rows with five mined A-tier sources and a new knowledge entry
  (`corpus/knowledge/workspace-rules-r27.md`) on ground the coverage map did not hold (base `git grep
  "workspacerules\|workspace rule" … -- tools corpus/knowledge` finds verb mentions only); every new row is
  cited by the entry's `source:` list and by `used-by`.
- **quality — improved.** Static `[INF]` schema limits are superseded by a measurement-status section at
  `20022a65`; the r26 population sentence is repaired with `evidence/r26-population-after.txt` and a
  hidden-dependency probe; two offline suites land and are measured red on 15 W / 15-of-18 H. Caveat: the r27
  registry rows are stale at landing (§1.1), so discoverability is overstated.
- **discernment — improved.** Three pre-data redesigns under the kill rule, each forced by a committed
  two-seed control receipt (FlatScan→v2, PrefixKeyed→v3, GlobalOnce+FileScope→v4), the first-returned landing
  rule exercised (A2 landed though RevRepair later found A1 wider), and the E01 format fix. Caveats: the Gate
  records no source-level reject, and M27-2's text/pointer are stale (§1.2–1.3).

## 6. Routed defects the lane must fix next round

1. Finalise the three r27 `SKILL.md` registry rows: landed entry command, verdict map, self-test spelling and
   stable finding id (or register the suites as probes), pinned-value path, write scope, owner. Drop "pending"
   and the "not present in the draft-time quality directory" sentence (§1.1).
2. Append a correction to lesson M27-2 (r28 lesson) naming the superseded text: the malformed rows exist in no
   commit, and the tip registry is valid and green. Do not rewrite the filed lesson (§1.2).
3. Commit a red-before receipt for the E01 fix or record the worktree-state evidence; a green start receipt
   alone does not show the fix able to fail (§1.3).
4. Fix the report's dead Q36 pointer (actual path `.ufo/waves/round-27/quality/q36-successor-receipts.txt`) in
   the next report/erratum (§1.4).
5. Correct the harm-watch absence claim: `tools/mado-binds.py` also changed (docstring-only at `b6650d5`), and
   the registry rows sit at `SKILL.md:630-635` (§1.5, §1.9).
6. Narrow the sourced-claim sentence: the tool docstring cites upstream files; the `S###` citation lives in the
   knowledge entry (§1.6).
7. Register the C2 repair flow before data next round (who repairs, from which public information, how many
   re-measurements, selection rule) and reconcile it with "one measurement" (§1.7).
8. Account for the w3 seat count: name the eighth seat or its death with its last error text (§1.8).
9. r28 C2 work (from w4 RevRepair, relayed by the orchestrator): the exact-≥3 tolerance disjuncts
   (`or nm == 3`, `or ne == 3`) survive both repair candidates — one surviving HeldC2 class leaves zero slack;
   and A1 (`e36f12f2…`) was empirically wider than the landed A2 (`aa0e14d1…`) while the first-returned rule
   landed A2. Carry both as r28 defects, not r27 conformance failures.
10. Keep the `quality/check-control-receipts.py` successor's receipts path in the registry row consistent with
    the committed file (`.ufo/waves/round-27/quality/q36-successor-receipts.txt`).

## 7. Closure recommendation

Every declared claim verifies against `767b12db…` and no owned axis is harmed; the lane-round is `ok` and
admitted, with the routed defects above. SHONEN boxes remain `[~]` (promotion is operator-owned; nothing here
supports `[x]`).
