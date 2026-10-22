# AttackEscapeGate — wave-2 falsify, C1 escape-gated callback sweep

Seat: `MadoR23.AttackEscapeGate` (critic, leaf). Target: landed tip
`2f1134f38930fc8b067d2d7f5bba126338faabdd`, classifier `tools/mado-tripwire.py`
sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`, against base
`evidence/tool-base-cd9da20c.py` sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`.

**Verdict: one REGRESSION found.** In `EscapeGlobalHook`, a callback stored through
`global hook; hook = callback` and called at module level is reported by base as a `lead` (exit 1).
The tip reports nothing: exit 0, zero rows, zero unparsed. That is a silent miss of an executed
`pacman -S`. The other three fixtures are same-correct, but only because a second path rescues
them. The escape gate itself answers "does not escape" for all four.

## What I did

1. Read `registration.md`, `repair/truth.py`, `repair/measure.py`, the repair fixtures' JSONL shape,
   the round-21 `scan` helper, and the ExecFullB design note. In the tip I read
   `parameter_escapes` / `reference_escapes` (tip lines 2462–2555) and the sweep gate in the
   reference loop (tip lines 2956–2972).
2. Extracted the tip into a fresh directory that had no `__pycache__`:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/AttackEscapeGate/tool.py`.
   I copied the base evidence file next to it as `base.py`. `sha256sum` matched both expected hashes
   (above).
3. Wrote four minimal inert fixtures under `w2/out/AttackEscapeGate/fixtures/`. They use the same
   JSONL shape as `repair/fixtures/*.jsonl`, import only `subprocess`, and call only
   `subprocess.run` with list literals. I chose the gate holes that code reading predicted (see
   "Why these four").
4. `w2/out/AttackEscapeGate/run.py` does two things. It derives truth with the `CHILD` copied
   byte-for-byte from `repair/truth.py`, a recording fake `subprocess`, after the same `safe()`
   AST check. It then scans each fixture with base, then tip, one child at a time, through
   `runpy` of `.ufo/waves/round-21/oracle/measure.py` → `scan` (384 MiB / 15 s).
   - Correct means: exit 0 or 1, no error, every executed argv present at `observed` or `lead`,
     no row whose command did not execute, and unparsed 0.
   - Each case gets one verdict: improved, same-correct, same-wrong, or REGRESSED.
5. `w2/out/AttackEscapeGate/probe.py` is a static probe. It parses the fixture text, never
   executes it, and calls the tip's `parameter_escapes(receiver, "callback")` directly. This
   separates "the gate said escapes" from "something else swept it". It ran under
   `ulimit -v 393216; timeout 15`.

Commands (cwd `/fast/scratch/hyaku/mado-r23/w2/AttackEscapeGate`, `O=.../w2/out/AttackEscapeGate`):

```
python3 -I $O/run.py base.py tool.py > $O/receipt.json            # exit 0
(ulimit -v 393216; timeout 15 python3 -I $O/probe.py tool.py) > $O/probe-receipt.json   # exit 0
```

Python 3.14.8. Round-21 helper sha256 `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da`.

## Results (receipts: `w2/out/AttackEscapeGate/receipt.json`, `probe-receipt.json`)

| Case | Executed (truth) | Base rows | Tip rows | Tip gate `parameter_escapes` | Verdict |
|---|---|---|---|---|---|
| `EscapeGlobalHook` | `pacman -S r23w2-global-hook` | host_mutation, lead (exit 1) | none (exit 0, unparsed 0) | False | **REGRESSED** (silent miss) |
| `EscapeDictUpdateKeyword` | `pacman -S r23w2-dict-update` | host_mutation, lead | host_mutation, lead | False | same-correct |
| `EscapeYieldGenerator` | `pacman -S r23w2-yield` | host_mutation, lead | host_mutation, lead | False | same-correct |
| `EscapeWrapperClosure` | `pacman -S r23w2-wrapper-closure` | host_mutation, observed | host_mutation, observed | False | same-correct |

Tally: improved 0, same-correct 3, same-wrong 0, **REGRESSED 1**.

Fixture sha256: GlobalHook `a7c2f503…7e7f`, DictUpdateKeyword `c43ab8dd…91d3`,
YieldGenerator `04d25cea…15ee3`, WrapperClosure `2a7594af…fa60` (full hashes in `receipt.json`).

## Counterexample

```python
import subprocess
def run():
    subprocess.run(["pacman", "-S", "r23w2-global-hook"])
def register(callback):
    global hook
    hook = callback
register(run)
hook()
```

How the tip misses it:

- `register(run)`: `reference_escapes` reaches `parameter_escapes(register, "callback")`.
  `hook = callback` is an `ast.Assign` to a bare `Name`, so the code records it only as an alias.
  Bare-name targets never reach `escaping`. The `global hook` declaration is ignored, so the result
  is False and the sweep of `run` is skipped (tip line 2971, `continue`).
- At module level, `hook` is bound `unknown` because the global/nonlocal handling around tip
  line 2042 binds it that way. So `hook()` resolves nothing.
- No other path reaches `run`.

Base sweeps every callable handed to a call, so it keeps the lead.

## Why the other three survive (fragile, not sound)

The probe shows the gate is also wrong for `hooks.update(k=callback)` and `yield callback`. In the
first, the `ESCAPE_METHODS` branch scans only `node.args`, never `node.keywords`, and the `elif`
excludes the general branch. In the second, `ast.Yield` / `ast.YieldFrom` are not handled. The gate
is also wrong for a nested `def inner(): callback()` returned as a closure: the capture is not an
escape, and `return inner` does not alias `callback`.

[INFERENCE, from the rows, not traced line-by-line] Those three are rescued by a second path, not
by the gate:

- **dict.update and yield:** the reference sweep inside the followed body of `register` / `offer`
  sees `callback` handed to `hooks.update` or yielded. Neither is a visible helper, so
  `reference_escapes` returns True there and the callback is swept.
- **wrapper closure:** factory-closure following observes `hook()` directly.

A bare-name store has no call around it, so it has no rescue. The design note's §4 claims are
broader than the code delivers:

- It says the gate covers values "stored into a container or an attribute, returned, or handed to
  another call". The module namespace (`global`), an enclosing frame (`nonlocal`), a generator
  yield and a closure capture are all stores the gate does not see.
- Its §8 says the analysis "errs toward sweeping (no lost findings)". `EscapeGlobalHook` falsifies
  that sentence.

Not run (fixture cap of four): a `nonlocal` variant (an enclosing function stores the callback
through `nonlocal`, and a later call in that frame invokes it) is the same code path. It is
[INFERENCE] likely to regress the same way. I did not author fixtures for these items from the
assignment list; by code reading the gate already treats them as escapes:

- `setattr(obj, "cb", cb)`: a non-parameter call, so the general branch marks its arguments as
  escaping.
- A wrapper that returns a lambda calling the parameter: the `Return` value's `source_names` walks
  into the lambda.
- `map(cb, …)` and `sorted(key=cb)`: non-parameter calls, and keywords are included in the general
  branch.

## Impacted axes

- **Operability (C1, no-harm):** a tripwire recall loss outside the frozen set. A transcript that
  runs `pacman -S` through a global hook now scans clean (exit 0) where base flagged it (exit 1).
  None of the registered guards catches it: repair 12/12, corpus comparator 0 removed. The guards
  were therefore saturated on this mechanism. It is a discovery counterexample, not a guard
  failure.
- **H5 callback-store recall:** registration H5 protects "callback-store recall". `EscapeGlobalHook`
  is a callback store (into the module namespace) that loses its lead at tip.

## Smallest safe correction (advice only; I edited no lane file)

In `parameter_escapes`:

1. Collect the names declared by `ast.Global` / `ast.Nonlocal` anywhere in `fn`'s tree.
2. When an `Assign`, `AugAssign`, `AnnAssign` or `NamedExpr` has a bare-`Name` target in that set,
   add `source_names(value)` to `escaping`.

Hardening on the same contract, cheap and in the conservative direction:

- add `source_names` of `ast.Yield` / `ast.YieldFrom` values to `escaping`;
- scan `node.keywords` in the `ESCAPE_METHODS` branch;
- treat a reaching name read inside a nested `FunctionDef` / `Lambda` / `ClassDef` body as an
  escape (closure capture).

This is a fixable defect, not a tradeoff: each of these only turns "skip sweep" back into the base
behaviour of sweeping, which re-emits a `lead` that is de-duplicated against `observed`. Re-run
`EscapeGlobalHook` plus the repair set, precision and the corpus comparator after any such change.
`ReturnedGlobalCallableShadow` and `ForwarderPassesCallerArgument` depend on the gate saying
"no escape", and neither uses `global`, `yield` or keyword `update`.

## Files written

- `.ufo/waves/round-23/w2/out/AttackEscapeGate/fixtures/{EscapeGlobalHook,EscapeDictUpdateKeyword,EscapeYieldGenerator,EscapeWrapperClosure}.jsonl`
- `.ufo/waves/round-23/w2/out/AttackEscapeGate/run.py`, `probe.py`, `receipt.json`, `probe-receipt.json`
- this report.

Outside the lane: `/fast/scratch/hyaku/mado-r23/w2/AttackEscapeGate/{tool.py,base.py}`.
These fixtures are uncommitted working-tree files in my out dir; the L1 decides whether to adopt them.

No tool installs or updates. No host change, no lane git or jj write.

## Addendum — re-run against the repair (2026-10-22, L1 follow-up)

**Result against the repaired tip: improved 0, same-correct 5, same-wrong 0, REGRESSED 0.**
The `EscapeGlobalHook` regression is repaired. The inferred `nonlocal` variant was a real
regression at the old tip and is also repaired.

Target: lane tip `3732c7a73244fab87558c704107418e5de01436c` (repair commit `03227ddf`).
I extracted it into a fresh scratch dir that had no `__pycache__`:
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 3732c7a73244fab87558c704107418e5de01436c:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/AttackEscapeGate-r2/tool.py`.
Its sha256 is `e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`; base is unchanged at `cd9da20c…ea84`.

How I ran it:

- The four out-dir fixtures and `run.py` are byte-unchanged; their hashes match the first run.
- The fifth fixture is `EscapeNonlocalHook`. Function `outer` defines `register(callback)`, which
  does `nonlocal hook; hook = callback`; `outer` then calls `register(run)` and `hook()`. The
  fixture sha256 is `fcee11c1…4986`. I wrote it in scratch, not in the lane, because this
  follow-up allows edits only to this report.
- The runner is scratch `rerun.py` (sha256 `77271f3d…26f0`). It loads `run.py` with `runpy`,
  so truth, scan, `reading` and `verdict` are the same code as the first run. It also calls the
  tip's `parameter_escapes` on each receiving function, found by walking the tree; this parses
  fixture text only.
- Command: `(ulimit -v 393216; timeout 120 python3 -I rerun.py base.py tool.py)`, exit 0. The
  receipt is scratch `rerun-receipt.json`, sha256 `b4bb9cad…fca4`.

| Case | Truth executed | Base | Repaired tip | Tip gate `parameter_escapes` | Verdict |
|---|---|---|---|---|---|
| `EscapeGlobalHook` | `pacman -S r23w2-global-hook` | lead | lead (exit 1, unparsed 0) | True | same-correct (was REGRESSED) |
| `EscapeDictUpdateKeyword` | `pacman -S r23w2-dict-update` | lead | lead | True | same-correct |
| `EscapeYieldGenerator` | `pacman -S r23w2-yield` | lead | lead | True | same-correct |
| `EscapeWrapperClosure` | `pacman -S r23w2-wrapper-closure` | observed | observed | True | same-correct |
| `EscapeNonlocalHook` | `pacman -S r23w2-nonlocal-hook` | lead | lead | True | same-correct |

Every finding row still has class `host_mutation`.

**Control.** I ran the same runner against the old tip `41489991…a009` (scratch
`control-old-tip.json`, sha256 `44bb9440…f6c`). It gave REGRESSED 2 and same-correct 3:

- `EscapeGlobalHook`: silent miss again (exit 0, no rows). This reproduces the first run.
- `EscapeNonlocalHook`: silent miss (exit 0, no rows), which confirms the inference in the main
  report.
- The gate returned False for all five receivers.

So the repaired gate now answers "escapes" for all five, not only the two that regressed. That
matches its new allowlist docstring.

Scope: I did not re-measure the repair set, precision or the corpus comparator. They are the L1's
guards (commit `03227ddf` adds `evidence/guards-fix5-scratch.json`) and outside this re-run.
No tool installs or updates. The only lane edit in this follow-up is this addendum.
