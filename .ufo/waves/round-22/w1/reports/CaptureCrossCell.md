# CaptureCrossCell — cross-cell factory capture: rebind before later-cell invocation

Seat: `MadoR22.CaptureCrossCell` · Lane: leaf member, no subagent dispatch.
Wave: round-22 w1, pre-implementation truth freeze. Source-only authoring: no production edits, no detector measurements, no payload execution, no fixture runs. Proposal is independent of detector results; it specifies Python truth, not predicted scanner output.

## Variant

Single independent static-truth C1 variant (F1 cross-cell projection):

- **Cell 1:** `import subprocess`; `spec = ["pacman","-S","r22-crosscell-exact"]`; `factory(argv)` returns nested `run()` whose body calls `subprocess.run(argv)`; `worker = factory(spec)`.
- **Cell 2 (same persistent eval namespace):** `spec = ["pacman","-Q","r22-crosscell-decoy"]` then `worker()`.

Declared expectation: `expected_kind = "exact"`, exactly one finding — `host_mutation`, `pacman -S r22-crosscell-exact`, `observed` — and zero unparsed.

## Python 3.14 semantic argument

1. `factory(spec)` binds `argv` to the list object existing at the factory call. The parameter becomes a cell variable because `run` closes over it; the closure captures the cell/object, never the name `spec`.
2. Rebinding `spec` in cell 2 stores a new list in the module global. Rebinding cannot mutate the captured object; nothing else references or mutates it. The captured argv is frozen at creation regardless of which cell the rebind lands in, since rebind precedes invocation.
3. Namespace persistence across eval cells keeps `worker` and `subprocess` resolvable; `run.__globals__` is that namespace.
4. `worker()` invokes `subprocess.run(["pacman","-S","r22-crosscell-exact"])` once. `shlex.join` over the literal tokens yields `pacman -S r22-crosscell-exact`. Class per established convention (`pacman -S` → `host_mutation`), evidence `observed`: a fully determined literal argv executed unconditionally.

## Falsifiers (`forbid_observed_commands`)

- `pacman -Q r22-crosscell-decoy` — the invoke-time rebinding row: exactly the r21 F1 defect (factory formals re-evaluated in the invocation environment) projected across cells, since cell 2's `spec` is the invoke-time literal.
- `pacman -S r22-crosscell-decoy`, `pacman -Q r22-crosscell-exact` — token recombinations; any observed row built from them is fabricated argv, not Python behavior.

A detector that correctly snapshots creation-time bindings reports the single exact row; one that re-binds at invoke reports the decoy as `package_query` and drops the `host_mutation`; one that fails persistence emits nothing. Truth admits only the first.

## Scope notes and unknowns

- Variant deliberately exercises only: factory-from-variable creation, cross-cell binding persistence, caller-side rebind-before-invoke. No starred/keyword/partial/unbindable forms — those belong to sibling seats (CaptureStarUnknown, CaptureKwargs, CapturePartial*).
- Unknown retained: whether a correct implementation must carry the creation-time literal snapshot on the persisted cross-cell binding (SimplifyCapture's `ClosureFrame` design says yes); proposal is truth-only and takes no position.
- `xd://lsp` reported absent in r21; not needed here — truth derives from language semantics, not call-site lookup.

## Tools

None installed or updated. Pacman transactions paused host-wide; no package queries run or needed.

## Artifacts

- Proposal: `.ufo/waves/round-22/w1/proposals/CaptureCrossCell.json`
- This report: `.ufo/waves/round-22/w1/reports/CaptureCrossCell.md`
- Grounding: `.ufo/waves/round-21/residual/FinalBindingReview.md` (F1 mechanism; cross-cell reach note citing scan_file 2643–2644, 2685–2686)
