# round-31 verifier spot-check

author: hyaku closure (non-author integrator, @m_swe)
round: mado 31 · lane tip `256222890d935212874a09751ff9b7869943c2d7` ·
base `d72243e1fec0f5fd4311ca9c29a2228b33ac348b` (pre-round HEAD); claim base
`274f7355366d38d6e78f641ad62472e68df4686a` (round-30 lane tip; the
post-closure protocol addendum `2db0c44` sits between the two).
Report: `.ufo/reports/round-31/mado.md`; registration frozen `6803a999`;
data `f621e3c0`; wave spec `72021ded`; records `25622288`.

## Step-1 conformance

- Report committed by lane identity: `0096373` + `3186fbe`, both
  `mado-shokunin <mado@shokunin.local>`; `3186fbe` is a named hyaku sweep
  ("L1 returned without committing; attribution defect") that appended the
  SHONEN + Round-shape sections — attribution defect recorded.
- `SHONEN` heading present, one `[~]` line per box, no `[x]` (no named
  non-author verifier — correct).
- Every cited commit exists and `git merge-base --is-ancestor <hash> master`
  holds for `d72243e1`, `274f7355`, `6803a99`, `f621e3c0`, `72021ded`,
  `25622288`.
- `jj-lane.sh state`: `branch=master local=25622288 remote=25622288 ahead=0
  behind=0` — pushed.
- `git status --porcelain`: 3 modified + 2 untracked files, all under
  `.ufo/waves/round-30/w1/reports/` — inherited orchestrator-dispatched seat
  artifacts predating this round, not uncommitted lane round work
  (receipt: `jj state` reports `tracked=3 untracked=2`).
- Dispatched prompt `.ufo/prompts/mado-round-31.md` carries the full round
  contract: mission/axes binding, 1–3 claims + lowest-axis rule, frontier
  step, L2 floor ≥8 one batched swarm, commit-then-push, push scope, L0
  channel, report path, SHONEN heading, commit-hash citation, write scope.
  L2 floor ≥8 confirmed against `MISSION.md` §L2 concurrency.

## Per-claim re-check (all re-run by this integrator over committed bytes)

**C1 — coverage / index-row fidelity** — re-measured.
`cd mado-shokunin && python3 -I quality/check-index-rows.py --rev REV --repo .`
- base `274f7355`: `rows=43 errors=1 warns=3`,
  `ERROR row-cells: knowledge/animation-table-r26.md … 2 cells`, exit 1 ✓
- tip `25622288`: `rows=43 errors=0 warns=3` (3 glob warns, ephemeral
  r12/r24 evidence), exit 0 ✓
- `--selftest`: `MADO_INDEX_ROWS_SELFTEST: 10/10 assertions passed`, exit 0 ✓
Verdict: **improved**. New gate sees the r26 2-cell defect at base and its
repair at tip; the predicate in `registration.md` (selftest 0 + errors=1 at
base + errors=0 at tip) holds verbatim.

**C2 — calibration / resolved-citation counter v2** — re-measured.
`python3 -I .ufo/waves/round-31/c2/count.py REV`
- base: `literal 40/52=0.7692`, `active=40 resolved_active=39=0.9750`,
  `UNRESOLVED criterion 35: id \bM23-7\b absent in section '#mistakes'`,
  `verdict=TARGET_MISSED`, exit 1 ✓
- tip: `literal 42/54=0.7778`, `active=41 resolved_active=41=1.0000`,
  `verdict=TARGET_MET`, exit 0 ✓
Negative controls (`--quality <fixture> --lessons-root <fixture>
--active-min 2`): n1-empty → `UNRESOLVED criterion 1` (empty file), exit 1;
n2-wrongfile → `TARGET_MET` (existence-only; lane-routed residual cheat —
confirmed, not re-admitted); n3-section → `UNRESOLVED` (wrong-section id);
n4-collapse → `FLOOR_VIOLATION active=1 < 2`. All reproduce.
Verdict: **improved**. Criterion 35's cite re-sectioned to
`#final-c1-disposition-…` (verified: `M23-7` row sits under
`### Final C1 disposition` at `lessons/round-23.md:229`, not `## Mistakes`);
rows 53–54 land with resolving lesson anchors.

**C3 — operability / gate robustness** — re-measured.
`python3 -I quality/check-index.py --rev REV --repo .` → `indexed=43/43
missing=0 dangling=0 coverage=10.0000/10` exit 0 at BOTH `274f7355` and
`25622288` (strengthened gate does not regress the honest measurement).
Selftests on the committed script bytes: base revision `9/9 assertions
passed`, tip `12/12 assertions passed` — the 3 new assertions cover the
routed findings (option-shaped rev, symlinked corpus ancestor, `--repo`
under `--root` → SETUP_ERROR).
Verdict: **improved**.

**Harm watch:** `git diff 274f7355 25622288 -- SCORECARD.md` adds only the
round-31 block + 2 capability rows; `tools/`, `corpus/knowledge/`,
`SKILL.md`, `PROVINCE.md`, `corpus/SOURCES.md` byte-unchanged; lane
navigation counter still `43/43` at tip. No axis harmed.

## Discernment spot-check (LEARNING.md §checked-from-outside)

The prompt's §3 source — `corpus/lessons/round-31.md` `## Gate` — does not
exist (no lesson file landed this round; conformance defect D1). Substitute
sample: this round's actual gate decisions — QUALITY admissions and the
committed negative-control verdicts.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| QUALITY criterion 53 (binding-repair bar; supersedes 48) | admitted at `f621e3c0` | `corpus/lessons/round-23.md` `### Final C1 disposition` — `M23-7` survivor row at line 229 | agree | the cited anchor resolves and M23-7's evidence (w2 attack reports) matches the criterion's fix wording |
| QUALITY criterion 54 (`file#anchor` resolves in the named file only) | admitted at `f621e3c0` | `corpus/lessons/round-30.md` `## Mistakes` `M30-1` (line 13) | agree | M30-1 records exactly the failure this criterion names — literal rubric counting ungrounded/bare citations; the criterion is the grounded fix |
| n3-section fixture | rejected (UNRESOLVED, exit 1) | `.ufo/waves/round-31/c2/negative/n3-section/` + counter re-run | agree | M23-7 id cited under `#mistakes` while living under `### Final C1 disposition` — correctly unresolved |
| n4-collapse fixture | rejected (FLOOR_VIOLATION, exit 1) | same, `--active-min 2` | agree | supersede-all drains `active` to 1 < floor — correctly refused |
| n2-wrongfile fixture | counter prints TARGET_MET | same | disagree — already learned | a non-empty unrelated lesson satisfies the syntactic rubric; the lane itself routed this as residual cheat #2 — the disagreement is on record, not unlearned |

SOURCES.md re-open: **not performable as specified** — `corpus/SOURCES.md`
is byte-identical base→tip (`grep -cE '^\|[[:space:]]*S[0-9]{3,}'` = 185 at
both revisions); no newly written or touched row exists to re-open. The
registry itself validates: `scripts/sources-census.sh validate --root …
mado` → `mado ok`, exit 0 (W04 duplicate-url warnings only, scoped).

## Trend verdicts

- **expansion: unchanged** — `corpus/knowledge/` untouched; SOURCES 185→185;
  no frontier rows advanced; two capability rows entered SCORECARD but no
  admitted knowledge on uncovered ground.
- **quality: improved** — all three counters re-measured green at tip with
  red-at-base controls; a real defect (r26 2-cell row, criterion-35
  mis-sectioned cite) found and repaired; 4 negative fixtures committed.
- **discernment: improved** — spot-check agrees on both sampled admits and
  both sampled rejects; the lone disagreement (n2) is already recorded and
  routed by the lane itself — no unlearned disagreement; criterion 54 is a
  grounded criterion grown from the routed r30 spot-check finding.

## Per-axis verdicts

coverage **improved** (C1) · calibration **improved** (C2) · operability
**improved** (C3) · depth/freshness/adjacency **unchanged** · none harmed.

## Conformance defects (status-neutral; routed to mado round 32 unless noted)

1. **No `corpus/lessons/round-31.md`** — the round's lesson (with `## Gate`
   and `## Mistakes` or the none-found sweep) never landed: the frontier
   step is unrecorded, the sourced-claim requirement has no evidence, and
   the SOURCES census before→after was never run by the lane.
2. **Report minimum-content gaps** — no `## Sources & frontier` section, no
   `## Trend verdicts` section, no `Stale-lane` line (prompt §6.6), no
   explicit `## Landed changes` heading (commits are cited inline).
3. **Report attribution defect** — L1 returned without committing; SHONEN +
   Round-shape sections swept into `3186fbe` under the lane identity
   (named in the sweep subject).
4. **Wave never dispatched** — `.ufo/waves/round-31/w1-spec.json` is 15
   prepared seats, under the v1 band 32–64 and the §3 ≥8 dispatched floor;
   0 dispatched. Lane names the missing host dispatch surface; recorded as
   an orchestrator-boundary defect, not silently passed.
5. **Axis label drift** — registration calls C2 `discernment`, report and
   SCORECARD call it `calibration`; same claim, distinct axes either way.
6. **Lane-routed residuals carried forward** — n2 relevance-free
   resolution; `outside`-only grounding (criteria 19/22/23/26/28, WARN);
   Holds≥5-words is a syntactic proxy; r24 `S###.bin` glob convention.
7. **Inherited worktree leftovers** — 3 modified + 2 untracked r30 wave-seat
   reports sit uncommitted (orchestrator artifacts; lane correctly left
   them). Orchestrator sweep, not lane debt.

SHONEN boxes: all four carry resolvable evidence pointers and look
checkable by a non-author (box 3 demonstrated by this closure's own
re-runs of the committed counters); promotion remains operator-owned.

## Verdict

All three declared claims verify on re-measurement; no axis harmed;
report is a real (defective) report, not a marker → **status ok,
verdict admitted**.
