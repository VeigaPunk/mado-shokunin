# RevSpotcheckRouting — routing is complete for 11 of 13 checked items; 2 disposition gaps (F17 unowned; R18-V2's committed-receipt fix absent from the declared text) and 1 minor gap (the '14/31' wording note), each with a recommendation

Seat: MadoR19.RevSpotcheckRouting. Date: 2026-10-20. Lane `mado-shokunin`,
baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, pre-registration
`17661e0fa83f978fb659f5bb8fef47f0969f6945`. Scope: does every routed item in
`corpus/lessons/round-18-verifier-spotcheck.md` §6 (R18-V1..V4, line anchors
117–120; item 5's carried list, line 121) and the closure's note about the
round-18 report's '14/31' wording (line 73) have a planned disposition in
`SCORECARD.md` `## Round 19 — declared claims` (SCORECARD.md:1059–1120)?

Pre-registration integrity checked first: `git merge-base --is-ancestor
9c54c56… 17661e0` → ok; `git show 17661e0:SCORECARD.md` contains the section at
line 1059 (commit subject "round-19: pre-registration (claims C1-C3, sub-axis
rubrics, baselines, counters)").

## Disposition matrix

| Routed item | Lesson anchor | SCORECARD R19 anchor | Status |
|---|---|---|---|
| R18-V1 S094 per-fetch HTML digests | `lessons/round-18-verifier-spotcheck.md:117` | C1 (SCORECARD.md:1092) + non-claim repair "S094 superseding row" (:1115; reserved S097) | **covered** |
| R18-V2 criterion 26 headerless red-before receipt | `:118` | C1 routes it into lessons + QUALITY criteria (:1094–1096); the receipt commitment itself is **not named anywhere** in 1059–1120 | **partial gap** (see G1) |
| R18-V3 stale walker pins, no in-file pointer | `:119` | C2 re-anchors the fixed 13-file set (:1099–1104) under the fresh-pins rubric (:1080–1084) | **covered** |
| R18-V4 S084 unpinned docs.rs `latest` | `:120` | C1 (:1093) + non-claim repair "S084 re-point" (:1115; reserved S098) | **covered** |
| Carried frozen F1 (blank-line pin reads verdict mismatch) | `:121` | non-claim repairs "frozen F1/F2" (:1116) | **covered** |
| Carried frozen F2 (`link/.` bypasses symlinked-dir check) | `:121` | same (:1116) | **covered** |
| Carried `measure-mutants.py` default `--out` into the lane | `:121` | non-claim repairs (:1116–1117) | **covered** |
| jj-audit F6 (tag row UNKNOWN + false FAIL after detach) | `:121` | "gate F6 (tip instead of `HEAD`)" (:1117) | **covered** |
| jj-audit F9 (`.git`-is-a-dir precondition misses worktrees) | `:121` | "F9 (`rev-parse --git-dir`)" (:1117) | **covered** |
| jj-audit F16 (no landedness check) | carried per goal context, not in lesson item 5 | "a landedness check (F16)" (:1117–1118) | **covered** |
| jj-audit F17 (colocated repo + non-helper `jj` runs) | carried per goal context | named **only** in the carry-list preamble (:1063); no claim, repair, or lesson routing | **gap** (see G2) |
| Three tripwire drafts (TwMissBashCVar / TwMissHelperFn / TwInstallerChannels) | `:121` | C3 apply-or-reject, rebased on the `c1ae45a7…` tool, suites all-pass, re-pin frozen baseline (:1105–1111) | **covered** |
| Closure note on the report's 'fails 14/31' wording | `:73` | absent from 1059–1120 | **gap, minor** (see G3) |

Grounding re-verified this session (all read-only):
- The C2 denominator is real: 13 owned files at `9c54c56` contain `2.17.0`
  (`git ls-tree -r --name-only 9c54c56 -- corpus SKILL.md PROVINCE.md tools`
  filtered to the declared owned set, `git show <rev>:<f> | grep -q '2\.17\.0'`):
  SKILL.md, corpus/README.md, corpus/knowledge/{arc-synthesis, closeout-r11,
  config-health-report-r3, remaining-planes-census, walker-deep, walker-deep-r9,
  walker-live-surface, walker-route-r18, waybar-walker-plane,
  waybar-walker-semantics}.md, tools/mado-verify.sh. 13 − 2 already-current
  (fresh-pins before 2/13, :1084) = the lesson's "eleven owned files … with no
  in-file pointer" — consistent.
- The C3 tool premise is real: `git show 9c54c56:tools/mado-tripwire.py |
  sha256sum` → `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`,
  the sha C3 names (:1108).
- The three drafts exist: `.ufo/waves/round-18/drafts/{TwInstallerChannels,
  TwMissBashCVar,TwMissHelperFn}.patch`.
- The R18-V2 premise is real: `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt`
  line 1 is `# gate-rc-redbefore — jj-w1 F10/F14 red-before receipt (round 18,
  GateRcFix)` — a comment, not the `RECEIPT … tool_sha256=… measured_commit=…`
  producer header.
- The '14/31' wording lives in the **fleet** repo report
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/mado.md:65` ("frozen
  suite 31/31 (the `abfbf35` tool fails 14/31)"); the pass-count convention
  lives at SCORECARD.md:998 ("the `abfbf35` tool 17/31"). The path does not
  exist in the lane worktree or `refs/heads/master` — the closure's "(fleet)"
  tag at `lessons/round-18-verifier-spotcheck.md` §1 is accurate.
- `F17` appears exactly once in SCORECARD.md (:1063), with no disposition.

## Gaps and recommendations

### G1 — R18-V2's routed fix (commit a header-bound receipt of the swapped-block run) is absent from the declared text — recommend: fix this round, one appended line

C1 routes R18-V2 into `lessons/round-19.md` mistakes + QUALITY criteria
(:1094–1096), i.e. it documents the defect and adds a red check, but the routed
fix itself — "Commit a header-bound receipt (`tool_sha256`, `measured_commit`)
of the swapped-block run" (`:118`) — appears nowhere in 1059–1120, not even in
the non-claim repairs list (:1114–1118). Without it, the new criterion's green
state has no declared artifact and criterion 26's own evidence stays headerless.

Execution already exists at wave level: `w1/reports/GateSwapReceipt.md` built a
byte-pinned swapped fixture (`.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh`,
sha `6e6782c3…`) with a provisional receipt, explicitly **not credit under
QUALITY 24 until L1 commits the fixture and re-cuts with the committing
revision** (`provisional=0` path proven in a /tmp clone at `3202de3d…`). So this
is a pre-registration completeness gap, not an execution gap. Recommendation:
since `17661e0` is immutable, L1 appends one line at results time (or into the
non-claim repairs of the results section) naming the committed fixture + re-cut
receipt as the R18-V2 fix, and makes it the stated green state of the new
QUALITY criterion.

### G2 — F17 has no owning disposition — recommend: fix this round as a lesson entry plus a named disposition line

The preamble carries "jj-audit F6/F9/F16/F17" (:1063); the claims and repairs
then name F6, F9, F16 — F17 is dropped. It is a real lane incident (non-helper
`jj` runs in the lane post-rule), so silence is the wrong default, and the wave
already produced the content: `w1/reports/JjIncidentScan.md` supersedes the
audit's F17 facts (the audit-era `.jj` was destroyed at 2026-10-20T15:18:07.972Z
and helper-re-created 90 ms later; ≥20 non-helper `jj` invocations, not 3; the
init came from an eval-surface argv list) and states a disposition: colocation
is durable, the enforceable invariants being (a) no non-helper `jj` in the lane,
(b) no direct git write verb after the round-17 cutover, (c) helper `commit`
only on sanctioned paths, (d) `jj-lane.sh state` treated as read.

Recommendation: fix this round — route F17 into `lessons/round-19.md`
`## Mistakes` via C1's lesson list using JjIncidentScan's superseding facts, and
let the results section declare the four invariants (a one-line addition to the
non-claim repairs). Fallback if the lane declines: carry with the explicit
reason "process finding; the standing contract rule is the control", written
down rather than implied — an unnamed carry is the one shape the round forbids.

### G3 — the closure's '14/31' wording note has no disposition — recommend: lesson-only

The closure note (`:73`) already reconciles the two conventions in an admitted
lesson: the report's "fails 14/31" counts failures, SCORECARD's "17/31"
(SCORECARD.md:998) counts passes — consistent. No round work is required;
however, a future reader comparing report:65 with SCORECARD:998 sees an apparent
31 − 14 ≠ 17 contradiction and must re-derive the reconciliation. Cheapest
durable fix if L1 wants one: a one-line append at SCORECARD.md:998 ("17/31 =
passes; the closure report's 'fails 14/31' = failures of the same run").
Recommendation: **lesson-only**, the optional append is polish, not debt.

## Secondary observations (adjacent, same genus as G3)

- GateSwapReceipt §4 shows round-18's prose "383/389, five OM9 failures" omits a
  sixth failure (R10, the fixture self-pin): 383 + 5 ≠ 389. Same
  count-vs-prose family as the 14/31 note; if L1 lands the G3 append, this is
  the second data point supporting a standing "counts are passes unless
  prefixed" convention note. `[INFERENCE]` per GateSwapReceipt itself, the
  round-18 note records only the count, so the omission cannot be confirmed as
  prose error vs. convention.
- The lesson item-5 list and the SCORECARD preamble differ deliberately: the
  preamble upgrades the carry set to include F16/F17 from
  `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`
  (F16 defined at :310–313, F17 at :322–324 of that report). Everything from the
  broader set except F17 has a disposition — the upgrade was executed 5/6.

## Limits

- I checked dispositions in the declared-claims text only; I did not audit
  whether in-flight seat work matches every claim (that is L1's integration
  pass), and I did not open the other 55 wave-1 reports.
- I did not re-run any counter (`fresh-pins.py`, `tw-recall.py`, `measure.py`);
  I verified the denominators' premises (13 files, tool sha, drafts, headerless
  receipt) by direct reads at `9c54c56` only.
- The '14/31' report line is fleet-repo state; I did not check the fleet repo's
  commit history for that file.
- F17's pre-15:18Z op-store evidence is gone per JjIncidentScan; I take its
  transcript-based counts on trust (its method section is detailed and
  internally consistent, but I did not re-parse the transcripts).

## Installs

none.
