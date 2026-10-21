# CapturePartialOverride — C1 static-truth variant report

Seat: `MadoR22.CapturePartialOverride` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Round 22 wave 1, pre-implementation freeze. Artifact authoring only; no production edits, no detector measurements, no payload execution.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialOverride.json` — written, JSON-parses, single eval cell parses with `ast.parse`. Independent specification, not derived from any detector output.

## Variant

Factory `make()` returns `functools.partial(worker, argv=["pacman","-S","r22-partial-fixed"])` — a fixed *keyword* argument stored at construction. The invocation `runner(argv=["pacman","-Q","r22-partial-override"])` supplies the same keyword again. Python's partial-call merge makes the invocation value win.

```python
import functools
import subprocess

def worker(argv):
    subprocess.run(argv)

def make():
    return functools.partial(worker, argv=["pacman", "-S", "r22-partial-fixed"])

runner = make()
runner(argv=["pacman", "-Q", "r22-partial-override"])
```

## Frozen expectation

| Field | Value |
|---|---|
| `expected_kind` | `exact` |
| `want` | `package_query` · `pacman -Q r22-partial-override` (shlex.join of the literal list) · `observed` |
| `forbid_observed_commands` | `["pacman -S r22-partial-fixed"]` |

Exactly one subprocess spawn point (`worker`'s `subprocess.run`), reached exactly once, argv fully literal at every step — so zero unparsed counters and one observed row. The stored `-S` list is provably unreachable; an observed row for it, alone or alongside the true row, is a defect.

## Semantic basis (Python 3.14)

- `functools.partial` docs: "If additional keyword arguments are supplied, they extend and override keywords" — the call-site `argv` overrides the stored one.
- Reference implementation `/usr/lib/python3.14/functools.py:392` (installed 3.14.8): `partial.__call__` computes `keywords = {**self.keywords, **keywords}` then `self.func(*pto_args, *args, **keywords)` — repeated keys take the invocation value. The C `partial` has identical documented behavior.
- Defect class: FinalBindingReview F1, line 75 — "a returned `functools.partial` evaluates its fixed arguments in the invocation env" was flagged same-class-by-source, unprobed. This variant exercises the adjacent *keyword-override* axis rather than the env-timing axis of `CaptureSameCell`/`CapturePartialFixed`: the winning argument is an invocation-site literal, so the truth holds no matter which environment a scanner snapshots; a scanner must additionally merge and deduplicate the stored keyword, not merely evaluate it in the right env.

## Independence and bounds

- Truth derived from Python call/`partial` semantics and stdlib source only; sibling proposals were consulted for JSON shape only, not for expectations.
- One subprocess run, one result row, inert `pacman -S`/`-Q` marker argv only; no live commands, installs, probes, or network.
- No tools installed or updated (none needed). No builds/tests/measurements run, per wave freeze.
- Cell never executed; it is inert ast-scanner input.

## Residual risk / unknowns

- If the delivered detector's supported form set excludes `functools.partial` keyword merging entirely, the honest outcome is unparsed/lead rather than the exact row; the proposal states the Python-truth expectation regardless, and `forbid_observed_commands` records the row that must never be claimed observed.
- The variant deliberately isolates the keyword-override merge; it does not combine with env-timing rebinding (no variable is rebound), so it cannot itself discriminate env-timing repairs — sibling seats cover that axis.
