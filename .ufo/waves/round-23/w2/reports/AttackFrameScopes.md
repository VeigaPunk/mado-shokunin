# AttackFrameScopes — wave 2 falsify report (C1, scope-chain edge cases)

Verdict: **C1 REGRESSES.** The tip classifier (`2f1134f3:tools/mado-tripwire.py`, sha256 `41489991…`) is worse than the base (`cd9da20c…`) on 4 of 4 delivered fixtures and on 11 of 41 discovery probes. In every regression the base was exactly right, or honestly unparsed, and the tip produces a false `observed` row, a silent miss, or both. The regressions come from three independent defects in the new provenance mechanism. None of the frozen guard suites contains these shapes.

## What I did

1. Extracted the tip into a fresh empty dir: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/AttackFrameScopes/tool.py`. I copied the base from `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py`. `sha256sum` printed tip `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` and base `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`. The import loader later wrote a `__pycache__` beside them during scans; the source files were not changed.
2. Read the design note `w1/out/ExecFullB/design-note.md` and diffed base against tip.
3. Wrote a probe harness, `discovery/probe.py`. Truth comes from the `CHILD` recording fake-`subprocess` runner, copied byte-for-byte from `repair/truth.py` and run as `python3 -I -S`, after the same `safe()` AST gate. Scans go through the unchanged round-21 helper (`runpy(.ufo/waves/round-21/oracle/measure.py)["scan"]`: `python3 -I`, 384 MiB, 15 s, one child at a time) for base, then tip.
4. Ran 41 discovery probes (`discovery/mkprobes.py` with 27 probes, `discovery/mkprobes2.py` with 14 controls and variants). Then I authored the 4 delivered fixtures (`discovery/mkfinal.py`) and measured them as the receipt.
   - Commands: `python3 -I mkprobes.py probes && python3 -I probe.py probes probes-result.json`, the same pair for `probes2`, then `python3 -I mkfinal.py $OUT && python3 -I probe.py $OUT/fixtures $OUT/receipt-fixtures-base-vs-tip.json`.
   - `probe.py` expects `base.py` and `tool.py` in its own directory.

How cases are graded: **correct** means the observed set equals the executed set, there are no extra rows, there are no lead-only rows for executed commands, and unparsed is 0. **REGRESSED** means the tip adds a false observed row or a miss compared with base, or base was correct and the tip is not.

All outputs are under `.ufo/waves/round-23/w2/out/AttackFrameScopes/`: `fixtures/*.jsonl`, `cases.json` (repair-set shape: exact kind, want, forbid_any, sha256), `receipt-fixtures-base-vs-tip.json`, and `discovery/` (scripts, `probes1-result.json`, `probes2-result.json`, `tools.sha256`).

## Delivered fixtures (all REGRESSED)

| Fixture | sha256 | Truth (executed) | Base | Tip |
|---|---|---|---|---|
| `FrameReusedBySecondInvocation` | `e0510933…` | `pacman -Q w2-afs-first-frame` | correct (observed) | **false observed** `pacman -S w2-afs-second-frame`, true command missed |
| `FrameReusedBothClosuresCalled` | `8eacf719…` | `-Q w2-afs-both-first`, `-Q w2-afs-both-second` | correct (both observed) | **silent miss** of `-Q w2-afs-both-first` |
| `NestedBinderFreezesLateGlobal` | `d7f16cc0…` | `pacman -Q w2-afs-late-global` | correct (observed) | **false observed** `pacman -S w2-afs-early-global`, true command missed |
| `MatchCaptureBinderNotOwned` | `5cdc9cb4…` | `pacman -Q w2-afs-match-capture` | honest `unparsed_spawns` 1, no rows | **false observed** `pacman -S w2-afs-module-global`, unparsed 0 (the miss is now hidden) |

Full sha256 values are in `cases.json`. The fixtures import only `subprocess`, call only `subprocess.run(name)`, and pass the `truth.py` `safe()` gate.

## Counterexamples and mechanisms

### D1: frame identity is the def node, not the frame (4 + 1 regressing probes)

`frame_scope(fn)` returns `("frame", id(fn))` (tip line 1337), and `follow_helper` overwrites `ctx["scopes"][frame_scope(helper)]` on every follow (tip line 2662). Every invocation of the same function therefore shares one scope view. A closure from an earlier invocation reads names through the scope chain of whichever invocation was followed last. The closure overlay protects only names the closure captures itself, not names read by a sibling nested def it calls.

```python
def outer(argv):
    def leaf(): subprocess.run(argv)
    def inner(): leaf()
    return inner
f = outer(["pacman", "-Q", "first"])
outer(["pacman", "-S", "second"])   # never runs leaf; overwrites frame(outer)
f()                                 # tip: observed "-S second"
```

The same defect shows up when the second invocation is assigned and never called (Q05), when both closures run (Q06, a silent miss), when the closure goes through a shadowing forwarder (Q07), and when the second invocation sits inside another helper (Q14). Controls: one invocation only (Q01) and a direct capture with no sibling def (Q03) are both same-correct, which isolates the shared frame key as the cause.

This is also false provenance. Design note §2 says "A frame's identity is the function object that owns it, which is the 'function frame object that executed the def' the L1 asked for". The code keys on the AST `def` node, which is shared by every frame. The L1's mechanism asked for the frame object.

### D2: `own_names` over-approximates by walking into nested scopes (4 regressing probes)

`own_names` runs `ast.walk` over the whole body (tip line 1354), so a name bound only inside a nested `def`, a nested `class` body, or a loop inside a nested def counts as owned by the enclosing frame. That frame's view then freezes the module value from the moment it was followed, and S121 late global binding (the design's own §3 rationale) is lost:

```python
argv = ["pacman", "-S", "early"]
def outer():
    def other(): argv = ["pacman", "-S", "other-local"]
    def inner(): subprocess.run(argv)
    return inner
f = outer(); argv = ["pacman", "-Q", "late"]; f()   # tip: observed "-S early"
```

Regressing probes: P13 (nested-def binder), P15 (nested-def binder seen through a sibling leaf), Q08 (nested class attribute binder), Q09 (nested `for` binder). Control Q02, the same shape without `other`, is same-correct; that is the round-22 `CaptureGlobalLate` shape, which is why the guards miss this. A comprehension binder (P14) happened to stay correct.

### D3: `own_names` under-approximates; it misses `match` and `with` binders (2 regressing probes)

`own_names` handles neither `match` capture patterns (`MatchAs`, `MatchStar`, mapping rest) nor `with … as` targets. A frame that binds `argv` that way has no `argv` in its own view, so the chain falls through to the module global. Base reported `unparsed_spawns` 1, which is honest. The tip reports a confident false `observed` row with unparsed 0, which converts a visible gap into a hidden wrong answer. Regressing probes: Q10 (match) and Q11 (with-as). `except … as` and `del` are probably in the same class [INFERENCE: not probed, because an exception object cannot reach `run` inside the fixture shape].

## The briefed edge cases (none of them regressed)

| Edge case | Probes | Result |
|---|---|---|
| Helper defined in a class body, run during class creation | P01 | same-wrong (both silent; the class-body call is never scanned) |
| Method reads a global that a class attribute shadows (module-level or class inside a function) | P02, P03 | same-correct |
| staticmethod/classmethod reads a global or callable shadowed by the caller | P04, P05, P06 | improved |
| def nested two deep, called from a third function | P07–P10 | P07, P08, P09 improved; P10 same-correct |
| Module helper redefined after a forwarder captured it | P16–P20 | P16 (default-argument capture) same-wrong, both report the redefinition; P17, P18 same-correct; P19, P20 improved |
| `global` statement | P21–P25 | P21, P23, P24, P25 same-wrong (both unparsed; a `global` declaration alone defeats tip resolution even with no shadowing); P22 improved (base false observed → tip unparsed) |

Other probes: P12, P26, P27, and Q12 improved. Q04 (two frames of the same method) and Q13 (recursion) are same-wrong.

Totals over the 41 probes: 13 improved, 9 same-correct, 8 same-wrong, **11 REGRESSED**.

## Impacted axes

- **Operability (C1):** the no-harm claim does not hold beyond the frozen guard populations. The comparator, oracle, and precision suites contain neither repeated-invocation closures nor nested-binder or `match`/`with` binder frames, so "0 removed, 0 added" is saturation of those suites, not absence of harm.
- **Precision:** false observed rows (D1, D2, D3).
- **Recall:** a silent miss of an executed command (D1, `FrameReusedBothClosuresCalled`).
- **Honesty of unparsed counts:** D3 turns `unparsed_spawns` 1 into 0 alongside a wrong row.

## Smallest safe correction (advice; not applied)

1. **D1:** give each followed invocation its own scope token, for example a per-`follow_helper` counter or `id()` of the per-call bindings dict. Carry the defining scope on the per-invocation binding dict (`bindings[name]["scope"]`), not on the shared AST attribute `node.mado_scope`. The closure or factory binding should then keep its own frame's view, so a later follow of the same def cannot overwrite it.
2. **D2:** `own_names` must stop at nested `FunctionDef`, `AsyncFunctionDef`, `Lambda`, and `ClassDef` (recording only their names) and at comprehensions. It must exclude names declared `global` or `nonlocal` in that frame.
3. **D3:** add `With`/`AsyncWith` `optional_vars`, `ExceptHandler.name`, `MatchAs`/`MatchStar` names, `MatchMapping.rest`, and `Delete` targets to `own_names`. Alternatively, any frame binder the function cannot classify should make the name own-but-unknown, which yields unparsed rather than a module value.
4. Admit the four fixtures (plus Q07, Q08, Q11 from `discovery/` if wanted) as no-harm guards before re-measuring C1. The base passes 3 of the 4 exactly; `MatchCaptureBinderNotOwned` is a base gap that is honestly unparsed.

Whether to reject the tip or repair it is the L1's decision. All three defects are fixable inside the provenance design; none is an inherent tradeoff.

## Bounds and tooling

- Writes: only `w2/out/AttackFrameScopes/`, this report, and the scratch dir `/fast/scratch/hyaku/mado-r23/w2/AttackFrameScopes/`.
- Lane git: read-only `git show` only; no jj commands.
- Execution: no transcript code ran except through the recording fake-subprocess `CHILD`.
- Installs: none.

## Addendum: re-run against repair tip 3732c7a7 (2026-10-22)

Verdict: **0 REGRESSED.** All 11 earlier regressions are gone. On the 41 discovery probes: 13 improved, 18 same-correct, 10 same-wrong. On the 4 delivered fixtures: 3 same-correct, 1 same-wrong.

- Tool: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 3732c7a73244fab87558c704107418e5de01436c:tools/mado-tripwire.py`, written into the fresh empty dir `/fast/scratch/hyaku/mado-r23/w2/AttackFrameScopes-rerun-3732c7a7/`. sha256 `e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`. Base unchanged, `cd9da20c…`.
- Inputs: the same probe harness, truth runner, and round-21 scan helper as above. Fixture sha256 values are unchanged from `cases.json`. Receipts (`probes-result.json`, `probes2-result.json`, `fixtures-result.json`) are in that scratch dir.

How each earlier defect now behaves:
- **D1 (all calls of a function shared one frame):** fixed. P11, Q05, Q06, Q07, Q14, `FrameReusedBySecondInvocation` and `FrameReusedBothClosuresCalled` now match the base exactly.
- **D2 (`own_names` counted names bound in nested scopes):** fixed. P13, P15, Q08, Q09 and `NestedBinderFreezesLateGlobal` now match the base exactly.
- **D3 (`own_names` missed `match` and `with` binders):** no longer harmful, but not resolved. Q10, Q11 and `MatchCaptureBinderNotOwned` now report an honest unparsed count of 1 with no false row, the same as the base. They are same-wrong, not correct.

The 13 improved probes and the other same-wrong cases (class-body execution, default-argument capture, `global` declarations, method-frame conflation, recursion) are unchanged from the first run.
