# CaptureReturnedRebound — static-truth C1 variant

Seat: `MadoR22.CaptureReturnedRebound` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Round-22 wave 1, proposal freeze only: no production edits, no detector measurements, no payload execution.

## Deliverable

`/.ufo/waves/round-22/w1/proposals/CaptureReturnedRebound.json` — one single-cell `exact` variant under the assigned shape: **two nested defs, then the returned name rebound to the second before `return`**.

```python
import subprocess


def make():
    def first():
        subprocess.run(["pacman", "-Q", "r22-rebound-first"])

    def second():
        subprocess.run(["pacman", "-S", "r22-rebound-second"])

    first = second
    return first


make()()
```

## Frozen expectation

| Field | Value |
|---|---|
| `expected_kind` | `exact` |
| `want` | `host_mutation` · `pacman -S r22-rebound-second` · `observed` (one row) |
| `forbid_observed_commands` | `pacman -Q r22-rebound-first` |
| unparsed counters | zero |

Exact requires exact rows and zero unparsed; both hold by static reasoning below.

## Static truth (Python 3.14, nothing executed)

1. `def first` creates F1 and binds the factory-local name `first`; `def second` creates F2 and binds `second`.
2. The prefix `Assign` `first = second` runs in the factory body before `return`: RHS evaluates `second` → F2, then rebinds the local name `first` to F2. F1 becomes unreachable; nothing is copied or mutated.
3. `return first` evaluates `first` in the namespace in effect at the return statement → F2. `make()` returns F2; `make()()` calls F2's body.
4. F2 calls `subprocess.run(["pacman","-S","r22-rebound-second"])` — fully literal argv, unconditional, no starred/keyword/dynamic arguments. `shlex.join` → `pacman -S r22-rebound-second` → one `observed` `host_mutation` row.
5. F1's `pacman -Q r22-rebound-first` is dead through every reachable path; it may never be reported observed. A scanner that selects the returned callable from the def map rather than the post-prefix namespace emits exactly that wrong row — the r21 F3 defect — which `forbid_observed_commands` turns into a red.

## Defect exercised

F3 from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md` (lines 85–88): `callable_info` built `local` from top-level defs only and selected `local[returned]`, ignoring the later `Assign` rebinding inside the factory body; r21 probe `returned-rebound.jsonl` (sha256 `774e2946…`) reported `pacman -Q r21-a` where truth was `pacman -S r21-b`. This variant is the same semantic class, independently authored: different function names (`first`/`second`), different tokens (`r22-rebound-*`), rebind spelled `first = second` with the returned name itself rebound. Distinct from sibling `CaptureReturnedAlias` (introduces a third name `run = worker`, returns the new name); here the rebound name is the returned name, matching the assignment's wording exactly.

## Independence and bounds

- Specified before implementation; no changed code exists to read and none was read. No detector source, detector output, or measurement consulted. Cell never executed.
- Convention mapping mirrors sibling proposals: `pacman -S` → `host_mutation`, `pacman -Q` → `package_query`; inert argv only.
- Unknowns: none for this variant — every name is a literal or a locally bound function object; resolution is total.
- Tools installed: none. Git: read-only, untouched. Lane files written: only the proposal and this report.

## Citations

- `.ufo/waves/round-21/residual/FinalBindingReview.md` F3 (lines 85–88) and author-lane check 1 (line 158: "Resolve the returned name against post-prefix bindings").
- Python 3.14 language reference: FunctionDef binds the name in the containing scope; simple assignment rebinds the target; `return` evaluates the expression against the local namespace in effect at the return statement (vendored under `.ufo/waves/round-22/w1/sources/SourceClosure/`; upstream `github.com/python/cpython` tag v3.14.8 `Doc/reference/`).

Report: .ufo/waves/round-22/w1/reports/CaptureReturnedRebound.md
