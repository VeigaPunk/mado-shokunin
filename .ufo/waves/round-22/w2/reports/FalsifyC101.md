# FalsifyC101 — C1 CX11Reset

## Verdict and findings by severity

**Agree, for this exact sealed case under its explicitly disclosed fresh-namespace reset premise.** No actionable candidate defect or truth/expectation contradiction was found in the assigned case. This is author-lane advisory falsification evidence, not non-author admission, integration authority, closure, or desktop clearance.

Axes: (1) complete class/command/evidence agreement; (2) callable and captured-frame lifetime across reset; (3) evidence-tier and parsed-clean honesty; (4) fixture/tool/runner identity and bounded-measurement provenance; (5) scope honesty.

## Independent semantic expectation

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX11Reset.json:3-17`. Its source citation is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/CriticScope.json:202-210,264-269`. The sealed case in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` retains the original cells, `cell_reset: [false, true]`, exact empty `want`, no addenda or correction, `accept_exact_want: null`, and `require_signal: false`.

1. Cell 1 imports `subprocess`, constructs the literal argv, defines `factory`, and calls that factory to store the returned `run` closure as `worker`. Returning that callable does not invoke its `subprocess.run(argv)` body. Therefore cell 1 contributes no finding.
2. Under the sealed premise that `reset: true` starts a fresh Python namespace, cell 2's `worker()` cannot resolve `worker`. It raises `NameError` before any subprocess call. There is no true executed command to preserve, no conditional target, and no permitted stale observed or lead argv.
3. Consequently the **complete expected row multiset is `[]`**, with `eval_unparsed = 0` and `unparsed_spawns = 0`. `pacman -S r22-cx11-reset` is forbidden at **every** evidence tier, not merely observed. A lead for that command would also be false. This is an exact no-spawn case, not an uncertainty case permitted to pass with a lead/unparsed signal. `accept_exact_want` does not apply.
4. Zero scanner counters mean the static input was handled, not that evaluating its Python would complete successfully. The expected `NameError` and an empty static findings set are compatible. “Clean” here is not general execution-safety proof.

The materialized input `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX11Reset.jsonl:1-2` actually carries `reset: false` followed by `reset: true`. Dropping the second flag would change semantics; it was not dropped. The runner checks each reset value against the sealed cell list and each code string against the original proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:409-443`.

## Actual diff and relevant candidate path

The delivered revision is `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; file history identifies `330de6887430cf54b1cdaee59b20183f0c3e24a0` as its last change to the selected tool. I read that implementation diff. The relevant change replaces invocation-time `capture_owner`/`capture_call` reconstruction with creation-time `closure_env`/`closure_bindings`. The reset branch itself was not a newly added repair in that diff; this case guards the new retained closure representation against crossing the existing reset boundary.

Relevant source reasoning, separate from the green result:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684` constructs the returned callable's lexical overlays. Deferred function bodies are not executed merely by definition; the eager walk visits function decorators/defaults instead of the deferred body at `:1993-2001,2051-2058`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2860-2868` clears Python literals before the reset cell and replaces every prior binding with a `reset_unbound` record. That replacement carries neither the old helper node nor captured closure overlays.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1748-1756` returns that current binding for the `worker` Name. The stale helper is not recovered through a def-name index. The helper-follow and closure-overlay branches at `:2510-2516,2547-2580` therefore do not apply. Nor is the record a spawn callable at `:2623-2631`. The reference sweep at `:2738-2750` has no helper/class/spawn target to sweep from that tombstone.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280-2293` parses to AST and reports static counters; it does not execute the fixture or observe the predicted Python exception.

The case contains no Thread/Timer scheduling, race, shared-object mutation, or conditional return, so this result does not establish those neighboring contracts.

## Sole authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX11Reset
```

| Quantity | Actual |
| --- | --- |
| Runner status / OS exit | `complete` / `0` |
| Case comparison | `1/1`, `pass: true`, `reasons: []` |
| Scanner OS exit / scanner error | `0` / `null` |
| Complete class/command/evidence rows | `[]` |
| Observed / lead findings | `0 / 0` |
| `eval_unparsed` / `unparsed_spawns` | `0 / 0` |
| File lines / eval calls / bash calls | `2 / 2 / 0` |
| Forbidden argv at any tier | absent; findings are empty |
| Runner stderr / scanner stderr | empty / empty |
| Integrity errors / before-after hash drift | `[] / {}` |

Scanner stdout begins `MADO_TRIPWIRE: clean`; its following JSON has `findings: []`, all five class counts zero, and the exact selected fixture path/digest. The report's semantic agreement follows the cell reasoning and source path above, not that banner.

The runner imposes one scanner child's 384 MiB address-space limit and 15-second timeout at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-660`. It validates the full frozen population before selecting and running the single case, then checks integrity afterward at `:789-870`. Both integrity records report 106 sealed source files, 52 proposal files, and 57 input files verified. **These are integrity counts, not 57 scanner runs or 57 semantic passes.** This seat made one scanner measurement only; no resource-saturation or universal lifetime claim follows.

Raw outer/scanner argv, exits, stdout, stderr, complete scanner payload, independent pre-measurement expectation, and hashes are retained in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC101/result.json`. Outer stdout/stderr also have byte-preserving base64 and SHA-256 records.

### Identity evidence

Each digest below was checked before and after the sole run; all were unchanged. The tool and expected-manifest digests match the assignment pins.

| Artifact | SHA-256 |
| --- | --- |
| Selected C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Oracle expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| CX11Reset fixture | `d406f22798043bf5aadc397d1e6582490801de6175c8060c6a6e7d94633fa920` |
| Original CX11Reset proposal | `1ab019a3689bc60411754ce5869a95bc7f5b3e8713d5d48f73682e6ebc568fac` |

## Residual risk and verification gaps

- The proposal explicitly discloses that independent on-disk authority for the eval reset protocol was not located; its original detector docstring was not used as truth. This review preserves that premise boundary. It does not turn a green detector result into independent protocol validation. If the premise is false for a different transcript producer, the exact expectation must be revisited, not silently normalized.
- `xd://lsp` was unavailable (`No such tool`). Semantic references, definitions, and diagnostics could not be requested. Literal grep served only to locate relevant source; it is not offered as semantic absence proof. Conclusions use the cited branches and retained bounded measurement.
- This exact reset-true negative does not prove reset-false positive recall, all closure lifetime forms, callable/scheduled repair generally, or corpus no-harm. No new source-shaped probe, mutant, original-old-tool rerun, build, lint, formatter, full-suite test, generic smoke, live probe, or fixture execution was performed. No other runtime, same-identity rerouting, saturation, or resume path was exercised; `resume_continuity_v1` is outside this leaf case.
- Original r19/r20/r21 rejected-harmed receipts, source authority, and rejection streak remain unchanged. Nothing here admits the recovery or changes L1's planner/integration authority.

Production, fixtures, expectations, tools, and shared documentation remained read-only. Only this assigned report and its receipt were written. No tools were installed or updated.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC101.md
