# FalsifyC148 — C1 case TimerRunAlias (author-lane advisory critic)

**Verdict: AGREE** for this one sealed case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The delivered tool reproduced the sealed row exactly, and independent reading of the archived CPython 3.14.8 source confirms the sealed truth. This is not admission, not a non-author grant, and not proof of the F4 family.

## Identities (checked before and after the run; no drift)

| artifact | sha256 |
|---|---|
| `tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches assignment; runner reports the same before and after) |
| `tools/mado-evidence-audit.py` (C2, not run) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (matches; not executed) |
| `oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches assignment and `expected.sha256`) |
| `audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (matches; not used here) |
| `oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` (= sealed `runner_sha256`) |
| `oracle/inputs/TimerRunAlias.jsonl` | `98a1495255b941df6e1e86f98f22bbbb7431c93d3c83f76364c86b0fefc0c544` (= sealed `input_sha256`; also reported by the scanner) |
| `w1/proposals/TimerRunAlias.json` | `750446f95542c3831fa3a6449783891a5bc04d12d08d5772d7c914af470e0201` (= sealed proposal sha) |
| producer `oracle/assemble.py` (runner-reported) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| population (runner-reported) | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |
| truth seal (runner-reported) | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` |

`hashes-before.txt` and `hashes-after.txt` in the receipt directory are byte-identical; the selected tool never moved during measurement.

## Measurement (the only scanner run)

Authorized command, run once:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py \
  --case TimerRunAlias
```

Runner exit `0`, status `complete`, totals `1/1`, stderr empty. The runner validated the full population before and after: 57 input fixtures, 52 proposal files, 106 sealed source files, and the truth-seal digest. It then executed exactly one case. The scanner child ran under the runner's `RLIMIT_AS` 384 MiB and 15 s caps; child exit `1` (findings present), child stderr empty.

Actual scanner rows (`got_rows`) — exactly one:

| class | command | evidence |
|---|---|---|
| `package_query` | `pacman -Q r22-timer-run-alias` | `observed` |

Supporting payload facts: `observed_findings 1`, `lead_findings 0`, class counts `package_query 1` and every other class `0`, rule `pacman:-Q`. `files[0]` reports `eval_calls 1`, `eval_unparsed 0`, `unparsed_spawns 0`, and the sealed fixture sha. `unpermitted 1` is only the scan-mode convention when no `--permit` list is supplied (all findings are unpermitted); it is not an error.

Oracle comparison: `want == got_rows` as a complete multiset, `unparsed 0`, `pass true`, `reasons []`. This exact case has `accept_exact_want: null` and empty `forbid_observed_commands` / `forbid_commands_any_tier`, so there is no accepted-alternate or ban-list slack. `require_signal: true` is moot for the exact branch, which instead demands exact equality and zero unparsed counters.

Raw receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC148/result.json` (embeds the full runner stdout and stderr and all hashes), with `stdout.json`, `stderr.txt`, `exit.txt`, `hashes-before.txt`, `hashes-after.txt`.

## Independent semantic expectation (fixture + Python 3.14 semantics, not tool output)

The one source cell:

```python
import subprocess
import threading

def worker(argv):
    subprocess.run(argv)

timer = threading.Timer(0, worker, kwargs={"argv": ["pacman", "-Q", "r22-timer-run-alias"]})
timer.run()
```

1. `threading.Timer.__init__` (archived `threading-v3.14.8.py` lines 1370–1376) calls `Thread.__init__(self)` and then binds `self.function = function` (1373), `self.args = args if args is not None else []` (1374), `self.kwargs = kwargs if kwargs is not None else {}` (1375), `self.finished = Event()` (1376). The call supplies `interval=0`, `function=worker`, `args` omitted, `kwargs={"argv": [...]}`. So `self.function` is `worker`, `self.args` is `[]`, and `self.kwargs` is the literal dict.
2. `timer.run()` resolves to `Timer.run` (lines 1382–1386). The instance has no `run` attribute, `Timer` is not subclassed, and nothing monkeypatches the class.
3. `self.finished.wait(0)` goes through `Event.wait` (651–670) to `Condition.wait` (337–381). With `timeout = 0`, the branch `if timeout > 0` is false, so it performs `waiter.acquire(False)` on the freshly acquired waiter lock, which returns `False`. There is no other thread and no signal handler that could call `cancel()`, so `Event.is_set()` is `False`. The guard at 1384 passes.
4. `self.function(*self.args, **self.kwargs)` is `worker(argv=["pacman", "-Q", "r22-timer-run-alias"])`, which executes `subprocess.run(["pacman", "-Q", "r22-timer-run-alias"])` with no shell. `shlex.join` yields exactly `pacman -Q r22-timer-run-alias`, a read-only local package query.
5. No statement rebinds `worker`, `timer`, or the kwargs dict, and none mutates `timer.function`/`timer.kwargs`/`timer.args`. No exception path exists: the `Timer` and `worker` signatures accept the given arguments and the argv is a list of strings.

Independent total: exactly one `package_query` / `pacman -Q r22-timer-run-alias` / `observed` row and nothing else, with zero unparsed signals. The sealed want is therefore semantically correct, and the delivered tool's complete multiset matches it.

## Falsification attempts for this case

| attack | outcome |
|---|---|
| False observed/lead argv (invented or borrowed command) | Refuted. The only argv literal in the cell is the one bound at `Timer` construction; the row equals that literal, there is no lead row, and there is no same-named module literal that could be borrowed. |
| Lost true command | Refuted. `want` and `got_rows` are both exactly one row; nothing is missing or duplicated. |
| Wrong identity (`worker` vs. a def-name index or another callable) | Refuted for this fixture: the only callable is the sole `worker` def, bound as the positional `function` argument at construction, with no rebinding. Discriminative limit: because the fixture has exactly one `worker` and one `.run` path, this case alone cannot distinguish correct constructor-target capture from a coincidentally correct name lookup. The bound-method alias form (`run = timer.run; run()`) is the separate `TimerRunAliasActual` case, not this one, and was not measured here. |
| Lifetime (cancel, repeat, mutation, stale frame) | Refuted. One `Timer` instance is constructed and run once; there is no `cancel()`, no rebinding, no mutation; `wait(0)` cannot observe a flag set that no code path sets. A repeated `run()` would be skipped by `finished`, but no second run exists. |
| Conditional target | Refuted. The only conditional is `not self.finished.is_set()` at 1384, and the flag is provably false with interval `0`, no cancel, no other thread, and no signal handler. |
| Parsed-clean ambiguity | Refuted. One valid eval cell parsed (`eval_calls 1`), `eval_unparsed 0` and `unparsed_spawns 0`; the scanner exited `1` with a finding rather than reporting an error, and the runner recorded zero parse errors. The uncertainty counters are not masking silence. |
| Forbidden command at any tier / accepted alternate | Not applicable and not exploitable here: both ban lists are empty and `accept_exact_want` is `null`. |

Mechanism attribution, read from the delivered tool as data (`[INFERENCE]` because no instrumentation isolates the site): `assignment_binding`'s scheduled branch (around 1841–1855) captures `threading.Timer` with target from positional argument 2, `args` index 2, `kwargs` index 3; the attribute branch (around 1788–1792) maps `.run` on that scheduled binding to `scheduled_invoke`; `spawn_scan` (around 2470–2488) replays the invocation with a synthetic `<scheduled target>` carrying `mado_resolved` and literal keyword nodes; the helper `worker` is then followed with `argv` bound to the literal list and `subprocess.run` is classified. The refs sweep guard (around 2733–2734) skips the `Timer` target so the same body is not swept a second time as unresolved. Because the only `argv` literal is inside the `Timer` kwargs and there is no module-level `argv`, the emitted command can only have come through this scheduled-binding replay; `unparsed 0` shows no unresolved fallback produced it.

## Uncertainty boundaries and scope

- This is **1 of 57** frozen cases. Full population integrity was validated but not executed: the other 49 eligible proposals and all 7 supplemental originals remain unmeasured in this receipt (50 eligible proposals + 7 originals = 57; `--case` selected one).
- `TimerRunAlias` is an eligible proposal but is **not** one of the three required proposals (`TimerRunAliasActual`, `CapturePartialGlobalLateActual`, `CaptureNestedFactory`). Its green cannot satisfy the required-proposal guard on its own.
- Not exercised: `Thread.run`, `Timer.cancel()`, repeated `run()`, a factory closure as timer target, the bound-method alias `run = timer.run`, multiple same-factory instances, multi-cell persistence, dynamic starred/`**` arguments, and partial-wrapped targets.
- This single agreement is not a semantics proof of the detector's general scheduled-call implementation, and it does not adjudicate the F4 family as a whole (the original reds were not rerun with any old tool).
- Out of scope and untouched: the 175-case historical guard, the entire 1356-fixture removal/error comparison, resource populations, the C2 artifact audit, and prior r19/r20/r21 rejected-harmed receipts and streak.
- No production, fixture, expected, proposal, gate, registry, or documentation file was edited. No installs, no extra scanner runs, no old-tool executions, no C2 execution. The only scanner child was the one spawned by the authorized runner invocation.
- LSP device unavailability: `xd://lsp` is not mounted in this session (`No such tool: xd://lsp`). Definitions and call sites were therefore read directly at exact line ranges in the archived CPython source and the tool source, not inferred from name-only search. No server result is claimed.

Report: .ufo/waves/round-22/w2/reports/FalsifyC148.md
Rendered absolute path: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC148.md
