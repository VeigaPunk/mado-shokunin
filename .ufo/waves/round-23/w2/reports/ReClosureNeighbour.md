# ReClosureNeighbour (W2 falsify): CritClosureNeighbour fixtures on the landed tip

Seat `MadoR23.ReClosureNeighbour` (reviewer, leaf, no subagents). Lane tip `2f1134f38930fc8b067d2d7f5bba126338faabdd`.
Tip classifier `tools/mado-tripwire.py`, sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`.
Base classifier `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py`, sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`.
Lane untouched (read-only `git show`, `grep`, `sha256sum`). All runs in scratch `/fast/scratch/hyaku/mado-r23/w2/ReClosureNeighbour/`.

## Verdict

**C1 does not regress the critic's three closure fixtures, but it regresses seven stored-callable neighbours of the same closure-lifetime family.** Do not call C1 clean on closure lifetime until the seven are routed.

- Critic's three fixtures, tip against base: 0 worse, 1 better (TwoFactory), 2 same. No `pacman -S` text at any tier or anywhere in the scanner output on tip.
- Full run, 50 items: 3 critic fixtures, 9 critic diagnostics, 3 round-20 call-site leads, 35 authored. Result: 13 better, 30 same, **7 worse**. No scanner error and no timeout in any item; every exit was 0 or 1.
- The seven worse items share one shape. A callable is handed to a receiving call that stores it (subscript, attribute or `append`), a global or factory local it reads is rebound after the handoff, and the callable is then called or never called. Tip emits a `lead` for the stale value, a `pacman -S` command that cannot run in that transcript. Tip also drops base's `unparsed` disclosure (1 to 0). In four items the command that does run, `pacman -Q`, is absent from the output.
- None of the seven shapes is in the frozen repair set. I also searched the round-21 corpus snapshot, the round-21 oracle and the round-22 files lexically; none has a store-then-rebind shape (Gaps).

**Operability read.** The tip is more operable on forwarder, callback and caller-local shapes: it removes three false `pacman -S` observed rows that base emits and clears ten unparsed residues, keeping a correct observed or lead row in each. It is less operable on stored callables rebound after the handoff: it adds false host-mutation leads and removes the disclosure base gave. The regression is the honesty-critical kind, so it outweighs the gains for a clean claim.

## Findings by severity

### 1. High, regression (7 items): stale handoff lead and lost disclosure

Items W2c-1, W2c-2, W2c-3, W2c-4, W2e-1, W2e-2, W2f-2 (table under "Authored neighbours"). Representative counterexample W2c-1:

```python
import subprocess
argv = ["pacman", "-S", "w2c-sub-initial"]
def run():
    subprocess.run(argv)
def register(cb, d):
    d["k"] = cb
hooks = {}
register(run, hooks)
argv = ["pacman", "-Q", "w2c-sub-final"]
hooks["k"]()
```

Truth: executed `pacman -Q w2c-sub-final`; `pacman -S w2c-sub-initial` never runs.
Base: exit 0, unparsed 1, no rows (disclosed).
Tip: exit 1, unparsed 0, one row `host_mutation pacman -S w2c-sub-initial lead`. The executed `pacman -Q` is absent.

Per-item effect:
- W2c-1, W2c-3, W2c-4, W2f-2: base exit 0 with one disclosed unparsed spawn. Tip exit 1 on a false host-mutation lead, unparsed 0, and the executed `pacman -Q` missing.
- W2c-2: nothing runs. Base is disclosed (unparsed 1). Tip emits a stale `pacman -S` lead and unparsed 0.
- W2e-1, W2e-2: base reports the correct observed `pacman -Q` with unparsed 1. Tip reports that row and also a foreign stale `pacman -S` lead, with unparsed 0.

### 2. Medium, pre-existing and not a regression: fail-open silent misses persist on both

- Critic's `LoopClosuresLateBinding`: executed `pacman -Q r23cc-loop-last`. Base and tip both exit 0, unparsed 0, no rows.
- Critic diagnostics A, C, F, G, H, I (closures defined under a loop or branch), authored W2-l (loop default-argument capture of an executed `-S`) and W2b-t (attribute-assigned callback called after a rebind). Both tools exit 0, unparsed 0, no rows.

The critic asked for these to be routed as new defects. The tip does not repair them.

### 3. Info: improvements on tip

- Caller-local leak: base emits a false observed `pacman -S` from a caller's local in W2-g, W2b-m (decorator wrapper) and W2b-n (unfollowed factory result). Tip emits the correct `pacman -Q` row in all three.
- Unparsed residue cleared with a correct row kept (observed or lead): critic TwoFactory (the critic required the `-Q` row to stay, and it does), critic diagnostic B, W2-j, W2c-5..8 (forwarder calls the callback under `if`, `for`, `try`, or directly), and W2d-1..3 (stored callbacks rebound before the handoff, or never rebound).

### 4. Residual, tradeoff: NonlocalReboundAfterFactory

Both tools keep unparsed 1 and no row. The critic's note accepts this as a disclosed tradeoff. I agree.

## Critic's three closure fixtures (per-case, required)

Probe receipts: `cases-tip.json` and `cases-base.json` (in scratch). The probe's JSON key `base` holds whichever tool was passed. In `cases-tip.json` it is the tip.

| Case | Truth: executed | Truth: never executed | Base exit / unparsed / rows / class | Tip exit / unparsed / rows / class | Tip against base |
|---|---|---|---|---|---|
| LoopClosuresLateBinding | `pacman -Q r23cc-loop-last` | `pacman -S r23cc-loop-first` | 0 / 0 / none / base-silent-miss | 0 / 0 / none / base-silent-miss | Same (fail-open on both) |
| NonlocalReboundAfterFactory | `pacman -Q r23cc-nonlocal-rebound` | `pacman -S r23cc-nonlocal-initial` | 0 / 1 / none / base-unparsed | 0 / 1 / none / base-unparsed | Same (disclosed miss on both) |
| TwoFactoryClosureReadsReboundGlobal | `pacman -Q r23cc-global-at-call` | `pacman -S r23cc-global-at-definition` | 1 / 1 / observed `pacman -Q r23cc-global-at-call` / base-unparsed | 1 / 0 / observed `pacman -Q r23cc-global-at-call` / base-correct | **Better**: residue cleared, row kept, decoy absent |

Forbidden `-S` text: absent from the full tip output for all three.

## Critic's diagnostics and round-20 call-site leads

Scratch variants reconstructed from `diag.json` and the round-20 AdvLeadMarks files (sha256 verified). Base reproduces each recorded base value (`base_diag_json=True` for all 12).

| Item | Truth: executed | Truth: never | Base exit / unparsed / rows | Tip exit / unparsed / rows | Tip against base |
|---|---|---|---|---|---|
| A loop-direct-call-in-factory | `pacman -Q d-last` | `pacman -S d-first` | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| B no-loop list-subscript call | `pacman -Q d-only` | none | 0 / 1 / none | 1 / 0 / lead `pacman -Q d-only` | Better |
| C module-loop direct call | `pacman -Q d-last` | `pacman -S d-first` | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| D module-loop body spawn | `pacman -S d-first`, `pacman -Q d-last` | none | 0 / 1 / none | 0 / 1 / none | Same (disclosed) |
| E nonlocal, no rebind | `pacman -Q d-only` | none | 1 / 0 / observed `pacman -Q d-only` | same | Same |
| F if-def | `pacman -Q d-only` | none | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| G try-def | `pacman -Q d-only` | none | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| H while-def | `pacman -Q d-only` | none | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| I for-loop defines `run` and calls it inside the loop body | `pacman -Q d-only` | none | 0 / 0 / none | 0 / 0 / none | Same (silent) |
| r20 lead-if-true-def | `pacman -Q hyprland` | none | 1 / 0 / lead `pacman -Q hyprland` | same | Same |
| r20 lead-try-def | `pacman -Q hyprland` | none | same | same | Same |
| r20 lead-while-false-def | `pacman -Q hyprland` | none | same | same | Same |

## Authored neighbours

My own fixtures, same JSONL shape and harness. Truth comes from the critic probe's fake-subprocess child and scans from the round-21 helper. Shorthand: `-Q x` is `pacman -Q x`; `obs` is observed; `lead` is lead; `FO` is a foreign row (any row for a command that did not run); `none` is no rows. Exit and unparsed are written as `exit/unparsed`.

**Set W2 (`w2.py`)**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| a same-frame rebind before return | `-Q w2-same-frame-final` | `-S ...initial` | 1/0 obs `-Q` final | 1/0 obs `-Q` final | Same |
| b call inside factory after rebind | `-Q` inside-final | `-S` inside-initial | 1/0 obs `-Q` final | same | Same |
| c module rebind before nested call | `-Q` module-final | `-S` module-initial | 1/0 obs `-Q` final | same | Same |
| d positive: factory parameter | `-Q` param-arg | none | 1/0 obs | same | Same |
| e default-argument decoy, called with an argument | `-Q` passed | `-S` default-decoy | 1/0 obs | same | Same |
| f `global`-statement rebind inside a function | `-Q` global-stmt-final | `-S` initial | 0/1 none | 0/1 none | Same (disclosed) |
| g caller-local shadows global (H4 shape) | `-Q` caller-global | `-S` caller-local-decoy | 1/0 FO `-S` caller-local | 1/0 obs `-Q` caller-global | Better |
| h factory-local shadows global | `-S` factory-local | `-Q` global-decoy | 1/0 obs `-S` factory-local | same | Same |
| i dict-literal escape, global rebound, subscript call | `-Q` dict-final | `-S` dict-initial | 1/0 obs `-Q` final | same | Same |
| j forwarder calls callback after rebind | `-Q` forward-final | `-S` forward-initial | 1/1 obs `-Q` final | 1/0 obs `-Q` final | Better |
| k nested two-level rebind | `-Q` nested-final | `-S` nested-initial | 1/0 obs `-Q` final | same | Same |
| l loop default-argument capture, executed `-S` | `-S` loopdef-first | `-Q` loopdef-last | 0/0 none (silent) | 0/0 none (silent) | Same (fail-open) |

**Set W2b (`w2b.py`)**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| m decorator wrapper, caller-local shadow | `-Q` deco-global | `-S` deco-caller-local | 1/0 FO `-S` | 1/0 obs `-Q` | Better |
| u decorator, positive control | `-Q` deco-plain | none | 1/0 obs | same | Same |
| n factory result unfollowed, caller-local shadow | `-Q` fallback-global | `-S` fallback-caller-local | 1/0 FO `-S` | 1/0 obs `-Q` | Better |
| o lambda closure rebound after definition | `-Q` lambda-final | `-S` lambda-initial | 1/0 obs `-Q` final | same | Same |
| p method reads a rebound module global | `-Q` method-final | `-S` method-initial | 1/0 obs | same | Same |
| q alias name rebound to another function | `-Q` alias-actual | `-S` alias-decoy | 1/0 obs | same | Same |
| s dict-literal store, never called, rebound after | nothing runs | `-Q` final, `-S` initial | 0/0 none | 0/0 none | Same |
| t attribute assignment, rebound, called via attribute | `-Q` attr-final | `-S` attr-initial | 0/0 none (silent) | 0/0 none (silent) | Same (fail-open) |

**Set W2c (`w2c.py`), escape-gate recall**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| 1 subscript store in receiver, called later, rebound after handoff | `-Q` sub-final | `-S` sub-initial | 0/1 none | 1/0 lead `-S` sub-initial (stale); `-Q` absent | **WORSE** |
| 2 subscript store, never called, rebound after handoff | nothing runs | `-S` never-initial, `-Q` never-final | 0/1 none | 1/0 lead `-S` never-initial (stale) | **WORSE** |
| 3 attribute store in receiver, called later, rebound after | `-Q` attrparam-final | `-S` attrparam-initial | 0/1 none | 1/0 lead `-S` attrparam-initial (stale); `-Q` absent | **WORSE** |
| 4 module-level append, rebound after, subscript call | `-Q` append-final | `-S` append-initial | 0/1 none | 1/0 lead `-S` append-initial (stale); `-Q` absent | **WORSE** |
| 5 forwarder calls callback under `if` | `-Q` if-final | `-S` if-initial | 1/1 obs `-Q` | 1/0 obs `-Q` | Better |
| 6 forwarder calls callback under `for` | `-Q` for-final | `-S` for-initial | 1/1 obs `-Q` | 1/0 obs `-Q` | Better |
| 7 forwarder calls callback under `try` | `-Q` try-final | `-S` try-initial | 1/1 obs `-Q` | 1/0 obs `-Q` | Better |
| 8 forwarder calls callback directly | `-Q` direct-final | `-S` direct-initial | 1/1 obs `-Q` | 1/0 obs `-Q` | Better |

**Set W2d (mechanism controls)**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| 1 subscript store, rebound before handoff | `-Q` sub-final | `-S` sub-initial | 0/1 none | 1/0 lead `-Q` sub-final (correct) | Better |
| 2 subscript store, no rebind | `-S` norebind | none | 0/1 none | 1/0 lead `-S` norebind (correct) | Better |
| 3 attribute store, rebound before handoff | `-Q` attr-final | `-S` attr-initial | 0/1 none | 1/0 lead `-Q` attr-final (correct) | Better |

**Set W2e (direct call after a rebind that follows the handoff)**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| 1 subscript store, rebound after handoff, direct call | `-Q` direct-final | `-S` direct-initial | 1/1 obs `-Q` | 1/0 obs `-Q` plus FO lead `-S` direct-initial (stale) | **WORSE** |
| 2 module-level append, rebound after, direct call | `-Q` append-final | `-S` append-initial | 1/1 obs `-Q` | 1/0 obs `-Q` plus FO lead `-S` append-initial (stale) | **WORSE** |

**Set W2f**

| Id | Truth: executed | Never executed | Base | Tip | Verdict |
|---|---|---|---|---|---|
| 1 rebind inside a helper through `global`, after handoff | `-Q` helper-final | `-S` helper-initial | 0/1 none | 0/1 none | Same (disclosed) |
| 2 factory-local rebind after handoff, subscript call | `-Q` factory-final | `-S` factory-initial | 0/1 none | 1/0 lead `-S` factory-initial (stale); `-Q` absent | **WORSE** |

## Mechanism of the seven regressions

Code locations are in the tip file `tool.py` in scratch (same bytes as the lane file at the tip).

1. The handoff reference loop records the handoff statement's scope view with `scope_entry` (tool.py:2916-2923).
2. The escape gate `reference_escapes` decides that a stored callable escapes (tool.py:2970-2972). The sweep then runs on the callee body (tool.py:2976-2980).
3. `sweep_body` builds the swept body's free-name view with `scope_view` (tool.py:2435-2459) at that moment (tool.py:2579-2580). That is the handoff, not the later call.
4. `ctx["swept"]` allows each body to be swept once per cell (tool.py:2573-2575). The later rebind is never seen, and the later call through the container adds nothing.
5. Base sweeps the same body with an empty environment (`base/tool.py:2380`, `prepare_eval_calls(body, {}, ...)`). The free name is unknown and counted as `unparsed_spawns`. That is why base discloses these shapes.

Controls: a rebind before the handoff (W2d-1, W2d-3) or no rebind (W2d-2) gives the correct lead with no unparsed. Only a rebind after the handoff gives the stale value. So the lead carries the value at the handoff statement.

Not reproduced: a rebind inside a helper function through a `global` statement (W2f-1). Both tools disclose it as unparsed 1. I did not establish why.

Not affected: a dict-literal assignment followed by a subscript call (W2-i), which is not a call handoff, and calls under compound statements, which are now observed (W2c-5..8).

## Reproduction

All commands run from `/fast/scratch/hyaku/mado-r23/w2/ReClosureNeighbour`.

1. Tip classifier: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > tool.py`. Read-only git.
2. Base classifier: `cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/evidence/tool-base-cd9da20c.py base/tool.py`.
3. Mirror. I copied the critic's out directory to `.ufo/waves/round-23/w1/out/CritClosureNeighbour/` under the seat, and the round-21 helper to `.ufo/waves/round-21/oracle/measure.py`. The runner computes `LANE = ROOT.parents[5]` to find the helper, so the mirror keeps the lane depth. Runner `probe.py` sha256 `abf3e40b…d7cd` (unchanged). Helper sha256 `4eb893d2…2c82da` (unchanged).
4. `python3 -I <mirror>/probe.py --tool tool.py` writes `cases-tip.json`. `python3 -I <mirror>/probe.py --tool base/tool.py` writes `cases-base.json`. The base run reproduces the critic's receipt exactly (sha256 `97cfb287…b235`).
5. `python3 -I dump.py` writes `dump.json`: three fixtures, diagnostics and round-20 leads, with full scanner output and receipt cross-checks (all true).
6. `python3 -I w2.py`, `w2b.py`, `w2c.py`, `w2d.py`, `w2e.py`, `w2f.py` write `w2-dump.json`, `w2b-dump.json`, `w2c-dump.json`, `w2d-dump.json`, `w2e-dump.json`, `w2f-dump.json`. Console output is in `*-run.txt`. Reruns of w2c, w2e and w2f were byte-identical (`cmp`).
7. Authored fixtures are in `w2/*.jsonl`. Truth is computed only by the probe's fake-subprocess child (`python3 -I -S`). Scanning is done only by the helper (`python3 -I`, RLIMIT_AS 384 MiB, 15 s).

Why a copy of the base classifier: the helper loads the tool with importlib, which writes `__pycache__` beside the file, and `-I` does not suppress that. Running it on the lane's evidence file would have written into the lane. I checked that the critic's out directory in the lane still has no `__pycache__`.

Receipt sha256 (prefixes): `cases-tip.json` `45508435…`, `cases-base.json` `97cfb287…`, `dump.json` `a4ceb3d9…`, `w2-dump.json` `fc3e653d…`, `w2b-dump.json` `ada7e318…`, `w2c-dump.json` `fd74ddb6…`, `w2d-dump.json` `aacfe97d…`, `w2e-dump.json` `6a1e31b6…`, `w2f-dump.json` `7032b97d…`.

Regression fixture sha256 (prefixes): W2c-1 `b7a8d94c…`, W2c-2 `e6c78baf…`, W2c-3 `ba2f8e4f…`, W2c-4 `9b16e20c…`, W2e-1 `35e30326…`, W2e-2 `71df6085…`, W2f-2 `5ebe6a97…`.

## Advice (not implemented; no lane file touched)

- A swept body's free name that is rebound after the handoff should stay unknown (unparsed), as base does. Or the sweep for a stored callable should be deferred to the call site. [INFERENCE] A literal-argv body keeps its lead either way, since its argv does not depend on a free name.
- Add one rebind-after-store case to the repair set before re-measuring. The existing `CallbackStoredInDict` and `CallbackStoredOnAttribute` fixtures pin only the form with no rebind, which the tip passes.

## Gaps and limits

- Not run: the 12-case repair counter, the round-22 and round-21 guards, the 1356-file corpus comparator, the selftests and the precision set. Other seats own them.
- Corpus exposure is lexical only. Pattern `] = (cb|callback|hook|handler|run|fn|func|cmd|action)\b`, `.cb =`, or `.append(<name>)`. It matches 0 files in the round-21 corpus snapshot (1356 files) and 0 in the round-21 oracle. It matches 7 files in round-22, none of them a store-then-rebind shape. The pattern is live: it matches the two frozen `CallbackStored*` repair fixtures. The precision and selftest populations were not searched.
- Round-22 `residual/ResidualForward.md` item 2 already named `register(run); hooks["k"]()` as a neighbour that no frozen input covers. The seven regressions are a rebind-after-store version of that neighbour.
- The authored expectations follow the critic's rule that any forbidden `-S` at any tier is a regression. Each stale lead names a command that cannot run in its transcript, because the value is replaced before any call.
- The probe's `classify` labels any foreign row, lead or observed, as `base-false-observed`. The tables above state row tiers explicitly.
- Not measured: a lambda stored by subscript and rebound, and a stored-callable handoff inside a class method. I expect the same mechanism; I did not run them.
- Operability: no scanner error, no timeout and no exit 2 in any of the 50 items.
- Provenance: the 35 authored fixtures are uncommitted scratch files under `w2/`; the three round-20 leads are sha256-verified copies of lane files. The classifier scanned them through the round-21 helper (`python3 -I`, 384 MiB, 15 s), the same way the critic scanned its diagnostics. Nothing was executed outside the recording fake-subprocess child. If the L1 requires committed fixture data for wave-2 evidence, the 35 authored items are not admissible as they stand, and the seven regressions would then need a committed repro.

## Tooling

No installs or updates. Used read-only `git show`, `cp` into scratch, `sha256sum`, `grep` and `python3 -I` (Python 3.14.8, system interpreter). No jj commands. No lane writes other than this report.

**Verdict:** C1 is falsified on the closure-lifetime family. The critic's three fixtures show no regression (TwoFactory better; LoopClosures and NonlocalRebound unchanged). Seven stored-callable neighbours with a rebind after the handoff regress on tip: a stale forbidden `pacman -S` lead at lead tier, the `unparsed` disclosure dropped in all seven, and the executed `pacman -Q` absent in four. Route as a regression before C1 is called clean on closure lifetime.
