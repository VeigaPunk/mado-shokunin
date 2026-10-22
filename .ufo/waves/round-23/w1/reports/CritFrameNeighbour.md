# CritFrameNeighbour — C1 caller-frame leak neighbours (wave 1, discovery outside the counter)

Verdict: **3/3 new neighbour fixtures are base-false-observed.** In each one, the base classifier
(`tools/mado-tripwire.py` sha256 `cd9da20c…ea84` at `a28e4815`) reports the foreign caller-frame argv
as an `observed` `host_mutation`. The executed global `pacman -Q` argv gets no row at any tier.
This is the H4 / `CallerLocalShadowsHelperGlobal` leak again, reached through a method, a lambda,
and a decorator wrapper instead of a plain `def` caller.

## What I did

1. Authored three inert fixtures in the repair-set JSONL shape. Each is one `eval` toolCall record,
   imports only `subprocess`, and calls only `subprocess.run` with a name. The fixtures are generated
   by `out/CritFrameNeighbour/author.py`. Every fixture passes the same `safe()` gate as `truth.py`.
2. Derived truth mechanically. `out/CritFrameNeighbour/measure.py` carries the `CHILD` runner copied
   from `round-23/repair/truth.py`; a check compared the two `CHILD` strings and they are byte-identical
   (`CHILD identical: True`). It runs the code with a recording fake `subprocess` in
   `python3 -I -S`. No real subprocess was run by fixture code. `forbid_any` is every literal argv in
   the fixture that did not execute.
3. Ran the base classifier through the unchanged round-21 oracle helper: `runpy` of
   `.ufo/waves/round-21/oracle/measure.py` (sha256 `4eb893d2…2da`), then `scan`. That runs one
   `python3 -I` child per fixture, capped at 384 MiB and 15 s. The base bytes are
   `git show a28e4815…:tools/mado-tripwire.py`, extracted to `out/CritFrameNeighbour/base-mado-tripwire.py`.
   After the run, `measure.py` re-checked the sha256 of both the tool and the helper.

Commands (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`, `D=.ufo/waves/round-23/w1/out/CritFrameNeighbour`):

    git show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py > $D/base-mado-tripwire.py
    python3 -I $D/author.py
    python3 -I $D/measure.py --tool $D/base-mado-tripwire.py     # exit 0, writes $D/cases.json

Python 3.14.8. No installs or updates.

## Results (receipt: `out/CritFrameNeighbour/cases.json`, sha256 `ee344b53…eea`)

| Case | Fixture sha256 | Executed (truth) | Forbid | Base rows | Unparsed | Verdict |
|---|---|---|---|---|---|---|
| HelperCalledFromMethod | `9150bf78…9de6` | `pacman -Q r23cf-method-global` | `pacman -S r23cf-method-foreign` | `host_mutation pacman -S r23cf-method-foreign observed` | 0 | base-false-observed |
| HelperCalledFromLambda | `332b4731…e727d` | `pacman -Q r23cf-lambda-global` | `pacman -S r23cf-lambda-foreign` | `host_mutation pacman -S r23cf-lambda-foreign observed` | 0 | base-false-observed |
| DecoratorWrapperCallsWrapped | `fd074be4…bedee` | `pacman -Q r23cf-deco-global` | `pacman -S r23cf-deco-foreign` | `host_mutation pacman -S r23cf-deco-foreign observed` | 0 | base-false-observed |

The scanner exited 1 with no error in every case. Each base result has two defects: a forbidden
command shows up at the `observed` tier, and the true command is silently missed.

Fixture shapes, with the global `argv = ["pacman","-Q",…]` and helper `def run(): subprocess.run(argv)`
shared by all three:

- **Method:** `class Runner: def go(self, argv): run()`; `Runner().go([…"-S"…])`.
- **Lambda:** `fire = lambda argv: run()`; `fire([…"-S"…])`.
- **Decorator:** `def wrap(fn): def inner(argv): fn(); return inner`; `@wrap def run(): …`; `run([…"-S"…])`.
  Python rebinds `run` to `inner`, and `inner` calls the original `run` without arguments.

Not authored: `functools.partial`. A partial needs `import functools`, which breaks the
"imports only subprocess" rule and would fail `truth.py`'s `safe()` check. A hand-rolled partial is
just a factory closure, which `ForwarderInvokesFactoryClosure` already covers.

## Counterexample and mechanism (critic view)

In `follow_helper` (base lines 2409–2446), the helper body inherits the caller's frame:
`body_bindings = dict(cbindings)` and `body_env = dict(cenv)`. Only then are the closure overlay and
the bound parameters applied. Python resolves a helper's free names lexically: first its definition
scope, then module globals at call time. It does not resolve them through the caller. So any caller
frame that binds the helper's free name (a method parameter, a lambda parameter, or a decorator
wrapper parameter) replaces the global, and the scanner marks the result `observed`.

Impacted axes:

- **Operability (C1):** these are false `observed` host mutations, the same harm class as H4.
- **Precision guard:** a fix limited to the `def`-caller shape would leave all three red.

## Smallest safe correction (advice only; the L1 judges)

Seed `body_env` and `body_bindings` in `follow_helper` from the helper's lexical scope instead of
`cenv`/`cbindings`. That scope is the module-level env and bindings as of the call (which keeps
`LateGlobalRebinding` green), plus `closure_env`/`closure_bindings` for nested defs (which keeps
`NestedDefReadsDefiningFrame` and `ForwarderInvokesFactoryClosure` green), plus the bound parameters.
Apply the same seeding on every descent path: plain call, method call (`skip_first`/`class_node`),
lambda helper (`ast.Lambda` body), and a decorated name rebound to the wrapper's inner function.

Overcorrection traps a candidate MUST avoid, all checkable with these fixtures plus the 12-case set:

- Dropping the foreign row without restoring the global value turns each case into
  base-silent-miss. The exact rule still needs the `pacman -Q … observed` row.
- Treating the decorated `run(…)` as a call to the undecorated `run` gives one argument against zero
  parameters. `bind_literal` then returns `None`, the helper is not followed, and the case
  becomes silent or unparsed.
- Stripping all caller names would break `ForwarderPassesCallerArgument`, where the caller's value
  arrives as an explicit argument.

## Files (all under `.ufo/waves/round-23/w1/out/CritFrameNeighbour/`)

- `fixtures/HelperCalledFromMethod.jsonl`, `fixtures/HelperCalledFromLambda.jsonl`, `fixtures/DecoratorWrapperCallsWrapped.jsonl`
- `author.py` (sha256 `7801cb23…6fec`), `measure.py` (sha256 `5dd070a2…9637`)
- `base-mado-tripwire.py` (base bytes, sha256 `cd9da20c…ea84`)
- `cases.json` (fixture sha256, truth, base rows and unparsed counts, verdict)

Wave-2 use: `python3 -I $D/measure.py --tool <candidate tripwire>` re-derives truth and scans the
candidate. Any verdict other than `base-correct` means the candidate still fails this neighbour
(the verdict labels keep the `base-` prefix even when the scanned tool is a candidate).

Verdict: base-false-observed on 3/3 (method, lambda, decorator wrapper); partial not authorable under the import rule.
