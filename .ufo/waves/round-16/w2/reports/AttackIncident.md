# AttackIncident — incident-shaped read-source and blocked-kind discriminators

Seat `MadoR16.AttackIncident` (critic). I only read source. I did not run
the gate, selftest, frozen mode, measure.py or any host command. I wrote only
this report. I installed or updated nothing. I read the required
`corpus/lessons/round-15-verifier-spotcheck.md` before starting, including the
R15-V1 argv at `:256-257`.

## Bound artifacts (read 2026-10-20, in-memory SHA-256 of the files on disk)

| Artifact | SHA-256 | Notes |
|---|---|---|
| `tools/mado-action-plan.py` | `eee51dda87bd19ffb86b826d984ad99faf2dd2061d753e80235c1131f39257aa` | 760 lines, read tag `#FD91`. The file changed during my review: `_read_regular` gained `O_NOFOLLOW` and lines moved by +8. The anchors below are for `#FD91`. |
| `.ufo/waves/round-16/safety-policy.json` | `fb134d8f…b7fc`, 792 B | Byte-identical to `frozen/policy.json` and matches the frozen pin |
| `.ufo/waves/round-16/safety-cases.json` | `9d0fac4e…6ed8` | Strict parse succeeded: 31 cases, no duplicate names |
| `.ufo/waves/round-16/frozen/plan.json` | `82bc7652…febc3`, 224 B | Matches the `expected.json` pin. Kind `read-source`, R15 argv |

The plan argv matches the incident argv token for token:
`sudo pacman -S --needed --noconfirm libinput libinput-tools`
(spotcheck `:256-257`; cases `:32-43` and `:289-300`; frozen `plan.json`).

## Verdict

The incident-shaped tests are correct, but they are narrower than the C2
wording suggests. **Fixable defects:** a missing discriminator and a wording
gap. **Not a defect:** the finite screen's limit, which the lane already
declares. The canonical judge does not need to reject anything. No promised
behavior is falsified. All counterexamples below come from reading the source
(`_classify`, `:327-357`). None was executed.

## CE1 — the mislabeled incident is refused only because argv[0] is `sudo` (the escalator)

- **Evidence.** `_classify` takes the basename of `argv[0]` only (`:349`) and
  checks it against the pinned set (`:353`, `:109-112`). `pacman` is at
  `argv[1]` and is never examined.
  - `r15_libinput_sudo_pacman_mislabeled_read_source` (`cases:289-300`) and the
    frozen red (`expected.json`: `denied_executable:sudo`/1) are both red
    because of one token, `sudo`.
- **Counterexample (one-token delta, from source).** Use kind `read-source`
  with argv `["doas","pacman","-S","--needed","--noconfirm","libinput","libinput-tools"]`.
  This gives `plan_safe`, exit 0.
  - `run0`, `pkexec` and `su -c` give the same result. So does
    `["timeout","120","sudo","pacman",…]`, which puts `sudo` at argv[1].
  - [INFERENCE] `run0` ships with systemd ≥256. I did not check the host.
- **Second counterexample (operator-sourced).** The standing tooling directive
  lists four install channels in order:
  1. `sudo pacman -S --needed --noconfirm`
  2. `uv tool install`
  3. official release binary into `~/.local/bin`
  4. `cargo install` / `npm -g`

  Under `read-source`, the screen refuses only channel 1, and only at `sudo`.
  `["uv","tool","install","x"]`, `["cargo","install","x"]` and
  `["npm","-g","install","x"]` all give `plan_safe`. These are the next things
  an actor would try after a refused pacman install, by the same directive the
  R15 actor followed.
- **Classification.** This is the declared classifier limit, not a broken
  promise. `SKILL.md:533-539`, the lesson (`round-16.md:30-31,84-85`) and
  `scope_limit` (`cases:17`) all say "unlisted names pass".
  - The residual controls show the limit only with `omarchy-pkg-add` and
    `python3 -c` (`cases:411-435`; selftest `:506-511`). Neither is the
    incident shape.
  - The C2 claim says "negative actual-incident-shaped input"
    (`SCORECARD.md:705`). A reader can take that to mean the incident is
    refused because of its package-manager content. It is not.
- **Impacted axes.** Operability (C2 claim precision) and calibration/quality
  (honest limit labelling). No coverage impact.

## CE2 — the incident kind has no blocked-kind negative discriminator

- **Evidence.** I parsed the cases statically and took the argv[0] basename of
  every blocked-kind action:

  | Case | Kind | argv[0] | Also on the deny list? |
  |---|---|---|---|
  | `r15_libinput_sudo_pacman_transaction` | package-install | sudo | yes |
  | `compositor_hyprctl_reload` | compositor-mutate | hyprctl | yes |
  | `raw_input_libinput_debug_events` | input-capture | libinput | yes |
  | `raw_input_evtest` | input-capture | evtest | yes |
  | `service_restart_waybar`, `multi_action_green_then_red` | service-mutate | systemctl | yes |
  | `service_mutate_kind_benign_argv` (`cases:226-237`) | service-mutate | `cat` | **no** |

  - The selftest is the same. `package-install-libinput` (`:512-516`, sudo),
    `compositor-mutate` (hyprctl), `input-capture` (evtest),
    `first-refusal-wins` (systemctl/pacman) and frozen `denied` (pacman) all
    use denied basenames.
  - **No test anywhere** shows `package-install`, `compositor-mutate` or
    `input-capture` blocked when argv[0] is *unlisted*. That is exactly where
    the kind label is the only defense.
- **Surviving mutant, if the exit code is the only check.** Make blocked kinds
  fall through to the argv[0] screen, for example by deleting both kind
  branches at `:340-345`.
  - Every package-install, compositor and input case above still exits 1, now
    as `denied_executable:<exe>`.
  - `cases:28` makes `expected_code` "authoritative" and says the finding
    should be "reconciled". Under that reading, only `service-mutate` (one case)
    detects this mutant.
  - The selftest and frozen comparisons check the finding string
    (`_parse_finding`, `:640-649`; frozen `:425-426`). So the full-branch
    mutant dies there, but only through the finding text.
  - A mutant scoped to package-install, the incident kind, has no
    exit-distinguishing test anywhere.
  - Nothing committed executes `safety-cases.json`. `measure.py:362-376` records
    only its presence and SHA (`executed: False`). The comparison mode for
    those cases depends on L1's verification step.
- **Impacted axis.** Operability. The C2 "fail-closed on package-install"
  credit rests on evidence that does not separate the kind defense from the
  argv defense.

## CE3 — the pause branch and the deny-disposition branch cannot be told apart (no-credit note)

- `_validate_policy` forces `paused is True` (`:241-243`) and
  `paused_scope == PINNED_PAUSED_SCOPE` (`:249`). It also forces exactly those
  four kinds to `deny` (`:113-120`, `:273-276`). As a result,
  `:340-342` (pause) and `:343-345` (disposition) return the same
  `(finding, code)` for every valid input. Only `detail` differs, and no
  selftest, frozen run or case asserts `detail`.
- Deleting either branch is therefore an equivalent mutant. "Persisted paused
  policy" (`SCORECARD.md:704`) is a policy-shape precondition, not a second,
  independently tested refusal layer. This is not a defect. Do not count it as
  two defenses.
- The five embedded-policy cases in `safety-cases.json` (`:332-409`) are
  `{"paused":false}`, `"false"`, `1`, `{}` and `{"paused":true,"allow":[…]}`.
  Each one also lacks `paused_scope`, `deny_executables` and `kinds`. They would
  be `policy_malformed` even if the paused check were removed, so they do not
  test pause handling.
  - The selftest `policy-paused-false`/`-string` cases (`:583-588`) do test it,
    because they use the full canonical policy.
  - No test anywhere covers `paused: 1` on a full policy. A mutant that weakens
    `type(paused) is bool and paused is True` to `paused == True` would survive.
    Impact is nil, because `paused` only feeds the redundant branch. I record it
    only so that the strictness is not credited as tested.

## Bounded edge observations (no correction demanded)

- **Empty argv under a blocked kind.** `{"kind":"package-install","argv":[]}`
  is refused by kind before the empty check (`:340` before `:346`). No test
  covers it. Swapping the order changes only the finding, to `empty_argv`, and
  the action is still refused.
- **NUL in argv[0].** `"sudo\u0000"` is valid JSON. `strip()` does not remove
  it, so the basename is `sudo\x00`, which is not denied, and the plan is
  `plan_safe`.
  - [INFERENCE] CPython `subprocess` rejects embedded NUL. A C `execve`
    consumer would truncate the string to `sudo`.
  - The gate never executes argv. This is a false-label case under the
    declared lying-plan limit (`round-16.md:84`), not a bypass of a promise.
- **Docstring.** `:22` refers to `PINNED_POLICY`, which does not exist. The
  real names are `PINNED_PAUSED_SCOPE`, `PINNED_DENY_EXECUTABLES` and
  `PINNED_KINDS`. `SKILL.md:529` correctly says `PINNED_*`. This is cosmetic.

## Smallest safe correction (L1-owned; no policy identity change required)

1. **Add one kind-only discriminator for the incident kind** to the
   `--selftest` list (which compares finding and code) and mirror it in
   `safety-cases.json`: kind `package-install`, argv
   `["doas","pacman","-S","--needed","--noconfirm","libinput","libinput-tools"]`
   → 1 `blocked_action_kind:package-install`.
   - `["omarchy-pkg-add","libinput"]` under `package-install` is also good. It
     pairs one-to-one with the existing residual control.
2. **Add one residual control** with the same argv under `read-source` →
   0 `plan_safe`, labelled `residual_control_escalator_swap_unscreened`.
   - It differs from the frozen and mislabeled reds by one token. It pins, on
     purpose, that those reds depend only on `argv[0]=="sudo"`.
3. **Fix the wording** in `SCORECARD.md` C2 and the `round-16.md` M1 receipts,
   for example: "incident argv refused under `package-install` by kind; under
   `read-source` refused only at argv[0] `sudo`; argv[1] `pacman` uninspected;
   an escalator swap (`doas`/`run0`/`pkexec`) or a RULES fallback installer
   (`uv`/`cargo`/`npm`) under `read-source` is `plan_safe`."
4. **If L1 runs `safety-cases.json`,** compare the finding class
   (`blocked_action_kind` / `denied_executable` / `plan_safe`) as well as the
   exit code. Do not let `cases:28` "reconcile" a finding to whatever the gate
   emits.

**Tradeoff for the judge, not demanded.** Adding `doas`, `run0`, `pkexec` and
`su` to `PINNED_DENY_EXECUTABLES` would close the escalator swap. It would also
change the pinned policy identity: `safety-policy.json` and the frozen
`policy_sha256` `fb134d8f…` would both have to be re-pinned, along with the
selftest. Wrappers such as `timeout`/`nice` and the `uv`/`cargo`/`npm`
installers would still pass. This is broad enforcement outside the assigned
scope. Corrections 1–3 make the existing limit explicit and tested without
changing what the gate is.

## Limits of this review

- **Not executed.** Nothing was run. The surviving and killed mutant analysis
  comes from reading the source. Observed outcomes are pending L1 verification.
- **Integrated, not final.** I attacked the integrated files as they stood at
  `#FD91` and the hashes above. If the gate changes further, re-bind.
- **Receipts pending.** Lesson M1 says "Exact observed receipts are appended
  below" (`round-16.md:14`). No gate receipt was present at read time, and
  `evidence/` holds only `source-bindings.json` and `census-before.txt`.
- **Overlap with w1.** The generic wrapper and escalator gaps were already
  raised in w1 (`ExecBasename.md:57-59`, `HostHarm.md:71-75`). This report adds
  the specific discriminator gaps against the integrated cases and selftest,
  the RULES-channel counterexample, and the pause/disposition equivalence.
- **Installs:** none.
