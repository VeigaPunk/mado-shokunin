# AtkPureShlex — scoped C1 critique

## Axes

- **Frozen-oracle truth / precision:** the frozen `PureShlex` expected result is warranted for its exact input.
- **Recall:** the current purity exemption misses one nearby, actually effectful iterable case.
- **Generality / provenance:** the exemption is callable-path-based, not keyed to the fixture text; its claimed purity is broader than the source semantics support.

## Verdict

**Accept `want: []` for the frozen PureShlex fixture; reject an unqualified `shlex.join` purity rule.** The repair is general with respect to the resolved callable name, but it does not preserve the important distinction between the fixture's literal list and an arbitrary iterable whose iteration runs user code.

## Frozen expected row

`.ufo/waves/round-21/oracle/expected.json` selects `PureShlex`, proposal `w1/oracles/PureShlex.json`, with `want: []` and fixture SHA-256 `c008d615c49873255a3ef4d6f528e62cd42b400d0da15508ffd6be6d14869bfb`. In that input, `shlex.join(["pacman", "-Q", "r21"])` receives a literal built-in list of strings; it only formats data and has no process-spawning path. CPython 3.14.8 `Lib/shlex.py:320-322` implements `join` as `return ' '.join(quote(arg) for arg in split_command)`. Iterating this literal list invokes no user-defined iterator. The `subprocess.run` call appears only inside `f`; `f` is only referenced inside `C.cmd`, which is never called. `C()` uses inherited `object` initialization and invokes no instance method. Thus the command-looking list is not a command, no class method reaches the process call, and there is no warranted observed or lead class/command/evidence row.

The current code expresses a general callable-path rule: `PURE_STDLIB_EXACT` contains `shlex.join`, `update_bindings` resolves the imported `shlex` module, and `callable_info` marks the resolved path pure. This is not keyed to `PureShlex` fixture text. However, `spawn_scan` skips a `pure` call without considering whether the argument's iteration protocol executes user code.

## One nearby counterexample

Retained inert scanner input: `.ufo/waves/round-21/w2/fixtures/AtkPureShlex-2/PureShlexIterable.jsonl` (SHA-256 `128f63730e47a9192297dcda9af032ee69dfc6ad09905eb1f82fdb2c499e8b70`). The eval code is:

```python
import shlex
import subprocess

class Query:
    def __iter__(self):
        subprocess.run(["pacman", "-Q", "r21"])
        return iter(["pacman", "-Q", "r21"])

shlex.join(Query())
```

This is semantically effectful: CPython's `shlex.join` iterates `split_command`, so calling it with `Query()` invokes `Query.__iter__`, which calls `subprocess.run`. I did **not** execute the payload. I ran the authorized `measure.py` `scan` API against this inert JSONL; it launched only the scanner under its 384 MiB / 15-second per-child bounds. Observed result: scanner `exit: 0`, verdict `clean`, `findings: []`, `eval_unparsed: 0`, `unparsed_spawns: 0` (stderr empty). This is a false negative for this one variant.

## Smallest safe correction

Keep the clean result for the frozen literal-list call, but do not treat every `shlex.join` argument as inert. Preserve the pure fast path for statically known, plain built-in literal sequences; for an argument that may have user-defined or lazy iteration, follow the applicable iteration protocol (including a visible `__iter__` body) or retain a bounded lead/unknown rather than silently skipping it. Do not reinterpret the list contents as a command merely because they resemble argv.

## Reproducibility and limits

- Candidate revision reported by L1: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Exact `tools/mado-tripwire.py` bytes used for the scanner probe: SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Primary implementation evidence: [CPython 3.14.8 `Lib/shlex.py`, `join`](https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/shlex.py#L320-L322); local source index `corpus/SOURCES.md` S107.
- The variant is one scoped counterexample, not a whole-tool completeness claim. Its code was scanned, not run. No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/reports/AtkPureShlex.md`
