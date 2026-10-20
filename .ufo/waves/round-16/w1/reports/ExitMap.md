# ExitMap — review of plan-gate exit codes, stable findings, invalid-policy fail-closed

Seat: `MadoR16.ExitMap` (reviewer, leaf). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: design review of the `mado-action-plan` gate as specified. Source reading only.
Nothing executed, installed, or changed outside this report.

Status at review time: **the gate is not yet implemented.** `tools/` contains only
`mado-verify.sh`; `.ufo/waves/round-16/safety-policy.json` does not exist. Every finding
below is against the spec text, not code. Verdict: the exit map is **not yet pinnable**; six
High items must be decided before SafetyGate and SafetyCases are written against it.

## Anchors read

- `.ufo/waves/round-16/w1/spec.json:10` (item `SafetyGate`): "Exit 0 clean finding plan_safe;
  1 failed stable reason; 2 could-not-evaluate malformed/policy"; "Persist policy paused=true";
  "unknown/malformed fail closed"; denylist `pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,
  evtest,sudo,sh,bash,env`; "--selftest self-invocation subprocess fixtures"; "--frozen DIR
  verifies expected.json input digests ... tampering returns 2 snapshot_tampered"; "Gate must
  never execute supplied argv or inspect host".
- `.ufo/waves/round-16/w1/spec.json` items `SafetyCases` ("Agree API from context"),
  `FindingStability`, `PlanSchema`, `PolicyTamper`, `UnknownActions`, `SelftestTruth`.
- `corpus/QUALITY.md:82-95` (criterion 21): declared-plan verdict is "not tool interception,
  host immutability, a real package dry run or remediation"; must fail on incident-shaped
  libinput transaction, disguised executable, unknown kind, malformed action.
- `corpus/lessons/round-15-verifier-spotcheck.md:154-163`: hard-coded predicate controls are not
  real plan validation; `already_installed_in_plan` exit 1 / `new_only_plan` exit 0.
- `.ufo/waves/round-13/w1/ReviewRegistry.md:42`: fleet vocabulary `0` clean · `1` failed · `2`
  could-not-evaluate; "any other exit code is could-not-evaluate". Lines `:31`, `:42`
  (failing self-test is not `1`), and `:65`-`:69` (per-mode exit map).
- `.ufo/waves/round-13/w1/reports/RegistryDraft.md:333-341`: frozen-snapshot precedent
  (digest before harness run; symlink escape is `snapshot_tampered`).
- `tools/mado-verify.sh:12-13` header exit map; `:3645-3665` argument refusal returns 2.

## Recommended exit and finding table (proposal to pin, one table only)

Evaluation order is fixed: usage → input integrity → policy → plan top level → each action in
index order. Short-circuit at usage, input, policy, and plan top level. Within the action list,
evaluate every action without short-circuit. Final exit = 2 if any class-2 finding, else 1 if
any class-1 finding, else 0. Printed findings are sorted by (action index, code); the verdict
line names the first finding in that order.

| Condition | Exit | Stable finding |
|---|---|---|
| All actions clean; policy valid | 0 | `plan_safe` |
| kind in {package-install, service-mutate, compositor-mutate, input-capture} | 1 | `blocked_kind` |
| read-source/repo-write argv0 basename in denylist (or outside allowlist, if adopted, see H5) | 1 | `forbidden_executable` |
| kind is not exactly one of the six known strings (case and whitespace are not normalized) | 2 | `unknown_kind` |
| action not object; extra key; missing kind/argv; argv missing, empty, non-list, non-string element, empty/whitespace/control-char/trailing-slash argv0 | 2 | `action_malformed` |
| plan not object; missing or extra top-level key; `actions` not list; `actions` empty (see M1) | 2 | `plan_malformed` / `plan_empty` |
| policy unreadable, not regular file, over size cap, not strict UTF-8 JSON, duplicate key, NaN/Infinity, extra/missing key, not exactly the in-code table, `paused` is not `True` | 2 | `policy_invalid` |
| `--policy` absent (no default file) or flags malformed, duplicated, unknown, or mixed with `--frozen` | 2 | `usage_error` |
| frozen: expected.json missing/malformed; digest mismatch; symlink or `..` escape | 2 | `frozen_error` / `snapshot_tampered` |
| frozen: computed verdict differs from expected | 2 | `frozen_mismatch` |
| selftest: any failed assertion, fixture mktemp failure | 2 | `selftest_failed` |
| any uncaught exception (guard at top level) | 2 | `internal_error` |

## Findings

### High

**H1 — Typo and extra keys can turn into exit 0.** The schema says "list of objects containing
kind and argv", which does not forbid other keys or require `actions`. If a missing `actions`
key defaults to `[]`, a plan written as `{"action": [{"kind": "package-install", ...}]}` yields
`plan_safe`, exit 0. Extra action keys (`shell`, `command`) are silently ignored and look like
commands the gate did not check. Fix: exact key sets for plan `{actions}` and action
`{kind, argv}`; missing or extra key is class 2. No defaults for any required key.

**H2 — Uncaught Python exceptions exit 1, which collides with "failed stable reason".** A bare
traceback from an unhandled exception exits with status 1 [INFERENCE: documented CPython
behaviour, not executed here]. Fleet vocabulary says only `1` means failed, and every other code
is could-not-evaluate. Paths that can raise include `RecursionError` on deep JSON, `MemoryError`,
`UnicodeDecodeError`, `json` errors, and `BrokenPipeError` on stdout. Fix: a top-level guard maps
every exception to `internal_error`, exit 2. The selftest must include one crash-path fixture
that asserts exit 2, not 1. Also: `--help` exits 0 with no verdict line; it must not look like a
clean plan. Make it exit 2 or print an explicit `no_plan_evaluated` line.

**H3 — Exit codes for unknown kind, missing argv, and malformed argv are not pinned.** Line 10
says "unknown/malformed fail closed" for kinds, and "2 could-not-evaluate malformed/policy" for
exit. It does not say whether an unknown kind is 1 or 2. SafetyCases must carry `expected_code`
per case, so two seats writing against this text will diverge. Recommendation: `unknown_kind`
and `action_malformed` are 2; `blocked_kind` and `forbidden_executable` are 1. An unknown kind is
"could not classify", not "classified as blocked".

**H4 — Policy file is an unpinned input.** `--policy PATH` lets the policy be edited to
`paused: false`, to move `package-install` into allowed kinds, or to drop denylist entries. The
spec says to persist `paused=true` but does not require the gate to reject other content. Fix:
after strict parse, compare to an in-code constant table; any difference is `policy_invalid`.
Further points: test `paused is True`, not truthiness (`1`, `"yes"`, `[0]` are truthy); missing
`paused` must not default to either value; reject duplicate keys via `object_pairs_hook`
(stdlib `json` keeps the last value silently [INFERENCE: documented]); reject NaN/Infinity via
`parse_constant`. No default policy path: an absent `--policy` must be `usage_error`, never
"no restrictions". PolicyTamper's rule "reject invalid or nonpaused policy this round" needs this
exact check, not a generic schema check.

**H5 — The denylist is fail-open for read-source and repo-write.** Bypass shapes that a
basename denylist does not catch, read as static text:
- argv0 `/usr/bin/pacman/` → `os.path.basename` returns `''` [INFERENCE: documented].
- argv0 containing whitespace or control characters, e.g. `"pacman -S libinput"` or `"pacman\u0000"`.
- Wrappers not on the list: `nice`, `nohup`, `timeout`, `xargs`, `stdbuf`, `setsid`, `flock`,
  `command`, `exec`, `busybox`, `doas`, `su`, `pkexec`, `runuser`, `systemd-run`,
  `python3 -c`, `find -exec`.
- `kind` is a self-declared label. `read-source` with `["rm", ...]` or `["tee", ...]` passes as
  `plan_safe`.

Fix (preferred, since the text says fail closed): allowlist argv0 basenames for read-source and
repo-write, instead of a denylist. Either way, reject argv0 that is not a plain basename (no `/`
trailing, no whitespace, no control characters). State explicitly that kind labels are not
enforced. ExecBasename owns wrapper depth; this seat flags the fail-open shape, not the list.

**H6 — The stable finding vocabulary is not in the spec.** The only pinned strings are `plan_safe`
and `snapshot_tampered`. SafetyGate and SafetyCases are told to "agree API from context", and the
context does not name the other findings. Two seats will invent divergent names, and a
selftest can pass against wrong constants. Fix: one table (H-section above) written into the
spec or `safety-policy.json`. SafetyCases copies its expected findings from that table and does
not import the gate.

### Medium

**M1 — Empty `actions` is undefined.** `{"actions": []}` would default to `plan_safe`, exit 0.
A generator that emits nothing then looks green. Recommend `plan_empty`, exit 2. If the owner
chooses 0, it must still carry a distinct finding and be pinned. PlanSchema owns the wider
ambiguity (arrays, strings, types).

**M2 — Precedence and ordering are undefined for multi-violation plans, and set iteration is not
stable.** A plan with `package-install` plus an unknown kind has no defined code. If the gate
collects matches in a `set`, string hash randomization per process (`PYTHONHASHSEED`) can change
which reason prints first [INFERENCE: documented]. Fix: the order and table above; sort findings
by (index, code); no absolute paths and no dict or set iteration in finding text.

**M3 — Frozen mode exit semantics are undefined, and one reading is fail-open.** "Compares
verdict/code" does not say what exit a matching run returns. If a matching red fixture returns 0
because "frozen matched", a caller reads a red plan as green. Fix:
- A matching frozen run returns the plan's own verdict code (red stays 1) and prints a separate
  `frozen_match` token. A mismatch is `frozen_mismatch`, exit 2.
- Digest check comes before any parse. Read the bytes once and hash and parse that same buffer
  (TOCTOU).
- Pin the digest algorithm (sha256, lowercase hex) and the `expected.json` schema.
- Reject `--frozen` mixed with `--plan` or `--policy` as `usage_error`.
- Limit to state: `expected.json` is itself unpinned. A paired edit of plan, policy, and
  expected passes unless `expected.json` is committed or pinned (cf. RegistryDraft:333-341).

**M4 — Self-test exit semantics.** A failed assertion or fixture failure must be exit 2
(`selftest_failed`), not 1: a red self-test is not "failed plan" (ReviewRegistry:31). A passing
self-test exits 0; it must print a mode-specific token (for example `MADO_ACTION_PLAN_SELFTEST:
N/N`) so no consumer reads it as `plan_safe`. Assertions must be subprocess exit plus finding,
not helper-only, and the constants must be written from the H6 table. Fixtures naming `pacman`
or `sudo` must never run; fixtures live under `mktemp` and nothing is written into the lane.

**M5 — `plan_safe` overclaims, and the verdict does not name its revision.** A token named
`plan_safe` with exit 0 reads as host or package safety. QUALITY 21 and the round-15 spot-check
say the verdict is declared-plan only. Recommend that the verdict line print the gate's sha256
(lane precedent: "a verdict names the revision it was measured against", PROTOCOL.md:393 as
quoted in ReviewRegistry F3) and the explicit limit. Naming is optional, for example
`declared_plan_clean`, but pick one and pin it.

**M6 — Input-integrity edges.** For `--plan` and `--policy`: a FIFO or device blocks on open;
require a regular file via `stat` before read. Set a size cap, returning `input_too_large`. Decide
on a UTF-8 BOM (reject). Require the top level to be a JSON object. Decide `--plan -` (stdin): refuse
or define it.

### Low

**L1 — Do not echo argv into findings.** argv may carry tokens or credentials. Print action index
and stable code only (CredentialFence privacy line).

**L2 — Residual behaviour, no change requested.** Interrupt and broken pipe are covered by H2's guard.

## Residual risk (not fixable by the table)

- `kind` is self-declared and argv is not semantically analysed; a `read-source` label can carry a
  write. This is the declared-plan limit, to be stated in the registry row.
- The gate has no execution authority. Consumers that pipe exit 0 into an executor would turn a
  classifier into an authorization. No consumer is defined; the spec should say the gate authorizes nothing.
- Pause is recorded in policy but not enforced by the gate on the host.
- Frozen digests prove byte identity, not that the pinned expected verdicts are correct.

## Verification gaps (for L1, once, after integration)

- Confirm `tools/mado-action-plan.py` implements the H-table, and no path exits 1 for an
  uncaught exception (grep the top-level guard and the selftest crash fixture).
- Confirm SafetyCases `expected_finding` strings equal the H-table strings, byte for byte.
- Confirm `--help` and `--selftest` success are not reportable as a plan verdict.
- Confirm `safety-policy.json` equals the in-code constant table, and that `paused` is checked with `is True`.
- Confirm no `subprocess`, `os.system`, or `exec` path touches supplied argv, except the
  selftest self-invocation of the gate itself.

## Tooling record

No tools installed or updated. No pacman, service, package, compositor, input-device, or
live-command operation. Source reading only. Python-behaviour statements marked [INFERENCE] are
documented stdlib behaviour and were not executed by this seat.
