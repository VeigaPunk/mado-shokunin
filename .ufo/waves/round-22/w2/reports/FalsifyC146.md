# FalsifyC146 — C1 sealed case `ThreadRunInline`

Seat: `MadoR22.FalsifyC146` · Wave: mado-r22-w2 · Delivered revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5` · Role: author-lane advisory falsifier, **not** non-author admission.

## Scope

One sealed C1 case, one bounded measurement. Read-only against all production, fixture, proposal, expected and tool bytes. Wrote only:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC146/` (argv, raw stdout/stderr, exit, before/after hashes, `result.json`)
- this report.

No edits to sources, fixtures, proposals, gates, registries, docs or tool bytes. No installs or updates were needed or performed. No old r21 tool was executed. No extra scanner run was made.

## Identity pins verified before and after (no drift)

| Item | sha256 |
|---|---|
| `tools/mado-tripwire.py` (selected C1 tool) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `.ufo/waves/round-22/oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `.ufo/waves/round-22/audit/fixtures/expected.json` (C2 identity) | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| `oracle/inputs/ThreadRunInline.jsonl` (fixture) | `0fcf386b9773fc1ec782638acc542616c41de6315f192f3869ba19008f7f4a85` |
| `oracle/assemble.py` (producer pin) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| population digest | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

`hashes-before.json` and `hashes-after.json` are byte-identical; `integrity_errors` is `[]` and `integrity_before == integrity_after` including `tool_sha256`. The tool was not a moving target.

## Sealed expectation under attack

From `expected.json`: `group=proposal`, `expected_kind=exact`, one cell (`reset=false`), `want` = exactly one row `{class: host_mutation, command: "pacman -S r22-threadruninline", evidence: observed}`; `forbid_observed_commands=[]`, `forbid_commands_any_tier=[]`, `accept_exact_want=null`, `require_signal=true`, no addenda or correction. Proposal sha `1832b38152a010fd30313f5862db94ce343fd39af4e27641a7bc4cc4553d665b`; its `want` is preserved verbatim in the sealed case. `measure.py` re-verified the proposal file digest/fields and fixture digest as part of population validation before running.

Fixture cell:

```python
import subprocess
import threading

argv = ["pacman", "-S", "r22-threadruninline"]

def worker(argv):
    subprocess.run(argv)

threading.Thread(target=worker, args=(argv,)).run()
```

## Independent truth (static derivation, payload never executed)

1. `threading.Thread(target=worker, args=(argv,))` evaluates a standard-library `Thread`; `__init__` stores `_target=worker`, `_args=(argv,)`, `_kwargs={}` (pinned snapshot `.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py:880-928`, read and confirmed).
2. `.run()` on that instance is `Thread.run`, which executes `self._target(*self._args, **self._kwargs)` synchronously in the caller when `_target is not None` (same snapshot `:1013-1028`, read and confirmed). No `start()`, no new thread, no scheduler, no cancellation.
3. Therefore `worker(["pacman","-S","r22-threadruninline"])` runs once; the parameter `argv` binds to that module-level literal list. Nothing reassigns or mutates `argv` (no subscript/attribute assignment, no later rebinding; final statement of the cell).
4. `worker`'s body calls `subprocess.run(argv)` with the three-element list. The canonical command is `shlex.join(["pacman","-S","r22-threadruninline"]) = "pacman -S r22-threadruninline"`; `-S` without a query-only flag is an install/sync attempt, i.e. `host_mutation`.
5. No other spawn path exists. Exactly one row, one evidence tier: `observed` (all links are literal/visible, which `supported-forms.md` explicitly claims for "newly constructed stdlib Thread … stored/inline/aliased standard `.start`/`.run`").

Independent result: `{(host_mutation, "pacman -S r22-threadruninline", observed)}`, zero unparsed. This matches the sealed `want` exactly. Confidence: high (semantic derivation independent of detector bytes).

## Authorized measurement (one child, one case)

Executed exactly once:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py \
  --case ThreadRunInline
```

Raw capture in `receipts/FalsifyC146/`: `argv.json`, `exit.txt`, `stdout.raw`, `stderr.raw`, before/after hash files, `result.json`.

- Runner exit `0`; status `complete`; `case_filter=ThreadRunInline`; totals `1/1`; `integrity_errors=[]`.
- Population validation covered 106 sealed source files, 52 verified proposal files (50 eligible proposals + 1 applied addendum + 1 preserved rejected typo) and 57 input fixtures (50 proposal cases + 7 supplemental originals); exactly **one** scanner child was launched (scan argv retained in `result.json`), not 57.
- Scanner child: exit `1` (one unpermitted finding), stderr empty, no scanner error.
- Got rows: exactly `[{"class":"host_mutation","command":"pacman -S r22-threadruninline","evidence":"observed"}]`; `unparsed=0`; payload `counts` = `{host_mutation:1, package_query:0, live_probe:0, tool_install:0, vcs_write:0}`; one file row with `eval_calls=1`, `eval_unparsed=0`, `unparsed_spawns=0`, reported digest `0fcf386b…` matching the sealed fixture and path resolving to that fixture.
- Case `pass=true`, `reasons=[]`. Comparison is complete sorted `(class, command, evidence)` multiset equality plus zero unparsed counters — the sealed row and the measured row are identical, so this is a genuine exact-tier pass, not subset containment.

## Falsification checks for this case

| Attack | Result | Basis |
|---|---|---|
| False observed/lead argv (invented command) | **Not found** | Measured command equals the only literal argv in the cell; `argv` literal is unmodified and passed positionally; no same-named competing literal exists. |
| Lost true command (silent miss, F4 shape) | **Not found** | The only reachable spawn is `subprocess.run(argv)` inside `worker`; it is emitted. `eager_calls` skips deferred function bodies, and the reference sweep explicitly skips targets handed to `threading.Thread`/`Timer`, so the row cannot be an accidental eager-body hit — it requires the chained `.run()` to be followed (candidate-path reading; [INFERENCE] on mechanism). |
| Wrong callable/command identity | **Not found** | `worker` resolves to the visible def; parameter binding is positional from the thread `args` tuple; class `host_mutation` / rule `pacman:-S` matches `pacman -S` install semantics, not `package_query`/`tool_install`. |
| Lifetime/rebinding defect | **Not found** | Single straight-line statement, no rebinding or mutation of `argv`/`worker`; scheduled state is consumed once (`run()` once → target once); no stale pre-mutation value exists to print. |
| Conditional/non-Name target | **Not applicable** | Target is a literal `Name` bound to a visible `def`; no branch, loop or descriptor. |
| Parsed-clean ambiguity | **Absent** | Zero `eval_unparsed`/`unparsed_spawns`, non-empty finding, scanner exit `1` (not a silent 0), input digest/path checks passed, stderr empty, no scanner error, before/after integrity equal. |
| `accept_exact_want` / uncertainty laundering | **N/A by contract** | `expected_kind=exact`; `accept_exact_want` is `null`; `require_signal=true` is inert under exact evaluation and creates no license to emit a lead. Independent truth fully determines the argv, so requiring an uncertainty tier here would invent an observation boundary contradicted by the declared supported form. |

No truth or expectation contradiction was found for this case, so nothing was normalized away and no correction is proposed.

## Discrimination limits (what this green does NOT show)

- **F1 non-discriminating in this shape.** The fixture's parameter name `argv` shadows the module global of the same name, and the call passes that same global positionally. A correct lexical-parameter binding and the known F1 defect "borrow the same-named module literal" produce the identical list here. Green is therefore compatible with the F1 mechanism still being latent; this case cannot separate them. [INFERENCE from source shape]
- **`.run` vs `.start`.** The row schema carries no timing field, and the candidate path routes both `.start` and `.run` through the same scheduled-invoke handler to an `observed` row with the same command. Green proves the chained, unbound thread expression's target is followed at all; it does not prove synchronous-versus-scheduled timing semantics.
- **Family coverage.** One exact case out of 57 validated inputs (50 proposal cases + 7 supplemental originals). No claim is made for starred/dynamic arguments, returned aliasing/rebinding (F3), partial wrappers, Timer cancellation, recursive/conditional returns, subclasses overriding `run`, the F5 reserved-key hygiene guard, the historical 175-case suite, the r21 1356-fixture removal/error comparison, or the closure-heavy resource population.
- **Class-label convention.** `host_mutation` was confirmed against this fixture's semantics and the tool's `pacman -S` rule; a corpus-wide label-convention cross-check against sibling cases was outside this seat's read scope.
- Prior r19/r20/r21 red receipts and the three-rejection streak remain authoritative and are untouched by this result.

## Verdict

**Agree** with the sealed `ThreadRunInline` expectation at the exact tier: one observed `host_mutation` `pacman -S r22-threadruninline`, zero uncertainty. Measured rows reproduce it exactly on delivered revision `71228fd…` with the pinned tool/runner/expected/fixture digests and no drift.

This is one-case static-source-shape agreement only. It grants no admission, closes no C1/C2 claim, retires no prior red, and cannot by itself qualify the delivered revision. Rows are retained in `receipts/FalsifyC146/result.json` for L1 review; any mutant-kill or aggregate conclusion is L1's private-sandbox work.

## Remaining unknowns

- Behavior of the other 56 validated cases and the separate no-harm/historical/resource guards (not run here).
- Whether this case kills any concrete mutant recipe (mutation execution is reserved to L1's private sandbox; no proposed fault is called killed here).
- Whether the green would survive a variant where the thread parameter and module literal diverge in name/value (the F1 discriminator this case lacks).
- Runtime success of the pacman command is irrelevant to and not asserted by the static row; the payload was never executed.
