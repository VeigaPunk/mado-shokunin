# AtkUnusedAdd — scoped C1 falsification

## Axes and verdict

- **Frozen-oracle truth / precision:** the frozen `want: []` is semantically warranted.
- **Generality:** the current clean result follows generic class-construction and call/reference handling, not a fixture-name or command-text exception.
- **Recall:** **Medium — concrete false negative.** A one-operation nearby variant invokes `__add__`, reaches `subprocess.run`, and is still scanned as clean.

**Verdict:** keep the frozen empty expectation; do not treat the current rule as complete for operation-triggered special methods.

## Identity and bounded scans

- Candidate revision reported by L1 and observed at repository HEAD: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Candidate: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`; SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Frozen input: `.ufo/waves/round-21/oracle/inputs/UnusedAdd.jsonl`, SHA-256 `3366fc79c21446d341c8b9281048a26e4b94b4c7db2bbfeedf4928ed66c9c6d2`. Frozen expectation selects `w1/oracles/UnusedAdd.json`, has `want: []`, and records the same input digest in `.ufo/waves/round-21/oracle/expected.json`.
- Retained variant: `.ufo/waves/round-21/w2/fixtures/AtkUnusedAdd/UnusedAddInvokedAdd.jsonl`, SHA-256 `9f50f87b4308392a80741e95afcc1c7b2074da0e410d63f671d6de41d3714ff8`.
- I used the existing `measure.py` `scan` API through `runpy` for each input. Each scan launched only its scanner child with the API's 384 MiB `RLIMIT_AS` and 15-second timeout. The transcript Python was parsed/scanned, never executed.
- Exact frozen scan result: scanner exit 0; `findings: []`; `lead_findings: 0`; `observed_findings: 0`; `eval_unparsed: 0`; `unparsed_spawns: 0`; stderr empty.
- Exact variant scan result: scanner exit 0; `findings: []`; `lead_findings: 0`; `observed_findings: 0`; `eval_unparsed: 0`; `unparsed_spawns: 0`; stderr empty.
- The supplied aggregate candidate receipt is not evidence for these current bytes: it identifies measured commit `843d301d1b17af78427918f7845af336b2218de0` and tool SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, both different from the candidate inspected here.
- No tools were installed or updated.

## Frozen expectation is warranted

The frozen code imports `subprocess`, defines `f` with a `subprocess.run(["pacman", "-Q", "hyprland"], ...)` call, defines `C.__add__` to call `f`, and ends with `C()`. **[INFERENCE]** Construction does not perform a binary addition, so it does not invoke `__add__`; the class has no custom `__init__`, `__new__`, or `__del__` that reaches `f`. The `subprocess.run` is inside the deferred `f` body, reachable here only from the uncalled `__add__` body. Therefore there is no command execution to classify, and no class/command/evidence finding is warranted for this exact input. The current scanner's clean result agrees with that semantics.

If reached by a real addition, the call would warrant **[INFERENCE]** one `package_query` finding with rule `pacman:-Q`, command `pacman -Q hyprland`, and evidence `observed`. The empty frozen expectation does not claim that this command is harmless or suppress a reached call; it says the call is not reached in the frozen transcript.

## Generality and operation-dispatch gap

The relevant implementation is shape-based. `spawn_scan` resolves a class call and follows its `__init__` when present, while separately considering `__new__` and `__del__`; its comment explicitly notes that construction does not invoke every operator/context dunder (`tools/mado-tripwire.py:2276-2292`). `eager_calls` adds protocol references for constructs such as comparison, subscription, and attribute access (`:1839-1844`), and `spawn_scan` follows protocol references supplied to it (`:2371-2385`). I found no `UnusedAdd` or `hyprland` literal in the candidate source. The clean frozen scan is thus not keyed to fixture wording; it results from the generic distinction between construction and special-method use.

That distinction is incomplete for binary addition: the `eager_calls` path does not add a `("protocol", "__add__")` reference for an `ast.BinOp` using `ast.Add`. The variant below reaches the method under Python's binary-operator semantics, but the scanner does not follow it. **[INFERENCE]** This is an operation-dispatch gap, not a reason to change the frozen `want: []`.

## One nearby counterexample

The retained inert JSONL variant changes only the final expression from `C()` to `C() + 1`:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "hyprland"], capture_output=True)

class C:
    def __add__(self, other):
        return f()

C() + 1
```

Observed candidate output is a clean verdict with zero findings and zero parse/unparsed-spawn counts. **[INFERENCE]** Executing this Python expression would dispatch to `C.__add__`, call `f`, and reach `subprocess.run`; expected scanner evidence is `class=package_query`, `rule=pacman:-Q`, `argv0=pacman`, `command=pacman -Q hyprland`, `evidence=observed`. I did not execute the payload. This is one bounded counterexample, not a claim about all operator protocols or all scanner behavior.

## Verification gaps and residual risk

No LSP device/server route is mounted in this session (`read xd://lsp` reported no such tool), so LSP status, references, definitions, and diagnostics were unavailable. The source reads above support the implementation-path discussion; no grep result is used as semantic proof. No full corpus or suite was run. The retained test is limited to this frozen case and one `__add__` variant; other special-method operations remain outside this scoped check.

Report: `.ufo/waves/round-21/w2/reports/AtkUnusedAdd.md`
