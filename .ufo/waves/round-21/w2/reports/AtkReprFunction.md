# ReprFunction — C1 scoped falsification

**Verdict:** The frozen `want: []` is semantically warranted. The current scanner implements the distinction by AST shape/protocol resolution, not by matching this fixture's text. One nearby instance-protocol variant was detected with the expected package-query class and command; no behavioral counterexample was found in that single probe. The variant's evidence is `lead`, not `observed` (precision caveat below).

## Observed facts

- Frozen case `.ufo/waves/round-21/oracle/expected.json:571-579` names `inputs/ReprFunction.jsonl`, `id: ReprFunction`, and `want: []`; its input digest is `6b7655c8327cc3153b10a97169e22d64361f64725be43f3c50f1edcd776ac0a0`. The proposal digest matches `.ufo/waves/round-21/w1/oracles/ReprFunction.json` (`37e5908e2bbc00c7900e7dd19522e19fbcbaf2f5e996043d9b7309ddfba67ce5`). The proposal also has `want: []` and states that `repr(f)` does not call `f`.
- That input imports `subprocess`, defines `f` with a `subprocess.run(["pacman", "-Q", "hyprland"])` body, then evaluates `repr(f)`; it never calls `f`.
- Tested scanner bytes: `tools/mado-tripwire.py` SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. Checked-out HEAD was `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`; the scanner Git blob at that commit is identical to the blob at `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (`368164381ebacc4f0c8fe43fd9c728dd4f767000`).
- Scanner source has no `ReprFunction` or `repr(f)` fixture-text match. `eager_calls` recognizes AST calls to the name `repr` and attaches a `__repr__` protocol reference (`tools/mado-tripwire.py:1845-1849`). The protocol consumer dispatches only for an instance receiver, or a call producing an instance/class (`2373-2384`); `class_method_info` resolves a directly defined method (`1549-1574`). A function binding is not an instance receiver. The broader scanner comment describes dunder-body sweeps as `lead` evidence (`2106-2133`).
- No LSP device was mounted in this session; source tracing used targeted reads and literal search, not semantic LSP results. No tools were installed or updated.

## Independent semantic assessment (inference)

Python evaluates the argument expression to `repr`, but here that expression is the function object `f`, not a call to `f`. The function object's representation does not execute its body or pass the function to a callback. Therefore the deferred `subprocess.run` is unreachable and an empty finding list is correct; there is no class/command/evidence row to expect. This conclusion follows from the input's control flow and Python representation semantics, not from a scanner result.

The implementation is shape-based: its `repr` branch is in the AST call walk, then the protocol resolver distinguishes a function binding from a constructed instance. This is not keyed to the fixture identifier or its `pacman`/`hyprland` strings. (The scanner's general `pacman` command classifier is unrelated to that decision.) This supports the frozen unshadowed-builtin shape, not every possible rebinding or dynamic-dispatch case.

## One nearby challenge

Saved inert JSONL: `.ufo/waves/round-21/w2/fixtures/AtkReprFunction-2/repr-instance-custom-repr.jsonl` (SHA-256 `22c9cf00535d923cc3aae4c8ab8dd69494fffe42172b078610bd76e2a5967a7d`). Its embedded source is:

```python
import subprocess

class C:
    def __repr__(self):
        subprocess.run(["pacman", "-Q", "hyprland"])
        return "C"

repr(C())
```

I called only the existing `measure.py` `scan` API on this JSONL: one scanner child, 384-MiB `RLIMIT_AS`, 15-second child timeout. The embedded Python was not executed. Observed result: scanner/verdict exit `1`; counts include `package_query: 1`; `eval_unparsed: 0`, `unparsed_spawns: 0`; finding `{class: package_query, command: "pacman -Q hyprland", rule: "pacman:-Q", evidence: lead}`.

This is the nearby boundary where `repr` does invoke a user-defined `__repr__`. The scanner retains the protocol route and the expected command classification rather than treating all `repr` arguments as inert. The `lead` label is conservative compared with this simple direct path: source routes protocol findings through `sweep_body`, whose documented policy is to label swept bodies as possible paths. Whether implicit protocol dispatch should be `observed` when this exact source proves the call is a remaining evidence-granularity question; it does not contradict the primary empty expectation. This one probe is not a global no-counterexample proof.

## Scope / limitations

No frozen expectations or production files were changed. No full corpus or suite was run. The existing `evidence/oracle-candidate.json` receipt reports `measured_commit: 843d301d1b17af78427918f7845af336b2218de0`, so it is historical and was not used as evidence for the tested bytes. Report: `.ufo/waves/round-21/w2/reports/AtkReprFunction.md`.
