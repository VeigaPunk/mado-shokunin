# WavePaths — round 16 w1 path-safety review

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin` (baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`, HEAD matches).
Scope: absolute lane paths and relative `Report:` trailer safety for `.ufo/waves/round-16/w1/dispatch.json`, `spec.json`, and `reports/swarm-registry.json`. Read-only. No fleet, sibling, or lane file was edited. No installs, no package operations, no build/lint/test runs.

## Verdict

Trailer confinement holds: every dispatched `Report:` trailer is relative, in-lane, unique, and carries the expected member name. Two artifact-level defects remain: spec.json drift and an undefined frozen-input location for the SafetyGate. Neither lets a seat write outside the lane, but both can misdirect an executor or lose report obligations on a re-dispatch.

## Findings by severity

### F1 — Medium: `spec.json` drops the Lane-bounds and Report trailer on all 64 items

- `spec.json` items are strict prefixes of the dispatched `taskCall.tasks[].task` text (64/64), but every spec item omits the trailing `Lane bounds: ...` and `Report: write your scoped findings to .ufo/waves/round-16/w1/reports/<Name>.md` lines (64/64 missing `Report:`, 64/64 missing `Lane bounds`).
- `dispatch.json` carries the trailer on all 64 tasks, so the executed wave is conforming. `spec.json` is the persisted mirror; a re-dispatch or resume driven from it would silently lose each seat's report obligation and its lane-bounds rule.
- Evidence: prefix check and spec-vs-dispatch tail comparison for `PlanningWalk` (spec ends at the rubric sentence; dispatch continues with Lane bounds and Report).
- Recommendation for the integrator (not edited here): regenerate `spec.json` items from `taskCall.tasks` so the two artifacts agree.

### F2 — Medium: SafetyGate `--frozen DIR` names no directory and no create target

- The SafetyGate task asks for `--frozen DIR` that "verifies expected.json input digests for plan.json and policy.json". No `DIR` is specified anywhere in the dispatch.
- The SafetyGate `Create ONLY` list is exactly `tools/mado-action-plan.py` and `.ufo/waves/round-16/safety-policy.json`. It does not include `expected.json`, `plan.json`, or a frozen directory. Other tasks (SafetyCases → `safety-cases.json`) also do not provide these.
- The bare name `policy.json` in the frozen clause does not match the created `safety-policy.json`. This is a naming ambiguity that could make the executor read or write the wrong file.
- Risk: an executor chooses a frozen location of its own, possibly outside the lane or outside the create-only list. Not observed as an existing violation; this is a missing contract.
- Recommendation: name one lane-relative frozen directory (e.g. `.ufo/waves/round-16/frozen/`) in the SafetyGate create list, and reconcile `policy.json` with `safety-policy.json`. FrozenDesign and FrozenInputs reviewers may resolve the design, but the write path belongs in the executor's create list.

### F3 — Low: trailing sentence period glued to a create target

- MeasureBuild: `Create ONLY /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-16/measure.py. Reuse ...`. A literal token parser extracts `measure.py.` (trailing dot). The intended file is `measure.py`.
- Low risk on its own, but a literal create-only checker would fail to match.

### F4 — Low: bare-name references depend on implicit base

- `QUALITY.md` (QualityGround and L1 ownership) resolves only as `corpus/QUALITY.md`. The bare name is unambiguous in practice but not lane-root relative.
- `round-15/measure.py` resolves only as `.ufo/waves/round-15/measure.py` (present, 11737 bytes). Correct, but implicit.
- Recommendation: write these as full lane-relative paths in future spec revisions.

### F5 — Info: no fleet-root write target

- The fleet root `/home/vgpnk/Projects/shokunin/.ufo/` (with its own `waves/`, `reports/`, `state/`) is not referenced by any dispatched task. The only absolute paths in dispatch/spec are inside the lane, plus `/home/vgpnk/.omp/agent/RULES.md` in the tooling directive.
- `RULES.md` is outside the lane and is a read-only instruction source named by the contract. I did not open it (no installs this round). It is not a write target and is not a credential or `agent.db*` path.

### F6 — Info: git tracking of round-16 artifacts

- `git status --porcelain -- .ufo/waves/round-16` reports `?? .ufo/waves/round-16/` (untracked). `.gitignore` does not exclude it; `git check-ignore` returned no match. The round-15 wave reports are tracked (65 files), so round-16 reports will need an integrator `git add`. Seats commit nothing per contract.

### F7 — Info: registry bookkeeping

- `reports/swarm-registry.json` has 64 members with populated `agentId` (0 null), including `WavePaths → MadoR16.WavePaths`, matching the dispatch roles 1:1 (no role mismatches, no duplicates, no names outside the registry).
- The registry file mode is `0600` while sibling reports are `0644`. Cosmetic; same-user readers are unaffected.

## Checks performed (all read-only)

1. Enumerated every absolute path in `dispatch.json` and `spec.json`: 9 unique, all inside the lane except `/home/vgpnk/.omp/agent/RULES.md` (see F5).
2. Extracted each task's `Report:` trailer path: 64/64 conforming (`.ufo/waves/round-16/w1/reports/<Name>.md`), 64 distinct targets, 0 absolute, 0 `..`, 0 escaping after `normpath` join with the lane root, trailer is the last line in every task.
3. Created-target check: every `Create ONLY` path is in-lane (4 targets, see F2/F3).
4. Spec vs dispatch: 64/64 prefix match; 64/64 missing trailer in spec (F1). Context strings identical.
5. Registry vs dispatch membership and roles: 64/64 match.
6. Referenced repo file existence: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `round-15/measure.py` (as `.ufo/waves/round-15/`) present. External Waybar sources (`custom.cpp`, `man/waybar-custom.5.scd`) absent as expected (raw GitHub, not lane). Gate fixtures `expected.json`, `plan.json`, `policy.json` absent (F2).

## Residual risk and verification gaps

- Only the dispatch/spec/registry artifacts were checked. The other 63 seat reports were not reviewed for trailer or write-path compliance; they are not yet present in full.
- Path safety was not verified at runtime: no seat's actual writes were observed. Only declared targets were checked.
- No checks were run on the content of the gate, measure, or case files; those belong to L1's single post-integration verify.

## Tool installs

None. This round installs nothing (contract). No package or service operations.
