# C1 falsification — OriginalF5ThreadKeyControl

**Verdict: agree, bounded to this frozen passing control.** Author-lane advisory evidence only; no admission grant. The assignment targets delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; this measurement identifies the actual selected bytes by the fixed C1 SHA-256 below, not by a fresh revision query.

**Axes:** complete semantic row fidelity; observed/lead calibration; callable identity and lifetime hygiene; bounded reproducible provenance; read-only/scope integrity.

## Independent expected semantics and authority

The exact case in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` is `supplemental-original`, `expected_kind: exact`, with `proposal: null`. Its source citation is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-control.jsonl`. The original and frozen input hashes are identical. The source-authoritative table at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:49-60` already calls this a passing control. I did not rerun the historical tool or reinterpret the original red receipts.

The single inert Python cell imports `subprocess` and `threading`, binds `__hyg_spawn = subprocess.run`, defines a zero-argument `worker` whose only call passes the literal argv `["pacman", "-Q", "r21-hyg"]` to that alias, then unconditionally calls `threading.Thread(target=worker).start()`. The definition alone does not execute the body. The newly constructed standard Thread captures that precise worker, and its visible start supplies the modeled invocation. No alias rebinding, factory frame, conditional target, unknown argument, subclass, cancellation, namespace reset, or shared mutable captured value intervenes. The worker's free global alias remains the spawn callable when it is invoked.

Thus the complete expected class/command/evidence multiset has exactly one row:

| Class | Command | Evidence | Multiplicity |
|---|---|---|---:|
| `package_query` | `pacman -Q r21-hyg` | `observed` | 1 |

`-Q` is a package query, not a host mutation. There is no second command and no reason to downgrade this resolved scheduled call to a lead under the declared static-source contract. Here `observed` is the scanner's source-path evidence tier, **not** proof that a real thread, subprocess, or package query ran. Payload code was only parsed.

The frozen case has `accept_exact_want: null`, empty forbidden-command lists, and `require_signal: true`. This is not an uncertain case: exact evaluation requires the entire sorted multiset and zero error counters. A lead-only result, missing row with clean parsing, duplicate row, extra invented argv, or wrong class/evidence would fail. `require_signal` does not require adding a lead to an exact result. The unknown-case `accept_exact_want` escape and all-tier forbidden-command rules do not alter this case's exact requirement; I did not substitute clean parsing or generic uncertainty for its true command.

## Authorized measurement and actual output

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case OriginalF5ThreadKeyControl
```

The runner configures one scanner child with `RLIMIT_AS = 402653184` bytes (384 MiB) and a 15-second timeout. It validated the frozen population before and after (57 input files, 52 proposal files, 106 sealed source files), but **executed only this one case**, not 57 cases. Both integrity records agree and `integrity_errors` is empty.

Actual complete finding row:

```json
{"argv0":"pacman","class":"package_query","command":"pacman -Q r21-hyg","evidence":"observed","file":"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/OriginalF5ThreadKeyControl.jsonl","line":1,"rule":"pacman:-Q","timestamp":"None","tool":"eval","tool_call_id":"FBR-thread-key-control"}
```

- Runner exit **0**, status `complete`, totals **1/1 pass**, no comparison reasons.
- Scanner exit **1**, because its one query finding is unpermitted; this is not a runner failure. Both runner and scanner stderr are empty; `scanner_error` is null.
- `observed_findings: 1`, `lead_findings: 0`; all other class counts are zero.
- Sole file: one line, one eval call, zero bash calls, `eval_unparsed: 0`, `unparsed_spawns: 0`; reported fixture path and SHA-256 match the selected frozen input.
- Full sorted row multiset equals the expected singleton. No lost true command, invented command at either evidence tier, false promotion/demotion, duplicate, wrong tool-call identity, or parsed-clean omission appears in this measurement.

Raw outer argv/exit/stdout/stderr, scanner argv/exit/stdout/stderr and payload, runner integrity records, and external before/after hash observations are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC156/result.json`. The actual outer invocation includes `-I`; the runner's self-reported `sys.argv` naturally does not include that interpreter flag.

## Identity and restoration evidence

Independent `sha256sum` calls before and after the sole measurement returned identical values:

| Artifact | SHA-256 before = after |
|---|---|
| C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Frozen fixture | `00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be` |
| Original source fixture | `00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be` |
| Sealed expected JSON | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |

The C1 tool and sealed expected JSON match the task's fixed identities. The runner's population digest is `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. No drift was observed. No production, fixture, expected, proposal, gate, or source file was modified. Restoration is therefore not applicable: no mutant bytes existed to restore, and the measured source/fixture artifacts remained hash-identical. No tools were installed or updated.

## One minimal proposed fault — not executed

**Recipe:** in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2481`, delete only `target.mado_resolved = info["target"]` in the `scheduled_invoke` branch; leave the synthetic `Name` and invocation intact. This is a plausible one-line callable-identity regression during synthetic-call refactoring.

**Expected detector:** the same frozen one-case command above must reject disappearance of the sole observed query. [INFERENCE] Without that assignment, `callable_info` has no node-carried identity to return at lines 1728–1730; its later Name lookup cannot resolve the non-source identifier `<scheduled target>`. The synthetic call cannot follow `worker`. The Thread-constructor reference exemption at lines 2731–2734 does not recover an observed target execution. Even an otherwise clean, empty result fails the exact full-multiset detector.

**Mutation outcome:** recipe only; no mutation was applied or run, so there is **no killed/survived result**. No extra scanner measurement or payload execution was performed.

## Limits relative to C1 and F5

The relevant current path resolves standard `.start`/`.run` methods at lines 1784–1792, captures targets at lines 1841–1853, and carries the scheduled target on a synthetic AST node at lines 2470–2486 rather than inserting a legal source identifier into the binding namespace. This source reading explains the observed control result; it is not universal Python-semantics proof or a repository-wide hygiene audit.

Crucially, this case uses the noncolliding alias `__hyg_spawn` and already passed before the repair. Its green cannot distinguish the old `__mado_thread_target__` collision defect from a sound implementation, cannot establish that all legal source identifiers are collision-free, and cannot close the original F5 red by itself. No new source-shaped case was created. Other lifetimes, conditional targets, dynamic calls, schedules, prior-corpus no-harm, resource scaling, C2, and admission remain outside this one-case result. Original r19/r20/r21 rejected-harmed authority and streak are unchanged.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC156.md
