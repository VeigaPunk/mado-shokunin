# TypingCast attack — round 21 C1

## Axes and tested artifact

Axes: (1) semantic correctness of the frozen TypingCast expectation; (2) whether the scanner rule generalizes by program shape rather than fixture text; (3) whether one nearby identity-preserving invocation exposes a gap.

Reviewed current `HEAD` **f499a8db7171b7476fe9f204ab9edbac5a956fa9**. Current `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` SHA-256: **2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d**. The `2ac0f9b..f499a8d` diff changes general callable/binding and eager-reference handling; it contains no TypingCast fixture-name special case.

## Frozen expectation: warranted

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json` records TypingCast with fixture `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/TypingCast.jsonl`, SHA-256 `fd01b87796c24961eef7009e178973766d76208dc88499489b8adccda71d30b9`, and `want: []`. The W1 proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/TypingCast.json` (proposal SHA-256 `25e9d75e3387dcc218eb2d5f87b3294f0b7c0a98f9ecf8e6f612251067fefd83`). Its program defines `f` with `subprocess.run(["pacman", "-Q", "hyprland"])`, then evaluates `typing.cast(object, f)` and discards the result. The function body is deferred; the bare `f` is passed as a value, not invoked. Python's documented `typing.cast(typ, val)` returns `val` unchanged ([Python typing documentation](https://docs.python.org/3/library/typing.html#typing.cast)), so this call neither runs the function nor produces a package-query command. The empty expected findings are semantically correct; no class, command, or evidence row is warranted.

## Generality of the current rule

The scanner reaches this result through generic binding and purity logic, not fixture text: `update_bindings` records imports as module bindings (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1730-1735`); `callable_info` resolves imported paths and delegates standard-library purity to `pure_stdlib_path` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1641-1651`, `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1527-1537`); and the reference pass skips a function value passed to a pure call (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2386-2393`). There is no `TypingCast` special case in the scanner. The current source therefore handles the frozen value-only shape generically for an unshadowed `typing.cast` import.

The existing `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` is historical rather than current: its `measured_commit` is `843d301d1b17af78427918f7845af336b2218de0` and its tool SHA is `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, both different from this reviewed revision. I did not use it as evidence for current behavior.

## Nearby falsification probe — actionable evidence downgrade

I created one inert two-cell JSONL fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkTypingCast-2/typing-cast-call.jsonl` (SHA-256 `529f8712c7a21ecfb6dad87dc2ac0dbdfeea97cf365338645b5a0658ea4389ca`). Cell 1 repeats the frozen code; cell 2 changes only the use to `typing.cast(typing.Callable, f)()`, with the same visible function body. Both cells reset independently. The JSONL stores transcript-shaped input only; the Python text was not executed. I ran only the existing `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py` `scan` API via `runpy`; that API launches one scanner child with `RLIMIT_AS=384 MiB` and a 15-second timeout.

Observed scanner result: `exit=1`, `eval_calls=2`, `eval_unparsed=0`, `package_query=1`; the sole finding is `class=package_query`, `command="pacman -Q hyprland"`, `evidence=lead`, `line=2`, `tool_call_id="TypingCastInvoke-0"`. There is no finding for cell 1, so the current tool still gives the frozen shape its empty result.

**Medium — a definite call through `typing.cast` is downgraded to `lead`.** In cell 2, `typing.cast` returns `f` unchanged and the trailing `()` immediately invokes it; `f` has no parameters and the call site supplies none. This is a definite reached call and should be `observed` under the scanner's stated rule that visible helpers called with bound arguments are followed (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:38-45`). The scanner retains the right class and command, so this is an evidence-strength defect, not a missed command. The source path is consistent with the downgrade: `eager_calls` tags nodes inside a non-name/non-attribute callee as `invoke` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1850-1852`); callable references then fall through to `sweep_body` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2433-2437`), which labels swept findings `lead` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2106-2113`). The result-return relation from known identity function `typing.cast` is not carried into that call.

## Residual risk and verification gaps

- This is one targeted nearby variant, not a general proof over aliases, wrappers, or all callable-returning pure APIs.
- The LSP device is not mounted (`read xd://lsp` returned “No such tool” and listed the mounted devices without LSP). I used targeted source reads; grep was navigation only, not semantic proof. No LSP references/definition/diagnostics were available.
- I did not run the corpus or full suite; L1 owns final verification. No tool was installed or updated.

## Verdict

Accept TypingCast's frozen `want: []`; do not change the expectation. The underlying shape handling is generic rather than fixture-keyed. Retain the nearby `typing.cast(..., f)()` evidence downgrade as an actionable scoped counterexample for L1's assessment.

Report: `.ufo/waves/round-21/w2/reports/AtkTypingCast.md`
