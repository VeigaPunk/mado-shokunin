# LabelRerun — round 17 wave 2 (FALSIFY): receipt-label checker rerun

Lane HEAD reviewed: `988b858bd6049bc709807534fd725c05264f7e60`. Target root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Install: **none** (host pause honoured; no
pacman/sudo/systemctl/compositor/input probes, no omp processes).

## Verdict

`python3 -I .ufo/waves/round-17/label-check.py` at HEAD:

```
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248...' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 4/7
EXPECT_SUMMARY: 7/7 claims met their declared expectation
exit=1
```

`LABEL_SUMMARY: 4/7` is correct for this file: three claims are declared red controls. The
calibration contract (`corpus/QUALITY.md`, criterion 23, added at `3722ba4`) requires
`EXPECT_SUMMARY` 7/7; that is reproduced. The same command run from `/tmp` gives identical
output (the tool resolves `SCRIPT_DIR` and the git toplevel, so the documented invocation is
cwd-independent).

`EXPECT_SUMMARY` is computed, not printed as a constant: flipping claim
`spotcheck-selftest-final-green` to `expect: MISMATCH` yields `EXPECT_SUMMARY: 6/7`; a claim
with an unresolvable `rev` yields `COULD_NOT_EVALUATE` and `exit 2` (`label-check.py:176-191`).
The archived `.ufo/waves/round-17/evidence/label-check.txt` (added at `3722ba4`, not earlier —
`git log --all --` that path shows only `3722ba4`) matches a fresh run on its nine checker
lines; its last four lines are a hand-assembled footer (`exit=1`, `245fd114…`, sha256 of tool
and claims). Tool, claims, fixture and evidence are byte-identical from `3722ba4` to HEAD
(`git diff --stat 3722ba4 988b858 -- <those paths>` is empty).

## Per-claim expectation audit (doc bytes at `rev`, receipt bytes at `rev_receipt`)

| claim | doc anchor | receipt anchor | independent result | expectation |
|---|---|---|---|---|
| R16-V1-red | `round-16.md:131-132 @27cd06f` = "Input tamper control returns **2 snapshot_tampered**, retained in `frozen-tampered.json`" | `frozen-tampered.json @1e31681`, blob `34a801bd…` unchanged at `27cd06f`/HEAD; `measured_commit 9dcf248`, exit 2, `MADO_PLAN: frozen_error`, `"finding": "frozen_error"` | doc attributes `snapshot_tampered`; receipt's outcome is `frozen_error` | **MISMATCH justified** |
| frozen-match-green | `round-16.md:128-129 @27cd06f` = "**frozen_match**, exit0, at corrected content; … `action-frozen-final.json`" | `action-frozen-final.json @4bfb236` (introduced there), `measured_commit 1e31681`, `MADO_PLAN: frozen_match` + `"finding": "frozen_match"`, gate `226220ae…` | correct citation | **ok justified** |
| spotcheck-selftest-final-green | `round-16-verifier-spotcheck.md:71-73 @27cd06f` = `action-selftest-final.json` (measured `1e31681`) exit 0, `52/52`, including `frozen-tampered-plan` and `frozen-tampered-policy` `want 2/snapshot_tampered got 2/snapshot_tampered` | same receipt @`4bfb236`, `measured_commit 1e31681`, `SELFTEST_SUMMARY: 52/52 passed`, both rows `got 2/snapshot_tampered` | every element of the sentence matches (both rows, not just one) | **ok justified** |
| want-side-only-mutant | synthetic `doc_text` | `label-fixtures/want-only.json` (blob `14483913…` at `245fd11` and HEAD), stdout `SELFTEST FAIL frozen-tampered-plan: want 2/snapshot_tampered got 2/frozen_error`; no `MADO_` line, no `finding` key | token exists only on the want side; got side is `frozen_error` | **MISMATCH justified** |
| superseded-commit-mutant | synthetic `doc_text` naming `1e31681` as measured | `frozen-tampered.json @1e31681`, `measured_commit 9dcf248` | receipt's measured revision is not the named one | **MISMATCH justified** |
| honest-red-green | synthetic `doc_text` naming `9dcf248` | same receipt, `measured_commit 9dcf248` | honest label of the same receipt | **ok justified** |
| recut-green | synthetic `doc_text` | `frozen-tampered-recut.json @fc6f960`, blob `2e44f207…` unchanged at HEAD; tampered run exit 2 `MADO_PLAN: snapshot_tampered` + `"finding": "snapshot_tampered"`; control run `frozen_match` | genuine, reproducible tamper receipt (see below) | **ok justified, non-trivial** |

`recut-green` receipt was independently re-derived rather than trusted:

- `pristine_digests` recompute exactly: `expected.json e76090a3…`, `plan.json 82bc7652…`,
  `policy.json fb134d8f…` (actual `sha256sum` of `.ufo/waves/round-16/frozen/`).
- Declared tamper is a single argv element, not a global replace: quoted `"libinput"` at byte
  offset 167 → `"libinpuv"`; recomputed digest = `052c03b2…`, exactly the receipt's
  `post_tamper_plan_sha256`; length unchanged. (A global replace of both `libinput`
  occurrences gives `7aa5bbbf…`; the receipt's narrower wording is the correct one.)
- `action_gate_sha256 226220ae…` equals `sha256` of `tools/mado-action-plan.py` at both
  `0175f13` and HEAD.
- `measured_commit 0175f13` and the receipt's control run (`frozen_match`, exit 0) are
  consistent with the stated purpose.

Cross-check outside the seven: the `3722ba4` erratum says the red `action-selftest.json`
(measured `9dcf248`) already evidences `snapshot_tampered`; the receipt at `4bfb236` indeed
has both tamper rows `got 2/snapshot_tampered` (`51/52`, failed `frozen-denied-match`), so
that erratum sentence is true.

## Findings

### F1 (medium) — want-side exclusion is incomplete for JSON-form want side

`label-check.py:18-22` and `corpus/QUALITY.md` criterion 23 promise that want-side text never
counts. `outcome_tokens` (`label-check.py:75-89`) does exclude the selftest `want N/token`
form (only `got N/token` is regexed, line 84) and does not scan free prose, but it recurses
into every dict and counts **any** key literally named `finding` (lines 79-80). A receipt that
records its want side structurally is therefore scored as if that were the outcome:

```
{"expected": {"finding": "snapshot_tampered"},
 "actual":   {"finding": "frozen_error"}}
→ collected outcome tokens: ['frozen_error', 'snapshot_tampered']
→ a claim with expect=MISMATCH is scored "ok"
```

The same shape embedded in `stdout` is also counted, because `FINDING_JSON`
(`"finding":\s*"([a-z_]+)"`, applied at line 83 to `stdout`/`stderr`) does not care whether
the object is under an `expected`/`want` container. The supplied red control
(`want-only.json`) only exercises the selftest line form, so the tool's central L1 claim —
"a substring match passed a want-only mutant" is fixed — holds only for that one encoding.

Not exploitable by the seven current claims: `grep -c '"expected":'` is 0 for all five cited
receipts, and the recut receipt's `expected_finding` (underscore) does not match
`FINDING_JSON`. No current expectation is invalidated, but a future receipt that prints an
expected verdict object would be scored green on its want side.

### F2 (low) — `recut-green`'s document half is synthetic, though a real citation exists

`label-claims.json:32-36` uses `doc_text` for the only round-17 receipt claim. The append-only
erratum in the same commit really cites that receipt at
`corpus/lessons/round-16.md:172-175 @3722ba4` ("`.ufo/waves/round-17/evidence/frozen-tampered-recut.json`
(one-byte plan change, exit 2 `snapshot_tampered`; untampered control exit 0 `frozen_match`;
gate `226220ae…`)"). Substituting that real path/rev/line range into the claim keeps
`EXPECT_SUMMARY` at 7/7 (verified). So the green is not false, but the claim as written proves
nothing about the actual erratum sentence; the real citation is only covered by manual
reading. This is the one place where the claim's doc side is trivially satisfied by the
fixture author rather than by a document.

### F3 (low) — one claim pins a floating revision

`want-side-only-mutant` (`label-claims.json:17-21`) uses `rev_receipt: "HEAD"`. At HEAD
`988b858` it resolves to the intended blob (`14483913…`, identical to `245fd11`), and the
archived evidence footer pins `245fd11`, but the claims file itself does not. The claim's
meaning is therefore history-dependent: a later fixture edit could flip the expected
`MISMATCH`, and evaluation before `245fd11` would be `UNEVAL`/exit 2. Every other receipt is
pinned to an immutable commit.

### F4 (info) — archived evidence file mixes checker output with a hand-built footer

`.ufo/waves/round-17/evidence/label-check.txt` is nine checker lines plus four appended lines
(`exit=1`, `245fd114…`, and the sha256 of tool and claims). A fresh run reproduces the nine
checker lines exactly and the footer hashes match current files, so this is provenance
bookkeeping, not a mismatch. A consumer parsing the file as pure checker stdout would see four
extra lines.

### F5 (residual) — co-occurrence-only document stage and `doc_text` bypass

The document stage (`label-check.py:111-120`) requires only that the receipt basename and the
token occur in the same 1-3 line window. A sentence that names both while negating the
attribution ("`X.json` does not show `token`") would pass an `expect: ok` claim. No current
claim is of that form. Separately, the presence of `doc_text` bypasses `git show` entirely
(`check_claim` line 103-ish) and nothing enforces that a `doc_text` claim is labelled
`doc: "mutant"`; a future claim could claim a real doc path yet be scored against a synthetic
string.

### F6 (residual) — contradictory verdict fields are unioned, not rejected

`outcome_tokens` accumulates a set (`lines 79-84`), so a receipt containing
`MADO_PLAN: frozen_error` plus `"finding": "snapshot_tampered"` would satisfy a claim for
either token. Criterion 23 defines all three forms as outcome evidence but does not say what
to do when a single receipt's fields disagree; the checker silently accepts either side.
Current receipts are internally consistent.

## What the attack failed to falsify

- The three declared red expectations are real defects/controls, not artefacts of rev choice:
  `frozen-tampered.json`'s blob is identical at `1e31681`, `27cd06f`, `3722ba4`, `fc6f960`
  and HEAD, so citing `1e31681` is not a stale-receipt trick; the doc line is at exactly
  `27cd06f:131-132`.
- The two real-document greens (`frozen-match-green`, `spotcheck-selftest-final-green`) match
  their receipts clause-by-clause, including the `52/52` summary and both tamper rows; the
  receipts were introduced at the cited `4bfb236` and are unchanged since.
- The `measured_commit` gate works (`1e31681` vs `9dcf248` separates claim 5 from claim 6),
  and `EXPECT_SUMMARY` is sensitive to a flipped expectation (6/7) and to a broken rev
  (`exit 2`).
- The round-17 recut receipt is not a self-declared string: its pristine digests, its
  single-byte tamper digest, its gate hash, and its control run all recompute from repo bytes.

## Verification gaps

- The recut outcome was verified from the recorded receipt plus recomputed digests, not by
  re-executing `mado-action-plan.py` (not on this reviewer's permitted runnable list under the
  host pause). The recorded `MADO_PLAN: snapshot_tampered` / exit 2 is consistent with every
  digest it pins.
- `EXPECT_SUMMARY` counts only claims that declare `expect`; all seven do, so the denominator
  is complete here, but a future claim could omit `expect` and silently leave the denominator.
- I did not assess C1's separate calibration literal (`14/22 → 15/23`) or the C3 tripwire
  suites; this report is scoped to `label-check.py`/`label-claims.json` and the documents and
  receipts they cite.
