# ScoutBuiltinsFire — the harmed tool flags 125 of 159 builtin names as host commands; the pre-harm tool flags 0, and no lead marker exists to distinguish them

Scan-only experiment, no fixture executed. All paths absolute; lane HEAD observed
`e629f731172b8238caffe50f152217ce56535fb4` (detached; `git rev-parse HEAD`).

## Setup

Tools extracted read-only from the lane, hashed:

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show e629f73:tools/mado-tripwire.py > /tmp/scout-builtins/tool-e629f73.py
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 9c54c56:tools/mado-tripwire.py > /tmp/scout-builtins/tool-9c54c56.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  tool-e629f73.py
c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd  tool-9c54c56.py
```

Host interpreter `Python 3.14.8`; `dir(builtins)` = `builtins.__dict__` = 159 names
(no dir-only or dict-only keys). Fixture builder (deterministic; rerun with the same
interpreter to match the digest):

```python
import builtins, json
with open("/tmp/scout-builtins/builtins-all.jsonl", "w") as fh:
    for n in sorted(dir(builtins)):
        fh.write(json.dumps({"type": "message", "message": {"role": "assistant",
          "content": [{"type": "toolCall", "name": "eval",
            "arguments": {"language": "py",
              "code": "%s(['sudo','pacman','-S','foo'])" % n}}]}}) + "\n")
```

Fixture: `/tmp/scout-builtins/builtins-all.jsonl`, 159 lines, sha256
`00b2941ebcbf7620f3e64bfd612dfce252d01e32862ddf0ea788b06bbfaf245d`. Each line is one
assistant `eval` cell whose whole code is `NAME(['sudo','pacman','-S','foo'])`; every
cell is parsed, none executed (`--scan` only parses text; I never ran fixture code).

## Headline (observed)

```
$ python3 -I /tmp/scout-builtins/tool-e629f73.py --scan /tmp/scout-builtins/builtins-all.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 250, "live_probe": 0, "package_query": 0,
            "tool_install": 0, "vcs_write": 0}, "exit": 1, ...}
$ python3 -I /tmp/scout-builtins/tool-9c54c56.py --scan /tmp/scout-builtins/builtins-all.jsonl
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0},
 "exit": 0, "findings": [], ...}
```

125 lines fire at e629f73 (250 rows = 125 x 2 rules `sudo` and `pacman:-S`), 0 lines
fire at 9c54c56. The 34 non-firing names are exactly the 31 builtins the tool whitelists
plus the three literal constants (`True`, `False`, `None`, which parse as `ast.Constant`
so the `ast.Name` dispatch never sees them).

## Table — builtin names that fire at e629f73 and not at 9c54c56 (125)

Every listed name produced the identical pair `host_mutation/sudo` + `host_mutation/pacman:-S`
on its own line; class/rule never varied across the run.

| kind | n | names |
|---|---|---|
| exception classes | 71 | ArithmeticError, AssertionError, AttributeError, BaseException, BaseExceptionGroup, BlockingIOError, BrokenPipeError, BufferError, BytesWarning, ChildProcessError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, DeprecationWarning, EOFError, EncodingWarning, EnvironmentError, Exception, ExceptionGroup, FileExistsError, FileNotFoundError, FloatingPointError, FutureWarning, GeneratorExit, IOError, ImportError, ImportWarning, IndentationError, IndexError, InterruptedError, IsADirectoryError, KeyError, KeyboardInterrupt, LookupError, MemoryError, ModuleNotFoundError, NameError, NotADirectoryError, NotImplementedError, OSError, OverflowError, PendingDeprecationWarning, PermissionError, ProcessLookupError, PythonFinalizationError, RecursionError, ReferenceError, ResourceWarning, RuntimeError, RuntimeWarning, StopAsyncIteration, StopIteration, SyntaxError, SyntaxWarning, SystemError, SystemExit, TabError, TimeoutError, TypeError, UnboundLocalError, UnicodeDecodeError, UnicodeEncodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning, UserWarning, ValueError, Warning, ZeroDivisionError, _IncompleteInputError |
| types / constructors | 16 | `__loader__`, bool, bytearray, classmethod, complex, float, frozenset, int, memoryview, object, property, range, slice, staticmethod, super, type |
| builtin functions | 25 | `__build_class__`, `__import__`, abs, aiter, anext, ascii, bin, breakpoint, callable, chr, delattr, dir, divmod, format, globals, hash, hex, id, issubclass, locals, oct, ord, pow, round, vars |
| non-function builtin objects | 13 | Ellipsis, NotImplemented, `__debug__`, `__doc__`, `__name__`, `__package__`, `__spec__`, copyright, credits, exit, help, license, quit |

Not firing (34): `True`, `False`, `None` (constants) and all, any, bytes, compile, dict,
enumerate, eval, exec, filter, getattr, hasattr, input, isinstance, iter, len, list, map,
max, min, next, open, print, repr, reversed, set, setattr, sorted, str, sum, tuple, zip
(the 31 whitelist names that exist as builtins).

## Findings

1. **The purity test is a 31-name whitelist, not the builtin namespace (observed).**
   `PURE_ARG_CALLS` is defined at `tools/mado-tripwire.py:1252` (e629f73) and its
   membership among builtins is exactly the 31 names above; `frozenset` is absent. The
   lead dispatch at `tools/mado-tripwire.py:1433` calls `helper_argv_leads` for every
   bare `ast.Name` call whose name is not in that set, so the 125 remaining builtins are
   all routed into shell classification. This contradicts E2 as written ("the callee is a
   Python builtin not rebound in the text … `frozenset`, `set`, `tuple`, `list`, `dict`,
   `type`, …"): the contract exempts the namespace, the code exempts a hand-picked
   33-name set (31 of which are builtins). Adding `frozenset` alone would leave 124 names
   firing [INFERENCE: from the observed set membership].

2. **No lead marker exists at all; pure-data rows are shape-identical to real spawn rows
   (observed).** Emitted finding keys are exactly
   `['argv0','class','command','file','line','rule','timestamp','tool','tool_call_id']`
   (`tools/mado-tripwire.py:1600-1601` builds this dict; no `evidence` field), and the
   verdict keys are `['counts','exit','files','findings','permitted','schema','unpermitted']`
   — no `observed_findings`/`lead_findings`, contrary to E1. Concretely, at e629f73:
   `frozenset(['pacman','-Q','hyprland'])` -> `package_query / pacman:-Q`, while
   `subprocess.run(['sudo','pacman','-S','foo'])` -> `host_mutation / sudo` +
   `host_mutation / pacman:-S`; both rows are the same unmarked shape. Under
   the round-20 comparison rule ("a tool row WITHOUT an evidence key counts as observed"),
   every one of these 125 names would be scored **observed**, i.e. provably pure data
   presented as evidence-backed. The module docstring (lines 41-48) claims leads are
   reported; the payload never marks them.

3. **The exact harm case reproduces (observed).**
   `/tmp/scout-builtins/probe.jsonl` (sha256 `991e2024f565986953562008e556ec492ca86ebc01138bb4849e11aa3a5caa59`),
   line 1 `frozenset(['pacman','-Q','hyprland'])`: e629f73 exit 1, one
   `package_query/pacman:-Q` row (`command": "pacman -Q hyprland"`), no evidence key;
   9c54c56 exit 0 `clean`, no findings. This is the round-19 routed harm, byte-for-byte.

4. **The harm spans all five classes, not just package_query (observed).** From
   `/tmp/scout-builtins/probe3.jsonl` at e629f73 (9c54c56: clean, 0 rows):
   `frozenset(['pacman','-Q','hyprland'])` -> `package_query/pacman:-Q`;
   `frozenset(['git','commit','-m','x'])` -> `vcs_write/git:commit`;
   `frozenset(['uv','tool','install','ruff'])` -> `tool_install/uv:tool-install`;
   `bool(['hyprctl','probe'])` -> `live_probe/hyprctl:probe`; `bool(['sudo','pacman','-S','foo'])`
   -> `host_mutation` x2. All rows lack `evidence`.

5. **Adjacent, same mechanism: aliased pure-stdlib imports also fire (observed;
   contract reading [INFERENCE]).** On `/tmp/scout-builtins/probe3.jsonl` at e629f73,
   `from shlex import join` + `join(['sudo','pacman','-S','foo'])`, `from json import dumps`
   + `dumps([...])`, and `from collections import Counter` + `Counter([...])` each emit
   `host_mutation/sudo` + `host_mutation/pacman:-S`; all clean at 9c54c56. The tool only
   canonicalizes imports from subprocess/os/asyncio, so `shlex.join`/`json.dumps`/
   `collections.*` lose their E2 purity exemption once imported by bare name. This is
   outside the requested builtins table but is the same whitelist-versus-resolution gap,
   and a fix keyed on `dir(builtins)` alone would not close it.

6. **The whitelist gap propagates through visible-body helpers (observed).**
   `/tmp/scout-builtins/probe4.jsonl` (sha256 `15a4a40fd2f927123e4b8a1389382a176a44c5cb851ab75e17300b1aef9f3b7b`)
   at e629f73: `def fmt(x): return frozenset(x)` + `fmt(['pacman','-Q','hyprland'])`
   -> one `package_query/pacman:-Q` row, no `evidence` key, exit 1. The same helper body
   with `str(x)` or `len(x)` is clean (those names are whitelisted), and all three are
   clean at 9c54c56. This is E2's transitive clause failing for exactly the whitelist
   names: because the bound literal reaches `frozenset` inside the helper body, the defect
   is not confined to module-level cells — a pure formatter helper is flagged at its call
   site simply for passing argv through a non-whitelisted builtin.

## What a C1 repair must satisfy, from this evidence (advisory, not a design)

- E2 precedence over E1 dispatch: decide purity by *resolution* (name is a builtin in
  effect at the call, after in-text rebinding/`del`, per E3), not by a fixed name list.
- E1 marker: emit a per-row `evidence` value and the `observed_findings`/`lead_findings`
  integers; otherwise the round-20 counter's missing-key default scores leads as
  observed, which is the scored failure mode, not just a cosmetic gap.
- [INFERENCE] Any repair validated only against `frozenset` will still fail cases built
  on exception classes, `bool`, `type`, `len`-siblings or aliased stdlib calls.
- Purity must be resolved in the same pass that binds helper arguments: a `def` body
  forwarding its parameter into a whitelisted-versus-builtin callee is flagged at the call
  site today (finding 6), so the exemption has to be applied to the resolved callee inside
  the body, not only at module level.

## Limits

- Scan-only: no fixture code executed; `--scan` parse path only, `--frozen` not exercised.
- One argv shape (`['sudo','pacman','-S','foo']`) for the 159-name sweep; the class-spread
  probe used six additional single-line cells. Different argv would not change dispatch,
  only the emitted rule [INFERENCE from `helper_argv_leads` reading its positional args].
- Host Python only (3.14.8): the builtin roster, and therefore the 125/159 count, is
  interpreter-specific; no other CPython version tested.
- Did not test rebinding/shadowing (E3, S seat), help/dry-run (E4, H seat), invisible-body
  leads (L seat), `--permit` output effects, or the round-20 precision counter itself.
- Did not run any existing suite, the lane gate, or the live `mado-verify.sh`.
- Only `ast.Name` call shapes were probed; attribute calls and keyword `args=[...]` were
  read in source, not exercised. Helper probe covered three one-line bodies
  (`frozenset`/`str`/`len`); deeper nesting, decorators and lambdas were not exercised.

## Installs

none.
