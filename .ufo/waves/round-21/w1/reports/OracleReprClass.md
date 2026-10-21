# OracleReprClass — C1 precision oracle proposal (repr(C), negative)

Seat: MadoR21.OracleReprClass, round-21 wave 1, leaf member, no delegation, no tool measurement, no installs.

Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ReprClass.json` (this file is the separate advisory note; the JSON is the proposal).

## Verdict

**Proposed (accepted).** The stated negative — expected no findings, `want: []` — is semantically correct for the class-argument form `repr(C)`. It was not forced: the instance-argument form was explicitly checked and rejected (below).

## Fixture (exact, one per proposal)

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "r21-reprclass"])

class C:
    def __repr__(self):
        f()
        return "C()"

repr(C)
```

Required preamble: `import subprocess` only; `repr` is a builtin. `f` is the visible subprocess-spawning function; `C` defines only the specifically relevant unused method `__repr__` and no constructor.

## Static semantic audit (no execution)

1. Module body executes only: the import, two definitions, and `repr(C)`. The class body contains only `def`, so definition time performs no call into `f`.
2. `repr(C)` passes the class object itself. Implicit special-method lookup happens through the object's type: `type(C)` is the default metaclass `type`, so `repr(C)` resolves to `type.__repr__(C)` and returns a string like `"<class '__main__.C'>"`. The `__repr__` function stored in `C.__dict__` serves instances of `C`; `C` is not an instance of `C`, so it is never consulted.
3. `f`'s sole reference is inside the never-invoked `C.__repr__` body; `f` is never called, so `subprocess.run` sits in deferred code that is never entered.
4. `C` is never instantiated; there is no `__init__` and no spawn routed through construction, per the assignment's constructor rule.
5. Therefore no process-spawning path is reachable and no finding of any class (neither observed nor lead) is expected: `want: []`. The transcript is inert — executed or only scanned, nothing in it spawns.

## Boundary checked before accepting the negative

- `repr(C())` would dispatch `repr` through `type(instance)` to `C.__repr__`, call `f`, and legitimately execute the spawn — a finding would then be semantically required and `want: []` would be wrong. That form is deliberately not used, and the proposal's rationale records this boundary so the integrator cannot swap the forms.
- The negative also must not be overgeneralized to "repr never dispatches": for an *instance* argument, `repr(instance)` is a real invocation path into `__repr__` (the recall-side complement). Round-20's committed guard list names a recall fixture `ar40-repr-dunder.jsonl` (`.ufo/waves/round-20/a2/evidence/guards-before-28c6837.txt:120`); this seat only pins the class-object case as clean.

## Provenance

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:11` — the value-only `repr(C)` shape is recorded as round-20 false-lead fixture line 19 (`package_query` lead at `a8960de`, clean at `28c6837`); its correction rule (:13) is that pure builtins are non-sinks and only dunders implied by an actual operation are followed. Provenance for the shape only; the expected result here is independently derived from Python semantics, as C1 requires.
- Python data model: special-method implicit invocation is via the object's type (`https://docs.python.org/3.14/reference/datamodel.html#special-lookup`); `object.__repr__` is the repr protocol for objects (`https://docs.python.org/3.14/reference/datamodel.html#object.__repr__`).

## Seat separation

Sibling seats cover the neighboring shapes: construction-without-dunder-call (`UnusedCall`, `PureJson`), value-only function reference (`OracleReprFunction`, `print`/`id`/`callable` seats). This seat uniquely pins `repr` applied to a class object, distinct from round-20 fixture lines 9, 10 (construction) and 11 (`repr(f)`).

## Limits

- Static reasoning only; the fixture was never executed, no tripwire or gate was run, no tool measurement occurred (wave-1 rule). Round-20 fixture bytes under `/tmp` are non-durable and were not relied on; only the committed review line is cited.
- The expectation is a truth statement about Python semantics; whether any tool revision matches it is decided later by the integration owner's frozen measurement, not by this proposal.
- Installs: none.
