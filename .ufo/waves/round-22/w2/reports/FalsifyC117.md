# FalsifyC117 — C1 falsification: case `CaptureCrossCell` (round22 delivered rev `71228fd582d6d9338d7916cc64e69bd4c2e928b5`)

Seat: `MadoR22.FalsifyC117` · lane: leaf reviewer, author-lane advisory attack only, no subagent dispatch, no installs or updates performed (pacman transactions paused; none needed).

## Measurement executed (the single authorized run)

- Outer invocation: `timeout 20 bash -c 'ulimit -v 393216; exec python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureCrossCell'`
- The runner itself enforces the seat caps on the scanner child: `RLIMIT_AS` 384 MiB via `preexec_fn` and `timeout=15` (measure.py 643–661), one synchronous child. Exactly one scanner child was spawned; no other probes, no reruns.
- Runner exit **0**, `status: complete`, `totals: {pass: 1, total: 1}`, `integrity_errors: []`; integrity before == after: tool `36fdc459…badce` (re-verified by my own before/after `sha256sum` — no drift), expected `b5cd4cf3…4357`, runner `41b021bb…28c7`, population `04616857…86ad`, 57 inputs / 52 proposals / 106 sealed sources verified.
- Scanner child exit **1** is the tripwire's findings-present verdict convention (payload `"exit": 1`, `unpermitted: 1`), identical to the sealed w1 green receipt `oracle-after-all57.json` for this same case; it is not a runner failure. stdout 5508 bytes (sha `58867a92…a2a2`) and empty stderr (sha `e3b0c442…7852`) retained raw in the receipt dir.

## Sealed case (oracle/expected.json, id `CaptureCrossCell`, group `proposal`, kind `exact`)

- Fixture `inputs/CaptureCrossCell.jsonl` sha `d4760b95…9115` (verified independently); two cells, `cell_reset [false, false]`.
- want exactly `[{host_mutation, pacman -S r22-crosscell-exact, observed}]`; `forbid_observed_commands`: `pacman -Q r22-crosscell-decoy`, `pacman -S r22-crosscell-decoy`, `pacman -Q r22-crosscell-exact`; `forbid_commands_any_tier: []`; `require_signal: true`.
- `accept_exact_want: null` — grounded in runner code: a non-null value is refused for non-uncertain kind (measure.py 272–279). Null is **not applicable**, not hidden uncertainty. The true-uncertainty distinction holds: this case's truth is fully statically determined; no uncertainty boundary was declared and none exists.

## Independent semantic truth (green not treated as proof)

CPython closure semantics, static reasoning only: `run` captures the factory parameter cell `argv`, bound to the list `["pacman","-S","r22-crosscell-exact"]` at the `factory(spec)` call in cell 1. Cell 2's `spec = [...]` rebinds the module global to a new list object; rebinding cannot mutate the captured cell. Both cells are `reset:false`, so the persistent per-file namespace keeps `worker` and `subprocess` resolvable. `worker()` executes `subprocess.run(["pacman","-S","r22-crosscell-exact"])` exactly once. Truth: exactly one observed `host_mutation` row with that command; the decoy list is never an argument to any call; zero unparsed, zero errors. This independently matches the sealed want.

## Actual outcome

`got_rows == want` — one identical row. Payload: `observed_findings 1`, `lead_findings 0`, `unparsed 0`, `eval_calls 2`, `eval_unparsed 0`, `unparsed_spawns 0`, class counts host_mutation 1 / all others 0. Finding identity: `line 2`, `tool_call_id CaptureCrossCell-1` (the invocation cell); creation cell `CaptureCrossCell-0` correctly emits nothing.

## Falsifier checklist — all attempted, none fired

| Attack | Result |
|---|---|
| False observed / lead argv | None: exactly one `observed` row carrying the creation-time argv. The F1-style invoke-time rebinding row (`pacman -Q r22-crosscell-decoy` as `package_query`) is absent; both token recombinations absent; zero lead rows. |
| Lost true command | Present, evidence tier `observed` (correctly not under-claimed as `lead`). |
| Wrong identity | Attributed to the invocation cell `CaptureCrossCell-1` / line 2; creation cell clean. No misattribution. |
| Lifetime | Cross-cell persistence of the creation-time binding confirmed within this case's `reset:false` scope. |
| Conditional target | Fixture contains no conditional return/branch; nothing conditional was invented — vacuously clean. |
| Parsed-clean ambiguity | Zero parse errors, zero unparsed: the clean row is grounded in a fully parsed population, no ambiguity between clean and error-bearing scans. |
| Full multiset + zero errors | Runner semantics verified in code: sorted `(class, command, evidence)` multiset equality **and** `unparsed == 0` (measure.py `evaluate` 736–756). Satisfied; `reasons: []`. |
| Forbidden argv at all tiers | `forbid_commands_any_tier` is empty for this case; all three `forbid_observed_commands` absent from `got_rows`. |

## Verdict

**agree** — the delivered tool's observed behavior for `CaptureCrossCell` equals the sealed independent truth exactly: no false observation, no lost command, no misattribution, correct evidence tier, clean parse. This is a bounded single-case agreement and a recommendation from an author-lane adviser; it grants no admission, no host recovery, and does not touch the r19/r20/r21 rejection streak.

## Scope and residual risk

- One case of the 57-case population measured; the runner validated full-population integrity but only this case's behavior. No claim about the other 56.
- The `reset:true` sibling `CX11Reset` was not measured here; the lifetime verdict is scoped to `reset:false` cross-cell persistence.
- Per supported-forms, closure is limited to the named tested F1 cross-cell form, not the whole defect family.
- Original r21 red receipts remain source authority; no old tool was rerun; all production/fixture/expected bytes read-only (runner integrity before/after plus my own before/after `sha256sum` show no drift).

## Artifacts

- Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC117/result.json` (+ raw `stdout.raw`, `stderr.raw`, `exit.txt`)
- Sealed inputs read: oracle `expected.json` (case entry), `w1/proposals/CaptureCrossCell.json` sha `8092ee64…4db7`, fixture `inputs/CaptureCrossCell.jsonl`, grounding `.ufo/waves/round-21/residual/FinalBindingReview.md` (F1, reach note 2643–2644/2685–2686)

Report: .ufo/waves/round-22/w2/reports/FalsifyC117.md
