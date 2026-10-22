# CritScheduledNeighbour — C1 scheduled/thread neighbours of the frame rule

Verdict: **3/3 new fixtures are base-false-observed.** In every case the base classifier
(`tools/mado-tripwire.py`, sha256 `cd9da20c…ea84`) reports the shadowing frame's
`pacman -S …-foreign` as an **observed host_mutation** row and has no row for the
`pacman -Q …-global` argv that actually executes. The frame leak the repair set targets also
reaches the `threading.Thread`/`threading.Timer` scheduled path, and none of the 12 frozen
cases or the round-20/21 Thread fixtures exercise that path from a shadowing frame.

## Fixtures (all in `.ufo/waves/round-23/w1/out/CritScheduledNeighbour/fixtures/`)

| id | shape | sha256 | executed (truth) | base rows | label |
|---|---|---|---|---|---|
| ThreadTargetReadsShadowedGlobal | `starter()` assigns local `argv`, then `threading.Thread(target=helper).start(); .join()`; `helper` runs global `argv` | `1656f77148ae88ea306ebe4053f48d96cc50dec01495990019acecfd699f29e7` | `pacman -Q r23w1-thread-global` | `host_mutation pacman -S r23w1-thread-foreign observed` | base-false-observed |
| TimerFunctionReadsShadowedGlobal | `schedule(argv)` parameter shadows global; `threading.Timer(0, helper).start(); .join()` | `d7c54dd01791cab4925779dc1d3fdf05e7c90223e09772cdfa323301843862c8` | `pacman -Q r23w1-timer-global` | `host_mutation pacman -S r23w1-timer-foreign observed` | base-false-observed |
| ThreadRunFromForwarder | module `worker = threading.Thread(target=helper)`; `forward(argv, job): job.run()` called with a foreign argv | `a95509b65c8ece18ea7d918b6be376831af5eef11776b21f883c72d9a9fb2aba` | `pacman -Q r23w1-run-global` | `host_mutation pacman -S r23w1-run-foreign observed` | base-false-observed |

All three: scanner exit 1, no error, `eval_unparsed` 0, `unparsed_spawns` 0, repair-set exact
rule fails. `cases.json` holds per case the fixture sha256, the truth, a ready-to-use exact
expectation (`want` = executed argv as observed, `forbid_any` = the fixture's string-list argv
literals that never executed) and the full base result.

## Method and commands (all from the out dir unless noted)

1. `python3 -I author.py` writes the three fixtures in the repair-set JSONL shape (one assistant
   `toolCall` record, `name` eval, `language` py, `reset` false, `json.dumps` default separators,
   trailing newline).
2. `python3 -I truth.py fixtures/*.jsonl` → `truth-receipt.json`, exit 0. `truth.py` copies
   `repair/truth.py`'s CHILD byte-for-byte (recording fake `subprocess` in a `-I -S` child); real
   `threading` runs the target, the fake only records argv. Nothing real was spawned.
3. `python3 -I cases.py` → `cases.json`, exit 0. It extracts base bytes with
   `git show a28e4815…:tools/mado-tripwire.py` to a temp dir, refuses them unless sha256 is
   `cd9da20c…ea84` (checked again after the runs), scans each fixture through `scan` from
   `round-21/oracle/measure.py` (runpy; one `python3 -I` child, 384 MiB, 15 s), and judges with
   `judge` loaded from `round-23/repair/measure.py`, so the pass rule is the repair set's own.
4. Controls:
   - My `truth.py` over the 12 frozen repair fixtures agrees with `evidence/repair-truth.json`
     on 12/12 executed sets (`control-truth-frozen12.json`).
   - `python3 -I .ufo/waves/round-23/repair/measure.py --tool <base extracted from a28e4815>` (lane
     root) gives **6/12**, matching the registered before value (`control-repair-measure-base.json`).

## Deviation from the item text (declared)

The item says "imports only subprocess", but it also asks for `threading.Thread`/`Timer`, which is
impossible without importing `threading` (the safety gate also bans `getattr`/`__import__`). The
fixtures import exactly `subprocess` and `threading`. My `truth.py` gate admits only those two
imports (no `from`-imports, no `as` aliases), only `subprocess.run`, `threading.Thread` and
`threading.Timer` attributes, and only list or name arguments to `subprocess.run`. The round-21
oracle inputs (`CallbackGlobal`, `ThreadInline`, `CallbackBoundArgs`) already import `threading`,
so this matches an existing lane shape. Consequence: the frozen `repair/truth.py` would reject
these fixtures as `unsafe_fixture`. Use `truth.py` in this out dir as their truth runner.

## Counterexample mechanism (code reading of base)

- When `threading.Thread(...)`/`threading.Timer(...)` is constructed, it binds a `scheduled` record
  whose `target` is resolved at the construction site (`assignment_binding`, around line 1843).
- `.start()`/`.run()` on that record becomes `scheduled_invoke` (around line 1791). `spawn_scan`
  then builds a synthetic call to `<scheduled target>` and rescans it with the **call-site**
  `cenv`/`cbindings` (around lines 2477–2493). That call goes through the same `helper` branch and
  `follow_helper(helper, bound_node, cenv, cbindings, …)` as a plain call (around line 2569).
- So the helper's free name `argv` resolves in the frame of whoever calls `.start()`/`.run()`. That
  frame is the starter (`ThreadTargetReadsShadowedGlobal`, `TimerFunctionReadsShadowedGlobal`) or
  the forwarder (`ThreadRunFromForwarder`), not the module globals that Python uses.
- The existing Thread guards (round-21 oracle `CallbackGlobal`, `ThreadInline`, `CallbackBoundArgs`;
  round-20 `ar11`–`ar15`, `ar50`) all call `.start()` at module scope, where the call-site frame and
  the defining frame are the same. That is why the leak never showed up there.

## Impacted axes

- **Operability (C1):** a read-only `pacman -Q` is reported as an observed host mutation of a
  package that is never installed, and the real query is missed. This is the same harm class as
  the H4 frame leak, on a path the 12-case counter does not measure.
- **Precision guard risk:** a candidate that reaches 12/12 could still leave this path leaking.

## Smallest safe correction (advice to the L1)

The fix should go where free names in a followed helper body are resolved, which the plain and
scheduled paths share. A non-closure target should resolve free names against module globals at
call time; a closure target should use its captured `closure_env`. Construction-time `args`/`kwargs`
should stay as they are: those are evaluated in the starter frame, which is correct.

[INFERENCE] A candidate that repairs only the plain call site, for example by special-casing a
forwarder's parameter or a caller local when the callee is an `ast.Name`, would not cover these
cases. The scheduled path's callee is the synthetic `<scheduled target>` name with a
`mado_resolved` binding.

Wave-2 attack recommendation: run `cases.py`'s judge against the candidate, or add the
`expectation` blocks from `cases.json`. All three must turn exact-pass. The round-21 oracle
`CallbackGlobal`/`CallbackBoundArgs` must stay passing as the module-scope guard.

Not authored, because the item caps this at three: an overcorrection guard
`Thread(target=helper, args=(argv,))` started from a shadowing frame, where the truth is the
starter's local. A candidate that over-applies "defining frame" to construction-time args would
regress there.

## Files written

Only `.ufo/waves/round-23/w1/out/CritScheduledNeighbour/` (`author.py`, `truth.py`, `cases.py`,
`fixtures/*.jsonl`, `truth-receipt.json`, `cases.json`, `control-truth-frozen12.json`,
`control-repair-measure-base.json`) and this report. No lane git or jj state was touched. A temp
copy of the base classifier went to `/tmp` and was removed. No tools were installed or updated.
