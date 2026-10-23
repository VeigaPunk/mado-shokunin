# CapFiniteDeclaredActionClas782 — C2 row re-run: SCORECARD.md:782 (`finite declared-action classifier`)

## Ledger line

`| SCORECARD.md:782 | finite declared-action classifier | Refuse blocked declared kinds, the 12 pinned argv[0] names, unknown kinds and malformed inputs; compare a digest-pinned declared-plan replay | observed at 41cc04c8: works — `--selftest` exit 0 `SELFTEST_SUMMARY: 52/52 passed`; `--frozen .ufo/waves/round-16/frozen` exit 0 `MADO_PLAN: frozen_match` (`frozen verdict denied_executable:sudo/1 matched`) | python3 -I tools/mado-action-plan.py --selftest; python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen | SCORECARD.md:1591-1592 (round-24 wave-2 correction) re-confirms the selftest as 52/52 exit 0 at 39c59630; no contradiction, --frozen not re-run there |`

## Row under test

- File at base: `git show 41cc04c8:SCORECARD.md`, sha256:6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08, 1618 lines.
- Location: `SCORECARD.md:782`, the single data row under `### Demonstrated capability` (`SCORECARD.md:778`) inside `## Round 16 — committed results and bounded author verdicts` (`SCORECARD.md:740`).
- Stated claim (row cells): refuse blocked declared kinds, the 12 pinned `argv[0]` names, unknown kinds and malformed inputs; compare a digest-pinned declared-plan replay. First-working round 16.
- Demonstration command named by the row: `python3 -I tools/mado-action-plan.py --selftest` (52/52) and `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` (frozen_match at corrected content).
- Evidence pointer named by the row: `evidence/action-selftest-final.json`, `action-frozen-final.json`, `committed-bindings.json` (resolved relative to `.ufo/waves/round-16/`; all three exist at 41cc04c8). The selftest receipt records `measured_commit 1e31681e76b5e7caadd1c749e18669a3632a1c3b`, `action_gate_sha256 226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`; `committed-bindings.json` binds `tools/mado-action-plan.py` sha256:226220ae…74 (39152 bytes) at that commit.

## Observation at 41cc04c8

Sandbox clone: `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapFiniteDeclaredActionClas782` then `git checkout -q --detach 41cc04c8` (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE unset). `HEAD` = `41cc04c8d593837a0d5078bffaacdaa163d12897`. The tool at base hashes sha256:226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3, byte-identical to the round-16 receipt; `git log` shows its last two touching commits as `1e31681` and `9dcf248` (both round 16), so no later round changed it.

Both commands named by the row ran as written, under `timeout 600` and `prlimit --as=4000000000`, in the clone (never in the lane), and both succeeded:

- `python3 -I tools/mado-action-plan.py --selftest` → exit 0; `SELFTEST_SCRIPT_SHA256: 226220ae…74`; 52 `SELFTEST PASS` lines; `SELFTEST_SUMMARY: 52/52 passed`. The suite includes denied-executable refusals (`pacman`, `sudo`, `bash`, `env`), blocked kinds, unknown kind, malformed plan/policy cases, symlink/FIFO plan paths, and frozen cases (`frozen_match`, `snapshot_tampered`, `frozen_error`, `frozen_verdict_mismatch`).
- `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` → exit 0; prints `MADO_PLAN: frozen_match` plus a `mado-action-plan-verdict-v1` JSON line with `"detail": "frozen verdict denied_executable:sudo/1 matched"`. The in-tree pins agree: `frozen/plan.json` sha256:82bc76520ee23804f20efb106df61023c30c2b74447ade39953a493a035febc3 and `frozen/policy.json` sha256:fb134d8f90d1bb4afbe11df874b5605024aeb2da64b393ed2c7536c15b18b7fc equal the `plan_sha256`/`policy_sha256` fields of `frozen/expected.json`; the tool compares plan and policy digests to those pins (`tools/mado-action-plan.py:427-437`).
- Supplementary (the round-16 section's own command list, `SCORECARD.md:747-750`, beyond the row's pointer): `--plan …/tight-red.json --policy …/safety-policy.json` → exit 1, `MADO_PLAN: denied_executable:sudo`; `--plan …/tight-green.json --policy …/safety-policy.json` → exit 0, `MADO_PLAN: plan_safe`. Both as the round-16 results row (`SCORECARD.md:756`) states.
- Claim-component check: `PINNED_DENY_EXECUTABLES` (`tools/mado-action-plan.py:109`) holds exactly 12 names — pacman, yay, paru, systemctl, hyprctl, omarchy, libinput, evtest, sudo, sh, bash, env — matching the row's "12 pinned argv[0] names"; the policy validator requires set equality with that pin (`:260-262`).

No command was unrunnable and no nearest-form substitution was needed.

## Supersession / contradiction grep

Grepped the whole `SCORECARD.md` at 41cc04c8 for `mado-action-plan`, `action-plan`, `52/52`, `SELFTEST_SUMMARY`, `classifier`, `Retired`. Findings relevant to this row:

- `SCORECARD.md:747-750` and `:756` — the same round-16 section's command list and results row: consistent, earlier in the file.
- `SCORECARD.md:1588-1596`, specifically `:1591-1592` — the round-24 wave-2 correction states that "finite declared-action classifier (round 16) prints `SELFTEST_SUMMARY: 52/52 passed`, exit 0" when re-run at `39c59630`, and that this repertoire row sits outside the 12-row counted C2 population. It confirms the selftest and does not re-run `--frozen`; it neither changes nor retires the row. This is the superseding pointer recorded in the ledger line.
- All later `classifier` mentions (`SCORECARD.md:1440`, `:1446`, `:1470`, `:1492`, `:1501`, `:1516-1524`) refer to `tools/mado-tripwire.py`, a different capability; none touches `mado-action-plan.py`.
- No "Retired" entry names this capability; the file's retirement sections say `none retired` at every round that mentions retirement.

Conclusion: no later text contradicts row 782; the only later re-observation agrees with it.

## Verbatim command output

Working directory: `/fast/scratch/hyaku/mado-r25a3/c2/CapFiniteDeclaredActionClas782` at `41cc04c8` (deleted after the run).

### `timeout 600 prlimit --as=4000000000 python3 -I tools/mado-action-plan.py --selftest` — exit=0

```text
SELFTEST_SCRIPT_SHA256: 226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3
SELFTEST PASS safe-read-repo: want 0/plan_safe got 0/plan_safe
SELFTEST PASS empty-actions: want 0/plan_safe got 0/plan_safe
SELFTEST PASS unlisted-argv0-unscreened: want 0/plan_safe got 0/plan_safe
SELFTEST PASS omarchy-prefix-unscreened: want 0/plan_safe got 0/plan_safe
SELFTEST PASS package-install-libinput: want 1/blocked_action_kind:package-install got 1/blocked_action_kind:package-install
SELFTEST PASS service-mutate: want 1/blocked_action_kind:service-mutate got 1/blocked_action_kind:service-mutate
SELFTEST PASS compositor-mutate: want 1/blocked_action_kind:compositor-mutate got 1/blocked_action_kind:compositor-mutate
SELFTEST PASS input-capture: want 1/blocked_action_kind:input-capture got 1/blocked_action_kind:input-capture
SELFTEST PASS unknown-kind: want 1/unknown_action_kind got 1/unknown_action_kind
SELFTEST PASS first-refusal-wins: want 1/blocked_action_kind:service-mutate got 1/blocked_action_kind:service-mutate
SELFTEST PASS read-disguised-pacman: want 1/denied_executable:pacman got 1/denied_executable:pacman
SELFTEST PASS read-sudo: want 1/denied_executable:sudo got 1/denied_executable:sudo
SELFTEST PASS read-shell: want 1/denied_executable:bash got 1/denied_executable:bash
SELFTEST PASS repo-env-wrapper: want 1/denied_executable:env got 1/denied_executable:env
SELFTEST PASS read-empty-argv: want 1/empty_argv got 1/empty_argv
SELFTEST PASS read-blank-argv0: want 1/empty_argv got 1/empty_argv
SELFTEST PASS plan-not-object: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-missing-argv: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-nonstring-argv: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-action-unknown-key: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-duplicate-key: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-nonfinite: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-bad-utf8: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-is-directory: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS policy-not-object: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-missing-paused: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-paused-false: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-paused-string: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-allows-package-install: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-removes-denial-kind: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-adds-allow-kind: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-unknown-key: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-shrunk-deny-exec: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-shrunk-paused-scope: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-before-plan: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-paused-one: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS policy-paused-null: want 2/policy_malformed got 2/policy_malformed
SELFTEST PASS blocked-kind-empty-argv: want 1/blocked_action_kind:package-install got 1/blocked_action_kind:package-install
SELFTEST PASS unknown-kind-empty-argv: want 1/unknown_action_kind got 1/unknown_action_kind
SELFTEST PASS denied-before-blocked-order: want 1/denied_executable:sudo got 1/denied_executable:sudo
SELFTEST PASS plan-is-symlink: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS plan-is-fifo: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS malformed-later-beats-denied: want 2/plan_malformed got 2/plan_malformed
SELFTEST PASS frozen-match: want 0/frozen_match got 0/frozen_match
SELFTEST PASS frozen-denied-match: want 0/frozen_match got 0/frozen_match
SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered
SELFTEST PASS frozen-missing-pin: want 2/frozen_error got 2/frozen_error
SELFTEST PASS frozen-verdict-mismatch: want 1/frozen_verdict_mismatch got 1/frozen_verdict_mismatch
SELFTEST PASS frozen-tampered-policy: want 2/snapshot_tampered got 2/snapshot_tampered
SELFTEST PASS frozen-invalid-pair: want 2/frozen_error got 2/frozen_error
SELFTEST PASS frozen-empty-finding: want 2/frozen_error got 2/frozen_error
SELFTEST PASS frozen-nonhex-pin: want 2/frozen_error got 2/frozen_error
SELFTEST_SUMMARY: 52/52 passed
```

### `timeout 600 prlimit --as=4000000000 python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` — exit=0

```text
MADO_PLAN: frozen_match
{"action_index": null, "action_kind": null, "detail": "frozen verdict denied_executable:sudo/1 matched", "exit": 0, "finding": "frozen_match", "schema": "mado-action-plan-verdict-v1"}
```

### Supplementary: `--plan .ufo/waves/round-16/fixtures/tight-red.json --policy .ufo/waves/round-16/safety-policy.json` — exit=1

```text
MADO_PLAN: denied_executable:sudo
{"action_index": 0, "action_kind": "read-source", "detail": "actions[0] executable 'sudo' denied for 'read-source'", "exit": 1, "finding": "denied_executable:sudo", "schema": "mado-action-plan-verdict-v1"}
```

### Supplementary: `--plan .ufo/waves/round-16/fixtures/tight-green.json --policy .ufo/waves/round-16/safety-policy.json` — exit=0

```text
MADO_PLAN: plan_safe
{"action_index": null, "action_kind": null, "detail": "passed finite kind/argv[0] screen; not permission or safety", "exit": 0, "finding": "plan_safe", "schema": "mado-action-plan-verdict-v1"}
```

## Scope, risks, blockers

- Observed population: only this row's two named commands plus the section's two plan fixtures. The rest of the round-16 selftest's companion evidence (`calibration-readings.json`, selection fixtures) was not re-run — it belongs to other rows.
- The frozen replay passes at 41cc04c8 because the tool bytes are unchanged since `1e31681` and the in-tree expected pins match the in-tree plan/policy; this is a byte-level pin check, not a live capture.
- Stated claim limits carried: the row's own section says `plan_safe` is not arbitrary-command safety, credential/probe permission or host prevention; unlisted wrappers/interpreters/operands/destinations are not analyzed (`SCORECARD.md:784-788`). Nothing here scores that caveat.
- No blocker. No packages/services/compositor state touched; hyprctl not invoked. No tool installed or upgraded. No builds, linters, formatters or tests run beyond the row's demonstration.
- Cleanup: the sandbox clone `/fast/scratch/hyaku/mado-r25a3/c2/CapFiniteDeclaredActionClas782` was deleted (`rm -rf`, exit 0) and is absent. The only file written in the lane is this report; `tools/`, `corpus/` and all other lane bytes are untouched.
