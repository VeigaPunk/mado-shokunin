# CaptureKwUnknown — C1 independent truth proposal

Seat: `MadoR22.CaptureKwUnknown` · Lane: leaf member, no delegation.
Artifact: `.ufo/waves/round-22/w1/proposals/CaptureKwUnknown.json` (authored, not measured).

## Assigned variant

F2 projection over the non-literal `**` mapping trigger: the factory call unpacks a name bound nowhere, and a same-named module global `argv` literal sits one scope away as bait. Single eval cell.

```python
import subprocess


def make(argv):
    def run():
        subprocess.run(argv)
    return run


argv = ["pacman", "-Q", "r22-kwunknown-global"]
runner = make(**unknown_map)
runner()
```

## Static truth (Python 3.14, reasoned — nothing executed)

- `make(**unknown_map)` evaluates `unknown_map`, bound nowhere in the transcript → `NameError` before parameter binding; `runner` is never bound and `runner()` never runs.
- Even if `unknown_map` existed, a `**` unpack takes keys from the mapping's runtime contents — statically unknowable for a non-literal mapping — so `argv` binds to no determined value.
- `run` references `argv`, making `make`'s parameter a closure cell variable; `run`'s load resolves through that cell and never consults module globals. The module `argv = ["pacman","-Q","r22-kwunknown-global"]` cannot supply the cell.
- No statically determined observed row exists. Sound outputs: zero findings + nonzero unparsed, or leads only. An observed `pacman -Q r22-kwunknown-global` is exactly r21 F2's fabricated row.

Expectation: `expected_kind: "uncertain"`, `want: []` (no required observed row; schema carries no unparsed field, so the explicit-unparsed honest outcome is declared in `rationale`). `forbid_observed_commands` names the borrowed-global bait `pacman -Q r22-kwunknown-global` and the class-flipped recombination `pacman -S r22-kwunknown-global`.

**Pre-seal addendum (parent directive, MadoR22):** `CaptureKwUnknown.addendum.json` strengthens the seal — `forbid_commands_any_tier` forbids both `pacman -Q r22-kwunknown-global` and `pacman -S r22-kwunknown-global` at ANY evidence tier; a lead carrying the borrowed global still invents a binding Python cannot produce, so it is forbidden, not merely downgraded. `require_signal: true` requires the unresolvable `**` unpack to leave a trace: at least one lead row or a nonzero unparsed counter; silent zero-row clean scan is an unsound miss. Exact error signal may be lead or unparsed; no invented argv. Original `CaptureKwUnknown.json` retained unchanged per directive. OracleHarness notified.

**Addendum consequence for the lead outcome:** "leads only" (line 30) narrows — leads may exist but must not name the global's argv; a lead row for `subprocess.run(argv)` must carry no resolved `r22-kwunknown-global` command. The unparsed outcome (a) is unchanged.

## Independence and discrimination

- Same defect class as r21 F2 (`capture-unbound-global.jsonl`) but independently authored: fresh r22 marker, a different trigger surface — non-literal `**` mapping (bind_literal 1998–2000) instead of a starred non-literal (`*parts`, 1972–1976) — so the fix cannot key on star-args alone.
- A detector that leaves the invocation env unchanged on bind failure reports the module global as observed (F2 mechanism, spawn_scan 2335). One that sweeps with `LITERAL_MISS` params emits leads only; one that counts the `**` unpack unparsed emits nothing. Both are honest; only observed is wrong.
- Derived solely from `FinalBindingReview.md` F2 (lines 78–83, plus contract/remedy quotes) and Python semantics. No detector source re-read, no measurement, no fixture execution.

## Compliance

- Payload uses `subprocess.run` with inert argv; only `pacman -Q`/`pacman -S` markers. Cell never executed; transcript is inert ast-scanner input.
- No production edits, no detector measurements, no package queries, no live probes, no background subprocess jobs. Git untouched (read-only). No pacman transactions (paused host-wide).
- `shlex.join(["pacman","-Q","r22-kwunknown-global"])` = `pacman -Q r22-kwunknown-global`; single-word tokens, serialization exact. Same for the `-S` recombination.

## Unknowns / limits

- Whether a correct repair emits a lead row for `subprocess.run(argv)` with no resolved argv, or instead counts the `**` unpack as unparsed with zero rows — the schema cannot express "row with unknown command," so `want` is empty and both outcomes pass via `expected_kind: "uncertain"`. This is the proposal's residual ambiguity, declared rather than smoothed over.
- `unknown_map` unbound makes `NameError` (not `TypeError`) the literal runtime result; the scanner models neither exception, so this stays a static-binding question, matching the r21 fixture's use of unbound `*parts`.
- Sibling seats own the other F2 triggers: `CaptureStarUnknown` (starred non-literal), `CaptureMissingRequired` (missing required param), `CaptureKwargs` (literal `**` mapping). This variant isolates the unknown `**` mapping only.
- `xd://lsp` was absent in r21; truth here derives from language semantics, not call-site lookup.

## Tools

None installed or updated. No installs needed.
