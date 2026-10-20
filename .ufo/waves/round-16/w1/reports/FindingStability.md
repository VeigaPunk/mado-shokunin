# FindingStability — Mado round 16, wave w1

Seat: `MadoR16.FindingStability` (reviewer, leaf). Scope: deterministic finding
priority for malformed policy/plan and unsafe action in the static action-plan gate
(`tools/mado-action-plan.py`, `.ufo/waves/round-16/safety-policy.json`). Source
reading only. Nothing executed, nothing installed or updated (the lane contract
suspends the operator tooling directive this round; pacman transactions are paused).

## Status and limit

**The gate and policy are not on disk.** At my read (2026-10-20, after 05:40)
`tools/` contains only `mado-verify.sh` and `.ufo/waves/round-16/` has no
`safety-policy.json`. Everything below is a **design specification the SafetyGate
implementation must meet**, not an audit of code. L1 must check the real file
against §3 and the edge fixtures in §4 after integration. No gate, fixture or
subprocess was run by this seat.

## 1. Axes

1. **Determinism.** Same plan bytes + policy bytes (+ frozen digests) → same
   id, exit code, reason and action index, on every run and host.
2. **Fail-closed coverage.** No input reaches exit 0 without full validation.
3. **Precedence.** Exactly one primary finding; no exit-code collision between
   "could not evaluate" and "unsafe".
4. **Report hygiene.** Output carries no raw argv, absolute path, parser message
   or timestamp, so it is stable across checkouts and does not inject target text
   into reports.

## 2. Anchors read

- `.ufo/waves/round-16/w1/spec.json` items: **SafetyGate** (exit 0 `plan_safe`;
  1 failed stable reason; 2 could-not-evaluate malformed/policy; `paused=true`;
  allowed kinds `read-source`/`repo-write` with nonempty argv; blocked kinds
  `package-install`, `service-mutate`, `compositor-mutate`, `input-capture`;
  basename denylist; `--frozen DIR` with `snapshot_tampered`; "Report API
  exactly"). **PolicyTamper**: "gate must reject invalid or nonpaused policy this
  round." **ExitMap**: "code0/1/2 and stable finding design, invalid-policy
  fail-closed edge cases." **ExecBasename**: "wrappers not covered." **NoShell**:
  argv never executed.
- Lane precedent for ordered checks and stable ids: frozen design behaviour list
  `.ufo/waves/round-13/w1/reports/RegistryDraft.md:336-347` (digest before any
  execution; ids; codes 0/1/2) and table rows `:364-365`.
- Lane precedent for exit-code collision defects that this design must not repeat:
  `.ufo/waves/round-14/w1/reports/ReviewReceipt.md:13,16` (H1: refusal exit 2 equals
  child exit 2) and `.ufo/waves/round-14/w1/reports/ReviewRegistry.md:29-33` (F4:
  exit 2 meant four things across modes).
- Digest-before-subprocess pattern: `.ufo/waves/round-15/w1/reports/SourceTrust.md:116-117`.
- Round-15 lesson R15-V2, `corpus/lessons/round-15-verifier-spotcheck.md:268-277`:
  hard-coded fixtures are not real plan validation. This gate is static and must
  not invoke `pacman` for its own "real plan" claim.

## 3. Deterministic finding priority (the specification)

**P0 — One primary finding per run.** Output is one id, one exit code, one reason,
and the action index when the finding is per-action. Selection is the *first
failing check* in the total order below; evaluation stops there. Do not emit a
list of findings. A list makes report order a stability surface.

**P1 — Stage order is fixed:** S0 invocation/frozen → S1 policy → S2 plan shape
(the **whole** plan) → S3 safety. Consequences: policy beats plan; malformed
anywhere in the plan beats an unsafe action anywhere in the plan.

**P2 — Within a stage, checks run in the numbered order below.** Per-action checks
run in ascending action index, then check number.

**P3 — Exit code is a function of stage only:** S0, S1, S2 → 2; S3 → 1; no failure
→ 0 (`plan_safe`). No uncaught exception may exit with any of these codes by
accident (see F1).

**P4 — Detail is bounded and fixed.** Detail is the reason, the action index, and
for `denied_executable` the observed basename. Basename is capped at 64 characters
with non-printables escaped. Never print raw argv, absolute paths, timestamps,
parser messages, or a denylist entry chosen by iteration.

**P5 — No hash- or order-dependent selection.** Constants are tuples or sorted
sequences. No `set` iteration may choose a finding or a detail. String hashing is
randomized per process (PYTHONHASHSEED) [INF-docs], so a set-driven choice would
make the same input report different details on different runs.

### Total order

| Stage | # | Check | Finding id | Exit | Reason |
|---|---|---|---|---|---|
| S0 | 0.1 | unknown or duplicate flag; missing `--plan`/`--policy`; extra positional | `usage_error` | 2 | `usage` |
| S0 | 0.2 | frozen mode only: `expected.json` malformed | `frozen_error` | 2 | `frozen_schema` |
| S0 | 0.3 | frozen mode only: input missing, digest mismatch, or path escapes frozen root; checked before any content read | `snapshot_tampered` | 2 | `frozen_digest` |
| S0 | 0.4 | policy path not a regular file, unreadable, or over size cap; then the same for plan | `unreadable_input` | 2 | `policy_unreadable` / `plan_unreadable` |
| S1 | 1.1 | policy not strict UTF-8 JSON: BOM, trailing data, NaN/Infinity, duplicate keys, nesting over cap, `RecursionError` | `invalid_policy` | 2 | `policy_not_strict_json` |
| S1 | 1.2 | policy top level not an object; key set not exactly the pinned set | `invalid_policy` | 2 | `policy_shape` |
| S1 | 1.3 | `paused` is not JSON `true` (false, missing, `"true"`, `1`) | `invalid_policy` | 2 | `paused_not_true` |
| S1 | 1.4 | allowed/blocked constants differ from the pinned sets | `invalid_policy` | 2 | `policy_constants` |
| S2 | 2.1 | plan not strict UTF-8 JSON (same sub-cases as 1.1) | `malformed_plan` | 2 | `plan_not_strict_json` |
| S2 | 2.2 | plan top level not an object; `actions` missing or not an array; extra top-level key | `malformed_plan` | 2 | `plan_shape` |
| S2 | 2.3 | per action i ascending: not an object | `malformed_plan` | 2 | `action_not_object` |
| S2 | 2.4 | key set not exactly `{kind, argv}` | `malformed_plan` | 2 | `action_shape` |
| S2 | 2.5 | `kind` not a string | `malformed_plan` | 2 | `kind_type` |
| S2 | 2.6 | `argv` not an array (required for **all** kinds) | `malformed_plan` | 2 | `argv_type` |
| S2 | 2.7 | an argv element is not a string, is empty, or contains NUL | `malformed_plan` | 2 | `argv_element` |
| S2 | 2.8 | allowed kind with empty argv | `malformed_plan` | 2 | `argv_empty` |
| S2 | 2.9 | allowed kind whose argv[0] has an empty basename (for example `"x/"`) | `malformed_plan` | 2 | `argv_program` |
| S3 | 3.1 | `kind` in the blocked set | `blocked_kind` | 1 | kind name |
| S3 | 3.2 | `kind` is a string outside allowed and blocked (exact match; no case-fold or trim) | `unknown_kind` | 1 | `unknown_kind` |
| S3 | 3.3 | allowed kind: casefolded basename(argv[0]) equals a denylist name | `denied_executable` | 1 | basename |
| — | — | none of the above | `plan_safe` | 0 | `plan_safe` |

basename = text after the last `/` of `argv[0]`. Only `/` is a separator. No
shell, no `PATH` lookup, no resolution.

### Worked ordering examples

| Input | Primary result | Why |
|---|---|---|
| action 0 `input-capture`; action 1 `argv` is a string | exit 2 `malformed_plan`, `argv_type`, index 1 | P1: S2 precedes S3 across the whole plan |
| action 0 `read-source` `["env","pacman"]`; action 1 `read-source` `["pacman"]` | exit 1 `denied_executable`, index 0, basename `env` | lowest index wins; `env` is the first denied basename in argv[0] of action 0 |
| action 0 `package-install` `["pacman","-S","libinput"]` | exit 1 `blocked_kind`, index 0 | 3.1 precedes 3.3; kind decides before argv |
| policy `paused:false`, plan malformed | exit 2 `invalid_policy`, `paused_not_true` | P1: policy before plan; plan never parsed |
| policy has `"paused":false` then `"paused":true` | exit 2 `invalid_policy`, `policy_not_strict_json` | duplicate keys rejected, not last-wins |

## 4. Edge fixtures L1 should check (not run here)

| # | Input | Required primary result |
|---|---|---|
| E1 | policy `"paused": false` | 2 `invalid_policy` `paused_not_true` |
| E2 | policy `"paused"` duplicated (`false` then `true`) | 2 `invalid_policy` `policy_not_strict_json` |
| E3 | policy `"paused": "true"` | 2 `invalid_policy` `paused_not_true` |
| E4 | policy with `package-install` moved into allowed, `paused: true` | 2 `invalid_policy` `policy_constants` |
| E5 | policy malformed and plan malformed | 2 `invalid_policy`; plan content never read |
| E6 | plan action 0 `input-capture`, action 1 `argv` a string | 2 `malformed_plan` `argv_type` index 1 (one-pass implementations fail this) |
| E7 | plan action 0 `input-capture`, `argv: []` | 1 `blocked_kind` index 0 (argv content not required for blocked kinds; still an array) |
| E8 | plan `package-install` `["pacman","-S","libinput"]` | 1 `blocked_kind` (kind before argv) |
| E9 | `read-source` `["/usr/bin/PACMAN","-Sp"]` | 1 `denied_executable`, detail `PACMAN` |
| E10 | `read-source` `["env","pacman"]` | 1 `denied_executable`, detail `env` |
| E11 | kind `"Read-Source"` or `"read-source "` | 1 `unknown_kind` (no normalization) |
| E12 | `read-source` `["pacman\u0000x"]` | 2 `malformed_plan` `argv_element` |
| E13 | `read-source` `["timeout","5","pacman"]` | **0 `plan_safe`** — documented wrapper gap, see F4; red control for ExecBasename |
| E14 | `repo-write` with `argv: []` | 2 `malformed_plan` `argv_empty` |
| E15 | `read-source` `["x/"]` | 2 `malformed_plan` `argv_program` |
| E16 | plan top level has `"note": ...` | 2 `malformed_plan` `plan_shape` |
| E17 | `"actions": []` | 0 `plan_safe` under D2 |
| E18 | any internal exception (for example `RecursionError` from deep nesting) | 2 `internal_error` via catch-all; never exit 1 (see F1) |
| E19 | two runs of the same input under different PYTHONHASHSEED | identical stdout and exit code |

## 5. Decisions I recommend L1 pin (ExitMap row)

- **D1.** Unknown *string* kind → exit 1 `unknown_kind`: the plan is well-formed, so
  exit 2 would be a misuse. Non-string kind → exit 2 at 2.5. Either choice is
  defensible; pick one and fixture it.
- **D2.** `"actions": []` → exit 0 `plan_safe`. The schema is satisfied and there is
  nothing to refuse. Exit 0 means "static classification clean," **not**
  authorization (see F7).
- **D3.** Denylist comparison is casefolded. Linux executable names are
  case-sensitive, so casefolding adds only false positives, which is the fail-closed
  direction.
- **D4.** `argv` must be an array of strings for every kind, including blocked kinds,
  so check 3.1 never depends on argv contents.

## 6. Findings (severity ordered)

**F1 — Medium, stability. Uncaught exceptions exit 1.** CPython exits 1 on an
uncaught exception [INF-docs]. Exit 1 is the "unsafe" code. A crash (for example
`RecursionError` on deep JSON, or an `OSError` on a racing file) is therefore
indistinguishable from a blocked plan by exit code. Required: a top-level catch-all
that maps any unexpected exception to exit 2 `internal_error`, with the traceback
suppressed from the finding. Fixture E18.

**F2 — High, safety. Duplicate JSON keys.** CPython's `json` keeps the last value
for a duplicated key [INF-docs]. `{"paused": false, "paused": true}` would then pass
S1, and `{"kind": "package-install", "kind": "read-source"}` would classify as
`read-source`. Required: an `object_pairs_hook` that rejects any duplicate key in
both policy and plan (E2). This is the single most important fail-open edge.

**F3 — Medium, stability. NaN/Infinity accepted by default.** `json.loads` accepts
`NaN`, `Infinity` and `-Infinity` unless `parse_constant` rejects them [INF-docs].
Required: reject all three in 1.1 and 2.1, so the input is strict JSON and identical
on every Python build.

**F4 — High, safety. Basename denylist is bypassed by wrappers.** Checks 3.3 inspect
only `argv[0]`. `timeout 5 pacman …`, `nice`, `nohup`, `stdbuf`, `setsid`, `xargs`,
`doas`, `su`, `ssh`, `busybox`, `python3 -c`, `perl -e`, and similar all put a denied
tool in `argv[1..]`, so E13 passes as `plan_safe`. The spec calls this a "bounded
declared-plan classifier," so the limit is disclosed by design. It is still a
fail-open path inside S3 and must be stated in the gate's output contract and the
SKILL caveat. Options for the operator or L1, both scope decisions:
(a) extend the denylist with the wrapper set; or
(b) replace the denylist for `read-source`/`repo-write` with an explicit executable
allowlist, which is the fail-closed design.
I recommend (b). I have not applied either option because it changes the pinned
denylist.

**F5 — Medium, stability. Set iteration can change the detail.** If SafetyGate
iterates a `set` of denylist names to find a match, the reported `denied_executable`
name depends on PYTHONHASHSEED, while the id stays the same. Required by P4/P5: the
detail is the observed basename, not a constant chosen during iteration. E19 must
show identical output across seeds.

**F6 — High, stability. Single-pass evaluation violates P1.** A one-pass loop that
returns 1 at the first unsafe action returns before it has seen a later malformed
action. The result then depends on action order, not on the stage precedence. E6
is the discriminating fixture; L1 must confirm it returns 2.

**F7 — Medium, safety/semantics. Exit 0 read as authorization.** `paused=true` and
exit 0 can be read as "execution permitted." The gate must state in its output
and in SKILL that exit 0 means classification clean, no execution authorized, and
that the gate never executes argv (NoShell). Data stays data.

**F8 — Low, hygiene. Unbounded echo.** Raw argv or basename echoed into a report is
a data-fence breach and makes output host-dependent. Covered by P4; the 64-character
cap and escaping are required.

## 7. Residual risk and verification gaps

- Gate and policy absent at read time; no implementation was audited (see Status).
- No execution: E1–E19 are specified, not run. CPython behaviours marked [INF-docs]
  (duplicate-key last-wins, NaN acceptance, uncaught-exception exit 1, set-hash
  ordering) are from documented stdlib behaviour and were not reproduced here.
- For SafetyCases (its own seat, not messaged by me, as the contract requires): E2,
  E6, E7, E13, E18 and E19 are the cases most likely to be missing, since they are
  the precedence and wrapper cases. L1 should confirm they exist with pinned expected
  codes before accepting the SafetyCases output.
- Wrapper bypass (F4) is unresolved and needs an operator or L1 decision.

## 8. Tools and host

No installs or updates by this seat. The lane contract suspends the operator tooling
directive this round, and all pacman transactions are paused host-wide. Nothing
under `~/.omp` was opened. No live probe, compositor, service or input-device access.

## 9. Files written

Only this report: `.ufo/waves/round-16/w1/reports/FindingStability.md`.
