# AttackPolicyCases — policy-variant cases (false/string/number) and frozen expected pins

Seat: `MadoR16.AttackPolicyCases` (reviewer, leaf, read-only). Root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Artifacts read as they stand: `tools/mado-action-plan.py` (752 L), `.ufo/waves/round-16/safety-policy.json`,
`.ufo/waves/round-16/safety-cases.json` (31 cases), `.ufo/waves/round-16/measure.py`, `.ufo/waves/round-16/frozen/*`,
`SKILL.md:529-542`, and the sibling reports `w1/reports/SafetyCompositor.md` (SC-1) for host context.

Axes named: **calibration** (does the expected-case set prove the property its name claims?), **operability**
(does a green verdict overstate safety?), **integrity** (does frozen mode bind what it says it binds?).

No gate, selftest, measure.py, test, probe, install or package operation was run. The one host file read
(`~/.local/share/omarchy/bin/omarchy-pkg-add`) is a source read. JSON was inspected by reading the file, not by
executing the gate. Installs: none.

## Verified-OK (not findings)

- Paused type check is exact: `type(paused) is bool and paused is True` (`tools/mado-action-plan.py:233-235`).
  `1`, `"true"`, `"false"`, `false`, missing and `null` are all rejected by the current code.
- Unknown policy keys are rejected before field checks (`:228-230`). Duplicate keys and NaN/Infinity are rejected
  by `_strict_pairs` and `_reject_constant` (`:181-191`).
- Frozen `expected_exit` rejects `bool` (`type(want_exit) is int`, `:411`), so `true`/`1.0` yield `frozen_error`.
- All 31 rows in `safety-cases.json` have an `int` `expected_code` (0, 1 or 2) and a finding string matching the
  vocabulary. Each `expected_code`/`expected_finding` pair is consistent with `_classify` (`:319-349`) and
  `_validate_plan` (`:284-308`) by source trace. No expected2-style malformed row exists in the cases file itself.

## Findings (ordered by severity)

### F1 — HIGH (calibration): the five embedded-policy variants do not isolate their named property; the numeric mutant survives every committed test

The cases file says an embedded `policy` **replaces** the default paused policy (`safety-cases.json:16`). Under that
semantics each variant is a partial object missing `paused_scope`, `deny_executables` or `kinds`. So each row is
rejected at whichever check runs first, not at the check its name names:

| row (safety-cases.json) | embedded policy | first rejecting check | would still exit 2 if the paused check were weakened? |
|---|---|---|---|
| `policy_paused_boolean_false` :332 | `{"paused": false}` | `:234` | yes (next: `paused_scope` missing, `:238`) |
| `policy_paused_string_false` :348 | `{"paused": "false"}` | `:234` | yes |
| `policy_paused_numeric_one` :364 | `{"paused": 1}` | `:234` | yes |
| `policy_paused_missing` :380 | `{}` | `:234` | yes |
| `policy_extra_allow_key` :394 | `{"paused": true, "allow": [...]}` | `:228-230` | yes (next: `paused_scope` missing) |

Surviving-mutant reasoning (source reading, not executed):

- **Numeric mutant.** Change `:234` to `if policy.get("paused") != True:`. In Python `1 == True`, so `paused: 1` is
  accepted. `policy_paused_numeric_one` still exits 2 `policy_malformed` (`paused_scope` missing), so it stays
  green. The committed selftest does not catch it either: `grep` finds **no** numeric, `null` or `0` paused variant
  in `tools/mado-action-plan.py` (`policy-paused-false` `:575` and `policy-paused-string` `:578` use `False` and
  `"true"`, both of which `!= True` still rejects). **So the numeric mutant survives every committed test.** The
  current code is correct; the test set cannot prove it.
- **Dropped unknown-key check.** Removing `:228-230` leaves `policy_extra_allow_key` green (still exit 2 via
  `paused_scope`). Only selftest `policy-unknown-key` (full canonical + `notes`, `:599-601`) catches it.
- **Default-true mutant.** `policy.get("paused", True)` leaves `policy_paused_missing` green (exit 2 via
  `paused_scope`). Only selftest `policy-missing-paused` (full canonical minus `paused`, `:569-574`) catches it.

The discriminating form is a **full canonical policy with only `paused` changed**, which the selftest uses for
`False` and `"true"` but not for numbers. Missing: canonical with `paused` set to `1`, `0`, `1.0`, `null`, `"True"`,
`[true]`.

Fix (test side, no gate change needed): (a) state overlay or full-canonical semantics for `policy` and make the
five rows overlay onto the canonical policy; (b) add numeric/null canonical variants to `run_selftest` and to the
cases file; (c) add a note that `policy_extra_allow_key` must include the full canonical policy.

### F2 — HIGH (operability / calibration): a green residual row pins plan_safe for a host helper that installs the exact forbidden package

`safety-cases.json:411-423` (`residual_control_omarchy_pkg_add_unscreened`) expects **exit 0 `plan_safe`** for
`{"kind":"read-source","argv":["omarchy-pkg-add","libinput"]}`. The host helper is
`~/.local/share/omarchy/bin/omarchy-pkg-add` (source read): line 6 `omarchy:requires-sudo=true`, line 8-9
`if omarchy-pkg-missing "$@"; then sudo pacman -S --noconfirm --needed "$@" || exit 1`. That is the R15-V1
transaction shape (`corpus/lessons/round-15-verifier-spotcheck.md:256`) with the exact package name.

The gate's `PINNED_DENY_EXECUTABLES` (`:109-112`) does not include `omarchy-pkg-add`, and `_basename` is lexical
(`:311-316`), so the gate returns `plan_safe`. The gate selftest `omarchy-prefix-safe` (`:501-503`) pins the same
exit 0. SC-1 in `w1/reports/SafetyCompositor.md` raised this as CRITICAL.

The limit is disclosed (`safety-cases.json:17`, `SKILL.md:533-539`), so this is not hidden. But the committed set now
affirmatively encodes a passing expectation for libinput installation. A reader, or a future L0 summary, can cite
"`plan_safe` for libinput" as clearance. "Residual disclosure" does not cover a pinned green fixture for the forbidden
package.

Fix (smallest honest): rename the row to `residual_known_bypass_green`, add `"residual_control": true` and the
host-source anchor, and state in the file that exit 0 here is not clearance. Preferred (outside this seat's files):
the gate should refuse `omarchy-*` helpers or package-name operands in the install family, as SC-1 proposes.

### F3 — MEDIUM (integrity / calibration): `safety-cases.json` has no executor; "independent cases" is a registry claim with no run behind it

- `SKILL.md:529` lists `safety-cases.json` as the independent-cases pinned path of the `mado-action-plan` gate.
- No file in the repo reads `safety-cases.json` (`grep -rn` finds only the descriptive `safety-cases.json:6,8,16,28`
  and `measure.py:364-365`).
- `measure.py:362-389` only hashes the file and sets `'safety_executed': False`.
- The gate's `--selftest` uses only its own literal cases (`:491-613`, `:674-704`).

So the 31 expected rows are correct by my source trace, but no committed command replays them. A reader who sees the
registry row will assume they run. Fix: add a replay step, or reword SKILL row 529 to "documentary expectations, not
executed by any committed command", and make L1's single verification run include a case replay (exit and finding
per row, with the embedded-policy overlay rule stated, per F1).

### F4 — MEDIUM (integrity): frozen mode accepts out-of-contract `expected_exit` and impossible pins and reports them as `frozen_verdict_mismatch` (exit 1), not `frozen_error` (exit 2)

- `tools/mado-action-plan.py:405-413` checks only the types (`str`, `str`, `str`, `int`). It does not check
  `expected_exit ∈ {0,1,2}`, that `expected_finding` is in the finding vocabulary (`:81-91`), or that the pair is
  consistent (`plan_safe` with `1` is impossible).
- `:425-430` compares equality, so an impossible pair returns `F_FROZEN_MISMATCH`, exit 1.
- The contract is stated differently: `:55` ("frozen_error exit 2: frozen expected.json unreadable/malformed")
  and `SKILL.md:530` ("2 could-not-evaluate (`snapshot_tampered` or `frozen_error`)").

Counterexample (by reading): `expected.json` with `"expected_exit": 7`, `"expected_finding": "plan_safe"` and valid
pins returns exit 1 `frozen_verdict_mismatch`. A malformed pin file is classed as "verdict differs". Likewise a
non-hex `plan_sha256` such as `"zz"` (`:420`) returns exit 2 `snapshot_tampered`, not `frozen_error`: fail-closed
exit code, wrong label.

Fix: after `:413`, require `expected_exit in (0,1,2)`, `expected_finding` in the vocabulary, the pair consistent with
`_classify`'s possible outputs, and both pins `^[0-9a-f]{64}$` (lowercase, or case-folded before check). Return
`F_FROZEN_ERROR` for each. Add selftest fixtures for exit 7, bad pin and impossible pair (none exist; the
`frozen-*` cases at `:674-704` cover only tamper, missing pin, match and mismatch).

### F5 — LOW-MEDIUM (integrity): frozen digest check and evaluation read the files separately (TOCTOU)

`run_frozen` verifies `_sha256(plan_path)` and `_sha256(policy_path)` at `:414-422`, then calls
`_evaluate(plan_path, policy_path)` at `:424`, which reopens and reparses both files. The bytes classified are not
the bytes digest-checked. A writer that swaps `plan.json` between `:416` and `:424` gets a `frozen_match` over
unpinned bytes. Requires local write access to the frozen dir during the run, so the severity is low, but the gate's
claim is "snapshot_tampered" detection and this path defeats it under concurrency.

Fix: read each input once with `_read_regular`, digest those bytes, and classify those same bytes (pass bytes or a
parsed object into `_evaluate`, not paths).

### F6 — LOW (calibration): frozen pins live in the same unauthenticated directory

`expected.json` carries `plan_sha256`, `policy_sha256` and the expected verdict. It is not itself pinned by the gate
(`:405-408` reads it from the same dir). Anyone who can write `plan.json` can also rewrite `plan_sha256` and
`expected_finding`/`expected_exit` to match their plan. The gate then emits `frozen_match` for a plan the operator
never approved. The gate proves only that the bytes match the pins beside them.

`SKILL.md:530` says "receipt separately binds executable and expectation digests to measured commit". That external
receipt is the actual anchor, and I did not verify it (outside this seat's lane). The gate's own wording
(`:65-66`, "both input digest pins are mandatory") and the `snapshot_tampered` label overstate what the gate itself
authenticates. Fix: say "self-consistency with co-located pins; authentication requires the external receipt", or
accept the pin as an argument rather than read it from the same directory.

## Counterexample summary (bounded, source-derived, not executed)

1. `paused: 1` accepted by a `!= True` paused check → `policy_paused_numeric_one` green, no committed test red (F1).
2. `omarchy-pkg-add libinput` as `read-source` → `plan_safe`, pinned as expected 0 at `safety-cases.json:411-423` (F2).
3. `expected_exit: 7` → exit 1 `frozen_verdict_mismatch` instead of exit 2 `frozen_error` (F4).
4. Swap of `plan.json` between `:416` and `:424` → `frozen_match` over unverified bytes (F5).
5. Rewrite of `plan.json` + `plan_sha256` + expected verdict together → `frozen_match` (F6).

## Residual risk and verification gaps

- Numeric/null paused behaviour is correct by source reading only. No test executes it, and this seat ran nothing.
- F2 is a classifier-limit design issue. Fixing it is a gate change, outside this lane. This seat only flags it.
- The receipt that binds expectation digests (SKILL:530) was not read. F6 severity depends on it.
- Counts: the cases file has 31 rows now. `w1/reports/SafetyCompositor.md` cites 20 (stale when written). Use 31.
- Checks for L1 to run once (not run by this seat): a per-row replay of `safety-cases.json` with overlay or full-canonical
  policy, the selftest with added numeric/null paused variants, and frozen fixtures for exit 7, bad pin and impossible pair.
