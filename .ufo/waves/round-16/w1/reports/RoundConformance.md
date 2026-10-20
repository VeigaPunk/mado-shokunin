# RoundConformance — mado round 16 (w1) contract census, identity order, report-last

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` (verified as HEAD at review time).
Scope: read-only review of `.ufo/waves/round-16/w1/{spec.json,dispatch.json,reports/swarm-registry.json}`, lane git history, and mtimes. No build, lint, test, install, package, or live probe was run. No commits, no sibling edits, no delegation.
Pre-work read: `corpus/lessons/round-15-verifier-spotcheck.md`, `AGENTS.md`, `~/.omp/agent/RULES.md`. Tooling: nothing installed or updated by this seat.

## Census (verified)

| Check | Result |
|---|---|
| spec.json items | 64; names unique; roles executor 3, scribe 10, connector 7, scout 12, reviewer 19, sentinel 3, critic 8, simplifier 2 |
| dispatch `registry.members` | 64 keys = spec names; kind spawn 64; roles equal spec roles |
| dispatch `taskCall.tasks` | 64; names and order equal spec; agent field equals spec role for all 64; `context` equals spec `context` |
| `counts` | spawn 64, resume 0, total 64; `resumeSends` empty; `compaction.applied` false |
| `model` keys in dispatch | none |
| `Report:` trailer per task | exactly one per task, 64 distinct, each equals `.ufo/waves/round-16/w1/reports/<Name>.md` (exact match, 64/64) |
| prompt relation spec→task | all 64 task texts = spec prompt + `Lane bounds` line + `Report:` line; spec.json contains neither trailer nor lane-bounds line |
| peer addressing | no task names `Main` or `agent://all` |
| write targets | five `Create ONLY` targets, each owned by one seat (`tools/mado-action-plan.py`, `.ufo/waves/round-16/{safety-policy.json,measure.py,safety-cases.json,waybar-draft.txt}`); no duplicates; no L1-owned file named as a write target |
| registry on disk | `reports/swarm-registry.json`: 64 members, roles equal dispatch, every agentId equals `MadoR16.<name>`; the only field differing from dispatch is `agentId` (null pre-spawn → populated post-spawn), which is runtime state, expected |

Execution-verb census of the dispatched prompts: every hit is a prohibition, a feature to implement (`--selftest`, `--frozen` in SafetyGate), or a read-only review. No seat is instructed to run a build, test, lint, pacman, or live command. The `sudo`, `restart`, `hyprctl`, `credential`, `agent.db` hits are all negative-scope text. [Only the three executor seats write files.]

## Findings by severity

### F1 — MEDIUM — dispatch grants a delegation exception the contract forbids
- Contract (`spec.json:3`, `# Contract`): "No delegation."
- Dispatched `taskCall.tasks` for `SafetyGate` (`dispatch.json:426`), `MeasureBuild` (`:431`), and `SafetyCases` (`:436`) carry `Lane bounds: leaf member — no subagent dispatch except your single labrat.`
- The other 61 seats carry `… — no subagent dispatch.`
- `grep -c labrat spec.json` = 0: the exception exists only in the dispatched batch, not in the spec items. "labrat" is undefined anywhere in the lane.
- This environment has agent spawning disabled, so the clause is unrealizable here, but it is an authority ambiguity inside a batch that already spawned.
- Recommendation for L1/planner: strip the clause from the dispatch record and treat the three seats as leaf members; or record an explicit operator decision if a labrat was intended. No seat should act on it.

### F2 — MEDIUM — MeasureBuild prompt wording can be read as fail-open
- `spec.json:15` and `dispatch.json:431` (MeasureBuild item): "Missing item exits 0 probe."
- Read literally, a missing item exits 0. That conflicts with the C2 fail-closed posture and with SafetyGate's "unknown/malformed fail closed" convention.
- The sentence is ambiguous (it may mean "missing item → exit-0 probe" or "exit 0 is a probe"). [INFERENCE: intent unclear from text alone.] Clarification required before MeasureBuild's `measure.py` is judged.

### F3 — LOW — "two waves" is not present in the artifacts
- The assignment names "two waves"; the artifacts describe one wave only: `wave: mado-r16-w1`, `counts.total` 64, `resume` 0, dispatch `note` ("one-swarm-per-wave"). No `w2` directory, no spec/dispatch reference to a second wave, and no "second wave" text in any prompt.
- The round-15 closure records "no optional second wave." Either the second wave is out of scope for this round or it is not yet planned. Cannot be verified from artifacts; planner must confirm.

### F4 — LOW — SkillSafety drafts SKILL wording while SKILL.md is L1-owned
- Task `SkillSafety`: "Draft SKILL current host pause superseding round15 future install wording."
- The contract says L1 owns `SKILL.md`; the prompt names no write target, so this is a draft-into-report instruction. Live tree shows `M SKILL.md` (mtime 05:39:23).
- Confirm the seat writes only `reports/SkillSafety.md` and does not touch `SKILL.md`.

### F5 — LOW (historical, not a round-16 defect) — baseline commit carries non-lane identity
- `AGENTS.md`: "Commits carry the lane identity."
- Lane commits `97c3583`, `5f13870`, `9ebd737` are `mado-shokunin <mado@shokunin.local>` (author = committer).
- Baseline `32c4fda` (`round-15 verifier spot-check (integrator, hyaku)`, +291 lines, sole file `corpus/lessons/round-15-verifier-spotcheck.md`) is `protocol-shokunin <protocol@shokunin.local>`.
- The baseline is supplied, so this is not a round-16 violation. It must not be cited as precedent: round-16 lane commits made by L1 must carry the mado identity.

### F6 — INFO — commit/report order: round-15 held; round-16 not yet committed
- Round-15 identity order (verified with `git show -s`): content `5f13870` 04:35:06 → outcome `9ebd737` 04:38:09 → report `745f1a9` (parent repo, mado identity) 04:40:16 → non-author closure `32c4fda` 04:47:43. Report-last held.
- Round-16 obligations for L1 (not seats): content commit(s) → outcome commit → report commit → closure last; all lane commits under `mado-shokunin <mado@shokunin.local>`; seats commit nothing.
- Live tree at 05:40: tracked modifications `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` (uncommitted); round-16 artifacts untracked. Integration is in progress; ordering cannot yet be verified.

### F7 — INFO — reserved ids S053–S055 are in-progress, not baseline
- Spec reserves S053 (Waybar custom man), S054 (custom.cpp), S055 (closure own-work safety).
- Working-tree `corpus/SOURCES.md` (mtime 05:39:45, uncommitted) now contains exactly one row each for S053, S054, S055 plus round-16 prose. `git show HEAD:corpus/SOURCES.md` and `git show 9ebd737:corpus/SOURCES.md` contain zero matches for `S05[345]`.
- No duplicate ids observed. Ownership is L1's; this is noted so nobody mistakes the in-progress rows for baseline content.

### F8 — INFO — registry and report-last mtimes consistent
- `reports/swarm-registry.json` mode is `0600` (other lane files `0644`); harmless, noted.
- Report-last by mtime: `waybar-draft.txt` 05:40:02 → `reports/WaybarDraft.md` 05:40:14 (report after artifact). `measure.py` 05:40:25 with no `MeasureBuild.md` yet, consistent with report-last. `source-bindings.json` 05:39:28 precedes `SafetyReceipt.md` 05:39:59.
- These are live snapshots; the final ordering must be re-checked after the wave completes.

## Obligations confirmed satisfied (census level)
- Every seat has exactly one report path, unique, under `reportDir`.
- Lane bounds: 61/64 "leaf, no subagent dispatch"; 3 exceptions (F1).
- No seat is pointed at Main or `agent://all`.
- No pacman, install, build, test, or live command is directed in any dispatched prompt.
- The dispatch batch is the single validated wave (one task call, spawn 64).

## Residual risk
- F1 and F2 are the only findings that can change seat behavior. F1 is an authority ambiguity in a batch already spawned; F2 can produce a fail-open measurement if read literally.
- The round is mid-integration: the working tree has uncommitted L1 edits. Commit identity and report-last ordering cannot be closed until integration lands.

## Verification gaps
- Did not verify the content of any seat's output (scope: contract census only).
- Did not verify `measure.py`, `tools/mado-action-plan.py`, or any gate; none executed (per contract).
- The "two waves" premise (F3) cannot be confirmed from artifacts.
- Live-tree state is a snapshot at 05:40 (-03:00); later writes by other seats will change mtimes and status.

## Tooling record
No tool installed, updated, or removed. No package or service operation. Reads only: `git` read subcommands, `stat`, `grep`, and JSON parsing of lane artifacts.
