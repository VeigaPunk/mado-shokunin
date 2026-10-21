# FalsifyC151 — C1 single-case falsification: OriginalF1CaptureInvokeTime

Seat: MadoR22.FalsifyC151 (leaf, read-only). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Round 22 recovery, C1 bounded static lifetime/callable/scheduled repair. Delivered revision as stated in the assignment: 71228fd582d6d9338d7916cc64e69bd4c2e928b5 (taken from the assignment; not independently checked, no git commands run).

## Verdict

- Sealed expectation versus independent static truth: **AGREE**. One `host_mutation` / `pacman -S r21-factory` / `observed` row; no other command is executed.
- Actual C1 output for this case: **AGREE**. Measured rows equal the sealed want exactly; zero unparsed counters; empty stderr; runner pass 1/1.
- Scope: one of 57 frozen cases. This is not a C1 pass and grants no admission.
- Residual, **unknown** (not probed): this fixture cannot separate call-time capture from a first-module-assignment heuristic, since both yield `pacman -S`. It does separate invocation-time binding (the r21 F1 defect), which the output does not exhibit.

## Independent truth (from inert source, reasoned before the run)

Source: eval cell `FBR-capture-invoke-time`, one cell, reset=false. Read as AST text; never executed.

```python
import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
cmd = ["pacman", "-S", "r21-factory"]
runner = make(cmd)
cmd = ["pacman", "-Q", "r21-invoke"]
runner()
```

1. `make(cmd)` binds parameter `argv` in make's frame to the list object currently named by `cmd` (list A = `pacman -S r21-factory`).
2. `run` closes over `argv` (a cell of make's frame), not over the module name `cmd`.
3. The later `cmd = [...]` rebinds the module name to a new list B. It does not mutate A, and B reaches no call. B is never executed.
4. `runner()` unconditionally, at top level, calls `run`, which executes `subprocess.run(argv)` with A. The cell has no branch, loop, default, starred or keyword dynamics, and no opaque construct (exec, eval, globals, import *).
5. `subprocess` is the real module import: a free global, unchanged, late-bound at call time.

Conclusion: exactly one executed command, class host_mutation, evidence observed. No lead row. No row for `pacman -Q r21-invoke` at any tier.
Uncertainty: none is warranted. A lead or an uncertain alternative would under-claim a definite execution, so exact kind with `accept_exact_want: null` is the right semantics. A failed `pacman` spawn would not change this: the invocation is still observed.

Sealed record (expected.json, case OriginalF1CaptureInvokeTime): group supplemental-original; expected_kind exact; want `[host_mutation | pacman -S r21-factory | observed]`; accept_exact_want null; forbid_observed_commands `[]`; forbid_commands_any_tier `[]`; require_signal true (see G1); cell_count 1; cell_reset `[false]`; fixture inputs/OriginalF1CaptureInvokeTime.jsonl, input sha256 6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7, byte-identical to the r21 source capture-invoke-time.jsonl; table_row F1 (FinalBindingReview.md line 55: "Wrong command. Host mutation missing."). The historical r21 row `package_query pacman -Q r21-invoke observed` is retained as known-red context only, not used as truth.

## Single run

- Argv (receipt): `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case OriginalF1CaptureInvokeTime`, cwd lane root. Runner-recorded sys.executable is /usr/bin/python3.
- Exit 0. Elapsed 0.107 s. Stderr empty (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). Stdout 5490 characters, one JSON line (sha256 52eb4a38431d1b777ad67a7d795b77d4f7b9d5854cc5ea895da368d37e0fbcee). Status complete; totals pass 1/1; integrity_errors `[]`.
- One scanner child, under the runner's caps (RLIMIT_AS 384 MiB, 15 s): `/usr/bin/python3 -I -c <WRAPPER> tools/mado-tripwire.py inputs/OriginalF1CaptureInvokeTime.jsonl`. WRAPPER loads the tool and calls `main(["--scan", fixture])` with no `--permit`. Scanner exit 1 (unpermitted finding), stderr empty, stdout `MADO_TRIPWIRE: findings` plus one JSON line.

Actual rows (identical to sealed want):

| class | command | evidence | rule | line | tool_call_id |
|---|---|---|---|---|---|
| host_mutation | pacman -S r21-factory | observed | pacman:-S | 1 | FBR-capture-invoke-time |

Scanner counters: counts host_mutation 1, all other classes 0; observed_findings 1; lead_findings 0; permitted `[]`; unpermitted 1. files row: eval_calls 1, eval_unparsed 0, unparsed_spawns 0, lines 1, sha256 6b21d584…f7 (matches sealed input). Runner: got_rows equals want; unparsed 0; reasons `[]`; scanner_error null.

Hashes, before equal after across the run:
- tools/mado-tripwire.py `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches fixed C1 identity)
- oracle/measure.py `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` (= expected.runner_sha256)
- oracle/expected.json `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches fixed oracle identity)
- oracle/expected.sha256 `7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6`
- .ufo/waves/round-22/truth-seal.json `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`
- inputs/OriginalF1CaptureInvokeTime.jsonl `6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7`
- Population (runner integrity_before and after): 57 inputs, 52 proposals and 106 sealed sources verified; population_sha256 `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`; producer_sha256 `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600`.

Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC151/result.json` (argv, exit, full stdout and stderr, hashes before and after, parsed runner JSON).

## Falsification attempts on this case

| Attack | What was checked | Result |
|---|---|---|
| False observed/lead argv | any `pacman -Q r21-invoke` row at any tier; any lead row | Not found. One row, observed. |
| Lost true command | presence of `pacman -S r21-factory` as observed | Not lost. |
| Evidence downgrade | evidence marker of the -S row | observed, not lead. |
| Wrong identity | class and command text exact; file sha equals sealed digest; tool_call_id equals sealed id | Not found. Fields outside the comparator: rule, argv0, line, and timestamp, which is the string `"None"` (scan_file line 2890). |
| Lifetime (invocation-time versus factory-call binding) | the stale -Q row is the F1 defect | Not reproduced. Source path (read, not probed): factory_result (1642-1684) takes `bound = bind_literal(owner, call, env)` at the call-site env (1652) and stores it in closure_env (1678-1683); spawn_scan applies closure_env at invocation (2511-2516). |
| Conditional target | branches; return form | None. The return is a bare Name, a supported form. Not applicable. |
| Parsed-clean ambiguity | eval_unparsed, unparsed_spawns, stderr, exit | Zero unparsed, empty stderr, exit 1 accepted. Oracle gap G2 below. |

Residual, unknown (not probed): a first-module-assignment implementation would also return `pacman -S` here. This run shows invocation-time binding is absent. Call-time capture is the mechanism only by source reading.

Run-time note (read, not probed): under the 384 MiB cap, run_with_stack (3433-3438) shrinks the worker stack to 64 MiB. A worker start failure propagates to the `__main__` handler (3448-3463), which prints could_not_evaluate with exit 2. The runner treats exit 2 as an error (measure.py 687-688), so resource failure fails closed.

## Oracle observations (no verdict change for this case)

- **G1, require_signal is inert for exact cases.** evaluate() returns on the exact branch (measure.py 752-756) before reading require_signal. require_signal is read only in the uncertain branch (765-766). F1 pins `require_signal: true` (verify_original_cases line 455; ORIGINALS line 45), but nothing enforces it.
- **G2, verdict label, exit, counts, observed/lead totals and unpermitted are not bound to rows.** parse_scan_output (683-729) reads files[0] identity, the unparsed counters and findings. Exit 0 and exit 1 are both accepted (687-688). A scanner emitting this row with exit 0 or a `clean` label would pass. The current tool derives exit, label and counts from findings (verdict_of 2909-2914), so this is not triggered. The oracle does not check it.
- **G3, F1 has no explicit forbid for the stale command** (forbid lists `[]`, ORIGINALS lines 44-45). The exact multiset is the only guard, and its failure reason (754-755) does not name the extra command. Diagnostic weakness only.
- **G4, discriminator gap.** This fixture separates invocation-time from call-time binding, but not call-time from first-binding (see Residual).
- **G5, redaction of identity text.** redact() (2892; pattern at 304) rewrites any 32-plus-character `[A-Za-z0-9_-]` run in a command string. Not triggered here; a command-identity risk for other cases, not probed.

## Scope against the current C1 target

- Target (registration): all eligible frozen expectations match, all original reds resolve, no-harm guards hold. This run measures one case, OriginalF1CaptureInvokeTime, of 57 frozen cases (one of the 7 supplemental originals).
- Not measured: the other 56 cases (F2-F5, the F5 control, R19 pure frozenset, 50 eligible proposals); the 166/175 historical floor; the 1356-fixture removal comparison; resource recipes; old oracle 35+17; incident recall; existing suites.
- Population validation (57 inputs, 52 proposals, 106 sealed sources, truth seal, pins) is input integrity, not scanner measurement.

## Compliance

- Scanner executions: exactly one, the assigned command. No new probes. No reruns of old tools. No r21 known-red receipts executed.
- Fixture payload read as text only; never executed.
- Writes: `.ufo/waves/round-22/w2/receipts/FalsifyC151/result.json` and this report only. No production, fixture, expected, proposal, gate or registry edits. No git commands. No installs or updates. No package, service or process queries.
- Tool, runner, expected and fixture hashes unchanged before and after the run.

Report: .ufo/waves/round-22/w2/reports/FalsifyC151.md
