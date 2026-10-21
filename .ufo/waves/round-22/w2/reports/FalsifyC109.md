# FalsifyC109 — CX9UnknownKeyword

## Verdict and findings by severity

**Verdict: agree, limited to the exact sealed case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. No actionable defect found in this case.** This is author-lane advisory evidence, not a non-author admission, clearance, integration decision, or reset of the prior r19/r20/r21 rejected-harmed receipts and streak.

The single authorized measurement returned the complete expected empty class/command/evidence multiset, with zero parser/unparsed counters. Neither decoy command appeared as observed **or** lead. The conclusion rests on independent call-binding reasoning and the relevant changed implementation paths below, not on the green banner alone.

## Axes

1. **Command truth and recall:** complete reachable-command multiset, with neither invented argv nor a lost real command.
2. **Callable identity and lifetime:** an invalid factory invocation must not create a closure or borrow a same-named module binding.
3. **Evidence and uncertainty calibration:** distinguish a definitely rejected call from an unresolved valid call; do not relabel fabricated argv as lead or treat parsed-clean as successful evaluation.
4. **Artifact and measurement integrity:** same delivered scanner identity, frozen proposal/input/expectation, one capped scanner child, and honest one-case coverage.

## Independent expected semantics and provenance

The original proposal is [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX9UnknownKeyword.json:3-17](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX9UnknownKeyword.json#L3). Its source cell is retained verbatim in the inert fixture [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX9UnknownKeyword.jsonl:1](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX9UnknownKeyword.jsonl#L1).

Static reasoning, without executing the payload:

- `make` has exactly one required formal parameter, `argv`, and no `**kwargs` or defaults. Its returned `run` would close over that parameter if a valid invocation reached the body.
- The call supplies only the explicit keyword `argvv`. That name cannot bind `argv`, and the required `argv` slot is also unfilled. Argument binding therefore raises `TypeError` before the factory body runs.
- Evaluating the keyword's literal list does not run a command. The earlier import, function definition, and module literal assignment likewise do not invoke either printed package-query command. “Nothing executes” in the proposal must be understood as **no command executes**, not as a claim that no preceding Python statement is evaluated.
- The inner function is not created by this invocation, the assignment to `runner` never completes in Python, and the final `runner()` is not reached. There is no captured lifetime, conditional target, scheduled callback, or alternative command to reconstruct in this case.
- Thus the complete expected multiset is `[]`, not a subset assertion. Both `pacman -Q r22-cx9-global` and `pacman -Q r22-cx9-passed` are forbidden at **every** evidence tier. The global `argv` is not a fallback parameter binding; the misnamed argument value is not an invoked argv.

The selected sealed entry is exact, with `want: []`, `accept_exact_want: null`, `require_signal: false`, no correction, and no addenda: [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:438-484](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json#L438). The filename's word “Unknown” does not make this an uncertain binding: there is no dynamic `*`/`**` expansion or unresolved argument identity here. Requiring a lead/unparsed signal would manufacture uncertainty for a provable pre-body rejection. This matches the predeclared invalid-call rule in [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:15-22](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md#L15).

The earlier scope seed called CX9 `uncertain` with `require_signal: false`, while also noting `TypeError at make(); runner never bound`: [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/CriticScope.json:183-191](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/CriticScope.json#L183). That wording difference is preserved here, not normalized away. The original independent case proposal itself already says exact empty; the measured expectation did not change that proposal to accommodate output. Its Python 3.14 “Calls” language-reference citation is by section name, explicitly not retained source bytes; this seat does not claim a separately authenticated language-document excerpt.

The original r21 F2 authority remains [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:78-83](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md#L78): a failed binding could previously leave the invocation environment unchanged and fabricate a module-global command. Its original dynamic-expansion red is not the same semantic case as this definitely invalid keyword call. No old scanner or original red was rerun.

## Relevant diff and current call-path review

Reviewed the actual read-only scanner diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to the delivered revision, focused on the F2 factory/binding/invocation changes. The old `capture_owner`/`capture_call` fallback was removed in favor of factory-result resolution. Relevant current paths are:

1. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2105-2143](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2105): `bind_literal` has `argv` in `keyword_params`, no `kwarg`, and returns `None` for the explicit unknown keyword `argvv`.
2. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1629-1656](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1629): `binding_failure` sees no unresolved starred expansion and classifies that failed binding as `invalid`. `factory_result` returns the invalid marker **before** constructing local environments, replaying the factory prefix, or resolving the returned helper.
3. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1757-1783](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1757) and [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1859-1861](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1859): callable and assignment resolution retain the invalid result instead of inventing a returned closure. The later analysis binding for `runner` is an invalid sentinel, not a claim that Python completed the assignment.
4. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2564-2567](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2564): the direct `make(...)` call also rejects definite invalid binding before `follow_helper`, marking its callee resolved rather than sweeping its body as a lead. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2461-2466](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2461) skips the invalid sentinel on `runner()`.
5. [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2051-2058](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2051) excludes deferred function bodies from eager traversal. The reference sweep's resolved-callee exclusion and helper-only sweep at [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2685-2687,2738-2742](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2685) do not reintroduce either command as a lead.

These paths explain why neither decoy can be borrowed from the global environment or the keyword value. The AST-only compilation boundary is explicit at [/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280-2293](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2280). The payload and its printed commands were never executed.

LSP availability: attempting to read `xd://lsp` returned `No such tool`. No LSP status, references, definition, or diagnostics service was available. Literal searches were used only to locate the directly reviewed source; they are not presented as semantic reference proof.

## Authorized measurement and actual rows

Exactly one invocation of:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX9UnknownKeyword
```

The runner selects one case only after population validation, at [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-839](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L789). Its scanner subprocess enforces `RLIMIT_AS = 402653184` bytes (384 MiB) and 15 seconds: [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L643). The selected tool argument, resolved tool path, and child argv name the same absolute file; its working-tree hash equals the delivered Git blob hash. No alternate scanner, stand-in, reroute, runtime, or additional source-shaped probe was used.

| Observation | Actual value |
|---|---|
| Runner status / process exit | `complete` / `0` |
| Scanner process exit | `0` |
| Complete expected rows / actual rows | `[]` / `[]` |
| Observed / lead finding totals | `0` / `0` |
| `eval_calls` / `bash_calls` | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Scanner error | `null` |
| Case reasons / integrity errors | `[]` / `[]` |
| Runner stderr / scanner stderr | empty / empty |
| Selected comparisons passed | `1/1` |

The scanner stdout begins `MADO_TRIPWIRE: clean`, followed by JSON with `findings: []` and all five class counts zero. The full raw runner stdout/stderr, scanner stdout/stderr, exact outer and child argv, exit codes, and integrity facts are retained in [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC109/result.json](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC109/result.json).

The canonical comparator checks forbidden commands before either exact/uncertain acceptance, and exact cases require full sorted multiset equality plus zero unparsed counters: [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-778](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L683). `accept_exact_want` is an uncertain-case alternate, not a license to accept arbitrary observations; it is null and unused here.

## Artifact identity

Independent `sha256sum` checks before and after the measurement matched in every row below. The delivered revision's scanner blob independently matched the selected working-tree scanner. No drift was observed.

| Artifact | SHA-256 before = after |
|---|---|
| Selected scanner | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Selected fixture | `547fb0b8b313581e513448417d142ba251bc9d1d26f8452c9afacface6af61d0` |
| Measurement runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Sealed expected JSON | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original case proposal | `374b2312d388d052648b9d003077fea3c52aceed85c62abe55501366732bc75f` |

Runner integrity facts agree before/after: 106 sealed source files, 52 proposal files, 57 input files; population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`; raw truth seal digest `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`. **Those counts describe integrity validation, not 57 scanner runs or 57 semantic passes.** Normalized expected JSON explicitly reports later materialization from the prior raw seal at [/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:3403](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json#L3403); this report does not misstate it as part of the original raw-seal bytes.

## Residual risk and verification gaps

- The result closes only this explicit unknown-keyword trigger. It establishes neither all F2 forms nor lifetime, partial, conditional-target, scheduled-call, cancellation, recursion, or cross-cell correctness. No resource-saturation claim is made; only the runner's existing cap was exercised.
- Parsed-clean is appropriate **for no reachable command in this fixture**. It does not mean the payload would evaluate successfully: Python would raise `TypeError`. The scanner's invalid sentinel is not a full exception/cell-abort interpreter, and this fixture has no independent later command with which to test broader abort propagation.
- No corpus, full oracle, old-tool red, historical guard, C2 audit, build, lint, formatter, generic smoke, mutation, or live probe was run. No general no-harm, historical-floor, resume-continuity, or admission conclusion follows from this one case.
- The unavailable LSP and the original proposal's section-only Python citation remain explicit evidence limitations, not claimed diagnostics or retained language-source proof.
- No production, fixture, expectation, proposal, gate, registry, or shared documentation was changed. Only this report and the assigned receipt were written. Nothing was installed or updated.

Report: .ufo/waves/round-22/w2/reports/FalsifyC109.md
