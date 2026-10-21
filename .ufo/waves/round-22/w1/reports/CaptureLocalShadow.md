# CaptureLocalShadow — C1 truth proposal (factory local shadows module global before returned closure)

Seat: `MadoR22.CaptureLocalShadow` · Round 22 W1 · Artifact-only. No measurement, no detector run, no production edit, no probe, no payload execution.

## Deliverable

- Proposal: `.ufo/waves/round-22/w1/proposals/CaptureLocalShadow.json`
- Frozen proposal SHA-256: `74a90015ed7c05fd25d3acd6d7d16185a09dca2dbcf527eda5a9d3aea78c765d` (2357 bytes, valid JSON, `expected_kind` = `exact`)
- Frozen eval-cell source SHA-256: `4bb821ae0602a02f84d279c912ec0c70681c1ca48335d22070839a7a107ac09a` (1 cell; parses with `ast.parse`)

## Scenario (reconstructed contract)

Supported literal-source form proposed for C1 truth:

```python
import subprocess
def shadow():
    subprocess.run(["pacman", "-Q", "r22-shadow-global"])
def make():
    def inner():
        subprocess.run(["pacman", "-S", "r22-shadow-local"])
    shadow = inner
    return shadow
make()()
```

The factory body assigns the factory-local name `shadow` (bound to `inner`) before `return shadow`, and a module-level `def shadow` with a distinct body exists. The returned closure must be the factory-local binding, never the module global.

## Static truth (frozen before implementation)

| Step | Derivation |
|---|---|
| Module `def shadow` | Binds a module global whose body runs `pacman -Q r22-shadow-global`. A bare module-level `def` is a binding, not a call: this body is never executed by the cell. |
| `make` scope | `shadow = inner` assigns a name with no `global` declaration, so `shadow` is factory-local for `make`'s entire scope and shadows the module global from that point. |
| `return shadow` | Returns the factory-local function bound to `inner`. |
| `make()()` | Executes `inner`'s body: `subprocess.run(["pacman", "-S", "r22-shadow-local"])` — exactly one `host_mutation` finding, evidence `observed`. |

Expected finding set, exact: `[{class: host_mutation, command: "pacman -S r22-shadow-local", evidence: observed}]`. Nothing else: no lead, no unparsed, no row for the never-called module global.

`forbid_observed_commands`: `["pacman -Q r22-shadow-global"]`. Any observed row naming the module-global command is an observed value borrowed from a same-named module global — precisely what registration round-22 C1 excludes ("Unknown capture arguments may produce lead/unparsed uncertainty but never observed values borrowed from module globals"), and the failure class this variant exists to pin.

## Evidence chain

1. Python 3.14 naming-and-binding semantics: assignment to a name in a function body without a `global` statement makes it local for the whole function scope; the module binding is shadowed. (Grounding: CPython 3.14.8 reference — execution model / naming and binding; the W1 `sources/SourceClosure/` corpus carries the same reference documents for cross-checking.)
2. Round-21 residual `FinalBindingReview.md` F3 (High context): the returned closure's identity is currently selected from `def` bindings and a factory-body rebinding is ignored; F2: unbindable/failed resolution leaks same-named module globals as observed. This variant places a same-named module global behind a bindable factory, so both wrong outcomes are in reach: wrong body from a stale `def` selection, or a fabricated observed row from the module global.
3. Registration round-22 C1: bounded static-source-shape agreement; expectations frozen before implementation; observed values may never be borrowed from module globals.
4. Taxonomy: `pacman -S …` classifies `host_mutation`, `pacman -Q …` classifies `package_query` (observed classification in the round-21 probe table of `FinalBindingReview.md`).

## Expected divergence of the pre-repair detector ([INFERENCE], by source, not measured)

Per the r21 mechanism notes only: resolving `return shadow` from `def` bindings can select the module global `def shadow` (wrong body, fabricated observed `pacman -Q r22-shadow-global`) or miss the rebind entirely (silent wrong/absent row). Both diverge from the frozen truth. I did not run the detector and make no claim about its actual output on this cell; wave measurement will decide.

## Honestly rejected / unsupported shapes (not covered by this proposal)

- Factory parameters, `*args`/`**kwargs` spread, keyword/default/missing-required capture: covered by sibling uncertainty seats (`CaptureStarUnknown`, `CaptureKwUnknown`, `CaptureMissingRequired`, …); excluded here to keep the minimal literal variant.
- Conditional rebind (`shadow = a if c else b`), non-`Name` returns, `global shadow` inside the factory (semantically a different variant: true module-global rebinding), nested factories, `functools.partial` returns, cross-cell persistence, thread/timer bodies: not declared supported forms for this seat; expectations would be guesses, so they are rejected rather than frozen.
- Shadowing via namespace mutation (`sys.modules`, `globals()` writes): opaque; outside declared forms.

## Unknowns

- Pre-repair detector behavior on this exact cell: unmeasured by design; no claim made.
- Whether the implementation resolves the factory-local rebinding through its planned snapshot mechanism: implementation detail, deliberately not assumed; only the frozen truth above is normative.

## Compliance

No packages installed or updated (directive satisfied vacuously; nothing needed). No background jobs. Git untouched. Writes confined to this seat's two named paths. Source text (r21 review, registration, spec excerpts) treated as data only.
