# AtkIdFunction — C1 supplemental review

## Verdict

**No actionable finding in scope.** The frozen `IdFunction` expectation `want: []` is semantically warranted, and the current scanner returns no finding for the frozen input. The adjacent rebound-builtin probe also follows the callback and reports the resulting command, so this check found no fixture-keyed `id` special case. This is a scoped result, not a claim that no counterexample exists elsewhere.

## Identity and frozen expectation

- Current candidate commit: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Tested `tools/mado-tripwire.py` SHA-256: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Frozen record: `.ufo/waves/round-21/oracle/expected.json:203-212`; case input SHA-256 `214bcd65fdd2bf43090c78c35bf2a1e02df2b9a26d3451fb8b326bc902b4f552`; expected `want: []`.
- The input defines `f` with a `subprocess.run(["pacman", "-Q", "r21"])` in its body, then evaluates `id(f)`. Defining `f` creates a function object; the built-in `id` observes that object's identity and does not call it. Thus the `subprocess.run` body is dormant: there is no executed package query, so no finding class, command, or evidence row belongs in the frozen expectation.

## Current-code probes

Both probes used the existing `oracle/measure.py` `scan` API. Each scanner subprocess was bounded by its API's 384 MiB address-space cap and 15-second timeout. The snippet text was parsed only; no Python or shell payload was executed.

1. **Frozen input**, `.ufo/waves/round-21/oracle/inputs/IdFunction.jsonl` (SHA-256 above): tested code hash `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`; scanner exit `0`; findings `[]`; counts all zero; `eval_unparsed: 0`, `unparsed_spawns: 0`.
2. **One nearby variant**, retained at `.ufo/waves/round-21/w2/fixtures/AtkIdFunction/identity-rebound.jsonl` (SHA-256 `18c1353dc457c6072c4798a50c75e06185c49c6427258d848aa947f6be2a8edc`): it keeps `f` and its command body but defines `def id(callback): callback()` before `id(f)`. Current scanner exit `1` (one unpermitted finding); output has `package_query: 1`, `eval_unparsed: 0`, `unparsed_spawns: 0`, and the finding `{class: package_query, command: "pacman -Q r21", evidence: observed, rule: "pacman:-Q", tool_call_id: "IdFunctionRebound-0", line: 1}`. This is static scanner classification, not execution of `pacman`.

## Generality assessment

The relevant rule is binding-aware rather than keyed to this fixture's source text. `tools/mado-tripwire.py:1593-1602` checks an in-scope binding before treating an unbound name in `PURE_ARG_CALLS` (including `id`) as a pure builtin. `update_bindings` records a function definition as a helper (`:1718-1725`). In the current helper-following path, actual callable arguments are resolved into their formal parameters (`:2173-2184`); reference handling skips a function value only when its receiving call is pure/value and not a higher-order operation (`:2386-2395`). The variant shadows built-in `id` with a callback-invoking helper; the observed package-query row shows that this binding is not mistakenly treated as the builtin and that the passed `f` body is reached. These mechanisms operate on bindings and call shape, not `IdFunction`, `pacman`, or fixture identifiers.

No counterexample was found in the frozen input plus this single adjacent variant. This does not establish correctness for all aliases, rebinding forms, or callback paths.

## Receipt and verification gaps

- `.ufo/waves/round-21/evidence/oracle-candidate.json` records `measured_commit: 843d301d1b17af78427918f7845af336b2218de0` and `tool_sha256: 56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`. Its `IdFunction` pass/no-findings result is historical, not evidence for the current candidate; the current-code scan above supplies that evidence.
- No `lsp` device is mounted (`xd://lsp` returned “No such tool”), so LSP status, references, definition, and diagnostics could not be obtained. Text search was used only to locate source sections, not as semantic proof; the assessment above is based on direct source reading and bounded scans.
- No full suite/corpus, dynamic program execution, or other runtime was run. No tools were installed or updated.
