# CapturePartialGlobal — FalsifyC128

## Findings and verdict

**Verdict: agree, bounded to this exact sealed case.** No actionable defect was found in the assigned case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. This is an author-lane advisory recommendation, not an admission or independent non-author closure.

The sole actual finding was:

| Class | Command | Evidence | Multiplicity |
|---|---|---|---:|
| `host_mutation` | `pacman -S r22-partial-global` | `observed` | 1 |

This is the complete expected and actual multiset, not a matching subset. There were **zero lead rows**, zero `package_query` rows, `eval_unparsed = 0`, and `unparsed_spawns = 0`. The late command `pacman -Q r22-partial-global-late` appeared at **no evidence tier**. The finding identifies the selected fixture, line 1, `tool = eval`, `tool_call_id = CapturePartialGlobal-0`, `argv0 = pacman`, and `rule = pacman:-S`.

### Axes

1. Creation-time argument-object lifetime versus invocation-time global lookup.
2. Returned callable identity, reachability, complete row count, and evidence tier.
3. Exact-result/uncertainty separation, including absence of invented argv and hidden parse errors.
4. Same-identity, single-case bounded measurement and immutable artifact provenance.

No broader Pareto, saturation, or family-completeness claim follows from this one-case agreement.

## Independent semantic derivation

Sources: the exact [sealed fixture](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialGlobal.jsonl#L1), the original [proposal, lines 3–18](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialGlobal.json#L3-L18), and the `CapturePartialGlobal` record in [sealed expected.json](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json).

[INFERENCE: Python source semantics; the payload was never executed.]

- `ARGV` first names list A, `['pacman', '-S', 'r22-partial-global']`.
- `bound = make_partial()` runs the visible, parameterless factory while that binding is current. The return expression constructs `functools.partial(run_helper, ARGV)`. Its stored first positional argument is list A, and its target is the visible `run_helper` function.
- The next assignment makes `ARGV` name a new list B, `['pacman', '-Q', 'r22-partial-global-late']`. It does not mutate A. The partial retains A even though the module name now refers to B.
- `bound()` calls `run_helper` once, binding its `cmd` parameter to A. The helper passes `cmd`, not a fresh lookup of global `ARGV`, to `subprocess.run`.
- Accordingly, the complete static truth is exactly one observed `host_mutation` row for `pacman -S r22-partial-global`, with zero unresolved counters. The `-S` classification is consistent with [classify_pacman, lines 775–780](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L775-L780).

There is no conditional target, unknown expansion, missing argument, helper rebinding, opaque operation, list mutation, scheduling race, or namespace reset in this cell. A lead-only result, a second row, a late-query row, or an empty parsed-clean result would disagree with its semantics. The exact expectation was not weakened: `expected_kind = exact`, `accept_exact_want = null`, no correction, and no addenda. `require_signal = true` does not require uncertainty on an exact case; the canonical exact branch demands the whole expected multiset and zero unparsed counters.

The historical [F1 review, lines 70–76](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md#L70-L76) remains source authority. Its original captured-closure red and its source-only partial diagnosis are not reinterpreted as fresh measurements of this sibling. The original [capture-invoke-time fixture](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-invoke-time.jsonl#L1) was read as inert data, never rerun with an old tool.

## Relevant implementation and actual diff

Read the relevant hunks of the actual candidate diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, restricted to the selected production path. The delivered commit's immediate-parent diff for that path was empty; the recovery-base diff contains the repair. `git show` of the delivered tool hashes to the same bytes measured below.

The relevant cutover replaces raw partial argument AST retention and invocation-time `capture_owner` replay with creation-time capture:

- [captured_node, lines 1417–1425](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1417-L1425) stores a resolved literal and callable identity on an inert synthetic node. [literal_value, lines 1355–1363](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1355-L1363) consumes the stored literal rather than looking up the later source name.
- [factory_result, lines 1652–1684](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1652-L1684) binds the factory call, resolves its return using the creation environment, and limits its lexical overlay to factory-local bindings. [callable_info, lines 1761–1781](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1761-L1781) resolves the partial target and captures its fixed arguments there.
- The assignment path retains that returned helper metadata through [assignment_binding, lines 1859–1861](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1859-L1861) and [update_bindings, lines 1928–1936](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L1928-L1936). [prepare_eval_calls, lines 2217–2253](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2217-L2253) snapshots statements in order; a plain global-name rebinding is not the tracked subscript/attribute mutation of a stored list.
- At `bound()`, [spawn_scan, lines 2556–2579](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2556-L2579) prepends the captured fixed argument and follows the retained helper. [follow_helper, lines 2415–2437](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2415-L2437) binds that argument to `cmd`; [spawn_scan, lines 2632–2679](/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py#L2632-L2679) classifies the resulting literal argv.

This source route supports the bounded lifetime/identity result independently of the oracle's green bit. It does not establish correctness of every caller or every Python partial form.

## Sole authorized measurement and retained evidence

Executed exactly once, without a new source-shaped probe:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CapturePartialGlobal
```

The runner exited **0**, status `complete`, totals **1/1**, reasons `[]`, integrity errors `[]`, and outer stderr empty. Its scanner child exited **1**, correctly reporting one unpermitted finding; this is not a scanner error. Child stderr was empty and `scanner_error` was null. Scanner stdout contains `MADO_TRIPWIRE: findings` followed by its JSON finding payload.

The canonical [scan logic, lines 643–680](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L643-L680) uses one `/usr/bin/python3 -I -c` child, the selected tool path, `RLIMIT_AS = 402653184` bytes, and a 15-second timeout. The [case selector and execution loop, lines 803–852](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L803-L852) selected only this case. No alternate scanner, rerouting, old-tool invocation, mutant, or additional scanner child was used.

The runner validated the full frozen population before and after, reporting 106 sealed source files, 52 proposal files, and 57 fixture files verified. **Those are integrity counts, not 57 scanner executions.** Its [output parser, lines 683–729](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L683-L729) checks fixture identity, digest, explicit evidence markers and both counters. Its [evaluator, lines 736–778](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py#L736-L778) checks forbidden argv before exact/uncertain handling and compares complete sorted multisets for exact cases. This pass did not use `accept_exact_want` or an uncertainty fallback. The any-tier forbidden list is empty for this exact case; nevertheless, full-multiset equality rejects every extra late-query row, including a lead.

Raw receipt, containing the actual outer argv, exit, complete stdout/stderr, parsed runner output, full child argv/stdout/stderr, and before/after hashes:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC128/result.json`

Independent `sha256sum` calls before and after the measurement returned identical values:

| Artifact | SHA-256 before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialGlobal.jsonl` | `1fa49e8cf1241ac9045ac55c0eab8673772ac165c66f021c117e35fba8ea4741` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialGlobal.json` | `74bb06ab1f5670474254b57a49ae2d549ef6411c9bf918da18b031f7bc2a7070` |

No drift from the assigned tool or expected identity was observed. Population SHA-256 was `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` before and after.

## Residual risk and verification gaps

- This closes only the assigned exact sibling's attempted falsification. It does not close F1 as a family, other frozen cases, C2, full-corpus no-harm, resource scaling, concurrent scheduling, conditional returns, or opaque/mutable capture semantics. In particular, list mutation and a helper reading a free global at invocation are different from this unmutated fixed positional argument.
- The measured cap is an enforced limit, not peak-memory, asymptotic, or saturation evidence. No benchmark, generic smoke, build, lint, formatter, full suite, or corpus rerun was performed.
- `xd://lsp` returned `No such tool`; no status, references, definition, or diagnostics request could be made. Text searches were the literal fallback for locating source only, not semantic caller proof. No claim of clean diagnostics or exhaustive semantic references is made.
- No resume path is present in this case; `resume_continuity_v1` was not exercised or certified. No host safety or recovery clearance follows from the scanner label.
- Fixture code and its printed commands remained inert scanner input. No production, fixture, expected, gate, registry, or source edit was made. Only this assigned report and its receipt were written. No installation or update was performed; no fault was proposed or called killed.
- The r19/r20/r21 rejected-harmed receipts and rejection streak remain authoritative and unchanged. L1 retains planner/integration authority. This report grants no admission.
