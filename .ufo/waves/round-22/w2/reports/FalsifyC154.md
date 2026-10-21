# FalsifyC154 — C1 OriginalF4ThreadRunDirect

## Verdict: agree, bounded to this frozen case

The delivered C1 scanner produced exactly the independently justified row for `OriginalF4ThreadRunDirect`, with both unparsed counters zero. This probe found no false observed/lead argv, lost true command, wrong target identity, lifetime error, conditional-target promotion, or parsed-clean ambiguity in this particular input. Agreement is with this case's semantics and complete expected multiset, not merely with a green oracle result. It grants no admission.

Axes: semantic class/command/evidence fidelity; target and capture-lifetime fidelity; complete-multiset and uncertainty accounting; immutable artifact identity; bounded, inert execution.

The assigned target is revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The selected tool's measured bytes match the fixed delivered C1 hash. No separate repository-revision check or other scanner run was performed.

## Independent truth and source authority

This case is `supplemental-original`, with `proposal: null`; its authority is the original round21 F4 source and report, not a newly authored proposal or the current scanner output:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-run-direct.jsonl`, line 1.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md`, table row F4 at line 58 and mechanism/contract at lines 90–95.
- Sealed case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`, case `OriginalF4ThreadRunDirect`.

The input imports `subprocess` and `threading`, defines `worker(argv)` containing exactly `subprocess.run(argv)`, constructs a standard `threading.Thread(target=worker, args=(["pacman", "-S", "r21-thread-run"],))`, then calls `t.run()`.

Static semantic reasoning:

1. Construction captures the visible `worker` callable and a one-element positional-argument tuple whose element is the literal argv list. There is no rebinding, intervening mutation, unresolved argument, or alternative target.
2. Calling the standard Thread instance's `.run()` directly invokes that captured target synchronously with the captured arguments. This is not an uncertain asynchronous scheduling opportunity and does not require `.start()`.
3. The reachable worker body passes the unchanged list to `subprocess.run`. There is exactly one reachable spawn site and one invocation. Defining the helper or supplying it to the constructor alone does not execute it.
4. `pacman -S r21-thread-run` is a package-install operation, hence `host_mutation`, not a package query. Its argv is fully known. `observed` is justified in the scanner's bounded static call-path sense; it does not claim any package manager was actually executed during measurement.

The independently justified complete multiset is therefore:

```json
[{"class":"host_mutation","command":"pacman -S r21-thread-run","evidence":"observed"}]
```

The original r21 authority reports an empty finding set with zero unparsed counters: a silent F4 miss. That reported red was not rerun or rewritten. This current single-case result repairs the named symptom on these bytes only; prior r19/r20/r21 rejected-harmed dispositions and other residual findings remain outside this probe.

## Authorized measurement and actual output

Exactly one measurement command was executed:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case OriginalF4ThreadRunDirect
```

The runner validates the sealed full population but selected and scanned only this one case. Its scanner subprocess is capped by `RLIMIT_AS=402653184` bytes (384 MiB) and a 15-second timeout. Fixture payloads and their printed command were never executed; the scanner only parsed the inert JSONL/Python source.

Actual normalized rows:

| class | command | evidence |
|---|---|---|
| host_mutation | pacman -S r21-thread-run | observed |

Actual raw finding identity: `argv0=pacman`, `rule=pacman:-S`, `tool=eval`, `tool_call_id=FBR-thread-run-direct`, `line=1`, and file `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/OriginalF4ThreadRunDirect.jsonl`.

- Runner exit: **0**; status: `complete`; totals: **1 passed / 1 measured**; integrity errors: `[]`; case reasons: `[]`.
- Scanner exit: **1**, meaning one unpermitted finding, not an evaluation failure.
- Scanner stdout begins `MADO_TRIPWIRE: findings` and includes its full JSON verdict, retained verbatim in the receipt.
- Runner stderr and scanner stderr: both empty; scanner error: `null`.
- `observed_findings=1`, `lead_findings=0`, `unpermitted=1`; `host_mutation=1`; all four other class counts zero.
- One input file, `lines=1`, `eval_calls=1`, `bash_calls=0`, `eval_unparsed=0`, `unparsed_spawns=0`.

The result is not an empty/clean finding report: it is a correctly detected mutation command. No extra row, duplicate, invented command, or lead substitution appears.

## Oracle and uncertainty boundaries

The sealed case is `expected_kind=exact`, `accept_exact_want=null`, with both forbidden-command lists empty. The runner's exact branch compares the complete sorted class/command/evidence multiset, including multiplicity, and requires zero combined unparsed counters after validating scan shape, exit, input path, and digest. `require_signal=true` does not turn this exact case into an uncertainty alternative; a lead-only result, missing row, extra row, evidence downgrade, or positive unparsed counter would fail exact comparison.

For uncertain cases the runner checks forbidden commands at all specified tiers before accepting an exact alternate or uncertainty signal. That distinction is not exercised here: this case has no `accept_exact_want` alternate and no genuine unresolved target or argv. An exact green on this input cannot establish the behavior of unknown/cancelled/racing schedules, conditional targets, subclasses overriding `run`, repeated invocations, mutable captures, dynamic argument binding, aliases, cross-cell lifetime, or other F4 forms. No new source-shaped probe was added.

Relevant current candidate path: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, lines 1784–1792 resolve `.run`/`.start` on scheduled receivers; lines 1840–1853 capture target/arguments at construction; lines 2470–2489 synthesize the captured invocation; lines 1726–1730 honor its resolved callable metadata; lines 2407–2439 and 2547–2580 follow the helper. Constructor-reference suppression at lines 2731–2734 makes the actual scheduled invocation responsible for the finding. Pacman classification at lines 775–780 agrees with the independent operation classification.

## Proposed minimal mutation — not executed

**Fault recipe:** in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1789`, replace:

```python
if node.attr in ("start", "run"):
```

with:

```python
if node.attr == "start":
```

This is a one-line behavior-bearing regression: it preserves `.start` handling but removes direct `.run` resolution for the scheduled receiver in this frozen case.

**Expected detector:** the identical bounded `measure.py --tool … --case OriginalF4ThreadRunDirect` command above, run by L1 later against a private mutant copy, should reject the missing required observed row through its complete-multiset comparison.

**Why this case should expose it:** [INFERENCE] `t.run()` would fall through to unresolved handling; it has no literal argv argument from which fallback leads could recover the command. The constructor-reference sweep remains suppressed, so the worker body would not be followed through that route. The expected regression is loss of the sole true observed row, plausibly the historical empty/zero-unparsed shape. The exact detector must fail even if fallback uncertainty differs from that prediction.

**Mutation verdict:** proposed and unexecuted. No mutant was edited, scanned, declared killed, or declared surviving. The actual observed verdict above concerns pristine delivered bytes only.

## Artifact identity and restoration evidence

Each value below was measured before and after the sole measurement; all pairs are equal, and required fixed identities match. `result.json` retains both complete hash maps and `drift={}`.

| Artifact | SHA-256 before = after |
|---|---|
| Selected C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Selected sealed fixture | `1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f` |
| Original r21 source fixture | `1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |

Restoration was unnecessary because no production, fixture, expected, or source bytes were edited. No restored-byte detector run was authorized or performed. Own writes were restricted to this report and the assigned receipt directory. No installs, old-tool runs, mutants, builds, linters, formatters, full suites, generic smokes, or other probes were performed.

Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC154/result.json` contains requested argv, actual exit/stdout/stderr, nested scanner argv/exit/stdout/stderr and payload, plus tool/fixture/runner and authority hashes. Exact raw runner stdout and empty stderr are retained in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC154/OriginalF4ThreadRunDirect-one-shot-20261021/`.

This is author-lane advisory evidence only. It neither supplies non-author falsification admission nor decides integration, shipping, historical streak disposition, C2, or general C1 completeness.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC154.md
