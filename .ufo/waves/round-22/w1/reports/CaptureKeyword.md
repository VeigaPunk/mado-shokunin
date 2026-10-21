# CaptureKeyword — C1 truth proposal: factory keyword argument, variable rebound after creation

Seat: `MadoR22.CaptureKeyword` (reviewer, leaf). Wave: mado-r22-w1 authorized recovery. Artifact authored: `.ufo/waves/round-22/w1/proposals/CaptureKeyword.json`. No production edits, no detector measurements, no payload execution — source text treated as data only.

## Variant

Independent finite variant of r21 FinalBindingReview **F1** ("factory arguments are bound at invocation time, not at factory-call time"), isolating the **keyword-argument** spine of the defect with a caller-side variable rebound between factory call and invocation.

Cell source (single eval cell, inert; NEVER run):

```python
import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
cmd = ["pacman", "-S", "r22-kw-factory"]
runner = make(argv=cmd)
cmd = ["pacman", "-Q", "r22-kw-invoke"]
runner()
```

## Frozen truth (static reasoning, not measured)

- `make(argv=cmd)` binds make's local `argv` to the creation-time list `["pacman","-S","r22-kw-factory"]` — keyword-argument assignment happens **at the call** (compound_stmts: a call "assigns values to all parameters … from keyword arguments").
- `run` uses but never binds `argv`; it resolves via the **nearest enclosing scope** (executionmodel) — make's frame cell — not the module name `cmd`.
- The later `cmd = [...]` assignment rebinds only the module-level name `cmd` (simple_stmts: assignment "(re)binds names"); the closed-over cell is untouched.
- `runner()` ⇒ `subprocess.run(["pacman","-S","r22-kw-factory"])` ⇒ exactly **one observed `host_mutation`: `pacman -S r22-kw-factory`**; zero leads from this source; argv fully literal ⇒ `expected_kind: "exact"`.

The invoke-time-rebind sibling value `pacman -Q r22-kw-invoke` must not appear as observed; it is pinned in `forbid_observed_commands` as the anti-F1 check. A detector honoring Python's creation-time binding produces the `want` row; one reproducing F1 emits the forbidden row (possibly *also* missing the `-S` host_mutation).

## Schema conformance self-check

- `id` matches seat; `cells` is a single Python source string per eval-cell convention (r21 fixture shape: one JSONL `eval` toolCall per file — one cell ⇒ one file).
- `want` rows carry `class`/`command`/`evidence`; `command` is the `shlex.join` serialization of the literal argv tokens (`pacman -S r22-kw-factory` — no quoting needed; verified token-for-token against the cell).
- `expected_kind` `"exact"`: exact observed rows required, zero unparsed — consistent because the argv is a literal list at creation, the closure binds cleanly, and `runner()` takes no arguments.
- `forbid_observed_commands` lists the semantically wrong invoke-time row only; no invented argv.
- Payload contains only the inert `pacman -S`/`pacman -Q` marker lists inside `subprocess.run`; no package query, network, service, or mutation action. Independent of any detector result — derived from the language reference alone.

## Independence from sibling seats

Keyword-argument + caller-variable-rebound differs from: `capture-invoke-time` (r21, positional `make(cmd)`), `CaptureKwUnknown`/`CaptureMissingRequired` (bind-failure/leak F2 family), `CaptureStar*` (starred args), `CaptureKwargs` (`**` mapping), `CapturePartial*` (`functools.partial`), `CaptureReturned*` (F3 identity), `CaptureTwoInstances` (two closures), `CaptureCrossCell`/`SameCell`/`GlobalLate`/`LocalReassign`/`NestedFactory`/`Default`/`LocalShadow` (orthogonal axes). Closest sibling `CaptureGlobalLate` concerns late-bound globals; this seat's rebind is an ordinary module assignment of a literal — kept distinct by the keyword-argument binding path under test.

## Unknowns / limits

- Whether the repaired detector treats keyword-bound factory arguments through the same creation-time frame as positional ones — unknown by design (proposals precede implementation).
- If a future harness treats `forbid_observed_commands` as uncertainty-only, it is redundant but harmless under the exact-row requirement.
- LSP unavailable (`xd://lsp` absent); no semantic callers checked — not needed for a self-contained truth proposal.

## Tools

None installed or updated; pacman transactions paused host-wide; no installs needed.
