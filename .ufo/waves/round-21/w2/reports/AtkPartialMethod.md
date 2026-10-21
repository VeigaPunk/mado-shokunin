# PartialMethod — C1 primary attack

**Verdict:** The frozen `package_query / pacman -Q r21 / observed` expectation is semantically warranted. The repair is structural for the direct `functools.partialmethod` spelling and is not keyed to the fixture's command text. One nearby, semantically equivalent imported-alias variant is a real miss in the current candidate.

## Frozen expectation

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json` records PartialMethod's `want` as class `package_query`, command `pacman -Q r21`, evidence `observed`; the frozen input digest is `e9d6cb5822962903bc10fca37f319a79355a3805cb8799b6ac9dac8dbc07b68d`. The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/PartialMethod.json` has the same expectation.

The input at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/PartialMethod.jsonl` defines `worker(self)` with a direct `subprocess.run(["pacman", "-Q", "r21"])`, assigns `C.run = functools.partialmethod(worker)`, then calls `C().run()`. Python 3.14's `functools.partialmethod` documentation specifies descriptor binding and that a normal function's bound `self` is inserted as the first positional argument. Thus this call reaches `worker` with its instance parameter bound and reaches the exact literal argv; there is no unknown callback, branch, or dynamic argument in the path. `pacman -Q` is classified by the candidate's `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:737-780` as `package_query`. `observed` is warranted as a fully resolved source path, not as a claim that I executed the transcript payload; no payload was run. Reference: https://docs.python.org/3.14/library/functools.html#functools.partialmethod.

The existing candidate receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` reports PartialMethod passing with one observed package-query finding, but its `measured_commit` is `843d301d1b17af78427918f7845af336b2218de0`, not the current candidate commit below. I treat it as historical corroboration, not current-code verification.

## Repair generality and traced source

Current candidate identity observed before the probe: commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

At `mado-tripwire.py:1549-1574`, `class_method_info` recognizes class-body assignment to the requested method name, checks for a call whose final dotted component is `partialmethod`, resolves its wrapped callable through `callable_info`, and returns helper metadata with `skip_first=True`, instance binding, and retained fixed positional/keyword arguments. The path is consumed by `callable_info`'s instance/class attribute resolution at `:1623-1637`, then `spawn_scan` at `:2214-2264` resolves the call and follows the helper. This encodes the descriptor/self-binding shape and forwards its bound arguments; the shown logic has no special case for `worker`, `r21`, or `pacman`. It is therefore general to this recognized syntax shape, but not to all equivalent Python spellings.

## Nearby counterexample (scanner-only)

I changed the import/call spelling to `from functools import partialmethod as pm` and `invoke = pm(dispatch)` while retaining the same class-body descriptor, bound invocation, and literal subprocess call. The exact inert input is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkPartialMethod/partialmethod-alias.jsonl` (SHA-256 `78e7d597de34f4572ef81a18cfd498b05e3154ef1eacfba7c354ddf2739b24fa`). Its code text is:

```python
from functools import partialmethod as pm
import subprocess

def dispatch(self):
    subprocess.run(["pacman", "-Q", "r21"])

class Runner:
    invoke = pm(dispatch)

Runner().invoke()
```

I called the existing `measure.py` `scan` API via `runpy` on this fixture, which invokes only the bounded scanner child (384 MiB address-space cap, 15-second timeout); the Python/shell payload was not executed. Exact observed result: scanner `exit=0`, `stderr=""`; payload `findings=[]`, all five counts zero, `lead_findings=0`, `observed_findings=0`, `eval_calls=1`, `eval_unparsed=0`, and `unparsed_spawns=0`. This is a concrete miss, not evidence of a global absence of other misses.

Source explains the miss: `update_bindings` at `mado-tripwire.py:1736-1747` recognizes `pm` as an imported `functools.partialmethod` binding, but `class_method_info` at `:1567-1568` tests the syntactic dotted name's final token for the literal string `partialmethod`. For `pm(dispatch)` that token is `pm`, so the descriptor is not resolved and the helper body is not followed. At runtime, `pm` names the same imported descriptor constructor, and `Runner().invoke()` uses the documented `partialmethod` binding behavior, so the same `package_query / pacman -Q r21 / observed` truth applies.

## Limits and provenance

No transcript payload, package command, suite, or corpus was run; no tool was installed or updated. No LSP endpoint/device was exposed in this seat's available tools. Text search was used only to locate definitions/call sites; conclusions above rely on the read source sections, Python documentation, frozen input, and bounded scanner result. Scope is the PartialMethod shape only; no claim is made about overall candidate correctness.

Report: `.ufo/waves/round-21/w2/reports/AtkPartialMethod.md`
