# AttackKind — blocked/unknown kinds, missing/empty argv, exit map, primary finding

Seat `MadoR16.AttackKind` (critic, leaf). Baseline `32c4fda8…`. Source reading only.
Read: `tools/mado-action-plan.py` (snapshots `#B5DD`, then `#583E`; the file was being
edited during the review, so line numbers are cited for `#B5DD` with function names),
`.ufo/waves/round-16/safety-policy.json`, `safety-cases.json`, `frozen/{plan,expected}.json`,
`measure.py`, `SKILL.md:529-543`, `corpus/QUALITY.md:82-96`, `corpus/lessons/round-16.md`,
`SCORECARD.md:703-709`, and `round-15-verifier-spotcheck.md`.
I did not run the gate, its selftest, cases, or any probe. The only computation was a
Python `json.load` of `safety-cases.json` to list its 31 case shapes; that file is data.
I installed nothing. Every verdict below comes from reading `_classify` and
`_validate_plan` and is `[INFERENCE until L1 runs it]`.

Axes: (A) fail-closed refusal of blocked and unknown kinds; (B) exit-map consistency
(0/1/2 against SKILL row and QUALITY21 wording); (C) whether the primary finding is
deterministic and pinned by fixtures.

## P1 (primary) — precedence that decides the primary finding is deterministic but not pinned

Code order in `_classify` (`#B5DD:327-356`), for each action in declared order:
1. unknown kind;
2. paused or blocked kind;
3. dead `disposition` branch;
4. `argv_nonempty`;
5. blank basename;
6. denied basename.

This is deterministic. No fixture constrains the order, however:
- Every blocked-kind fixture uses nonempty argv: selftest `:531-544`, and all five
  blocked rows in `safety-cases.json` (argv length 2–7).
- The only unknown-kind fixtures also use nonempty argv: selftest `:545-547` and the cases
  row `unknown_action_kind`.
- `first-refusal-wins` (`:548-552`) and the cases row `multi_action_green_then_red` both
  open with a *safe* action. Neither puts an allowed-kind refusal ahead of a blocked kind.
- `_parse_finding` (`#B5DD:~466`) reads only `finding`. The selftest (`:663`) and frozen
  mode (`:452`) compare only finding and exit. `action_index` is never asserted.

The following mutations change the primary finding but keep exit 1. All 40 selftest rows
and all 31 cases would still pass:

| Mutation | Input | Today | Mutant |
|---|---|---|---|
| Move argv checks (`:346-352`) above the kind checks | `{"kind":"package-install","argv":[]}` | `blocked_action_kind:package-install` | `empty_argv` |
| Same mutation | `{"kind":"net-fetch","argv":[]}` | `unknown_action_kind` | unchanged (the unknown check is first). Fails only if the unknown check also moves, so it is unpinned too. |
| Two-pass (all kinds first, then all argv) | `[{"kind":"read-source","argv":["sudo","cat","x"]},{"kind":"package-install","argv":["pacman","-S","y"]}]` | `denied_executable:sudo`, index 0 | `blocked_action_kind:package-install`, index 1 |
| Report a fixed `action_index` of 0 | any refusal at index > 0 | correct index | wrong index, never detected |

SKILL `:529` credits "self-invocation asserts code and finding". The docstring
(`:59-60`) promises "first refusing action in declared order". The fixtures cannot detect
a regression of either promise as long as the exit code stays the same.

Impacted axes: operability (C2's evidence), calibration of what the selftest proves.
This is not a safety hole: refusal (exit 1) survives every mutation above.

Smallest safe correction: add three literal rows to the selftest, mirrored in `safety-cases.json`:
- `blocked-kind-empty-argv`: `package-install`, `[]` → `1 blocked_action_kind:package-install`.
- `unknown-kind-empty-argv`: `net-fetch`, `[]` → `1 unknown_action_kind`.
- `denied-exec-before-blocked`: the two-action plan above → `1 denied_executable:sudo`.

Optionally, have `_parse_finding` also return `action_index` and assert it on the
multi-action rows.

## P2 — malformed argv on a blocked kind is exit 2 "could-not-evaluate", not a "failed" refusal

`_validate_plan` (`#B5DD:292-316`) validates the whole plan before `_classify` runs. Two
consequences:

- `{"actions":[{"kind":"package-install","argv":"sudo pacman -S --needed --noconfirm libinput libinput-tools"}]}`
  gives `plan_malformed`, exit 2, with `action_index`/`action_kind` `null`. A single
  string argv is exactly how the r15 command line would be declared naively. The same
  happens for `{"kind":"package-install"}` with no argv, and for `["pacman", null]`.
- Masking: `[{"kind":"package-install","argv":["sudo","pacman","-S","libinput"]},{"kind":"read-source"}]`
  also gives exit 2 `plan_malformed`. The verdict never names `package-install`.
  The detail reads only `actions[1].argv must be a list of strings`.

This behavior is declared, at docstring `:59` and in the cases.json `finding_priority`, so
fail-closed holds: the exit is nonzero. The wording around it disagrees, though:
- SKILL row `:529` maps 1 to "failed (blocked kind/name, unknown kind or empty argv)" and
  2 to "could-not-evaluate (malformed plan/policy or usage)".
- QUALITY21 (`corpus/QUALITY.md:88-90`) says the classifier "must **fail** on … unknown
  kind, and malformed action".
- Lesson M1 (`round-16.md:14`) says it "must reject … malformed/unknown action".

By the registry's own vocabulary, a malformed action is not a "fail". In mado's gate
conventions, could-not-evaluate is SKIP/UNKNOWN-adjacent. A consumer that keys on exit 1
for "refused" would downgrade a declared package-install with stringly argv.

This is a tradeoff the judge should accept as declared; the defect is the wording.

Smallest safe correction, wording only:
- SKILL `:529` and QUALITY21: "any nonzero exit means do not execute; exit 2 is a
  refusal-to-evaluate, never a skip or pass".
- Add one cases row pinning `package-install` with string argv → `2 plan_malformed` so the
  precedence is explicit.

## P3 — `empty_argv` fires on a nonblank argv[0]

`_basename` (`#B5DD:319-324`) maps `"/"` and `"///"` to `""`. `_classify` `:349-352` then
emits `empty_argv` with the detail "argv[0] is empty", even though argv is nonempty and
argv[0] is not blank.

The exit (1) is correct, but three texts describe the trigger differently:
- docstring `:47`: "argv empty or argv[0] blank";
- cases.json vocabulary `:23`: "empty argv list" only;
- SKILL `:529`: "empty argv".

Correction: describe it as "argv empty or argv[0] has an empty basename". No code change
is needed.

## P4 — the `paused` input is vestigial in classification

`_validate_policy` forces `paused is True` and `paused_scope` equal to all four deny kinds.
At `:340` every deny kind therefore returns "denied by paused policy". The `disposition`
branch (`:343-345`) is unreachable, and `paused` cannot change any verdict.

After an operator lift, a `paused:false` policy gives exit 2 `policy_malformed`. That
fails closed and is consistent with "pinned in code", but nothing in the gate represents
the "pause" separately from the permanent denials. Simplification note only; no defect.

## Checked and held (no counterexample found)

- **Kind spelling variants fail closed.** `Package-Install`, `package_install` and
  `"package-install "` give `unknown_action_kind`, exit 1. The kind's identity is lost to
  "unknown", which is acceptable.
- **Blocked kind with a benign argv** is still blocked. The kind check (`:340`) precedes
  the argv checks; cases `service_mutate_kind_benign_argv` covers it.
- **No input path leads to an uncaught-exception exit 1** that would collide with
  "refused":
  - `_parse_json_bytes` (`#583E:201-211`) wraps decode and parse in `except Exception`,
    which also covers `RecursionError` and int-digit limits;
  - non-regular inputs are rejected;
  - verdict JSON uses `ensure_ascii`, so lone-surrogate kinds are escaped;
  - the `finding` line embeds only pinned names.

  Closed stdout (BrokenPipe) was not analysed.
- **All 31 `safety-cases.json` expectations agree with the current code** by reading. The
  w1 `NoLiveBreach.md:128-132` finding-name mismatch (`denied_kind` and others) is stale.
  The landed gate emits `blocked_action_kind:*`, `unknown_action_kind`, `empty_argv` and
  `denied_executable:*`.
- **The frozen snapshot is correct.** Mislabeled `read-source` plus the sudo/pacman argv
  gives `denied_executable:sudo`, exit 1, which `expected.json` pins. The current code
  reads each input once, so the earlier hash-then-reopen TOCTOU is removed (`#B5DD:432-451`).

## Hand-off (outside this seat; not duplicated)

- **cases.json embedded policies are partial.** `policy_paused_*` and
  `policy_extra_allow_key` lack `paused_scope`, `deny_executables` and `kinds`, so they
  are malformed for unrelated reasons. They do not discriminate the `paused` check.
  Example: a mutation of `type(paused) is bool and paused is True` to `paused == True`
  would accept `paused: 1`, and no selftest row (False and "true" only) or cases row
  catches it. Owner: AttackPause or PlanSchema.
- **No committed runner exists for `safety-cases.json`.** Its per-case `policy` override
  needs one. SKILL `:529` cites the file as independent cases, so L1's verification should
  state how it was executed.

## Installs

None. No tool was installed or updated, and no package, service, compositor or input
operation was performed.
