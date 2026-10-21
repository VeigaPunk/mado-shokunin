# ClassTargetDormant — scoped C1 attack
**Axes:** frozen oracle semantic correctness; repair generality; nearby inherited-constructor coverage.


## Result

- **Frozen expectation: warranted.** The proposal (`w1/oracles/ClassTargetDormant.json`, `want: []`) matches the Python path. `Thread(target=C).start()` starts a worker that invokes the callable target with no arguments, i.e. `C()`. With no class-defined `__init__`, construction uses the inert `object.__init__`; it does not invoke the ordinary `never_called` method. The only `subprocess.run(["pacman", "-S", "r21"])` is inside that uncalled method, so no command/evidence row is warranted. The frozen manifest binds this exact input SHA-256 `f591067dd1303b2f324c836b95e06ef44c1fda635a31847f4ecd5b7362631f99` to `want: []` (`oracle/expected.json:104-113`; proposal `w1/oracles/ClassTargetDormant.json:1-10`).
- **Repair shape: structural, not fixture-text keyed.** Current source handles resolved class targets generically: the `Thread`/`Timer` plus `.start()` reference path turns a class target into a synthetic constructor call (`tools/mado-tripwire.py:2396-2411`); class-call handling follows a class-body `__init__` and the construction-relevant `__new__`/`__del__`, rather than sweeping every ordinary method (`tools/mado-tripwire.py:2276-2292`). These branches use AST/binding kinds and method names, not the case ID, class name `C`, method name `never_called`, or command text. This supports the frozen no-initializer shape. It does not resolve inherited methods.

## Finding — Medium: inherited constructor side effect is silently missed

A nearby semantic variant preserves the dormant ordinary method but adds a base class whose initializer is executed when the thread target constructs `C`:

```python
import subprocess, threading
class Base:
    def __init__(self):
        subprocess.run(["pacman", "-S", "r21-base"])
class C(Base):
    def never_called(self):
        subprocess.run(["pacman", "-S", "r21-dormant"])
threading.Thread(target=C).start()
```

**Semantically expected:** `host_mutation`, command `pacman -S r21-base`, rule `pacman:-S`; the target invocation constructs `C`, which resolves `__init__` to `Base.__init__`. The `r21-dormant` command remains unreachable. The direct constructor-follow path represents a resolved body as `observed` (`follow_helper`, `tools/mado-tripwire.py:2155-2165`).

**Actual scanner output:** ran only the bounded scanner API `measure.py`'s `scan()` on this inert JSONL input; no code in the transcript was executed. The child scanner exited 0 under the API's 384 MiB address-space limit and 15-second timeout. It returned `eval_calls: 1`, `eval_unparsed: 0`, `unparsed_spawns: 0`, all class counts zero, and `findings: []`. Input file SHA-256: `323b9157ddd70571af4a86912bcaab553898b21653bb08e889fcf41f539cbea7` (ephemeral path `/tmp/mado-class-target-di5nijt0/variant.jsonl`). Thus it misses the reachable inherited initializer command, not the dormant method.

This is consistent with the source's direct search for `__init__` only in `helper.body` and no base-class traversal (`tools/mado-tripwire.py:2276-2292`). The module's limits also explicitly say inherited methods are not resolved (`tools/mado-tripwire.py:71-74`). I record it as a scoped coverage gap in the class-target rule, not as evidence against the frozen `want: []`.

## Receipt, identity, and verification limits

- L1 identified the production candidate as commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. The actual tested `tools/mado-tripwire.py` bytes were SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Existing `evidence/oracle-candidate.json` is **not** a receipt for that candidate: its `measured_commit` is `843d301d1b17af78427918f7845af336b2218de0`; at that revision it reported the original dormant `pacman -S r21` as one `host_mutation` lead. I did not treat that old result as current behavior.
- No LSP route/server was mounted (`xd://lsp` returned “No such tool”); therefore there was no LSP status, references, definition, or diagnostics response. Text search was used only to locate source sections; the semantic checks above are based on Python call semantics and the cited source. No tests/full corpus were run; only the one bounded scanner-only variant probe was run. No tools were installed, and expectations were not changed.
