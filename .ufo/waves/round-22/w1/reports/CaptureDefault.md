# CaptureDefault — frozen truth proposal

Seat: `MadoR22.CaptureDefault` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Round-22 wave 1. Static truth only: no production edits, no detector measurements, no payload execution. Artifact: `.ufo/waves/round-22/w1/proposals/CaptureDefault.json`.

## Variant (one, independent)

**Factory omitted literal default parameter with a same-named module global.** One eval cell:

```python
import subprocess
def make(argv=["pacman", "-S", "r22-default"]):
    def run():
        subprocess.run(argv)
    return run
argv = ["pacman", "-Q", "r22-default-global"]
runner = make()
runner()
```

Cell ordering deliberately mirrors the r21 failing fixture `capture-unbound-global.jsonl` (`def` factory → same-named decoy global → factory call → invoke). The only changed fact: the factory call is *bindable* — the argument is omitted and `argv` carries a literal default.

## Frozen expectation

- `expected_kind`: `exact`
- `want`: `host_mutation` · `pacman -S r22-default` · `observed` — exactly one row, zero unparsed.
- `forbid_observed_commands`: `pacman -Q r22-default-global` — the decoy module global's argv must never surface as an observed row.

## Semantic argument (Python 3.14, static, nothing executed)

1. `def make(argv=[...])` evaluates the list-literal default once, when the `def` statement executes; "the same 'pre-computed' value is used for each call" (compound_stmts.rst 1305–1308).
2. `make()` omits the argument, so `argv` is bound from that pre-computed default — "the corresponding argument may be omitted from a call, in which case the parameter's default value is substituted"; a call "always assigns values to all parameters … either from positional arguments, from keyword arguments, or from default values" (compound_stmts.rst 1297–1301, 1327–1329). The module global plays no part in parameter binding.
3. Inside `run`, `argv` is a free variable resolved "using the nearest enclosing scope" (executionmodel.rst 89–93, 113–115) — `make`'s local parameter cell, captured by the closure at `def run` creation. The module-level `argv` assignment is dead on this path: it is written but never read by any evaluated expression.
4. Therefore `runner()` performs exactly `subprocess.run(["pacman", "-S", "r22-default"])`: one `host_mutation` observed row (`pacman -S`, matching the r21 observed classification for literal argv inside a followed closure). No uncertainty: every name resolves statically, so `exact` with zero unparsed.

## Relation to r21 findings

This variant sits between F1 and F2. It is **not** F1 (no post-creation rebinding of the passed object; the parameter gets the default, a different object than the same-named global). It directly guards the **F2** defect shape — "an unbindable factory call lets the closure's parameters resolve to same-named module globals, which are then reported as observed" (FinalBindingReview.md F2, spawn_scan line 2335 mechanism). A detector that treats "omitted argument" as "unbound parameter" and falls through to module-global resolution would fabricate `pacman -Q r22-default-global` as observed — exactly what `forbid_observed_commands` rejects. Truth: the parameter is bound, to the `def`-time literal.

## Independence and limits

- Authored from Python language semantics and the published F2 failure shape only; no candidate detector source read, no measurement, expectation not derived from any implementation.
- One cell; `reset` semantics not exercised. Single literal-defaulted positional parameter; no `*`, `**`, keyword, or non-literal default forms claimed — adjacent forms are owned by sibling Capture* seats.
- If the harness tokenizes `command` differently than `shlex.join` of the argv tokens, the want row needs re-serialization, not re-reasoning.
- Class assignment (`host_mutation` for `pacman -S`) is inherited from the r21 probe's observed row classification; if the frozen class map changes, only `class` changes — the argv and evidence tier do not.

## Citations

- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst` lines 1297–1329 (official CPython 3.14.8 reference, fetched by SourceClosure; HTTP 200, raw.githubusercontent.com).
- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst` lines 89–115, 136–148.
- `.ufo/waves/round-21/residual/FinalBindingReview.md` F1/F2 findings and probe table; fixture `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl` (sha256 `9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d`) for the decoy ordering.

## Tools

None installed or updated. Git/files read-only; no packages queried, no live probes, no cells executed.
