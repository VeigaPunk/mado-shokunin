author: hyaku closure (non-author integrator, @m_zfl)

# mado round 84 — non-author verifier spot-check

## Decision and scope

**Status ok; admitted false; rejected-honest-stop.** C1's frozen finite refusal-class coverage verifies. C2's frozen instrument stops with setup rc2; a repaired successor's green result cannot substitute for the declared frozen result. Neither claim is exploratory. No capability is admitted. This judge did not author or improve the round and executed no lane gate, selftest, desktop command or mutation battery.

Reviewed before `7fd43921294116299dfce1443d56a951b9c81493`, frozen declaration `3f9eec3906ddd1492e8bc08325e83064f00111ea`, measured content `6229a0eb8be551660aa2862e52c3991613429532`, final publication `e24ba4bc8da94f70ff1edb1b81c0be45c362c7a6`, and round tip `1a7e2ca4e0234e8cfec2aafa7f0c1ec6f11d3c49`. Below, W means `.ufo/waves/round-84/` inside the lane repository. Receipt paths are W-relative, not root-level paths. Fresh read-only reviewers CloseMadoR84.Mado84ClaimReview and CloseMadoR84.Mado84SourceReview supplied independent checks; this closure judge retains the admission decision.

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %ad' --date=iso -- .ufo/reports/round-84/mado.md` returned `mado-shokunin <mado@shokunin.local> feb5e131347824f7ee2252513fa0a41e7d9a645e 2026-11-04 12:10:10 -0300`. Correct report path, lane identity and substantive report, not a marker.
- Report has exactly the SHONEN heading and four `[~]` assessment lines with pointers, matching the four boxes in SHONEN.md. No `[x]` was written.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e HASH^{commit}` and `merge-base --is-ancestor HASH master` succeeded for all four reported landed hashes above and the base. Branch `master`, never detached HEAD's upstream, was the ancestry target.
- `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin` returned `branch=master local=1a7e2ca4e0234e8cfec2aafa7f0c1ec6f11d3c49 remote=1a7e2ca4e0234e8cfec2aafa7f0c1ec6f11d3c49 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` was empty before this verifier file.
- Final lane commit time was 12:09:08 -0300, before report 12:10:10 -0300. Prompt is durable in fleet commit `6917cd401da1de1dde488847a7d4870b10f419fd` (11:38:50 -0300).
- Dispatched prompt sections 1–5 embed mission/axes binding, distinct falsifiable claims/lowest-axis obligation, ≥8 L2 in one batch, commit/push, push scope and L0 side channel. Section 6 supplies write scope, report-last ordering, pushed-hash citation and report identity; section 4 requires SHONEN. All five child-lane items present. Host route-table amendments are explicitly operator rulings; ≥8 floor agrees with MISSION.md §L2 concurrency. Lane reports one ten-seat wave, planner held by L1, 30% formal attacks. Expired terminal statuses and actual answering models are explicitly unavailable, not inferred from outputs.

Committed dispatch/completion digest (mutable watchdog lines re-opened and matched):

```text
2026-11-04T11:39:23-03:00 launch mado round=84 pgid=2809300 driver=hyaku-inline attempt=1
2026-11-04T12:11:26-03:00 complete mado round=84; hyaku-inline attempt=1
```

## Claim re-checks: measurement versus evidence verification

### C1 coverage — improved, bounded finite predicate

Evidence-verified from W/claims-declaration-r84.md, W/w1/R84ExecC1.md and W/w1/R84ReviewerC1.md: frozen revision `3f9eec39` produces `cases=61 correct=61 mutants=41 killed=41 base_correct=58/61 carried=58/58 tool_selftest=139/139 verdict=TARGET_MET`, exit0. `receipts/control-c1-r84-at-base.txt` retains the actual held tool's 58/61 TARGET_MISSED, exit1. `receipts/final-c1-r84.txt` measures `6229a0eb`, repeats that result, and pins counter/control hashes. Counter selftest receipt is 99/99, exit0 at that content revision; tool selftest139/139 is in the full receipt.

Independent plain measurements over Git objects, not gate execution:

```python
# Run with python3; the same read-only Git-object measurements were executed by this judge.
import subprocess, json, re, hashlib
R = '/home/vgpnk/Projects/shokunin/mado-shokunin'
B = '7fd43921294116299dfce1443d56a951b9c81493'
T = '1a7e2ca4e0234e8cfec2aafa7f0c1ec6f11d3c49'
P = '.ufo/waves/round-84/'
def blob(rev, path):
    return subprocess.check_output(['git','-C',R,'show',rev+':'+path])
a = json.loads(blob(T,P+'controls/c1-cases-r84.json'))['cases']
b = json.loads(blob(B,'.ufo/waves/round-83/controls/c1-cases-r83.json'))['cases']
print(len(a),len(b),a[:len(b)]==b,[x['name'] for x in a[58:]])
for stem, tag in [('c1','CASE'),('c2','PROBE')]:
    text = blob(T,P+'receipts/final-'+stem+'-r84.txt').decode()
    pins = json.loads(re.search(r'^input_sha256=(.*)$',text,re.M).group(1))
    print(stem, all(hashlib.sha256(blob(T,p)).hexdigest()==v for p,v in pins.items()))
    print('correct/matched rows',len(re.findall(r'^MADO_R84_'+tag+r':.*(?:correct|match)=yes.*$',text,re.M)))
    print('killed rows',len(re.findall(r'^MADO_R84_MUTANT:.*killed=yes$',text,re.M)))
print(round(10*58/61,4),10*61/61)
```

Observed: population61, carried58, parsed equalityTrue, new names duplicate-extra-namespaces / duplicate-bar-namespace / duplicate-allocation-keys; all four pinned inputs match final bytes in each receipt; C1 correct rows61/killed41; C2 matched33/killed29; score9.5082→10.0. Both frozen control files remain byte-identical through final tip. Tool, SKILL and both counter bytes at measured content equal final-tip bytes.

This verifies only the three named refusal witnesses. Narrowing an ambiguous declaration input grammar earns bounded refusal-edge coverage, not predictive expansion, a protocol uniqueness law, arbitrary duplicate handling, or causal authentication. The disclosed surviving cheats remain real limitations.

### C2 operability — unprovable as declared; honest stop

Evidence-verified, not re-executed: W/w1/R84ExecC2.md binds frozen revision `3f9eec39`, retains33 matched rows and28 killed mutants, then `ERROR (stage=setup mutant pipeline-guard-stripped anchor occurs 2 times, not once)`, exit2. The frozen29-mutant predicate therefore does not verify.

`receipts/control-c2-r84-unguarded.txt`: producer exits7 after `b true`, tail yields pipeline0, expected failed-pair matches0/1, TARGET_MISSED exit1. This is a one-case intervention, not a full31-row before replay. `receipts/final-c2-r84.txt` at repaired `6229a0eb` reports33 executed/matched,26/26 shapes,33/33 anchors/rows,29/29 kills, TARGET_MET exit0; counter selftest98/98 exit0. This is successor evidence only.

Independent JSON counts: final C2 controls contain33 rows versus31 carried;15 carried argv rows include pipefail (17 including the two additions). Read-only reviewer compared all carried fields: only declared fifteen rows change argv/skill_anchor. Counter/control hashes match final-tip bytes; this binds identity, not historical execution chronology or arbitrary child honesty. Four carried C2 rows depend on the same barfoot tool as C1; only the incremental pipefail mechanism is independent.

### Harm watch and carry-in repairs

Executed `git diff B T -- SCORECARD.md`: the round appends bounded C1 improvement and explicit C2 honest stop; no C2 scalar/capability upgrade. Current publication104/104 navigation,86/86 calibration,12/12 operability. Committed gate evidence (never run here): index104/104 missing0/dangling0/duplicates0; ledger154/154 uncovered0; standing selftest460/460; wave1/1 settled, ten seat records; final-axis checked3/mismatched0 at `e24ba4bc`. Initial stale102/102 publication failure remains in `receipts/axis-prepublication-r84.txt`.

Independently counted SKILL gate-table rows for the four r83 R1 paths at base/tip: missing4/4→0/4. All six r82–r84 home-registry rows now exist. `receipts/population-drift-refusals-r84.txt` records both constant-only drifts refusing setup rc2; this is evidence-verified, not a self-run. R83 R3 connector debt has file:line output at W/w1/R84ConnSiblings.md. PROVINCE.md:471–485 retains read-only/frozen-read-verb bounds and sibling ownership; general source-only/live wording tension remains disclosed.

## Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| coverage | improved | Frozen finite refusal witness58/61→61/61,41/41 kills; not arbitrary prediction coverage. |
| operability | unprovable | Frozen C2 setup rc2 fails its declared29-kill predicate; repaired successor is not retroactive. |
| depth | unchanged | No separate technical-depth claim. |
| freshness | unchanged | Dormant host rubric stays operator-owned; no fresh scalar awarded. |
| calibration | unchanged | Publication correction and honest stop preserve86/86; no numeric upgrade. |
| adjacency | unchanged | Connector preserves tsukuroi/tameshi/kumitate ownership; no sibling ground absorbed. |

No observed owned-axis harm; unprovable is not harmed. Failure of one declared claim nevertheless bars round admission.

## Outside discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S486 allocation-key ambiguity | admit | https://www.rfc-editor.org/rfc/rfc8259.txt §4 Objects, page6; retained pin line322 | agree | Exact8-word quote: “The names within an object SHOULD be unique.” JSON interoperability guidance supports deliberate tool refusal; SHOULD is not MUST. New row's scoped tierA and used-by pointers resolve. |
| S487 pipeline status | admit, offline evidence verified | GNU Pipelines URL timed out on this judge's two attempts and reviewer's bounded retry; W/fetch/bash-pipelines.html:119–125 reopened | agree within pinned scope | Exact12-word quote: “value of the last (rightmost) command to exit with a non-zero status”. Verified in committed primary-source pin, not claimed live fetch. No inference about arbitrary /bin/sh support. |
| Declaration uniqueness is upstream layer-shell law | reject | RFC8259 §4 reopened by this judge; reviewer also reopened https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/master/unstable/wlr-layer-shell-unstable-v1.xml | agree | RFC concerns JSON names, not layer namespaces. Reviewer found namespace-purpose text and no uniqueness rule/error; no protocol law can be inferred from this join's restriction. |
| Shape-perfect tail proves producer succeeded | reject | W/fixtures/failing-producer.sh:1–3 and W/receipts/control-c2-r84-unguarded.txt reopened | agree | Script prints plausible text then exits7; committed actual control retains pipeline0. Payload shape cannot recover erased producer status. Control result evidence-verified, not executed here. |

Live S486 re-open independently resolves the new row's ≤25-word quote and location. Source reviewer also fetched RFC raw bytes identical to committed pin (SHA256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`). GNU unreachability is recorded as degraded verification, never quote absence or harm. The required at-least-one admit/reject sample is fully satisfied independently of GNU availability.

Executed `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`: exit0, final `mado ok .../corpus/SOURCES.md`; W04 scoped duplicate-URL warnings and W01 S277 tierC-mined warning persist. No warning was suppressed or called repaired. Independent `len(re.findall(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|', text, re.M))` over `git show REV:corpus/SOURCES.md` produced base420 and final422. `git diff --name-only B T -- corpus/knowledge` listed exactly bar-footprint-namespace-discipline-r84.md and runbook-producer-status-r84.md; `git ls-tree -r --name-only REV -- corpus/knowledge` counted102→104. Both new entries begin source/verified-at/recheck, cite mined S486/S487, and are indexed in README.md with bounded frontier ground.

## Trend verdicts

- **expansion improved:** two new admitted, sourced and indexed notes on previously unheld named ambiguity/status ground; knowledge102→104 and SOURCES420→422 independently counted. This is corpus expansion, not admission of failed frozen C2.
- **quality improved:** registry missing4→0 independently remeasured; constant-drift refusal evidence, grounded QUALITY138/139, privacy/output-size repair and explicit retention of frozen failure improve the record. No sampled admitted fact was found false or left falsely advertised as verified.
- **discernment improved:** this independent closure agrees with sampled admits and rejects above; r83 registry disagreement becomes lesson-backed QUALITY139 and a measured repair. GNU's pin-only verification is explicitly distinguished from live re-opening.

## Routed defects — mado owns next-round correction

1. **R1, medium:** carry forward the finite-oracle gaps in W/w1/R84ReviewerC1.md and R84MutationTester.md: equal-valued/interleaved duplicate collapse, cross-level identities, casefold over-refusal, any-nonzero producer-status and stdout-prefix acceptance. Add grounded controls/falsifiers only in a new declaration; never widen r84 frozen populations after scoring.
2. **R2, low:** `quality/counters/c2-r84-runbook.py:679–687` permits skill_anchor changes for every carried row, broader than the declared fifteen supersessions. Actual r84 controls comply. Tighten the next counter's enforcement to the declared superseded fields; preserve frozen bytes.
3. **R3, low:** population-before-scoring receipt lacks revision/hash attribution. Final input hashes establish identity, not chronology; bind the next declaration/pre-scoring receipt to revision and inputs, and do not call tree=bound full counter/control authentication.
4. **R4, low:** lesson's bare source-pins-r84.json pointer should explicitly resolve as W/fetch/source-pins-r84.json in a future append-only clarification. Re-attempt GNU live source at a subsequent recheck; present unreachability is not fabrication.

Frozen C2 anchor failure is retained as the reason for honest stop, not an unaddressed current anchor repair: successor repair is already committed. Red gate/status defects stay status-neutral. Terminal-provider success and dead-seat count remain unavailable; do not backfill telemetry from nonempty outputs.

## Operator notes and self-evaluation

All four SHONEN boxes look checkable by a dedicated non-author promotion review (cited decision tables, logged end-to-end work, executable bounded instructions, scoped province). This closure does not grant promotion or write marks; operator owns promotion. No tools installed/updated; no sibling files or lane-authored files changed by this judge.

Self-evaluation: accuracy4 (gate results evidence-verified, not freshly executed; GNU live unavailable), completeness4 (all closure checks covered, dedicated promotion outside scope), clarity4 (frozen/successor separated; long evidence section), actionability4 (four routed forward corrections with paths), conciseness3 (reproducible evidence expands the record). Mean3.8/5. Main improvement: preserve this minimal frozen/successor distinction in the one-line handoff rather than repeating the full report; user should agree the rejected frozen claim stays rejected.
