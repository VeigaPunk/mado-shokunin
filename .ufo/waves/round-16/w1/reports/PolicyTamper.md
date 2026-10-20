# PolicyTamper — round 16 w1 sentinel report

Seat: `MadoR16.PolicyTamper` (sentinel, read-only, leaf). Surface: the
persisted `paused` policy consumed by the round-16 action-plan gate
(`tools/mado-action-plan.py --plan PATH --policy PATH`, policy
`.ufo/waves/round-16/safety-policy.json`, owned by `MadoR16.SafetyGate`).
Contract read first: `corpus/lessons/round-15-verifier-spotcheck.md`
(R15-V1/R15-V2: pacman paused host-wide; fixtures are not real plan
validation). `~/.omp/agent/RULES.md` read; round context forbids installs and
takes precedence. **No tools installed or updated.**

## Axes

1. **Fail-closed**: no tampered/invalid/non-paused policy may yield exit 0
   `plan_safe`.
2. **Exit-map truth**: policy defects map to exit 2 (could-not-evaluate) with a
   stable finding, never a Python traceback exit 1 (which collides with the
   "failed" verdict).
3. **Authority**: the policy file cannot weaken code-pinned blocked kinds or
   denied basenames while the pause holds.
4. **Snapshot integrity**: `--frozen` policy tampering returns 2
   `snapshot_tampered`, never a changed verdict.

## Status of the reviewed artifact

At review time `tools/mado-action-plan.py` and
`.ufo/waves/round-16/safety-policy.json` **did not exist** (three glob checks
of `tools/*` and `.ufo/waves/round-16/*`; present were only
`tools/mado-verify.sh`, `waybar-draft.txt`, `measure.py` and
`safety-cases.json`). This report is therefore a **spec-level adversarial
review** of the SafetyGate assignment in `.ufo/waves/round-16/w1/spec.json`
(item `SafetyGate`) plus a static read of the landed independent
`safety-cases.json` (PT-10), not an audit of gate code. L1 must apply the
checklist in §Acceptance to the landed bytes. Early must-haves and the
PT-10 case gap were sent to `MadoR16`.

## Grounding performed

Language-semantics probe run in this seat's own Python session (CPython
stdlib `json`; no gate, plan, policy, host, compositor, package or service
was read or executed):

| Input / operation | Observed |
|---|---|
| `json.loads('{"paused":false,"paused":true}')` | `{'paused': True}` — last duplicate wins silently |
| `json.loads('{"paused":true,"x":NaN}')` | accepted, `nan` |
| `bool(json.loads('{"paused":"false"}')['paused'])` | `True` |
| `json.loads('{"paused":1}')['paused'] == True` | `True` (also `1.0`; `1 in {True}` is `True`; `isinstance(True, int)` is `True`) |
| invalid UTF-8 byte decode | `UnicodeDecodeError` (a `ValueError`, **not** `JSONDecodeError`) |
| UTF-8 BOM text | `JSONDecodeError` |
| 200000-deep `[` nesting | `RecursionError` (not `ValueError`) |
| `json.loads('[]').get('paused')` | `AttributeError` |
| `open('/tmp')` (directory as `--policy`) | `IsADirectoryError` |
| uncaught exception in `python3 -c` | process exit **1** |

## Findings

### PT-1 — HIGH: truthiness / equality `paused` check admits non-paused policy

**Exploit path:** policy `{"paused": "false", ...}` (or `1`, `1.0`, `[0]`,
`{"x":0}`, `"no"`) with a gate written as `if policy.get("paused"):` or
`policy["paused"] == True` / `in (True,)`. All evaluate as paused; the gate
proceeds and can emit 0 `plan_safe`.
**Impact:** the round's sole persisted pause signal is bypassable by type
confusion; a reviewer reading `"paused": "false"` believes the gate is not
paused while it behaves as paused (or vice versa if a later permissive branch
exists) — fabricated policy provenance.
**Remediation:** `type(v) is bool and v is True`; anything else → exit 2,
stable finding (proposed `policy_not_paused` for well-typed `false`,
`policy_invalid` for missing/wrongly typed). Do not use `isinstance(v, bool)`
plus `==`; do not use truthiness.

### PT-2 — HIGH: duplicate keys flip the effective value invisibly

**Exploit path:** `{"paused": false, "paused": true}` parses as `True`; a
reviewer grepping the file sees `"paused": false` first. The reverse
(`true` then `false`) correctly fails but the forward order passes 0.
Same applies to duplicated `blocked`/`allowed` keys if the policy carries them.
**Remediation:** `json.loads(..., object_pairs_hook=hook)` where `hook` raises
on any repeated key, and `parse_constant` raising on `NaN`/`Infinity`/
`-Infinity` → exit 2 `policy_invalid`. Apply the same loader to the plan.

### PT-3 — HIGH: policy file as authority can weaken the floor

**Exploit path:** policy keeps `"paused": true` but lists `package-install`
(or `service-mutate`, `compositor-mutate`, `input-capture`) as allowed, or
drops `pacman`/`sudo` from denied basenames, or adds an unknown permissive
key (`"allow_all": true`, `"override": ...`). If the gate reads its kind/
basename lists from the policy, the round-15 transaction
`sudo pacman -S --needed --noconfirm libinput libinput-tools` declared as
`package-install`, or as `read-source` with argv `["pacman", ...]`, returns 0.
**Impact:** the "fail-closed static desktop action-plan safety gate" claim is
false; C2 would be credited for a classifier whose verdict is set by an
editable data file.
**Remediation (smallest):** keep blocked kinds, allowed kinds and the twelve
denied basenames (`pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`)
as code constants. Require the policy object to have **exactly** the expected
key set and values structurally equal to those constants (sets compared after
type check: list of unique strings); any difference, extra key or missing key
→ exit 2 `policy_invalid` (or `policy_mismatch`). Policy may not add or
remove entries this round. Equivalent acceptable design: policy digest pinned
in code. Either way the persisted file is a declared record of the pause,
not an override channel.

### PT-4 — HIGH: uncaught exceptions mis-map to "failed" exit 1

**Exploit path / defect:** top-level non-object policy (`[]`, `null`, `"x"`,
`true`) → `AttributeError`; invalid UTF-8 → `UnicodeDecodeError` (escapes an
`except json.JSONDecodeError`); deep nesting → `RecursionError` (escapes
`except ValueError`); `--policy /tmp` → `IsADirectoryError`; `--policy` naming
a FIFO or `/dev/stdin`/`/dev/zero` → hang or unbounded read. Uncaught Python
exceptions exit 1.
**Impact:** exit 1 means "evaluated, unsafe plan" in the declared map; an
invalid policy would be reported as a plan verdict — an exit-map lie that the
selftest might even "pass" if it only checks `rc != 0`.
**Remediation:** open with `os.open(..., O_RDONLY | O_NOFOLLOW?)` is optional;
minimally `fstat` the opened descriptor and require `S_ISREG`, read a bounded
size (e.g. ≤ 1 MiB), decode strict UTF-8, and wrap `main()` so every
`Exception` (plus `RecursionError`) maps to exit 2 with a stable finding.
`KeyboardInterrupt` may stay default. Applies to plan and expected.json too.

### PT-5 — MEDIUM: ordering lets an unsafe policy coexist with plan_safe

**Exploit path:** gate classifies actions first, returns 0 for an all
`read-source` plan, and only consults `paused` when a `package-install`
action appears (lazy check). A `paused:false` / malformed policy then yields 0
for benign plans, so the receipt shows `plan_safe` under an invalid policy.
**Remediation:** validate the policy completely and first; any policy defect
returns 2 before the plan is parsed for verdict purposes. Deterministic
priority (coordinate with `FindingStability`): usage → policy read/parse →
policy schema/paused → plan read/parse → plan schema → first unsafe action.
Never emit `plan_safe` unless the policy validated.

### PT-6 — MEDIUM: dead permissive `paused: false` branch

**Exploit path:** implementing "if not paused: allow package-install when
new-only" (anticipating the future R15-V2 flow) creates a latent bypass that
PT-1/PT-2/PT-3 tampering can reach, and implies a capability the round has
not built (real `pacman -Sp --print-format '%n %v'` plan + installed-name
comparison).
**Remediation:** this round there is no un-paused mode. `paused != True` is
exit 2; no code path changes classification on the flag. Future un-pause
semantics belong to an operator-authorized later round.

### PT-7 — MEDIUM: `--frozen` self-referential pins

**Exploit path:** `--frozen DIR` verifies `plan.json`/`policy.json` against
digests in `DIR/expected.json`. A tamperer editing `policy.json` to
`paused:false` and rewriting both the pin and expected verdict/code in
`expected.json` gets a consistent "match". Also, if `expected.json` omits the
`policy.json` pin and the gate skips absent pins, policy tampering is
undetected. Prior `round-14/frozen/verify.py` lines 64-71 show the correct
exact-key pattern but likewise do not pin `expected.json` itself.
**Remediation:** require exactly `{plan.json, policy.json}` pins (missing/extra
→ 2 `snapshot_tampered` or `frozen_error`), verify both digests before
evaluation, and run the same full policy validation (PT-1..PT-5) on the frozen
policy — a correctly pinned `paused:false` snapshot must still be 2, not
`frozen_match` against an expected code 2/0. Record `expected.json` SHA-256 in
the L1 receipt / registry pinned-value column so the snapshot set is anchored
outside itself. State the limit: frozen mode detects post-pin drift, not a
malicious re-pin.

### PT-8 — LOW: environment/argument fallbacks

**Exploit path:** missing `--policy` silently falling back to a built-in or
default path, or any env var (`MADO_POLICY_*`) overriding the flag.
**Remediation:** `--policy` required; no env overrides; missing → argparse
usage exit 2. `--plan` and `--policy` naming the same file is caught by schema
validation (exact key set), not special-cased.

### PT-9 — LOW: kind/key normalisation

**Exploit path:** case-folding or `.strip()` on kinds/keys (`"Paused"`,
`"package-install "`, `"Read-Source"`) collapses distinct tamper inputs into
accepted ones.
**Remediation:** exact byte-string comparison; unknown → fail closed (plan) or
`policy_invalid` (policy).

### PT-10 — HIGH: landed independent cases never vary the policy

**Evidence:** `.ufo/waves/round-16/safety-cases.json` (landed during this
review, `SafetyCases`) line 8 states all cases use the committed
`paused=true` policy "unless a case embeds its own policy field"; none of its
20 cases (lines 29–283; parsed count 20, zero carry a `policy` key) embeds
one. Its vocabulary (line 22) defines
`policy_malformed` (exit 2) but no case exercises it.
**Exploit path:** a gate that never reads `paused`, or reads it truthily
(PT-1), or trusts policy lists (PT-3), passes every independent case and its
receipt would read as a fail-closed policy gate.
**Impact:** C2's "reject invalid or nonpaused policy" property would be
unmeasured while appearing covered — inflated operability credit.
**Remediation:** L1/SafetyCases add policy-embedding cases P1, P3, P4, P6,
P8, P9, P13 from the table below, each `expected_code: 2`,
`expected_finding: "policy_malformed"` (the landed vocabulary; a distinct
`policy_not_paused` id is acceptable only if the gate and cases agree).
Cases need a policy-bytes field (not a parsed object) so duplicate-key and
`NaN` rows survive JSON round-tripping.

## Required selftest controls (subprocess self-invocation, exit + finding)

Each case writes a temporary policy beside a fixed benign plan
(`{"actions":[{"kind":"read-source","argv":["cat","README.md"]}]}`) and must
assert **exit 2 and the specific policy finding**, plus absence of
`plan_safe` in output; the green control asserts exit 0 `plan_safe`.

| # | Policy bytes (abbrev.) | Expected |
|---|---|---|
| P0 | canonical persisted policy | 0 `plan_safe` (green control) |
| P1 | `"paused": false` | 2 `policy_not_paused` |
| P2 | `paused` key absent | 2 `policy_invalid` |
| P3 | `"paused": "true"` / `"false"` | 2 `policy_invalid` |
| P4 | `"paused": 1` | 2 `policy_invalid` |
| P5 | `"paused": null` | 2 `policy_invalid` |
| P6 | `{"paused":false,"paused":true}` | 2 `policy_invalid` |
| P7 | top-level `[]` / `null` / `true` | 2 `policy_invalid` |
| P8 | canonical + `"allow_all": true` | 2 `policy_invalid` |
| P9 | canonical with `package-install` moved to allowed | 2 policy finding |
| P10 | canonical with `pacman` removed from denied basenames | 2 policy finding |
| P11 | invalid UTF-8 byte / `NaN` value | 2 `policy_invalid` |
| P12 | `--policy` pointing at a directory | 2 (no traceback) |
| P13 | P1 policy with the round-15 `package-install` plan | 2 (policy first), not 1 |
| F1 | `--frozen` with policy edited to `paused:false`, old pin | 2 `snapshot_tampered` |
| F2 | `--frozen` with `policy.json` pin missing | 2, not match |

Finding names are this seat's proposals; the landed cases vocabulary
collapses all policy rows to `policy_malformed`, which is acceptable if the
gate agrees. L1 should bind them to the landed constants.
A helper-only test (calling `validate_policy()` in-process) does not satisfy
this; each row must go through the CLI exit code (see `SelftestTruth`).

## Acceptance checklist for L1 (static reading of landed bytes)

- [ ] `paused` compared with `type(...) is bool and ... is True`; no truthiness.
- [ ] Duplicate-key and non-finite-constant rejection on policy, plan, expected.
- [ ] Kinds and twelve basenames are code constants; policy must equal them
      exactly; extra/missing keys rejected.
- [ ] Policy validated before plan; no `plan_safe` path without valid policy.
- [ ] No branch alters classification when `paused` is false.
- [ ] Whole-`main` exception wrapper → exit 2; regular-file + size bound.
- [ ] `--frozen` requires both pins and re-validates policy content.
- [ ] Selftest rows P0–P13, F1–F2 exist as subprocess exit+finding asserts.
- [ ] `safety-cases.json` (or gate selftest) carries policy-varying rows
      (PT-10), using a raw policy-bytes field.
- [ ] Persisted `safety-policy.json` has `"paused": true` (JSON boolean).

## Limits

- Spec-level review; landed gate and policy bytes were not available to this
  seat. No gate, selftest, plan or policy was executed; `safety-cases.json`
  was read statically only.
- A static declared-plan classifier cannot stop an agent that never submits a
  plan, mislabels intent outside argv, or runs commands directly; policy
  integrity here protects the gate's verdict, not the host. The R15-V1 harm
  remains operator-owned and is not remediated by any of this.
- Frozen pins detect drift, not a coordinated re-pin (PT-7).
- No package, service, compositor, input-device or live probe performed; no
  install. Python semantics above come from the seat's own interpreter only.
