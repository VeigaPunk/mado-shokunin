# CritContextDrift — w2 dispatch compliance attack

Seat: CritContextDrift (critic, leaf). Wave w2, round 48, policy v1.
Attack: verify every w2 seat's dispatched bytes carry the Godspeed directive, absolute
lane paths, no model param, host-table roles, the pacman guard, the RULES read, and
seat-private scratch; then probe the wave validator's refusal behavior on mutated specs
(plan only — nothing was dispatched).

Artifacts examined (all read-only):
- `.ufo/waves/round-48/w2-spec.json` (48 items), `w2-plan.json`, `w2-dispatch.json`,
  `w2.ready.dispatched`, `w2/swarm-registry.json`, `make-w2-spec.py`
- Host table: `~/.agents/skills/swarm/SKILL.md`; validator: `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`
- `/home/vgpnk/.omp/agent/RULES.md` (read first, per tooling authorization)

The assembled seat message is `taskCall.context` + `# Seat <Name>` + per-seat task text.
`w2-dispatch.json taskCall.context` is byte-identical to `w2-spec.json context`, and every
dispatched task is byte-identical to the spec item prompt plus a uniform trailer:

    Lane bounds: leaf member — no subagent dispatch[ except your single labrat].
    Report: write your scoped findings to .ufo/waves/round-48/w2/<Seat>.md

(trailer-exact for 48/48; 23 executor seats carry the labrat variant; report path matches
the seat name for all 48.)

## Required checks — all 48 seats pass all seven

Evidence: `seat-checks.txt`, `dispatch-full-check.txt`, `trailer-check.txt`.

1. Godspeed directive bytes: all 48 dispatched tasks start with the byte-exact
   `/skill:godspeed` + "You are a Godspeed-enabled subagent" header (compared against the
   canonical constant in `make-w2-spec.py:11`).
2. Absolute lane paths: context names `/home/vgpnk/Projects/shokunin/mado-shokunin`
   absolutely (goal, write-scope ×2, tooling bullets). 48/48 assembled messages contain it.
3. No model param: zero matches for `--model`, `model=`, `kimi`, `claude`, `gpt-`,
   `sonnet`, `opus` across spec, plan, dispatch and registry bytes. Consistent with the
   swarm contract: "there is no per-lane model key … Never pass a model"; roles route
   through the operator's global OMP config (`task.agentModelOverrides`/`modelRoles`).
4. Task roles through host table: 7 distinct roles used — executor, reviewer, critic,
   scout, connector, sentinel, mutation-tester — all members of the swarm taxonomy
   (`SKILL.md:122`). Three-way agreement `task.agent == registry.role == spec.role` holds
   for 48/48; live `w2/swarm-registry.json` matches the dispatch.
5. Pacman guard: "pacman transactions PAUSED host-wide—do not run pacman or any package
   transaction" present in every seat's shared context.
6. Read RULES: "read /home/vgpnk/.omp/agent/RULES.md first" present in every seat's
   shared context; I read the file before any writer command.
7. Seat-private scratch: context mandates `/fast/scratch/hyaku/mado-r48/<Seat>/` with an
   explicit mktemp recipe, "Never use /tmp", 2 GB total / 1 MB per-file bounds; every one
   of the 48 tasks carries its own `ulimit -f 2048` writer bound. No task hardcodes a
   non-seat scratch path.

Additional scans: all 48 tasks contain `# Target` / `# Required shell writer bound` /
`# Task`; no `xdg-terminal-exec` use without `--print-*`; no `xkbcli` verb outside
compile-keymap/test/kccgst read verbs (five regex hits were prose like "xkbcli env",
not invocations); no `sudo`; `/tmp` and "serials" matches are all prohibition/guard text.
Wave size 48 ∈ [32, 256] band; counts `{spawn:48, resume:0}`.

## Validator refusal probes (plan verb only — no dispatch, no run)

`ufo-swarm-wave.mjs plan` against the committed `w2-spec.json` succeeds (rc=0) and its
output is byte-identical to `w2-dispatch.json taskCall` for both context and all 48 task
texts — the dispatch is validator-fresh. Mutated specs refuse with typed codes
(`refusal-*.json`):

| mutant | refusal code |
|---|---|
| role `overlord` | `unknown_role` |
| duplicate seat name | `duplicate_name` |
| identical prompts | `duplicate_expansion` |
| 16 lanes | `too_few_lanes` (band floor 32) |
| 0 lanes | `empty_wave` |
| 260 lanes | `too_many_lanes` (cap 256) |

## Structural gaps found (2, both low severity; neither breaks w2 compliance)

- **G1 — committed `w2-plan.json` is stale vs the final spec/dispatch.** Its context lacks
  two bullets that spec and dispatch both carry: the `ulimit -f 2048` shell-writer-bound
  bullet and the "Data candidate location" (l1-draft) bullet. All 48 of its task texts end
  with the plain "no subagent dispatch." trailer, while the dispatch gives 23 executor
  seats "except your single labrat". Its policy records `minLanes=16 / waveMaxLanes=64`
  where the live config now yields `32 / 256`. The authoritative triplet
  (spec, dispatch, live registry) is mutually consistent and the dispatch equals a fresh
  plan, so what seats received is compliant; but any auditor replaying from `w2-plan.json`
  would see divergent context and trailers. Smallest correction: regenerate
  `w2-plan.json` from the committed spec (`ufo-swarm-wave.mjs plan --spec w2-spec.json`)
  or mark it superseded by `w2-dispatch.json`.
- **G2 — no Godspeed enforcement hook in this repo.** The swarm skill states the OMP
  pre-dispatch hook `.omp/hooks/pre/ufo-godspeed-inject.js` enforces the directive and is
  project-scoped; no copy exists at fleet root or in the mado lane (find across the repo
  returns nothing). W2 is nonetheless compliant because the renderer
  (`make-w2-spec.py:11`) bakes `/skill:godspeed` into every prompt byte-exactly — the
  guard here is convention-only, not hook-enforced. Smallest correction: install the hook
  (or record its absence as an accepted residual for this lane).

Defense-in-depth note (not a live defect): content-level guarantees (Godspeed bytes,
context bullets) are renderer-produced, and the validator's typed refusals cover
roles/names/expansion/band — a seat message is only as vetted as the renderer, so G2 is
the one worth landing before a wider wave.

## Process

- Scratch: `/fast/scratch/hyaku/mado-r48/CritContextDrift/` (seat-private, created
  explicitly); every writer shell ran under `ulimit -f 2048`; largest output file
  `plan-clean.json` = 72,252 bytes (< 1 MiB cap). Scratch removed after receipts were
  copied here. No /tmp use, no package transactions, no host mutation.
- No lane files edited; only this report and the `CritContextDrift/` evidence dir were
  written, per seat scope.
