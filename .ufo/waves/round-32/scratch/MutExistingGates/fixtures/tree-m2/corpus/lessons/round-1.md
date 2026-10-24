# Fleet round 1 — evidence navigation, not behavioral closure

2026-10-15. Axis: coverage, narrowed to discoverability of the existing
admitted corpus. This explicit fleet run follows the historical training
arc; it does not relabel its rounds. Motivation and observed commands:
`LOG.md` → “fleet round-1: admitted-corpus navigation”; scoring and the
commit-based counter: `SCORECARD.md` → “Fleet round 1”.

## Gate

| Candidate | Decision | Evidence and boundary |
|---|---|---|
| Route the existing but unindexed notes and expose per-province source/limit paths | Admit as navigation, not new domain knowledge | Baseline `bb08dd57f4b48bfb001a178e57b9c25e7040447f`: the scorecard counter prints `indexed=8/22 missing=14 dangling=0 duplicates=0`; corpus map/frontier at `corpus/README.md`. No knowledge file is added by this round. |
| Treat a complete index as complete desktop coverage or current health | Reject | `corpus/knowledge/arc-synthesis.md:290-307` retains behavioral gaps; `corpus/knowledge/closeout-r11.md:243-263` records hermetic/file-plane success alongside historical live DIVERGED. A navigation row cannot turn UNKNOWN, SKIP or a proposal into PASS. |
| Treat the inherited idle/lock absence sample as timeless or its timing as observed | Reject | `corpus/knowledge/idle-lock-plane.md:129-136,241-263,364-379`: competing timing inferences and session-turnover evidence require dated declarations, process-vs-unit distinction, and an unexercised-transition limit. |
| Copy planned filenames or a stale recheck link into a new route | Reject | `corpus/knowledge/closeout-r11.md:138-142` names the standing-use F4 pointer; landed artifacts are `arc-synthesis.md` and `closeout-r11.md`. No compatibility aliases or historical-note rewrite. |
| Use this round's L2s as outside-lane promotion or discernment verification | Reject | Canonical `LEARNING.md:37-43` and `PROTOCOL.md:63-73`; all dispatched L2s belong to the mado authoring lane. `SHONEN.md` retains four `[~]` assertions. |

Outside-lane spot-check: **not supplied**. No independent agreement on an
admit/reject sample or promotion clearance is claimed. The L2 planner,
reviewer and critic provide authoring-lane review only. No criterion is
added to `QUALITY.md` without an outside-disagreement lesson behind it.

## Counting and interpretation

The frozen comparison is the immediate `corpus/knowledge/*.md` inventory
at the measured commits. Count exact first-column note targets, not prose
mentions or province-table links. Missing, dangling or duplicate targets
fail completeness; a matching filename without a supporting source/limit
is also a semantic failure. Preserve the original note rows and the
inherited source dates. The scorecard's numeric proxies are bounded
measurements, never averages of axis verdicts or expertise scores.

The existing gate is unchanged at SHA-256
`93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`.
The parent observed `bash tools/mado-verify.sh --selftest` →
`MADO_SELFTEST: 268/268 assertions passed`, exit 0, and `--no-live` → file
plane CLEAN with `pass=29 fail=0 unknown=0 skip=8 note=4`, exit 0.
Neither result establishes current live behavior; the skip scope stays
visible. No gate row, assertion, expected value or mutation obligation
is changed to obtain the navigation improvement.

## Learning trends

- Expansion: unchanged. Previously admitted evidence becomes reachable;
  no new ground or knowledge entry is admitted.
- Quality: unchanged for domain evidence. Navigation is repaired, but the
  inherited notes keep their timestamps, errata and unresolved findings.
- Discernment: unprovable-but-better as an authoring process only; explicit
  rejects and adversarial review are recorded, but the required outside-lane
  spot-check is absent. This is not independent clearance.

## Boundary

All domain config trees, the running compositor and sibling repositories
remain read-only. Route actuator/repair instructions to the operator;
never execute them as an index recheck. Secret contents, browser sessions,
model endpoints and harness implementation are not absorbed into mado.

## L2 batch receipt

One native OMP `task` dispatch carried all the roles below. No per-lane
model parameter, routing override, generic UFO-wave validation claim or
outside-lane verifier claim is made. The names identify the actual
authoring-lane advisers; their session-local drafts are not closure-time
evidence. The durable source anchors and retained decisions are below.
Paths in this receipt table are relative to `corpus/`; `../` reaches the
lane repo root. The rest of this lesson uses lane-root-relative paths.

| Adviser | Host role | Retained contribution / durable source |
|---|---|---|
| MadoPlan | planner | Representative idle/lock row generalized into source/date/errata/recheck/unknown criteria; `knowledge/idle-lock-plane.md:129-136,364-379` prevents declaration→transition and unit→process conflation. |
| MadoConnect | connector | Outbound operator-action, browser, secret and harness boundaries stay explicit; `../PROVINCE.md:10-18`, `../SHONEN.md:6,10`, `knowledge/gate-mutation-proof.md:4-5`. No sibling scope is absorbed. |
| MadoExecConfig | executor | Config/audit/Walker/census routes preserve turnover E2 and unapplied ledgers; `knowledge/idle-lock-plane.md:364-379`, `knowledge/remaining-planes-census.md:326-333`, `knowledge/walker-live-surface.md:207-241`. |
| MadoExecGate | executor | Gate routes distinguish historical scratch from persisted revision/spec contracts; `../tools/mado-verify.sh:1216-1293`, `knowledge/gate-standing-use.md:251-297`. No fresh sweep or pin update. |
| MadoExecSynthesis | executor | Exact terminal filenames, gap/disposition routes and candidate-not-applied errata; `knowledge/walker-deep-r9.md:357-396`, `knowledge/arc-synthesis.md:290-307`, `knowledge/closeout-r11.md:181-205`. |
| MadoScribe | scribe | Inherited partial same-scope work, report-after-commit ordering and four `[~]` assessments; `../SHONEN.md:5-12`, `../LOG.md` fleet-round-1 entry. |
| MadoRecon | scout | Per-PROVINCE evidence-type routes and frontier, not filename-only coverage; `../PROVINCE.md:6-12`, `knowledge/remaining-planes-census.md:32-49`. |
| MadoReview | reviewer | Exact-target/duplicate/dangling and same-commit supersession conditions; `../SKILL.md:1548-1563`, `knowledge/closeout-r11.md:138-142`. Review is authoring-lane, not promotion clearance. |
| MadoCritic | critic | Counterexample to green-proxy health inference and explicit finite-denominator limits; `knowledge/closeout-r11.md:243-263`, `knowledge/arc-synthesis.md:296-307`. Use “suite pass fraction,” not complete operability. |

All nine returned advisory findings. L1 trims their dense row drafts into
the existing three-column index and owns final measurement and integration.
The reviewer identified the sibling harness boundary; the index states it
explicitly. The critic's L2-only no-commit restriction is not an L1 hold:
the user requires lane/report commits and pushes. No authority to judge or
ship is delegated to an L2.

## Interactive continuation — dispatch blocked before admission

The interactive operator dispatch supersedes the preceding sentence's push
requirement: **no push is authorized**. The nine-adviser receipt above is
inherited partial-round history, not evidence that this session dispatched
the required 32-scope wave. Its adviser contributions were not re-attested
by reading native transcript bodies.

The L1 saved `.ufo/plans/fleet-round-1-wwkd.md`, preserved the dirty
navigation work, and re-measured the committed baseline:
`.ufo/evidence/fleet-round-1/navigation-baseline.txt` records 8/22 indexed,
14 missing, zero dangling/duplicates, exit 1 at `bb08dd57f4b48bfb001a178e57b9c25e7040447f`.

The complete 32-scope spec is in
`.ufo/waves/fleet-round-1-interactive/spec.json`. Canonical
`ufo-swarm-wave.mjs plan --spec <that file>` returned exit 0 with
`spawn=32 resume=0 total=32`; full plan and outcome are retained beside it.
The validator accepts the connector taxonomy role; the retained plan has
`MadoConnectAxes` as `connector`. Validation is not dispatch or admission.

Actual global role bindings do not realize the operator's requested
content/audit/connector aliases, and `m_antigravity` has no `m_zfl`
fallback. Exact safe metadata and the operator-owned unblock action:
`.ufo/blocked/fleet-round-1-routing.json`. No replacement role, per-task
model, routing overlay, configuration edit, registry with fake agent IDs,
or native task call was made. No specialist was started by this session.

The navigation candidate is retained and locally verified, but the round
remains **blocked and unadmitted** until the required authorized wave and
outside-lane admit/reject spot-check exist. The inherited “Admit as
navigation” decision is a proposed local curation decision, not a completed
fleet-round admission. Local checks cannot replace those missing duties.
The Sighting stays open; no receipt or verified completed round is claimed.

Fresh-session continuation resumes this same fleet round 1 after the named
prerequisites, not round 2. Historical training rounds remain intact.
Launches and this blocked partial round add zero toward the operator's
target of at least 100 verified rounds.
