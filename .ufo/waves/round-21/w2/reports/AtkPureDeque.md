# PureDeque C1 supplemental review

Axes reviewed: frozen-case semantic correctness; whether the repair is shape-generic rather than fixture-keyed; whether adjacent callback behavior escapes scanning.

Inspected scanner bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

## Finding — Medium: `collections.deque` purity exemption misses an iterable callback

The exemption is not keyed to the `PureDeque` fixture: `PURE_STDLIB_MODULES` includes `collections`, `pure_stdlib_path()` classifies every `collections.*` path as pure, and `callable_info()` resolves imported module paths before applying that rule (`mado-tripwire.py:1502-1537, 1641-1651`). This is a generic rule, but it is broader than the semantics needed for the frozen literal-list case.

Nearby counterexample input, retained as inert JSONL at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkPureDeque-2/deque-iter-callback.jsonl` (input SHA-256 `1cc7288ccb8c5dbcd16803f6f3ce77f709f884058e4d3445e4c4b8814dfc682a`):

```python
import collections
import os
class IteratorWithSideEffect:
    def __iter__(self):
        os.system("pacman -Q r21")
        return iter(())
collections.deque(IteratorWithSideEffect())
```

Python's deque constructor consumes its iterable, which invokes this object's `__iter__`; that method calls `os.system`. The scanner-only run instead returned a clean result: nested scanner exit `0`, all five counts `0`, `findings: []`, `eval_unparsed: 0`, and `unparsed_spawns: 0`. The fixture code was not executed. The scan used `oracle/measure.py`'s `scan` API, whose child is bounded at 384 MiB and 15 seconds.

The source path explains the miss: `eager_calls()` does not visit deferred function bodies, and only emits selected protocol references (`mado-tripwire.py:1813-1893`); `spawn_scan()` skips calls classified as `pure` (`2293-2294`) and class construction follows `__init__` plus `__new__`/`__del__`, not `__iter__` (`2276-2292`). No deque-iteration protocol edge reaches the deferred method body. This is a concrete false negative for the generic `collections.*` exemption. The observed command is a package query; applying the same unvisited method path to a more consequential command is a source-based risk, not a separately executed/tested case.

A narrow eager-argument control was also scanned from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkPureDeque-2/deque-eager-argument.jsonl` (SHA-256 `38bf18c4397f73b83d60663759c8eae7932373a521e6b35d2273a9209d877e31`): `collections.deque([os.system("pacman -Q r21")])`. It produced one observed `package_query` finding (`command: "pacman -Q r21"`, `rule: "pacman:-Q"`, `exit: 1`). Thus eager calls in the argument are still scanned; the counterexample is specifically a deferred protocol callback invoked by consuming a custom iterable.

## Frozen expectation — warranted

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/PureDeque.json:2-9` contains only `collections.deque(["pacman", "-Q", "r21"])`. The frozen row `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:478-486` is supplemental, has no normalization, and wants `[]`; the top-level contract at line 732 compares the strict multiset of class, command, and evidence. This expectation is semantically correct: the built-in deque consumes a literal list of strings as data; those strings do not call a process API or act as a shell command.

I independently scanned the exact frozen input against the inspected current bytes via `measure.py`'s bounded `scan` API. It returned nested exit `0`, input SHA-256 `6669baf034c3e5a57085b6aa010abf3c7b981445f62ca4e39096daf18e10da62`, `findings: []`, all counts `0`, and both unparsed counters `0`. The retained candidate receipt reports `PureDeque` passing too, but is marked `measured_commit: 843d301d1b17af78427918f7845af336b2218de0`; I did not treat that older receipt as proof of the inspected bytes.

## Residual risk and verification gaps

- The exact frozen literal-list shape is warranted and clean on the inspected scanner hash. The generic rule is not fixture-keyed, but the custom-iterable counterexample shows it does not safely generalize to all `collections.deque` inputs.
- These probes do not establish behavior for all iterator/callback protocols or other standard-library pure classifications; no whole-suite/corpus run was performed.
- The `lsp` device is not mounted (`read xd://lsp` returned “No such tool” and listed the available devices). Caller/definition/diagnostics LSP checks were unavailable; source ranges were read directly, and the one grep use only located the frozen row, not semantic proof.
- Only the two bounded scanner probes and the inert counterexample scan were run; no snippet code or shell payload was executed. No tools were installed.

**Verdict:** Keep the frozen `PureDeque` expectation `[]`; record the generic purity exemption's custom-iterable miss as an actionable adjacent false negative. No expectations were changed.

Report: `.ufo/waves/round-21/w2/reports/AtkPureDeque.md`
