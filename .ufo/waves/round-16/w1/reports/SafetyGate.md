# SafetyGate — mado round 16 (C2): static action-plan safety gate

**Revision 2** (post-W2 review; supersedes revision-1 wording in this file).
Seat: `MadoR16.SafetyGate` (executor). Scope: bounded declared-plan
classifier. Files written (exclusive ownership):

- `tools/mado-action-plan.py` — new; Python 3 stdlib only
- `.ufo/waves/round-16/safety-policy.json` — new; persisted pinned policy

No installs, no host operations, no test/build/lint execution (per round
contract; L1 verifies once after integration). The gate itself never
executes supplied `argv`, never resolves executables on the host
(basename is a pure string operation), and never inspects host state.

## Delivered behavior

Input: `--plan PATH --policy PATH` (also `--selftest`, `--frozen DIR`).
`--policy` is rejected with `--frozen`/`--selftest`; empty `--frozen ""`
is rejected by argparse error.

Plan schema `mado-action-plan-v1`: object with `actions` list; each action
is an object with exactly `kind` (string) and `argv` (list of strings).
`schema` key optional but must equal the schema name if present. Unknown
keys on plan or action objects are malformed. Empty `actions` is safe.
Whole-plan schema is validated before any classification: a malformed
later action yields `plan_malformed`, never an earlier `blocked_*`.

Policy: the required policy is pinned in code (`PINNED_KINDS`,
`PINNED_PAUSED_SCOPE`, `PINNED_DENY_EXECUTABLES`). The supplied policy
must match it semantically: `paused` must be exactly boolean `true`
(`false`, `"true"`, `1`, `null`, missing → `policy_malformed`),
`kinds` must be exactly the six pinned kinds with pinned dispositions,
`paused_scope`/`deny_executables` must equal the pinned sets (duplicates
rejected), no unknown keys. Removing a denial, allowing `package-install`
or any mutation kind, adding a kind, or extra keys → `policy_malformed`.
This implements the PolicyTamper directive: denials cannot be removed and
`package-install` can never become allowed.

Classifier (finite, fail-closed; evaluated after both files pass
malformation checks; first refusing action in declared order wins):

- kind declared `deny`, or kind inside `paused_scope` while `paused`
  → exit 1 `blocked_action_kind:<kind>`
- kind absent from policy → exit 1 `unknown_action_kind`
- allowed kind with empty `argv` or blank `argv[0]` → exit 1 `empty_argv`
- allowed kind whose `argv[0]` lexical basename is one of the finite 12
  names `pacman yay paru systemctl hyprctl omarchy libinput evtest sudo
  sh bash env` → exit 1 `denied_executable:<basename>` (first basename
  wins: `argv=["sudo","cat",...]` → `denied_executable:sudo`;
  `/usr/bin/pacman` → `denied_executable:pacman`)
- otherwise → exit 0 `plan_safe`, detail "passed finite kind/argv[0]
  screen; not permission or safety"

Unlisted `argv[0]` values on allowed kinds return `0 plan_safe`
(`omarchy-pkg-add`, `python3 -c ...` residual controls present as
`omarchy-prefix-unscreened` / `unlisted-argv0-unscreened` — finite name
screen only, no allowlist/shell parsing; unscreened does not mean safe).

Exit 2 (`could-not-evaluate`): `plan_malformed`, `policy_malformed`,
`snapshot_tampered`, `frozen_error`. Policy is validated before the plan.
Malformed UTF-8, duplicate JSON keys, non-finite numbers (`NaN`/
`Infinity`), directories, symlinks (`O_NOFOLLOW`), FIFOs, devices and
other non-regular inputs → exit 2, no traceback. File reads are bounded
(`O_RDONLY|O_NONBLOCK|O_NOCTTY|O_NOFOLLOW`, `fstat` on the opened fd,
16 MiB cap, growth past stat size is an error — no silent truncation).
Any unexpected internal error is caught at top level and emitted as
exit 2 (`plan_malformed`/`frozen_error` with `unexpected internal …`
detail), never an exit-1 traceback.

## Verdict API (exact)

stdout, two lines:

```
MADO_PLAN: <finding>
{"schema":"mado-action-plan-verdict-v1","finding":"<finding>","exit":<int>,"action_index":<int|null>,"action_kind":<str|null>,"detail":"<str>"}
```

Finding strings (vocabulary pinned to `safety-cases.json`; SafetyCases
confirmed zero divergence across their 32 committed expectations):

- `plan_safe`
- `blocked_action_kind:<kind>` for `package-install`, `service-mutate`,
  `compositor-mutate`, `input-capture`
- `denied_executable:<basename>` for the 12 pinned basenames
- `unknown_action_kind`
- `empty_argv`
- `plan_malformed`, `policy_malformed`
- `snapshot_tampered`, `frozen_error` (exit 2)
- `frozen_match` (exit 0), `frozen_verdict_mismatch` (exit 1)

## `--frozen DIR` schema (for L1's `.ufo/waves/round-16/frozen/`)

`DIR` must contain `plan.json`, `policy.json`, `expected.json`.
`expected.json` (schema `mado-action-plan-frozen-v1`), exactly these keys
(all mandatory; unknown keys → `frozen_error`):

```json
{
  "schema": "mado-action-plan-frozen-v1",
  "plan_sha256": "<64-hex sha256 of plan.json bytes>",
  "policy_sha256": "<64-hex sha256 of policy.json bytes>",
  "expected_finding": "<evaluate-mode finding string>",
  "expected_exit": <0|1|2>
}
```

Pins must be exactly 64 hex chars; `(expected_exit, expected_finding)`
must be a reachable evaluate pair (`0/plan_safe`;
`1/blocked_action_kind:*`, `denied_executable:*`, `unknown_action_kind`,
`empty_argv`; `2/plan_malformed`, `policy_malformed`) — e.g. exit 7 or
empty finding or `plan_safe/1` → `frozen_error`. Both digest pins are
mandatory. Each input is read once; the same bytes are hashed and then
parsed/classified in-process (no re-open — no TOCTOU window). Mismatch or
unreadable input → `snapshot_tampered` (2). Verified inputs replayed:
match → `frozen_match` (0), mismatch → `frozen_verdict_mismatch` (1).

## `--selftest`

Self-invocation only, via a one-time snapshot of the script's own bytes
copied into the private temp dir (prevents mid-run reload drift; prints
`SELFTEST_SCRIPT_SHA256: <hex>`): `[sys.executable, "-I", <copy> ...]`,
`shell=False`, `stdin=DEVNULL`, `capture_output`, 60 s timeout, temp-dir
cwd, minimal env (`PATH` only). 52 cases (43 evaluate + 9 frozen; dynamic
`len(cases)+len(frozen_cases)` tally printed as `SELFTEST_SUMMARY:
<n>/52 passed`), each with literal pinned `(exit, finding)` constants;
ordering cases also pin `action_index`. Exit 0 iff all pass; exit 1 lists
failed names (declared mapping — selftest failure is 1 by protocol).

Coverage includes: actual libinput `sudo pacman -S` transaction blocked
as `blocked_action_kind:package-install`; service/compositor/input
mutations; unknown kind; missing/non-list/non-string `argv`; empty/blank
argv; denied executables (path-prefixed pacman, sudo wrapper, bash -c,
env wrapper); unlisted-argv0 residual controls; `paused` false/string/
1/null/missing; policy kind allow/removal/addition, shrunk deny lists,
unknown keys; duplicate JSON keys; NaN; bad UTF-8; directory/symlink/
FIFO inputs; malformed-later-action priority; policy-before-plan order;
first-refusal and denied-before-blocked ordering with `action_index`
asserted; frozen match/denied-match/tampered-plan/tampered-policy/
missing-pin/nonhex-pin/invalid-pair/empty-finding/verdict-mismatch.

## Anchors and limits

Anchors: `tools/mado-action-plan.py` — `PINNED_*` constants,
`_read_regular`, `_parse_json_bytes`, `_validate_policy`,
`_validate_plan`, `_classify`, `_evaluate`/`_evaluate_raw`,
`run_frozen`, `run_selftest`, `main`. `.ufo/waves/round-16/
safety-policy.json` is the persisted pinned policy, semantically
identical to `PINNED_*`.

Limits (explicit, unchanged): `plan_safe` means only absence of the
finite findings above — not credential/probe/privacy safety, not host
prevention, not enforcement, not permission. Denied `argv[0]` matching is
a lexical basename check on the declared string only; wrappers,
indirection and unlisted names are unscreened. The gate does not run
pacman or any argv member and does not read package/service/device state.
This catches the round-15 failure shape only when a plan is declared
through it — a seat that never writes a plan bypasses it; that residual
is operator/process-owned, not claimed here.

Revision-2 changes (W2 directives applied): `O_NOFOLLOW`/`O_NOCTTY` +
single-read hash-then-parse in frozen (TOCTOU closed); growth-past-stat
error; strict-JSON duplicate/non-finite rejection; top-level exception →
exit 2; `--policy` rejected under `--frozen`/`--selftest`; 64-hex pin and
reachable-pair validation; literal fixtures for paused=1/null,
empty-argv ordering, symlink/FIFO, malformed-later; `action_index`
assertions; selftest self-snapshot (`SELFTEST_SCRIPT_SHA256`); residual
labels renamed to `*-unscreened`; `plan_safe` detail wording bounded.

Risks/blockers: none blocking. `tools/__pycache__` from the earlier
syntax check was removed. Vocabulary reconciliation with `SafetyCases`
completed and confirmed two-way (their committed `safety-cases.json`
strings adopted verbatim; `paused:null` full-canonical case covered as
`policy_malformed`). L1 owns frozen-input authoring and post-integration
verification.
