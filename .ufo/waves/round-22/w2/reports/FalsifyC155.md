# FalsifyC155 — OriginalF5ThreadKeyHygiene

## Verdict: agree, for this frozen case only

The independently reasoned expected row and the delivered scanner's complete result agree. The single authorized measurement passed **1/1 selected case**, with exactly one observed `package_query` row, no leads, no additional rows, and zero parse/error counters. This establishes bounded agreement for the original F5 collision shape, not universal namespace hygiene, complete Python semantics, or admission.

Target revision supplied by the assignment: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The selected working-tree tool was independently bound to the required SHA-256 before and after measurement; no separate commit-tree audit was performed.

### Axes

1. Semantic fidelity: complete command/class/evidence multiset, not command containment.
2. Identity and lifetime hygiene: distinguish a captured thread target from a source global callable.
3. Evidence integrity and boundedness: immutable fixtures and tool, exact raw process capture, one capped scanner child, no source execution or mutation.

## Sealed case and independent truth

The selected record in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` is `supplemental-original`, `expected_kind: exact`, `proposal: null`, and `accept_exact_want: null`. Its source authority is the F5 row and hygiene discussion in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:53-60,97-125`, not the historical scanner's output. There is no separate original proposal for this supplemental case.

The frozen input `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/OriginalF5ThreadKeyHygiene.jsonl` is byte-identical to its original citation `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-hygiene.jsonl`.

Its inert Python source assigns the module global `__mado_thread_target__ = subprocess.run`, defines `worker()` to call that global with `["pacman", "-Q", "r21-hyg"]`, and invokes `threading.Thread(target=worker).start()`.

Independent static reasoning:

- `target=worker` captures the visible worker callable when the standard thread is constructed. Neither that identity nor the source global is subsequently rebound.
- The worker's global lookup resolves to `subprocess.run`, not back to the worker. The spelling `__mado_thread_target__` has no reserved meaning in Python.
- The argv list is fully literal. `pacman -Q r21-hyg` is a package query, not a host mutation or installation.
- The direct standard `.start()` path is an exact-result supported form. There is no conditional target, cancellation, subclass override, opaque argument, nonlocal mutation, or intervening binding change in this case.
- Under this bounded static contract, the reachable spawn has `observed` evidence. This label is not a claim that the fixture, worker, or package query was actually executed.

Therefore the **entire** expected multiset is:

```json
[{"class":"package_query","command":"pacman -Q r21-hyg","evidence":"observed"}]
```

Both forbidden-command arrays are empty. `require_signal: true` does not turn this exact case into an uncertainty case: the runner's exact branch requires complete multiset equality and zero unparsed counters. No `accept_exact_want` alternative applies. A lone lead, a missing command, a duplicate/additional command, or positive error counters must fail; a parsed-clean empty scan is not acceptable.

For genuinely uncertain cases, named forbidden commands must be rejected at every specified evidence tier before any exact alternative is considered. This case does not exercise that uncertainty branch and supplies no coverage claim for it.

## Relevant delivered implementation

Source review was restricted to the scheduled-call/callable/helper path in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`:

- Lines 1726-1756 resolve `mado_resolved` AST metadata before normal source-name lookup.
- Lines 1784-1792 recognize standard scheduled `.start`/`.run` invocation; lines 1839-1853 capture the target identity and arguments.
- Lines 2470-2488 create a synthetic `Name("<scheduled target>")`, attach the resolved target as `target.mado_resolved`, and recurse with the existing `cbindings`. They do not insert a synthetic target under a legal source identifier.
- Lines 2407-2439 follow the helper with copied source bindings and bound arguments. Thus the worker's global alias remains the spawn callable.

This is structural support for the relevant F5 repair, beyond merely observing green. It is not an exhaustive audit of every synthetic node or binding path in the scanner. In particular, this single fixture cannot prove that every other legal source identifier, unrelated lifetime form, or unknown scheduled target is handled correctly.

The original round-21 receipt remains authoritative: the same command was previously reported as **lead**, silently, with zero unparsed counters. The original report's old tool identity and rejection are not rewritten. No old tool was run.

## Authorized measurement and actual output

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case OriginalF5ThreadKeyHygiene
```

The runner enforces `RLIMIT_AS = 402653184` bytes (384 MiB) and a 15-second scanner-child timeout. It validated all 57 fixture identities, 52 proposal files, and 106 sealed source files before and after, but scanned **only this one fixture**. Integrity validation is not a 57-case behavioral run.

| Observation | Actual value |
|---|---|
| Measurement process exit | `0` |
| Measurement status | `complete` |
| Selected total / passed | `1 / 1` |
| Scanner child exit | `1` — one unpermitted finding, not a measurement failure |
| Scanner error | `null` |
| Measurement / scanner stderr | both empty |
| `eval_unparsed` / `unparsed_spawns` | `0 / 0` |
| Observed / lead findings | `1 / 0` |
| `package_query` count | `1` |
| Other class counts | all `0` |
| Mismatch reasons / integrity errors | both `[]` |
| Outer measured elapsed time | `0.11072146700462326` seconds |

Actual complete row multiset:

```json
[{"class":"package_query","command":"pacman -Q r21-hyg","evidence":"observed"}]
```

The finding identifies the selected fixture, line `1`, tool `eval`, tool-call ID `FBR-thread-key-hygiene`, `argv0: pacman`, and rule `pacman:-Q`. The scanner-reported fixture digest matches the sealed input. There is no substituted input, wrong callable row, invented argv, dropped true command, downgraded evidence, or parsed-clean ambiguity in the observed result for this case.

The receipt retains the outer invocation, exit, full unabridged stdout and stderr, including the runner's exact nested scanner argv/output/payload, plus independent before/after hashes. The runner's self-reported argv omits interpreter startup flag `-I` because it builds from `sys.argv`; the outer receipt records the actual requested `-I` invocation, and the nested scanner argv also records `-I`.

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC155/result.json`.

Receipt SHA-256 at creation: `186d308815612c47c6ab749a3041428914a2aac5b9a3eddf18513cee01aa2dbc` (9737 bytes).

## Before/after identity and restoration evidence

All listed hashes were independently identical before and after measurement. The receipt records absolute paths and byte counts.

| Artifact | SHA-256 before = after |
|---|---|
| Selected tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Frozen fixture and original fixture | `4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original review | `9caedd3d4c521b1a07e4206274e0b3041911caefbf845f85890737e1daef888f` |

The runner additionally reported unchanged population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` and no integrity errors. No drift was found. No source bytes were mutated, so restoration is not applicable; unchanged before/after identities are the preservation evidence.

## One minimal proposed source-code fault — not executed

**Fault:** reintroduce synthetic target metadata into the legal source-binding namespace when descending into the scheduled call. At `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2486`, change only the binding argument:

```python
take(spawn_scan([invocation], cenv,
    dict(cbindings, __mado_thread_target__=info["target"]),
    depth + 1, ctx=ctx))
```

This is a plausible one-expression caching/regression fault, not a changed fixture or contract. It overwrites the fixture's source-global alias with the captured `worker` identity inside the scheduled-call descent. `follow_helper` propagates that polluted map into the worker body. The source call then resolves back to the already-active worker rather than to `subprocess.run`; the recursion branch at lines 2547-2555 uses lead evidence.

**Expected detector:** the same frozen-case measurement should reject the resulting complete multiset, expected to contain a lead rather than the required observed query. The expected failure is an evidence-tier mismatch even if the command text survives and both parse counters stay zero. This specifically tests namespace collision, not just scheduling recall.

**Mutation verdict: not run / not evaluated.** This is a proposed fault recipe only. No mutant was created, no mutant/restored detector run occurred, and no kill or survival is claimed. L1 retains actual private-sandbox mutation execution authority.

## Scope and authority

- This was author-lane advisory falsification of one original C1 case, not non-author admission.
- No new source-shaped probe, full oracle replay, corpus scan, C2 audit, build, lint, formatter, generic smoke, live/package query, or fixture execution was performed.
- Production, fixtures, expectations, proposals, gates, registries, and documentation were not edited. Only this assigned report and its seat-local raw receipt were created.
- No tools were installed or updated.
- The broader C1 target includes all eligible finite expectations, every original red, structural hygiene, and no-harm guards. This case's agreement does not establish those other obligations, erase the r19/r20/r21 rejected-harmed history, grant admission, or authorize another round.
