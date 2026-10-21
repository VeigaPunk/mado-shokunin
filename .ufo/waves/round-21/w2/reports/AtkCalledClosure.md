# CalledClosure — scoped adversarial finding

## Verdict

The frozen `CalledClosure` expectation is semantically warranted. The repair is generic for the direct returned-nested-function shape, not keyed to the fixture’s names or command text, but the current implementation does not model reassignment of a captured cell before the closure is returned. One nearby scanner-only variant exposes that gap: the candidate reports the original argument as a package query instead of the reassigned host mutation.

## Frozen case

- Oracle: `.ufo/waves/round-21/oracle/expected.json:76-91`; proposal: `.ufo/waves/round-21/w1/oracles/CalledClosure.json`; input: `.ufo/waves/round-21/oracle/inputs/CalledClosure.jsonl` (SHA-256 `f7b158fc4f057b401bf46d5d8ec6f00cf7c10f85e1af05bde21e980e11a3afb2`).
- The expected multiset is `package_query / pacman -Q w2shape / observed`.
- **Semantic assessment:** `outer` is called with the literal argv list, defines `inner` closing over its parameter `argv`, and returns `inner`; the immediate `()` invokes it. Since the owner does not rebind `argv`, `subprocess.run(argv)` receives exactly `['pacman', '-Q', 'w2shape']`. This is a directly visible, statically bound path, so `observed` (not `lead`) and the expected category/command are warranted. This assessment follows the stored code and Python closure/call semantics; the stored payload was not executed.

## Repair generality and source trace

The tested candidate file SHA-256 was `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` (candidate revision reported by the coordinator: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`). In `tools/mado-tripwire.py`, `callable_info` recognizes a called helper whose body directly returns a locally defined nested function and tags it with `capture_owner`/`capture_call` (lines 1613-1622). `spawn_scan` binds the owner’s call arguments and merges them into the call-site literal environment before following the returned helper (2231-2235). This is AST-shape-based and contains no `CalledClosure`, fixture path, package name, or command-text special case; it generalizes to other literal-bound instances of this same narrow shape.

It is not a general model of Python closure-cell state: capture is computed by `bind_literal` from the owner’s call arguments (1896-1962), without propagating assignments performed in the owner body before its return. Thus the source supports the base case, but not arbitrary closure mutations/rebindings.

## Nearby counterexample (one bounded scanner-only probe)

Inert input retained at `.ufo/waves/round-21/w2/fixtures/AtkCalledClosure/captured-rebind.jsonl` (SHA-256 `00cc1cabeca7f51ada1ef70edcae18af3be9f744448df2c403b7f678880164e2`). It defines the same `outer`/returned-`inner`/immediate-invocation shape, but reassigns `argv` after defining `inner` and before returning it:

```python
import subprocess

def outer(argv):
    def inner():
        subprocess.run(argv)
    argv = ["pacman", "-S", "r21capture"]
    return inner

outer(["pacman", "-Q", "initial"])()
```

Python’s closure cell contains the reassigned list when `inner` runs; the semantically warranted row is `host_mutation / pacman -S r21capture / observed`. The bounded scan instead returned `package_query / pacman -Q initial / observed`, with `exit=1`, `host_mutation=0`, `package_query=1`, and `unparsed_spawns=0`. This is a concrete misclassification, not an unparsed/timeout result. The scanner was run once through `oracle/measure.py`’s `scan` API via `runpy`; its implementation imposes one child, 15 seconds, and 384 MiB. Only the inert JSONL was scanned; its Python text was never executed.

## Evidence limits and environment

- `.ufo/waves/round-21/evidence/oracle-candidate.json` is historical, not evidence for the tested bytes: it records `measured_commit=843d301d1b17af78427918f7845af336b2218de0`, `tool_sha256=56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, and a passing `CalledClosure` row. The frozen expected case and this probe were not rewritten.
- The LSP device is unavailable (`xd://lsp` returned “No such tool”); grep was used only to locate definitions/call sites. The findings above are grounded in the read source ranges and the bounded scan, not grep presented as semantic proof.
- No tools were installed.
