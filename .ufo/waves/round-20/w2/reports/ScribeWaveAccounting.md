# ScribeWaveAccounting — partly falsified: 85/85 seats reported and none dead, but the one-batch dispatch record is contradicted by two 85-spawn attempts

Full accounting table, hashes and commands: `.ufo/waves/round-20/w2/ScribeWaveAccounting/accounting.md`.

## Findings

1. **Seats per role (holds).** 85 members: executor 21, scout 20, reviewer 15, scribe 8, critic 7, connector 6, revenger 3, sentinel 2, mutation-tester 2, simplifier 1. Evidence: `jq -r '.members|to_entries[]|.value.role' .ufo/waves/round-20/w1/reports/swarm-registry.json | sort | uniq -c`. `spec.json` roles and names are identical to the registry; `assignments.json` agentIds are identical to the registry; `record.json` agentIds are identical and none null.

2. **Reports per member, joined by name (holds).** 85 registry members, 85 `reports/*.md`, 0 missing, 0 orphan. Every report header names its filename seat (`HarmWatch20` header carries `-3` suffix). Evidence: `comm -3` of sorted registry keys vs `ls reports/*.md` basenames, empty.

3. **Dead seats (holds: 0).** Every member has a non-empty report. Keyword hits (`killed`, `failed`, `dead seat`, `reportless`) refer to mutation kills or round-19 facts, not wave-1 seats.

4. **Task-result attempts (partly falsified).** `task-result.json` records `attempts: [[1,"16:36",85],[2,"16:39:52",85],[3,"16:42:57",0]]` (local -03). `dispatch.json` records `counts {spawn 85, resume 0, total 85}` and instructs a single batched taskCall. Two attempts each recorded 85 spawns about 3 minutes apart, so the one-batch record is not supported as stated. All 85 agentIds carry `-3`; no `-1`/`-2` IDs exist in wave 1. Whether a duplicate spawn occurred is [UNK]; a re-record rather than a second spawn is [INFERENCE] only. Routed to L1, consistent with the unresolved item in `reports/ScribeLog.md` item 6.

5. **Non-report files.** `drafts/` holds 8 scribe drafts that differ by sha256 from their `reports/` counterparts; the `reports/` copies are the ones counted. `cases/`, `patches/`, `corpus/` are not reports.

## Limits

- Report content was not verified; only identity, headers and dead-seat keywords.
- Duplicate-spawn question cannot be settled from wave-1 artifacts; no session transcripts were read.
- Registry `item` is null for all seats.
- Timezone mapping (-03 to UTC) is [INFERENCE] from matching timestamps.

## Installs

none
