# RecutRerun — attack on `frozen-tampered-recut.json` (round 17, wave 2)

Target: `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` (git blob
`2e44f2075e6f89c3…`, committed `fc6f960`, worktree byte-identical) and
`tools/mado-action-plan.py --frozen` (`sha256 226220ae…` at `0175f13`,
`fc6f960`, `988b858` and the worktree — all four equal).

**Attack result: every measured value in the receipt reproduced byte for byte;
the attack failed to falsify any number, exit code, digest or label. It did
falsify one causal sentence (P2) and three wording/derivation details (P3).**
No C1/C2/C3 claim loses support from this artifact.

## 1. Reproduction

All work under `/tmp`; lane files were only read.

```
$ T=$(mktemp -d /tmp/mado-r17-retamper-XXXXXX)
$ C=$(mktemp -d /tmp/mado-r17-recontrol-XXXXXX)
$ cp -p .ufo/waves/round-16/frozen/*.json "$T"/; cp -p … "$C"/
$ python3 -c 'b=open("…/plan.json","rb").read(); open(…,"wb").write(b.replace(b"libinput",b"libinpuv",1))'
$ python3 -I tools/mado-action-plan.py --frozen "$T"     # exit 2
MADO_PLAN: snapshot_tampered
{"…","detail": "plan.json sha256 052c03b2… != pinned 82bc7652…","exit": 2,
 "finding": "snapshot_tampered","schema": "mado-action-plan-verdict-v1"}
$ python3 -I tools/mado-action-plan.py --frozen "$C"     # exit 0
MADO_PLAN: frozen_match
{"…","detail": "frozen verdict denied_executable:sudo/1 matched","exit": 0,
 "finding": "frozen_match","schema": "mado-action-plan-verdict-v1"}
```

Comparisons against the receipt's stored strings: for both runs `exit`,
`stdout` and `stderr` are byte-equal (including the trailing newline); the
receipt's `matched: true` on both runs is correct.

| Receipt claim | Measurement |
|---|---|
| `measured_commit 0175f13…` | gate blob at `0175f13` = `226220ae…`; frozen trio at `0175f13` = `e76090a3…` / `82bc7652…` / `fb134d8f…` — exactly `pristine_digests`. Timeline: dirs born `11:01:24.221 -0300`, tampered `plan.json` written `11:01:42.089`; previous commit `0175f13` `10:56:28`, next commit `f52f43f` `11:11:09`, receipt commit `fc6f960` `11:12:41`. The run's HEAD was necessarily `0175f13` — not merely consistent, uniquely pinned. |
| `action_gate_sha256 226220ae…` | `sha256sum tools/mado-action-plan.py` = `226220ae41436506…`; `git show 0175f13:… \| sha256sum` identical. |
| pristine digests | lane files and both `/tmp` controls: `e76090a3…`, `82bc7652…`, `fb134d8f…`; unchanged since the snapshot's only commit, `9dcf248`. |
| tamper = one byte, `'t' 0x74 -> 'v' 0x76`, no length change | binary diff pristine↔tampered: exactly **1** differing byte, 0-based offset **175**, `0x74→0x76`; both 224 bytes. Only occurrence 1 of 2 of `libinput` was edited. |
| `post_tamper_plan_sha256 052c03b2…` | `sha256sum` of the tampered copy = `052c03b2beed7a3e…`; it is also the digest the gate printed. |
| tampered: exit 2 `snapshot_tampered` | reproduced, exit 2, exact detail string. |
| control: exit 0 `frozen_match` | reproduced, exit 0, exact detail string. |
| round-16 receipt recorded `frozen_error` at `9dcf248` | `.ufo/waves/round-16/evidence/frozen-tampered.json`: `measured_commit 9dcf248`, gate `13d86fb0…` (= blob at `9dcf248`), exit 2, `frozen_error`, `"expected.json pair 1/'denied_executable:sudo' is unreachable"`, `matched_exit: true` (exit-only; no finding field). Its control, `action-frozen.json`, is exit 2 `frozen_error` with `matched_exit: false`. |

## 2. Findings

### P2-1 (medium) — the purpose sentence misattributes the round-16 `frozen_error` to a "stale expected.json pair"; the pair was correct, the gate predicate was buggy

Anchor: `frozen-tampered-recut.json:3` — "…recorded `frozen_error` because the
stale expected.json pair was unreachable at that commit."

Three independent counter-observations:

1. `expected.json` at `9dcf248` is byte-identical to today's (`e76090a3…`) and
   its pins are the pristine digests. Nothing was stale; the fixture was never
   edited (snapshot has no commit after `9dcf248`).
2. The `9dcf248` gate's own **evaluate** mode on those pristine bytes returns
   `denied_executable:sudo` / 1 — the pair was semantically reachable at that
   commit:
   `python3 -I /tmp/mado-r17-oldgate.py --plan … --policy …` → exit 1,
   `denied_executable:sudo`.
3. Why frozen mode nevertheless rejected it (blob `13d86fb0`, lines 447-456):
   the table held `"blocked_action_kind:"`, `"denied_executable:"` (trailing
   colons) and the predicate was `want_finding.startswith(a + ":")`. The probe
   therefore becomes `"denied_executable::"` / `"blocked_action_kind::"` and no
   parameterized finding can ever match; reproduced `False` for both. This is
   corroborated by the red selftest at `9dcf248`: 51/52 with
   `failed=['frozen-denied-match']`, while `frozen-tampered-plan/policy` pass
   `2/snapshot_tampered`. `1e31681` replaced the prefix table with exact
   `(exit, finding)` pairs.

The round-17 erratum in the same corpus states the correct mechanism — "the M6
pair defect fired before any digest check" (`corpus/lessons/round-16.md:167`).
The receipt's "stale … pair" contradicts the erratum it exists to support, and
"stale" invites the wrong repair: editing the fixture instead of the gate —
the hazard round-16 explicitly disclaimed ("No fixture expectation was
weakened", `corpus/lessons/round-16.md:132-133`). Suggested replacement:
"…because the 9dcf248 gate's prefix table rejected every parameterized finding
(`startswith(a + ':')` against entries that already ended in `:`); the pair
itself was correct and unchanged."

### P3-1 (low) — "the digest pin alone detects it" is unconditioned

Anchor: `frozen-tampered-recut.json:16`. Counterexample A: tamper `plan.json`
**and** rewrite `expected.json`'s `plan_sha256` to `052c03b2…` → exit **0**
`frozen_match` on tampered inputs (`/tmp/mado-r17-anchor-*`). The corpus itself
discloses the boundary at `corpus/lessons/round-16.md:142` ("Frozen pins alone
do not authenticate coordinated edits"), so the note is true only given an
unmodified `expected.json`. Fix: condition the sentence ("the pin is the only
in-gate detector, absent a coordinated rewrite of `expected.json`").

### P3-2 (low) — tamper is under-specified by one byte of identity

Anchors: `frozen-tampered-recut.json:13-16`. `libinput` occurs twice in
`plan.json` (offset 168 = `argv[4]`, offset 188 = inside `libinput-tools`).
A naive replace of both yields `7aa5bbbf26ac776f…`, **not** the claimed
`052c03b2…`; only first-occurrence replacement reproduces the receipt. The
post-digest disambiguates, so this is derivable rather than contradictory, but
recording `byte_offset: 175` (0-based `0x74→0x76`) would make the derivation a
single step instead of a digest search.

### P3-3 (low) — "superseding round-16 evidence/…" overstates what was superseded

Anchor: `frozen-tampered-recut.json:3`. The erratum supersedes the *sentence*
at `round-16.md:131-132`, re-receipts the control, and labels itself
"Status-neutral" (`corpus/lessons/round-16.md:161-176`). The `9dcf248` receipt
is retained and still passes as an honest label:
`.ufo/waves/round-17/label-claims.json:26-31` (`honest-red-green`) →
`LABEL honest-red-green ok`. The recut supersedes the claim's evidence pointer,
not the old receipt's truth. Wording only.

## 3. Boundary probes (all consistent with the tool's taxonomy, `mado-action-plan.py:53-56`)

| Probe | Result |
|---|---|
| tampered plan + consistently rewritten pin (A) | 0 `frozen_match` — pin has no external anchor (see P3-1) |
| `plan.json` as symlink | 2 `snapshot_tampered`, "unreadable: Too many levels of symbolic links" (`_read_regular`, `O_NOFOLLOW`, `mado-action-plan.py:150-160`) |
| one-byte `policy.json` edit (`pacman`→`pacmar`) | 2 `snapshot_tampered`, detail names the policy digest |
| truncated/invalid-JSON plan (digest also differs) | 2 `snapshot_tampered` — digest check precedes evaluation; not `plan_malformed` |
| reachable-but-wrong pair (`plan_safe`/0 on pristine inputs) | 1 `frozen_verdict_mismatch` |

Ordering matters for the claim, and it holds: the digest loop
(`mado-action-plan.py:459-471`) verifies both files before `_evaluate_raw`, and
the same bytes are classified (single read, `:473`).

The receipt is also strictly stronger than the tool's own tamper selftest:
`frozen-tampered-plan` appends `b"\n#tampered\n"` (`mado-action-plan.py:778`),
which additionally breaks JSON, so that fixture cannot distinguish "the pin
caught a verdict-preserving edit" from "the plan became malformed". The recut's
tamper **is** verdict-preserving — evaluate mode on the tampered bytes returns
the identical `denied_executable:sudo` / 1 — so without the pin the replay
would have returned `frozen_match`. This is the receipt's strongest property
and it is real.

## 4. Residual risk

- **In-snapshot anchor.** `expected.json` sits beside the inputs; a coordinated
  rewrite masks any tamper (demonstrated). Already disclosed at
  `corpus/lessons/round-16.md:142`; the receipt's note (P3-1) should not be read
  as authentication.
- **Volatile `/tmp` artifacts.** Both claimed tmpdirs still existed at attack
  time and matched (`…-tamper-PDanoS` = `052c…`, `…-control-kGThY6` = `82bc…`,
  with `expected`/`policy` mtimes preserved from the lane checkout,
  `05:51:09.948`, consistent with `cp -p`). I nevertheless reconstructed both
  runs from the prose alone, so durability does not depend on `/tmp`.
- **Label-checker granularity** (C1's artifact; observation only).
  `outcome_tokens` recurses over every run's `stdout`
  (`label-check.py:75-90`), so `recut-green`
  (`.ufo/waves/round-17/label-claims.json:32-36`) passes on the tampered run's
  token — correct — but the same receipt would equally satisfy token
  `frozen_match` from the control run. The checker cannot express "the tampered
  run returned X and the control returned Y". Not a defect of the receipt.
- **Exit-code collapse.** `snapshot_tampered` and `frozen_error` are both exit
  2; the receipt is discriminating only because it records `expected_finding`.
  Round-16's `matched_exit`-only shape is exactly what allowed R16-V1; the
  recut closes that for this artifact.

## 5. Verification gaps

- I did not execute `tools/mado-action-plan.py --selftest` (outside my read-only
  allowance). I read the committed `9dcf248`/`1e31681` selftest receipts and
  extracted the historical gate blob to `/tmp` for behavioral comparison
  instead.
- I did not re-measure C1, C2 or C3; sibling lanes own them. The label check was
  run once to test the `recut-green` binding only.
- No web sources were needed; every anchor is lane-local or a git object.

## 6. Install / mutation record

Installs: **none** (no pacman/sudo/uv/npx/pip/curl). No compositor, service,
input or host probes. Lane writes: this report only. All other writes are
copies under `/tmp`, including the historical gate blob `13d86fb0…`.
