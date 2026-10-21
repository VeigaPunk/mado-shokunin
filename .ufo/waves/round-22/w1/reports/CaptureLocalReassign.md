# CaptureLocalReassign — C1 static-truth variant proposal (seat report)

Seat: `MadoR22.CaptureLocalReassign` · Lane: leaf member, reviewer · Wave: round-22 attempt 1, C1 bounded operability. Author-lane artifact only; not admission, not a measurement.

## Deliverable

- Proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureLocalReassign.json`
- Proposal sha256: `744cadda3aa69ee9eed2532f2d448cb9f5834fda72a57ca5bb19b4ae1b360032`
- Single eval cell, source sha256: `ae4e68804f4a7e4c5f35e6b3242176056299d7e437091be6b2fb79ef133296a9`
- `expected_kind`: `exact`

## Variant specified

Factory parameter rebound inside the factory before `return` of the nested function:

```python
import subprocess
def make(cmd):
    def run():
        subprocess.run(cmd)
    cmd = ["pacman", "-S", "r22-local-rebound"]
    return run
runner = make(["pacman", "-Q", "r22-local-initial"])
runner()
```

## Static truth (independently reasoned, not executed)

- `cmd` is bound to `["pacman","-Q","r22-local-initial"]` when `make` is called (invocation-time binding).
- Because `run` references `cmd`, it is a cell variable of `make`; `run`'s free variable dereferences that cell at call time.
- The `Assign` inside `make`'s body rebinds the cell to `["pacman","-S","r22-local-rebound"]` before `return run`.
- `runner()` therefore executes `subprocess.run(["pacman","-S","r22-local-rebound"])` — `shlex.join` → `pacman -S r22-local-rebound`, class `host_mutation`, evidence `observed`.
- Exactly one finding; zero unparsed. Every statement is statically resolvable: import, def, literal Assign, return, plain calls with literal values. No starred/`**`/unknown-keyword/missing-parameter triggers.
- `pacman -Q r22-local-initial` is never passed to `subprocess.run`; it is listed in `forbid_observed_commands` as the exact trap this variant discriminates.

## Discrimination vs round-21 defects

Per `round-21/residual/FinalBindingReview.md`: F1 (arguments bound at invocation time, not factory-call time — line 2334 evaluates `capture_call` args in the invocation-statement `cenv`), F3 (returned identity resolved from `def` only; prefix replay at 2338–2343 updates `captured_bindings` after node choice). This variant requires the correct conjunction: parameter bound at the call, **then** the cell updated by replaying the in-body prefix before the returned closure is scanned. A detector that snapshots the parameter binding without applying the in-body rebinding reports the stale `-Q` argv as observed; one that replays the prefix reports `-S` observed.

## Distinctness

- Not `returned`-name rebinding (sibling atom `CaptureReturnedRebound`/Chain; r21 fixture `returned-rebound`): the returned name is never rebound here — the **parameter** is.
- Not caller-side post-creation rebinding (r21 `capture-invoke-time` F1 class): the rebind is inside the factory body, before return, on the parameter name itself.
- Payload side effects: `pacman -S`/`-Q` markers only, inert argv, subprocess.run inert under the wave contract (parsed, never executed — and the cell was never run by this seat).

## Source citation

Python 3.14.8 Language Reference, `executionmodel`: "Name resolution of free variables occurs at runtime, not at compile time", canonical example `i = 10; def f(): print(i); i = 42; f()` prints 42 (lines 322–329); lines 89–93 establish local-binding/free-variable rules. Fetched copy: `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst`, sha256 `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`, fetched by sibling seat SourceDraft from `raw.githubusercontent.com/python/cpython` tag `v3.14.8` (peeled `8e6e75d9102e39bed2a2b279203a396741180f12`, receipt in `receipts.jsonl`). Plus `round-21/residual/FinalBindingReview.md` F1/F3 mechanism lines cited above.

## Independence / wave-contract compliance

- No production edits, no detector measurements, no cell execution, no package queries, no probes. All Git/docs access read-only.
- Read only: `round-22/registration.md`, `round-22/audit-contract.json`, `round-21/residual/FinalBindingReview.md`, two r21 fixture files (format pinning), sibling-fetched docs + receipts.
- Expectation derived from language semantics + prior review text, not from any detector output or sibling proposal content.

## Unknowns / limits

- Scanner row shape (`class`, `command`, `evidence` fields) follows the schema given in the assignment; exact field names beyond these three are the harness's concern, not this artifact's.
- Whether the detector treats `pacman -S` as `host_mutation` is asserted from r21's own table (`pacman -S r21-b` → `host_mutation`); no new measurement made.
- Two-statement call site (`runner = make(...)` then `runner()`) exercises module-level `Name` resolution for `runner`; if the detector only follows inline `make(...)()` invocation forms, this could yield zero rows rather than a wrong row — a coverage note for harness authors, not an ambiguity in truth.

## Tools installed/updated

None. (ALL pacman transactions paused host-wide; directive acknowledged, nothing needed.)
