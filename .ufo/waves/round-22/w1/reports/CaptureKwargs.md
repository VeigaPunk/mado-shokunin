# CaptureKwargs — factory literal `**` mapping argument rebound after construction

Seat: `MadoR22.CaptureKwargs` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Round-22 wave 1: proposal only — no production edits, no detector measurements, no payload execution.

## Proposal

Artifact: `.ufo/waves/round-22/w1/proposals/CaptureKwargs.json` (valid JSON; single eval cell compiles as Python).

```python
import subprocess
def make(**kw):
    def run():
        subprocess.run(kw["argv"])
    return run
spec = {"argv": ["pacman", "-S", "r22-kwargs-a"]}
runner = make(**spec)
spec = {"argv": ["pacman", "-Q", "r22-kwargs-b"]}
runner()
```

## Declared truth

`expected_kind`: **exact** — one row, zero required unparsed:

| field | value |
|---|---|
| class | `host_mutation` |
| command | `pacman -S r22-kwargs-a` (`shlex.join(["pacman","-S","r22-kwargs-a"])`) |
| evidence | `observed` |

`forbid_observed_commands`: `["pacman -Q r22-kwargs-b"]` — the rebound mapping's argv must never surface as an observed row. (A `lead` row naming it is not forbidden; only observed fabrication is.)

## Semantic argument

1. `make(**spec)` runs while `spec` names the first dict literal. Per the 3.14.8 reference, a `**identifier` parameter "is initialized to a **new** ordered mapping receiving any excess keyword arguments" — the closure cell `kw` captures `{"argv": ["pacman","-S","r22-kwargs-a"]}` at factory-call time.
2. `spec = {"argv": [...-b]}` rebinds the *name*; the closed-over mapping is a different object and is unaffected. This is the F1 lifetime axis transported onto the `**` binding path: factory arguments are fixed at construction, not re-evaluated at invocation.
3. `runner()` → `subprocess.run(["pacman","-S","r22-kwargs-a"])` — one inert `pacman -S` host-mutation argv, fully literal.
4. The `**` expansion is a name bound to a dict literal, so the call is statically bindable; Python semantics requires neither a lead nor an unparsed row. A detector that reports `pacman -Q r22-kwargs-b` as observed exhibits the F1 defect on `**kwargs`; one that fabricates nothing or claims uncertainty exhibits an F2-class handling gap on a bindable `**` argument.

## Axes

- **Correctness:** exact observed row from the construction-time mapping; rebound `-b` mapping forbidden as observed.
- **Independence:** truth derived from the language reference plus r21 FBR F1, not from detector output; no detector code read or run.
- **Parsimony:** one cell, one closure, one observed row; no unrelated unsupported forms (no star-args, no missing params, no unknown keywords).

## Sources

- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst` lines 1331–1334 (`**identifier` → new ordered mapping per call), sha256 `35e6dfbf2794d367774253655d95b6d5ef91ba63084685624144f2b3945e3e2f`, fetched per `.ufo/waves/round-22/w1/sources/SourceClosure/receipts.jsonl` (python/cpython tag v3.14.8, peeled commit `8e6e75d9…`).
- `.ufo/waves/round-21/residual/FinalBindingReview.md` F1 (factory arguments bound at invocation, not factory-call, time) and F2 trigger list (non-literal `**` mapping) — used only to position the variant on the supported-forms frontier; no detector bytes read.

## Checks performed (authoring-time only)

- Proposal file parses as JSON; cell compiles under `compile(..., 'exec')` — not executed.
- `shlex.join(["pacman","-S","r22-kwargs-a"])` → `pacman -S r22-kwargs-a` (no quoting characters present).

## Unknowns / limits

- Whether the candidate scanner folds `**name` dict literals through `bind_literal` is intentionally unexamined — that is the detector's problem; this proposal only declares Python truth.
- Cross-cell persistence is out of scope; the variant is single-cell like the r21 inert fixtures.

## Tools

None installed or updated. No package queries, service probes, or payload executions.
