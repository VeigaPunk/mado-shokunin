# AttackLateCell — wave 2 C1 attack: late enclosing-cell rebinding (RevTruthD F1)

Verdict: **no regression found.** Of the four delivered fixtures, two improved at the tip and two are wrong on both base and tip (`same-wrong`). A wider sweep of 27 scratch variants also found no case where the tip does worse than the base. The sweep did surface one **pre-existing silent miss** that the tip does not fix: a `def` nested inside any `for`, `while`, `if` or `try` body is invisible to both classifiers. Calling it yields no row and no unparsed count.

## What I did

1. Extracted the tip classifier into a fresh scratch dir with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/AttackLateCell/tool.py`. Its sha256 is `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`.
2. Copied the base classifier to `/fast/scratch/hyaku/mado-r23/w2/AttackLateCell/base/tool.py`. Its sha256 is `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`. I scanned the copy instead of the original because the round-21 scan wrapper loads the tool with `importlib` and no `-B`, which writes `__pycache__` beside the tool file. Scanning the lane path in place would have written into the lane.
3. Derived truth by running each fixture through the `CHILD` program from `round-23/repair/truth.py`, loaded with `runpy` so the code is byte-identical. It runs under `python3 -I -S` with the recording fake `subprocess`. Every fixture passed `truth.py`'s own `safe()` check: it imports only `subprocess` and calls only `subprocess.run` with names or list literals.
4. Scanned each fixture with base and tip through the unchanged `scan` from `round-21/oracle/measure.py`, which runs one child at a time with 384 MiB and 15 s caps.
5. Classified each case with the repair set's exact rule. A case is correct when the scanner exits 0 or 1 with no error, the rows equal the truth rows, the unparsed count is 0, and no `forbid_any` command appears at any tier. The case is marked REGRESSED if the base is correct and the tip is not, or if the tip adds a false observed row, a silent miss, or a forbidden-command row that the base did not have.

Commands, all run from `/fast/scratch/hyaku/mado-r23/w2/AttackLateCell`:

```
python3 -I -B probe.py <scratch>/probes [names...]   # 27-variant exploration
python3 -I -B deliver.py                             # four fixtures + receipts into out/AttackLateCell
```

Python 3.14.8. Scan helper sha256: `4eb893d2…c82da`. `truth.py` sha256: `7f9e7865…d18b0`.

## Delivered fixtures (`.ufo/waves/round-23/w2/out/AttackLateCell/`)

Truth passed 4/4 (`truth-receipt.json`). Full rows are in `scan-receipt.json`, and the exact `want` and `forbid_any` lists with sha256s are in `cases.json`.

| Fixture | Shape | Truth | Base | Tip | Class |
|---|---|---|---|---|---|
| `LateEnclosingLocalViaRelay` | The enclosing local is rebound after the nested def and before the call. The call goes through a sibling relay that has its own `argv` local. | `pacman -Q r23w2-late-cell` | false observed `pacman -S r23w2-relay-foreign` (host_mutation); silent miss of truth | correct | improved |
| `NonlocalRebindThenCallInSibling` | A sibling nested function does `nonlocal argv`, rebinds it, then calls the closure. | `pacman -Q r23w2-after-nonlocal` | no rows, unparsed 1 | no rows, unparsed 1 | same-wrong (both abstain honestly) |
| `LoopClosureCalledAfterLoop` | A closure is defined in a `for` body over the loop variable and called after the loop. | `pacman -Q r23w2-loop-last` | no rows, unparsed 0 (**silent miss**) | no rows, unparsed 0 (**silent miss**) | same-wrong |
| `SecondFrameInvokesFirstFrameClosure` | A closure from the first invocation of `outer` is called inside a second invocation of the same `outer`. This targets the tip keying frames as `("frame", id(def node))` rather than per invocation. | `pacman -Q r23w2-first-invocation` | correct row, but unparsed 1 (fails exact) | correct, unparsed 0 | improved |

Tally: improved 2, same-correct 0, same-wrong 2, REGRESSED 0.

## Wider sweep (scratch, `probe-sweep.json`, 27 variants)

There were no regressions in any of the 27 variants. Grouped by result:

- **Same-correct on both:** enclosing local rebound before a direct call; factory local rebound after the def and before `return`; two factory invocations with the first closure called; a call before and after rebinding (both values are reported).
- **Improved:** in addition to the two delivered cases, three more. A factory closure was passed to a relay that has its own `argv` parameter. A first-frame closure was invoked through a relay inside a second frame. A late rebind was followed by forwarding the closure to a nested forwarder. In all three, base had the correct row plus unparsed 1, which fails the exact rule. The tip has unparsed 0.
- **Honest abstention (unparsed > 0, no false row) on both:** every `nonlocal` and `global` rebind shape. This includes the caller doing `global argv; argv = …; helper()`, a forwarder that rebinds with `nonlocal` and then calls the callback, and a nested setter using `nonlocal`. It also covers a walrus rebind in the call's own statement, an `if`-guarded rebind, and a loop-assigned rebind before the call. The tip's per-scope "own view" could have produced a false observed of the pre-rebind value here, but it did not. Both versions refuse these shapes upstream.
- **Silent miss on both (pre-existing):** every case where the `def` sits inside a compound statement's body. That covers a closure over the loop variable in a function or at module level, closures collected in a list and called after the loop, and a def called inside the loop. It also covers `for`, `if True:`, `try:/finally:` and `while` bodies even when `subprocess.run` gets a **constant list literal** with no late binding at all. A bare `subprocess.run(argv)` directly in a `for` body is reported as unparsed, so the silence is specific to defs.

## Counterexample worth acting on (not a tip regression)

The following fixture is executed by Python (`pacman -Q r23w2-const-after-loop`). Base and tip both exit 0 with no findings and `eval_unparsed + unparsed_spawns == 0`:

```python
import subprocess
for n in (1, 2):
    def cb():
        subprocess.run(["pacman", "-Q", "r23w2-const-after-loop"])
cb()
```

The `if True:` and `try:` versions behave the same way. Swap the `-Q` for a mutating command and a real host mutation goes unreported, with no unparsed signal.

[INFERENCE] I believe the cause is in `prepare_eval_calls`. It calls `update_bindings` once per top-level statement, so a `FunctionDef` nested in a compound body never enters `bindings`. A later `cb()` is then neither followed nor counted as an unparsed spawn. I read the code shape but did not trace it with a debugger.

- Impacted axis: operability, meaning recall and silent misses. The frozen 12-case repair score is unaffected because none of the 12 fixtures has this shape.
- Smallest safe correction (advice only; the L1 decides): when a statement in a scope is a compound statement whose body defines a function or class, register that name so a later call to it is counted as an unparsed spawn. That abstains instead of staying silent. Following such defs is a larger change and is not required to close the silent path.

## Residual risk I could not exercise

The tip's frame key is the def node, not the invocation. My two collision attempts were both correct at the tip, because factory-returned closures appear to carry captured bindings. A collision through a non-returned path, such as recursion or a closure stored in a global, needs `global` or a conditional to construct inside the allowed shape. Those routes hit the honest-abstention guard instead, so this risk is untested rather than refuted.

## Hygiene

- Lane writes: only `.ufo/waves/round-23/w2/out/AttackLateCell/` (fixtures, `cases.json`, `truth-receipt.json`, `scan-receipt.json`, `probe-sweep.json`, plus copies of `probe.py` and `deliver.py`) and this report. All my own runs used `-B` and scanned only scratch copies.
- `.ufo/waves/round-23/evidence/__pycache__/tool-base-cd9da20c.cpython-314.pyc` appeared in the lane at 08:57:18 -0300. It was absent when I first checked, and my scripts never load that path. Its mtime falls inside my run window, so it was probably written by a peer scanning the base file in place, but I cannot prove that from timestamps alone. I left it untouched.
- Installs or updates: none.

## Addendum — re-run against repaired tip 3732c7a7 (lane commit 03227ddf)

The repaired tip has **1 regression** across the 27-variant sweep (`SecondFrameRelayInvokesFirstClosure`). This case was correct at the previous tip 2f1134f3, so the repair commit introduced it. The four delivered fixtures are unchanged: improved 2, same-wrong 2, REGRESSED 0.

- Tip: `git show 3732c7a73244fab87558c704107418e5de01436c:tools/mado-tripwire.py`, extracted into a fresh scratch dir `/fast/scratch/hyaku/mado-r23/w2/AttackLateCell-rerun-3732c7a7/`. Its sha256 is `e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`. The base is the same `cd9da20c` copy as before.
- Method: same truth `CHILD`, same round-21 `scan`, and the same classify rule (`verdict`/`classify` loaded from my original `deliver.py`). I scanned the four delivered lane fixtures read-only after checking their sha256 against `cases.json`. Receipt: `/fast/scratch/hyaku/mado-r23/w2/AttackLateCell-rerun-3732c7a7/rerun-receipt.json`, written to scratch only.

| Set | improved | same-correct | same-wrong | REGRESSED |
|---|---|---|---|---|
| Delivered fixtures (4) | 2 | 0 | 2 | 0 |
| 27-variant sweep | 4 | 4 | 18 | **1** |

Compared with the previous tip, 26 of 27 sweep cases give byte-identical rows and unparsed counts. The one change is the regression.

**REGRESSED: `SecondFrameRelayInvokesFirstClosure`.** The fixture is in scratch at `probes/fixtures/`. The closure `inner` from the first invocation of `outer` is called by a nested `relay` during a second invocation:

```python
import subprocess
def noop():
    pass
def outer(argv, cb):
    def inner():
        subprocess.run(argv)
    def relay():
        cb()
    relay()
    return inner
first = outer(["pacman", "-Q", "r23w2-first-relay"], noop)
outer(["pacman", "-S", "r23w2-second-relay"], first)
```

- Truth: only `pacman -Q r23w2-first-relay` runs.
- Base: correct row plus unparsed 1. It fails the exact rule but abstains honestly.
- Previous tip 2f1134f3: correct row, unparsed 0. This was a pass.
- Repaired tip 3732c7a7: correct row, plus `(host_mutation, pacman -S r23w2-second-relay, lead)`, unparsed 0. The extra row is a never-executed host mutation, reported at lead tier rather than observed, and it hits `forbid_any`.
- [INFERENCE, not traced] The likely trigger is the new per-call frame tokens. The relay call made during frame 2 appears to bind the first frame's closure body to frame 2's `argv`. The control case `SecondFrameInvokesFirstFrameClosure` calls `cb()` directly in `outer` with no relay, and it stays correct, which isolates the relay hop.

All findings from the original report still stand, and the repair did not change any of these results:

- The silent miss for a `def` inside a `for`, `while`, `if` or `try` body persists on 8 sweep cases. They all exit 0 with no rows and unparsed 0.
- `nonlocal`/`global` shapes still abstain honestly.

Lane writes in this re-run: this addendum only. Installs: none.
