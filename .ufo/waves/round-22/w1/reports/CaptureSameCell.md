# CaptureSameCell — C1 independent truth proposal

Seat: `MadoR22.CaptureSameCell` · Lane: leaf member, no delegation.
Artifact: `.ufo/waves/round-22/w1/proposals/CaptureSameCell.json` (authored, not measured).

## Assigned variant

Factory gets a literal command variable; the caller rebinds that variable before invoking the stored closure. Single eval cell, same-cell scope.

```python
import subprocess


def make(argv):
    def run():
        subprocess.run(argv)
    return run


spec = ["pacman", "-Q", "r22-samecell-held"]
slot = make(spec)
spec = ["pacman", "-S", "r22-samecell-decoy"]
slot()
```

## Static truth (Python 3.14, reasoned — nothing executed)

- `make(spec)` binds `argv` to the list object `["pacman","-Q","r22-samecell-held"]` as it existed at factory-call time.
- `run` closes over `make`'s local cell for `argv`; it keeps referencing that same list object.
- `spec = ["pacman","-S","r22-samecell-decoy"]` rebinds the module name to a new list. It does not mutate the held object, so the closure is unaffected.
- `slot()` runs `subprocess.run(["pacman","-Q","r22-samecell-held"])`.

Expectation: `expected_kind: "exact"` — exactly one row, `package_query` `pacman -Q r22-samecell-held`, `observed`; zero unparsed. `forbid_observed_commands` names the decoy `pacman -S r22-samecell-decoy`, which is passed to no call and must never be an observed row.

## Independence and discrimination

- Same lifetime shape as r21 F1 (`capture-invoke-time.jsonl`) but independently authored: fresh r22 markers, renamed bindings, and reversed evidence-class direction (truth is `package_query`; the invoke-time misreading would fabricate `host_mutation`). The F1 fixture's truth was `host_mutation` against a `package_query` misreading.
- A detector binding the factory argument at closure-invocation time reports the decoy — caught by `forbid_observed_commands` and by the want row mismatch. A correct detector binds at creation time and emits the held row.
- Derived only from `FinalBindingReview.md` F1 (lines 70–77) and Python semantics. No detector source, detector output, fixture rerun, or measurement was consulted for the expectation.

## Compliance

- Payload uses `subprocess.run` with inert argv; only `pacman -Q`/`pacman -S` markers. Cells never executed.
- No production edits, no detector measurements, no package queries, no live probes, no background jobs. Git untouched.
- `shlex.join(["pacman","-Q","r22-samecell-held"])` = `pacman -Q r22-samecell-held`; tokens are single words, serialization exact.

## Unknowns / limits

- Cross-cell persistence is not exercised (single cell by assignment scope); F1's cross-cell reach remains source-only.
- Mutation-instead-of-rebinding (`spec[2] = ...`, `spec.append(...)`) is a different variant — here the name is rebound, so the held object is immutable from the caller's side.
- Unknowns: none beyond the above; the expectation is fully determined by Python semantics.

## Tools

None installed or updated. No installs needed.
