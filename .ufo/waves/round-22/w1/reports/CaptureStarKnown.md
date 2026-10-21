# CaptureStarKnown — C1 truth proposal: starred literal-tuple factory argument, caller variable rebound

Seat: `MadoR22.CaptureStarKnown` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: round-22 w1, freeze-before-implementation. Source-only static truth; **no production edits, no detector measurements, no payload execution**.

Artifact: `.ufo/waves/round-22/w1/proposals/CaptureStarKnown.json`

## Assigned variant

ONE static-truth C1 variant: factory `*` literal tuple argument, caller variable rebound. Read prior `FinalBindingReview.md` (F1–F5 plus the six immutable fixtures) as the only prior-art input; no changed code exists to read, nothing was measured.

## The cell (single eval cell)

```python
import subprocess
def make(*argv):
    def run():
        subprocess.run(argv)
    return run
t = ("pacman", "-S", "r22-starknown")
runner = make(*t)
t = ("pacman", "-Q", "r22-starknown-rebound")
runner()
```

- `subprocess.run` receives an inert argv tuple (pacman `-S` marker); the cell is ast-scanner input and is never executed.
- `expected_kind`: `exact` — one want row, `host_mutation` / `pacman -S r22-starknown` / `observed`, zero unparsed.
- `forbid_observed_commands`: `pacman -Q r22-starknown-rebound` — the invoke-time-misbinding serialization.

## Static Python 3.14 truth (rationale, unmeasured)

1. `make(*t)` evaluates `t` **at the factory call statement** and splices the tuple's elements as positional arguments (language ref 6.3.4). With `def make(*argv)`, argv becomes the fixed tuple `("pacman","-S","r22-starknown")`. The varargs form is required: `def make(argv)` arity-1 under `make(*t)` raises `TypeError` (3 positional args), which would make the starred-argv variant vacuous. `subprocess.run` accepts the resulting tuple as its args parameter.
2. `run` closes over `make`'s parameter cell — the object, not the caller's name `t`.
3. `t = (...rebound)` is a later **rebinding** of the module-level name to a new tuple; it cannot mutate the closed-over cell. Caller-variable rebinding is semantically inert for the closure.
4. `runner()` therefore runs `subprocess.run(("pacman","-S","r22-starknown"))`; `shlex.join` serialization = `pacman -S r22-starknown` → `host_mutation`, `observed` (same classification as r21 truths `r21-factory`, `r21-b`, `r21-thread-run`).
5. The starred `t` is bound to a literal tuple at **every** program point, so the argument is statically known — this exercises F1's bindable path, not F2's starred-non-literal bind-failure path. Under r22 C1's declared contract, a *known* capture argument must yield the exact observed row; lead/unparsed here is itself a defect.

## Why this discriminates (defect map)

| Defect | This variant's signal |
|---|---|
| F1 (factory args re-bound in invocation-env, `spawn_scan` 2334) | Affected detector re-resolves `t` after the rebound → observed `pacman -Q r22-starknown-rebound` → forbidden, want mismatched |
| F2 (bind-fail leaks module globals to observed) | Not triggered: argument is statically known; any lead/unparsed outcome violates `exact` and C1's known-form clause |
| Silent miss (F4-class) | Zero rows also fails the exact want |

Distinct from `capture-invoke-time` (starred + varargs adds the *splice* surface to lifetime discrimination) and `capture-unbound-global` (known vs unknown starred argument; sibling `CaptureStarUnknown` owns the uncertain counterpart).

## Contract compliance

- One cell, one expected result, no unrelated/unsupported forms; inert `pacman -S`/`-Q` markers only.
- No cells executed; no detector output consulted; proposal stands on Python semantics alone.
- No production edits, no installs, no package queries, no probes; Git untouched.
- Unknowns: none material — the starred argument is statically known by construction; cross-cell binding persistence is explicitly out of scope for this variant (single cell keeps env state trivial).

## Tools

None installed or updated.
