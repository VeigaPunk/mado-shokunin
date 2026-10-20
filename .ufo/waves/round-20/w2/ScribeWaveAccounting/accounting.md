# Round 20 wave 1 — wave accounting (mado-r20-w1)

Scope: `.ufo/waves/round-20/w1/` in `/home/vgpnk/Projects/shokunin/mado-shokunin` (lane tip a4046a8). Read-only over wave-1 artifacts; the only writes are this file and the report.

## Source hashes (sha256)

| file | sha256 |
|---|---|
| `w1/assignments.json` | `21d901eee9c97723f1fd8652e4b229fae634b1379367f907c2163a8d5085bb6a` |
| `w1/reports/swarm-registry.json` | `387ee4752a396563822d893fdddcbf188067f2102aa54cbe7d2a9b451f0c7e15` |
| `w1/task-result.json` | `5bb18e899b6adb47d500dc96e946dce70c29319875a3c9f616fda918b0e64513` |
| `w1/dispatch.json` | `8f26ea67dd4f98afdcc724886132b0139cb9f2a6371057ca38f43fab231eb689` |
| `w1/record.json` | `5483f5d22af5c5ba720bc453bc93532d64247405b6cbf31c39dbc30907d4b821` |
| `w1/spec.json` | `a70afe1fdd3b10266e0e8ea41df1edf35f068b5b8814a6afb22f1834c78cdfef` |

## Seats per role

Command: `jq -r '.members|to_entries[]|.value.role' reports/swarm-registry.json | sort | uniq -c`

| role | seats | reports present (name join) | dead |
|---|---:|---:|---:|
| executor | 21 | 21 | 0 |
| scout | 20 | 20 | 0 |
| reviewer | 15 | 15 | 0 |
| connector | 6 | 6 | 0 |
| critic | 7 | 7 | 0 |
| scribe | 8 | 8 | 0 |
| revenger | 3 | 3 | 0 |
| sentinel | 2 | 2 | 0 |
| mutation-tester | 2 | 2 | 0 |
| simplifier | 1 | 1 | 0 |
| **total** | **85** | **85** | **0** |

Cross-checks:
- `assignments.json` has 85 keys; its values equal registry `agentId`s pair-for-pair (`diff` empty).
- `spec.json` has 85 items; names and roles match the registry exactly (`diff` empty on `name role` pairs). Role counts from `spec.json` equal the registry counts above.
- `record.json` has 85 members, 0 null `agentId`s, member names and `agentId`s identical to `reports/swarm-registry.json`.
- Registry `kind` is `spawn` for all 85 (`resume` 0). `item` is null for all 85. Registry value keys: `agentId, item, kind, role`.

## Reports present per member (join by name)

- `reports/*.md`: 85 files. Registry members: 85. Registry-without-report: none. Report-without-member: none.
- `reports/` also holds `swarm-registry.json` (the only non-`.md` entry).
- Every report's first-line seat name equals its filename. One exception in form: `HarmWatch20.md` header reads `# HarmWatch20-3`, i.e. the agentId suffix, not the bare seat name. Name identity holds after stripping `-3`.
- Report sizes: min 2,781 B (`RevR19V5Wording.md`), total 1,045,056 B.

## Dead seats

None. Every member has a non-empty report with a seat-name header. Keyword hits in report bodies are not wave-1 dead-seat evidence:
- `MutVcsTip` "killed" = mutation kills.
- `SrcBashErrexit` "failed" = round-19 failed `mount` discussion.
- `ScribeCorrections` "dead-seat count" and `RevR19V6Seats` "reportless" refer to round-19 registry (86 members) and are not wave-1 facts.

## Task-result attempts

`w1/task-result.json` `attempts` (fields `[attempt, time, spawned]`):

| attempt | time (file/local, -03) | UTC (inferred) | spawned |
|---|---|---|---:|
| 1 | 16:36 | 19:36Z | 85 |
| 2 | 16:39:52 | 19:39:52Z | 85 |
| 3 | 16:42:57 | 19:42:57Z | 0 |

Corroborating times: `dispatch.json` mtime 16:36:34 local; `swarm-registry.json` `createdAt` `2026-10-20T19:36:34.817Z`, `updatedAt` `2026-10-20T19:43:13.856Z`; `task-result.json` mtime 16:42:57; system TZ reads `-03`. The -03 to UTC mapping is [INFERENCE] from these matching minutes.

Single `text` field in `task-result.json`: "Spawned 85 background agents…", listing 85 jobs, all `-3` suffixed.

`w1/dispatch.json`: `counts {spawn 85, resume 0, total 85}`; `note` says issue exactly one batched taskCall; `taskCall` carries 85 tasks; `resumeSends` empty; `compaction.applied` false.

**Dispatch-accounting anomaly (unresolved, same as ScribeLog item 6):** two recorded attempts each report 85 spawns (attempt 1 and attempt 2, ~3 min apart), which is inconsistent with the one-batch rule as recorded. Whether a duplicate spawn occurred is [UNK]. Artifacts show one agentId set (85 IDs, all `-3`), no `-1`/`-2` IDs anywhere in wave 1, and a single registry with `createdAt` at attempt 1. That is consistent with attempt 2 being a re-record rather than a second spawn, but no artifact proves it [INFERENCE]. Attempt 3's 0 is consistent with a no-op re-check.

## Non-report artifacts (not counted as reports)

- `drafts/`: 8 scribe drafts (`ScribeProvince, ScribeShonen, ScribeKnowledge, ScribeLog, ScribeCorrections, ScribeMistakes, ScribeSkill, ScribeQuality`). Each differs by sha256 from its `reports/` counterpart; `reports/` copies are the counted ones [INFERENCE: reports/ are later/final].
- `cases/` 200 files, `patches/` 22 files, `corpus/` 1 file. Not reports; not counted.

## Limits

- Report bodies were checked for header identity and dead-seat keywords, not for content correctness (out of scope).
- Attempt duplication cannot be resolved from wave-1 artifacts; no session transcripts were read (per host/data rules).
- Registry `item` is null for all seats; no per-item join was possible.
- Round-19 "25 dead seats" and "reportless" claims are round-19 facts; not re-measured here.

## Installs

none
