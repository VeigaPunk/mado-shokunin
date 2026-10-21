# RecallDecorators — C1 decorators/defaults falsification

**Verdict:** The current candidate has a concrete eager-decorator false negative: a helper passed through `functools.partial` as a decorator executes during function definition, but its value-only reference is discarded. The same scanner probe correctly reports an executable helper call in a default expression, so the missed decorator path is distinct from ordinary eager-default handling.

## Candidate and bounded probe

Candidate observed before the probe: commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; SHA-256 of `tools/mado-tripwire.py`: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

The inert fixture is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/RecallDecorators-2/decorator-default.jsonl` (SHA-256 `78bd74a67c65c2722ed3d3c60418ca7e11507c264da33e8beb0d9cf76fa743bc`). It contains two independent shapes:

```python
import functools
import subprocess

def decorator_worker(fn):
    subprocess.run(["pacman", "-S", "decorator-eager"])
    return fn

@functools.partial(decorator_worker)
def decorated():
    pass

def default_worker(cb):
    cb(["pacman", "-S", "default-eager"])
    return None

def with_default(value=default_worker(subprocess.run)):
    pass
```

I invoked the existing `oracle/measure.py` `scan` API via `runpy`. It launched one scanner child with its 384 MiB `RLIMIT_AS` cap and 15-second timeout; the transcript code was treated as data and not executed. Exact observed result: scanner `exit=1`, `stderr=""`, `eval_unparsed=0`, `unparsed_spawns=0`, `observed_findings=1`, `lead_findings=0`; the sole finding was `host_mutation / pacman -S default-eager / observed` (`rule=pacman:-S`). There was no `decorator-eager` finding.

## Finding

**High — eager `functools.partial` decorator drops the wrapped helper.** At runtime, evaluating `@functools.partial(decorator_worker)` produces a partial, and function-definition decorator application calls that partial with `decorated`; it therefore enters `decorator_worker` and reaches `subprocess.run(["pacman", "-S", "decorator-eager"])`. Python's language reference defines decorators as evaluated/applied as part of function definition, and `functools.partial` as a callable that invokes its wrapped function with the bound arguments (references: [function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions), [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial)).

The candidate loses this path in three linked places: `eager_calls` explicitly marks only bare `Name`/`Attribute` decorator expressions as decorator references (`tools/mado-tripwire.py:1861-1864`); the `decorator_worker` name nested inside the call has the `functools.partial(...)` call as its parent; and `spawn_scan` skips references whose parent resolves to a pure/value callable unless it is one of the modeled higher-order callables (`:2386-2394`). Since `functools.partial` is treated as pure, the helper reference is discarded even though the resulting partial is then invoked by decorator application. `update_bindings` tries to resolve decorator wrappers (`:1720-1725`) but does not represent this returned-partial application as a helper call. This is a real executable path, not merely passing a callback as inert data.

The default-expression control is the contrasting positive case: `default_worker(subprocess.run)` is a call in `FunctionDef.args.defaults` (`:1865-1867`), and the candidate follows its helper body with the callback binding, reporting the literal `default-eager` command as observed.

## Residual risk and verification gaps

- This probe isolates decorator application from a normal eager default. It does not establish annotation behavior. The function-definition traversal explicitly includes decorators and defaults, but not parameter or return annotations (`:1865-1867`); annotation evaluation is runtime/version/future-import-sensitive, so no annotation verdict is made here.
- No full suite or corpus was run. LSP was unavailable in this seat: `read xd://lsp` returned “No such tool”; text search was used only to locate code, not as semantic proof. The finding is based on the source, Python semantics above, and the single bounded scanner result.
- No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/reports/RecallDecorators.md`
