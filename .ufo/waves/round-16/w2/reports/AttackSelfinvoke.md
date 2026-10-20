# AttackSelfinvoke — `tools/mado-action-plan.py --selftest`

Seat: MadoR16.AttackSelfinvoke (leaf reviewer, read-only). Target root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Method: source reading only. Read `tools/mado-action-plan.py` (752 lines), `.ufo/waves/round-16/safety-policy.json`, `.ufo/waves/round-16/safety-cases.json` (31 cases), `.ufo/waves/round-16/measure.py`, `.ufo/waves/round-16/frozen/*`, `corpus/lessons/round-15-verifier-spotcheck.md`, and the SKILL.md gate row (line 529–530). `sha256sum` and `cat` were run on the frozen fixtures only as byte reads. No gate, selftest, frozen replay, measure, or probe was executed. No installs. No edits outside this report.

Anchors use `tools/mado-action-plan.py` line numbers unless stated.

## Direct answer to the assignment

`--selftest` does invoke the actual CLI. `_self_invoke` (463–470) runs `[sys.executable, "-I", script, ...]` with `shell=False`, `stdin=DEVNULL`, a 60 s timeout, a temp cwd, and a minimal env. Each of the 40 fixtures (35 plan/policy at 491–614, 5 frozen at 674–704) carries literal `want_code` and `want_finding` in its own tuple. The assertion (636–638 and 709–711) requires `returncode == want_code AND parsed JSON finding == want_finding AND "Traceback" not in stderr`. No assertion rests on a helper alone; `_parse_finding` only decodes CLI stdout. The code-plus-finding pin requirement is met.

The gaps below concern what the selftest does not pin. Its pinned expectations are correct against the source as I read it. The gate itself is not shown to be wrong. Mutant claims are reasoned from code, not executed.

## Findings, by severity

### F1 — MEDIUM: selftest never exercises the committed policy file; its policy is generated from the same constants the gate checks

- `_canonical_policy` (446–460) is built from `PINNED_PAUSED_SCOPE`, `PINNED_DENY_EXECUTABLES` and the kinds table, and every fixture uses it, including `policy-shrunk-deny-exec` (602–605), which is also derived from the constant.
- The SKILL gate row (SKILL.md:529) documents the operational command `--policy .ufo/waves/round-16/safety-policy.json`. No selftest fixture reads that path.
- Counterexample A: add `"pkexec"` to `PINNED_DENY_EXECUTABLES` (109–112). `_canonical_policy` follows the constant, so every literal fixture still passes and `--selftest` stays green. The committed `safety-policy.json` lacks `pkexec`, so `_validate_policy` (248–250) returns `policy_malformed`. Every real run of the documented command exits 2 while the selftest reports 40/40. Fail-closed, but the green gate is false.
- Counterexample B: edit the committed JSON only (for example, drop `"sudo"` from `deny_executables`). Runtime exits 2 for every plan; selftest is still green.
- The strictness of the validator itself is covered: a mutant that removes the `deny` set-equality check (248) is killed by `policy-shrunk-deny-exec`.
- Fix (not applied): add one self-invocation case that passes the committed policy path and asserts `plan_safe`/0, and assert the committed bytes validate.

### F2 — MEDIUM: the independent cases file is executed by nothing

- `safety-cases.json` (31 cases, author MadoR16.SafetyCases) has no runner. I searched `tools/`, `SKILL.md`, `SCORECARD.md`, `corpus/`, and `.ufo/waves/round-16/`. Its only consumer is `measure.py` lines 362–366, which hashes it with `'executed': False` and `'scored': False`.
- The file's assumptions say `expected_code` is authoritative and that findings should be reconciled to the gate, not retrofitted. Nothing performs that reconciliation.
- I checked each case against the source by reading. All 31 expectations match the implementation. The verification gap is that they can never fail.
- Cases present only in `safety-cases.json` (not in the selftest's 40): `policy_paused_numeric_one` (`paused: 1`), `missing_actions_list` (`plan: {}`), `argv_not_a_list` (`argv: "cat corpus/SOURCES.md"`), `policy_extra_allow_key`, `read_source_hyprctl_version_r15_probe`, and `read_source_libinput_debug_events_help` (`/usr/bin/libinput`). Several of the mutants in F3 are killed only by these cases.
- Fix (not applied): either wire `safety-cases.json` into `run_selftest` (or a sibling runner) or stop calling it an executed expectation set. Its present SKILL/measure framing ("SafetyCases" cases) overstates what runs.

### F3 — MEDIUM: surviving mutants (no selftest fixture distinguishes them)

Each item is a mutation that leaves every one of the 40 selftest fixtures green. I reasoned each from the cited lines.

Fail-open (exit changes toward 0):

1. **String `argv` accepted.** If `_is_str_list` (218–219) drops its `isinstance(value, list)` check, a string `argv` iterates as characters and passes. `{"kind":"read-source","argv":"sudo cat x"}` then has `argv[0] == "s"`, is not denied, and returns `plan_safe`/0. Only `safety-cases.json` `argv_not_a_list` (which expects 2/`plan_malformed`) kills this mutant, and it is not wired (F2).
2. **Missing `actions` defaults to `[]`.** With `actions = plan.get("actions", [])` (293), `{"schema":"mado-action-plan-v1"}` becomes `plan_safe`/0 instead of 2/`plan_malformed`. Only `safety-cases.json` `missing_actions_list` covers this.

Fail-soft / availability:

3. **`S_ISREG` check (159–160) is masked.** The selftest's only non-file case is `plan-is-directory` (564–565, 631–632). Removing the check still returns 2/`plan_malformed`, because the directory's `os.read` raises `IsADirectoryError`, caught by the outer `except OSError` (175–176). No FIFO fixture exists. Without the check, a FIFO with a silent open writer makes `os.read` raise `BlockingIOError` forever, and the `except BlockingIOError: continue` (166–169) spins. The selftest would then hit its 60 s `TimeoutExpired` in the parent as a traceback, which no fixture pins.
4. **16 MiB bound (161–162)** has no oversize fixture.

Validator branches with no fixture:

5. **Numeric `paused`.** `type(paused) is bool and paused is True` (234) can be weakened to `paused == True`, which accepts `1`. No selftest case sets `paused: 1`; only `safety-cases.json` `policy_paused_numeric_one` does.
6. **Non-string `kind`** (302–304): no fixture. Removing the check turns exit 2 into exit 1 (`unknown_action_kind`), which the selftest would not see.
7. **Non-object action** (297–298): no fixture. Removing the check yields a `TypeError` traceback, exit 1.
8. **Non-list `actions`** (294–295), e.g. `"actions": {}`: no fixture. Removing the check yields `plan_safe`/0 for `{}`.
9. **`schema` checks**: plan (291–292) and policy (231–232) have no wrong-schema fixture.
10. **Duplicate deny entries** (246–247): a 13-entry list with one duplicate still set-equals the pin. No fixture.
11. **Unknown keys inside a `kinds` rule** (262–264): no fixture.
12. **`argv_nonempty` non-bool** (270–271): no fixture. `0 != False` is `False`, so a `0` value for a pinned-`False` kind is accepted without the type check.

Frozen mode (`run_frozen`, 380–430):

13. **Policy digest pin.** The loop (414–422) covers plan and policy, but `frozen-tampered-plan` (687–691) tampers only the plan. Removing the policy tuple entry from the loop survives.
14. **Plan pin mandatory check.** `frozen-missing-pin` (692–697) drops only `policy_sha256`. Dropping `plan_sha256` from the mandatory-key loop (400–404) makes `expected["plan_sha256"]` at 405 raise `KeyError` (traceback, exit 1). No fixture drops `plan_sha256`.
15. **Expected field types and envelope**: `expected_exit` as bool/string (409–411), unknown keys (393–396), wrong `schema` (397–399). No fixtures.

Verdict envelope:

16. **Unasserted fields.** The selftest checks the process exit and the JSON `finding`. It never checks the `MADO_PLAN:` line, the JSON `exit`, `action_index`, `action_kind`, `detail`, or `schema`. The docstring's Verdict API (35–39) is therefore unpinned. A mutant that corrupts `action_index` (for example, always 0) survives. Multi-action "first refusing action" is pinned only by its finding, not its index.

Count integrity:

17. **Case count is not pinned.** `SELFTEST_SUMMARY` prints `passed/total` (720–722) but no fixture compares total to a fixed number. Deleting a tuple from `cases` produces a lower total and exit 0.

Killed mutants (for balance): removing the `basename` step (fixture `read-disguised-pacman`), reversing first-refusal (`first-refusal-wins`), removing the unknown-kind guard (`unknown-kind`, which turns into a traceback and fails the no-Traceback check), removing `sudo`/`bash`/`env` deny entries (`read-sudo`, `read-shell`, `repo-env-wrapper`), and removing the duplicate-key parse hook (`plan-duplicate-key`) are killed by the current fixtures. Removing the non-finite parse hook is **not** killed: `NaN` then fails `_is_str_list` (218–219) and still yields 2/`plan_malformed`, so `plan-nonfinite` is masked by the schema check and does not pin the hook.

### F4 — LOW (design, not selftest-detectable): frozen mode verifies one read and evaluates another

- `run_frozen` hashes `plan.json` and `policy.json` at 416 and compares them to pins at 420–422. It then calls `_evaluate(plan_path, policy_path)` at 424, which re-opens and re-reads both files (356, 364).
- A writer that changes either file between 416 and 424 makes the replay evaluate bytes whose digest was never checked. `frozen_match` (426–427) then asserts a verdict about unpinned bytes.
- The threat model is local and requires write access to the frozen directory, so the severity is low. The SKILL row (529–530) and the docstring call this a "digest-bound" run, so the claim is stronger than the code.
- Fix (not applied): evaluate from the verified byte buffers (`_load_json` on the already-read bytes), not from paths.
- The selftest cannot detect this (static fixtures, no race).

### F5 — LOW (documentation, outside `--selftest`): SKILL row claims a receipt that is not in the tree

- SKILL.md:530 says "receipt separately binds executable and expectation digests." No receipt file exists under `.ufo/waves/round-16/frozen/` (the directory holds `expected.json`, `plan.json`, `policy.json`). A grep of `frozen/`, `fixtures/`, and the gate for "receipt" returns nothing.
- Also `fixtures/tight-green.json` and `fixtures/tight-red.json` are not referenced by the selftest or any runner I found.

## Equivalent or dead branches (not test gaps, but relevant to what "paused" means)

- **`paused` has no verdict effect.** The paused branch (332–334) returns the same finding, code, and index as the disposition branch (335–337) for each of the four paused kinds, which are exactly the four `disposition: deny` kinds in the pinned table. Removing the paused branch changes only `detail`. The validated `paused: true` flag is therefore decorative for verdicts. The `safety-cases.json` assumption that "paused" is what blocks mutation kinds is true only by coincidence of the disposition table.
- **`argv_nonempty` branch** (338–340) is redundant with the empty-`exe` check (341–344) for allow kinds.

## Declared classifier limits (checked, not defects)

- `_basename` (311–316) is lexical. `"sudo\u200b"` and `"\u0000sudo"` are not stripped and are not denied. The docstring (6–13) declares this, and the gate's own `safety-cases.json` residual controls (`omarchy-pkg-add`, `python3 -c`) pin the unscreened boundary. An executable with a zero-width or NUL argv[0] is not a real execution bypass in Python's `subprocess` (embedded NUL raises), but no fixture pins this boundary either way.
- Only `argv[0]` is screened. `["cat", "sudo"]` is `plan_safe` by design.

## Verification gaps (for L1)

- None of F1–F3 is a runtime defect in the current tree on my reading. F1 and F2 are false-green and unexecuted-expectation gaps. F3 items 1–2 are the only fail-open mutants I found, and both are reachable only by removing validator logic.
- L1 should confirm with one run (not performed here): `--selftest` 40/40, and `--plan` against the committed policy with a clean plan (expect 0/`plan_safe`). The second is the run F1 says the selftest never makes.
- L1 should not treat `safety-cases.json` as an executed check until F2 is resolved.

## Tooling

No tools were installed, updated, or upgraded by this seat. No pacman or service operation was performed. Frozen-fixture digests were read with `sha256sum` only (plan `82bc7652…`, policy `fb134d8f…`, both match `expected.json` pins; policy matches `safety-policy.json` byte-for-byte).
