# ScribeClaims — round 14 (mado-r14-w1) rendered report

Status: **draft; no verdict; no claim admitted; no check run except read-only observation.**
Findings: `.ufo/waves/round-14/w1/ScribeClaims.md` (full matrix, anchors and gap list).
Baseline HEAD observed: `873ff081b2ac363df771261b0ed950cba50d8988`. Last measured content commit in SCORECARD: `95cbc41fe5d5db121b89c2ddd1f953728663c5f4`.

## 1. Behaviour

Scribe role only. No source, gate, registry or note was edited. Writes: this report and the findings file.

## 2. Axes and declared claims

- **C1 coverage** (lowest non-retired scored axis): U1–U4 4/7 = 5.7143 → U1–U5 5/7 = 7.1429 by one sourced U5 output-management/colour boundary note citing S047 and S048 with reciprocal `mined` joins. No feature exercise. Source: uncommitted `SCORECARD.md:457–483`.
- **C2 operability**: three isolated directory-shaped `hypr.root.sources_resolve` cases (direct directory, all-directory glob, mixed glob) fail with the named non-regular target and overall exit 1. 0/3 → 3/3 is a prediction; baseline not yet run. Clean and order-swapped controls are preservation checks, not score.

## 3. Evidence matrix (condensed)

Full table with owners and proposed evidence paths: findings §4.

| Group | Rows | Status |
|---|---|---|
| C1 coverage (U1–U4 re-measure, U5 join, U5 facets, S047/S048 rows, reciprocal joins, navigation 27→28) | M1–M9 | UNRUN; navigation row PREDICTED on addition |
| C1 frontier wording (`corpus/README.md:93–94`) | M8 | GAP until edited |
| C2 cases (direct, all-directory glob, mixed glob), per-case overall exit, controls, local-inventory overlap | M10–M15 | UNRUN; baseline PREDICTED only |
| C2 score formula, literal diagnostic token, symlink policy | M16–M18 | GAP (unpinned) |
| Harm watch (selftest 310/310, file plane 29/29, regression 10/10 pin, frozen `frozen_match`) | M19–M22 | UNRUN; regression and frozen mismatch PREDICTED after gate edit, to be labelled re-cut owed |
| Receipt (R13-V3) selftest | M23 | UNRUN; no receipt file exists |
| Source census (validate, exit 0 retained) | M24 | UNRUN after-run; before-run retained only |
| R13-V1 / V2 / V3 corrections | M25–M27 | OPEN; no seat's Change applies the errata |
| Pre-registration commit, baseline revision pin | M28–M29 | not satisfied / GAP |

Prior values (27/27 navigation, 310/310 selftest, 29/29 file plane, 10/10 regression, 4/4 four-case subset) were measured at `95cbc41`. They are not re-observed here and are not carried forward as current.

## 4. Unrun checks (labelled)

- Census `validate` and other modes of `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`: unrun by this seat. Exit 0 is read from `.ufo/waves/round-14/evidence/census-before.txt` (retained).
- `measure.py`, `receipt.py`, `regular-target.spec`: not created yet; unrun.
- Gate `--selftest`, `--no-live`, `--live`, `--regression`, `--snapshot`: unrun.
- `.ufo/waves/round-13/frozen/verify.py`: unrun.
- Any fixture or mutation run: unrun.

## 5. Required source-census sections and exact paths

1. Census command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`. Before: `.ufo/waves/round-14/evidence/census-before.txt`. After (proposed): `.ufo/waves/round-14/evidence/census-after.txt`. Required exit 0; no E-codes; W04 only for S030, S042, S045.
2. `corpus/SOURCES.md` `## Registry` (header line 11; last row S046 line 58): append S047 and S048, 13 cells each.
3. `corpus/SOURCES.md` `## Paths` (line 60): add U5 route.
4. `corpus/SOURCES.md` `## Search log` (line 76): round-14 bounded-search entry with counts actually observed.
5. `corpus/SOURCES.md` `## Leads (unopened)` (line 142): leads only.

## 6. Required knowledge, index, lesson and report sections

- U5 note, new, filename unpinned: header within 15 lines with `source:` (S047/S048), `covers: U5`, `verified-at:`, `recheck:`; body facets for output management, colour, and feature-unknown; located quotes ≤25 words.
- `corpus/README.md`: coverage-map row (lines 10–38) for the U5 note; update Frontier lines 93–94.
- `corpus/lessons/round-14.md` (new, proposed): `## Mistakes`; `## Gate` with `### Candidate decisions`, `### Opened sources and located quotes`, `### Registry mutations — old → new`, `### Advisory review and outside spot-check`; `## Exercised verification (L1, after all seats finished)`.
- `corpus/knowledge/wayland-protocol-boundaries-r13.md`: append-only erratum for R13-V1 and R13-V2. Do not rewrite `corpus/lessons/round-13-verifier-spotcheck.md`.
- `SCORECARD.md`: Round 14 declared block at lines 457–483 (commit it first); later `## Round 14 — committed measurements and author verdicts`.
- `LOG.md`: round-14 entry.
- `.ufo/waves/round-14/w1/reports/`: rendered reports for every seat, including this one.

## 7. Gaps and owner actions

- **G1** Round 14 declared block uncommitted. Owner L1: commit before baseline.
- **G2** C2 score formula not pinned (implied `10 × n ÷ 3`). Owner L1.
- **G3** Literal FAIL token ("non-regular") not pinned in gate or measure. Owner GateImplement + MeasureBuild; L1 arbitrates.
- **G4** Symlink policy (`-f` follows symlinks) not stated. Owner ParserIntent / GateRecon; L1 states it in the report.
- **G5** U5 note filename not named by any seat. Owner L1.
- **G6** `corpus/README.md:93–94` still lists output management as open. Owner ScribeFrontier draft; L1 applies with the note.
- **G7** Regression pin `87910c39…` and frozen gate SHA `037b05dc…` will mismatch after the gate edit by design. Owner L1: re-cut regression; re-freeze or label frozen verify. Not harm.
- **G8** Navigation needs a README row for the U5 note, or the counter reports a missing row. Owner L1.
- **G9** R13-V1..V3 application unassigned: BoundaryPrecision drafts text; ReviewResolver verifies; no seat applies it. Owner L1 assigns.
- **G10** Baseline inheritance: round-13 values are at `95cbc41`, HEAD is `873ff08`. Owner MeasureBuild: measure at the pinned revision.
- **G11** Write order: U5 note must exist before S047/S048 rows are `mined` (census E11). Owner L1.
- **G12** S047/S048 URL collision check unverified (E04/W04). Owner SourceInventory.
- **G13** U5 note must not claim advertised output or HDR behaviour. Owner EvidenceChain.

## 8. Tool records

No tools installed or updated by this seat.
