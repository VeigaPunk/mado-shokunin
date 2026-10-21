# CapturePartialGlobal — static-truth C1 variant proposal

Seat: `MadoR22.CapturePartialGlobal` (leaf reviewer). Round-22 wave 1: independently authored truth fixture, frozen before implementation. No production edits, no detector measurements, no payload execution, no package queries, no installs.

## Deliverable

`.ufo/waves/round-22/w1/proposals/CapturePartialGlobal.json` — one eval cell, `expected_kind: "exact"` (retained; see Revision 1 for the paired opposite-direction guard `CapturePartialGlobalLateActual.json`).

## Variant

Returned `functools.partial` wraps a module-level helper whose argv global is late-bound (rebound between partial construction and invocation):

```python
import functools
import subprocess

def run_helper(cmd):
    subprocess.run(cmd)

def make_partial():
    return functools.partial(run_helper, ARGV)

ARGV = ["pacman", "-S", "r22-partial-global"]
bound = make_partial()
ARGV = ["pacman", "-Q", "r22-partial-global-late"]
bound()
```

## Static truth (Python 3.14 semantics; not executed)

- `functools.partial` copies fixed positional argument **objects** into `partial.args` at construction time. `make_partial()` evaluates `ARGV` against module globals at factory-call time, when `ARGV` is the `["pacman", "-S", "r22-partial-global"]` list.
- The subsequent `ARGV = [...]` is a rebinding of the module global to a new list object; it never mutates the object already stored in `partial.args`. (Unlike F1's closed-over parameter, a `partial` arg slot is an object reference, not a cell — the rebind is invisible either way.)
- `bound()` invokes `run_helper` with the construction-time list; `subprocess.run(cmd)` inside it spawns exactly `pacman -S r22-partial-global`.

**Expected rows:** exactly one — `host_mutation`, `pacman -S r22-partial-global`, `observed`. Zero unparsed required ⇒ `expected_kind: "exact"`.

**Forbidden observed row:** `pacman -Q r22-partial-global-late`. Reporting it as observed means the detector folded the partial's fixed argument in the *invocation* environment — the invoke-time-literal defect family. In that failure mode the real `host_mutation` row is also missing/wrong, matching the F1 signature.

## Defect mapping

F1 in `.ufo/waves/round-21/residual/FinalBindingReview.md`: "factory arguments are bound at invocation time," with the same-class note (line 75) that a returned `functools.partial` evaluates fixed arguments in the invocation env. This variant exercises that path through a distinct surface: fixed arg is a **module global name** (not a literal, not a factory parameter), wrapped helper is a **module-level `def`** (not a nested closure), and the global is **rebound between construction and invoke**. It is a sibling to `CapturePartialFixed`/`CapturePartialOverride`, which cover literal fixed args and invoke-time overrides.

## Axes considered

| Axis | Choice |
|---|---|
| Discrimination | Truth `-S` early vs defect `-Q` late: wrong class **and** wrong command if invoke-time folding persists |
| Scope | Single cell, single eval; no unrelated unsupported forms (no `*args`, no `**kwargs`, no conditional return) |
| Inertness | `pacman -S`/`-Q` with invented names; payload is scanner input only, never executed |
| Exactness | All names statically resolvable; argv fully literal at the one reachable spawn site |

## Alternatives kept off the frontier

- Helper reading `ARGV` as a global *inside* the body (`subprocess.run(ARGV)` with no partial arg): genuinely late-bound → resolves to the late value. Initially rejected as "zero discrimination" against the original-F1 reading; parent review corrected this — it is the required opposite-direction guard (see Revision 1 below).
- Rebinding `ARGV` before `make_partial()` is called: construction and invocation see the same value → no discrimination. Rejected.
- `expected_kind: "uncertain"`: no unparsed source exists — argv is fully determined. Rejected.

## Unknowns / limits

- Whether the future implementation resolves `ARGV` inside the factory via the invocation env, the factory-call snapshot, or literal-folds at `partial(...)` parse time is detector behavior — deliberately not inspected (changed code does not exist; no measurements permitted).
- Cross-cell persistence variant (factory in cell n, invoke in cell m) left to `CaptureCrossCell`-family seats; this proposal stays single-cell per "prefer one expected result."
- `pacman -S` as `host_mutation` classification follows the frozen convention evidenced by the r21 probe rows (`pacman -S r21-factory` → `host_mutation`).

## Tools

None installed or updated. Git untouched. Writes: this report plus `w1/proposals/CapturePartialGlobal.json` and `w1/proposals/CapturePartialGlobalLateActual.json`.

---

# Revision 1 — parent direction: retain original, add late-bound-body guard

Parent seat `MadoR22` reviewed the original proposal: valid, but it covers the eager-capture direction already represented by `CapturePartialFixed` and lacks the **opposite timing guard**. Per direction, `CapturePartialGlobal.json` is retained unchanged and a second proposal was authored:

## CapturePartialGlobalLateActual — late-bound module global read in the helper body

`.ufo/waves/round-22/w1/proposals/CapturePartialGlobalLateActual.json` — one eval cell, `expected_kind: "exact"`.

```python
import functools
import subprocess

def run_helper():
    subprocess.run(ARGV)

def make_partial():
    return functools.partial(run_helper)

ARGV = ["pacman", "-S", "r22-partial-global-early"]
bound = make_partial()
ARGV = ["pacman", "-Q", "r22-partial-global-late"]
bound()
```

## Static truth (Python 3.14 semantics; not executed)

- `ARGV` inside `run_helper` is a **module-global read resolved at call time** — not at `def` time, not at factory return, not at `functools.partial(run_helper)` construction. The partial carries no fixed arguments.
- `bound()` executes the body after `ARGV` was rebound to `["pacman", "-Q", "r22-partial-global-late"]`; the spawned argv is exactly `pacman -Q r22-partial-global-late`.

**Expected rows:** exactly one — `package_query`, `pacman -Q r22-partial-global-late`, `observed`; zero unparsed ⇒ `expected_kind: "exact"`.

**Forbidden observed row:** `pacman -S r22-partial-global-early`. Reporting it as observed means the repair froze module globals at factory-call/partial-construction time — an **over-frozen** F1 fix that fabricates a `host_mutation` and drops the real query.

## Why this pair is the complete guard

| Proposal | Binding site | Python truth | Defect caught |
|---|---|---|---|
| `CapturePartialGlobal` | `partial` fixed arg: object captured at **construction** | early `-S` | invoke-time folding (original F1) |
| `CapturePartialGlobalLateActual` | global read in **body**: resolved at **call** | late `-Q` | over-frozen globals (wrong-direction repair) |

A correct repair must freeze the first and leave the second late-bound; the pair discriminates both failure directions. The forbidden serialization differs in class (`host_mutation` vs `package_query`) and command token, so the guard is non-trivial.

## Unknowns / limits (revision)

- A third failure mode — `ARGV` unresolved at invocation producing a miss or lead instead of the observed `-Q` — is not named in `want`; `forbid_observed_commands` names only the fabricated-observed discriminator.
- All earlier limits stand: no detector inspected, no cells executed, no tools installed, Git untouched.
