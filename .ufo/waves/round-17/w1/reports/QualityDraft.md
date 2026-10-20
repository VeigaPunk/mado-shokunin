# QualityDraft — round 17 report (mado-r17-w1)

Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Scope: draft one append-only QUALITY criterion 23 (lesson M1, outside R16-V1) and a candidate criterion 24 (lesson M2). Host pause honored: no sudo, pacman/yay/paru, systemctl, hyprctl, live probes, transcript reads, jj or git commands. No tools installed or updated.

## Behavior

- Wrote `.ufo/waves/round-17/drafts/QualityDraft.md` (only file written besides this report). It contains criterion 23 (admitted-candidate text, first line carries `(lesson: lessons/round-17.md#mistakes M1; outside lessons/round-16-verifier-spotcheck.md R16-V1)`) and candidate criterion 24 (lesson M2, limits stated inline). Nothing edited in `corpus/QUALITY.md`; L1 owns admission.
- No executions. Reads only: `corpus/QUALITY.md` (criteria 1-22), `corpus/lessons/round-16-verifier-spotcheck.md`, `.ufo/waves/round-17/w1/spec.json` (context and QualityDraft item), and two round-16 receipts.

## Gates

- Not run by this seat, per assignment: no test, build, lint, or tripwire execution.
- Receipts read and checked by hand (grep/read, not executed):
  - `.ufo/waves/round-16/evidence/frozen-tampered.json`: `measured_commit` 9dcf248993a9622a5b016edec0003187141745d2; `exit` 2; stdout `MADO_PLAN: frozen_error`; detail "expected.json pair 1/'denied_executable:sudo' is unreachable". It does not record `snapshot_tampered`. Red for the R16-V1 citation.
  - `.ufo/waves/round-16/evidence/action-selftest-final.json`: `measured_commit` 1e31681e76b5e7caadd1c749e18669a3632a1c3b; `exit` 0; row `SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered`. Green target for a corrected citation.

## Touched surfaces

- Drafted: `.ufo/waves/round-17/drafts/QualityDraft.md` (new).
- Report: `.ufo/waves/round-17/w1/reports/QualityDraft.md` (this file).
- Not touched: QUALITY.md, LOG.md, lessons, SKILL.md, SCORECARD.md, SOURCES.md, tools, transcripts.

## Out-of-scope items

- The round-16 `lessons/round-16-verifier-spotcheck.md` line 131 and the report still cite `frozen-tampered.json` for `snapshot_tampered`. Correcting them is L1/LessonDraft work (append-only correction). Not done here.
- The round-17 tripwire (`tools/mado-tripwire.py`) is not written or verified by this seat. Criterion 24 is a candidate until it exists and passes its selftest.
- `lessons/round-17.md#mistakes M1/M2` did not exist at the time of drafting; the anchors are cited as planned.
- No `[UNK]` host state was queried; host pause honored.

## Findings

### Criterion 23 — rationale

R16-V1 (verified above): the lesson and report cite a receipt that records `frozen_error` at 9dcf248 as showing `snapshot_tampered`. The token was true only of a different receipt at 1e31681. The round-16 closure already labels this a status-neutral evidence-labeling defect; C2 rests on the 52/52 selftest and `frozen_match`, not on the mis-cited receipt.

Why a new criterion rather than an existing one:
- Criterion 9 binds a verdict to a commit or frozen sha. The R16-V1 receipt *was* bound to 9dcf248; the defect was the token attributed to it. Criterion 9 cannot catch that.
- Criterion 13 requires committed or quoted evidence. The receipt is committed and was quoted; the quoted outcome did not match the sentence.
- Criterion 22 concerns counting rules, not token attribution.

Label check (manual here; L1 should script it once, stdlib, against the lane):
- Red: round-16 lesson line 131 cites `frozen-tampered.json` for `snapshot_tampered`. Must fail: the recorded outcome is `frozen_error`, and the revision is 9dcf248, not the 1e31681 revision the claim describes.
- Green: the corrected citation to `action-selftest-final.json` at 1e31681, token on the `got` side. Must pass.
- The check must match the outcome field (exit, stable id, or `got`), not raw substring. A substring grep would pass the red case through the `want`/`got` fixture text of a failed row, so the check must be shown failing on a row like `want 2/snapshot_tampered got 2/frozen_error`.

How criterion 23 can fail:
- Paraphrase bypass: a sentence says "the frozen gate refused the tamper" with no token. A token check passes it; a semantic reviewer must judge it.
- Field mismatch: a receipt's exit or stable id carries the token in a field the check does not read, so a correct citation is rejected (false negative on the rule).
- Revision field absent: an older receipt has no `measured_commit`; the check cannot bind it and must say so rather than pass it.
- `want`/`got` confusion: a check that accepts the token on either side passes a failing row. The draft excludes `want`.
- Scope creep: applied to non-verdict tokens (counts, paths) it produces false positives. The draft limits it to verdict tokens.

### Criterion 24 (candidate) — rationale

Round-16 M5 (`pacman -Q waybar` during a source-only, host-paused round) was disclosed as a process defect, not an axis harm, and no tool existed to check seat conduct after the fact. The tripwire, per the spec's C3 anchor, gives a repeatable post-hoc check over the actual issued bash/eval calls, and this criterion requires any "no host-mutation" claim about a seat to cite its verdict and file hashes.

How criterion 24 can fail (stated in the draft as limits):
- False negatives, by design: scripts written by the seat and executed later; tools other than bash and `!`-eval; non-`!` eval code; subagent session files outside the scan set. A clean verdict therefore bounds nothing beyond the parsed calls.
- False positives: the tripwire splits on newlines, so heredoc or file-payload text may be classified as issued. Findings need adjudication against execution.
- Misreading exit 2 as clean: a `could_not_evaluate` verdict must never support a clean claim.
- Rule names classify command text, not effect (e.g. `pacman -Sp`, a dry-run plan, is `package_query`).
- Permit selection after the fact can hide a finding; the permit set must be named.
- Tripwire classifier is unverified against host behavior; its selftest proves only declared-fixture classification.
- Reading session JSONL is restricted by the assignment: this seat did not read any transcript and did not verify the spec's line-54 anchor. Its statement is taken from the spec.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/drafts/QualityDraft.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/w1/reports/QualityDraft.md`
- Read-only evidence: `.ufo/waves/round-16/evidence/frozen-tampered.json`, `.ufo/waves/round-16/evidence/action-selftest-final.json`

## Checks for the main agent to run once after integration

- Script the criterion 23 label check (red: lesson line 131 vs `frozen-tampered.json`; green: corrected citation vs `action-selftest-final.json`) and confirm the red case fails.
- Confirm `lessons/round-17.md#mistakes M1/M2` exist at the anchors cited, or re-anchor.
- When `tools/mado-tripwire.py` lands, run its `--selftest` once before admitting criterion 24 out of candidate status.
