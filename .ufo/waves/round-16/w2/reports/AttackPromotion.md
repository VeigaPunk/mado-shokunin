# AttackPromotion — Mado round 16 (w2, leaf reviewer)

Scope: promotion state and outside-review claims in the integrated round-16 artifacts at
`/home/vgpnk/Projects/shokunin/mado-shokunin` (baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`).
Source reading and read-only `git log`/`git show`/`git diff` only. No gate, selftest, measure.py,
census, build, or test was executed. No package, service, compositor, or input operation. No tool
installed or updated. No `~/.omp` file opened.

## Verdict

No newly fabricated SHONEN mark and no fabricated outside review was found in round-16 text.
Historical promotion statements are mostly labeled as not current. Four pre-existing stale
promotion statements lack a superseded-by note, one registry row mis-anchors its closure baseline,
and one untracked bytecode artifact suggests an in-lane import of the gate. Findings are ranked below.

## Checks that pass (with anchors)

| # | Check | Observation | Anchor |
|---|---|---|---|
| P1 | SHONEN.md unchanged | `git diff` empty; 1036 B at HEAD and worktree; 12 lines; 4 × `- [~]`, 0 × `- [x]` | `SHONEN.md:1-12`; `git diff -- SHONEN.md` empty |
| P2 | No new `[x]` in round-16 text | Grep of every `+` line in LOG/SCORECARD/SKILL/QUALITY/README/SOURCES and the new lesson, knowledge note, gate, policy, and cases files finds no `[x]` mark | `git diff -U0`; `corpus/lessons/round-16.md`; `corpus/knowledge/waybar-observation-boundaries-r16.md` |
| P3 | No outside verdict claimed | Round-16 lesson states the outside spot-check is pending and that seat advice does not clear SHONEN | `corpus/lessons/round-16.md:75-77` |
| P4 | Seat advice labeled as not outside | OutsideLearning draft: "Not an outside review… nothing here clears SHONEN" | `.ufo/waves/round-16/w1/reports/OutsideLearning.md:5,9`; ReportContract `:113,119` |
| P5 | Historical 4/4 explicitly not current | SCORECARD fleet-round-1 section: "historical 4/4 `[x]` at arc close is not current promotion clearance" | `SCORECARD.md` (fleet round 1 header, lines ~ "The historical 4/4") |
| P6 | Round-16 LOG entry | "SHONEN remains four author assertions; historical SKILL promotion tables remain dated, not current independent clearance" | `LOG.md` round-16 entry |
| P7 | Closeout note labeled | README row: "the old promotion assertion is not current independent clearance" | `corpus/README.md` closeout-r11 row |
| P8 | SKILL current-state section | "Promotion remains operator/integrator-owned… this round's dispatched subagents are still the mado authoring lane" | `SKILL.md:1712-1714` |
| P9 | U7 credit excludes own-work row | `measure.py` credits only S053/S054; S055 is explicitly "deliberately absent" from U7 credit | `.ufo/waves/round-16/measure.py:203-206` |
| P10 | S053/S054 bindings agree | SOURCES digests `efb6a63a…d82` (S053) and `2232f7f7…291` (S054) match `evidence/source-bindings.json` (6656 B and 8746 B). Read-only comparison; no re-fetch | `corpus/SOURCES.md:65-66`; `.ufo/waves/round-16/evidence/source-bindings.json` |
| P11 | Gate "independence" is a self-claim | `safety-cases.json` `independence` says cases are authored from the dispatch spec only. This is an authoring-seat statement, not outside verification | `.ufo/waves/round-16/safety-cases.json` assumptions.independence |

## Findings (ranked)

### F1 — medium — SKILL.md promotion-box table still shows `[x]` with no superseded-by note

- Anchor: `SKILL.md:582-600` (HEAD `:553-571`). The table is dated "State measured 2026-10-14 16:28Z" and
  lists box 1 `[x]` (MADO-R3-4), box 3 `[x]` (MADO-R3-4), box 2 `[~]`, box 4 `[~]`.
- Current truth: `SHONEN.md:5-11` has four `[~]`. Commit `7cd7f33` (2026-10-15) downgraded the two
  `[x]` marks, which carried VER-M3 and VER-M4B attributions, to `[~]`
  (`git show 7cd7f33 -- SHONEN.md`). SCORECARD `:39-40` states the historical `[x]` is not current.
- Counterexample: a no-context reader who follows the "Promotion-box status" section sees 2 of 4
  boxes cleared. The current SHONEN has 0 cleared boxes.
- Compounding: `SKILL.md:662-664` says "When it lands, SHONEN reads 4/4 `[x]`". That closure edit
  never landed and is now superseded.
- Round-16 SKILL diff (+29 lines, at `:37-44`, `:476-510`) touched the file and did not correct this.
  The w1 SHONEN seat flagged the same table.
- Recommended fix (append-only, not executed here): add a dated block under the table stating that it
  is superseded by `SHONEN.md` (four `[~]`), by the `7cd7f33` downgrade, and by `SCORECARD.md:39-40`.
  Owner: L1 (SKILL.md).

### F2 — medium-low — arc-synthesis states a superseded 4/4 `[x]` fact without a marker

- Anchor: `corpus/knowledge/arc-synthesis.md:73`: "`SHONEN.md` is 4/4 `[x]` byte-identical since
  `c03c249`". Related: `:316` and `:327`.
- The note header says `verified-at: 2026-10-14`, so the claim was true when written. It is false at
  HEAD (`7cd7f33`, 2026-10-15, changed the marks to `[~]`). The note has no superseded marker. The
  `corpus/README.md` row for this note says "no promotion inferred", which does not cover the stale
  body line.
- Recommended fix: an append-only errata line citing `7cd7f33` and `SCORECARD.md:39-40`. Owner: the
  corpus-knowledge owner.

### F3 — low-medium — S055 registry row mis-anchors the closure baseline and titles own-work as "Independent"

- Anchor: `corpus/SOURCES.md:67` (S055). Row text: "Independent rejected-harmed safety closure…"
  with type `own-work`, tier `A`, anchor "closure at baseline 32c4fda…".
- The closure's own text (`corpus/lessons/round-15-verifier-spotcheck.md`, header and opening
  paragraph) says it reviewed baseline `ea0446fcb4840089…`, measured content `5f13870…`, and delivered
  `9ebd737…`. Commit `32c4fda` is the closure's own commit (`git show 32c4fda --stat`: adds that file),
  not its review baseline.
- Counterexample: a reader following the S055 anchor reaches a baseline that the closure never reviewed.
- The round-16 lesson and LOG use `32c4fda` correctly as the round-16 baseline. Only the S055 row is
  wrong.
- The word "Independent" in a lane-owned tier-A row can be read as outside authority. The independence
  belongs to the hyaku closure seat, not to the lane. The row's teaches cell does state the limit
  correctly.
- Recommended fix: change the S055 anchor to "closure reviewed `ea0446f`, content `5f13870`, delivered
  `9ebd737`, committed `32c4fda`", and retitle to "own-work record of non-author closure (hyaku,
  2026-10-20)". Owner: L1 (SOURCES.md).

### F4 — low — pre-existing dated packs and logs state `[x]` without a superseded note

- `plans/completion-evidence.md` (2026-10-14 pack): "all four boxes `[x]`" under "SHONEN status". The
  header is dated, but there is no superseded-by line.
- `LOG.md:295,417`: historical "PROBATION COMPLETE 4/4" and "Probation 4/4 `[x]`". LOG is append-only;
  the 2026-10-15 section and the round-16 entry supersede these in context. Acceptable as historical.
- `SCORECARD.md:28`: arc-end text. Explicitly superseded by `:39-40`.
- Recommended fix: a one-line superseded-by note at the top of the pack. No edit to LOG history.

### F5 — medium (process) — untracked bytecode shows an in-lane import of the gate after its last write

- Anchor: `tools/__pycache__/mado-action-plan.cpython-314.pyc`, mtime `2026-10-20 05:46:56.81`.
  `tools/mado-action-plan.py` last written `05:46:34.09`, 22 s earlier.
- A `.pyc` is created only when the module is imported or compiled, not when it is run as a script.
  So some seat imported or compiled the gate during the wave. The wave contract says no gate execution
  by seats. Import runs module top-level code, and compile reads the source.
- `tools/__pycache__/` is untracked and not covered by `.gitignore` (which lists only
  `.ufo/interactive-sessions/`). `git status` shows it as `??`.
- I cannot determine which seat did this from the artifact alone. Not deleted here.
- Recommended action for L1: identify the seat; disclose the event in the round-16 LOG/lesson without
  rewriting history; remove `tools/__pycache__/`; consider adding `__pycache__/` to `.gitignore`.
  This is a no-execution disclosure, not a promotion finding by itself.

### F6 — low — SCORECARD round-16 section states measurement before L1 verification

- Anchor: `SCORECARD.md` round-16 block: "All three claims are measured; none is exploratory." and
  "C1 … 7/7 (10/10)" and "C2 … demonstrated (1)". The same block says "Baseline/delivered fractions
  will be recorded from committed inputs" — a future tense that conflicts with the present "are measured".
- The lane has not yet verified these claims; L1 verifies once after integration. "Demonstrated" and
  "measured" read as completed verification.
- Recommended wording: "declared; L1 verification pending" until the single post-integration run.

### F7 — info — prior SHONEN downgrade rationale is only in SCORECARD

- Commit `7cd7f33` downgraded two `[x]` marks with verifier attributions to `[~]`. Its message is
  "retain fleet round 1 navigation candidate; record routing block", and the reason is not in the
  message. The conservative downgrade is consistent with PROTOCOL/QUALITY 12. History is not rewritten.
  Noted for completeness.

## Verification gaps for L1 (not run here)

- No after-integration census artifact exists under `.ufo/waves/round-16/evidence/`; only
  `census-before.txt` (measured at `32c4fda`, exit 0, with the historical duplicate-URL warnings).
  The post-integration `sources-census.sh validate` result is unobserved.
- `source-bindings.json` digests were compared with SOURCES.md text only; no re-fetch was done, and
  this seat did not verify the raw bytes.
- Whether any seat imported the gate (F5) is unresolved.

## Tooling record

No installs or updates. No `pacman` query or transaction. No service or compositor operation. No
`~/.omp/agent/*` read or write. Git read-only history subcommands only (`log`, `show`, `diff`,
`status`).

## Limits

This is a static read of the integrated lane tree and its committed history at the working state. It
does not prove that the historical round-3 through round-11 verifier attributions are sound. Outside
closure is out of scope for a leaf reviewer and is not claimed.
