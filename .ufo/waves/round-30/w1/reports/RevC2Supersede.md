# RevC2Supersede — supersession discipline (mado round 30, w1)

Role: reviewer (report only). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Item: reconcile `corpus/QUALITY.md` rows 41–51 against the rows they supersede;
check criterion 20 under criterion 21's supersession; check that no new row
sneaks an ungrounded criterion past PRED-C2-r30.

Canonical bytes read (never the worktree for measurements):
- base `8f51071b5bc44c815eeb5da76bb7f1947994ffb8` (round-29 closure)
- data `446dc3966193c81e64896f4880a19a4bd249255b` (round-30 data commit)

Method: ran the frozen counter at both revisions; independently re-implemented
its criterion/supersession parse and diffed every supersession pair from
`git show REV:corpus/QUALITY.md`; read the cited lesson rows. No `lsp` device or
server exists on this seat (the tool surface exposes none), so reference/
definition/diagnostics checks were done against committed bytes with the frozen
counter plus an independent parse — not via text grep.

## Findings

### F1 — HIGH (content loss in an active restatement; predicate not flipped): row 48 drops criterion 32's credit-limiting and harm statement

Criterion 32 (`8f51071b`) ends:

> This criterion is added after final falsification, supplies no retroactive pass
> and no numeric C2/criterion-count credit; delivered C1 fails it and remains harmed.

Row 48 (`446dc396`) restates the rule and ends at `...a finite direct-literal
fixture pass is insufficient.` then `Supersedes criterion 32; … (lesson:
lessons/round-21.md#mistakes M13; residual/FinalBindingReview.md F1–F5 and its
six inert fixtures)`. Both sentences are absent (verified by sentence-level
containment against the normalized row text).

This is the one dropped clause that binds a **count**: criterion 32 explicitly
supplied “no numeric C2/criterion-count credit”, and row 48 is counted as a
literal line (40/52) and a resolved-active line (40/40) in the C2 claim. The
section preamble (“restates its rule verbatim”) and the lesson's M30-1 fix cell
(“supersede the ungrounded criteria verbatim”) are therefore false for this
pair, and the supersession silently converts a credit-barred criterion into a
credit-bearing row.

Predicate impact: none. Even if row 48's literal credit is withheld under
criterion 32's clause, literal is `39/52 = 0.7500` (≥ 0.70) and active resolved
is `39/39` (row 48 excluded) — `PRED-C2-r30` still `TARGET_MET`. The defect is
fidelity of the supersession, not the verdict.

### F2 — MEDIUM (content loss in active restatements): rows 49–51 drop the evidence anchors of 38–40

Rule sentences are preserved word-for-word; the parenthetical evidence is not:

- 38 → 49: drops ``(M28-1, `count.py:100` pinned count-v4.py at `3d7d301f…` vs
  committed `635ae788…`)``; note says only “the bare M-id becomes a canonical
  citation”.
- 39 → 50: drops ``(M28-2: H1's directory was cleaned before closure; leg 1
  verified from the committed `ReviewerSuiteMonotone.md` receipt)`` — the named
  receipt 39 relies on as its verification basis.
- 40 → 51: drops ``(M28-3: `ref-chk-no-anchor` survived;
  `ref-chk-unreadable-exit-one` in the same round was killed)``.

No metric impact (rows 38–40 are superseded and excluded; rows 49–51 resolve via
M28-1/2/3, all present in `corpus/lessons/round-28.md`). The document does not
lose the bytes — the superseded rows remain, and I verified the base file's
first 336 lines are byte-identical to the data commit's first 336 lines — but
the active restatements do not carry the concrete evidence their source rows
used, contradicting the “verbatim” claim.

### F3 — MEDIUM-LOW (rubric fidelity): criterion 20 is parsed as fully superseded, but criterion 21 supersedes a scoped route conditionally

Criterion 21's text: “Supersedes criterion 20's prospective install route
**while the operator's host-wide pause holds**” … “After explicit operator lift,
criterion 20's complete real-plan/installed-name comparison still applies”.
Criterion 20 therefore is not fully superseded; it is suspended for the pause's
duration and reactivates on lift. The counter's `SUPER_RE` matches the number
and excludes 20 from both fractions unconditionally, while `count.py`'s
docstring states “full supersedes only”.

Observed set matches the assignment's expected set exactly:
`[1,2,3,4,5,18,19,20,32,38,39,40]` (12), reproduced by the counter at both
revisions and by my independent parse. Consequence: reported denominators are
`39` active at base and `40` at tip; with 20 active they would be `40` and `41`,
and because 20 resolves at both revisions (`lessons/round-15.md#mistakes M2`)
the fractions would read `32/40` and `41/41` — verdict unchanged. The exclusion
is disclosed in the registration (“20 is already superseded by 21”), so this is
a declared-but-wrong rubric statement, not a hidden adjustment.

Same area: the registration's C2 target sentence says “12 lines superseded by
rows 41–51”. Rows 41–51 supersede 11 criteria; the 12th is 20, superseded by
row 21. Numbers are right, attribution is not.

### F4 — LOW (factual error in the repair narrative): “18, 19 and 32 cite a lesson outside the numbered line”

The round-30 section preamble (line 343) and lesson M30-1 repeat this. It is
true for 18 and 19 (citations on indented continuation lines) and false for 32:
`Ground: lesson round21 M13, …` is on criterion 32's numbered line, and the
counter resolved criterion 32 at base (base `UNRESOLVED` is exactly
`{1,2,3,4,5,38,39,40}`; 32 is not among them). 32 was only absent from the
**literal** fraction because its numbered line lacks the string `lessons/`.
The fix note in row 48 (“the `lesson round21` spelling becomes the canonical
path”) is accurate; only the preamble's classification is wrong.

### F5 — LOW (residual predicate gaps; no exercised bypass found)

(a) Rows 41–45 cite only `lessons/round-30.md#mistakes M30-1`, whose content is
the finding that criteria 1–5 carried no lesson citation. That is meta-grounding,
not a lesson of the rules' failure modes; the in-text declared ground
`MINT.md` exists at the data commit (two demand instances) and is ignored by the
counter. Five of the 40 active criteria pass on a citation about their prior
absence. This is disclosed in rows 41–45, so I do not grade it a defect, but the
predicate cannot distinguish it from substantive grounding.

(b) Bare `lessons/<file>` citations are checked for existence only. Row 52's
first citation, `lessons/round-29.md`, passes on file existence; I verified
substantively that round-29.md's `M29-sweep` row does record the counter at
41/43 “base and tip alike … routed to round 30”, so the citation is true here.
A bare path citing an unrelated lesson would pass.

(c) The counter attributes every line up to the next numbered criterion to the
preceding criterion, so a section note's `lessons/` citation could prop a
citation-less criterion. At the data commit this is exercised only on superseded
32 (absorbs the Round-22 notes) and 40 (absorbs the round-30 “Grounding repair”
paragraph); a per-criterion scan shows the only criteria lacking `lessons/` in
their own numbered line + indented continuations are 1–5, 32, 38–40, all
superseded. No active criterion relies on note-attached citations at either
revision.

(d) “Resolved” tests presence, not relevance: an M-id that exists but does not
support the restated rule would pass. My spot check confirms presence of
M30-1/M30-2 (round-30), M29-sweep + `41/43` (round-29), M13 (round-21),
M28-1/2/3 (round-28), M4/M1 (round-14), and R13-V1 in
`corpus/lessons/round-13-verifier-spotcheck.md`.

## No-finding confirmations

- **Superseded set is exact.** No other `Supersedes criterion …` occurrence in
  the data file; self-reference is guarded; no chain or double supersession.
  Rows 41–45 → 1–5, 46 → 18, 47 → 19, 48 → 32, 49 → 38, 50 → 39, 51 → 40,
  21 → 20. Active = 52 − 12 = 40.
- **Append-only.** `QUALITY.md@8f51071b[0:336] == QUALITY.md@446dc396[0:336]`;
  the data commit inserts exactly 22 lines after criterion 40. No superseded
  row was rewritten, and the document retains every dropped detail (F1/F2 are
  restatement losses, not document losses).
- **No new row is wholly ungrounded.** Every row 41–52 has a citation that
  resolves at `446dc396`; row 52 is a genuinely new criterion (+1) grounded in
  M30-2 and the round-29 sweep record. No restated row double-counts its source
  (each is excluded from the active set).
- **Registered metrics reproduce.** Counter at data: `literal 40/52 = 0.7692`,
  `superseded=[1,2,3,4,5,18,19,20,32,38,39,40]`, `active=40 resolved=40`,
  `TARGET_MET`, exit 0. At base: `literal 28/40 = 0.7000`, `superseded=[20]`,
  `active=39 resolved=31`, `UNRESOLVED {1–5,38–40}`, `TARGET_MISSED`, exit 1 —
  exactly the registration's before/after numbers.
- **Row 47's outside expansion is correct.** `outside R13-V1` →
  `lessons/round-13-verifier-spotcheck.md R13-V1`; that file exists and its
  “Routed defects” item 1 is R13-V1 (retained-data wording).
- No resume path is involved in this item, so `resume_continuity_v1` was not
  exercised (n/a).

## Residual risk

- Criterion 20's reactivation after an operator lift is not modeled; any future
  round re-running `count.py` keeps excluding 20 from both fractions.
- Grounding is presence-checked, not relevance-checked (F5b/d); the 40/40 is a
  citation-resolvability claim, not a support-quality claim.
- Lane worktree state at review time: `M quality/q36-successor-receipts.txt`
  (reported by peer RevC1Fence; not my item, not restored). The bytes I measured
  are unaffected — `git diff 446dc396 -- corpus/QUALITY.md corpus/lessons/round-30.md
  .ufo/waves/round-30/c2/count.py` is empty, and the worktree `QUALITY.md`
  equals the data commit.

## Verification gaps

- No `lsp` capability on this seat; no semantic server could answer
  `corpus/QUALITY.md`. Substituted with the frozen counter at the two named
  revisions, an independent re-implementation of its parse (identical superseded
  set and active count), and byte-level append-only diffing.
- I did not re-run C1/C3 or their gates (outside item).
- No tools were installed or updated for this review.
