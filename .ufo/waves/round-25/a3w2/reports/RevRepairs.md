# RevRepairs — review of routed repairs at lane commit `2896dc4a`

Scope: the six repairs routed from round-24 closure `corpus/lessons/round-24-verifier-spotcheck.md` §7 against
base `41cc04c8`. Checks: is each repair true of the cited bytes, append-only except the one declared in-row
correction, and does it close the routed defect? Reviewer: `MadoR25A3.RevRepairs` (non-author, leaf). Method:
read-only `git diff/show/log` in the lane; two counters re-run read-only (`tw-precision.py` reads committed bytes;
`MistakeFix.py` reads `corpus/SOURCES.md`); criterion-36 checker run read-only (`GIT_OPTIONAL_LOCKS=0` inside the
script itself). No edits made; no `__pycache__` left (`python3 -I` + `PYTHONDONTWRITEBYTECODE=1`).

Whole-range append-only check: `git diff --stat 41cc04c8 2896dc4a` shows exactly one deletion in the whole
range — `rule-attribution-r24.md` −1/+5, the declared R3 in-row row. All other pre-existing-file changes are
pure insertions. The two mid-file SCORECARD pointer paragraphs are insertions, not edits (zero lines removed),
which matches defect 6's own "add pointers … append-only" wording (the rows it names are mid-file).

## Per-repair findings

- **R1 (defect 1, M24-2; counter meetable by a generic note) — CLOSED.**
  The round-24 C1 claim is closed (`rejected-honest-stop`) and its counter is not reused (`registration.md:78`).
  QUALITY criterion 36 (`corpus/QUALITY.md`, appended section) gates any future counter on pre-data control
  receipts covering the shortcut shapes that have met counters — the round-24 failure class is detectable
  pre-data by exactly these controls. Checker `check-control-receipts.py` re-run by me reproduces the committed
  red receipt byte-for-byte: `--round 24 --data-registry .ufo/waves/round-24/w1/reports/swarm-registry.json
  --tip 41cc04c8 --any-md` → `order=LATE gap_s=-1083 shapes_missing=EmptyArray|AllFalse,Echo,LabelKeyed`, exit 1.
  Residual: the defect's literal clause "the claim anchor must require attribution content" is not encoded in
  the criterion; closed via mechanism (pre-data controls) + non-reuse, same standard the routing row declares.

- **R2 (defect 2, M24-5; population + transcription) — OPEN on one clause (F1).**
  Criterion 36's oracle clause covers transcription ("a counter whose expected value the lane computes with its
  own model is replaced by an independent oracle or declared to measure only agreement"). Round-25 C2 is
  exploratory with no counter, so nothing this round re-triggers the defect. But the defect's other clause —
  "the predicate's population must equal the counter's (all capability tables, 15 rows)" — is encoded nowhere:
  nothing in criterion 36 or `check-control-receipts.py` compares a counter's counted population to a
  predicate's named population. The 12-vs-15 row mismatch that produced M24-5 could recur undetected.

- **R3 (defect 3; `rule-attribution-r24.md:25` A18 body) — CLOSED.**
  Exactly one line changed in-row (the sole deletion in the range). New text says A18 logs the window-rule
  `workspace` *effect* — verbatim agreement with the note's own errata item 5 (`:152-154`), and the in-row note
  points at it. Whole-note sweep: `workspace-rule` appears only at `:25` (the corrected negation), `:153` (item
  5 itself), `:170` (the new round-25 errata quoting history). Appended `## Errata (round 25; append-only)`
  block documents the in-row exception, cites the closure lines, and explains the round-24 errata heading was
  true when written. Defect asked for an in-row correction plus corrections sweeping every mention: done.

- **R4 (defect 4; lesson `:58-59` S161 rationale) — CLOSED.**
  Append-only block at end of `lessons/round-24.md`. Verified: the committed S161 quote at `round-24.md:48`
  (`query.className = …`, 15 words) contains no `|` — the `||` rationale was indeed false of the committed
  bytes. Correction names the closure's surviving reason (no note row cites S161 — verified, `S161` absent from
  `rule-attribution-r24.md`; file is a query filter).

- **R5 (defect 5; receipts "before any data seat") — CLOSED.**
  Append-only corrections in both `registration.md` (+7) and `lessons/round-24.md` (same block as R4).
  Timestamps verified against history: receipts `464a0245` committed `2026-10-23T00:53:36-03:00`; wave-1
  registry `createdAt 2026-10-23T03:35:33Z` = `00:35:33 -03`; first data `cf86f9e0` `2026-10-23T01:03:16-03:00`
  — every number in the corrections matches, including "two controls scored at 00:36" (closure §2.3). The
  corrected claims still read verbatim at tip (registration `:92`, lesson `:6`), with the appended corrections
  pointing at them and at each other. "True only as before any data landed" is correct.

- **R6 (defect 6; `SCORECARD.md:437`, `:1342` stale rows) — CLOSED.**
  Pointer paragraph inserted immediately after the collision-screen table (`:440-443`) and immediately after
  the `tripwire evidence marker`/`harness fail-closed` table (`:1349-1352`) — the rows' own sections, as routed.
  Claim truth, independently re-verified: `MistakeFix.py --registry corpus/SOURCES.md` prints `collisions=4`,
  exit 1 right now (round-24 base/tip corroborated by `SCORECARD.md:1601-1603` and closure `:109`);
  `tw-precision.py 8e5d9369` re-run by me gives L 15/18, P 66/66, exit 0 — the row's L 17/18 at `28c6837` is
  superseded. Both pointers cite the round-24 correction (closure §2.2 / Capability-status row `:1591` and
  scope paragraph) and resolve `## Current state (round 25)`, which exists at `:1629` and itself names both
  stale rows `fails`. Line-shift bookkeeping in the ledger (`:1643-1644`) is consistent.

## Findings by severity

- **F1 (medium): R2 partially closed.** Criterion 36 and its checker encode the ordering and the oracle/
  transcription clause but nothing about counter-vs-predicate population equality — the other half of routed
  defect 2. Moot this round (C2 has no counter); a standing-rule hole for the next counter claim.
- **F2 (low): checker's shape coverage is filename-substring only** (`:102-107`). A receipt file merely named
  for a shape covers it; and `CtlLabelKeyed.md` carries no `CONTROL `/`# Control` marker, so the default
  receipt detector sees 9 of 10 attempt-3 receipts (`--any-md` is the documented escape; round-24 receipts
  needed it too). Neither blocks the criterion as worded ("receipts name the shapes"), but the check enforces
  naming, not that a control actually exercised the shape.
- **F3 (note): `--data-registry` is caller-declared** (docstring `:21-23`), so "before any data seat" means
  "before the named wave's `createdAt`". Round 25 is clean on the honest reading — `a3w2` is the declared data
  wave (`registration.md:221`) and its registry `createdAt 07:31:20Z` postdates the receipts `459dd17f`
  `07:29:16Z`; but `a3w1` (C2 exploratory re-runs, created 06:52:29Z) predates the attempt-3 receipts, so a
  strict "any seat that produces data" reading of criterion 36 would already fail round 25.

## Residual risk and verification gaps

- Round-25 green is not yet demonstrable via the checker: `a3w2/reports/swarm-registry.json` exists in the
  worktree (createdAt 07:31:20Z) but is absent at `2896dc4a` and at HEAD `fa466833` — checker exits 2
  UNEVALUABLE. Timestamp comparison already shows order holds. Checker does PASS (exit 0, `order=ok
  gap_s=5364`) against `a3w1`'s committed registry.
- Pointer-1's "at round-24 base" leg not re-run by me at `8e5d9369`; corroborated by committed receipts
  (`SCORECARD.md:1601-1603`, `AtkC2Table.md:89-96`, closure `:109`) plus my fresh `collisions=4` run at tip.
- R1's unencoded literal clause (anchor must require attribution content) shares F1's family; closed by the
  routed mechanism + counter non-reuse rather than by rule text.
- Repairs R7/R8 (SHONEN pointers, H2 carry) are outside this assignment's routed set and were not checked.

## Verdict

REPAIRS: closed 5/6; open: R2 — the routed defect's "predicate population must equal counter population"
clause is encoded nowhere in criterion 36 or `check-control-receipts.py` (F1); R1, R3, R4, R5, R6 verified true
of cited bytes, append-only except the declared R3 in-row correction, and closing their defects.
