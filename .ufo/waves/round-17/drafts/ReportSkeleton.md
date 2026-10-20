# Mado round 17 — {{ROUND_TITLE}}

## Work performed

Declared claims: **C1 {{C1_AXIS}}**, {{C1_DELTA}}; **C2 {{C2_AXIS}}**, {{C2_DELTA}}; **C3 {{C3_AXIS}}**, {{C3_DELTA}}. {{CLAIM_SELECTION_NOTE}}

- {{WORK_ITEM_C1}}
- {{WORK_ITEM_C2}}
- {{WORK_ITEM_C3}}
- {{SEAT_WAVE_SUMMARY}}
- {{PROCESS_DEFECTS_RETAINED}}
- {{OPERATOR_OR_WRAPUP_NOTE}}

Evidence: {{EVIDENCE_PATHS}}.

## Landed changes

**Pushed lane HEAD: `{{HEAD_SHA}}`.** {{LANE_CLEAN_STATE}}

| Commit | Landed work | LOG entry |
|---|---|---|
| `{{COMMIT_1}}` | {{COMMIT_1_WORK}} | {{COMMIT_1_LOG}} |
| `{{COMMIT_2}}` | {{COMMIT_2_WORK}} | {{COMMIT_2_LOG}} |
| `{{COMMIT_3}}` | {{COMMIT_3_WORK}} | {{COMMIT_3_LOG}} |

{{UNCHANGED_OWNED_FILES_NOTE}}

## Before → after measurements

Run from the lane root:

```sh
{{MEASURE_COMMAND_BEFORE}}
{{MEASURE_COMMAND_AFTER}}
```

{{RECEIPT_PATHS}}

| Claim | Before | After | Verdict |
|---|---|---|---|
| C1 {{C1_AXIS}} | {{C1_BEFORE}} | {{C1_AFTER}} | {{C1_VERDICT}} |
| C2 {{C2_AXIS}} | {{C2_BEFORE}} | {{C2_AFTER}} | {{C2_VERDICT}} |
| C3 {{C3_AXIS}} | {{C3_BEFORE}} | {{C3_AFTER}} | {{C3_VERDICT}} |

{{C1_RUBRIC_NOTE}}
{{C2_RUBRIC_NOTE}}
{{C3_RUBRIC_NOTE}}
{{CONTROL_RUNS_NOTE}}

## Sources & frontier

Source rows: {{SOURCE_COUNT_BEFORE}} → {{SOURCE_COUNT_AFTER}}; new ids {{NEW_SOURCE_IDS}} (reserved range S056–S069, assigned on integration by L1; drafts say `S0xx-pending`). A/B/C {{ABC_BEFORE}} → {{ABC_AFTER}}; mined/queued/rejected {{MQR_BEFORE}} → {{MQR_AFTER}}.

{{NEW_SOURCE_DESCRIPTIONS}}

Frontier advanced: {{FRONTIER_ADVANCED}}. Still open: {{FRONTIER_OPEN}}.

{{CENSUS_COMMAND}}

Before: {{CENSUS_BEFORE_EXIT}} (`{{CENSUS_BEFORE_PATH}}`)

```text
{{CENSUS_BEFORE_OUTPUT}}
```

After: {{CENSUS_AFTER_EXIT}} (`{{CENSUS_AFTER_PATH}}`)

```text
{{CENSUS_AFTER_OUTPUT}}
```

{{CENSUS_LIMITS_NOTE}}

## Trend verdicts

- **Expansion: {{EXPANSION_VERDICT}}**, {{EXPANSION_BASIS}}.
- **Quality: {{QUALITY_VERDICT}}**, {{QUALITY_BASIS}}.
- **Discernment: {{DISCERNMENT_VERDICT}}**, {{DISCERNMENT_BASIS}}.

Per-axis: {{PER_AXIS_VERDICTS}}. {{ADMISSION_STATEMENT}}.

## SHONEN

- [{{SHONEN_BOX_1_STATE}}] {{SHONEN_BOX_1_TEXT}}
- [{{SHONEN_BOX_2_STATE}}] {{SHONEN_BOX_2_TEXT}}
- [{{SHONEN_BOX_3_STATE}}] {{SHONEN_BOX_3_TEXT}}
- [{{SHONEN_BOX_4_STATE}}] {{SHONEN_BOX_4_TEXT}}

{{SHONEN_STATUS_NOTE}}

## Stale-lane

{{STALE_LANE_STATUS}}

## Tool installs

{{TOOL_INSTALL_LINES}}

## Wave seat counts, role mix, dead seats

- Seats dispatched: {{SEATS_DISPATCHED}}; registry members: {{REGISTRY_MEMBERS}}; registry agentIds recorded: {{AGENT_IDS_RECORDED}}.
- Role mix: {{ROLE_MIX}}.
- Reports present in `.ufo/waves/round-17/w1/reports/`: {{REPORTS_PRESENT}} of {{REPORTS_EXPECTED}}.
- Dead seats: {{DEAD_SEATS}}.
- Host-wide pause in force: {{PAUSE_STATE}}.

## Misroot sweep

{{MISROOT_SWEEP_RESULT}}

## L0

{{L0_LINES}}
