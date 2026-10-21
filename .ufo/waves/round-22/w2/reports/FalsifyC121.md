# FalsifyC121 — C1 CaptureKwUnknown

## Findings, by severity

No actionable current-target defect was demonstrated for this sealed case. **Verdict: agree**, specifically with the uncertainty result, not with an assertion that all source behavior was resolved or that the host is safe. This is an author-lane advisory recommendation and grants no admission.

The original round-21 F2 red remains historical source authority; this result does not erase the r19/r20/r21 rejected-harmed receipts or their streak.

## Scope and axes

Reviewed delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, the selected C1 tool bytes, the exact sealed `CaptureKwUnknown` record and fixture, its original proposal/addendum, its cited F2 source, and the candidate binding/invocation/output paths relevant to this case. The actual tool diff was read against registration base `741122d177ae8ff68a73768777f20484d5bdcbe4`; unrelated changed behavior was not graded.

Axes: **command/class/evidence truth; lexical callable identity and lifetime; explicit uncertainty versus parsed-clean claims; immutable artifact identity/provenance; bounded execution and honest coverage.** No production, fixture, expectation, proposal, registry, or documentation edits were made by this reviewer. No new source-shaped probe, mutant, old-tool run, full-suite run, build, lint, formatter, installation, live probe, or delegated job was performed.

## Independent semantic expectation

Authority read:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureKwUnknown.json:2-13` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureKwUnknown.addendum.json:2-19`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:53-59,78-83`: the original F2 defect borrowed a module global after factory argument binding failed. Its reported old-tool failure was not rerun.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:13-22`: unresolved expansion cannot borrow a same-named module literal at any evidence tier; exact and uncertain cases have different acceptance contracts.

The sole inert cell defines `make(argv)`, whose returned `run` closes over that parameter; assigns module `argv = ["pacman", "-Q", "r22-kwunknown-global"]`; then attempts `runner = make(**unknown_map)` and `runner()`.

Static reasoning, not fixture execution:

1. There is no visible binding of `unknown_map`. In the visible-source namespace, evaluating that name fails before factory argument binding, so the factory does not run and `runner` is not assigned by this statement.
2. Even allowing an opaque preexisting mapping because this cell has `reset: false`, no mapping contents or parameter value can be reconstructed from the fixture. A mapping could supply a different command or cause binding failure; the scanner cannot assert either command from that possibility.
3. `run` loads `argv` from the enclosing parameter cell. The same-named module global is not a fallback for that lexical cell. Reporting the module command as either observed **or lead** would therefore invent argv, not merely lower confidence.
4. Consequently no class/command/evidence finding is required. This is not a proved exact-empty scan: the frozen original/addendum require the unresolved expansion to remain visible as lead/unparsed uncertainty.

Complete sealed contract: `expected_kind: uncertain`, `want: []`, `accept_exact_want: null`, `require_signal: true`. Both `pacman -Q r22-kwunknown-global` and `pacman -S r22-kwunknown-global` are forbidden at **all** evidence tiers. There is no accepted-exact alternate permitting an observed row or permitting an empty, zero-unparsed result. In contrast, the runner's exact-case branch requires the complete sorted class/command/evidence multiset and zero unparsed counters; that branch does not apply here.

## One authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureKwUnknown
```

The runner selected one case only. It statically verified all 57 fixture identities, 52 proposal files, and 106 sealed source files before/after; these are integrity counts, **not** 57 scanner executions or 57 semantic passes. Measured totals were **1/1**. The scanner child cap was 402653184 bytes (384 MiB) of address space and 15 seconds, enforced by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661`; the selected-case loop is at lines 806-810 and 828-852.

| Observable | Actual |
|---|---|
| Measurement process exit / stderr | `0` / empty |
| Scanner child exit / stderr | `0` / empty |
| Complete finding-row multiset | `[]` |
| Observed / lead findings | `0` / `0` |
| `eval_calls` / `bash_calls` | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / **`1`** |
| Runner combined `unparsed` | **`1`** |
| Scanner process/output error | `null` |
| Case pass / reasons | `true` / `[]` |
| Raw first scanner line | `MADO_TRIPWIRE: clean` |
| Before/after identity drift / integrity errors | none / `[]` |

All five class counters (`host_mutation`, `live_probe`, `package_query`, `tool_install`, `vcs_write`) were zero. No forbidden command appeared at any tier, and there were no additional rows to hide behind subset matching. The nonzero unresolved-spawn counter, not the exit code or the banner, makes this a valid uncertainty outcome. The outer process elapsed time was approximately 0.111 seconds; this single small case supports no saturation or general resource-performance claim.

Raw outer argv/exit/stdout/stderr, nested child argv/exit/stdout/stderr and payload, and before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC121/result.json`. The runner's self-reported argv omits interpreter startup flags because it reconstructs argv from `sys.argv`; the receipt separately preserves the actual outer invocation including `-I`, and the nested scanner argv explicitly includes `-I`.

## Candidate path and attempted falsifications

The actual diff replaces late `capture_owner`/`capture_call` reconstruction with `factory_result` and explicit closure overlays. Relevant current source:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1629-1662`: a nonliteral double-star expansion is classified uncertain; failed binding installs `LITERAL_MISS` for factory parameters and overrides the copied module environment. It is not treated as a definitely invalid ordinary keyword call.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1663-1684,1757-1783,1820-1861`: prefix bindings and the returned helper are resolved at the factory boundary, carried through assignment, and accompanied by lexical environment/binding overlays.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2509-2516`: invocation overlays the captured lexical values onto the caller environment. The unresolved `argv` therefore masks the module literal instead of borrowing it.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2407-2439,2547-2579,2635-2684`: helper follow/sweep and spawn resolution retain unresolved arguments as uncertainty rather than manufacturing a command. The measured unresolved-spawn count is consistent with that path; this is source reasoning, not an instruction-level trace.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729,736-778`: the canonical oracle checks selected-file identity, validates evidence markers and counters, rejects forbidden commands at every tier, rejects observed rows outside a complete accepted-exact alternate, and requires a lead or positive unparsed counter for this case.

| Attack axis | Result for this fixture |
|---|---|
| False observed or fabricated lead argv | Not reproduced: complete actual rows are empty; neither forbidden bait command appears. |
| Lost true command | No statically determined true command exists here. Empty rows do not conceal a required `pacman -S` result; explicit uncertainty remains. |
| Wrong callable/lexical identity | No wrong-identity command was emitted. Source overlays explain why the module-global bait does not satisfy the closure parameter. |
| Lifetime | The relevant unresolved parameter remains unresolved at use; the fixture contains no later rebinding/mutation of a successfully captured value. No broader lifetime conclusion is warranted. |
| Conditional or scheduled target | Absent from this case. This measurement does not test those forms or close their defect families. |
| Parsed-clean ambiguity | The banner is literally `clean`, but `unparsed_spawns: 1` prevents a parsed-clean interpretation. The oracle correctly preserves it as uncertainty. |

The runner imports the one selected absolute tool path and invokes its `main(["--scan", selected_fixture])`; it does not substitute another classifier. That import wrapper is shown in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:34-38,655-661`. No alternative runtime was invoked. The script-only `run_with_stack` entry path was not exercised by this import wrapper; this was the required measurement route, not a claim of full CLI-entry parity.

## Identity evidence

Each artifact below had the same SHA-256 before and after the single measurement:

| Artifact (absolute path) | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureKwUnknown.jsonl` | `3597dfea7424caa53a8ded7bed0c52d2b556479b51254190f4edbca5be10f39d` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureKwUnknown.json` | `6126a54eb3b0995e0bd78049fa624e608e037b478d01df980519a23fa250d14b` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureKwUnknown.addendum.json` | `abb870f1cda045c5c1331687eaa38b75016c7b8713c67c2ee52221fbab8c7659` |

The selected tool and normalized expected identities match the assignment pins. Original proposal/addendum and the later normalized manifest remain distinct artifacts; no expectation was rewritten or inferred from the green measurement.

## Residual risk and verification gaps

- **The clean banner is not zero uncertainty.** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2909-2939` derives the label from finding presence and retains file counters in JSON. Its documented contract at lines 26-36 expressly disclaims inferring that no host command ran. The observed banner/counter combination is therefore not a newly demonstrated contract defect, but any summary that calls this a zero-error or fully parsed scan would contradict this receipt. This report does not do so.
- Only this uncertain expansion fixture was scanned. No valid-capture case, arbitrary factory family, conditional target, scheduled call, historical population no-harm result, or C2 result is established here. No source-wide completeness, host recovery, admission, or outside-lane independence claim follows.
- `xd://lsp` is unavailable: the device discovery returned `No such tool`. LSP status, references, definitions and diagnostics could not be obtained. Literal grep located relevant sections, followed by direct source/diff inspection; grep results were not treated as semantic proof. No empty cold-index result was treated as absence.
- No resume path or `resume_continuity_v1` behavior is present in this assigned scanner case; no preflight/mutation claim is made about it.
- No installs or updates were needed or performed. All scanner evidence is from the single authorized bounded run; the inert payload and printed command strings were never executed.

**Disposition:** agree with the sealed bounded C1 uncertainty outcome for `CaptureKwUnknown`; no actionable case-specific counterexample remains from this attack. Admission and historical streak disposition remain with L1/Main and the required non-author process.

Report: .ufo/waves/round-22/w2/reports/FalsifyC121.md
