# Round 22 W2 — C1 CaptureDefault

## Findings by severity and verdict

**No actionable defect found in the assigned sealed case. Verdict: agree.** The delivered scanner returns the complete independently justified singleton class/command/evidence multiset, with both unparsed counters zero. This is author-lane advisory evidence only, not an admission, integration decision, non-author review, or reversal of the r19/r20/r21 rejected-harmed receipts.

Axes: **(1) semantic argv/callable/lifetime fidelity; (2) exact row multiplicity, classification, evidence, and uncertainty honesty; (3) immutable identity, bounded execution, and truthful scope.** No source-shaped variant or additional scanner invocation was introduced.

## Independent semantic judgment

The exact sealed input is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureDefault.jsonl:1`, retaining the original proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureDefault.json:2-18`.

[INFERENCE: static Python semantics, not payload execution] `def make(argv=["pacman", "-S", "r22-default"])` creates a literal default list. The argument omitted by `make()` is supplied from that default, not from the later module-level `argv`. The nested `run` reads the enclosing factory's parameter cell, which survives the factory return. `return run` is unconditional, `runner` receives that exact function, and the one explicit `runner()` reaches the one `subprocess.run(argv)` call. There are no intervening mutations, rebinding of the returned helper, dynamic arguments, conditional targets, callbacks, scheduling, or namespace resets. The module-level `argv = ["pacman", "-Q", "r22-default-global"]` executes as an assignment but its value is not used by this spawn.

Independent source authority:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst:1297-1308,1326-1329`: omitted arguments receive defaults, which are evaluated when the definition executes; every parameter receives an argument or default value.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:89-115,136-148`: local/free-variable resolution uses the nearest enclosing scope; no `global` declaration redirects this parameter cell to the module.

Therefore the complete expected multiset is exactly one `host_mutation / pacman -S r22-default / observed` row, with zero parse/unparsed errors. `pacman -Q r22-default-global` must not occur as either observed or lead. The sealed `forbid_observed_commands` explicitly forbids its observed form; the exact full-multiset comparison also rejects its lead form or any other extra row. The input contains no true uncertainty: this is `expected_kind=exact`, `accept_exact_want=null`. The sealed `require_signal=true` does not convert the exact branch into an uncertainty case. A missing row, a lead-only replacement, an invented global argv, an extra row, or positive unparsed count would all disagree.

The older F2 red remains authoritative and distinct: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:56,78-83` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl:1` concern a required parameter supplied through unresolved `*parts`. CaptureDefault instead has a valid, completely known omitted default. Passing this case neither converts that original uncertainty into exact truth nor independently establishes repair of that original case. No old classifier was executed.

## Actual changed path reviewed

Reviewed the C1-relevant diff from delivered r21 base `741122d177ae8ff68a73768777f20484d5bdcbe4` to requested target `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The target commit itself changes C2-related files; the accumulated C1 repair is present in the target tree. The committed target scanner blob and the measured on-disk scanner both hash to the fixed C1 identity below.

Relevant definition/caller behavior in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`:

- `:2089-2160`, particularly `:2148-2154`: `bind_literal` fills the omitted positional parameter from its literal default; it does not look up module `argv` for that default.
- `:1642-1683`: the new `factory_result` binds the factory call, overlays its local parameters, processes the prefix before the first direct return, resolves the actual returned name, and records lexical environment/bindings on the returned helper. The captured `argv` is part of that overlay.
- `:1757-1783,1859-1861,1928-1937`: factory-result identity is resolved through the canonical callable/assignment path and stored under the actual `runner` binding.
- `:2203-2254`: statement snapshots preserve execution order. `:2051-2058` excludes deferred function bodies from eager execution, so merely defining `run` does not count its spawn as an executed command.
- `:2510-2516,2547-2580`: invocation uses the returned helper's lexical overlay before the normal helper descent. This replaces the old invocation-time `capture_owner` replay in the reviewed diff; there is no second evaluator for this case.
- `:2407-2439,2630-2679`: the ordinary helper/spawn path reads the bound literal argv. `:775-780` classifies plain `pacman -S` as `host_mutation`; `:2875-2894` emits explicit evidence and call identity.

Static path review and the language source, rather than the runner's green status, support the semantic judgment. No source-namespace metadata collision, conditional callable, or lifetime ambiguity is present in this exact fixture; other shapes were not probed.

## One authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureDefault
```

Canonical run logic is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-874`: population preflight, unique case selection, selected-tool digest, one `scan` call for the selected case, row parsing/evaluation, and postflight. The scanner wrapper at `:34-38` imports that selected source and calls its `main(["--scan", fixture])`; no alternate classifier runtime or rerouting was invoked. The actual scanner child argv is retained verbatim in the receipt. The cap is enforced at `:643-644,655-661`: 402653184-byte address space and 15-second timeout, one child for the selected case.

| Actual class | Actual command | Actual evidence | Multiplicity |
| --- | --- | --- | --- |
| host_mutation | pacman -S r22-default | observed | 1 |

Measured details:

- Runner process exit **0**, status `complete`, totals **1/1 passed**, empty runner stderr.
- Scanner process exit **1**, label `MADO_TRIPWIRE: findings`, empty scanner stderr, `scanner_error=null`, reasons `[]`. Exit 1 means the mutation finding was correctly reported; it is not a clean verdict. The runner's exit 0 means agreement with the expectation.
- Raw finding: `argv0=pacman`, `rule=pacman:-S`, `tool=eval`, `tool_call_id=CaptureDefault-0`, JSONL line **1**, exact selected fixture file, and its sealed digest below.
- Counts: host_mutation **1**; package_query/live_probe/tool_install/vcs_write **0**. Observed findings **1**, lead findings **0**, unpermitted **1**, permitted `[]`.
- File counters: lines **1**, eval_calls **1**, bash_calls **0**, eval_unparsed **0**, unparsed_spawns **0**.
- No decoy global command at any evidence tier, no lost true command, and no extra or downgraded row. This is findings-plus-zero-errors, not parsed-clean ambiguity.

The exact comparison at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-756` sorts the complete row multiset and requires zero unparsed counts after parse errors have already failed. Any-tier and observed-only prohibitions run first at `:740-748`. The uncertain `accept_exact_want` alternate at `:758-778` is a separate branch and is not used here. Input path/digest and counter checks are at `:683-729`.

The runner validated **57 input artifacts**, **52 proposal files**, and **106 sealed source files** before and after. It scanned **one case only**, not 57. Before/after integrity records agree, with no integrity errors or identity drift. This is not whole-population semantic saturation or a resource-scaling measurement.

## Identity and raw evidence

All five identities were independently hashed immediately before and after the sole measurement and were unchanged:

| Artifact | SHA-256 before = after |
| --- | --- |
| Selected scanner | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| CaptureDefault fixture | `52ff553b151d265a84790f5636ac1a325abefc3cc76dc4440dca7ef3927d7378` |
| Canonical measurement runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected.json | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original CaptureDefault proposal | `030059e07b850d1528caa91603ca9b98f9414b5d94708f1819a6c08698afc122` |

Population digest: `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. Raw truth-seal digest retained by the runner: `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`. This measurement does not claim that the later normalized expected manifest existed before implementation; original proposal/seal provenance is retained separately by the canonical preflight.

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC118/result.json`. It retains the exact outer argv, process exit, complete outer stdout/stderr, parsed runner output, scanner argv/exit/stdout/stderr/payload, all five before/after paths and hashes, and integrity records.

## Residual risk and verification gaps

- The `lsp` device is not mounted: attempting to read `xd://lsp` returned `No such tool`. References, definitions, server status, and diagnostics therefore could not be requested. Narrow literal searches and explicit source reads were used as the allowed fallback; grep output is not presented as semantic proof, nor was an empty cold result treated as absence.
- No fixture code or printed command was executed. `observed` is the scanner's static evidence tier, not a claim that a package operation occurred or would succeed on the host.
- Only this single literal-default, unmutated, stored-returned-helper shape is assessed. No added source probe, full suite, generic smoke, build, lint, formatter, old-tool rerun, C2 audit run, or whole-corpus/oracle execution occurred. Shared mutation, nonlocal updates, conditional returns, scheduler races, and other cases remain outside this result.
- No resume path is touched by the assigned changed behavior; no `resume_continuity_v1` or zero-mutation-preflight claim is made.
- No production, fixture, expectation, registry, gate, or source edits were made. No tools were installed or updated. Owned writes were restricted to this report and the assigned raw receipt.
- One-case agreement does not satisfy the overall C1 no-harm guards, C2 registered target, independent non-author admission, or closure/streak requirements. L1 retains planning and integration authority.

Rendered report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC118.md`.
