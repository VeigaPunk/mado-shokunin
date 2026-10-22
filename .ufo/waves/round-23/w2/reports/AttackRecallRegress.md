# AttackRecallRegress — wave 2 falsify, C1 recall regressions of the callback-sweep gate

Seat: `MadoR23.AttackRecallRegress` (critic, leaf). Target: landed lane tip `2f1134f38930fc8b067d2d7f5bba126338faabdd`,
classifier `tools/mado-tripwire.py` sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`
(the C1 change in commit 2e592aff). Base: `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py` (sha256 `cd9da20c…ea84`).

**Verdict: C1 has a no-harm defect. The new callback-sweep gate (`reference_escapes` → `parameter_escapes`) drops recall
the base had. All four delivered fixtures REGRESSED: in each one, the base reported the executed command as a `lead` and
the tip reports nothing. The exploratory battery found 13 regressions in 45 shapes, with 0 improvements and 0 new
false-observed or unparsed results.** The registered 12/12 still holds. None of the registered guards covers these
shapes: the corpus comparator reported 0 removed findings, so the corpus contains no instance of them.

## What I did

1. Extracted the tip classifier into a fresh directory with no `__pycache__`:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/AttackRecallRegress/tool.py`
   (sha256 `41489991…a009`, the same as the registered C1 bytes).
2. Read the gate at the tip: `parameter_escapes` (line 2471), `reference_escapes` (line 2527) and the gate call site (line 2971,
   `if not reference_escapes(parent, ref, rbindings, penv): continue`).
3. Wrote a probe harness, `out/AttackRecallRegress/probe.py`. For each case it:
   - writes a JSONL fixture in the same shape as `repair/fixtures/*.jsonl`;
   - applies `truth.py`'s own `safe()` check and runs its unchanged `CHILD` under a recording fake `subprocess` module
     (both are extracted from `repair/truth.py` by AST, not copied by hand), using `python3 -I -S`;
   - scans the fixture with the base and then the tip, one child at a time, through the round-21 helper
     (`runpy(.ufo/waves/round-21/oracle/measure.py)['scan']`, 384 MiB / 15 s);
   - checks that the sha256 of the tool, helper and truth file did not change during the run.
   A case is correct when the scanner exits cleanly, every executed command appears as `observed` or `lead`, no
   non-executed command appears as `observed`, and the unparsed count is 0. A case REGRESSED when the base was correct
   and the tip is not.
   Commands: `python3 -I probe.py cases1.json probes1 probe1-result.json` and the same for `cases2`, both run in
   `/fast/scratch/hyaku/mado-r23/w2/AttackRecallRegress`. Python 3.14.8.
4. Picked one fixture for each of the four requested shapes and wrote them under `out/AttackRecallRegress/fixtures/`.
   They import only `subprocess`, call only `subprocess.run` with list literals, and pass `truth.py`'s `safe()`.

## The four fixtures (receipt `out/AttackRecallRegress/receipt-final-base-vs-tip.json`)

| Fixture (sha256 prefix) | Shape | Truth executes | Base | Tip | Verdict |
|---|---|---|---|---|---|
| `RecallConditionalAugAssignStore` (931c2432) | the followed consumer stores the callback **conditionally** with `box.cbs += [callback]`, then the module loops over `box.cbs` and calls each item | `pacman -S r23y-aug-cond` | lead | nothing | **REGRESSED** (silent miss) |
| `RecallTryExceptDunderCall` (d52885d4) | the followed consumer calls the callback through **try/except** as `callback.__call__()` | `pacman -S r23y-try-dunder` | lead | nothing | **REGRESSED** (silent miss) |
| `RecallSecondCallDunder` (c9fc86a1) | the followed consumer calls `a()` (followed), then makes a **second call that is not followed**, `b.__call__()` | `pacman -S r23y-second-dunder` | lead | nothing | **REGRESSED** (silent miss) |
| `RecallClosureStoredInDict` (eb2aa4e6) | the consumer wraps the callback in a nested `def inner(): callback()` and **stores** it (`hooks["k"] = inner`); the module calls `hooks["k"]()`. This is a one-step neighbour of the frozen `CallbackStoredInDict` case | `pacman -S r23x-closure-dict` | lead | nothing | **REGRESSED** (silent miss) |

The tip produced no false observed rows, no foreign rows and no unparsed spawns on any of the four. Every failure is a
silent miss of a command that executes.

Code of `RecallClosureStoredInDict` (the other three are in `cases-final.json`):

```python
import subprocess
hooks = {}
def run():
    subprocess.run(["pacman", "-S", "r23x-closure-dict"])
def register(callback):
    def inner():
        callback()
    hooks["k"] = inner
register(run)
hooks["k"]()
```

## Exploratory battery (45 shapes, `probe1-result.json`, `probe2-result.json`; inputs in `cases1.py` and `cases2.py`)

- **REGRESSED (13):** `AugAssignGlobalList`, `AugAssignAttrList`, `AnnAssignAttr`, `AnnAssignSubscript`, `GlobalNameStore`
  (`global saved; saved = callback`), `ClosureStoredInDict`, `DefaultArgClosureAppended` (`def inner(cb=callback)`),
  `DunderCallInvoke`, `WalrusThenReturnHolder`, `ConditionalTryDunder`, `SecondCallDunderAfterCall`, `AugAssignConditional`,
  `AnnAssignInTry`. In every one, the base reports `lead` and the tip reports nothing.
- **same-correct (30).** These include plain conditional calls, early return, `try`/`except`/`else`/`finally` calls,
  `while`, `match`, nested-def calls, immediately invoked lambdas, comprehensions, decorators, `yield`, keyword and star
  arguments, `.update(k=cb)`, and a store made through a second helper. Conditional and try/except calls are safe when the
  consumer calls the callback by name, because the follower reads both branches and every try clause.
- **same-wrong (2):** `ConditionalFalseSkips` (both base and tip report a false observed row for a branch that never runs)
  and `NonlocalStoreReturned` (both miss it). Neither is caused by C1.
- **improved: 0.**

## Root cause

`parameter_escapes` works from a blocklist. It counts a value as escaping only when it appears in an `ast.Assign` to a
non-Name target, in a `return`, as an argument to a call other than the callback itself, or as an argument to an
`ESCAPE_METHODS` call. Every other use is treated as "only called, so the followed call reads it". Python has more ways to
keep a value than that list covers:

- `AugAssign` and `AnnAssign` are not handled at all.
- A plain Name `Assign` to a name declared `global` or `nonlocal` is treated as a local alias.
- A walrus (`NamedExpr`) does not propagate the alias.
- Capture by a nested `def`, including through its default arguments, never adds the def's name to `reaches`.
- Attribute calls on the callback, such as `callback.__call__()`, count as "not an escape", but the follower does not
  resolve them.

The design note (`w1/out/ExecFullB/design-note.md` §8) says the analysis "errs toward sweeping (no lost findings)". The
first regression above falsifies that statement.

Impacted axes: **operability (recall)**, through a C1 no-harm defect: lost `lead` rows for commands that execute. There is
also a **provenance/calibration** issue: the design note claims a property that the code does not have.

This is a fixable defect, not a tradeoff. The base swept these callables, and the repair-set wins do not depend on
leaving them unswept (shown below).

## Smallest safe correction (prototyped in scratch only; no lane file was touched)

Turn `parameter_escapes` into an allowlist. A value counts as not escaping only when every load of a reached name is one
of these two uses:

- the `func` of a call (`cb(...)`);
- the whole right-hand side of a plain `Assign` whose targets are all Names that are not declared `global`/`nonlocal` in
  the body. That case only adds an alias.

Any load inside a nested `def`, `lambda` or `class` counts as an escape (capture), and so does any other use. The diff is
`out/AttackRecallRegress/prototype-correction.diff`: one function, 70 diff lines. Prototype sha256 `f3eab240…7bd7`.

Measured on the prototype (scratch, run by this seat):

| Check | Result | Receipt |
|---|---|---|
| Four delivered fixtures | 4/4 same-correct | `receipt-final-base-vs-prototype.json` |
| 45-shape battery | all 13 regressions become same-correct; no case gets worse (the same 2 same-wrong cases remain, both present at the base) | `fix1-result.json`, `fix2-result.json` |
| Frozen repair set: `python3 -I .ufo/waves/round-23/repair/measure.py --tool tool-fix.py` | 12/12 | `fix-repair.json` |
| Round-22 oracle: `python3 -I .ufo/waves/round-22/oracle/measure.py --tool tool-fix.py` | 57/57 | `r22-oracle-prototype.json` |
| Round-22 residual truth: `python3 -I .ufo/waves/round-22/residual-truth/measure.py --tool tool-fix.py` | 4/4 | `r22-residual-prototype.json` |

The tip also scored 57/57 and 4/4 on the same two round-22 commands. **Not run on the prototype:** round-21 replay
35/35+17/17, precision 166/175 with the same passing set, the eleven selftest suites, the 1356-file corpus comparator, and
the resource guards. Those checks have not passed. The L1 should run them before admitting any correction.

## Recommendation to the judge

- Do not count the C1 no-harm guards as clean on the strength of the registered population alone. On the four delivered
  fixtures, the landed tip has lower recall than the base.
- Admit the four fixtures (or an equivalent set) as recall guards with the `present` rule; they fail at the tip.
- Fix the gate with the allowlist correction or something equivalent, then rerun the full guard list.

## Files written

Only `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/out/AttackRecallRegress/` (the fixtures, the
harness, the case generators and the receipts) and this report. All scratch work is in
`/fast/scratch/hyaku/mado-r23/w2/AttackRecallRegress/`. I ran no git write and no jj command. Nothing was installed or
updated.

## Addendum — re-run against the repaired tip 3732c7a7 (2026-10-22, re-run only)

Tool: `git show 3732c7a73244fab87558c704107418e5de01436c:tools/mado-tripwire.py`, extracted into a fresh directory
`/fast/scratch/hyaku/mado-r23/w2/AttackRecallRegress/rerun-3732c7a7/` (no `__pycache__`), sha256
`e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`. The harness and inputs are the same as above:
`probe.py` with `cases1.json`, `cases2.json` and `cases-final.json`, base `cd9da20c…` against this tool. The four
fixtures were regenerated in scratch and are byte-identical to the delivered ones (sha256 eb2aa4e6, 931c2432, c9fc86a1,
d52885d4).

| Population | REGRESSED | same-correct | same-wrong | improved |
|---|---|---|---|---|
| All 45 probe shapes | **0** | 43 | 2 | 0 |
| The four delivered fixtures | **0** | 4 | 0 | 0 |

- All 13 earlier regressions are now same-correct. None of the 45 shapes has a false observed row, a foreign row or an
  unparsed spawn that the base did not have.
- The 2 same-wrong cases are the same two as before, and the base has both: `ConditionalFalseSkips` (a false observed
  row for a branch that never runs) and `NonlocalStoreReturned` (missed by both). Neither is caused by C1.
- Frozen repair set at this tool: `python3 -I .ufo/waves/round-23/repair/measure.py --tool <rerun>/tool.py` gives 12/12.
- Receipts (scratch, not lane): `rerun-3732c7a7/{cases1,cases2,cases-final}-result.json` and `rerun-3732c7a7/repair.json`.
- Scope: I re-ran only this seat's probes and the repair set. I did not run the other no-harm guards (round-21 replay,
  precision, selftests, corpus comparator, resource). No lane file was edited except this report. Nothing was installed.

Verdict: the C1 recall regressions this seat found are repaired at 3732c7a7.
