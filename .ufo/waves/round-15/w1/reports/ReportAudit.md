# ReportAudit — mado round 15 report contract and evidence checklist

Seat: ReportAudit (scribe, read-only). Wave: mado-r15-w1. Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Scope: read the round-prompt report contract and the round-15 wave artifacts; propose an evidence checklist. No edits outside this file, no commits, no tests/gates/builds/linters/smoke runs, no live probes, no input-event access, no credential or `agent.db` access, no omp CLI launch, no subagent dispatch.

## 1. Contract read (sources)

- `/home/vgpnk/Projects/kimi-shokunin/templates/round-prompt.md` §4 (report contract), §2b (frontier step), §3 (L2 floor), §5 (commit/push). Read.
- `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-15.md` §4 — renders the canonical contract with path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-15/mado.md` (fleet report, owned by L1). Same six headings, same marker rule.
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/mado.md` — precedent; headings at lines 3, 21, 33, 82, 122, 128 are exactly the six required sections in order.
- `mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md` — non-author precedent: checks six sections, `[~]` count, census command, tool-install record.
- `mado-shokunin/SHONEN.md` — four `[~]` boxes; no `[x]` (no named non-author verifier on record).
- `/home/vgpnk/.omp/agent/RULES.md` — tooling directive (install/update allowed via official channels; record every install in the report).

Required sections (in order): **Work performed · Landed changes · Before → after measurements · Sources & frontier · Trend verdicts · SHONEN**. Marker rule: missing `Work performed`, `Landed changes`, `Before → after measurements`, `SHONEN`, placeholder text, or absence of evidence pointers = round **failed**. `Sources & frontier` and `Trend verdicts` missing = `ok` plus a conformance defect, not a marker failure.

## 2. Evidence checklist — six required sections

| Section | Required evidence (pass condition) | Source for the checklist |
|---|---|---|
| Work performed | Opens by naming the declared claims (1–3) with target axis. Declared claim for round 15: **C1 coverage** (U1–U5 5/7 → U1–U6 6/7). One bullet per work item, each with path:line, command output, or commit hash. Must cover R14-V1 as a separately labelled, unscored correction. Must state unexercised delivery/IME/kernel limits as retained unknowns. | contract §4; wave `context` (Goal); R14-V1 in `corpus/lessons/round-14-verifier-spotcheck.md` lines 169–170 |
| Landed changes | Each change tied to a LOG.md entry and to the commit hash carrying it. Explicit R14-V1 correction: append a correction mapping the provisional headers of `.ufo/waves/round-14/w1/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt` (lines 3–4: `input_binding: provisional worktree snapshot`, old whole-gate hashes) to derived target `cd1d73d7…`. Historical bytes kept. Future standalone mutation receipts bind measured_commit + gate_sha256. | round-14 verifier lines 169–170; contract §4 |
| Before → after measurements | One per claim (C1 only). Each with the counting command and the measured commit. Coverage counting command is the round-14 recipe (`corpus/SOURCES.md` + `corpus/knowledge/` joined on `covers: U[1-7]`, `mined` status). Before = committed round-14 head `97c35835…` / `ea0446f…` depending on baseline; after = measured commit. Must print the U1–U6 set and the count. | `corpus/lessons/round-14-verifier-spotcheck.md` lines 49–86 (recipe) |
| Sources & frontier | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` run at round start and round end, both outputs and exit codes pasted; exit 0 required at end. SOURCES rows before→after; rows added by tier; rows touched old→new logged in the lesson; frontier rows advanced. At least one of the round's claims cites an `S###` row **opened this round** with a ≤25-word located quote. A mined mistake in `corpus/lessons/round-15.md ## Mistakes` (class · evidence pointer · captured-by · fix) — `corpus/lessons/round-15.md` does **not yet exist** (checked). Conformance line must start `SOURCES:` and name the state. | contract §2b; `scripts/sources-census.sh` present |
| Trend verdicts | Exactly three verdicts: `expansion`, `quality`, `discernment`, each one of `improved` / `harmed` / `unchanged` / `unprovable-but-better`, with evidence. No scalar. `unprovable-but-better` requires a named non-author reviewer and reasons. | contract §4; `mado-round-15.md` §2 item 8 |
| SHONEN | One line per SHONEN.md box (currently four). `[x]` only with a named non-author verifier (none exists → keep `[~]`). `[~]` requires a resolvable pointer. Pointers checked present: `corpus/knowledge/executor-test-sufficiency.md`, `corpus/knowledge/config-health-report-r3.md`, `corpus/knowledge/province-accuracy-selfaudit.md`, `corpus/knowledge/output-colour-boundaries-r14.md`. | `SHONEN.md`; contract §4 |

Additional checks for the L1 report:
- Report path: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-15/mado.md` (fleet repo, committed separately).
- Wave-level tool-install record (RULES.md): either "Tool installs/updates: none" or one line per install with tool, version, channel, reason. Round 14 precedent: `wlr-protocols r112.a741f0a-1`, official pacman extra, channel `sudo pacman -S --needed --noconfirm`.
- Axes: state in Work performed whether operability is in or out of scope (see §4 finding F2).

## 3. Wave role mix, tool installs, stale lane — observed

### 3a. Role mix (read-only, from `.ufo/waves/round-15/w1/spec.json`, `dispatch.json`, `reports/swarm-registry.json`)

- Spec items: **64**, unique names 64. Registry members: **64**, all `kind: spawn`, no name diff against spec, no role mismatch against spec.
- Role counts (spec = registry = dispatch `taskCall.tasks[].agent`):

| Role | Count | Floor (round-prompt §3) | Status |
|---|---|---|---|
| executor | 3 | ≥3 | met (MeasureBuild, ReceiptCorrection, InputDraft) |
| scout | 13 | ≥1 | met |
| connector | 8 | ≥1 | met (PlanningWalk is the bounded planning walk) |
| reviewer | 17 | ≥1 | met |
| critic | 9 | ≥1 | met |
| scribe | 4 | ≥1 | met (GateDecisions, FrontierRecord, ReportAudit, MistakeRecord) |
| sentinel | 4 | — | added |
| revenger | 4 | — | added |
| mutation-tester | 1 | — | added (ReceiptMutation) |
| simplifier | 1 | — | added (SimplifyScope) |
| planner | 0 | ≥1 | held by L1 (campaign addendum maps planner to L1) — not a subagent item |

- Godspeed lead: 64/64 prompts begin `/skill:godspeed`.
- Models: 0 `model` params in any task (compliant with "no model params").
- Agent IDs: all 64 registry members have `agentId` (e.g. `MadoR15.ReceiptCorrection`).

### 3b. Tool installs / updates (this seat)

- This seat: **none**. Read-only inspection only.
- Read-only `pacman -Q` observation of versions in the host (no install): `libinput 1.32.0-1`, `wayland-utils 1.3.0-1`, `wlr-protocols r112.a741f0a-1`, `wayland-protocols 1.49-1`, `hyprland 0.56.2-2`, `wayland 1.26.0-1`, `uv 0.13.0`.
- Round-15 wave artifacts record **no install** by any seat. Installs made by any seat during round 15 must be added to the report (none is recorded at check time; the swarm is still running).

### 3c. Stale lane

- `.ufo/state/mado.round` = `1`, mtime `2026-10-15 01:50:57`. `mado.mission` = `2685226`, mtime `2026-10-15 01:50:57`. `mado.out` mtime `2026-10-15 01:51:00`. These were not updated for rounds 2–15.
- `.ufo/state/mado.report-baseline` mtime `2026-10-20 04:20:54` = `15 e3b0c442…` (sha256 of empty file: no round-15 report at launch).
- `.ufo/watchdog.log`: `2026-10-20T04:20:56-03:00 launch mado round=15 pgid=2382589 driver=hyaku-inline attempt=1`. No `complete mado round=15` line at check time.
- `ps` for pgid 2382589 and pid 2685226 returned no process at check time.
- Consequence: `lane-watch.sh` reads `mado.round` (= 1) and `mado.mission` (not running) and will show mado as `round 1 idle`. This misrepresents the live round.
- Precedent: round-14 report recorded `Stale-lane: respawn-per-round` and the wave progressed via lane commits. Round 15 has no lane commit yet (`git log` head is `ea0446f`, pre-round).

## 4. Findings for the L1 scribe / driver (observations, not fixes)

- **F1 — stale state files.** `.ufo/state/mado.round` and `mado.mission` are not updated on launch; `lane-watch` will show the wrong round. Owner: driver/watchdog (outside this seat). Not edited.
- **F2 — axis binding mismatch.** `spec.json` `axes` and all 64 registry rows say `["coverage"]`. `.ufo/prompts/mado-round-15.md` §1 says `Your lane axes: coverage + operability`. Round-15 claim set is coverage only (C1). L1 should either state operability is not claimed this round or align the wave axes.
- **F3 — dispatch shape.** `dispatch.json` `taskCall.tasks[]` (64 entries) have no `solutionSpace` field. The `_task` schema requires one per task. Any re-issue must add it; this seat did not re-dispatch.
- **F4 — tooling directive placement.** The RULES.md directive and tool-install reference live in the wave `context`, not in any of the 64 item prompts (0/64 carry the literal "Tooling directive"). Context-level coverage is sufficient for the seats to read it, but the seats must still read RULES.md first (the context says so).
- **F5 — no per-item `Report:` trailer.** The `Report:` trailer contract in `context` is satisfied only by the inline path in each item's Acceptance (e.g. `.../reports/ReportAudit.md`). Items do not carry a separate `Report:` line. Reports are under `reportDir` `.ufo/waves/round-15/w1/reports` for all 64 items.
- **F6 — round-15 lesson missing.** `corpus/lessons/round-15.md` does not exist; the Mistakes section (frontier step 3) must be created by the L1 owner. Not created here.

## 5. Out-of-scope items

- R14-V1 correction content, the coverage counting recipe, and the source admission are owned by the other seats (ReceiptCorrection, MeasureBuild, InputDraft, FrontierRecord). This seat only lists their required evidence.
- No check of input-event, IME, or compositor behaviour; none claimed.
- `~/.omp/agent/agent.db*` and credential/auth files were not opened.
- No `omp` CLI was run; no subagent was spawned.

## 6. Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/ReportAudit.md` (this file only).
- Read: `/home/vgpnk/Projects/kimi-shokunin/templates/round-prompt.md`; `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-15.md`; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/mado.md`; `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` (tail); `/home/vgpnk/Projects/shokunin/.ufo/state/mado.*` (names, mtimes, values); `mado-shokunin/{SHONEN.md, corpus/lessons/round-14-verifier-spotcheck.md, corpus/lessons/round-14.md}`; `mado-shokunin/.ufo/waves/round-15/w1/{spec.json, dispatch.json, reports/swarm-registry.json}`; `/home/vgpnk/.omp/agent/RULES.md`.
- Commands (read-only): `pacman -Q` (6 packages), `uv --version`, `ps -o` for two PIDs/PGIDs, `stat`, `tail`, `git -C … log -1`, Python JSON parsing of wave artifacts.
- Tool installs/updates by this seat: **none**.
- Commits: none.

## 7. Verdict for this seat

- Six-section checklist: complete (§2).
- Role mix / floor: met (§3a); planner held by L1.
- Tool installs: none by this seat; none recorded by the wave; host versions listed (§3b).
- Stale lane: state files stale; live watchdog launch recorded; no completion (§3c, F1).
- Findings F2, F3 need L1 action before the report is committed; F1 needs the driver owner.
