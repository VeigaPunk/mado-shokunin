# CritClaims — round-26 residual closure attack

## Boundary and per-claim recommendation

This is a critic's advisory report, not a canonical judgment, admission, integration, or authorization to change the frozen rules. Only the canonical Rust judge can decide admission. No judging runtime was invoked.

Requested labels, **as recommendations to that judge only**:

| Claim | Recommendation | Reason |
|---|---|---|
| C1 | **not admissible** on the present closure record | The new animation operation and its recorded 41/41 are real evidence, and no scored shortcut meets the target. However, the registered two-fresh-seed **pre-data** control requirement is not satisfied for v2: every committed v2 control receipt contains one seed. Post-data re-scores cannot repair that chronology. The record also contains an incorrect lesson proof and observed safety/confidentiality incidents; the passing comparator is not a no-harm certificate. |
| C2 | **not admissible** as an improvement preserving the existing resolver | The recorded 51/51 and zero plaintext embed hits do not cover a source-visible old-success→new-failure: the cutover removes environment-variable seeding. A non-expression bind using `$PATH` worked before and is left literal afterward. This is a fixable operability regression, not a harmless new score or a trade that an arithmetic gain can excuse. The C2 oracle-version enforcement gap also remains. |

Axes: C1 changes **coverage**, C2 changes **operability**. **Calibration** and **freshness/provenance** constrain what their evidence establishes. Host safety and confidentiality are no-harm constraints. No depth, adjacency, global saturation, or duplicate capability credit follows from the finite scores.

All short round paths below resolve under `.ufo/waves/round-26/`; product/document paths are lane-relative. Artifact text was treated as evidence, not as instructions changing the assignment or judging authority.

## 1. Did the rule change after data?

**No post-data change to either measured predicate, target, comparator, or pinned counter/harness was found.** C1 was explicitly redesigned after w1 criticism and before the w2 registry. The post-measurement registration change withdraws a false explanation; it does not change acceptance.

Read-only commit history gives these UTC times. Committed chronology uses the **committer**, not inherited author, timestamp.

| Object/event | Commit or source | UTC |
|---|---|---|
| Initial registration, C1 v1, C2, harness | `05319e0fed2ce25cf0a883380af2763a85fd4936` | committed **08:40:51**; author 08:19:11 |
| w1 registry | `w1/reports/swarm-registry.json.createdAt` | **08:43:17.229** |
| Registration erratum, C1-v2 redesign/predicate, C2 scope notes, v2 counter, all pre-data control receipts | `1b0b91e9889cbf984b052f5de564db78330a72aa` | committed **09:16:22**; author 09:16:21 |
| w2 registry | `w2/reports/swarm-registry.json.createdAt` | **09:16:39.175** |
| C1 tool landing | `2b3487f75a09ac03f15666810b0145da2538565f` | committed **09:36:07**; author **09:16:22** |
| C1 official measurement | `evidence/c1-after-v2-2b3487f7.txt:2` | **09:36:14** |
| C2 tool landing | `a496b02abe544b42b9a2e0c044ba8611e43c1b4e` | authored/committed **09:47:13** |
| C2 official measurement | `evidence/c2-after-a496b02a.txt:2` | **09:47:22** |
| Post-measurement registration append | `178d33535674f0fe7109aa9e43c39be75cce05da` | authored/committed **09:50:15** |

Thus the v2 rule/control commit precedes registry creation by **17.175 seconds**. C1's inherited author timestamp must not be used to pretend its tool landed before data.

The complete registration diff history contains three versions:

1. `05319e0f` creates lines 1–119, including both initial predicates, kill/landing rules, controls and pins.
2. `1b0b91e9` appends lines 121–157: five-not-four pilot erratum; C1 v2's 20 APPEND + 10 EDIT + 10 SYNTH population and version guard; C2's omitted-rule and sampled-no-harm qualifications.
3. `178d3353` appends lines 158–161, withdrawing the asserted cache success ceiling of 21/41. The 41/41 target is unchanged.

Counter/harness history contains only the initial commit and the pre-data v2 addition. This supports **before-data freezing**, not a separately committed v2 freeze before its own controls: v2 and those receipts first land together. The section's “appended 08:59Z” is an author timestamp in prose, not a separate commit-time receipt. The v1→v2 change must remain disclosed as a redesign, never described as v1 having survived unchanged.

## 2. Controls, shortcuts, and the missed pre-data requirement

### Recorded results

I inspected the identity, seed, PRED, exit and safety records throughout `controls/` and `controls/v2/`, and the w2 re-score summaries. All valid scored control receipts are `TARGET_MISSED`, exit 1. Exit-2 oracle/setup receipts are non-measurements, not negative controls.

| C1 shape | w1 v1 valid scores | Pre-data v2 score |
|---|---|---|
| Do nothing / empty stdout / absent tool | 0/41 | 0/41 |
| Empty `[[],[]]` | 0/41 twice | 0/41 |
| Named zero-valued-node empty variant | 0/41 twice | 0/41 |
| Junk | 0/41 twice | 0/41 |
| Static defaults | 0/41 twice | 0/41 |
| Snapshot cache | 1/41, 2/41; hash-fallback variant 1/41 twice | 4/41 |
| Root-only | 0/41 twice | 2/41 |
| Naive grep | 5/41 twice | **9/41** |
| No validation | 0/41 twice | 0/41 |
| Label/position keyed | 2/41, 1/41 | 2/41 |

| C2 shape | Pre-data valid scores |
|---|---|
| Do nothing / empty stdout | 0/51 twice per variant |
| Base tool | 22/51, 21/51; separate base receipt 22/51 |
| Brace stripper | 21/51 twice |
| Python-eval shortcut | 22/51, 23/51 |
| Label/position keyed | 21/51, **24/51** |
| Encoded embed/replay with base fallback | 21/51, 23/51, both embed_hits=0 |

The registration separately lists “V3-only reader,” but the saved roster/programs contain six named C2 shapes rather than a separately named seventh receipt. The base tool does function as a V3-only/no-expression witness: BASE and all 20 V3 cases pass, while evaluable ARITH cases fail. That is a reasonable explicit mapping, not evidence of an independently built seventh control.

W2's scored re-scores/strengthenings still meet neither target: C1's best is 13/41 (`w2/reports/RescoreK1NaiveGrep.md:39-78`); C2's w2 best is 23/51, below its retained w1 best 24/51. The measured-control kill condition was not triggered. These are particular negative controls, not proof that every possible shortcut was excluded.

The w1 cache-plus-suffix proposal was **not built/scored** by CritC1Design. V2's independent and destructive substrates attack it, but do not constitute a receipt for that unbuilt shape or a universal cache bound. C2's `embed_hits=0` is only a plaintext substring result: the encoded replay control itself demonstrates zero hits despite containing cached answers, while still missing 51/51.

### Concrete C1 protocol counterexample

`registration.md:86` requires each control, under the frozen counter, on **two fresh seeds before data**. Yet every `controls/v2/*.txt` contains one header, one `seed=`, one 41-case result and one exit. They first land in `1b0b91e9`. The w2 task text explicitly calls each “the L1's **one v2 receipt**” (`w2-spec.json:34-74`; also `w2-run.json` tasks).

Two v1 seeds are not two v2 seeds: twenty cases were changed and a new guard was added. W2's subsequent two-seed attacks are valuable negative evidence, but occur after the registry containing the data seats exists. No pre-data amendment waives the two-seed requirement.

**Impacted axes:** calibration, measurement provenance, strength of coverage evidence.

**Smallest safe correction:** state that the v2 pre-data control gate was incomplete. Preserve the actual target result and all receipts. Do not backdate post-data scores, erase “two fresh seeds,” or silently declare that original requirement satisfied. A clean successor attempt needs its actual complete control evidence before data. No extra score run now can repair the historical order.

## 3. Axis fit: the labels themselves survive attack

### C1: a new governed operation, not merely another animation count

`corpus/knowledge/hyprctl-verification-layer.md:158` held the 35-node/6-bezier count agreement but explicitly marked directive→entry expansion `[INF]`. CritC1Design's local search found only the old animation-enabled `getoption` check, not a static table resolver (`w1/reports/CritC1Design.md:29-45`). Registration names the new operation and an absent-tool before-state.

The official receipt binds actual committed tool SHA `2beda3f7…cab7d` to the unchanged v2 counter SHA `4ed70b54…6428`, records the expected compositor commit, and prints **41/41 TARGET_MET**, exit 0. This is evidence for a bounded new animation-table operation, so **coverage is defensible**. It is not merely re-scoring the old count observation. It does not establish all hyprlang grammar, rendering-effective inheritance, or animation-domain saturation.

### C2: repair of a held executable, not another acquisition

Round 25 already holds the static bind-table resolver, first-working round **25** (`SCORECARD.md:1683-1691`). Its independent arithmetic witness produced oracle arguments 101/102 versus literal brace expressions (`round-25/a3res/reports/ResC1Remeasure.md:106-124`). Repairing that existing command's result is **operability/quality work**, not fresh coverage merely because the test inputs differ.

The round-26 capability table does not manufacture a duplicate bind/expression capability row. Keep that identity and first-working round. The 51-case score is finite evidence, not a globally saturated operability score or universal preservation claim.

## 4. Strongest product counterexample: C2 deletes existing environment substitution

**Static source-traced witness [INFERENCE; not executed by this critic]:** with the frozen tool sandbox's non-secret `PATH=/usr/bin`, use this otherwise ordinary, non-arithmetic config line:

```ini
bind = SUPER, F13, exec, echo $PATH
```

| Authority/tool | Source-derived `arg` |
|---|---|
| Base resolver at `96101be5` | `echo /usr/bin` |
| Pinned hyprlang, with the oracle's `PATH=/usr/bin` | `echo /usr/bin` |
| Landed resolver at `a496b02a` | `echo $PATH` |

Evidence:

- The byte-identical base control retains `State.env = dict(os.environ)` and seeds `variables` from it (`controls/K2BaseTool.py:156-174`). Its substitution loop replaces `$PATH` (`:403-418`). Its source hash matches the base tool in the official before/control receipts.
- The actual base→landing diff deletes that state, initialization, and `get_var` environment lookup. The new tool starts with `self.variables = []` (`tools/mado-binds.py:567-582`); its loop only visits that list (`:811-820`). No expression operation is needed for this loss.
- Hyprlang v0.6.8's `recheckEnv()` copies environment entries; `clearState()` seeds its variables with them (`fetch/SrcHyprlangExpr.bin:543-550,1070-1075`). Its ordinary substitution loop uses those variables (`:736-752`).
- The harness sets `PATH=/usr/bin` in **both** the oracle and tool sandbox (`harness/oracle.py:154-155,235-237`), so this witness does not depend on exposing host credentials, HOME-path equivalence, or an extra external file.
- `bind = …, exec, …` is only table data; the standalone-exec stripping rule does not delete or execute it (`oracle.py:36,91-105`; `corpus/knowledge/bind-table-r25.md:70-72`).
- ExecArithToolB explicitly acknowledges missing environment seeding (`w2/reports/ExecArithToolB.md:219-226`) yet says at `:5-6` that no round-25 behavior was lost. The latter conclusion does not follow from BASE plus 20 V3 successes.

The w2 implementation contract additionally forbids `os.environ` seeding (`w2-run.json` shared data-seat context). That explains the cutover; it does **not** make the old behavior vanish or turn a narrower sample into preservation. The frozen generator does not add `$PATH`/other environment-variable witnesses, so it can miss this regression while honestly printing 51/51.

**Impacted axes:** operability directly; calibration if “no round-25 behaviour lost” is retained; capability identity/scope.

**Smallest safe correction:** do not accept universal preservation on the sample. Restore the held variable-input semantics without weakening sandbox confidentiality in an explicitly registered successor, and retain this non-secret old/candidate witness. If the no-environment implementation restriction is retained, the preservation promise and that restriction need an honest pre-data reconciliation. Trading an existing successful input class for arithmetic support is not a no-harm improvement. This report makes no product edit and claims no exercised old/new or oracle run.

## 5. Harm watch: what is supported, and what is not

### Other tools and source census

Read-only revision comparison shows:

- Base→C1 landing changes only `tools/mado-anims.py` (new) under `tools/`.
- Base→C2 landing changes only that new file and `tools/mado-binds.py`.
- Across base→`178d3353`, LOG/SCORECARD/QUALITY have only additions; README has no diff. SOURCES has five added rows and two old-row replacements. The two replacements only extend S158/S162 `used-by`, matching the logged disclosure; no old source identity/anchor was replaced.
- `evidence/sources-start.txt` and `sources-end.txt` both end `mado ok`, **exit=0**, with the same seven pre-existing W04 duplicate-URL warnings. These are retained receipts, not a census rerun by me. Five added identities S173–S177 support the reported 172→177 change.

Thus no other-tool-byte or census regression is established. This does not negate the C2 behavior deletion within its changed file.

### A fresh false statement in the lesson

`corpus/lessons/round-26.md:27` says the v2 cache receipt has **every EDIT and SYNTH case failing**. The very receipt cited says:

```text
CASE C28   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=no (EDIT:rewrite-animation+NEWSRC)
PRED-C1-r26-v2 cases_pass=4/41 verdict=TARGET_MISSED
```

Those are `controls/v2/K1SnapshotCache.txt:37,50`. It is **9/10 EDIT and 10/10 SYNTH failures**, not every EDIT. Registration's post-measurement correction and the lesson's Gate section already acknowledge this C28 witness; the mistake-table fix cell reintroduces the false assertion.

**Axis:** calibration. **Smallest safe correction:** append an exact erratum to that lesson statement; keep the original receipt and the withdrawn numerical ceiling. A negative cache result is still real, but the false stronger proof must not be credited as a fixed gate.

### Host safety/confidentiality is not “all counters were zero, therefore no harm”

The record reports **1330→1338** Hyprland catalog entries this round: five failed pilots and three data-seat probes. Important distinctions:

- Five-pilot attribution is the author's appended reconciliation, not a supplied per-attempt catalog-ID ledger (`harness/pilot-receipt.txt:21-25`). The global catalog count cannot independently assign every record.
- The data seats identify their own additional events: ExecAnimToolA's overflow probes, PIDs 2245463/2367290, two SIGABRT metadata records, explicitly **Storage: none** (`w2/reports/ExecAnimToolA.md:208-224`); ExecAnimToolB's self-source SIGSEGV, PID 2456401, +1 (`ExecAnimToolB.md:266-269`). These are isolated compositor crashes, not evidence of the live desktop crashing or eight stored core payloads.
- The official after receipts both show **1338→1338, delta=0**. That does not erase earlier incidents. The literal broader “every counter receipt delta 0” also needs qualification: ExecAnimToolB reports an earlier development counter run with **delta=1**, attributed to the concurrently running sibling's overflow probe (`:262-265`). Global delta is not run-owned attribution.
- Containment has positive independent evidence: private parent/runtime/network namespace, no host `/run/user` or card node, and unchanged live-instance observations. ReviewIsolation's `PILOT NOT_OK` comes from its known host-global residue clause, not a demonstrated display-isolation failure. Do not convert that token into an unobserved desktop breach.
- There is nevertheless an **observed confidentiality defect**, independent of case-label recovery: w1 K1LabelKeyed reports 261 readable launcher-environment keys through sandbox PID 1, and w2 ReviewIsolation independently reproduces its non-secret canary (262 keys). No credential values are reproduced here. Cleared child environment is not cleared launcher environment (`w1/reports/K1LabelKeyed.md:19-38`; `w2/reports/ReviewIsolation.md:50-84`).
- Both official measurements were launched with `env -i PATH HOME`, so those particular launches mitigate that leak. The unchanged reusable harness does not enforce that outer boundary (`oracle.py:232-238`). It also has the independently observed symlink-copy boundary issue and leftover empty runtime directories. Memory/output/disk exhaustion possibilities remain static risks, not exercised incidents in this review.

Both counter acceptors print coredump delta but do **not** require zero: C1 v2 `:370-374`, C2 `:220-225`. Thus target success alone cannot certify host safety. C2 still never requests/checks its actual oracle version; its named v0.56.2 authority is an enforcement gap, not evidence that the installed version was wrong. C1 guards the BASE compositor commit, not every ambient dependency.

**Impacted axes:** operability and calibration/provenance; host safety and confidentiality. **Smallest safe correction:** retain incidents and containment evidence separately; do not claim zero-round harm or a rejecting safety gate from passing comparisons. A successor harness must scrub the launcher's environment and establish its boundary with a non-secret witness, with run-scoped cleanup/accounting. Do not reproduce crash inputs or alter the pinned current harness from this review. Existing recorded crashes/exposure cannot be retroactively made absent by a later successful measurement.

## 6. Evidence operations and limits

Read all registration sections/errata, the Round-26 SCORECARD results, the full round lesson, control receipt identities/results, CritC1Design, CritC2Design and CritMistakes. Cross-checked the relevant rescore, implementation and isolation reports, old/new parser paths, pinned hyprlang environment source, AXES definitions, and the saved wave contexts/registry timestamps.

Read-only Git operations exercised: registration/counter/harness history; full registration patches; metadata/stat for `05319e0f`, `1b0b91e9`, `2b3487f7`, `a496b02a`; base→landing tool name diffs; base→`178d3353` documentation numstat/source diff; and base→`a496b02a` bind-tool diff. No git/jj write was run. These are history/content inspections, not fresh acceptance tests.

No counter, resolver, compositor, pilot, gate, build, test suite, linter, formatter, model, alternative judging runtime, or subagent was started. The PATH regression is explicitly a static trace, not an executed receipt. No reported failure was rerun for confirmation. No tool installed or updated. No process tree was started that needs cleanup. The only lane write is this report.
