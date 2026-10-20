author: MadoR17.RevR16V1Facts (mado round-17 reviewer, L2 facts seat)
date: 2026-10-20
scope: verify R16-V1 from the artifacts themselves; audit every `evidence/`
citation in `corpus/lessons/round-16.md` against its receipt's actual finding.
method: git show/diff/log, file bytes, JSON parse with python3 stdlib. No gate,
selftest, fixture, sibling script or host operation was executed.

# R16-V1 — verified, with two premise corrections

## Bottom line

1. **R16-V1 is real for the lesson.** `corpus/lessons/round-16.md:131-132`
   attributes `snapshot_tampered` to `evidence/frozen-tampered.json`; that
   receipt records exit 2 **`frozen_error`**, not `snapshot_tampered`.
2. **The report does not name the receipt.** No line of
   `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mado.md` contains the
   string `frozen-tampered`; line 64 only asserts the token. The assignment's
   and the round-16 spot-check's phrasing ("report … cite
   `evidence/frozen-tampered.json`") is therefore imprecise: only the lesson
   names the file.
3. **No other round-16 lesson sentence mislabels a receipt's finding.** All 14
   other citation rows reproduce the receipt's code and/or token. Two
   citation-attachment gaps exist (census counts; the 96-report census) but
   neither is a finding mislabel.
4. **The disputed receipt is a pre-fix red artifact, not a green control.**
   The claimed `snapshot_tampered` is true only of (a) the round-16 *selftest*
   fixtures, which passed at **both** `9dcf248` and `1e31681`, and (b)
   statically, the corrected standalone path. A round-17 sibling recut at
   `0175f13` records (2, `snapshot_tampered`), but I neither authored nor
   executed it.

## 1. Artifact identity (verified)

Lane HEAD is `0175f13`; the round-17 pre-registration commit. Baseline named
by the assignment is `27cd06f`.

| Artifact | Identity | Verified |
|---|---|---|
| `corpus/lessons/round-16.md` | sha256 `6d47d6f3aefa2e259551f873a93b3bb0fd48a01e53fb5f895380be9c4d71eca5` | identical at `27cd06f` and HEAD; `git diff --stat 27cd06f -- <file>` empty; worktree clean (`git status --porcelain` empty) |
| `.ufo/waves/round-16/evidence/frozen-tampered.json` | sha256 `34a801bd1fad32521882eac5f8906cc56b83fc70c0ebe01cda578d01be9722fa` | equals the committed blob at `1e31681`; `git cat-file -e 9dcf248:<path>` → fatal (absent at the red commit) |
| fleet `.ufo/reports/round-16/mado.md` | sha256 `a8019dd971256fdcaae069f46e5475d46a99202ae1cf3a8a41da4de37d2efb62` | single history entry `cd4c0ea round-16: mado report` |

The lesson sentence and the receipt are both stable; nothing below depends on
a moving worktree.

## 2. Exact quotes

**Lesson, `corpus/lessons/round-16.md:129-132`, at `27cd06f` (unchanged at
HEAD):**

> at corrected content; `action-selftest-final.json`, `action-frozen-final.json`.
> Frozen match compares an expected refused plan, never authorizes it.
> Input tamper control returns **2 snapshot_tampered**, retained in
> `frozen-tampered.json`. No fixture expectation was weakened.

**Report, `.ufo/reports/round-16/mado.md:64` (complete line):**

> - Initial failed selftest51/52 and frozen_error exit2 remain in original receipts. Only failed behavior and final revision observation were rerun after the direct fix. Tampered frozen input returns2 `snapshot_tampered`; original receipt retained. In-directory pins do not authenticate coordinated rewrites; the committed external binding is the authority.

`grep -n "frozen-tampered" .ufo/reports/round-16/mado.md` returns nothing.
`grep -n "tamper\|Tamper"` returns only line 64, i.e. the token assertion
without a receipt path.

**Receipt, all decisive fields verbatim:**

```json
{
  "label": "frozen-tampered",
  "measured_commit": "9dcf248993a9622a5b016edec0003187141745d2",
  "action_gate_sha256": "13d86fb0b34c21bccde0a8314875d66deb287624a9d971e4f4ed287496dcdb73",
  "command": ["python3", "-I", ".../tools/mado-action-plan.py", "--frozen",
              "/tmp/mado-r16-frozen-tamper-pt60l_e_"],
  "exit": 2,
  "stdout": "MADO_PLAN: frozen_error\n{\"action_index\": null, \"action_kind\": null, \"detail\": \"expected.json pair 1/'denied_executable:sudo' is unreachable\", \"exit\": 2, \"finding\": \"frozen_error\", \"schema\": \"mado-action-plan-verdict-v1\"}\n",
  "stderr": "",
  "expected_exit": 2,
  "matched_exit": true
}
```

`grep -c snapshot .ufo/waves/round-16/evidence/frozen-tampered.json` → `0`;
`grep -c frozen_error` → `1`. The token the lesson attributes to the receipt
occurs nowhere in it.

## 3. Why the receipt says `frozen_error` (mechanism, from code)

The gate's frozen path validates the expected pair **before** any digest check:
at `tools/mado-action-plan.py` (corrected content, sha `226220ae…ba5aea3`) the
pair-reachability block is lines 446-459; the plan/policy digest pins are
lines 460-470. At `9dcf248` (gate sha `13d86fb0…dcdb73`) that block was:

```python
    valid_pairs = {
        0: ("plan_safe",),
        1: ("blocked_action_kind:", "denied_executable:",
            "unknown_action_kind", "empty_argv"),
        2: ("plan_malformed", "policy_malformed"),
    }
    allowed = valid_pairs.get(want_exit)
    ok_pair = allowed is not None and any(
        want_finding == a or want_finding.startswith(a + ":")
        for a in allowed)
```

For `want_finding = "denied_executable:sudo"`, `a + ":"` is
`"denied_executable::"`, so neither equality nor `startswith` holds; the pair
is declared unreachable and the run returns `frozen_error` **before** the
digest comparison that would have produced `snapshot_tampered`. The `1e31681`
fix replaces the prefix test with exact `(exit, finding)` pairs generated from
`PINNED_PAUSED_SCOPE` and `PINNED_DENY_EXECUTABLES`; `sudo` is in the latter
(lines 109-112), so the committed pair is reachable there.

Consequence: `frozen-tampered.json` is a **red receipt of the M6 defect on the
tamper path**, not evidence that the tamper control passed. The lesson moves a
corrected-content truth into a pre-fix receipt — a time-shift, not merely a
filename typo.

## 4. Provenance: the sentence was written after the receipt existed

This forecloses "stale prediction":

| Commit | Lesson length | Tamper sentence | Receipt present |
|---|---|---|---|
| `9dcf248` source/classifier baseline | 94 lines | absent | absent |
| `1e31681` pair fix | 95 lines (adds M6 row only) | absent | **present** (added here, measured at `9dcf248`) |
| `4bfb236` final records | 159 lines | **added at 131-132** | present |

`frozen-tampered.json` was committed at `1e31681`; the sentence asserting it
shows `snapshot_tampered` was committed one commit later, at `4bfb236`. At
authoring time the contradicting receipt was already in the tree and its
`stdout` already read `frozen_error`. The reporting lane could have read it.

## 5. The receipt schema is exit-only — the mislabel's likely mechanism

All 15 generic round-16 receipts share the field set:
`action_gate_sha256, command, exit, expected_exit, label, matched_exit,
measured_commit, stderr, stdout`. There is **no `expected_finding` field**.
`frozen-tampered.json` therefore reports `"matched_exit": true` because
`exit == expected_exit == 2`, while the finding is `frozen_error`.

Only `independent-cases.json` pins both code and finding (`total/passed/
results[].expected_finding`), which is why the lesson's 32/32 claim is
checkable at token level. A label check that keys on `matched_exit` or on the
exit code alone **cannot** detect this defect: both the claimed and the actual
outcome are exit 2. Any round-17 label criterion must read the `finding`
field / `MADO_PLAN:` first line.

## 6. Full audit of the round-16 lesson's receipt citations

Every citation, with the claim and the receipt's actual content. "OK" means
the receipt carries the claimed code and token; "GAP" means the cited receipt
does not carry part of the sentence (claim still true elsewhere).

| Lesson line | Citation | Sentence claim | Receipt truth | Verdict |
|---|---|---|---|---|
| 19 | `evidence/action-selftest.json`, `action-frozen.json` | selftest 51/52; `frozen_error` for valid `denied_executable:sudo` | 51 PASS / 1 FAIL (`frozen-denied-match` want 0 `frozen_match` got 2 `frozen_error`), exit 1; frozen exit 2 `frozen_error`, detail "pair 1/'denied_executable:sudo' is unreachable" | OK |
| 55 | `evidence/source-bindings.json` | S053/S054 raw digest binding | JSON list carries S053/S054 url, accessed 2026-10-20, bytes, sha256 (`efb6a63a…`, `2232f7f7…`) | OK (upstream not refetched here) |
| 105-106 | `evidence/before.json`, `evidence/after-final.json` | C1 `6/7→7/7`, `8.5714→10.0000`; navigation `29/29→30/30`; exact commands/exits/revisions | before: coverage count 6, score 8.5714, nav 29/29, exit 0; after-final: count 7, score 10.0, nav 30/30, exit 0; revisions `32c4fda…`/`1e31681…` | OK |
| 110 | `evidence/calibration-readings.json` | literal `12/20→14/22` (6.0000→6.3636); block `15/20→17/22` (7.5000→7.7273) | exact: `{20,12,15,6.0,7.5}` then `{22,14,17,6.3636…,7.7272…}`, exit 0 | OK |
| 116 | `evidence/selection-red.json`, `selection-green.json` | audit exits 1 then 0, scores fixed, lowest calibration | red exit 1 `lowest=calibration, obligation_met=false`; green exit 0 `declared_axes` gains calibration only; both `scores {calibration 6.0, coverage 8.5714, freshness 10, operability 10}` | OK |
| 119 | `evidence/tight-{red,green}.json` | 1 `denied_executable:sudo` → 0 `plan_safe` | red exit 1 `denied_executable:sudo` (detail: executable 'sudo' denied); green exit 0 `plan_safe` | OK |
| 123-125 | `evidence/independent-cases.json` | 32/32 exact code+finding at initial content; template, generation/replacement policy, every input digest | `total 32`, `passed 32`, `measured_commit 9dcf248…`, `command_template`, `generation`, per-case `expected_finding` + `plan_sha256`/`policy_sha256` | OK |
| 126-127 | `action-selftest.json`, `action-frozen.json` | 51/52 and 2 `frozen_error` red evidence retained | as row 19; both exits 1 / 2, red | OK |
| 129 | `action-selftest-final.json`, `action-frozen-final.json` | 52/52 exit 0; `frozen_match` exit 0 at corrected content | selftest exit 0 `SELFTEST_SUMMARY: 52/52 passed`; frozen exit 0 `frozen_match`, detail "denied_executable:sudo/1 matched" | OK |
| 131-132 | `frozen-tampered.json` | tamper control returns 2 `snapshot_tampered` | exit 2, **`frozen_error`**, detail "expected.json pair 1/'denied_executable:sudo' is unreachable", measured `9dcf248` | **MISLABEL (R16-V1)** |
| 133-136 | `legacy-selftest.json` | 372/372 exit 0; gate sha `fba82a66…f5c207` | `MADO_SELFTEST: 372/372 assertions passed`, exit 0; sha matches committed-bindings and both measure receipts | OK |
| 137-139 | `census-before.txt`, `census-after.json` | census exit 0, W04 S030/S042/S045 retained; sources 52→55, tiers 48/1/3→51/1/3, statuses 40/8/4→43/8/4 | both carry exit 0 + the three W04 lines + `mado ok`; **neither carries row/tier/status counts**. The counts are in `before.json` (52/48/1/3/40/8/4) and `after-final.json` (55/51/1/3/43/8/4) | GAP (claim true in other receipts) |
| 140-142 | `committed-bindings.json` | binds final gate/policy/cases/frozen expectation + other inputs to corrected content; selftest prints same code SHA | all 12 inputs with sha/bytes/`worktree_equal: true`, incl. `tools/mado-action-plan.py 226220ae…`, `safety-policy.json fb134d8f…`, `safety-cases.json 33180d11…`, `frozen/expected.json e76090a3…`, `measure.py`, QUALITY/SOURCES/README/note; final selftest prints `SELFTEST_SCRIPT_SHA256: 226220ae…` | OK |
| 146-148 | `evidence/wrapup.json` | misroot sweep: no mado report names in fleet wave tree | `misroot_sweep.mado_seat_report_names_found: []`, sweep path and observed list; directive and 64/32 dispatch counts | OK (the "96 seat reports, no missing" clause is not in wrapup; it is in the uncited `evidence/wave-census.json`, which records 64/32 present, `missing_reports: []`, `round_total: 96`) |
| 149 | `falsification-adjudication.json` | records accepted fixes and bounded limits | wave-root JSON has `accepted_and_integrated`, `declared_residuals_not_claimed`, `rejected_requirements`, `scope_breaches_disclosed` | OK (path is wave root, not `evidence/`; resolves under the stated root) |

Only one finding-token mislabel exists: line 131-132. The census GAP is a
citation-attachment defect (numbers are correct, wrong receipt credited); it
may be worth an erratum but is not a false verdict token.

## 7. `snapshot_tampered` evidence inside round 16

Contrary to the round-16 spot-check's "`snapshot_tampered` is evidenced only by
the final self-test fixtures"
(`corpus/lessons/round-16-verifier-spotcheck.md:169-170`), the **initial**
selftest receipt also carries both tamper cases, green:

`action-selftest.json` (`9dcf248`, exit 1):
```
SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered
SELFTEST PASS frozen-tampered-policy: want 2/snapshot_tampered got 2/snapshot_tampered
```
`action-selftest-final.json` (`1e31681`, exit 0) carries the same two PASS
lines. The selftest's tamper control therefore did not discriminate the defect
— it was green at the red commit. Only the standalone `--frozen` path failed.
A round-17 criterion that cites "the tamper control passed" without naming
which path would inherit that non-discrimination.

Also note the spot-check's own sentence structure at
`round-16-verifier-spotcheck.md:164-166` — "report (…) and lesson round-16
l.131 cite `evidence/frozen-tampered.json`" — attaches the filename to the
report too. The report names no file (section 2). The defect is unaffected;
the *description of where it lives* needs the distinction.

## 8. Round-17 artifacts already present (read-only, sibling-authored)

`.ufo/waves/round-17/evidence/frozen-tampered-recut.json` records
`measured_commit 0175f13`, `action_gate_sha256 226220ae…`, a one-byte
`plan.json` tamper (`libinput`→`libinpuv`), and two runs: tampered exit 2
`snapshot_tampered` (detail `plan.json sha256 052c03b2… != pinned 82bc7652…`)
and untampered control exit 0 `frozen_match`.

Static preconditions I could confirm without running it: the committed frozen
pair is `(1, denied_executable:sudo)`; `sudo ∈ PINNED_DENY_EXECUTABLES`
(`tools/mado-action-plan.py:109-112`); the pair check precedes digest pins
(446-470); a differing plan digest then yields `snapshot_tampered`. The recut's
outcome is therefore consistent with the code — but it is another seat's
artifact, and I did **not** execute it, so it remains unverified until L1's
single integration run. It is strictly better than the R16 receipt: it
records the tamper mutation, the post-tamper digest, and the control run.

`.ufo/waves/round-17/label-claims.json` + `label-check.py` implement the C1
label check: claim `R16-V1-red` (doc `27cd06f`, lines 131-132, receipt
`1e31681`, token `snapshot_tampered`, expected MISMATCH) and claim
`frozen-match-green` (doc lines 128-129, `action-frozen-final.json` at
`4bfb236`, token `frozen_match`, expected ok). Static trace: red → doc window
contains basename+token, receipt's finding-like strings lack the token
(`grep -c snapshot` = 0) → MISMATCH; green → both present → ok. I did not run
the script (not mine).

Recommendations for that check before integration:
- Compare the parsed finding (the `MADO_PLAN:` first line or JSON `finding`),
  not substring-presence over `stdout`; today a token could satisfy the check
  by appearing in `detail` for a different reason.
- Never accept `expected_exit`/`matched_exit` as the label; they are exit-only
  (section 5).
- State explicitly whether the fleet report sentence is in scope. It cannot be
  a claim in the current design: `label-check.py` resolves docs/receipts
  through `git -C <lane root>`, and the report lives in the fleet repo. If the
  M1 lesson repeats "the report cites `evidence/frozen-tampered.json`", it
  repeats a false citation while correcting one.
- If the recut is cited by M1, L1 must verify it once and record that it is
  round-17 content at `0175f13`, not round-16 evidence.

## 9. Consequences for the pre-registered C1 (lesson round-17 M1)

Verified-sufficient for the claim as written in SCORECARD:836-838 ("receipt
cited for a verdict token it does not carry") — that is exactly true, and the
label check can fail on the round-16 lesson line. The M1 lesson should state:

1. Lesson `round-16.md:131-132` attributes `snapshot_tampered` to
   `frozen-tampered.json`; the receipt's actual pair is (2, `frozen_error`),
   detail "expected.json pair 1/'denied_executable:sudo' is unreachable",
   measured at `9dcf248`, committed at `1e31681`.
2. The sentence was authored at `4bfb236`, after the receipt existed.
3. The receipt's `matched_exit: true` is exit-only; the receipt schema has no
   finding pin.
4. The report asserts the token without naming any receipt (premise
   correction); only the lesson names the file.
5. `snapshot_tampered` in round 16 is carried by the selftest cases
   `frozen-tampered-plan`/`frozen-tampered-policy`, green at both `9dcf248`
   and `1e31681`; that control did not catch M6.
6. A corrected-content standalone re-receipt of the tamper path is the
   appropriate optional remedy; one now exists (sibling-authored at
   `0175f13`), pending L1 verification.

## 10. Residual risk and verification gaps

- I executed no gate/selftest/fixture/recut and no sibling script. Behavioral
  statements above come from receipt stdout or static code reading; the only
  [INFERENCE]-level items are (a) the label-check red/green outputs (static
  trace of the code against the artifacts) and (b) the corrected standalone
  path's `snapshot_tampered` (code order + reachable pair + digest mismatch).
- `/tmp/mado-r16-frozen-tamper-pt60l_e_` is gone, and the R16 receipt records
  no tamper description or post-tamper digest, so the exact round-16 mutation
  is unreconstructable. This is a second receipt-quality reason R16-V1 was
  hard to read.
- S053/S054 upstream identity was not re-fetched; their recorded digests match
  `source-bindings.json`, and `committed-bindings.json` binds the local corpus
  files, but "tag source ≠ installed binary" remains as the round states.
- Host versions/health remain `[UNK]`; irrelevant to this finding.
- No other round-16 lesson citation was found to mislabel a receipt. If a
  wider artifact set (LOG.md, wave reports) repeats the tamper sentence, it
  was outside this assignment's citation set; `grep` found no `snapshot_tampered`
  or `frozen-tampered` in `LOG.md`.

## 11. Tooling

None installed or updated. No sudo/pacman/yay/paru/systemctl/hyprctl/omarchy/
live-probe/screenshot/credential access; reads only (`cat`, `sed`, `grep`,
`sha256sum`, `git show/diff/log`, `python3` stdlib JSON parsing). No file
written except this report.
