# ReportPointerJoin — exact pointer spellings for the round-17 report

Status: report only. No file was written except this report; every other path
was read read-only and inside the lane. No git mutation (only read-only
`git log`/`git show`), no jj command, no package/service/compositor/input
command, no tool install. Host pause respected: no host-side path under
`~/.config` or elsewhere was opened as anything but lane-local text, and none
was opened at all by this seat.

## Axes and the one move

Declared axes this seat can affect: **C1 calibration** (citation text is the
scored artifact), **C2 coverage** (documentary route pointers), **C3
operability** (pointer to receipts). The non-harm axis is the binding host
pause (R15-V1).

Move: replace free-form round-name pointers with a two-grammar pointer
discipline that is *mechanically resolvable* against the exact heading lines:

1. Prose/lesson pointer: `<file>` §"`<full heading line, minus the leading
   `#`s>`" — copy the heading character-for-character.
2. QUALITY criterion pointer: `lessons/round-N.md#<lowercase-h2-slug> Mn`
   (the existing convention of criteria 6–22), e.g.
   `lessons/round-17.md#mistakes M1`; never a file-base-only root anchor.
3. Every pointer must be paired with a failing label check that the wrong
   spelling (`round16`, `Round16`, bare `round 16`) fails.

This improves C1 (the criterion's own citation resolves) and de-risks C2/C3
(report pointers resolve) without touching any other axis.

## Evidence — exact LOG.md headings (current tree, 1253 lines)

Whole-line exact counts verified with `grep -Fxc`; each is 1.

| Line | Exact heading (copy verbatim; `—` is U+2014) |
|---|---|
| 656 | `## 2026-10-19 — round 12 (kaika): calibration, freshness, sourced coverage` |
| 769 | `## 2026-10-20 — round 13: protocol boundaries and named-set census` |
| 880 | `### Round-13 closure — measured content revision` |
| 917 | `## 2026-10-20 — round 14: U5 boundaries and regular source targets` |
| 987 | `### Round-14 closure — committed measurement and correction record` |
| 1071 | `## 2026-10-20 — round 15: U6 diagnostic route and an honest safety stop` |
| 1127 | `### Round-15 committed measurements and final author verdict` |
| 1162 | `## 2026-10-20 — round 16: source-only learning after rejected-harmed closure` |
| 1204 | `### Round-16 verification correction — M6` |
| 1219 | `### Round-16 final evidence and handoff` |

Non-round LOG headings, for completeness (also unique as whole lines):
`# mado-shokunin — Iteration Log` (l.1),
`## 2026-10-15 — fleet round-1: admitted-corpus navigation` (l.440),
`## 2026-10-15 — fleet round 1 interactive cutover: candidate retained, dispatch blocked` (l.484),
`## 2026-10-15 — fleet round 1 candidate durability and committed measurement` (l.582),
`## 2026-10-15 — fleet round 1 reproducibility erratum: caller-selected revision` (l.609),
`## 2026-10-16 — protocol conformance: SCORECARD contract fields` (l.642),
`## 2026-10-17 — README: Devin wiki link` (l.762).

**There is no round-17 LOG heading yet**: `grep -cE '^#+ .*round 17' LOG.md`
→ `0`; same 0 for `Round 17`, `Round-17`, `round17`.

## Evidence — exact lesson headings

`corpus/lessons/round-16.md` (H1 is on line 3; lines 1–2 are blank):

| Line | Exact heading |
|---|---|
| 3 | `# Round 16 — source-only Waybar boundary and host-safety learning` |
| 10 | `## Mistakes` |
| 34 | `## Gate` |
| 86 | `## Boundaries and handoff` |
| 97 | `## Observed verification and round disposition` |

`corpus/lessons/round-16-verifier-spotcheck.md`:

| Line | Exact heading |
|---|---|
| 3 | `# Mado round 16 — independent closure: admitted` |
| 21 | `## Step-1 conformance` |
| 40 | `## Per-claim re-check` |
| 112 | `## Per-axis verdicts` |
| 131 | `## Discernment spot-check (LEARNING.md)` |
| 151 | `## Trend verdicts` |
| 162 | `## Routed defects (mado, next authorized round)` |

Per-claim labels inside `## Per-claim re-check` are **bold lines, not
headings** (e.g. l.42 `**C1 coverage — documented custom-module observation
route U7, 6/7 → 7/7.**`; l.87 `**C3 calibration — original literal
lesson-citation fraction, 12/20 → 14/22.**`). A pointer to them must quote the
bold label, not just "C3" — in that file C3 is *calibration*, not
operability.

Other lesson H1s that round-17 may cite (exact, per file — the forms are not
uniform; copy, do not normalize):

- `# Round 15 — input layer boundaries, receipt precision and a host-safety failure`
  (`corpus/lessons/round-15.md:1`), with
  `### Tool transaction and process evidence` (:24),
  `## Gate` (:51), `### Committed measurement and verification receipts` (:159).
- `# Round 14 — output/colour boundaries and regular source targets`
  (`round-14.md:1`); `# Round 13 — bounded protocol knowledge and exact-set
  diagnostics` (`round-13.md:1`); `# Round 12 lessons — mado-shokunin
  (2026-10-19)` (`round-12.md:1`).
- Spotchecks: `# round-12 — non-author verification and spot-check
  (orchestrator, kaika)` (lowercase `round`, hyphen); `# Round 13 —
  independent verification and source spot-check`; `# Round 14 — independent
  verification and discernment spot-check`; `# Mado round 15 — independent
  closure: rejected-harmed`.

Planned round-17 lesson (does not exist yet): `corpus/lessons/round-17.md`
with `# Round 17 — <subtitle>` and `## Mistakes`; the QUALITY anchor for M1 is
therefore `#mistakes` (lowercase slug), consistent with criteria 6–22. Do not
spell `round17.md`, `Round-17.md`, or `#Mistakes`.

## Required spelling set for the round-17 report

For each likely citation target, use exactly:

1. R16-V1 lineage → `LOG.md` §"Round-16 verification correction — M6"
   **and** `corpus/lessons/round-16.md:131` at baseline `27cd06f` with the
   line quoted (`  Input tamper control returns **2 snapshot_tampered**,
   retained in`). The heading alone is not enough; the defect is
   line-and-revision specific.
2. Round-16 closure context →
   `LOG.md` §"2026-10-20 — round 16: source-only learning after rejected-harmed closure",
   and either H3 closure pointer above by its full text.
3. R15-V1 / pause →
   `LOG.md` §"2026-10-20 — round 15: U6 diagnostic route and an honest safety stop"
   and §"Round-15 committed measurements and final author verdict";
   lesson `corpus/lessons/round-15.md` §"Tool transaction and process evidence"
   for the libinput transaction.
4. R16-V2 / M4–M5 →
   `corpus/lessons/round-16-verifier-spotcheck.md`
   §"Routed defects (mado, next authorized round)" (this section carries
   R16-V1, R16-V2 and R15-V1).
5. C1 criterion citation → `lessons/round-17.md#mistakes M1` (plus the
   outside pointer `lessons/round-16-verifier-spotcheck.md R16-V1`, or the
   full section heading from item 4).
6. C2 declared rubric anchor → `SCORECARD.md` §"Round 17 — declared claims
   (2026-10-20)" (exists now, unique; line 821).
7. Report "LOG entry" column → quote the committed entry heading verbatim.
   The heading L1 must write is:
   `## 2026-10-20 — round 17: <subtitle>` (lowercase `round`, space, colon,
   U+2014). Until that line exists, cite the SCORECARD anchor in item 6; never
   invent or abbreviate the LOG entry.
8. Commit/claim context, if cited → `SCORECARD.md` H2s are unique only in
   full: `## Round 16 — declared claims (2026-10-20)`,
   `## Round 16 — committed results and bounded author verdicts`,
   `## Round 17 — declared claims (2026-10-20)`. Bare `## Round 16` matches
   two headings.

## Measured failure of the wrong spellings (the label check)

Heading-only and total counts in `LOG.md`:

```text
pattern            headings  total
round16            0         1     # only prose, l.1242 "in round16 evidence"
Round16            0         0
round 16           1         4     # heading + 3 prose (ll.1167,1173,1184)
Round-16           2         2     # the two H3s; bare form is ambiguous
round-16           0         3     # prose only (ll.1166,1173,1184)
Round 16           0         0
round 17           0         0
Round 17           0         0
Round-17           0         0
Round-16 closure   0         0     # no such heading
Round-15 closure   0         0     # no such heading
```

Check that must be shown to fail, then pass only with the full heading:

```sh
# fails (0): the round-16 conformance note's spelling does not resolve to a heading
grep -cE '^#+ .*round16' LOG.md            # 0
grep -cE '^#+ .*Round16' LOG.md            # 0
# passes (1): the exact H2
grep -Fxc '## 2026-10-20 — round 16: source-only learning after rejected-harmed closure' LOG.md  # 1
```

Label check on the lesson line (C1's target), read-only at the baseline:

```sh
git show 27cd06f:corpus/lessons/round-16.md | sed -n '131p'
# => "  Input tamper control returns **2 snapshot_tampered**, retained in"
```

A checker of the form "cited token == receipt outcome token" must fail for
`lesson round-16.md:131` + `.ufo/waves/round-16/evidence/frozen-tampered.json`
(that receipt records `measured_commit` 9dcf248, exit 2, `frozen_error`, detail
"expected.json pair 1/'denied_executable:sudo' is unreachable"), and pass only
for `evidence/action-selftest-final.json` (`SELFTEST PASS
frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered`,
`measured_commit` 1e31681, exit 0). This seat re-read the lesson line at
`27cd06f` and both receipt JSON files directly; the drafts' claims match.

## Adjacent finding outside LOG/lesson (do not mispointer C2)

`PROVINCE.md` has **one** heading — `# mado-shokunin — Province` — and no
`P1`–`P6` headings or labels (`grep -nE '\bP[1-6]\b' PROVINCE.md` → no
matches). The P1–P6 names exist only in
`SCORECARD.md` §"Round 17 — declared claims (2026-10-20)"; PROVINCE's
equivalent prose is line 9, `declared files, screen/idle behavior
(hypridle/hyprlock where present).` A round-17 report must not cite
`PROVINCE.md § P6`; cite the SCORECARD anchor plus `PROVINCE.md:9` (or the
quoted phrase).

## Risks / limits

- The separator in every date/title heading is U+2014 (`—`), not `-` or
  `–`; a hyphen copy silently fails an exact match. `Round-16` is a hyphen
  only because that is how the two H3s are written.
- `## Mistakes` occurs in 5 lesson files and `## Gate` in 8; a lesson H2
  pointer is never unique without the file name.
- LOG line numbers are stable only while LOG is append-only. Round-17 will
  append at the tail, so l.656–1242 stay valid; for cross-revision claims
  cite `HEAD:path:line` at the named commit, not a bare line.
- The spelling set above is a *transcription* of the current tree. If L1 edits
  a heading while integrating, the report must re-copy it, not reuse this
  table. No heading was edited by this seat.
- `round 16` and `Round-16` each match more than one line; only the full
  heading line is unambiguous.

## Verification performed (all read-only)

- `grep -n '^#' LOG.md` and repr/codepoint checks of every heading above;
  U+2014 confirmed on all em-dash separators.
- `grep -Fxc` whole-line counts = 1 for every exact heading listed.
- Variant matrix above (`grep -Fc`, `grep -cE '^#+ …'`).
- Read-only `git log --oneline -4`, `git show --stat 0175f13`, and
  `git show 27cd06f:corpus/lessons/round-16.md | sed -n '131p'`.
- Read `corpus/QUALITY.md` criteria 6–22 (anchor convention), the round-17
  drafts (`LessonDraft.md`, `QualityDraft.md`, `ReportSkeleton.md`), and
  `corpus/lessons/round-16-verifier-spotcheck.md` routed-defects section.
- No test, build, lint, package, service, compositor, input or screenshot
  command was run. No tool was installed.
