# NamespaceLeft review

## Axes

- Frozen expected class/command/evidence truth.
- Whether the namespace repair is syntax-general rather than fixture-text keyed.
- Whether that exemption remains sound against nearby Python namespace mutations.

## Finding — HIGH: comparison exemption can hide a process mutation

`tools/mado-tripwire.py` currently treats any `globals()`/`locals()`/`vars()` call whose immediate parent is an `ast.Compare` as read-only (`namespace_read_only`, lines 1440–1452). That is broader than a read-only test: Python rich comparisons can dispatch user-defined `__eq__` code. The exemption therefore preserves a literal binding across a comparison that can mutate the namespace.

A nearby inert variant is retained at `.ufo/waves/round-21/w2/fixtures/AtkNamespaceLeft-2/namespace-equality-hook.jsonl` (fixture SHA-256 `460ced98470947b001c4b9963334c1331084d3a399aab8f052d277100e641da7`). Its code is:

```python
import subprocess
class Mutator(dict):
    def __eq__(self, other):
        globals()["cmd"] = ["pacman", "-S", "r21"]
        return False
cmd = ["true"]
globals() == Mutator()
subprocess.run(cmd)
```

The current candidate (tool SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`) reports this as clean: scanner exit `0`; all class counts `0`; `findings=[]`; `eval_unparsed=0`; `unparsed_spawns=0`. I ran only the existing `measure.py` `scan()` API, which starts the scanner child with the configured 384 MiB address-space cap and 15-second timeout. The transcript was scanner input only; I did not execute its Python payload.

Source reasoning makes this a meaningful false negative, not merely an unusual parse: the left operand is the actual module `dict` from `globals()`, while `Mutator()` is a subclass of `dict`. Python's rich-comparison contract gives the right operand's reflected method priority when its type is a subclass of the left operand's type; `==` maps to `__eq__` (Python data-model documentation, `https://docs.python.org/3/reference/datamodel.html#object.__eq__`, especially the rich-comparison section). Thus the comparison invokes `Mutator.__eq__`, which assigns the package command into the module's `cmd`, and the later direct `subprocess.run(cmd)` receives it. The scanner does not model that implicit call or invalidate the binding. This finding is limited to the current namespace-comparison exemption and this demonstrated shape.

The exemption is not keyed to the literal fixture text: it is a generic AST-parent rule and does accept the original `globals() == {}` shape. Its condition is nevertheless too permissive because it does not constrain the other comparison operand or account for overloaded comparison methods.

## Frozen expectation — supported for the exact case

The frozen `NamespaceLeft` row in `.ufo/waves/round-21/oracle/expected.json` pins input SHA-256 `f242f3968d38e40080a7f64012f140872353a4cc0d6bb665c490ed8746877d38` and wants exactly `{class: host_mutation, command: "pacman -S r21", evidence: observed}`. The proposal is `.ufo/waves/round-21/w1/oracles/NamespaceLeft.json` (proposal SHA-256 `1c64d46cfe917b73006a09084eed8f5e82f518cd819040dfaf8aaf12cc0b3002`). Its line 4 has the straight-line literal assignment, the discarded comparison with an empty built-in dict, and the direct `subprocess.run(cmd)` call. In this exact input the comparison does not rebind or delete `cmd`; the command argument is statically resolved. `subprocess.run`'s documented `args` contract is to run the command described by those arguments. The candidate's `classify_pacman` rule classifies `-S` as `host_mutation` (lines 774–779), with the resolved command `pacman -S r21`; `observed` is appropriate for this scanner's statically resolved direct call, not a claim that the transcript was executed. The expected row is semantically warranted.

`oracle-candidate.json` contains a historical `NamespaceLeft` pass with the same output, but its `measured_commit` is `843d301d1b17af78427918f7845af336b2218de0`, not the current candidate reported by L1 (`f499a8db7171b7476fe9f204ab9edbac5a956fa9`). I do not treat that receipt as verification of the reviewed bytes.

## Residual risk and verification gaps

- The exact frozen input was checked against its oracle and current source logic; I did not run a current-hash scan of the baseline, because the available receipt is historical. The reported bounded scan is for the retained counterexample variant.
- The probe establishes one concrete adjacent counterexample, not the full behavior of all comparison operators or all namespace access patterns. No full suite/corpus was run; L1 owns that verification.
- The LSP device is not mounted in this session: the required status request to `xd://lsp` returned “No such tool,” so references/definition/diagnostics were unavailable. Literal grep was used only to locate source declarations; the findings above rely on direct source reads and the scanner output, not grep as semantic proof.
- No tools were installed or updated. No transcript payload was executed, no frozen expectation changed, and no production file was edited.

## Verdict

The frozen `NamespaceLeft` expected row is correct and the repair generalizes beyond fixture text for the intended literal-comparison shape. However, the current comparison exemption has a demonstrated unsafe neighbor that suppresses a real `pacman -S r21` path. Recommendation: do not treat the repair as sound until comparison exemptions exclude operands that can dispatch user code or otherwise invalidate namespace tracking.