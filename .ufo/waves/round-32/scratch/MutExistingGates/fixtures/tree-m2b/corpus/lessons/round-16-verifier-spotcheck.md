author: hyaku closure (non-author integrator, @m_opus)

# Mado round 16 — independent closure: admitted

Date: 2026-10-20. Non-author integrator of record for lane-round mado r16
(hyaku campaign, phase 2 closure debt). I did not author this round, did not
execute any lane gate, and edited no lane-authored file. Pre-round lane HEAD
`32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`; post-round lane HEAD
`4bfb2363afd6e05d079127d8f91e57f01bbdca92`. Report
`.ufo/reports/round-16/mado.md` (fleet repo). Lane LOG entries: LOG.md
§"2026-10-20 — round 16: source-only learning after rejected-harmed closure",
§"Round-16 verification correction — M6", §"Round-16 final evidence and handoff".

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```text
2026-10-20T05:35:42-03:00 launch mado round=16 pgid=3021226 driver=hyaku-inline attempt=1
2026-10-20T06:06:30-03:00 complete mado round=16; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %ae %H %s' -- .ufo/reports/round-16/mado.md` (fleet) | `mado-shokunin mado@shokunin.local cd4c0eac41803183fb245569bfa47e8794d8c63b round-16: mado report` | ok |
| Prompt committed | same, `.ufo/prompts/mado-round-16.md` | `mado-shokunin … 67f4e00f0573ec7b639a8b5454e206ae4d698e64 round-16: mado dispatch evidence` | ok |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | ok |
| Cited commits exist and are ancestors | `git cat-file -t` + `git merge-base --is-ancestor <h> HEAD` for `9dcf2489…`, `1e31681e…`, `4bfb2363…` | `commit` + `anc-ok` ×3 | ok |
| Round commits carry lane identity | `git log --format='%an %ae %h %s' 32c4fda..HEAD` | 3 commits, all `mado-shokunin mado@shokunin.local` | ok |
| No uncommitted round work, pushed | `git status --porcelain`; `git rev-list --count @{u}..HEAD` | empty; `0` | ok |
| Prompt carries template contract | grep of prompt: report path (l.101), commit-before-report / cite pushed HEAD (l.240), SHONEN (l.118), write scope (l.226), MISSION/AXES binding + lowest axis (l.5–16), L2 floor ≥8 in one batch (l.80–82), §5 commit/push scope/L0; `diff` vs `templates/round-prompt.md` l.1–140 = 22 changed lines (placeholder renderings) + hyaku addendum §6 | all items present | ok |
| Lane identity of the fleet misroot repair | `sha256sum mado-shokunin/.ufo/waves/round-16/w1/reports/RoundConformance.md` | `ac48edb4…cf67e`, equals the report's claimed digest; HANDOFF.md Incident 3 confirms the fleet copy was copied byte-exact and removed | ok (defect M4 disclosed) |

Status-neutral conformance notes: the report's LOG pointers spell
"round16"/"Round16" where LOG headings read "round 16"/"Round-16" (resolvable,
cosmetic). An operator commit `f898e52` ("considerthese: 2026-10-20 daily
reflection") landed on the lane remote after the round; it is not lane work and
was fast-forwarded before this file was committed.

## Per-claim re-check

**C1 coverage — documented custom-module observation route U7, 6/7 → 7/7.**
Re-measured (plain git/grep, plus the lane's read-only counter for the facet
joins):

```text
$ git grep -hE '^covers: U[0-9]' <rev> -- corpus/knowledge | sort | uniq -c
32c4fda: U1..U6 one each (6)        4bfb236: U1..U7 one each (7)
$ grep -nE '^(covers|## )' corpus/knowledge/waybar-observation-boundaries-r16.md
4:covers: U7 / 13:## Producer contract / 35:## Renderer boundary / 58:## Safe observation / 77:## Unexercised rendering
$ awk '/^## Unexercised rendering/{f=1} f' <note> | grep -c '\[UNK\]'      → 2
$ grep -E '^\| *S05[34] ' corpus/SOURCES.md | grep -c <note path>       → 2 (both mined, tier A)
$ python3 .ufo/waves/round-16/measure.py 32c4fda… | jq .c1.count,.c1.score → 6, 8.5714
$ python3 .ufo/waves/round-16/measure.py 4bfb236… | jq .c1.count,.c1.score → 7, 10.0
```

Matches the reported 6/7 (8.5714) → 7/7 (10.0000). Verdict: **improved**
(finite documentary rubric; now at its ceiling, which the lane itself declares
harm-watch only).

**C2 operability capability — finite declared-kind/12-name action classifier,
absent → demonstrated.** Gate claim: evidence-verified, not executed
(PROTOCOL §Gate standard, Closure consequence).

- Absent at baseline: `git show 32c4fda:tools/mado-action-plan.py` → fatal, path not in revision.
- Revision bytes: `git show 4bfb236:tools/mado-action-plan.py | sha256sum` =
  `226220ae…ba5aea3` = `git show 1e31681:…` = the final receipts' `action_gate_sha256`;
  `9dcf248` bytes = `13d86fb0…dcdb73` = the red receipts' digest.
- Self-test tally: `evidence/action-selftest.json` (measured `9dcf248`) exit 1,
  `SELFTEST_SUMMARY: 51/52 passed failed=['frozen-denied-match']`;
  `evidence/action-selftest-final.json` (measured `1e31681`) exit 0,
  `SELFTEST_SUMMARY: 52/52 passed`, including `frozen-tampered-plan` and
  `frozen-tampered-policy` `want 2/snapshot_tampered got 2/snapshot_tampered`.
- Frozen-run verdict: `evidence/action-frozen.json` exit 2 `frozen_error`
  (red, retained); `evidence/action-frozen-final.json` exit 0 `frozen_match`,
  "frozen verdict denied_executable:sudo/1 matched".
- Committed bindings: every one of the 12 `inputs` digests in
  `evidence/committed-bindings.json` equals `sha256sum` of the same path at
  `4bfb236` (12/12 OK, my loop).
- Controls: `tight-red.json` exit 1 `denied_executable:sudo`; `tight-green.json` exit 0 `plan_safe` ("not permission or safety").
- Registry rows at the lane's registry home: SKILL.md:543 `mado-action-plan`
  and :544 `mado-action-plan-frozen`, with verdict maps and self-test spelling.

Verdict: **improved** (capability only, as the lane itself bounds it). This
is not host recovery and not install prevention.

**C3 calibration — original literal lesson-citation fraction, 12/20 → 14/22.**
Re-measured:

```text
$ git show <rev>:corpus/QUALITY.md | grep -cE '^[0-9]+\. '             → 32c4fda 20, 4bfb236 22
$ git show <rev>:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'   → 32c4fda 12, 4bfb236 14
```

12/20 = 6.0000 → 14/22 = 6.3636, matching the report. C3 is the lowest active
scored axis (`evidence/selection-red.json` exit 1 with lowest=calibration
6.0; `selection-green.json` exit 0 after adding it). The pre-measurement
selection correction is recorded in SCORECARD, not silently swapped. Verdict:
**improved** (placement-sensitive literal rubric, as disclosed).

Owned-axis harm check: `git diff 32c4fda 4bfb236 -- SCORECARD.md` is
append-only (131 insertions, 0 deletions). The only deletions in the round
(`git diff --numstat`) are 2 lines of SKILL.md and 1 of corpus/README.md;
read: they replace present-tense live claims ("waybar v0.15.0 running (PID
1707 …)") with explicitly historical wording plus the new U7 route — stale
marking, not loss. Host window check: `/var/log/pacman.log` has **0** lines
timestamped 2026-10-20T05:35–06:09 (the round window), so no package
transaction occurred during the round. The `pacman -Q waybar` seat query (M5)
is a read-only query, not a transaction; it breached the round's own
source-only scope and is a disclosed process defect, not an axis harm.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | C1 re-measured 6/7 → 7/7 |
| operability | improved | C2 capability evidence-verified; no new host transaction in the round window; R15-V1 harm is round 15's, carried and operator-owned |
| calibration | improved | C3 re-measured 12/20 → 14/22 |
| freshness | unchanged | no fresh live/no-live run; no score change claimed |
| depth | unchanged | unscored, no claim |
| adjacency | unchanged | host recovery routed, not absorbed |

**Carried R15 harm, honesty:** round 16 carried it honestly. The report,
SCORECARD and lesson repeatedly state R15-V1 remains unresolved and
operator-owned, that green gates are not no-harm clearance, that the round
"does not readmit round15", and they add no L0 duplicate or remediation.
R15-V2 landed as QUALITY21 (the real-plan/installed-name comparison retained
as a necessary-not-sufficient condition after an operator lift) and SKILL
pause/no-live instructions. This closure does not resolve R15-V1.

## Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-16.md` §Gate.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| U7 documentary route from S053/S054 | admit | `curl` of S053 `waybar-custom.5.scd` @0.15.0 (sha256 `efb6a63a…2de30d82`, = recorded) and S054 `custom.cpp` @0.15.0 (sha256 `2232f7f7…3b291f`, = recorded) | agree | Both raw digests match `SOURCES.md`; the manual defines the producer contract and the code shows parse → format → hide/`set_markup`, which is exactly what the note claims and no more. |
| Producer output as proof of rendered text | reject | S054 `custom.cpp` lines 174–181 (`fmt::format(…)`, `hide-empty-text`/`str.empty()` → `event_box_.hide()`, else `label_.set_markup(str)`) | agree | Producer text is reformatted, may hide the module, and is then GTK-markup parsed; producer output cannot establish visible text. |
| Tagged source as installed-binary equivalence | reject | same raw tag sources; nothing built or compared to the host binary | agree | A tag's source digest says nothing about the packaged binary. |

SOURCES row re-opened: **S053**, quote in lesson §Gate "The *custom* module
displays either the output of a script or static text." — `sed -n 8p` of the
fetched raw file returns that exact line; 13 words (≤25). S054's one-token
quote `label_.set_markup(str);` is at raw line 181 as stated.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
→ exit 0; output identical to the report's before/after (W04 S030/S042/S045
duplicate-url warnings, `mado ok …/corpus/SOURCES.md`). Row count 52 → 55
re-counted (`grep -cE '^\| *S[0-9]{3}'`).

## Trend verdicts

- **Expansion: improved.** New admitted knowledge entry on uncovered ground
  (U7) citing two mined A rows, plus a capability admitted to SCORECARD.
- **Quality: improved.** Stale present-tense Waybar claims in SKILL/README
  re-marked historical; QUALITY21 supersedes criterion 20's install route
  while paused; red→green M6 correction kept both receipts; no admitted entry
  failed my re-check (sources, digests, quotes, counts all reproduced).
- **Discernment: improved.** This non-author sample agrees with the gate on
  one admit and two rejects.

## Routed defects (mado, next authorized round)

- **R16-V1 (evidence labeling):** report ("Tampered frozen input returns2
  `snapshot_tampered`") and lesson round-16 l.131 cite
  `evidence/frozen-tampered.json` as showing `snapshot_tampered`, but that
  receipt was measured at `9dcf248` and records exit 2 `frozen_error`
  ("expected.json pair 1/'denied_executable:sudo' is unreachable") — the
  pair defect fired before any digest check. `snapshot_tampered` is evidenced
  only by the final self-test fixtures. Append a correction naming the
  superseded text; optionally re-receipt the tamper control at the corrected
  content. Status-neutral: C2 rests on 52/52 + frozen_match.
- **R16-V2 (process):** M4 fleet misroot and M5 `pacman -Q` during a
  source-only round are disclosed; keep the pause/no-query instruction in
  every seat context until the operator lifts it.
- **R15-V1 (carried, operator-owned):** libinput partial-upgrade decision
  stays on the existing L0 line; no lane action.

SHONEN: four `[~]` author assertions; box 2 rests on a historical round-3
task and no box carries a non-author verification. Not judged promotion-ready
by this closure; promotion remains operator-owned. No tools were installed or
updated by this closure.

Admission: every claim verifies (C1, C3 re-measured; C2 evidence-verified)
and no axis is harmed by round 16 → **admitted**.
