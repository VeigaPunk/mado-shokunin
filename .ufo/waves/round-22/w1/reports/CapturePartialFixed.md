# CapturePartialFixed — factory returns functools.partial with fixed literal argv; caller rebinding cannot reach it

Seat: `MadoR22.CapturePartialFixed` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: round-22 w1, pre-implementation truth freeze. Source-only static semantics; no production edits, no detector measurements, no payload execution.

## Deliverable

`/.ufo/waves/round-22/w1/proposals/CapturePartialFixed.json` — one eval cell, `expected_kind: "exact"`, one expected row:

| class | command | evidence |
|---|---|---|
| `host_mutation` | `pacman -S r22-partialfixed-held` | `observed` |

`forbid_observed_commands`: `pacman -Q r22-partialfixed-decoy`, `pacman -S r22-partialfixed-decoy`.

## Variant (one cell)

```python
import functools
import subprocess


def factory(cmd):
    return functools.partial(subprocess.run, cmd)


argv = ["pacman", "-S", "r22-partialfixed-held"]
runner = factory(argv)
argv = ["pacman", "-Q", "r22-partialfixed-decoy"]
runner()
```

## Static-truth argument (Python 3.14 semantics; nothing executed)

1. `functools.partial(subprocess.run, cmd)` evaluates and stores its fixed arguments at construction. The returned object holds `cmd` in its stored `args`.
2. `factory(argv)` binds the parameter `cmd` to the list object `argv` referenced **at factory-call time** — `["pacman", "-S", "r22-partialfixed-held"]`.
3. `argv = ["pacman", "-Q", "r22-partialfixed-decoy"]` rebinds the module-level name to a fresh list. Name rebinding never mutates the previously bound object, so the partial's stored argv is unaffected.
4. `runner()` invokes `subprocess.run(["pacman", "-S", "r22-partialfixed-held"])` — exactly one observed `host_mutation` row, zero unparsed (all tokens literal, all names statically resolvable).

## Defect class exercised

F1 invoke-time binding, extended to `functools.partial` fixed arguments — explicitly flagged same-class in FinalBindingReview.md line 75: "a returned `functools.partial` evaluates its fixed arguments in the invocation env (1635–1638, 2384–2388)". A detector carrying that defect has two stacked routes to the same wrong row here:

- the capture path re-binds `cmd` from `Name(argv)` in the **invocation** `cenv`, seeing the rebound decoy;
- the partial path re-folds the fixed argument against the invoke environment.

Either fabricates observed `pacman -Q r22-partialfixed-decoy` and misses the true `host_mutation`. `expected_kind: exact` is satisfied: the correct detector emits exactly the one `want` row; any observed decoy spelling is forbidden.

## Independence and inertness

- Specified from Python semantics and the r21 review citation only; no detector output or changed code was consulted (none exists). Class mapping follows the r21 probe convention (`pacman -S` → `host_mutation`, `pacman -Q` → `package_query`).
- The cell is a scanner input transcript only: `subprocess.run` argv contains inert pacman markers; the wave never executes cells. No package query or transaction is performed.
- Single cell; `reset` is not exercised (cross-cell persistence is sibling `CaptureCrossCell`'s variant; keyword/global/partial-override shapes are sibling seats' variants).

## Unknowns

- Whether the repaired detector treats partial fixed args through the capture path, the partial path, or both — the expectation is identical under each, so no ambiguity in verdict.
- Mutation-vs-rebinding (e.g., `argv[2] = ...`) is a different, unclaimed shape; out of scope per "prefer one expected result".

## Tools

None installed or updated. No pacman transactions, no service or compositor interaction, Git untouched.

## Artifacts

- Proposal: `.ufo/waves/round-22/w1/proposals/CapturePartialFixed.json`
- This report: `.ufo/waves/round-22/w1/reports/CapturePartialFixed.md`
