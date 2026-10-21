# FalsifyC138 — C1 case CaptureTwoInstances (author-lane advisory critic)

**Verdict: AGREE** (scoped to this one sealed case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`). This is advisory only. It grants no admission, does not count as non-author falsification, and leaves the r19/r20/r21 rejected-harmed receipts and the streak unchanged.

## Identities (checked before and after the run, no drift)

| Artifact | sha256 |
|---|---|
| `tools/mado-tripwire.py` (worktree == `git show 71228fd:tools/mado-tripwire.py`) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `oracle/expected.json` (matches `expected.sha256` pin) | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `oracle/assemble.py` (producer) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| `oracle/inputs/CaptureTwoInstances.jsonl` | `0e414ef429849c3ce4584c1f6cf7a6cf08e698a70161d30d25e30b3de009c764` |
| `w1/proposals/CaptureTwoInstances.json` | `3fd117ad0a2669129e996d1c9391a47c0a336a7f3bc514f41ecccc0070e24827` |
| population digest | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

HEAD is `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The C2 tool `mado-evidence-audit.py` matched `277eced2…8fca`; it was not used or run.

## Sealed truth versus the original proposal

The sealed record matches the raw proposal: the same cell, `expected_kind: exact`, `want` (in sorted order and `want_input_order`), `forbid_observed_commands: ["pacman -Q r22-ti-c"]`, `forbid_commands_any_tier: []`, `accept_exact_want: null`, `require_signal: true`, one cell with `reset: false`, no addenda and no correction. The runner's own population validation (106 seal files, 52 proposals, 57 cases) passed before and after the run.

## Independent semantic expectation

Inert source (parsed by reasoning only, never executed):

```python
def make_runner(argv):
    def run(): subprocess.run(argv)
    return run
conf = ["pacman","-S","r22-ti-a"]; first  = make_runner(conf)
conf = ["pacman","-Q","r22-ti-b"]; second = make_runner(conf)
conf = ["pacman","-Q","r22-ti-c"]
first(); second()
```

- **Python semantics.** Each `make_runner(conf)` call evaluates `conf` at the call and binds the parameter `argv` in a fresh frame. `run` closes over that frame's `argv` cell. Rebinding the module-level `conf` afterwards neither reaches the existing cells nor mutates the earlier list objects, and nothing is mutated in place. So `first()` runs `pacman -S r22-ti-a` and `second()` runs `pacman -Q r22-ti-b`.
- **Classes.** `pacman -S` is `host_mutation` and `pacman -Q` is `package_query`, consistent with the r21 conventions.
- **Evidence tier.** Both argv lists are fully literal when each instance is created, so both rows are `observed`.
- **Uncertainty.** Every construct is a plain `def`, `Assign`, `Return` or `Name` call. There is no star argument, conditional, mutation, namespace reset or opaque call, so there is no legitimate uncertainty. The correct exact answer has zero `eval_unparsed` and zero `unparsed_spawns`, and no lead rows.
- **Forbidden output.** `pacman -Q r22-ti-c` is never executed, so it must not appear as observed. Emitting it at lead tier would also be wrong for an exact case: the full multiset must match.
- **Expected multiset.** Exactly `{(host_mutation, pacman -S r22-ti-a, observed), (package_query, pacman -Q r22-ti-b, observed)}` with zero errors. I agree with the sealed expectation in full.

`require_signal: true` does not matter for exact cases in `evaluate`, because the exact branch requires a full multiset match and zero unparsed.

## The single authorized measurement

Command: `python3 -I .../oracle/measure.py --tool .../tools/mado-tripwire.py --case CaptureTwoInstances`. One scanner child ran under the runner's RLIMIT_AS 384MiB and 15s caps. No other scanner runs were made.

- **Runner.** Exit 0, empty stderr, `status: complete`, `totals 1/1`, `integrity_errors: []`.
- **Scanner child.** Exit 1 (unpermitted findings present), empty stderr, no `scanner_error`.
- **File row.** `eval_calls 1`, `eval_unparsed 0`, `unparsed_spawns 0`, and the reported sha matches the sealed input.
- **Actual rows.**
  - `host_mutation | pacman -S r22-ti-a | observed` (rule `pacman:-S`, call `CaptureTwoInstances-0`)
  - `package_query | pacman -Q r22-ti-b | observed` (rule `pacman:-Q`, call `CaptureTwoInstances-0`)
- **Payload counters.** `observed_findings 2`, `lead_findings 0`, `unpermitted 2`. These agree with the rows: no observed/lead split mismatch.
- **Result.** `pass: true`, `reasons: []`.

## Falsification attempts for this case

| Attack | Result |
|---|---|
| False observed command (`pacman -Q r22-ti-c`, the invoke-time re-evaluation from F1) | Absent at every tier. |
| Lead argv or invented uncertainty | None: 0 leads and 0 unparsed. That is correct, because nothing is genuinely unknown. |
| Lost true command | Both true commands are present. |
| Wrong identity (instances swapped or merged, `first` resolving to b's frame) | No. Class and command pair correctly per instance; two distinct rows. |
| Lifetime (late lookup of `conf` at invocation) | No. See the mechanism below. |
| Conditional target | Not applicable; no branches. |
| Parsed-clean ambiguity (zero unparsed hiding a failed parse) | No. `eval_calls 1` and both expected rows were emitted from that cell, so the clean counters reflect a real parse. |

**Mechanism, read-only check that the green result comes from the right reason.** `prepare_eval_calls` (lines 2203–2254) updates `env` after each straight-line `conf = [...]`. The repeated simple assignments to `conf` are not in `module_unsafe_names`. `update_bindings` then classifies `first = make_runner(conf)` with the `env` that is live at that statement. `factory_result` (lines 1642–1684) calls `bind_literal(owner, call, env)`, which evaluates `conf` at creation time to the a-list (b-list for `second`). It stores that value in a per-result `closure_env` overlay, so each instance keeps its own frame. Invocation reads the stored overlay instead of re-evaluating the factory-call argument expression. This is creation-time capture, matching Python semantics for this form.

**The case discriminates.** The pre-implementation receipt `evidence/first/oracle-before-new50.json` (r21-delivered `evidence/tool-before.py`) recorded `got_rows: [package_query pacman -Q r22-ti-c observed, …]` for this case. That is exactly the F1 defect. It was read only, not rerun.

## Scope and uncertainty boundaries (not covered by this agreement)

- This is a finite pass on one F1-family form. It does not close F1 in general, F2–F5, or other no-harm guards: historical 166/175, the 1356-fixture removal/error comparison, and resource recipes.
- **Shared mutable aliasing.** `closure_env` stores the literal value at creation. In real Python, a later in-place mutation (`conf.append(...)` or `conf[2] = ...`) after `first = make_runner(conf)` would change `first()`'s argv, because the cell aliases the same list object. The tool tracks subscript or attribute assignment through `MUTATED_LITERALS` by object id, but this case does not exercise it. A search for mutation handling finds only the subscript/attribute assignment targets at lines 2233–2242 feeding `MUTATED_LITERALS`, and no `.append`/`.extend`/`.insert` method-call handling. [INFERENCE] A stale observed command after `conf.append(...)` is therefore a plausible counterexample to look for in sibling cases. It is outside this case and not measured here.
- The `MUTATED_LITERALS` key is a non-string `object()` sentinel, so it does not collide with source identifiers. This was noted only; F5 hygiene is not adjudicated here.

## Smallest safe correction

None required for this case.

## Receipts

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC138/result.json` contains the argv, exits, stdout/stderr, rows, hashes before and after, and `hash_drift: false`.
- The raw files in the same directory are `stdout.raw`, `stderr.raw` (empty), `exit.txt` (0), `hashes-before.txt` and `hashes-after.txt`.

No production, fixture, expected, proposal, gate, registry or doc edits were made. No installs or updates were made. No delegation was used.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC138.md
