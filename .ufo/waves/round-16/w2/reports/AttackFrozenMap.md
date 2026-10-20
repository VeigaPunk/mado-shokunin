# AttackFrozenMap — round 16 w2 (mado)

Seat: `MadoR16.AttackFrozenMap` (reviewer, leaf, no dispatch). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: falsify two claims against integrated artifacts: (a) `frozen_match` means recorded comparison, not a safe plan; (b) SKILL.md action-plan registry exit classes match `tools/mado-action-plan.py`.

Method: source reading; read-only `sha256sum` on four files; `git status --porcelain` and `git log -1`. No gate, selftest, frozen run, probe, package, service or compositor operation. No installs. No files other than this report written.

Artifacts read: `tools/mado-action-plan.py` (sha256 `9537e6c13f4ae198c4ea3d242583dca3ee02a473bbc99f209a4a8428f5d40fd0`, mtime 05:53), `.ufo/waves/round-16/frozen/{expected.json,plan.json,policy.json}`, `.ufo/waves/round-16/safety-policy.json`, `.ufo/waves/round-16/safety-cases.json`, `.ufo/waves/round-16/fixtures/tight-{red,green}.json`, `SKILL.md:518-542`, `SCORECARD.md:696-709`, and w1 reports ExitMap, FrozenDesign, FrozenInputs, GateRegistry, SafetyReceipt, plus round-13 ReviewRegistry F4.

## Axes

- A1 `frozen_match` semantics: what exit 0 claims.
- A2 registry-to-code exit agreement, all modes.
- A3 snapshot integrity: what the pins bind, and to what anchor.
- A4 fail-closed ordering and input I/O.

## Findings, by severity

### F1 — High: registry cites a receipt that does not exist; frozen pins are co-located and self-consistent

- Claim: `SKILL.md:530` says `expected.json` "pins plan/policy input bytes and exact expected code/finding; receipt separately binds executable and expectation digests to measured commit."
- Reality: no such receipt exists. `round-16/w1/reports/SafetyReceipt.md:9` reads "draft; the receipt cannot bind a gate digest yet." `git status --porcelain` shows `?? tools/mado-action-plan.py` and `?? .ufo/waves/round-16/`. HEAD is still `32c4fda` (baseline). No committed revision binds the gate, policy, cases, or frozen DIR.
- Code: `tools/mado-action-plan.py:386` loads `expected.json` from the same DIR. Lines 405-406 take the pins from it. Line 416 hashes the files against those pins. `_EXPECTED_KEYS` (127-129) only checks shape. Nothing outside the DIR pins `expected.json`.
- Counterexample (by reading; not executed): the committed DIR is consistent today. `sha256(frozen/plan.json)=82bc76520ee23804f20efb106df61023c30c2b74447ade39953a493a035febc3` equals `plan_sha256`. `sha256(frozen/policy.json)=fb134d8f90d1bb4afbe11df874b5605024aeb2da64b393ed2c7536c15b18b7fc` equals `policy_sha256`, and matches `safety-policy.json`. Anyone who can write `frozen/` can replace `plan.json`, set `plan_sha256` to the new bytes, and set `expected_finding`/`expected_exit` to the new plan's computed verdict. The run then returns `frozen_match`, exit 0, over bytes no committed artifact pins.
- Declared or not: the docstring (`:65-66`) says "both input digest pins are mandatory" and does not say the pins are self-contained. The registry asserts an anchor that is absent. This matches ExitMap M3, FrozenDesign F1 and FrozenInputs E2 from w1, none of which landed.
- Impact: the "digest-bound frozen run" second-evidence claim (`SCORECARD.md:706-707`) has no anchor beyond co-location.
- Fix (L1): either commit the gate digest and `expected.json` out-of-band, from a process other than the runner, and write the receipt at a measured commit; or rewrite `SKILL.md:530` to "co-located consistency check; not provenance."

### F2 — Medium: selftest failure exits 1; registry matches code but contradicts the lane's stated convention

- Code: `tools/mado-action-plan.py:723` `return 0 if not failed else 1`, propagated by `main` at `:742-743`. The docstring (`:67`) lists `--selftest` with no exit codes.
- Registry: `SKILL.md:529` says "same script `--selftest`; 0 clean, 1 failed". This matches the code.
- Convention conflict: `round-13/w1/reports/ReviewRegistry.md:29-31` (F4) says "A red self-test is not `1`." The same SKILL table gives selftest failure exit 2 for `mado-verify` (`:520`), `mado-frozen-regression` (`:523`) and `mado-frozen-regression-r14` (`:528`). Only `mado-source-merge` (`:524`) uses 1. The frozen row (`:530`) defers to "same script `--selftest`", so it inherits 1.
- Consequence: a red selftest prints `SELFTEST_SUMMARY ... failed=[...]` and exits 1. A consumer keyed on the registry reads that as "1 failed = declared plan refused." Uncaught exceptions inside selftest, such as `subprocess.TimeoutExpired` from `_self_invoke` (`:470`, timeout 60), also exit 1 by default. See F8.
- Fix (L1): pick one code. ExitMap M4 recommends 2. If 2 is chosen, change `:723` and the registry row together.

### F3 — Medium: tampering with `expected.json` returns 1 `frozen_verdict_mismatch`, not 2 `snapshot_tampered`

- Counterexample: edit `frozen/expected.json` `expected_exit` from 1 to 0 and leave the inputs alone. Both input digests still match, so the flow reaches replay at `:424`. The replay computes 1. Lines `:428-430` return `frozen_verdict_mismatch`, exit 1.
- The registry maps exit 1 to "failed comparison" (`SKILL.md:530`). A snapshot edit therefore reads as a verdict about the plan.
- FrozenInputs T13 forbids exactly this outcome (`FrozenInputs.md:89`, forbidden "1 frozen_verdict_mismatch"). R-5 (`:62`) requires an out-of-band pin on `expected.json`. Not implemented. The spec sentence only assigns exit 2 to input-digest tampering, so this is a design gap rather than a literal spec violation.
- Fix (L1): pin `expected.json` out-of-band (R-5), or state the T13 mapping in `SKILL.md:530`.

### F4 — Medium: frozen stdout carries classifier finding tokens; FrozenInputs §4 output mitigation not implemented

- Code: `:426-427` `detail=f"frozen verdict {want_finding}/{want_exit} matched"`. `want_finding` comes from the unpinned `expected.json`.
- Output: a green frozen run prints `"detail": "frozen verdict plan_safe/0 matched"` under exit 0. The committed red frozen DIR prints `denied_executable:sudo/1` under exit 0.
- FrozenInputs §4 (`:54`) asked that a frozen run print no classifier finding token, so a naive caller cannot read exit 0 as safe. The textual mitigation is present (`SKILL.md:540-541`: "Frozen match means recorded comparison matched, never that a red plan is safe"). The output-level mitigation is not.
- The detail string echoes the expectation, not a computed value.
- Fix (L1): drop the expected finding from the detail, or print a non-classifier token such as `frozen_compared` in place of the finding.

### F5 — Low-Medium: frozen replay re-reads inputs by path after the digest check (TOCTOU; R-4 unmet)

- `:416` `_sha256(path)` reads and hashes the file. `:424` `_evaluate(plan_path, policy_path)` reopens both by path. Bytes can change between the two.
- Bounded: `_evaluate` re-validates the policy against pinned constants (`:360`, `_validate_policy` `:224-281`). A substituted plan must still produce the pinned expected finding and exit to return 0. The effect is `frozen_match` over unpinned bytes of the same verdict class, not a policy bypass.
- Fix: read once, then parse and classify the same buffer (FrozenDesign F2; FrozenInputs R-4).

### F6 — Low: symlinks followed; extra DIR entries ignored

- `:154` `os.open(path, O_RDONLY | O_NONBLOCK)` has no `O_NOFOLLOW`. `:159` `S_ISREG` tests the target. Symlinks to regular files are accepted.
- `run_frozen` reads only the three named paths. There is no `scandir` (FrozenInputs R-2, T11). A stray `plan.json.bak` is ignored, not rejected.
- The docstring (`:150-152`) says "Read a regular file only" and does not address symlinks. This is compatible with the code's declared text but not with the R-2/R-3 design (T09 expects `snapshot_tampered`).
- Verdict impact: extra entries cannot change the verdict. A symlinked plan or policy is accepted only when its target bytes match the pins.

### F7 — Low: `--policy` silently accepted with `--frozen` or `--selftest`

- The mutually exclusive group (`:732-738`) covers `--plan`, `--frozen` and `--selftest`, not `--policy`. `main` (`:744-745`) returns `run_frozen` and ignores `args.policy`. FrozenInputs R-1 asked for usage exit 2.
- No verdict impact: frozen mode uses the DIR's `policy.json`, which is validated against the pinned constants.

### F8 — Low: no top-level guard; `--help` exits 0 with no verdict line

- `main` (`:728-748`) has no top-level exception guard. ExitMap H2 (`ExitMap.md:68-75`) asked for one. Not landed.
- Parse and I/O paths are guarded: `_load_json` catches `Exception` (`:206`); `_read_regular` catches `OSError` (`:155-176`).
- Unguarded paths are narrow. The selftest path `_self_invoke` (`:470`) can raise `TimeoutExpired`. Any uncaught exception exits with Python's default status 1, which the registry reads as "failed." [INFERENCE: Python default exit status; not executed.]
- `--help` exits 0 via argparse with no `MADO_PLAN:` line. A wrapper treating exit 0 as clean would accept it. Not listed in the registry row.
- Fix: a top-level guard mapping exceptions to 2, and either a non-zero or explicitly named exit for `--help`.

### F9 — Process: untracked artifacts and stale bytecode

- `tools/__pycache__/mado-action-plan.cpython-314.pyc` (05:46) predates `tools/mado-action-plan.py` (05:53). Both are untracked. The pyc shows an earlier revision was compiled or imported. No verdict impact, because `python3 -I script` does not read the pyc.
- Lane cleanup: remove `tools/__pycache__/` before commit.

## Verified by reading (no counterexample found)

- Plan row exit classes (`SKILL.md:529`) match code. 0 `plan_safe` (`_classify` `:348`). 1 `blocked_action_kind:*`, `denied_executable:*`, `unknown_action_kind`, `empty_argv` (`:319-347`, `EXIT_DENY`). 2 `plan_malformed` and `policy_malformed` (`:356-372`). argparse usage errors exit 2 (`:739`, `:747`).
- Frozen rows match code. `frozen_match` 0 (`:426-427`). `frozen_verdict_mismatch` 1 (`:428-430`). `snapshot_tampered` 2 (`:418-422`). `frozen_error` 2 (`:387-413`). Matches `SKILL.md:530` and the FrozenInputs §4 table.
- Frozen DIR is consistent with its own pins (digests verified this round). The expected `denied_executable:sudo`/1 is the code's computed verdict for the frozen plan: `argv[0]=sudo` under `read-source` (`:341-347`). By reading, a frozen run returns `frozen_match`, exit 0. This is the exit-0-for-a-refused-plan case that `SKILL.md:530` documents ("including expected refused plan").
- Committed `safety-policy.json` (and the frozen copy) satisfies `_validate_policy` exactly: `paused` true, paused scope and deny set equal the pinned sets, six kinds with pinned dispositions.
- `safety-cases.json`: all 25 cases traced through the code. `expected_code` and `expected_finding` agree with `_validate_plan`, `_validate_policy` and `_classify`. Includes first-refusal ordering (`multi_action_green_then_red` gives `blocked_action_kind:service-mutate`) and malformed-before-classify ordering. The `residual_control_*` cases (`omarchy-pkg-add`, `python3 -c`) return `plan_safe` by design.
- Tight fixtures (`fixtures/tight-red.json`: `sudo cat`; `tight-green.json`: `cat`) give `denied_executable:sudo` and `plan_safe` respectively by reading `_basename` (`:311-316`) and `_classify`.
- Declared classifier limits (exact basename only; wrappers, interpreters, operands unanalysed) match the docstring (`:9-13`) and `SKILL.md:533-539`. Not counted as defects.

## Residual risk

- F1 is the only finding that bears on the C2 "digest-bound frozen run" claim. Everything else is text, exit-class, or I/O hardening.
- Frozen-mode exit 0 for a refused plan is documented, but a `$?`-keyed consumer is still exposed to it. Registry and text documentation are the only mitigation.
- Nothing above was executed. Verdicts are predictions from reading.

## Verification gaps (for L1, once after integration)

- `python3 -I tools/mado-action-plan.py --selftest`. Confirm the exit for a red selftest (F2) and that the 25 cases plus frozen fixtures pass.
- `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen`. Predicted: `frozen_match`, exit 0, detail naming `denied_executable:sudo` (F4).
- Negative control on a copied DIR: edit `expected_exit` and predict 1 `frozen_verdict_mismatch` (F3). Replace `plan.json` with a symlink to an identical copy and predict acceptance (F6).
- Commit gate, policy, cases and frozen DIR with a recorded sha; then re-check the `SKILL.md:530` receipt claim (F1).
- Remove `tools/__pycache__/` before commit (F9).

## Tooling record

No install, update or package operation this seat. Read-only only: `sha256sum` on four lane files, `git status --porcelain`, `git log -1`. No gate, selftest, frozen run, probe, service or compositor operation.
