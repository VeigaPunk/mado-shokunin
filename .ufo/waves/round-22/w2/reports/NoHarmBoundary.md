# MadoR22.NoHarmBoundary — fresh C1 static-snapshot/scope attack (author-lane advisory, not admission)

Revision 71228fd582d6d9338d7916cc64e69bd4c2e928b5. C1 `tools/mado-tripwire.py` sha256 `36fdc459…badce` was the same before and after the probe, so the target did not move. Oracle `expected.json` sha256 `b5cd4cf3…c4357` matches the pin. No tool, fixture, oracle or proposal was modified. The payload was parsed only, never executed.

## Verdict

**Counterexample found. It is inside the declared supported forms.** The C1 scanner invents an observed `host_mutation` command and drops the true observed `package_query`. This is invented argv promoted to observed evidence, which the supported-forms uncertainty rules and the guard-clarifications no-harm-on-additions rule both forbid. Under registration line 7, a new counterexample to the declared supported forms defeats C1 admission even if the 57-case numeric target passes.

## Counterexample (inert JSONL, one eval cell)

```python
import subprocess

argv = ["pacman", "-Q", "r22-nhb-module"]


def helper():
    subprocess.run(argv)


def make(argv):
    return helper


job = make(["pacman", "-S", "r22-nhb-factory-local"])
job()
```

**Independent truth (frozen before the probe; see `truth.json`).** `make` returns the module-level function object `helper` by an executed Name binding. `helper` is defined at module scope, so under Python's LEGB rule its free name `argv` is resolved at invocation against module globals. `make`'s parameter `argv` lives only in `make`'s frame, and `helper` cannot see it.

- **Expected (exact):** one row, `{package_query, "pacman -Q r22-nhb-module", observed}`, with zero unparsed counters.
- **Forbidden at all tiers:** `pacman -S r22-nhb-factory-local`.

**Observed output** (`scan-result.json`): the scanner child exited 1, `eval_unparsed` and `unparsed_spawns` were both 0, and the complete row list was a single row:

```
[{"class":"host_mutation","command":"pacman -S r22-nhb-factory-local","evidence":"observed","rule":"pacman:-S"}]
```

This produces two failures under the oracle's exact multiset rule:

- **False positive:** an invented host mutation reported as observed.
- **False negative:** the real package query is missing.

Because both error counters are zero, the result looks clean and certain.

## Why it fits the declared supported forms

`supported-forms.md` lines 7–8 cover each element of this case:

- a straight-line visible factory with a positional literal argument;
- a stored factory result in one cell;
- returned helper identity from an executed Name binding;
- "Enclosing factory locals stay distinct from module globals; globals are read at invocation."

The case uses no star-args, no conditional or non-Name return, no mutation, no namespace reset and no scheduling. None of the uncertainty or out-of-scope exclusions apply. It is not a duplicate of an existing case:

- `CaptureGlobalLate` and `CapturePartialGlobalLateActual` read a module global, but have no factory parameter that shares the global's name.
- `CXPartialLocalFunction` and `CaptureLocalShadow` shadow a *helper name*, not a free data name.

None of the 57 inputs returns a module-level helper from a factory that has a same-named local.

## Root cause (static reading of the fixed source)

`factory_result` in `tools/mado-tripwire.py` is at lines 1642–1684.

- It collects `names` from the factory's bound parameters, its closure names, and the bindings in the prefix before `return` (lines 1664–1673).
- It then attaches an overlay of `closure_env` and `closure_bindings` covering **all** of those names to **any** `kind == "helper"` result (lines 1675–1683). It never checks whether the returned helper's definition is lexically nested inside the factory.
- At invocation, `spawn_scan` (lines 2511–2516) layers `closure_env` over the caller environment. The module-level `helper` body therefore resolves `argv` to `make`'s parameter.

So the factory's frame leaks into every module-level, or otherwise non-enclosed, callable it returns. This is the "overfreeze" side of the snapshot concern. `statement_snapshot` (lines 2163–2200) is not at fault here: it correctly gathers `argv` from `helper`'s body, and the late-bound global value is present in the snapshot until the overlay overrides it.

The same mechanism applies to callable identity, not just literals:

- `closure_bindings` overlays factory-local *callable* names (for example a local `def f` or a callable parameter) onto a returned global helper that calls a global `f`.
- `bound_callables` stores `{"kind": "parameter"}` for non-callable parameters, and that placeholder can mask a global callable binding of the same name. A global helper calling a global `run` would then resolve `run` as a parameter instead of the module binding.

These two consequences are `[INFERENCE]` from reading the code. Only the literal-argv form was probed.

## Impacted axes

- **C1 operability, precision:** invented observed argv.
- **C1 operability, recall:** the true observed command is lost.
- **Calibration:** the result is wrongly certain, with zero unparsed counters.

The existing F1/F2 lexical-scope repair claim is incomplete for this returned-identity form. The no-harm guard on additions applies, because this would be a relabelled or added finding with invented argv.

## Smallest safe correction (proposal only; L1 owns implementation)

In `factory_result`, apply the overlay only to names that are free in the returned helper's own lexical chain. Concretely, attach `closure_env`/`closure_bindings` only when the returned helper node is lexically enclosed by the factory `owner`, meaning it is a descendant of `owner.body` (a nested def/lambda, or an alias that resolves to one). A helper defined outside the factory keeps the closure it already had (`result.get("closure_env")`/`closure_bindings`), and gets no overlay from the factory frame.

A tighter version restricts the overlay to the free variables of the nested helper that are bound in `owner`, rather than to every name in the factory frame.

Add this fixture to the frozen population as an exact case. Do not remove it after the fact as unsupported.

## Receipts

All receipts are under `.ufo/waves/round-22/w2/receipts/NoHarmBoundary/`.

| File | sha256 |
|---|---|
| `NHBFactoryReturnsGlobalHelperParamShadow.jsonl` (fixture) | `bba513187e957d79032e76c9c7e549414c8e7452968ed67f3115c86715e80ede` |
| `truth.json` (authored before the probe) | `a2fcfc6e7c992190e06fde6bafd952a621b9f1016bcf2b1a1cf0bffc9bd64c74` |
| `scan-result.json` (argv/exit/stdout/stderr/payload) | `863640f7fddc483b260083edbb33e23d92ebbe6207b184ee0def542a235a53e9` |

- `digests-before.txt` and `digests-after.txt` record the tool, fixture and truth hashes; both list tool sha `36fdc459…badce`. `digests-before.txt` also records `measure.py` `41b021bb…28c7` and `expected.json` `b5cd4cf3…c4357`.
- **Probe:** a single child created by the existing `oracle/measure.py::scan` helper (RLIMIT_AS 384 MiB, 15 s timeout, `python3 -I` wrapper calling `main(["--scan", fixture])`). The exact argv is in `scan-result.json`. There were no other scanner runs, no whole-corpus run and no reruns.
- **Installs:** none.
