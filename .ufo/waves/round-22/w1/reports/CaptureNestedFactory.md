# CaptureNestedFactory — C1 truth proposal report

Seat: `MadoR22.CaptureNestedFactory` · role: revenger · wave: mado-r22-w1 · base `741122d177ae8ff68a73768777f20484d5bdcbe4`
Deliverable: `.ufo/waves/round-22/w1/proposals/CaptureNestedFactory.json`. No measurement, no probe, no production edit, no fixture execution, no tool install (wave contract).

## Axes (godspeed)

1. Capture fidelity at nesting depth 2 (level-1 factory argument reaching the depth-2 leaf through chained factory calls).
2. Overlay independence (level-2 parameter binding must not clobber or shadow the level-1 closure cell).
3. Within declared bounded literal-source forms (eligibility of the proposal itself).

## Reconstructed contract

A factory call whose func is itself a call (`outer(a)(b)()`) must, per Python 3.14 semantics, resolve the leaf closure's free variables through the chained closure cells created at each enclosing factory call. The declared contract (r21 `FinalBindingReview.md`, quoting the tripwire docstring 38–41) requires a followed def to run "with those values bound"; `sweep_body` (2179–2186) requires unknown parameters to degrade to `lead`, never borrowed module globals (F2). No contract text declares a nesting-depth cap; the capture branch exists precisely for call-as-func, and `Name` returns at every level are the examined form.

## Frozen truth (what the proposal locks)

Single eval cell, all literals, `def`-defined factories, plain `Name` returns, no rebinds, no keywords:

```python
import subprocess


def outer(host):
    def middle(pkg):
        def leaf():
            subprocess.run(["pacman", "-S", host, pkg])
        return leaf
    return middle


outer("r22-nest-outer")("r22-nest-inner")()
```

Expected: exactly one row — `host_mutation`, `pacman -S r22-nest-outer r22-nest-inner`, `observed` (`expected_kind` `exact`, `forbid_observed_commands` `[]`, zero unparsed implied). Class verified against the r21 probe table (`pacman -S …` → host_mutation; serialization = shlex.join of literal tokens). No name is rebound anywhere, so create-time and invoke-time resolution coincide; the discriminating content is purely the two-level chained capture: if the scanner drops or mis-scopes the level-1 overlay when following the level-2 factory, `host` has no same-named module global to leak, and the output becomes uncertain/lead/empty — an exact-row mismatch either way.

## Evidence chain

- `.ufo/waves/round-21/residual/FinalBindingReview.md` F1 (parameters bind at factory-call time), F2 (unbindable args → lead/unparsed, never globals), frozen CalledClosure input `outer(["pacman","-Q","w2shape"])()` as the depth-1 chained-call precedent (parsed, `eval_unparsed` 0).
- r21 probe fixtures (`.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/*.jsonl`) for the inert eval-cell JSONL shape and command serialization.
- Python 3.14 language reference, execution model / naming and binding: parameters bind to argument objects at call time; free variables resolve through enclosing-function closure cells before globals.

## Honestly rejected shapes (not in the proposal)

| Shape | Disposition | Reason |
|---|---|---|
| Non-`Name` factory returns (`return a if c else b`) | unsupported — rejected | r21 review lists this under "Not examined"; not a declared supported form. Not guessed. |
| Caller-side late rebind before invoking at depth 2 | rejected for scope | Owned by CaptureSameCell (single level) and CaptureCrossCell (cross-cell); compounding axes blurs seat ownership and duplicates the F1 timing counterexample. |
| Factory-internal parameter rebind before return | rejected for scope | Owned by CaptureLocalReassign. |
| Keyword / starred / `**` / missing-required factory arguments | rejected for scope | Owned by CaptureKeyword, CaptureKwargs, CaptureStarKnown/Unknown, CaptureMissingRequired; F2's unbindable branch is separately covered. This proposal stays all-bindable literal. |
| Depth ≥ 3 | unsupported — rejected | No contract text beyond the depth-limited follow; a finite supported form cannot be argued for arbitrary depth. |
| `partial()` fixed-argument factories | out of scope | Owned by CapturePartialFixed/Override/Global. |
| Thread/Timer scheduled bodies, reserved-key hygiene | out of scope | Owned by ThreadRun/TimerRun/ThreadRunAlias/ThreadHygiene. |
| Default-argument capture (`def middle(pkg=…)`) | unsupported — rejected | Def-time evaluation is a different mechanism, not a named C1 form. |

## Unknowns (exact)

1. Whether the C1 repair declares chained two-level factory calls as supported: argued from the declared contract (no stated depth cap, call-as-func capture branch, examined `Name` returns), never measured — r21 probes reached depth 1 only. If the delivered fix supports depth 1 only, this proposal must be excluded as out-of-contract rather than satisfied by weakening the expectation.
2. `w1/sources/SourceClosure/executionmodel.rst` (listed in the wave tree earlier) was not present at read time; the citation names the Python 3.14 language reference directly instead of quoting the local snapshot.
3. Scanner recursion/depth internals are unknown by contract (no detector source or measurement read this wave).

## Tooling

None installed or updated (nothing needed; all pacman transactions paused host-wide).

## Typo correction (pre-seal, 2026-10-21)

Author typo found in review (`MadoR22`), confirmed independently against the cell source; truth itself unchanged:

- **Original** `CaptureNestedFactory.json` is **retained unmodified** and will be rejected as author typo pre-seal, not as a tool-based exclusion.
- **Superseding file**: `CaptureNestedFactoryCorrected.json` (same seat id `CaptureNestedFactory`, same cell, same class/evidence).
- Exact delta, both occurrences of the same dropped token (`nest-`):
  1. `want[0].command`: was `pacman -S r22-nest-outer r22-inner` → now `pacman -S r22-nest-outer r22-nest-inner`, matching the cell's `pkg="r22-nest-inner"` argument.
  2. Rationale shlex serialization quote: was `'pacman -S r22-nest-outer r22-inner'` → now `'pacman -S r22-nest-outer r22-nest-inner'`, matching the stated argv `['pacman','-S','r22-nest-outer','r22-nest-inner']`.
- The stale token also appeared in this report's "Frozen truth" line above; corrected in place and logged here.
- No other field changed: cells, expected_kind, forbid_observed_commands, source, and the semantic argument are byte-identical in intent; verified the corrected file parses as JSON with the corrected row.
