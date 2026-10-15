# Mado — fleet round 1 interactive continuation

**BLOCKED before native specialist dispatch. Not a completed or admitted round.**

Content commit: `7cd7f331ae151845ebff7bd100c1073ebad49351`.
Baseline: `bb08dd57f4b48bfb001a178e57b9c25e7040447f`.
Lane identity: `mado-shokunin <mado@shokunin.local>`. No push.
Mission: `m_bda9bde95130412f914a953eb0c93835`.
Run/session: `shk-mado-interactive-20261015T050057Z`.
New verified completed rounds: **0**. Sighting remains open.

## Work performed

- Reconciled the stopped headless work with actual lane state: same-scope uncommitted navigation, lesson and bookkeeping were preserved and committed, not reset. Historical training rounds 1–11 remain intact. The headless launch counter 1 is not a completion. Evidence: `LOG.md` → “fleet round 1 interactive cutover”; inherited fleet-round-1 entries; content commit above.
- Read canonical UFO run-logic §0/§5, canonical Shokunin protocol load order, fleet read-only MISSION/AXES and lane authorities. Saved the L1 WWKD plan before implementation: `.ufo/plans/fleet-round-1-wwkd.md`.
- Retained the single coverage-navigation candidate: 14 missing-note routes, seven province-surface routes, Frontier limitations and exact landed filenames; no historical knowledge body or gate implementation was changed. Evidence: `corpus/README.md:20-84`, `SKILL.md:1548-1580`, `corpus/lessons/round-1.md:89-126`.
- Re-measured the committed baseline and candidate with the scorecard's exact-target counter. Exercised the actual SKILL → index → idle/lock note reading path, retaining config provenance, unverified timing/reset, UNKNOWN transitions and process-versus-unit turnover E2. Evidence: `.ufo/evidence/fleet-round-1/{navigation-baseline.txt,navigation-committed.txt,navigation-smoke.json}`.
- Prepared 32 distinct, bounded audit scopes and validated them through canonical `ufo-swarm-wave.mjs plan`; rendered the complete canonical payload as a preview without dispatch or registry persistence. Evidence: `.ufo/waves/fleet-round-1-interactive/{spec.json,plan.json,validation.json,dispatch-preview.json}`. The 32 scopes are 22 note audits, seven province-route audits, connector, admission critic and provenance scribe. Each has a distinct report-only write scope and skips build/lint/tests/formatters.
- Stopped before dispatch because the measured live global authority cannot realize the operator-required role bindings. No role relabeling, concrete model pins, replacement route, configuration edit or routing overlay. Exact safe metadata: `.ufo/blocked/fleet-round-1-routing.json`.
- Ran L1-only hermetic and file-plane acceptance after integration; captured full output and exit codes, not remembered verdicts. Evidence: `.ufo/evidence/fleet-round-1/{selftest.txt,file-plane.txt,gates.json}`. No live UI, idle transition, raw journal, environment value or native transcript body was inspected.

## Landed changes

The content commit is `7cd7f331ae151845ebff7bd100c1073ebad49351`; every row below is motivated in `LOG.md` → “fleet round 1 interactive cutover: candidate retained, dispatch blocked”.

| Paths | Landed work |
|---|---|
| `corpus/README.md` | Complete existing-note index, province routes and explicit unheld frontier; dated evidence is not present desktop health. |
| `SKILL.md`, `SHONEN.md`, `corpus/lessons/round-1.md` | Retained entry/filename corrections and four `[~]` independence caveats; appended cutover qualifications supersede inherited completion/push/admission language without erasing history. |
| `SCORECARD.md`, `LOG.md` | Lowest LIVE sub-axis, candidate-only per-axis/trend verdicts, route blocker, no-push rule and zero completion increment. |
| Explicit `.ufo/plans/`, `.ufo/blocked/`, `.ufo/waves/`, `.ufo/evidence/` artifacts | WWKD, safe missing-binding evidence, validated undispatched 32-scope plan/preview, baseline, full gates and representative navigation smoke. Native interactive-session material is excluded. |

The subsequent committed-revision measurement, this report and the continuation record are durability records written after that content commit. They do not change its measured index or gate.

## Before → after measurements

Counting command: `SCORECARD.md` → “Counting command”, executed with `REV` set to each exact commit. A note's first-column target must exist exactly once; prose mentions and province-table links are not index rows.

| Measurement | Baseline `bb08dd57f4b48bfb001a178e57b9c25e7040447f` | Candidate `7cd7f331ae151845ebff7bd100c1073ebad49351` |
|---|---|---|
| Uniquely indexed existing notes | 8/22 | 22/22 |
| Missing / dangling / duplicate note rows | 14 / 0 / 0 | 0 / 0 / 0 |
| Bounded navigation score | 3.6364/10 | 10.0000/10 |
| Counter exit code | 1 | 0 |

Full committed after-output:

```text
revision=7cd7f331ae151845ebff7bd100c1073ebad49351 indexed=22/22 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
```

The candidate smoke additionally resolved 54 local Markdown links with zero broken/outside-lane targets and identified seven province routes. The throwaway probe initially skipped two table headers although only one matched; correcting the probe's parser required no repository edit. It was an in-memory smoke, not a permanent source-text test. This local smoke does not stand in for the undispatched semantic audit wave.

## Local gate and smoke evidence

Gate SHA-256: `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`.

```text
$ bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 268/268 assertions passed
exit=0

$ bash tools/mado-verify.sh --no-live
counts: pass=29 fail=0 unknown=0 skip=8 note=4
MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)
exit=0
```

The complete file-plane output also records `boundary.readonly PASS`, config bytes identical before/after, combined SHA `bb2639d9a980…`. SKIPs are not agreement. These runs show hermetic capability and file-plane conformance only; no current live desktop-health, rendering, dispatcher, rule-effect or idle-transition claim is added. Reported Phase 0/self-iter failures were not re-run; no NativeRoundHandoff, Rust verdict or Pareto acceptance is claimed.

## Axis verdicts — candidate only, not round admission

| Axis | Verdict | Evidence / limit |
|---|---|---|
| coverage | improved | Committed navigation 8/22 → 22/22; finite admitted-note denominator only. |
| depth | unchanged | No new technical-depth claim or knowledge entry admitted. |
| operability | unchanged | Gate unchanged; 268/268 assertions, exit 0. This is not whole-domain operability. |
| freshness | unchanged | File-plane point sample CLEAN; historical live claims are not re-verified. |
| calibration | unprovable-but-better | Candidate versus admission and author assertion versus outside authority are explicit; independent spot-check absent. |
| adjacency | unchanged | Province and read-only sibling/substrate boundaries unchanged. |

No local axis harm is observed. That is insufficient for admission while required dispatch and outside checking are missing. No scalar substitutes for these verdicts.

Learning trends: **expansion unchanged**; **quality unchanged** for domain evidence; **discernment unprovable-but-better**, with no outside-lane agreement claim. The admit/reject decisions and missing spot-check are in `corpus/lessons/round-1.md`.

## Exact blockers and unblock owners

1. **Authorized native dispatch — operator/global routing authority owner.** Actual connector/executor/reviewer bindings are `@m_mid`, critic is `@m_strong`, scout/scribe are `@m_fast`. Required: content `@m_composer`, audit/review/scout/critic `@m_grok`, connector `@m_antigravity` with `@m_zfl` fallback. The required aliases exist, but `m_antigravity`'s fallback chain is empty. Concurrency is already 32. No new specialist was started. The canonical validator accepts `connector`; this is a routing mismatch, not a validator-taxonomy mismatch.
2. **Outside-lane admit/reject spot-check — fresh non-author verifier/operator, not this lane's L2s.** Sample at least one proposed admit and one reject; record agree/disagree and reasons in the lesson. No promotion clearance is inferred.
3. **Applicable receipt binding — owning integrator.** The inspected direct interactive launch/selected Sighting metadata supply no task key, prompt/config digest or receipt path. See `.ufo/blocked/fleet-round-1-receipt-binding.json`. No task key/config digest was invented. No receipt was minted/validated and no Sighting completion command ran. Schema-only validation would not establish fleet acceptance.

Routing/configuration remediation is outside this training lane; report it, never absorb it. Secret handling belongs to kagi; model/service configuration and orchestration ownership are unchanged. No sibling or shared fleet ledger was edited.

## SHONEN

- [~] Decision tables/error patterns/checklists/sources: inherited evidence `corpus/knowledge/executor-test-sufficiency.md`; current caveat `SHONEN.md:5-6`. Outside-lane verifier independence is not established.
- [~] End-to-end domain task: inherited `corpus/knowledge/config-health-report-r3.md` and historical LOG round 3; `SHONEN.md:7-8`. Navigation is not a newly executed desktop transition.
- [~] No-oral-context instructions: inherited `corpus/knowledge/executor-test-sufficiency.md`; current representative route smoke is author evidence, not an outside verifier; `SHONEN.md:9-10`.
- [~] No cross-domain bleed: `PROVINCE.md`, `corpus/knowledge/province-accuracy-selfaudit.md`, `SHONEN.md:11-12`. No new independent province clearance.

## Continuation

Machine-readable handoff: `.ufo/continuations/fleet-round-1.json`.
After operator-owned prerequisites, authorize a fresh interactive L1 session to resume **this same unfinished fleet round 1**, inspect current state and dispatch its complete authorized batch. Re-measure before admission. Do not advance to round 2, restart the stopped headless driver, spawn another L1 here, reuse stale route evidence as fresh, or loop rounds inside this session.

The target remains at least 100 verified rounds per included lane. This partial blocked attempt adds zero; historical rounds are neither erased nor automatically re-certified. One blocked attempt is recorded, not three consecutive blocked rounds. No sound-saturation stop is claimed. The fleet integrator owns shared ledgers and redispatch; this report does not retire the Sighting.

## Append-only reproducibility erratum — caller REV wrapper

This corrects the “Counting command ... executed with REV set” reproduction
claim in the filed report at `220e0f6682cece6e02028f65abf021fa98b84f83`.
The original published shell wrapper hardcoded the baseline SHA, although
the earlier Python-body measurements selected the intended REV through
their process environment. Those measured results stand; the old literal
wrapper did not support the documented candidate invocation.

`SCORECARD.md` now honors exported caller REV, defaulting only an unset/empty
REV to the baseline. The complete corrected bash fence was passed unchanged
to `bash -s`, not reconstructed as an equivalent Python invocation.
Its SHA-256 is
`8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`.
Caller baseline REV produced 8/22, missing 14, dangling/duplicates 0,
exit 1; caller content REV `7cd7f331ae151845ebff7bd100c1073ebad49351`
produced 22/22, missing/dangling/duplicates 0, exit 0.
Full output and execution method:
`.ufo/evidence/fleet-round-1/counter-literal-{baseline.txt,candidate.txt,invocations.json}`.

Motivation, correction and proof are appended in `LOG.md` → “reproducibility
erratum: caller-selected revision”. This is a local reproducibility repair,
not a second craft round or a change to the domain gate, admission blockers,
axis/trend verdicts, receipt state or zero verified-round increment.
