# CasePureBuiltins — P cases capture pure-builtin false positives

## Scope and method

Created eight Family P cases under `.ufo/waves/round-20/w1/cases/CasePureBuiltins/`: seven pure builtin regressions expected clean, plus one existing `PURE_ARG_CALLS` control. The seven regressions cover the exact round-19 `frozenset` closure, direct `frozenset`, `type`, `bool`, `callable`, `ascii`, and `format`. The closure fixture copies the r19 assistant-toolCall envelope and substitutes only the code, as requested. All case JSONL content is data for `--scan`; no fixture code was executed.

The required isolated clone command, `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20-CasePureBuiltins`, observed HEAD `e629f731172b8238caffe50f152217ce56535fb4`. Pinned tools were copied with read-only `git show` into `/tmp/mado-r20-CasePureBuiltins/revisions/`:

- `1f7f995caa25627db804e996cccd87fe38a3a1b6` (`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`)
- `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` (`c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`)

The case copies in `/tmp/mado-r20-CasePureBuiltins/case-copy/` were scanned from that directory, one command per file and revision: `python3 -I /tmp/mado-r20-CasePureBuiltins/revisions/tool-REV.py --scan FILE`. The counter's before values below are pass/fail against each case's declared clean outcome: the seven regression cases fail at `1f7f995` because it emits a row, and pass at `9c54c56`; the control passes at both.

## All-builtin census at 1f7f995

To satisfy the initial census requirement, I generated one-call JSONL fixtures for all 159 identifier names in `dir(builtins)`, using the syntax shape `<name>(['pacman','-Q','hyprland'])`, then scanned all 159 paths with the pinned `1f7f995` tool. These fixtures were also never executed. Exact summary from the scan harness: `builtins=159 exit=1`; stdout first line `MADO_TRIPWIRE: findings`; parsed verdict `finding_count=125`; stderr was empty. Every listed hit was a `package_query` / `pacman:-Q` row for `pacman -Q hyprland` with no `evidence` key (the counter treats an unmarked row as `observed`).

Names that emitted a row (125):

```text
ArithmeticError, AssertionError, AttributeError, BaseException, BaseExceptionGroup, BlockingIOError, BrokenPipeError, BufferError, BytesWarning, ChildProcessError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, DeprecationWarning, EOFError, Ellipsis, EncodingWarning, EnvironmentError, Exception, ExceptionGroup, FileExistsError, FileNotFoundError, FloatingPointError, FutureWarning,
GeneratorExit, IOError, ImportError, ImportWarning, IndentationError, IndexError, InterruptedError, IsADirectoryError, KeyError, KeyboardInterrupt, LookupError, MemoryError, ModuleNotFoundError, NameError, NotADirectoryError, NotImplemented, NotImplementedError, OSError, OverflowError, PendingDeprecationWarning, PermissionError, ProcessLookupError, PythonFinalizationError, RecursionError, ReferenceError,
ResourceWarning, RuntimeError, RuntimeWarning, StopAsyncIteration, StopIteration, SyntaxError, SyntaxWarning, SystemError, SystemExit, TabError, TimeoutError, TypeError, UnboundLocalError, UnicodeDecodeError, UnicodeEncodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning, UserWarning, ValueError, Warning, ZeroDivisionError, _IncompleteInputError, __build_class__, __debug__,
__doc__, __import__, __loader__, __name__, __package__, __spec__, abs, aiter, anext, ascii, bin, bool, breakpoint, bytearray, callable, chr, classmethod, complex, copyright, credits, delattr, dir, divmod, exit, float,
format, frozenset, globals, hash, help, hex, id, int, issubclass, license, locals, memoryview, object, oct, ord, pow, property, quit, range, round, slice, staticmethod, super, type, vars
```

Names with no row (34): `False`, `None`, `True`, `all`, `any`, `bytes`, `compile`, `dict`, `enumerate`, `eval`, `exec`, `filter`, `getattr`, `hasattr`, `input`, `isinstance`, `iter`, `len`, `list`, `map`, `max`, `min`, `next`, `open`, `print`, `repr`, `reversed`, `set`, `setattr`, `sorted`, `str`, `sum`, `tuple`, `zip`. `False`, `None`, and `True` are syntax constants rather than callable names, so their generated forms were not valid call expressions. This census mechanically covers every name as requested; it is not a claim that all generated calls are valid Python invocations. The committed cases avoid invalid `bytearray([...])` and `vars([...])` shapes and use valid value-inspection/formatting calls instead.

## Case list and exact pre-repair scans

`cases.json:1` declares all eight cases with `want_exit: 0` and `want_findings: []`. Each fixture is a single JSONL line (`line=1`); every row below is one call with literal argv-like strings. For all seven reds, the exact `1f7f995` stdout was `MADO_TRIPWIRE: findings` followed by the complete JSON line shown below. The corresponding `9c54c56` scan returned exit 0, first line `MADO_TRIPWIRE: clean`, and an empty `findings` list.

| Case | Fixture | Before `1f7f995` | Before `9c54c56` |
|---|---|---|---|
| `P-CasePureBuiltins-frozenset-closure` | `frozenset-closure.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-frozenset-direct` | `frozenset-direct.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-type-list` | `type-list.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-bool-list` | `bool-list.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-callable-list` | `callable-list.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-ascii-list` | `ascii-list.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-format-list` | `format-list.jsonl:1` | fail | pass |
| `P-CasePureBuiltins-str-control` | `str-control.jsonl:1` | pass | pass |

The exact `1f7f995` scan output for each red (the first line is identical for all seven):

```text
frozenset-closure.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "frozenset-closure.jsonl", "sha256": "14558b6dd1574253772b30af041169c6fb0eda992d47c7773c342c225472f040", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "frozenset-closure.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

frozenset-direct.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "frozenset-direct.jsonl", "sha256": "4228358619a714c130d0b3778bb9d2e1a27e260a5105e0dbfd8e981f45c5307b", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "frozenset-direct.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

type-list.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "type-list.jsonl", "sha256": "4f7a5a5becdd8c0dcc979b330b800aa00757c57bd3c7318d8df87645a425d0f4", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "type-list.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

bool-list.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "bool-list.jsonl", "sha256": "e60eedcbd7b5b8ccc886056d471a1fa68ba0c7689dbca7f9a8a66d437e0ebe4b", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "bool-list.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

callable-list.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "callable-list.jsonl", "sha256": "8c89ebe97448496782579d7e0ee6ed8c014fab64b1355c4b175fd70af31d3543", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "callable-list.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

ascii-list.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "ascii-list.jsonl", "sha256": "13316acb052412e1721e0bb4836578f1d960befbe6a16c6575e3502ae9f84b17", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "ascii-list.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}

format-list.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "format-list.jsonl", "sha256": "5d854b132e86722be247bfd8e65e4383f708fa8285e5ad88f438b2994f368ddd", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "format-list.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

The exact copied lesson establishes the harm at `corpus/lessons/round-19-verifier-spotcheck.md:67-81`; the original envelope is `corpus/.../py-lead-cross-cell-literal.jsonl:1`. The current helper rule exempts only names in `PURE_ARG_CALLS`, shown at `tools/mado-tripwire.py:1252-1257`; all selected red builtins are outside that list. Expected rows for this P family are empty because these builtins only transform or inspect data; the same source rule produces an unmarked `package_query` row on the harmed revision.

## Risks and blockers

The all-name census deliberately uses one syntactic call shape for every `dir(builtins)` entry; a subset are non-callables or reject a list at runtime. That census therefore measures scanner behavior only, not runtime validity. The committed cases use valid builtin calls, and the fixture code was never executed. No blockers observed.

## Limits

No post-integration revision, precision counter, existing tripwire suite, full-corpus diff, gate, or implementation patch was run; those remain with L1. The case scans above are the specifically assigned before-comparison only.

## Installs

none
