# CaptureMissingRequired — scoped findings

Seat: `MadoR22.CaptureMissingRequired` · Lane: leaf member, no delegation · Wave: round-22 attempt 1, C1 bounded operability truth freeze.

## Scope performed

Authored ONE independent static-truth C1 variant: **missing required factory parameter**. Wrote the frozen proposal to `.ufo/waves/round-22/w1/proposals/CaptureMissingRequired.json`. No production edits, no detector measurements, no payload execution, no package queries. All input files read were data.

## The variant

One eval cell (Python 3.14.8 semantics, inert):

```python
import subprocess


def make(argv):
    def run():
        subprocess.run(argv)
    return run


argv = ["pacman", "-S", "r22-missing-required"]
runner = make()
runner()
```

Factory `make` requires one positional `argv`. The transcript calls `make()` with zero arguments while a module-global `argv` names an inert pacman marker.

## Static truth (source-derived, not measured)

- `runner = make()` supplies no positional, keyword, or default value for required parameter `argv`. Argument binding therefore raises `TypeError` **before the body of `make` executes** (compound_stmts.rst: a call "always assigns values to all parameters ... from positional arguments, from keyword arguments, or from default values"; none exists here).
- No `except` clause is present, so the exception propagates: `runner` is never bound and `runner()` is unreachable.
- Even if `run` were formed, its `argv` is a free variable bound to `make`'s parameter cell (executionmodel.rst name resolution) — a cell that never received a value — and could not resolve to the module global.
- `subprocess.run` exists only inside `run`'s never-entered body → the transcript provably spawns **no process**.

## Expectation decided

- `expected_kind: "exact"`, `want: []` — **no-findings with a source reason**.
- `forbid_observed_commands: ["pacman -S r22-missing-required"]` — the unreachable body must not borrow the same-named module global into an observed row (the F2 fabrication family).

### Why exact (no-findings), not uncertain

Siblings `CaptureStarUnknown`/`CaptureKwUnknown` own the genuine-uncertainty axis (`make(*parts)` / `make(**kw)` — outcome unknowable). This seat's call `make()` has a **decidable** arity failure visible in source: provable `TypeError`, provable unreachability, provably zero spawns.

- An **observed** row is the F2 fabrication — wrong.
- A **lead** row is wrong: it asserts a possible spawn on a body that is provably unreachable, not unresolved-but-reachable.
- An **unparsed** marker is wrong: the file parses cleanly and the failure is decidable, not "cannot be determined."
- `uncertain` would mask a determinate TypeError and, under its required lead-or-unparsed condition, could brand the most precise repair (zero rows, zero unparsed) a regression.

The only sound frozen expectation is exact-zero.

## Risk noted (recorded, not waived)

`exact`/`want:[]`/`zero unparsed` is the strictest admissible claim: a repaired scanner that emits a conservative `unparsed` or `lead` for the unbindable `make()` call will fail this expectation despite not fabricating an observed row. Accepted deliberately — the semantics justify "no findings," and `uncertain` would weaken the F2 boundary. This is a documented edge between "honest-conservative" and "precise" repair shapes, flagged for the wave integrator; it is not a defect in the proposal's static truth.

## Sources (data read)

- `w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst` (fetched v3.14.8; function-definition + call-parameter assignment semantics).
- `w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst` (fetched v3.14.8; free-variable name resolution).
- `.ufo/waves/round-21/residual/FinalBindingReview.md` — F2 defect provenance (missing-required-parameter is one of the `bind_literal` failure triggers, tool lines 2027–2028).

## Tooling / contract ledger

- Tools installed/updated: **none** (none needed). No pacman transactions; host-wide pause honored.
- No subprocess jobs spawned; no cells executed; payloads are inert transcript data only.
- Git/filesystem: read-only reads plus the two authored artifacts above (proposal + this report). No sibling/lane/host state mutated.

Report: `.ufo/waves/round-22/w1/reports/CaptureMissingRequired.md`
