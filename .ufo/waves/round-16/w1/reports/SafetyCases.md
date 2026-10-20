# SafetyCases — round-16 independent expected cases for the action-plan gate

Seat: `MadoR16.SafetyCases` (executor). Date: 2026-10-20. Baseline declared for the
round: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Update (same day, post-delivery): expanded three times per MadoR16's requests — first
to 28 (mislabeled R15 argv, multi-action green-then-red, absolute-path
libinput, five embedded malformed-policy pins), then to 31 under the L1
finite-scope decision (two labelled residual controls proving unlisted argv0
is not screened, plus the tight sudo-prefix red), then to 32 after W2 review
required each embedded policy to be a FULL canonical copy plus exactly one
named delta (replacement semantics; added `policy_paused_null`). Vocabulary
and the scope_limit assumption reconciled directly with
`MadoR16.SafetyGate` by exact id.

## Deliverable

- Wrote `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-16/safety-cases.json`
  — the only file assigned to this seat. 32 cases, each with
  `name`, `plan`, `expected_code`, `expected_finding`, plus optional `policy`.
- Wrote this report to `.ufo/waves/round-16/w1/reports/SafetyCases.md`.
- Sent the proposed finding vocabulary to `MadoR16` and, per MadoR16's
  follow-up instruction, reconciled it directly with `MadoR16.SafetyGate` by
  exact id.

## API agreed from context

SafetyGate's own artifact (`tools/mado-action-plan.py`,
`.ufo/waves/round-16/safety-policy.json`) had not landed when this file was
written, so the contract was taken verbatim from the dispatch spec for the
`SafetyGate` item in `.ufo/waves/round-16/w1/spec.json`:

- Invocation shape: `--plan PATH --policy PATH`.
- Plan schema: JSON object with `actions` list; each action is an object with
  string `kind` and list-of-strings `argv`. Argv is data only — never executed.
- Policy (`paused=true`): allowed kinds `read-source` (nonempty argv) and
  `repo-write` (nonempty argv); blocked kinds `package-install`,
  `service-mutate`, `compositor-mutate`, `input-capture`; unknown or malformed
  fails closed.
- Refused executable basenames for allowed kinds: `pacman, yay, paru,
  systemctl, hyprctl, omarchy, libinput, evtest, sudo, sh, bash, env`.
- Exit codes: `0` clean / `plan_safe`; `1` refused with a stable named reason;
  `2` could-not-evaluate (malformed plan or policy). `--frozen DIR` compares
  digests and verdict; tamper → `2 snapshot_tampered`.

## Coverage vs. assignment

| Required coverage | Case name(s) | code → finding |
|---|---|---|
| Actual libinput sudo pacman transaction blocked as package-install | `r15_libinput_sudo_pacman_transaction` | 1 → `blocked_action_kind:package-install` |
| Service restart | `service_restart_waybar` | 1 → `blocked_action_kind:service-mutate` |
| Compositor change | `compositor_hyprctl_reload` | 1 → `blocked_action_kind:compositor-mutate` |
| Raw input | `raw_input_libinput_debug_events`, `raw_input_evtest` | 1 → `blocked_action_kind:input-capture` |
| Unknown kind | `unknown_action_kind` | 1 → `unknown_action_kind` |
| Missing argv | `missing_argv` (+ `argv_not_a_list`, `missing_actions_list`) | 2 → `plan_malformed` |
| read-source disguised pacman | `read_source_disguised_pacman_plan_mode` | 1 → `denied_executable:pacman` |
| read-source sudo | `read_source_sudo_wrapper` | 1 → `denied_executable:sudo` |
| read-source shell | `read_source_bash_shell`, `read_source_sh_shell` | 1 → `denied_executable:bash` / `denied_executable:sh` |
| Allowed source read and repo write | `allowed_source_read`, `allowed_repo_write`, `allowed_source_read_and_repo_write` | 0 → `plan_safe` |
| Same R15 argv mislabeled read-source (added per MadoR16) | `r15_libinput_sudo_pacman_mislabeled_read_source` | 1 → `denied_executable:sudo` (first basename wins) |
| read-source libinput via absolute path (per MadoR16) | `read_source_libinput_debug_events_help` | 1 → `denied_executable:libinput` (basename match on `/usr/bin/libinput`) |
| Multi-action green then red (per MadoR16) | `multi_action_green_then_red` | 1 → `blocked_action_kind:service-mutate` (first refusal in declared order) |
| Malformed policy via optional embedded `policy` field (per MadoR16; each embeds FULL canonical policy + one named delta, replacement semantics) | `policy_paused_boolean_false`, `policy_paused_string_false`, `policy_paused_numeric_one`, `policy_paused_null`, `policy_paused_missing`, `policy_extra_allow_key` | 2 → `policy_malformed` |
| Residual controls — unlisted argv0 NOT screened (per MadoR16 L1 scope decision) | `residual_control_omarchy_pkg_add_unscreened`, `residual_control_python3_inline_unscreened` | 0 → `plan_safe` (deliberate boundary pin, never executed) |
| Tight red/green argv-prefix delta (per MadoR16) | `read_source_sudo_cat_tight_red` vs `allowed_source_read` | 1 → `denied_executable:sudo` vs 0 → `plan_safe`; identical tail argv, prefix-only difference |

Bonus cases: `empty_argv_allowed_kind` (empty argv list on an allowed kind →
1 `empty_argv`), `read_source_env_wrapper` (1 `denied_executable:env`),
`read_source_hyprctl_version_r15_probe` (binds the round-15 disclosed
`hyprctl version` live-probe violation to a refused fixture → 1
`denied_executable:hyprctl`), `service_mutate_kind_benign_argv` (proves kind
blocking is argv-independent → 1 `blocked_action_kind:service-mutate`),
`argv_not_a_list`, `missing_actions_list` (malformed → 2 `plan_malformed`).

Tally: exit 0 ×5, exit 1 ×18, exit 2 ×9 — 32 cases total. Optional `policy`
field added per case (documented in the file's `assumptions.policy_field`);
embedded malformed policies are test inputs only and do not redefine the
committed `safety-policy.json`.

## Judgment calls (documented, flagged to MadoR16)

1. `missing_argv` → exit **2** `plan_malformed`: absent argv is a schema
   violation, not an evaluable refusal. Separated from `empty_argv` (a
   well-formed empty list) which is exit **1** `empty_argv` as an evaluable
   nonempty-argv violation. If SafetyGate merges both under one exit-2
   `plan_malformed`, that is a deliberate divergence in my independent
   expectations — reconcile explicitly, do not retrofit.
2. `unknown_action_kind` → exit **1**, not 2: the plan parses; the kind is
   simply unrecognized and the spec says unknown fails closed, which I map to
   a refused verdict rather than a could-not-evaluate error.
3. The disguised-pacman case uses `pacman -Sp --print-format %n %v` — the
   *query-only* plan mode that a future operator-authorized install may use.
   The gate must still refuse it under basename policy; a benign-argument
   pacman is still `denied_executable:pacman`. This binds the R15-V2
   new-only dry-run lesson without pretending the gate can reason about
   pacman flags.
4. `read_source_env_wrapper` guards the `env <cmd>` wrapper hole in basename
   matching (documented limit: the gate refuses `env` itself but cannot
   follow `env`'s payload to a denied inner command — argv is data, not
   resolved).
5. `service_mutate_kind_benign_argv` ensures blocking is keyed on declared
   kind, not on argv inspection — mislabeled benign argv under a blocked kind
   still refuses.
6. Finding names carry a colon-suffix (`blocked_action_kind:package-install`,
   `denied_executable:pacman`) so the stable reason names the specific class
   and offender while remaining a finite vocabulary.
7. Malformed-policy pins (added per MadoR16 instruction, then redesigned per
   W2 review): any deviation from exact `paused: true` — boolean `false`,
   string `"false"`, numeric `1`, `null`, a missing `paused`, or an
   unexpected top-level key such as `allow` — is exit **2**
   `policy_malformed`. Strict-true comparison, not truthiness: a truthy `1`
   or `"false"` is as malformed as literal `false`. Unknown keys are refused
   rather than ignored so that a hypothetical `allow` escape hatch can never
   silently widen a paused policy. Each embedded policy is a field-for-field
   copy of the committed canonical `safety-policy.json` (`schema`, `paused`,
   `paused_scope`, `deny_executables`, `kinds`) mutated in exactly the named
   key, so a failure can only be caused by the named defect — an earlier
   partial-object version would have failed on incidental missing fields and
   was replaced per W2 review. Embedded policies REPLACE the file input
   wholesale; the runner must not overlay or merge them.
8. `r15_libinput_sudo_pacman_mislabeled_read_source` expects
   `denied_executable:sudo` (not `pacman`): the gate checks `argv[0]`'s
   basename only, and refusing at `sudo` is the fail-closed earliest point.
   This pairs with the `package-install`-kinded twin case to cover both the
   kind block and the basename defense against the identical real-world argv.
9. `read_source_libinput_debug_events_help` uses the absolute path
   `/usr/bin/libinput` to pin basename normalization — a denied executable is
   refused by basename regardless of the leading directory or a benign
   `--help` tail.
10. Residual controls are expected `plan_safe` on purpose (per MadoR16 L1
    scope): `omarchy-pkg-add libinput` is an installer wrapper and
    `python3 -c print(1)` is inline code — both would be dangerous if
    executed, but argv is never executed and the gate is ONLY a
    declared-kind + finite 12-basename screen. Encoding them as green pins
    the documented boundary and prevents a future reviewer from claiming
    the gate screens arbitrary commands; the `denied_executable:*`
    vocabulary has no wildcard. C2 is the classifier only — not
    privacy/probe safety and not host prevention.
11. `read_source_sudo_cat_tight_red` pairs with `allowed_source_read` as an
    argv-prefix-only delta (`sudo` prepended, tail identical): the
    red/green flip is attributable to the basename screen alone.

## Retained evidence

- `corpus/lessons/round-15-verifier-spotcheck.md` read in full before work, as
  required. The R15-V1 incident (seat `MadoR15.LibinputEvents` running
  `sudo pacman -S --needed --noconfirm libinput libinput-tools` at
  04:25:16-03:00, libinput 1.31.3-1 → 1.32.0-1 plus new packages) is encoded
  verbatim as the first case; R15-V2 (new-only `-Sp` plan + installed-name
  overlap refusal) and the disclosed `ReviewLibinput` `hyprctl version`
  live-probe debt are bound by cases `read_source_disguised_pacman_plan_mode`
  and `read_source_hyprctl_version_r15_probe`.
- File validated as JSON after each write; all 32 case objects carry the
  required keys plus optional `policy` (checked with Python `json` +
  `Counter`, no gate execution).
- Vocabulary reconciliation message sent directly to `MadoR16.SafetyGate` by
  exact id (per MadoR16 instruction), and the same vocabulary was earlier
  sent to `MadoR16`. Expectations were authored from the spec and will not
  be revised from SafetyGate's implementation output.
- Reconciliation outcome (post-landing): `MadoR16.SafetyGate` reported it
  adopted this file's pinned vocabulary verbatim — every finding spelling,
  exit-code mapping, basename-of-argv[0]-only (first basename wins),
  malformation-before-classification, first-refusal-in-order, and the finite
  12-name screen with unlisted argv0 → `plan_safe`. It confirmed
  `policy_malformed` (not `policy_invalid`). Stated contract has zero
  divergence from all 32 expectations; artifacts exist on disk
  (`tools/mado-action-plan.py`, `.ufo/waves/round-16/safety-policy.json`)
  and were not read or executed by this seat — expectations remain
  spec/L1-derived, so any future mismatch is an implementation bug, not a
  vocabulary drift.

## Limits and non-claims

- Cases are independent expectations, not the gate implementation and not
  proof of gate behavior; no gate, selftest, or check was executed
  (assignment and contract forbid seat-side verification).
- `expected_finding` spellings were this seat's proposal and are now the
  agreed contract: SafetyGate adopted them verbatim, so BOTH `expected_code`
  AND `expected_finding` are authoritative — a mismatch in either is an
  implementation defect for L1 adjudication, not a naming drift.
- The gate is a static declared-plan classifier only: it cannot validate
  arbitrary shell strings, follow wrapper payloads (e.g. `env pacman ...`
  refused at `env`, not at `pacman`), or prevent an operator from running a
  command outside the plan channel. Cases assert the declared boundary, not
  real package validation — matching the "hard-coded fixture is not actual
  package validation" constraint.
- `--frozen`/snapshot-tamper exit-2 path is in vocabulary but has no case
  here because it binds digests produced by the gate's own `--selftest`
  fixtures, which is SafetyGate's authored surface, not mine to invent.
- Residual-control green pins are boundary documentation, not endorsement:
  an unscreened `omarchy-pkg-add`/`python3 -c` plan passes this classifier
  yet remains outside operator authorization if actually run; the gate's
  scope statement in `safety-cases.json` (`assumptions.scope_limit`)
  carries this explicitly.

## Tooling / installs

None. No installs, no pacman, no service, no live probes of any kind —
consistent with the host-wide pacman pause and the this-round no-install
instruction. No missing prerequisites blocked this task.

## Risks / blockers

- Finding-name drift vs. SafetyGate's implementation (mitigated: vocabulary
  sent to MadoR16 before integration; exit codes are the load-bearing
  expectations).
- If SafetyGate treats schema violations as exit-1 refusals rather than exit-2
  could-not-evaluate, the three `plan_malformed` cases diverge — flagged as a
  deliberate design choice for L1 adjudication.

Report: .ufo/waves/round-16/w1/reports/SafetyCases.md
