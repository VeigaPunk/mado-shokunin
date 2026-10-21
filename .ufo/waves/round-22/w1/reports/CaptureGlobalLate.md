# CaptureGlobalLate — static-truth C1 variant (independent proposal)

Seat: `MadoR22.CaptureGlobalLate` · role: reviewer · wave: mado-r22-w1 · proposal: `.ufo/waves/round-22/w1/proposals/CaptureGlobalLate.json`

## Variant

Closure refers to an **unshadowed module global** changed after factory construction; **late global binding expected**. One eval cell, inert — never executed:

```python
import subprocess

CMD = ["pacman", "-Q", "r22-early"]


def make_runner():
    def runner():
        return subprocess.run(CMD)

    return runner


runner = make_runner()
CMD = ["pacman", "-S", "r22-globallate"]
runner()
```

## Frozen expectation

- `expected_kind`: **exact** — the argv reaching `subprocess.run` is fully determined statically; no unknown operand exists.
- `want`: exactly one row — `{"class":"host_mutation","command":"pacman -S r22-globallate","evidence":"observed"}` (argv serialized via `shlex.join(["pacman","-S","r22-globallate"])`).
- `forbid_observed_commands`: `["pacman -Q r22-early"]` — the pre-rebind value must never surface as an observed execution.
- Zero unparsed expected; exactly one spawn site; no lead expected (every operand is a literal resolvable in the live module env at invocation).

## Python 3.14 static semantics (independent of detector)

1. `runner` has **zero parameters** — the F1/F2 defect class (factory-argument binding timing / parameter-miss fallback to module globals) is unreachable by construction; `bind_literal` is never consulted for this closure.
2. `CMD` is bound only at module level; inside `runner` it is a free *global*, not a closure variable. CPython emits `LOAD_GLOBAL` against `make_runner.__globals__` at **call time**; `runner.__closure__` is empty — there is no cell whose contents a capture mechanism could legitimately freeze.
3. Order of module effects: bind `CMD`→`-Q` list; `make_runner()` returns `runner` capturing nothing; `CMD` rebinds to the `-S` list; `runner()` runs `subprocess.run` with the **late** value.
4. Sound truth: exactly one observed `host_mutation` `pacman -S r22-globallate`.

## Why this variant discriminates (axes)

- **Guard against over-freezing repair.** Registration C1 repairs F1–F3 by freezing *factory arguments* at creation. A naive `ClosureFrame` that snapshots the whole module literal env at factory construction would emit the early `-Q` row — a new counterexample to a declared supported form. This fixture separates "parameters freeze at creation" (correct) from "free globals freeze at creation" (wrong): same rebinding-before-invocation shape, opposite required answer.
- **Evidence/class discrimination.** Early value is `package_query` (`pacman -Q`), late value is `host_mutation` (`pacman -S`) — a wrong-timing answer is detectable by both class and command, not just digest.
- **Orthogonal axes, no padding.** Same-cell only (cross-cell belongs to `CaptureCrossCell`); zero params only (bindable/unbindable parameter paths belong to `CaptureBoundArgs`/`CaptureStar*`/`CaptureKw*` siblings). One expected row keeps the frontier crisp.

## Independence and bounds

- Authored from Python semantics plus the r21 `FinalBindingReview.md` defect text and the `SimplifyCapture` note's authority map (`file_literal_env` persistence) — **no detector measurement, no candidate-source reading, no payload execution**. Derived independently of any sibling proposal's expected rows.
- Leaf seat: no delegation, no shared-file edits (own proposal + this report only), Git untouched, no installs, no probes.

## Residual unknowns (explicit, none fabricated)

- Whether the wave's eval-cell format resets or persists module env between `cells[]` entries is irrelevant here: the variant is intentionally single-cell. Cross-cell global rebinding is a separate, uncovered-by-me axis (sibling territory).
- Behavior under a scanner that resolves globals at *binding-record* time rather than invocation time is exactly what this fixture detects; I assert no prediction about the current detector — only the static truth.
- `forbid_observed_commands` is populated but the `want` row is the sole expectation; whether the harness treats `forbid` as hard-fail or soft flag is a harness contract detail outside this proposal.

## Tools installed

None. No pacman transactions, no upgrades, no service changes — per contract, all pacman activity paused host-wide; nothing was needed.

Report: `.ufo/waves/round-22/w1/reports/CaptureGlobalLate.md`
