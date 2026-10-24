# ScoutLaneState — published self-assessment vs repo (read-only)

Seat: ScoutLaneState · wave round-32/w1 · executed 2026-10-24 at lane tip
`91862344b9fddbb5b4c3a9977acc776632993799` (`git rev-parse master`).

## 1. Axis-table publications in `SCORECARD.md`

Literal finding: **no line in `SCORECARD.md` starts with the token `Axis
table re-derived at`**. The axis re-derivation publications exist but are
worded differently; verbatim lines (line numbers per `read`):

Round 30 publication — `SCORECARD.md:1908-1910`:

```text
`446dc396`. Axis selection re-derived every scored sub-axis at base
(criterion 22): calibration literal 0.7000 / resolved-active 0.7949 is
lowest; coverage-nav 0.9535; sourced-art and operability 1.0.
```

(begins mid-paragraph on `:1907` `Base `8f51071b` (round-29 closure:
admitted; index gap routed). Data commit`)

Round 31 publication — `SCORECARD.md:2014-2017`:

```text
before the data commit `f621e3c0` (base `274f7355`, r30 tip). Axis table
re-derived at base (criterion 22): navigation 43/43 = 1.0; calibration
resolved-active 39/40 = 0.9750 (lowest — criterion 35's mis-scoped M23-7);
sourced-art 1.0; operability selftest 9/9 = 1.0. Three claims, three
```

(line 2018 completes the sentence: `distinct surfaces; each measured without
the others.`)

## 2. Instrument re-runs at tip `91862344b9fddbb5b4c3a9977acc776632993799`

### `python3 -I quality/check-index.py --rev 91862344b9fddbb5b4c3a9977acc776632993799 --repo .`

```text
MADO_INDEX: rev=91862344b9fddbb5b4c3a9977acc776632993799 indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
EXIT=0
```

### `python3 -I .ufo/waves/round-31/c2/count.py 91862344b9fddbb5b4c3a9977acc776632993799`

```text
counter=c2-grounding-r31-v2 rev=91862344b9fddbb5b4c3a9977acc776632993799
METRIC literal lines=42/54 fraction=0.7778
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40, 48]
METRIC active=41 resolved_active=41 fraction=1.0000
WARN criterion 19: outside 'R13-V1' unverifiable (no lane path)
WARN criterion 22: outside 'R16-V1' unverifiable (no lane path)
WARN criterion 23: outside 'R17-V1/V2/V5' unverifiable (no lane path)
WARN criterion 26: outside '/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports' unverifiable (non-lane path)
WARN criterion 26: outside 'R18-V1/V3/V4' unverifiable (no lane path)
WARN criterion 28: outside 'R19-V3' unverifiable (no lane path)
LINE 1 superseded excluded
LINE 2 superseded excluded
LINE 3 superseded excluded
LINE 4 superseded excluded
LINE 5 superseded excluded
LINE 18 superseded excluded
LINE 19 superseded excluded
LINE 20 superseded excluded
LINE 32 superseded excluded
LINE 38 superseded excluded
LINE 39 superseded excluded
LINE 40 superseded excluded
LINE 48 superseded excluded
PRED-C2-r31-v2 verdict=TARGET_MET
EXIT=0
```

### `python3 -I quality/check-index.py --selftest`

```text
MADO_INDEX_SELFTEST: 12/12 assertions passed
EXIT=0
```

## 3. Published vs re-derived per axis

Benchmark: round-31 publication, which records **before** (base `274f7355`)
and **after** (data `f621e3c0`) values; the tip value is compared to the
published **after** value.

| Axis | Published (r31 base → after `f621e3c0`) | Re-derived at tip | Verdict |
|---|---|---|---|
| navigation / index completeness | 43/43 = 1.0 (unchanged base→after) | `indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | **MATCH** |
| calibration / resolved-active citations (v2 rubric) | 39/40 = 0.9750 → 41/41 = 1.0000 TARGET_MET; literal 40/52 → 42/54 | `resolved_active=41/41 fraction=1.0000`; `literal 42/54 fraction=0.7778`; `PRED-C2-r31-v2 verdict=TARGET_MET` | **MATCH** |
| operability / gate selftest | 9/9 at base → `12/12 assertions passed` at `f621e3c0` | `MADO_INDEX_SELFTEST: 12/12 assertions passed`, exit 0 | **MATCH** |
| sourced-art | published 1.0 | *not covered by the three named instruments* | **NOT COVERED** |

No axis is STALE against its published post-commit value. The 0.9750 figure
is the round-31 *base* reading (criterion 35 mis-scoped M23-7), repaired by
the round-31 data commit — the tip reading 41/41 is the published *after*
value, not drift.

## 4. `SHONEN.md` four boxes (verbatim)

`SHONEN.md` (12 lines) verbatim:

```text
# mado-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  Historical assertion: corpus/knowledge/executor-test-sufficiency.md (MADO-R3-4); outside-lane verifier independence is not established by the inherited record.
- [~] At least one end-to-end domain task executed and logged in LOG.md
  Historical assertion: corpus/knowledge/config-health-report-r3.md and LOG.md round 3 (VER-M3); no new end-to-end desktop task or outside-lane verification in fleet round 1.
- [~] Instructions executable by an agent without oral context
  Historical assertion: corpus/knowledge/executor-test-sufficiency.md (MADO-R3-4); dispatched subagents do not satisfy the current outside-lane promotion rule.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  Historical assertion: corpus/knowledge/province-accuracy-selfaudit.md round-5 receipt (VER-M4B); PROVINCE.md remains the read-only boundary, not a fresh outside-lane approval.
```

Pointer resolution from repo root (test `-f`):

| Box | Named pointer(s) | Resolves? |
|---|---|---|
| 1 (decision tables) | `corpus/knowledge/executor-test-sufficiency.md` | EXISTS |
| 2 (end-to-end task) | `corpus/knowledge/config-health-report-r3.md`; `LOG.md` | EXISTS; EXISTS |
| 3 (executable instructions) | `corpus/knowledge/executor-test-sufficiency.md` | EXISTS |
| 4 (no cross-domain bleed) | `corpus/knowledge/province-accuracy-selfaudit.md` | EXISTS |

All four boxes are `[~]` (partial), each hedged with a "Historical
assertion" and an explicit note that outside-lane verification is not
established — the file's own text does not claim current promotion
clearance.

## Limits

- `sourced-art` has no named instrument in this scope; its 1.0 publication
  was not re-derived.
- The prompt's expected literal line prefix (`Axis table re-derived at`)
  matches no line; nearest matches reported above verbatim.
- WARNs in the C2 counter are outside-scope pointer advisories emitted at
  every revision (including at `f621e3c0`); they do not affect the verdict.
