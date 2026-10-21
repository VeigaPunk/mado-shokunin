# CaptureReturnedAlias — nested def assigned to a returned alias name before return

Seat: `MadoR22.CaptureReturnedAlias` · Lane: leaf reviewer, no delegation. Round-22 wave 1: frozen static-truth proposal only; no production edits, no detector measurements, no payload execution. Ground truth for the defect class: `.ufo/waves/round-21/residual/FinalBindingReview.md` F3 (lines 85–88) and its returned-rebound fixture.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureReturnedAlias.json` — one independent C1 variant, `expected_kind: "exact"`.

## The variant (single eval cell, inert source)

```python
import subprocess


def make():
    def worker():
        subprocess.run(["pacman", "-S", "r22-alias"])

    def decoy():
        subprocess.run(["pacman", "-Q", "r22-alias-decoy"])

    run = worker
    return run


make()()
```

## Static truth (Python 3.14 semantics, nothing executed)

| Step | Semantic fact |
|---|---|
| `def worker` / `def decoy` | Two distinct function objects bound to factory-local names. |
| `run = worker` | Executed before `return`; binds local name `run` to the **same worker object**. This is a new binding to an existing object, not a rebinding of `worker` and not a new def. |
| `return run` | Evaluates `run` against the post-prefix local namespace → returns the **worker** object. `decoy` is unreachable through this call chain. |
| `make()()` | Invokes `worker()` → `subprocess.run(["pacman","-S","r22-alias"])` with a fully literal argv. |

Expected rows: exactly one — `{"class":"host_mutation","command":"pacman -S r22-alias","evidence":"observed"}` (argv serialized with `shlex.join`). Zero unparsed: every operand is a literal or a locally resolvable name; nothing is unknown.

`forbid_observed_commands`: `["pacman -Q r22-alias-decoy"]` — the decoy body is never invoked; any observed row for it is fabricated.

## How this variant differs from siblings and the r21 fixture

- r21 `returned-rebound` fixture and seat `CaptureReturnedRebound`: two defs, **same** def name rebound (`a = b`), returned name is itself a `def` target. Mine: the returned name `run` is **never** a def target — it exists only through `Assign`. Under the F3 mechanism (`local` map built from top-level `def`s only, `local[returned]` lookup at lines 1645–1652 per the review) `run` is absent entirely, so the defective detector's failure mode here is a **silent miss**, not a wrong-body row — a distinct edge of the same defect.
- `CaptureReturnedChain` (sibling): chained aliasing `x = y; return x`-style indirection over multiple assigns. Mine is the minimal single-alias atomic case; the chain seat extends it.
- Distinctness rationale: alias-before-return tests whether the resolver consults the **binding map** (Assign entries) rather than only the def index; rebind tests whether it re-reads a def name after Assign overwrite. A repair handling only one shape fails the other.

## Detector-independent expectation

`expected_kind: "exact"` is justified by construction: one literal argv, no unresolved names, no opaque calls. The proposal asserts Python semantics only and commits no claim about any detector result; it remains valid whether the eventual implementation passes, misses silently, or fabricates the decoy row.

## Checks performed

- `json.load` on the proposal: valid.
- `ast.parse` on the cell source: parses cleanly (parse-only; never executed, per resource contract).
- `shlex.join(["pacman","-S","r22-alias"])` → `pacman -S r22-alias`, matching the want row verbatim.

## Tools installed

None. Pacman untouched; no queries, transactions, services, or probes.

## Limits and unknowns

- Cross-cell reach (factory in cell *n*, alias resolution in cell *m*) is covered by sibling seats; this proposal keeps one cell for minimality.
- Whether the repaired detector treats alias-to-def through the binding map or via prefix replay is implementation detail; the frozen expectation holds under either.
- No measurement was run; `want` derives from the Python 3.14 language reference (assignment binds target to the evaluated object; `return` evaluates against the in-effect local namespace) cited in the proposal `source` field.
