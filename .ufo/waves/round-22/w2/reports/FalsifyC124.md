# FalsifyC124 — C1 case `CaptureLocalShadow` (round-22 w2)

Seat: `MadoR22.FalsifyC124` · Lane: leaf falsifier · One runner invocation (one scanner child, 384 MiB / 15 s caps) plus read-only source and receipt reads · **No admission granted**

Report: .ufo/waves/round-22/w2/reports/FalsifyC124.md
Absolute: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC124.md
Receipt: .ufo/waves/round-22/w2/receipts/FalsifyC124/result.json

## Verdict

| Item | Verdict |
|---|---|
| Sealed truth expectation for `CaptureLocalShadow` | **AGREE** |
| Current tool on this single case | PASS: exact multiset equal, zero error counters |
| Population, C1 clearance, admission | Not assessed by this seat; nothing granted |

## Scope against the current target

- Target: C1 all eligible frozen expectations match. This case is 1 of the 57 frozen cases.
- The runner validated the full population before running and then executed only `CaptureLocalShadow`. Totals: 1/1.
- Not covered here: the other 56 cases, the 1356-fixture removal comparison, the resource recipes, and F1–F5 beyond this shape.

## Actual measurement

- Runner argv: `python3 -I .../oracle/measure.py --tool .../tools/mado-tripwire.py --case CaptureLocalShadow`
- Runner exit 0. `status: complete`. `integrity_before == integrity_after`. No integrity errors.
- Scanner child argv: `/usr/bin/python3 -I -c <WRAPPER> <tool> <fixture>`. Exit 1, which means one unpermitted finding. Stderr empty.
- Rows: `host_mutation | pacman -S r22-shadow-local | observed` (one row; line 1; `tool_call_id` `CaptureLocalShadow-0`; rule `pacman:-S`).
- Counters: `eval_calls` 1, `eval_unparsed` 0, `unparsed_spawns` 0, `lead_findings` 0, `observed_findings` 1, `unpermitted` 1.
- Hashes, recomputed by me and matching the runner's reports:
  - tool `36fdc459…` before and after the run (no drift)
  - runner `41b021bb…`
  - expected `b5cd4cf3…`
  - pin `7cc4aae9…`
  - truth seal `47f403f6…`
  - fixture `d1b0520a…` (equals sealed)
  - proposal `74a90015…` (equals sealed)
  - population `046168571f…`, producer `0270c10b…` (runner-reported)

## Independent semantic derivation

1. `make()` defines `inner`, then executes `shadow = inner`. With no `global` declaration, `shadow` is local to `make` for its whole body, so `return shadow` yields `inner`.
2. `make()()` calls `inner`. Its body runs `subprocess.run(["pacman","-S","r22-shadow-local"])`. That is one executed spawn with a literal argv.
3. The module-level `def shadow` is only a binding. No eager call names it, so `pacman -Q r22-shadow-global` is never executed on any schedule.
4. Class: `pacman -S` with no query or refresh flags is `host_mutation`. `classify_pacman` lines 775–780 send `-S` without `yuwc` or `silgp` flags to the `host_mutation` fall-through (line 780). The module docstring reserves `tool_install` for non-pacman channels.
5. Evidence `observed`: the path is literal, unconditional, single-cell and executed.
6. Complete expected multiset: `{(host_mutation, "pacman -S r22-shadow-local", observed)}` with zero unparsed. This equals the sealed `want`.

The source's stated version (Python 3.14.8) was not re-verified. The scoping rule is stable across CPython 3.x, so the version does not change the truth.

## Why the pass is principled (read-only source)

- `factory_result` replays the prefix (`shadow = inner`) into `local_bindings` before resolving the return: lines 1663–1675.
- `update_bindings` writes the Assign into bindings: lines 1928–1937. `assignment_binding`'s Name branch returns the local helper: lines 1828–1831. `callable_info`'s Name branch: lines 1748–1753.
- The module `shadow` is reached only through a module-scope Name lookup, and no eager call names it. [INFERENCE from control flow; consistent with zero `-Q` rows.]
- Zero leads. The docstring (line 55) says each swept body is swept once per cell. I did not trace the dedupe code path.

## Falsification attempts

| Target | Attempt | Result |
|---|---|---|
| False observed (borrowed module global) | Emit `pacman -Q r22-shadow-global` observed by resolving the return to module `shadow` | Not produced. Forbid list and exact multiset both clear. |
| False lead argv | Any extra lead row fails the exact comparison | `lead_findings` = 0. Not produced. |
| Lost true command | Current tool drops `-S` | Not lost now. The r21 before tool **did** lose it (see prior receipts). |
| Wrong identity | An identity route yielding the same argv, e.g. a def-name lookup that finds the sole `inner` | **Not falsifiable by this case.** Rows carry class/command/evidence only, and the runner does not compare provenance. |
| Lifetime | Closure frame outliving its factory; cross-cell persistence | **Not exercised.** No free variables, one cell, `reset` false, no captured mutation. |
| Conditional target | Branch-dependent call target | **Not present.** The call is unconditional. |
| Parsed-clean ambiguity | Silent clean with zero counters | Current 0/0 counters are correct (no unsupported construct). **But the r21 red has identical 0/0 counters.** Counters cannot separate the two; only the exact multiset does. |
| Uncertainty hedging | Tool reports `uncertain` instead of exact | Would FAIL. `accept_exact_want` is null and no real runtime uncertainty exists in this cell. |

## Prior recorded receipts (read-only; not re-executed)

- `evidence/first/oracle-before-new50.json` (r21 delivered classifier, bytes `46c82902…`): rows `[]`, exit 0, `pass: false`, reason "complete class/command/evidence multiset or zero-error condition differs". Counters `eval_calls` 1, `eval_unparsed` 0, `unparsed_spawns` 0; no scanner error. This is a silent parsed-clean false negative, the actual r21 red for this case.
- `evidence/first/oracle-after-all57.json` (`36fdc459…`): rows identical to my fresh run, exit 1, `pass: true`. It agrees with this measurement but is not independent of the sealed truth.

## Notes (non-blocking)

1. `forbid_commands_any_tier` is `[]` on this exact case. The `pacman -Q r22-shadow-global` protection rests on exact multiset equality. If this case were re-kinded to `uncertain`, a lead-tier borrow would pass unforbidden.
2. `require_signal: true` is inert for exact cases; `evaluate` reads it only in the uncertain branch. Harmless, but misleading.
3. The registration text says shadowed bindings "may yield lead/unparsed uncertainty". The sealed truth is stricter and forbids leads. That is defensible: the call provably binds to `inner`, so a `-Q` lead would be a spurious row. Exact is the correct kind here.
4. The finding's `timestamp` is the string `"None"`, not null, for a fixture line that has no timestamp. That is outside the sealed contract and not compared by the runner. Flagged for L1.

## Proposed fault recipes (proposed, NOT run, NOT killed; for L1 in a private sandbox)

- **P1 (F3 regression):** in `factory_result`, resolve `returned.value` against module-level `bindings` instead of `local_bindings`. Predicted FAIL: observed `pacman -Q r22-shadow-global` plus a missing want row.
- **P2 (silent clean):** in `classify_eval`, when a factory result is a helper, skip following and return no hits with zero counters. Predicted FAIL: rows `[]` against the want.
- **P3 (identity by name):** resolve a returned name by searching the module for any `FunctionDef` with that name. Predicted PASS on this case, because `inner` is the sole match. This is an expected survivor, which a sibling case with two same-named inner defs across factories would need to kill.

## Installs and updates

None. No packages, services, live probes, or old-tool executions. One scanner child was spawned in total.

## Checks for Main

- The population-level C1 run and the 1356-fixture comparison remain L1's. This seat ran one case only.
- Do not read this as clearance. It shows only that the one sealed expectation is correct and that the current tool meets it for the stated reason.

Report: .ufo/waves/round-22/w2/reports/FalsifyC124.md
