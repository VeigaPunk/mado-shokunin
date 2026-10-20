# AttackStaleReports — mado round 16, w2 (leaf critic)

Seat: `MadoR16.AttackStaleReports`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Method: source reading, `sha256sum`, `wc`, `git status --porcelain`, and a parse-only `ast.parse` of the gate. No gate, selftest, measure.py, frozen run, install, pacman, service, compositor or input operation. Read-only throughout. One background grep/python job (bg_2872) was started before wrap-up and its output is not relied on here.

## 0. Moving-target caveat (read first)

`tools/mado-action-plan.py` changed several times during this review. Digests observed:

| time (-03:00) | sha256 | lines | state |
|---|---|---|---|
| 05:56:29 | `3c39a398…` | 856 | classifier/frozen/policy bodies as analysed below |
| ~05:56:50 | `9bce5710…` | 847 | **mid-edit: `ast.parse` → SyntaxError line 471** (`def _canonical_policy():` nested inside `_parse_verdict`'s `try`; orphan dict body after `_parse_finding`) |
| 05:57:08 | `cd284a37…` | 854 | `ast.parse` OK; `_canonical_policy` back at module level (anchor reads below) |

`.ufo/waves/round-16/safety-cases.json` also changed (05:55): sha `33180d11…`, 32 cases, 6 carry an embedded `policy` object. L1 must re-hash at integration. Findings below are against the bodies read; they are not a verdict on any future digest.

## 1. Axes named

- **S — staleness:** is a w1 absence/"does not exist" observation still true of integrated bytes?
- **A — adoption:** did the integrated gate/corpus adopt a w1 requirement?
- **X — exposure:** does the current integrated artifact keep a concrete counterexample, by reading?
- **F — claim fidelity:** do lane docs (SKILL row, SCORECARD C2, lesson, notes) state more than the bytes support?

## 2. Stale w1 absence observations (now false, S-axis)

| w1 claim (anchor) | Current integrated fact (verified by read/sha) |
|---|---|
| `tools/mado-action-plan.py` and `safety-policy.json` "do not exist" — ExecBasename.md:15-18,178; FrozenInputs.md:5; UnknownActions.md:9-12,211; PolicyTamper.md:26-30; ExitMap.md:7-8,212; FindingStability.md:212; CredentialFence.md:66; FrozenDesign.md:19 | Both exist. Gate `tools/mado-action-plan.py` (sha moving, see §0). `.ufo/waves/round-16/safety-policy.json` sha `fb134d8f…`, byte-equal to `.ufo/waves/round-16/frozen/policy.json`. |
| `frozen/` snapshot absent (SKILL/registry expectation) | Exists: `frozen/expected.json` (sha `e76090a3…`), `plan.json` (`82bc7652…`, matches its pin), `policy.json` (`fb134d8f…`). |
| "U7 absent" — ExistingU7.md; MeasureBuild.md:70-72; MetricInflation.md:4 | Note exists: `corpus/knowledge/waybar-observation-boundaries-r16.md` line 4 `covers: U7`, with the four level-2 headings and `[UNK]`. |
| "README has no U7 row" — MetricInflation.md:142-146 | Row present: `corpus/README.md:41`, real filename. |
| "S053/S054 absent" — FrontierDraft.md:24-25; ClaimsSeparable.md:25 | Present: `corpus/SOURCES.md:65-66`, mined, tier A, used-by the U7 note. S055 at `:67` (own-work, used-by `corpus/lessons/round-16.md`). Digests match `evidence/source-bindings.json` (`efb6a63a…`, `2232f7f7…`). |
| "lessons/round-16.md missing" / "no M1/M2 rows" | Present, rows M1–M5 at lines 13–18. |
| "`waybar-draft.txt` absent" — CoverageSimplify.md:9 | Exists at `.ufo/waves/round-16/waybar-draft.txt` (7800 B). Not the integrated note; superseded. |
| "36 selftest cases (31 evaluate + 5 frozen)" — SafetyGate.md:105-108 | Stale. Reader count of the 856-line body: 43 evaluate + 5 frozen = 48. Not executed. |
| "PT-10: 20 cases, zero carry `policy`" — PolicyTamper.md:179-190 | Stale. `safety-cases.json` (05:55): 32 cases, 6 embed `policy` (parsed objects, not raw bytes). |
| "tools/ holds only mado-verify.sh" — FrozenDesign, GateRegistry, others | Stale, superseded by the gate file. |

Stale but still correct at baseline (no defect): ClosureDebt.md:75-78 "Gate absent at baseline".

## 3. Adopted w1 findings (A-axis) — accepted, verified in current bodies

- **PT-1** `paused` strict bool: `_validate_policy`, `type(paused) is bool and paused is True` (~line 246).
- **PT-2 / M1** duplicate keys, NaN/Infinity, strict UTF-8: `_strict_pairs`, `_reject_constant`, `_parse_json_bytes` (~188–212). Applied to policy, plan and `expected.json` (`_load_json`).
- **PT-3 / PT-6 / PT-8 / PT-9** policy is code-pinned: kinds, deny set and paused scope must equal `PINNED_*` (~113–120, ~236–293). No unpaused branch. No env override. Exact string compare.
- **PT-4 / H5** uncaught exceptions: `main()` wraps all modes and emits exit 2 (`except Exception`, ~842); loaders catch `Exception`.
- **PT-5** ordering: `_evaluate_raw` validates policy before plan and classifies only after both validate (~366–385).
- **FrozenInputs R-3** `_read_regular`: `O_NOFOLLOW | O_NONBLOCK | O_NOCTTY`, `fstat` + `S_ISREG`, 16 MiB bound, growth check (~150–185). Symlink plan now rejected (selftest `plan-is-symlink`); FIFO (`plan-is-fifo`).
- **FrozenInputs R-4 / R-8 / TOCTOU** (first-draft defect closed): `run_frozen` reads each file once into `inputs[label]` and classifies those exact bytes via `_evaluate_raw` (~440–455).
- **FrozenInputs R-6 (partial):** unknown keys rejected, field types checked, `expected.json` loaded with the strict loader (duplicate keys rejected).
- **H2** kind exact match; unknown kind → exit 1 `unknown_action_kind` (`_classify`, ~331–343). Non-string kind → plan_malformed (exit 2).
- **H4** closed key sets for plan and action; missing `actions` → exit 2.
- **M2** kind set is code; policy cannot add or remove kinds.
- **Selftest additions:** `policy-paused-one`, `policy-paused-null`, `blocked-kind-empty-argv`, `unknown-kind-empty-argv`, `denied-before-blocked-order`, `plan-is-symlink`, `plan-is-fifo`, `malformed-later-beats-denied`; selftest copies its own bytes to a private tmp and invokes that copy (`SELFTEST_SCRIPT_SHA256`, ~693).

## 4. Rejected or still-open w1 findings (A/X-axis)

Each is a bounded counterexample by reading. Nothing was executed.

**R1 — frozen expectation is self-pinned (HIGH for claim fidelity; PT-7, FrozenInputs R-1/R-2/R-5/T13/T14, FrozenDesign A3, SafetySimplify F6).**
`run_frozen` takes digests from the same `expected.json` it then trusts. There is no `--frozen-pin`.
- Coordinated re-pin: rewrite `plan.json` to a safe plan, set `plan_sha256`, and set `expected_finding=plan_safe, expected_exit=0` → `frozen_match`, exit 0.
- Expectation-only edit (T13): `expected_exit` changed → `frozen_verdict_mismatch`, exit 1. The FrozenInputs requirement was exit 2. The selftest `frozen-verdict-mismatch` pins exit 1, so the test asserts the disputed behaviour.
- Consequence: SCORECARD round-16 C2 says "digest-bound frozen run"; the SKILL row says the expectation is pinned. Neither is outside-bound. The frozen run detects only inconsistent edits.

**R2 — `argv[0]` NUL/control characters pass (medium-low; H3/U10).**
`_basename` (~323–328) strips whitespace and splits on `/` only. `["sudo\u0000","x"]` under `read-source` → `exe="sudo\x00"` ∉ deny set → `plan_safe`, exit 0. [INFERENCE] a C-string consumer truncates at NUL and resolves `sudo`. Control characters in other positions are not refused either.

**R3 — denylist residuals (declared; accepted as disclosed limits, but see F-items).**
Under `read-source` these pass as `plan_safe`:
- `["omarchy-pkg-add","libinput"]` — pinned as expected `plan_safe` in `safety-cases.json` (`residual_control_omarchy_pkg_add_unscreened`) and selftest `omarchy-prefix-safe`. This is the R15 install shape through a helper (SafetyCompositor SC-1, `omarchy-pkg-add:9`). The green expectation enshrines it.
- `["libinput-debug-events","--device","/dev/input/event5"]` (input-capture by label only).
- `["nice","pacman","-Qi"]`, `["doas","pacman",…]`, `["zsh","-c",…]`, `["python3","-c",…]` (selftest `unlisted-argv0-safe` pins 0).
- `["cat","/dev/input/event3"]`.
SKILL.md ~533–539 and the lesson disclose unlisted names pass. Accepted as declared; the `plan_safe` label on the R15-shaped case overstates.

**R4 — `repo-write` accepts any argv (medium; SafetySimplify F5, SS3).**
`["rm","-rf","/"]` as `repo-write` → `plan_safe` (`rm` not denied; no path or verb screen). `grep` for `repo-write` in SKILL.md, LOG.md, `corpus/lessons/round-16.md` and `corpus/QUALITY.md` returned no hits: the kind's unscoped nature is undisclosed in lane docs. Kind retained by L1; not adopted.

**R5 — `actions: []` → `plan_safe` (decision; UnknownActions U21/H4).**
Selftest `empty-actions` pins 0. Docstring says "actions may be empty (safe plan)". Accepted as an explicit decision, but a vacuous pass.

**R6 — selftest failure exit 1 collides with "denied" (ExitMap H2; SafetyControlRed).**
`run_selftest` returns 1 on failure (`return 0 if not failed else 1`). SKILL registry row for `mado-action-plan` says selftest 1 = failed. The mado-verify convention in the same registry uses 2 for selftest failure. The mid-edit SyntaxError (§0) also exits 1 under `python3`, which is indistinguishable from a denied plan. Open.

**R7 — `expected_sha` uppercase accepted (low; FrozenInputs R-6/T16).** `digest.lower() != pin.lower()` accepts uppercase pins.

**R8 — frozen `plan_safe` token in stdout (low; FrozenDesign §4).** `frozen_match` detail echoes the expected finding, so `plan_safe` appears on stdout in a replay-match. SKILL row documents exit 0 as "replay matched". Accepted with the documented wording.

**R9 — `--frozen DIR` entries not enumerated (low; FrozenInputs R-2/T11).** Extra files such as `plan.json.bak` are ignored, not refused.

**R10 — `SafetyCases` "independent" expectations not executed (medium; PT-10; SKILL row 529).**
`safety-cases.json` (32 cases, 6 with parsed `policy` objects) has no runner. The gate references it only in a docstring comment (~line 41). Raw-bytes policy rows (duplicate key, NaN) cannot be expressed in it. The SKILL row lists it as a pinned value of the gate row, which overstates what `--selftest` covers.

**R11 — selftest coverage gaps on the policy side (low-medium; PT-10, P6/P8/P11/P12, F1).**
No policy-side duplicate-key, NaN, invalid-UTF-8, directory, FIFO or symlink rows. No frozen policy-tamper row (F1). No coordinated re-pin row (R1). Code paths are present by reading; the tests do not exercise them.

## 5. Integrated-only defects (not in any w1 report)

- **N1 — mid-edit parse break (HIGH while it lasted).** Snapshot `9bce5710…` (847 L): `ast.parse` SyntaxError at line 471 `def _canonical_policy():` inside `_parse_verdict`'s `try`; orphan dict body after `_parse_finding`. Snapshot `cd284a37…` (854 L) parses. Current state: resolved for parsing; not re-executed. Re-check at integration.
- **N2 — stale docstring reference (low).** Gate docstring line 22 says "pins … (PINNED_POLICY)". No such name; actual constants are `PINNED_PAUSED_SCOPE`, `PINNED_DENY_EXECUTABLES`, `PINNED_KINDS` (~103–120).
- **N3 — dead code (low, cleanup rule).** `_sha256` (~223–227) has no call sites.
- **N4 — receipt claimed, absent (medium; F).** SKILL.md:530 says "receipt separately binds executable and expectation digests to measured commit". No receipt file exists under `.ufo/waves/round-16/` (only `frozen/{expected,plan,policy}.json`, `evidence/{source-bindings.json,census-before.txt}`). Gate sha is not recorded anywhere in the lane. Per parent note, L1 receipts are intentionally after commits: this is a claim ahead of its artifact, not an absence defect.
- **N5 — lesson promises receipts (low-medium; F).** `corpus/lessons/round-16.md:14` says "Exact receipts below." The file is 94 lines; the sections are the M-table, Gate, and Boundaries/handoff. No receipts section. Same post-commit caveat as N4.
- **N6 — untracked artifacts (low; cleanup).** `tools/__pycache__/mado-action-plan.cpython-314.pyc` (05:46:56, untracked, not in `.gitignore`); origin is an import/compile, not confirmed. `.ufo/waves/round-16/fixtures/tight-{green,red}.json` (05:52): no reference found from the gate; not searched further under wrap-up. Remove or gitignore before commit.

## 6. Summary

- Stale absence observations (S): 10 rows in §2 are now false. The only stale-correct item is ClosureDebt's baseline statement.
- Adopted (A): 11 items in §3 are verified in current bodies.
- Rejected/open (X/F): R1–R11 in §4 and N1–N6 in §5. The most material unresolved items are R1 (self-pinned frozen expectations, contradicting the C2 "digest-bound" wording), R3 (declared denylist residuals with the R15 helper pinned green), R4 (unscoped `repo-write`), R10 (unexecuted safety-cases), and N4/N5 (claimed receipts not yet present).

## 7. Bounded unresolveds for L1

1. Re-hash `tools/mado-action-plan.py` and `safety-cases.json` at integration; the bodies moved during this review (§0).
2. Decide R1: add `--frozen-pin` out of band, or reword C2/SKILL to "consistency-checked frozen replay, not outside-bound".
3. Decide whether R3's `omarchy-pkg-add` case should be pinned `plan_safe` or relabelled as a known bypass.
4. Decide R4: scope or remove `repo-write`; disclose in SKILL if kept.
5. Run the selftest once after integration (not by this seat) to confirm the 48-case count and the frozen T13 assertion.

## Tooling

No installs, updates or package operations. No files written other than this report. No peers messaged. Background job bg_2872 (grep/python, read-only) was not polled.
