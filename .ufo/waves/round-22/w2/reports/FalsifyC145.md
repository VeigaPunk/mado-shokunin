# FalsifyC145 — C1 ThreadRunHygiene

## Verdict

**Agree, for this exact sealed case only.** The complete expected class/command/evidence multiset is one `package_query` row for `pacman -Q r22-runhyg` at `observed`, with zero `eval_unparsed`/`unparsed_spawns`; the single authorized measurement produced exactly that multiset, zero error counters, and no forbidden command. No false observed/lead argv, lost true command, wrong callable identity, lifetime misbinding, conditional-target overclaim, or parsed-clean ambiguity was found in this case.

This is author-lane advisory falsification evidence. It is **not** non-author admission, does not close C1, does not reverse the r19/r20/r21 rejected-harmed receipts or the rejection streak, and does not transfer L1 planner/integration authority. No admission is granted.

## Independent semantic expectation (not derived from the green result)

Proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadRunHygiene.json:1-19`, sha256 `48b8b9f64a2b3ff3eabbee703a1b0fcd50f6cf27800ba3a68d48d8ca09ce0044`. Sealed case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`, id `ThreadRunHygiene`; one cell, `reset: false`, `expected_kind: exact`, `want_input_order` equals `want`, `accept_exact_want: null`, `require_signal: true`, `forbid_observed_commands: ["pacman -S r22-runhyg"]`, `forbid_commands_any_tier: []`. Fixture: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/ThreadRunHygiene.jsonl` (the runner's `inputs/` is oracle-relative), sha256 `970e172c89d643e0f418a5cda272c53fb3a9ac26b856382b0bb47bfb78bd4a58`.

Source:

```python
import subprocess
import threading


__mado_thread_target__ = subprocess.run


def worker():
    __mado_thread_target__(["pacman", "-Q", "r22-runhyg"])


t = threading.Thread(target=worker)
t.run()
```

1. **Execution path.** Module top level executes in order: imports, the global assignment, the function definition, the Thread construction, then `t.run()`. Nothing branches around those statements. `t` is a plain `threading.Thread` instance, not a subclass and not rebound. `Thread.__init__` stores `self._target = target` at `/usr/lib/python3.14/threading.py:925`; `t.run()` calls `Thread.run` at `:1013`, which invokes `self._target(*self._args, **self._kwargs)` at `:1024` synchronously in the caller's thread. The stored target is `worker` (non-`None`), `_args == ()`, `_kwargs == {}`, and `worker` accepts no arguments, so the invocation is reached.
2. **Name identity.** Inside `worker`, `__mado_thread_target__` has no local binding (no parameter, assignment, import, loop/with/except target, or global/nonlocal declaration). It is therefore a global load under LEGB and resolves to the module-level assignment, made before `t.run()`. Executed at module scope, the name is not class-mangled. Its value is the real `subprocess.run`, not a scanner-injected target. The fixture deliberately reuses the spelling of r21's reserved injection key as a *legal source global*.
3. **Command.** The reached call is `subprocess.run(["pacman", "-Q", "r22-runhyg"])`, shell `False`, a literal argv list. The command string is exactly `pacman -Q r22-runhyg`. `pacman -Q` is a query operation (`classify_pacman` maps `Q`, `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:738-772`), so the class is `package_query`.
4. **Evidence tier.** The call is unconditionally reached by straight-line module execution plus the known `Thread.run` body. `Thread.run`'s only guard is `self._target is not None`, which is statically known true from the constructor argument. This is not an unknown conditional or an unresolved callback; it is the exact `run`-on-constructed-Thread form declared in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md`. `observed` is therefore semantically justified, not a lead promoted by the detector.
5. **Completeness.** The only spawn call on the executed path is the one above. The assignment `__mado_thread_target__ = subprocess.run` merely loads a callable; the Thread constructor, imports, and `def worker` are not commands; `worker` is invoked exactly once, by the single `t.run()`. Complete expected multiset: `[{"class":"package_query","command":"pacman -Q r22-runhyg","evidence":"observed"}]`; zero error counters; forbidden `pacman -S r22-runhyg` absent at every tier (its observed-only exclusion is stricter than needed because an exact multiset would reject an extra row anyway).

This case is an exact-result claim, not an uncertainty claim. No alternate `accept_exact_want` exists; a lead row or any positive error counter would fail by construction. The expectation does not borrow an observation from a dynamic star/double-star argument, a stale pre-mutation command, or an opaque callback.

## Sole authorized measurement and actual rows

Executed exactly once, with no retry and no extra scanner run:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case ThreadRunHygiene
```

| Quantity | Actual |
| --- | --- |
| Runner status / OS exit | `complete` / `0` |
| Cases executed | `1` (`ThreadRunHygiene` only); totals `1/1`, `pass: true`, `reasons: []` |
| Scanner argv | `/usr/bin/python3 -I -c <importlib wrapper> /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/ThreadRunHygiene.jsonl` |
| Scanner OS exit / scanner error | `1` / `null` |
| Complete class/command/evidence rows | `[{"class":"package_query","command":"pacman -Q r22-runhyg","evidence":"observed"}]` |
| Observed / lead findings | `1 / 0` |
| `eval_unparsed` / `unparsed_spawns` | `0 / 0` |
| Scanner counts | `package_query: 1`; all other classes `0` |
| File row | one file, exact selected fixture path, sha256 `970e172c...bd4a58`, `lines: 1`, `eval_calls: 1`, `bash_calls: 0` |
| Forbidden argv | `pacman -S r22-runhyg` absent at all tiers |
| Runner stderr / scanner stderr | empty / empty |
| Integrity errors / before-after drift | `[]` / none |
| Population validated (not run) | 106 sealed sources, 52 proposal files, 57 input fixtures; population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

The runner's population check is integrity validation, **not** 57 semantic passes. Its `RLIMIT_AS` cap is 384 MiB and its timeout 15 s at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661`; one scanner child was used.

## Falsification attempts against the named failure modes

- **False observed or lead argv accepted as observed.** The observed row is not a `callback_argv_leads`/`sweep_body` lead: leads carry the `lead` marker, and the payload reports `lead_findings: 0`. The row comes from following the scheduled target with its empty stored arguments (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2467-2485`), entering the visible `worker` helper, and classifying the literal `subprocess.run` argument. Its `rule: pacman:-Q` and `argv0: pacman` identify the actual inner call, not the injected-key spelling.
- **Lost true command.** The only true executed command is present exactly once with exact spelling and class. No command was displaced to a different class, quoting, or tier. The Thread constructor and the callable assignment do not execute a command.
- **Wrong callable identity / F5 reserved key.** The current tool contains no `__mado_...` reserved key at all; the source global is resolved from the ordinary module binding. Synthetic callable metadata is attached to AST nodes as `mado_resolved` on identifiers `<captured argument>` (`:1422-1424`) and `<scheduled target>` (`:2480-2481`). Those strings are not legal Python identifiers and are never inserted as source-binding keys. A structural review of every `bindings[...] =` write (`:1885-1987`, `:2230`, `:2374`) shows keys derive only from source identifiers: function/class names, import aliases, assignment target names, and callable parameter names. The old reserved key was not renamed to another legal identifier; the metadata is carried on the synthetic node. This satisfies the F5 structural requirement for this mechanism, not merely this fixture's green.
- **Lifetime / capture boundary.** `assignment_binding` identifies the `threading.Thread` constructor and stores `target` info resolved at construction (`:1841-1852`). `statement_snapshot` retains the syntactically reachable names of the `t.run()` statement, including the stored target's node and the global `__mado_thread_target__` binding (`:2163-2201`); `follow_helper` then binds the empty invocation and scans the worker body (`:2407-2445`). The callable is followed at its construction-time identity rather than by a later def-name lookup. Here there is no rebinding of `worker`, `t`, `threading`, `subprocess`, or the global key after construction, so no stale or crossed frame is possible.
- **Conditional target.** The only conditional in the path is `if self._target is not None` inside `Thread.run`, and `target=worker` makes it true. No source-level `if`/`try`/loop guards `t.run()`. Treating this as `observed` does not claim knowledge of an arbitrary concurrent schedule; `run()` is synchronous here and `start()` is not used. A subclass overriding `run` or a runtime monkeypatch would fall outside the declared exact form, and neither is present.
- **Parsed-clean ambiguity.** Scanner exit `1` is the findings verdict and is explicitly allowed by the runner; it is not an error-bearing scan accepted as clean. `scanner_error` is `null`, the single file row has the sealed digest and exact path, both unparsed counters are `0`, and the runner reports no parse reasons. `status: complete` with `integrity_errors: []` and identical before/after integrity records distinguishes this from an error-masked clean.
- **`accept_exact_want` versus true uncertainty.** The case is `expected_kind: exact` with `accept_exact_want: null`; the runner's exact branch requires full multiset equality and zero unparsed (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-760`). The green is therefore exact agreement, not an uncertain fallback acceptance. There is no unknown-case any-tier forbidden-argv obligation to evaluate here; the mutation command is separately absent.

## Scope, confidence, and residual unknowns

- **Confidence:** high for this case's static expectation and for the measured row. The CPython 3.14.8 source lines cited by the proposal were verified at the installed path (`925`, `1013`, `1024`), and the measured result matches the independently reconstructed multiset.
- **Scope:** one frozen case on the delivered C1 tool sha256 `36fdc459...badce`, at delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. This does not establish the other 56 oracle cases, C2 artifact-audit calibration, the 175-case historical suite, the 1356-fixture removal/error comparison, resource-closure bounds, mutation kill status, or any universal lifetime/scheduling claim.
- **Evidence-tier boundary:** `observed` here denotes a statically certain spawn **call site**. It does not prove that a `pacman` binary exists or that the query succeeds; the class is derived from argv. This is the established detector convention (the original F4 direct-`subprocess.run` expectation also uses `observed`), not a per-case contradiction.
- **Version boundary:** the exact expectation depends on standard `threading.Thread` retaining construction-bound `_target` and synchronous `run` semantics. The installed CPython 3.14.8 matches the citation; a different runtime could invalidate the frozen semantic premise and would require a new pre-seal truth, not normalization of this one.
- **Structural boundary:** the F5 review above covers the binding-namespace mechanism in the selected tool. It does not prove that every possible legal source identifier is collision-free in every code path; it establishes that synthetic callable metadata is not stored under a legal identifier in the source binding namespace and that this case's source global resolves normally.
- **Tooling boundary:** no LSP server is exposed to this seat, so definitions/references were read from the cited source lines and the delivered tool; literal grep was used only to locate code, not as semantic absence proof. No fixture code or printed command was executed. No old tool was rerun. No build, lint, formatter, full-suite test, generic smoke, live probe, install, or extra source-shaped probe was performed.

## Identity evidence

Every digest below was checked before and after the sole run; no drift.

| Artifact | SHA-256 |
| --- | --- |
| Selected C1 tool (`tools/mado-tripwire.py`) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Oracle expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Oracle pin file | `7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6` |
| Runner (`measure.py`) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Producer (`assemble.py`) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| ThreadRunHygiene fixture | `970e172c89d643e0f418a5cda272c53fb3a9ac26b856382b0bb47bfb78bd4a58` |
| ThreadRunHygiene proposal | `48b8b9f64a2b3ff3eabbee703a1b0fcd50f6cf27800ba3a68d48d8ca09ce0044` |
| Raw truth seal | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` |

The C2 audit expected digest `b5df74b5...fd09` is outside this C1 case measurement and was not used to derive this verdict. Production, fixtures, expectation bytes, tools, and shared documentation were read-only. Only this report and the uniquely named receipt directory were written. No tool was installed or updated.

Raw outer/scanner argv, exits, stdout, stderr, complete scanner payload, expected-case fields, and before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC145/result.json` (with raw `measure.stdout`, `measure.stderr`, and `measure.exit`).

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC145.md
