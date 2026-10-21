# FalsifyC107 — CX7ThreadRepeatedRun

## Recommendation and findings

**Verdict: agree, for this exact sealed case and pinned C1 tool only.** No actionable defect was found in the assigned case. This is an author-lane advisory falsification result, not a runtime judgment, admission, or recovery grant.

The sole authorized measurement returned the complete expected multiset: **one observed `host_mutation` row for `pacman -S r22-cx7-twice`, no duplicate, no lead, and zero scanner uncertainty counters**. Independent source reasoning supports that result; the comparison's green status is not the semantic proof.

Reviewed delivery: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The selected on-disk tool matched its assigned SHA-256 before and after measurement. The relevant actual diff was inspected from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that delivery, limited to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`.

## Axes

1. Exact class/command/evidence multiset, including multiplicity and no extra rows.
2. Thread-instance lifetime and captured callable/argument identity.
3. Honest uncertainty, error accounting, and distinction between static observation and live execution.
4. Pinned artifact provenance, single bounded measurement, and read-only execution.

## Independent expectation and semantic rationale

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX7ThreadRepeatedRun.json:2-12`. The normalized sealed entry in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` retains that proposal, its source citation, and its single wanted row. It is an **exact** case; `accept_exact_want` is null, addenda are empty, and there is no correction. The inert fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX7ThreadRepeatedRun.jsonl:1` contains one Python eval cell, reset false: define `worker(argv)` calling `subprocess.run(argv)`, construct one standard `threading.Thread` with that worker and the literal argv, then call `t.run()` twice.

The retained independent CPython source establishes the relevant sequence:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py:925-928` stores the target and argument objects on the newly constructed instance.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py:1013-1028` shows ordinary `Thread.run()` synchronously invoking `_target(*_args, **_kwargs)` inside `try`, then unconditionally deleting those instance attributes in `finally`.
- Thus the first call reaches `worker` and one `subprocess.run(["pacman", "-S", "r22-cx7-twice"])` invocation. If that subprocess call raises, the cell exits after the first invocation and cleanup still occurs. If it returns, the second `t.run()` cannot invoke the target: `_target` has been deleted, so access raises `AttributeError`; its cleanup can raise again. Neither path invokes the worker twice.

There is no `.start()`, concurrent schedule, cancellation race, subclass override, conditional target, dynamic argument, rebinding, or target replacement in this input. The literal `pacman -S` requests a host mutation; it is not a package query. This classification comes from the independently stated proposal mapping, consistent with the candidate's unchanged mapping at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:775-780`.

The complete expected multiset is therefore exactly:

```json
[{"class":"host_mutation","command":"pacman -S r22-cx7-twice","evidence":"observed"}]
```

Here “observed” is the detector's static reachable-call tier for transcript source, **not evidence that this review launched pacman or that a package operation succeeded**. The fixture's second Python call failing is not a scanner parse failure. Zero `eval_unparsed`/`unparsed_spawns` is compatible with knowing this command history; it does not assert that the Python cell completes successfully.

## Relevant delivered behavior

The inspected diff adds `.run()` to the scheduled invocation path, introduces per-instance state, and replaces the former legal-identifier synthetic binding with resolved AST metadata. The current relevant path is:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1841-1853`: one constructed scheduled object records the worker identity, literal args, kwargs, and a nested `state` initially not done/cancelled.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1930-1936` and `:2163-2200`: assignment and statement snapshots retain the scheduled binding and its nested state identity rather than creating a fresh state for each later call site.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1784-1792`: `t.run` resolves to a shallow scheduled-invoke record sharing that state.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2470-2489`: the first invocation marks it done and scans the captured target with literal arguments; the second sees done and produces no second target scan. The synthetic target carries `mado_resolved`, which is consulted before binding lookup at `:1728-1730`; it is not inserted into the source binding namespace.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2564-2579` follows the visible worker with bound arguments. The Thread-constructor reference at `:2731-2734` does not independently sweep that worker into an extra lead.

For this source, the consumed-state shortcut has the same finding multiset as CPython's target deletion. It does **not** demonstrate general Python exception/control-flow equivalence after a failed repeated invocation: this fixture ends at the second call.

Original r21 authority is unchanged: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:90-95` records the `.run()` recall failure and ownership of the Thread target. Those original reds were read, not re-executed with an old tool. This one variant does not replace the original cases or close every F4 trigger.

## Sole measurement and actual rows

Invoked once, with no additional scanner run:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX7ThreadRepeatedRun
```

The scanner child cap is defined and applied by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:26-27,643-660`: 384 MiB address-space limit and 15-second timeout, one selected case scanned serially. A write-denying Landlock ruleset was applied before the measurement runner exec and inherited by its scanner, preventing filesystem mutation, including import bytecode writes. Captured output was retained afterward through the write tool outside that restriction. No fixture code or printed package command was executed.

Actual retained result:

| Item | Actual |
|---|---|
| Runner exit/status | `0` / `complete` |
| Executed case count | `1`, `CX7ThreadRepeatedRun` only |
| Comparison | pass `1/1`; reasons `[]` |
| Scanner child exit | `1` — finding present, not could-not-evaluate |
| Exact row | `host_mutation` / `pacman -S r22-cx7-twice` / `observed` |
| Raw finding identity | selected absolute fixture path, line `1`, tool `eval`, tool call `CX7ThreadRepeatedRun-0` |
| Rule / argv0 | `pacman:-S` / `pacman` |
| Observed / lead count | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Scanner error / stderr | null / empty |
| Runner stderr / integrity errors | empty / `[]` |

All other class counts were zero. The scanner reported the exact sealed fixture digest. The runner validated 57 input artifacts, 52 proposal files, and 106 sealed source files before and after; this is **artifact validation, not 57 executed scanner cases**.

The comparison is not subset containment or deduplication: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-756` sorts full row tuples and requires equality plus zero unparsed counters for exact cases. A duplicate, lead substitution, extra command, missing true command, or empty parsed-clean result would fail this case. The selected fixture identity is checked at `:683-729`.

The any-tier prohibition check runs before exact/uncertain handling at `:740-748`; the uncertain branch's complete accepted-exact alternate and signal checks are at `:758-777`. They were reviewed, **not independently exercised by this exact-case measurement**. Although the sealed exact case has `require_signal: true`, the exact branch does not turn it into an uncertain case or accept a lead in place of its observed row. No expectation was normalized to match this output.

## Hash identities

Independent `sha256sum` commands before and after the sole measurement returned identical values for every artifact below. Tool and expected match the assignment pins; the runner also retained matching before/after integrity records. No drift was observed.

| Artifact, absolute path | SHA-256 before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX7ThreadRepeatedRun.jsonl` | `1bdd4f479e5aa9ec297ebf4ad026c11ebc05c4586a9bfa6ff99bb94778767ca5` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX7ThreadRepeatedRun.json` | `cf7029dc0856dadd8031379a1abc7a038e273de377bd14d1cd5303a6ab0a5679` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py` | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC107/result.json`. It retains the exact requested argv and runner exit/stdout/stderr, parsed runner evidence, nested actual scanner argv/exit/stdout/stderr/payload, resource and read-only enforcement details, and before/after hashes.

## Residual risk and verification gaps

- `xd://lsp` returned **No such tool**. No LSP status, semantic references, definitions, or diagnostics endpoint was available. The fallback was targeted literal search and direct source/diff reasoning; search matches are not represented as semantic caller proof.
- One frozen case was measured. No new source-shaped probe, mutation test, build, lint, formatter, smoke, full oracle/corpus execution, old-tool rerun, live host probe, or package operation was performed. No tools were installed or updated.
- This result establishes only bounded static command-history agreement for the standard same-instance repeated `.run()` form. It does not establish all scheduled lifetime semantics, aliased/distinct-instance behavior, Timer behavior, conditional targets, subclasses, downstream control flow after an exception, cross-cell behavior, resource scaling, C2 arithmetic, or no-harm on the historical population.
- There is no saturation, rerouting, or resume claim in this case; no orchestration runtime, routing table, or admission state was changed. The r19/r20/r21 rejected-harmed receipts and streak remain authoritative. L1 retains planning/integration authority, and non-author admission requirements remain outstanding outside this seat's scope.

Report: .ufo/waves/round-22/w2/reports/FalsifyC107.md
