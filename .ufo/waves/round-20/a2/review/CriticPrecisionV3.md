# CriticPrecisionV3 — falsified: v3.1 adds 18 impossible-call leads and silences a stdlib process launcher caught by 28c6837.

## Findings

### 1. False lead rows from value-only references — high severity
- Reproduce from the lane root:
  `python3 -I ../../../../../tmp/mado-r20a2-CriticPrecisionV3/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-CriticPrecisionV3/fixtures/precision-ref-probes.jsonl`
  and substitute `tw-9c54c56.py` / `tw-a8960de.py` for the other revisions.
- Input: `../../../../../tmp/mado-r20a2-CriticPrecisionV3/fixtures/precision-ref-probes.jsonl`; SHA-256 `8d98edee9b712c76fdc56cef9deff414129719c4c654c1ffc09157052b92f84f`.
- Observed: `28c6837` = clean, 0 findings; `9c54c56` = 20 `observed` rows; `a8960de` = 18 `package_query` `lead` rows at fixture lines 1, 2, 4–6, 8–20. Expected at `a8960de`: no row for those cases—the function bodies are not called. The command scan itself did not execute any fixture code.
- False rows, all `pacman -Q hyprland`: line 1 `print(f)`; 2 `print(lambda)`; 4 `isinstance(object(), C)`; 5 `hasattr(C, 'missing')`; 6 a variable annotation `annotation: f`; 8 `saved = f`; 9 constructing `C` whose `__add__` is never used; 10 constructing `C` whose instance `__call__` is never used; 11 `repr(f)`; 12 `id(f)`; 13 `callable(f)`; 14 `getattr(f, '__name__')`; 15 `typing.cast(object, f)`; 16 a return annotation naming `f`; 17 a class annotation naming `f`; 18 `issubclass(C, object)`; 19 `repr(C)`; 20 `functools.partial(f)` discarded without invocation. These are plain reads/stores or class construction, not paths into the bodies. Lines 3 (`f.__name__`) and 7 (`del f`) are clean at `28c6837` and `a8960de` and are negative controls.
- Impacted axes: precision (18 new false leads vs `28c6837`); no new row vs `9c54c56` because it already reported these as observed.
- Smallest safe correction: only sweep a referenced body when the surrounding operation is an invocation-capable sink or a statically recognized operation that calls it. Treat metadata/value-only uses, annotations, deletion, and pure builtins as non-sinks. On class construction, follow `__init__` and only dunders implied by an actual operation, not every dunder.

### 2. New purity split miss: `imaplib.IMAP4_stream` — high severity
- Reproduce from the lane root:
  `python3 -I ../../../../../tmp/mado-r20a2-CriticPrecisionV3/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-CriticPrecisionV3/fixtures/stdlib-purity-probes.jsonl`
  and substitute `tw-a8960de.py` for the second run.
- Input: `../../../../../tmp/mado-r20a2-CriticPrecisionV3/fixtures/stdlib-purity-probes.jsonl`; SHA-256 `682d3ca9e3e543b3dc69b32a1547364899b20ebfd88af1b88bce6b0f54120ba7`.
- Fixture line 1 is `from imaplib import IMAP4_stream; IMAP4_stream(['loginctl'])`. Observed: `28c6837` emits a `lead` `live_probe` row (`loginctl:list-sessions`) on line 1; `a8960de` emits no row on line 1 (its only row in this fixture is the `functools.reduce` control on line 2). Expected: retain a row for this real process launch.
- Evidence: CPython source `../../../../../usr/lib/python3.14/imaplib.py:1795-1812` stores the command and calls `subprocess.Popen(self.command, ..., shell=True)` from `open`; `IMAP4_stream.__init__` calls `IMAP4.__init__` at `:1795-1797`, and the base constructor dispatches to `self.open` at `:202-219`. `../../../../../usr/lib/python3.14/subprocess.py:1837-1852` accepts a sequence and converts it to `/bin/sh -c` plus its first item, so this fixture launches `loginctl`. In `tools/mado-tripwire.py:1504-1510`, `imaplib` is absent from `PROCESS_STDLIB`; `:1523-1525` therefore marks its callable path pure, and the pure-call branch skips it. The 28c opaque-name path instead sends the literal list to `helper_argv_leads` (`../../../../../tmp/mado-r20a2-CriticPrecisionV3/tw-28c6837.py:1874-1877`).
- Impacted axes: recall / purity boundary. This is a v3.1 regression against `28c6837`.
- Smallest safe correction: classify `imaplib.IMAP4_stream` as process-capable (an exact spawn path is narrower than making every `imaplib` callable opaque).

### 3. Other process-capable “pure” callables checked — pre-existing misses, not v3.1-only
- The same reproduction command/input above compares `28c6837` with `a8960de`. At line 4, `uuid._get_command_stdout('pacman', '-Q', 'hyprland')` is clean at both revisions; CPython `../../../../../usr/lib/python3.14/uuid.py:424-446` resolves the executable and calls `subprocess.Popen((executable, *args))`. This is a real spawn when `pacman` resolves in `PATH` [INFERENCE], but not a differential regression: 28c6837's opaque helper only extracts a literal argv list, while v3.1 classifies `uuid.*` pure. Smallest correction: classify this exact path as process-capable.
- At line 6, a `logging.config.dictConfig` configuration passes `subprocess.run` as the handler factory with `args=['pacman','-Q','hyprland']`; both revisions are clean. CPython `../../../../../usr/lib/python3.14/logging/config.py:481-493` calls the supplied factory with its config kwargs. This is a real callback-driven spawn path, but 28c6837 also misses the nested config and it is not a newly lost row. Smallest correction: do not treat `dictConfig` as data-only; inspect its nested callable factory and arguments.
- At line 3, `operator.methodcaller('__call__', ['pacman','-Q','hyprland'])(subprocess.run)` is also clean at both revisions despite being an actual callable dispatch: `../../../../../usr/lib/python3.14/operator.py:310-327` implements `__call__` as `getattr(obj, name)(*args, **kwargs)`. This remains a pre-existing hole because `operator` was already in the explicit pure-module set at `28c6837`. Smallest correction: do not mark the returned methodcaller callable data-only when it is invoked.
- Control: line 2 uses `functools.reduce` with `subprocess.run` and a literal argv. `28c6837` is clean; `a8960de` emits the expected `pacman -Q hyprland` lead. The v3.1 reference sweep catches this callback case; it does not offset the misses above.
- Impacted axes: recall / purity boundary; only the `imaplib` item is counted as newly regressed against `28c6837`.

## Limits
Only the listed fixtures were scanned; no transcript payload was executed and no CPython module was imported. Source establishes callable paths, not runtime availability of external commands. The probe set is targeted, not an exhaustive audit of every CPython 3.14 stdlib module. The v3.1 tool copy matched the pinned SHA-256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`.

## Installs
none
