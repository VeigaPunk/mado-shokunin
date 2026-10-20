# AttackReportReadiness — round-16 fleet-report input readiness

Seat: `MadoR16.AttackReportReadiness` (scout, read-only leaf, no dispatch).
Wave: `mado-r16-w2`. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`. Snapshot: 2026-10-20
05:55 -03:00 (08:55 UTC).
Pre-work read: `corpus/lessons/round-15-verifier-spotcheck.md`.
Method: source reading only. I did not execute `measure.py`, the action-plan
gate, any selftest, build, lint, census or live probe; no package/service
operation; no fleet file written (the fleet report does not exist and this
seat did not create it). `[OBS]` = read in a file; `[INFERENCE]` = derived by
static inspection, **not observed by execution**; `[MISSING]` = required input
absent at snapshot.

Target question only: the exact remaining inputs, commit order, census and
claim measurements needed before `.ufo/reports/round-16/mado.md` can be
written. Gate semantics, U7 body semantics, registry collisions, C3 metric
critique and promotion are other seats' questions; I do not re-adjudicate them.

## Verdict

**Not report-ready.** The lane content is largely present. The U7/facet/join
predicates and the C3 counter are statically consistent with their expected
delivered values, and the U1–U6 inputs are byte-unchanged from the revision
where they last measured 6/7, but the report contract cannot be satisfied from
committed artifacts yet:

1. the fleet report is absent (`MISSING`);
2. no L1 measurement/verification receipt exists — census-after, measure
   before/after, gate selftest/plan/frozen outputs and the digest binding are
   absent, and `SafetyReceipt.md` is an explicit draft that withholds the gate
   digest;
3. `SCORECARD.md` has no round-16 result block and no capability row;
4. `adjudication.json` predates w2 and contains zero w2 findings;
5. 8 of 32 w2 reports are absent at snapshot;
6. no lane commit exists, so every evidence pointer currently names an
   untracked worktree path.

Two count defects must be resolved in the report, not copied: the w1
`SafetyGate.md` selftest count is stale (36 vs the current static 40), and w1
line anchors are version-bound.

## 1. Required inputs by report section

Report path and order: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-16.md:101`
and `:105-119`; marker rule `:121`; commit order `:133-135`. Round-15 format
precedent: `.ufo/reports/round-15/mado.md:3,23,34,75,111,117` (six sections in
that order).

| Section | Exact input required | State at snapshot |
|---|---|---|
| Work performed | Opens by naming C1 coverage, C2 operability/capability, C3 calibration. C1: note `corpus/knowledge/waybar-observation-boundaries-r16.md:1-4` (provenance trio, one `covers: U7`), headings `:13,:32,:54,:69`, `[UNK]` at `:71-72`; rows `corpus/SOURCES.md:65-66`; digests `evidence/source-bindings.json`. C2: `tools/mado-action-plan.py`, modes at `:1-77`, pinned policy `:113-127`, policy validation `:236-286`, classification `:330-360`, selftest `:504-750`; `safety-policy.json`; `frozen/*`; `fixtures/{tight-red,tight-green}.json`. C3: `corpus/QUALITY.md:82` (21), `:102` (22); `SCORECARD.md:719-734`; `selection-{initial,corrected}.json`; lesson M3 `corpus/lessons/round-16.md:16`. Host-pause/no-op statement and process debt M2/M4/M5 (`:15,:17,:18`). | Present except observed receipts and commit hashes |
| Landed changes | One row per change, tied to `LOG.md:1162-1202` and the commit that carries it. Current LOG entry has no hashes; round-15 used a results addendum at `LOG.md:1127-1160`. | `[MISSING]` outcome addendum + hashes |
| Before → after | C1/C3: `python3 .ufo/waves/round-16/measure.py REV` at `32c4fda…` and the delivered commit; C2: the four gate commands below. Each needs observed stdout/exit and the measured commit. | `[MISSING]` outputs |
| Sources & frontier | Census command, before and after outputs + exits; rows `52 → 55`; added tier `A×3`; old-row changes `none`; nav `29 → 30`; frontier U7 route and C2 gate. Before receipt: `evidence/census-before.txt:1-7`. After: absent. | `[MISSING]` after census |
| Trend verdicts | Exactly `expansion`, `quality`, `discernment`, each with evidence, no scalar. No named non-author exists, so `unprovable-but-better` is unavailable; round-15 `quality: harmed` must not be silently reset (round-15 closure §Per-axis). | Draftable, judgment input pending w2 + closure |
| SHONEN | One line per box, four boxes at `SHONEN.md:5,7,9,11`; all `[~]` with pointers; no `[x]` without a named non-author. | Present; keep `[~]` |

## 2. Claim measurements — exact commands and expected observations

All expected values below are `[INFERENCE]` from reading the committed/current
bytes; **none was observed by this seat**.

### C1 coverage

```sh
python3 .ufo/waves/round-16/measure.py 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea
python3 .ufo/waves/round-16/measure.py <delivered-content-commit>
```

Expected baseline (`32c4fda…`): `coverage.items` `U1–U6`, `count 6`,
`score 8.5714`; `u7_present false`; `navigation` 29/29 with empty
missing/extra/duplicates; `source_registry.rows 52`, tiers `A48/B1/C3`,
statuses `mined40/queued8/rejected4`; all three `safety_artifacts.*.present
false`; `gate_sha256 fba82a66…`; `gate_executed false`.

Expected delivered: `coverage.items U1–U7`, `count 7`, `score 10.0`;
`u7_present true`; `u7_facets` all true for `producer_contract`,
`renderer_boundary`, `safe_observation`, `unexercised_rendering`,
`rendering_unknown`; `u7_candidates[0]` path
`corpus/knowledge/waybar-observation-boundaries-r16.md`, `reserved`
`{S053: true, S054: true}`, `cited ["S053","S054"]`, `inverse true`;
`navigation` 30/30; rows 55, tiers `A51/B1/C3`, statuses
`mined43/queued8/rejected4`; safety artifacts present true with
`executed false, scored false`; `gate_sha256` unchanged.

Static predicate check (mine, no execution): the note's head-15 carries the
trio and exactly one `covers: U7`; both rows are `mined`, tier `A`, and name
the note in `used-by` (`SOURCES.md:65-66`); S055's `used-by` is the lesson
(`:67`), so the inverse set is exactly S053/S054; all four level-2 headings and
`[UNK]` inside the rendering body are present; README indexes the note once
(`README.md:41`). Existing knowledge notes and old source rows are untouched
(`git diff 32c4fda -- corpus/SOURCES.md` = 19 insertions, 0 deletions;
README 7/0), so U1–U6 should not be lost. **Marker count alone is insufficient**
(round-15 closure §Claim re-check); the report must paste the facet booleans,
the inverse join and the reserved map, not only `7/7`.

### C2 operability / capability acquisition

Recommended invocation uses `-I`, matching the registered gate rows at
`SKILL.md:529-530`:

```sh
python3 -I tools/mado-action-plan.py --selftest
python3 -I tools/mado-action-plan.py --plan .ufo/waves/round-16/fixtures/tight-red.json --policy .ufo/waves/round-16/safety-policy.json
python3 -I tools/mado-action-plan.py --plan .ufo/waves/round-16/fixtures/tight-green.json --policy .ufo/waves/round-16/safety-policy.json
python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen
```

Expected verdicts `[INFERENCE]`:

| Run | Expected | Exit |
|---|---|---|
| `--selftest` | `SELFTEST_SUMMARY: 40/40 passed` **iff** all pass; total is 40 | 0 on pass |
| tight-red (`read-source` argv `sudo cat …`) | `MADO_PLAN: denied_executable:sudo` (gate `:350-359`) | 1 |
| tight-green (`read-source` argv `cat …`) | `MADO_PLAN: plan_safe` | 0 |
| `--frozen` | `MADO_PLAN: frozen_match`; expected pin `denied_executable:sudo`, exit 1 | 0 |

Verified frozen consistency `[OBS]`: `frozen/expected.json` pins plan
`82bc7652…` and policy `fb134d8f…`; actual `sha256sum` matches both;
`frozen/policy.json` is byte-identical to `safety-policy.json` (`diff` exit 0).
The policy's deny-kind entries omit `argv_nonempty`; the validator defaults it
to `False` (`tools/mado-action-plan.py:269`), equal to the pinned value, so
this is **not** a `policy_malformed` blocker.

Digest binding to redo at the measured commit (`sha256sum`/`git show`):
gate `e506bc2338bb…`, policy `fb134d8f90d1…`, cases `9d0fac4ec7a0…`, measure
`ea3db43fdc75…` (worktree values at snapshot; must be recomputed from the
commit). `frozen_match` authenticates **plan and policy bytes only** — it does
not pin the classifier binary; the classifier digest and revision must be
reported separately, as `SKILL.md:530` itself states.

Capability entry `[MISSING]`: `AXES.md:57-64` requires the row to enter
`SCORECARD.md` in the round that demonstrates it. The canonical table at
`SCORECARD.md:200-206` still reads `— none yet —`; round-12/13 precedent uses
per-round tables at `:304` and `:435`. A round-16 row (`mado-action-plan`:
what it can now do, evidence pointer, first-working round 16) is absent and
must be added **after** the observed runs, not before.

### C3 calibration

Same counting command; separate fields, never folded into C1/C2
(`measure.py` comment block above `calibration`).

```sh
python3 .ufo/waves/round-16/measure.py 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea
python3 .ufo/waves/round-16/measure.py <delivered-content-commit>
```

Expected baseline: `criteria_total 20`, `lesson_grounded 12`, ids `1–20`,
grounded `6–17`, ungrounded `[1,2,3,4,5,18,19,20]`, `fraction 0.6`,
`score 6.0`.
Expected delivered: `criteria_total 22`, `lesson_grounded 14`, ids `1–22`,
grounded `6–17,21,22`, ungrounded `[1,2,3,4,5,18,19,20]`, `fraction 0.6364`,
`score 6.3636`; delta `+0.3636`. Both new criteria carry a same-line
`lessons/round-16.md` citation (`QUALITY.md:82,102`), which is why the literal
numerator rises by 2 while the denominator rises by 2. Calibration is the
lowest axis at baseline (6.0 < 8.5714), so C3 — not C1 — is the lowest-axis
claim; the report must state the initial selection was superseded, not hide it.
The two selection JSON files are static declaration diffs (`declared_axes`
only); describe them as such, not as an executed audit (metric critique belongs
to `AttackC3Metric`).

## 3. Census

### Source census (required, conformance)

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

Before `[OBS]`: `evidence/census-before.txt:1-7`, `measured_commit=32c4fda…`,
exit 0, warnings `S030/S042/S045` W04 duplicate-url, final `mado ok …`. End
census must be run at the integrated tree after the lane commit. Static rule
check: S053/S054 URLs are unique (`grep -c` = 1 each); S055 has no URL and
`kind own-work` is admitted; its symbolic `recheck on-operator-recovery-decision`
passes `symbolic()` (`scripts/sources-census.sh:582`); all three `used-by`
paths exist (E11, `:538-567`); deny/status enums are valid. Expected end output
is therefore **identical** to before — same three historical warnings, `ok`
line, exit 0. Do not call this warning-free; do not omit the warnings.

Registry/nav counts `[OBS]` (from file bytes, not a checker): rows `52 → 55`;
tier `A 48 → 51`, `B 1 → 1`, `C 3 → 3`; status `mined 40 → 43`,
`queued 8 → 8`, `rejected 4 → 4`; knowledge notes `29 → 30`; README index
`29 → 30`, one row for the new note, no missing/extra/duplicate by set
comparison. Added rows are three tier-A rows (S053 docs, S054 code, S055
own-work); only S053/S054 credit C1. Existing-row changes: none
(append-only diff). Counting command for the report: the two `measure.py`
runs (their `source_registry`/`navigation` fields) plus the census outputs.

### Wave/report census

`[OBS]` w1 spec/dispatch: 64 items, 64 tasks, `spawn 64 / resume 0 / total
64`, zero `model` keys (re-read by this seat); 64/64 unique `Report:` paths are
reported by `RoundConformance.md` and were not re-counted here. w2 spec = 32 items; dispatch = 32 tasks with 32 unique report paths,
all equal to `.ufo/waves/round-16/w2/reports/<Name>.md`, zero mismatches;
dispatch counts `spawn 32 / resume 0 / total 32`, zero `model` keys; registry
= 32 members. At 05:55:24 -03, **24/32 report files present**. Missing:
`AttackU7Source`, `AttackC3Ground`, `AttackPause`, `AttackFrozenPins`,
`AttackFrozenMap`, `AttackC2Limits`, `AttackStaleReports`, and this seat's
`AttackReportReadiness.md` (written after the count). L1 must require 32/32
before adjudicating; any missing report is a declared gap, not silently
ignored. All 32 report files and `w2/{spec,dispatch,record}.json` are untracked
and must enter a commit for their paths to be usable as evidence pointers.

## 4. Commit order

Prompt `:133-135`: lane commit, lane push, fleet report commit, fleet push.
Identity: `mado-shokunin <mado@shokunin.local>` (`AGENTS.md:5-6`; fleet report
precedent `745f1a9` has this author). Round-15 order held: content
`5f13870` 04:35 → outcome `9ebd737` 04:38 → report `745f1a9` 04:40 → external
closure. Report-last is mandatory.

1. **Adjudicate w2 first.** Extend `.ufo/waves/round-16/adjudication.json`:
   it currently contains only w1 names (zero `Attack` entries; mtime 05:45:27),
   so w2 dispositions are unresolved. Do not commit the report before this.
2. **Content commit** (`round-16`, lane identity). Stage lane docs and wave
   artifacts, not the fleet or sibling trees:
   `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/{QUALITY,README,SOURCES}.md`,
   `corpus/knowledge/waybar-observation-boundaries-r16.md`,
   `corpus/lessons/round-16.md`, `tools/mado-action-plan.py`, and
   `.ufo/waves/round-16/**` (adjudication, measure, policy, cases, selection
   files, waybar draft, evidence, fixtures, frozen, w1, w2). **Exclude**
   `tools/__pycache__/mado-action-plan.cpython-314.pyc` (untracked; round-15
   removed an analogous generated pyc). Verify `git status` shows no
   round-16 work left untracked except intentional ignores.
3. **Verify once at that commit.** Run census end; both `measure.py`
   revisions; the four gate commands; `bash tools/mado-verify.sh --selftest`
   (harm watch; round-15 recorded 372/372, unchanged gate digest
   `fba82a66…`). Do **not** run the default live mode; if file-plane evidence
   is wanted, use `--no-live`, never the live probe. Write receipts under
   `.ufo/waves/round-16/evidence/`
   (`census-after.txt`, `measure-before/after` outputs, gate run outputs,
   digest list). If a receipt is omitted, the corresponding report row cannot
   cite observed output.
4. **Outcome commit** (second `round-16`, lane identity). Append SCORECARD
   per-claim rows (score delta, evidence pointer, counting command, measured
   commit), the C2 capability row, and a LOG results addendum in the
   round-15 shape (`LOG.md:1127-1160`). The measured inputs must be
   byte-identical between the content and outcome commits
   (`corpus/knowledge/**`, `SOURCES.md`, `README.md`, `QUALITY.md`,
   `tools/mado-action-plan.py`, `safety-policy.json`, `safety-cases.json`,
   `frozen/**`, `fixtures/**`); if any changes, re-run step 3 and re-pin
   `frozen/expected.json`. Cite the content commit as the measured revision
   when only records changed.
5. **Fleet report commit** (report-last). Write
   `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mado.md`; stage **only
   that path** — the fleet tree has 14 unrelated dirty/untracked entries
   (`.ufo/watchdog.log`, other lanes' `state/*.report-baseline`,
   `.ufo/waves/round-16/build/`, `MoriR16.Lesson`, etc.). Commit with mado
   identity, then push lane and fleet remotes. Independent non-author closure
   follows, not part of the report.

## 5. Readiness defects (bounded)

- **D1 `MISSING` — fleet report absent.** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mado.md`
  does not exist; the fleet round-16 directory holds other lanes only.
- **D2 `MISSING` — receipts.** No census-after, measure before/after, gate
  selftest/plan/frozen stdout, or digest binding exists under
  `.ufo/waves/round-16/evidence/` (only `census-before.txt` and
  `source-bindings.json`). `w1/reports/SafetyReceipt.md:9` says in terms
  "the receipt cannot bind a gate digest yet"; `:83-88` lists the gate digest,
  selftest/plan/frozen exits and measure run as L1 work. Do not cite the draft
  as a receipt.
- **D3 `MISSING` — SCORECARD result block and capability row.**
  `SCORECARD.md:690-734` contains declarations and the C3 correction only; no
  per-claim measured deltas and no round-16 capability table (compare
  `:304`, `:435`). Prompt §2.6 and `AXES.md:57-64` require the row.
- **D4 `MISSING` — w2 adjudication.** `adjudication.json` is w1-only
  (mtime 05:45:27, zero `Attack` names); w2 findings are unadjudicated.
- **D5 `MISSING` — 8/32 w2 reports** at snapshot (list in §3). A report may
  not cite a peer finding whose file never landed.
- **D6 Stale selftest count.** `w1/reports/SafetyGate.md:105,108` says
  "36 cases (31 evaluate + 5 frozen)" and `<n>/36 passed`; the current gate
  statically contains 35 evaluate + 5 frozen, and the summary prints
  `passed/total` (`tools/mado-action-plan.py:748`). Use the observed
  `SELFTEST_SUMMARY` (expected total 40), never `36`; if the observed total or
  pass count differs from 40/40, report it and treat C2 as unverified rather
  than editing the expectation into the gate.
- **D7 Version-bound w1 line anchors.** `w1/reports/MetricInflation.md`
  (05:43:23) predates the final note (05:44:53) and cites headings at
  `:28/:50/:65`; current anchors are `:32/:54/:69`. Re-anchor anything copied
  into the fleet report against the committed file.
- **D8 Untracked evidence and fixtures.** `frozen/`, `fixtures/`,
  `safety-{policy,cases}.json`, `measure.py`, `evidence/*`, `adjudication.json`
  and the wave records are untracked. Without a commit, `--frozen` and
  `measure.py REV` cannot be reproduced from the reported revision.
- **D9 Generated bytecode.** `tools/__pycache__/mado-action-plan.cpython-314.pyc`
  is untracked; exclude it from commits (round-15 precedent removed the
  analogous pyc).
- **D10 Census/report honesty.** End census must retain the three historical
  W04 warnings and exit 0; README must keep the `[UNK]`/rendered-text caveat
  (`README.md:111-116`). U7 is a documentary **observation boundary**, not
  rendered verification — the report must say so, matching the note's
  `## Unexercised rendering` and `[UNK]` lines.
- **D11 Trend-verdict constraints.** No named non-author reviewer exists
  (lesson `:81` "pending independent non-author closure"), so
  `unprovable-but-better` is unavailable; round-15 `quality: harmed` remains
  historical and must not be reset by a fixture-only gate. Expansion may be
  `improved` only on the bounded C1 route.
- **D12 Process-debt disclosure.** M4 (fleet-cwd report write) records that a
  stray fleet copy existed and Main owned removal; `find` shows no
  `RoundConformance.md` under the fleet `.ufo` tree now, so the report should
  state the incident and its removal, not claim it never happened. M5
  (`pacman -Q waybar`) must be disclosed and not rerun. No tool installs
  occurred; the report must state "Tool installs/updates: none."

## 6. Retained limits

- I executed nothing: all baseline/delivered values are static predictions.
  L1's single post-integration run is the first observation; a mismatch is a
  finding, not a reason to alter the counter.
- I did not inspect `~/.omp/agent/agent.db*`, credentials, sibling lane trees,
  live compositor/service/input state, or any package state. No install or
  update was performed.
- The w2 report census is a time-bound snapshot (24/32 at 05:55:24 -03);
  peers were still landing files. Re-run the census; do not cite this count as
  final.
- Gate semantics, U7 source-body correctness, registry collision review,
  C3 metric validity and promotion independence are owned by other seats; this
  report only states what the fleet report must contain and which claimed
  observations are still missing.

## Touched surfaces

Written: `.ufo/waves/round-16/w2/reports/AttackReportReadiness.md` only.
Not touched: lane docs/corpus/tools, `.ufo/reports/**` (fleet), sibling
repos, `~/.omp` state. No commits.
Tooling record: nothing installed, updated or removed; read-only shell
inspection (`git show`, `grep`, `sha256sum`, `stat`, `diff`, Python parsing of
JSON/source) only.
