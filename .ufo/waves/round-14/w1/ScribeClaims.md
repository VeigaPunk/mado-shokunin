# ScribeClaims — round 14 (mado-r14-w1): measurement/evidence matrix draft

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Seat: ScribeClaims (scribe, leaf, no delegation).
Status: **draft; no verdict issued; no claim admitted.** Every row not marked OBSERVED is UNRUN or PREDICTED.

## 0. Checks this seat ran (read-only only)

| Command / read | Result |
|---|---|
| `git rev-parse HEAD` | `873ff081b2ac363df771261b0ed950cba50d8988` |
| `git cat-file -t 95cbc41fe5d5db121b89c2ddd1f953728663c5f4` | `commit` |
| `git log --format='%h %cI %s' 95cbc41..HEAD` | `59cfbdc` "round-13: record committed measurements and verdicts"; `873ff08` "round-13 verifier spot-check (integrator, hyaku): non-author admit/reject". Diffs not inspected. |
| `git status --short` | `A` round-14 `evidence/census-before.txt`, `dispatch.json`, `reports/swarm-registry.json`, `spec.json`; `M SCORECARD.md` (+28 lines) |
| `git diff -- SCORECARD.md` | adds the Round 14 declared-claims block (see §2) |
| Read: `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-13.md`, `corpus/lessons/round-13-verifier-spotcheck.md` (lines 203–205), `.ufo/waves/round-13/measure.py`, `.ufo/waves/round-14/w1/spec.json`, `dispatch.json` | read only |
| Read: `tools/mado-verify.sh` via grep for `sources_resolve`, `compgen -G`, `EXPECT`, regression markers | anchors only; no execution |
| Read: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` header (lines 1–47) | present; modes census/validate/overdue/shared/selftest; exits 0/1/2/3 |
| Read: `.ufo/waves/round-14/evidence/census-before.txt` | retained output, exit 0 (not re-run) |

Not run by this seat: the census command (exit taken from the retained file only), `--selftest`, `--no-live`, `--live`, `--regression`, `frozen/verify.py`, `measure.py` (file does not exist yet), `receipt.py` (not yet created), builds, lint, formatters, tests, live probes, mutations, and any sibling or host config. No commits, no pushes, no installs or updates (tooling directive considered; nothing needed for a read-only draft).

## 1. Axes and scope

- **coverage** (C1): sourced current-art ground, U1–U7 joins. Lowest non-retired scored axis at baseline.
- **operability** (C2): regular-source-target subset of `hypr.root.sources_resolve`.
- Harm-watch only (not scored here): navigation, hermetic selftest, `--no-live` file plane, `--regression`, frozen companion, source census.
- Not claimed: depth, adjacency, calibration, freshness (no round-14 claim); feature behaviour of any output/colour protocol; HDR; kernel input.

## 2. Declared claims

Source: uncommitted `SCORECARD.md:457–483` (`## Round 14 — declared claims (2026-10-20)`), cross-checked against `spec.json` item Change texts.

- **C1 coverage:** U1–U4 4/7 = 5.7143/10 → U1–U5 5/7 = 7.1429/10 by admitting one substantive U5 output-management/colour boundary note citing opened primary S047 (wlr-output-management) and S048 (color-management-v1) with reciprocal `mined` joins. No feature exercise; unknown behaviour retained.
- **C2 operability:** three isolated directory-shaped cases — direct directory, all-directory glob, mixed file/directory glob — each must fail the owning `hypr.root.sources_resolve` row naming the non-regular target, with overall exit 1. Target 0/3 → 3/3. Clean and order-swapped controls are preservation checks, not score.
- Revision-bound counter per SCORECARD: `python3 .ufo/waves/round-14/measure.py <revision>` (not yet created).
- Verifier corrections R13-V1..V3 are "lesson-backed corrections within these claims", not a third axis claim.

Pre-registration gap: the Round 14 block is **not yet committed** (working-tree diff only). Round 12 and round 13 committed their declared claims before baselines. Commit the block before any baseline measurement, or the baseline will not be pre-registered.

## 3. Known baseline (prior records; not re-observed by this seat)

| Item | Value | Where recorded |
|---|---|---|
| Last measured content commit | `95cbc41fe5d5db121b89c2ddd1f953728663c5f4` (2026-10-20) | `SCORECARD.md:369` |
| Current HEAD | `873ff081…`, two commits after 95cbc41 | `git log` (§0) |
| C1 U1–U4 | 4/7 → 5.7143 | `SCORECARD.md:334–335`, `:387–390` |
| C1 U4 facets | 3/3 | `SCORECARD.md:390` |
| Navigation | 27/27, missing/extra/dup 0 | `SCORECARD.md:394` |
| C2 four-case named-set | 4/4 → 10.0000 (finite subset only) | `SCORECARD.md:390` |
| Overall failing runs (round 13 before) | 3/4 already | `SCORECARD.md:390`; `lessons/round-13.md:68–70` |
| Selftest | 310/310, exit 0 | `SCORECARD.md:396–397` |
| File plane `--no-live` | 29 PASS, FAIL+UNKNOWN 0, exit 0; 8 live SKIPs | `SCORECARD.md:399–401` |
| Regression | 10/10 KILLED, spec `c7ee75b9…`, re-cut `87910c39…`; covering 8/8 | `SCORECARD.md:402–405` |
| Frozen companion | `frozen_match`, exit 0; selftest 12/12 | `SCORECARD.md:406–409` |
| Gate SHA-256 (round-13 committed) | `037b05dcd3f86e12…` | `SCORECARD.md:410–411` |
| Source registry | 46 rows: A42/B1/C3; mined 34 / queued 8 / rejected 4 | `SCORECARD.md:427–429` |
| S047/S048 | absent at HEAD; registry ends at S046 (`corpus/SOURCES.md:58`) | read this seat |
| Census (before, retained) | `validate --root … mado`, exit 0; W04 S030, S042, S045; `ok` | `.ufo/waves/round-14/evidence/census-before.txt` |
| Gate source resolver | `sources_resolve` block `tools/mado-verify.sh:2404–2437`; glob ≥1-match via `compgen -G` at `:2422` | grep this seat |
| Gate regression pin comment | `:2346–2347` (pin is re-cut by L1, never edited to match) | grep this seat |

Baseline caution: the round-13 numbers were measured at `95cbc41`. The round-14 baseline must be measured at the pinned round-14 revision. This seat did not inspect the diffs of `59cfbdc` or `873ff08`; their subjects suggest record-only changes, but that is `[INFERENCE]`.

## 4. Measurement / evidence matrix

Status key: **UNRUN** = no command has run for this row. **PREDICTED** = expectation from documents or code reading, not measured. **PRIOR** = recorded value from an earlier commit, not re-observed. **GAP** = no owner or value pinned.

| ID | Claim / sub-axis | Measure (command or anchor) | Baseline | Target / expectation | Status | Owner seat (per spec) | Evidence path (proposed) |
|---|---|---|---|---|---|---|---|
| M1 | C1 coverage U1–U4 | `measure.py <rev>` (U-join count) | 4/7 = 5.7143 | re-measure at pinned rev | PRIOR → UNRUN | MeasureBuild | `.ufo/waves/round-14/evidence/before.txt` |
| M2 | C1 U5 sourced entry | count of `corpus/knowledge/*.md` with `source:` naming a `mined` A/B row, `covers: U5`, `verified-at:`, `recheck:` in first 15 lines | 0 (no U5 note; README and lesson say U5 open) | 1 → 5/7 = 7.1429 | UNRUN | ScribeFrontier drafts wording; note author seat not pinned | `…/evidence/after.txt` |
| M3 | C1 U5 body facets | body read: output-management facet, colour facet, feature-unknown facet each present | none | 3 facets, feature unknown explicit | UNRUN (no note) | note author; reviewer | — |
| M4 | C1 S047 row | `corpus/SOURCES.md` `## Registry` row, 13 cells, tier A, status `mined`, anchor = revision + section, used-by = U5 note path | absent (registry ends S046, line 58) | present | UNRUN | OutputSpec (source), SourceInventory (collision) | `corpus/SOURCES.md` |
| M5 | C1 S048 row | as M4 for color-management-v1 | absent | present | UNRUN | ColourSpec | `corpus/SOURCES.md` |
| M6 | C1 reciprocal join | note `source:` cites S047+S048; each row's `used-by` lists note path | — | both directions | UNRUN | MeasureBuild | `…/after.txt` |
| M7 | C1 navigation | `corpus/README.md` coverage-map row for U5 note; navigation counter | 27/27 (`SCORECARD.md:394`) | 28/28, exit 0 | PREDICTED on row addition; UNRUN | note author / L1 | `…/after.txt` |
| M8 | C1 frontier wording | `corpus/README.md:93–94` still lists "output management" as open | open | updated in the same change as the note | GAP until edited | ScribeFrontier draft; L1 applies | `corpus/README.md` |
| M9 | C1 feature exercise | none | — | not claimed; unknown retained in note | N/A by design | — | — |
| M10 | C2 direct directory (replaces `ai-usage.conf`) | `sources_resolve` row for that case | PREDICTED PASS today (existence-style check; the directory check at `:2404–2437` was not read in full by this seat — GateRecon owns the exact anchor) | FAIL, detail names the non-regular target and basename | UNRUN | GateImplement (gate), MeasureBuild (fixture) | `…/evidence/c2-direct.txt` |
| M11 | C2 all-directory glob | `compgen -G` at `:2422` treats any ≥1 match as satisfied | PREDICTED PASS today | FAIL naming the directory match(es) | UNRUN | same | `…/evidence/c2-glob-dir.txt` |
| M12 | C2 mixed file/directory glob | as M11 with one regular match | PREDICTED PASS today | FAIL naming the directory | UNRUN | same | `…/evidence/c2-glob-mixed.txt` |
| M13 | C2 overall exit per case | overall gate exit printed separately from the row | — | exit 1 for M10–M12 | UNRUN | MeasureBuild | `…/evidence/c2-*.txt` |
| M14 | C2 controls (clean, order-swapped) | selftest-isolated fixtures | not scored | clean exit 0 / order preserved | UNRUN | MeasureBuild | `…/evidence/c2-controls.txt` |
| M15 | C2 overlap with `hypr.local.inventory` | local-inventory row on the direct-directory fixture | SCORECARD says local inventory "may already detect" | reported separately, not double-counted | UNRUN | MeasureBuild | `…/evidence/c2-direct.txt` |
| M16 | C2 score formula | `10 × cases-with-stable-named-diagnostic ÷ 3` is implied by "0/3 → 3/3" | — | formula not pinned in SCORECARD | GAP | L1 pins before run | `SCORECARD.md` |
| M17 | C2 literal diagnostic token | measure counts FAIL rows containing "non-regular" plus basename | — | exact token not pinned anywhere | GAP | GateImplement + MeasureBuild must agree | `tools/mado-verify.sh`, `measure.py` |
| M18 | C2 symlink policy | `-f` follows symlinks, so a symlink to a regular file passes and a symlink to a directory fails | — | policy stated in the report | GAP (round 13 said directory/symlink policy not claimed) | ParserIntent, GateRecon | report §policy |
| M19 | Harm: selftest | `bash tools/mado-verify.sh --selftest` | 310/310 (`SCORECARD.md:396`) | N/N, exit 0, count may grow with new cases | UNRUN | L1 | `…/evidence/selftest.txt` |
| M20 | Harm: file plane | `bash tools/mado-verify.sh --no-live` | 29 PASS, 0 FAIL, 0 UNKNOWN | unchanged or explained | UNRUN | L1 | `…/evidence/file-plane.txt` |
| M21 | Harm: regression | `--regression` | 10/10 KILLED against pin `87910c39…` / spec `c7ee75b9…` | pin mismatch expected after gate edit; L1 re-cuts; label as re-cut owed, not harm | PREDICTED fail-until-recut; UNRUN | L1 (pin owner) | `…/evidence/regression-recut.txt` |
| M22 | Harm: frozen companion | `.ufo/waves/round-13/frozen/verify.py` | `frozen_match` | refuses on changed gate SHA-256 by design | PREDICTED mismatch; UNRUN; re-freeze owner GAP | L1 | `…/evidence/frozen.txt` |
| M23 | Receipt (R13-V3) | `receipt.py --selftest`: match, mismatch → exit 2, exit propagation, stable ids | no receipt exists | 4 assertions green | UNRUN | ReceiptBuild | `…/evidence/receipt-selftest.txt` |
| M24 | Census (required) | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exit 0, W04 S030/S042/S045, `ok` (`census-before.txt`) | exit 0; new rows add no E-codes; W04 only for retained historical rows | UNRUN (after-run) | L1 | `.ufo/waves/round-14/evidence/census-after.txt` (proposed name) |
| M25 | R13-V1 correction | U4 note statement "retained S041 data is only registry interface/version headers" (`lessons/round-13-verifier-spotcheck.md:203`) | uncorrected | append-only erratum in the U4 note | OPEN; no seat's Change applies it | BoundaryPrecision drafts; ReviewResolver verifies; L1 assigns | `corpus/knowledge/wayland-protocol-boundaries-r13.md` (append) |
| M26 | R13-V2 correction | within-run boundary (`gate-file-plane.txt:47`) vs cross-revision output equality (`lessons/round-13.md:72–73`) | "byte-identical before/after" wording ambiguous | separate the two in errata text | OPEN | BoundaryPrecision; ReviewResolver | same as M25 + lesson |
| M27 | R13-V3 correction | standalone selftest receipts carry revision/digest; `gate-selftest.txt` lacks its own header | no retroactive claim | future receipts only (ReceiptBuild); old receipt labelled | OPEN for future; status-neutral | ReceiptBuild | `…/receipt.py` |
| M28 | Pre-registration | Round 14 block committed before baseline | uncommitted (`git status`: `M SCORECARD.md`) | committed | UNRUN / not satisfied | L1 | `SCORECARD.md` |
| M29 | Baseline pin | `measure.py` revision argument | HEAD `873ff08`; prior `95cbc41` | one pinned revision recorded in SCORECARD and evidence headers | GAP until pinned | L1 | `SCORECARD.md`, `evidence/before.txt` |

## 5. Unrun checks, labelled

Every check in §4 with status UNRUN is unrun. In addition, these are unrun by design for this seat:

- `validate`, `census`, `overdue`, `shared` and `selftest` modes of `scripts/sources-census.sh`. The census exit is taken from the retained `census-before.txt` only; it is recorded here as `[RETAINED]`, not re-observed.
- `measure.py`, `receipt.py`, `regular-target.spec` (not yet created).
- Gate runs: `--selftest`, `--no-live`, `--live`, `--regression`, any `--snapshot` mode.
- Frozen verification (`frozen/verify.py`).
- Any mutation or fixture run in an isolated temp root.

## 6. Required source-census sections and exact paths

1. **Census command and retained exit.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`. Before-run retained: `.ufo/waves/round-14/evidence/census-before.txt` (exit 0). After-run: `.ufo/waves/round-14/evidence/census-after.txt` (proposed; follows the before-file's name). Required exit: 0. E-codes must be absent; W04 only for the retained historical S030/S042/S045 rows.
2. **`corpus/SOURCES.md` `## Registry`** (table header at line 11; last row S046 at line 58). Append S047 and S048 rows, 13 pipe-separated cells each (E01). Ids `S\d{3,}` (E02). Unique id (E03). URL+scope must not duplicate an existing row without a `supersedes` link (E04). `kind` enum (E05), `tier` enum with community never A (E06, E10), `status` enum (E07), `opened` past or present ISO date (E08), `recheck` valid (E09), `used-by` path must exist on disk (E11). Rows must sit inside `## Registry` (E12).
3. **`corpus/SOURCES.md` `## Paths`** (line 60). Add a U5 route line, as U4 did at round 13.
4. **`corpus/SOURCES.md` `## Search log`** (line 76). Add a round-14 bounded-search entry listing question, identified/screened/included/excluded counts, and stop rationale. Do not invent counts.
5. **`corpus/SOURCES.md` `## Leads (unopened)`** (line 142). Leads only, never rows.
6. **U5 knowledge note** (new; name not pinned by any seat — see G5). Header keys within the first 15 lines: `source:` (must cite S047/S048), `covers: U5`, `verified-at:`, `recheck:`. Body: output-management facet, colour facet, feature-unknown facet, and the S047/S048 located quotes (≤25 words each).
7. **`corpus/README.md`**: one coverage-map row for the U5 note (table at lines 10–38) so navigation reaches 28/28; update the Frontier bullet at lines 93–94 so "output management" is no longer listed as open.
8. **`corpus/lessons/round-14.md`** (new; proposed). Use the `round-13.md` structure: `## Mistakes` (table), `## Gate` (`### Candidate decisions`, `### Opened sources and located quotes`, `### Registry mutations — old → new`, `### Advisory review and outside spot-check`), `## Exercised verification (L1, after all seats finished)`.
9. **U4 note append-only erratum** for R13-V1 and R13-V2: `corpus/knowledge/wayland-protocol-boundaries-r13.md`. Append only; do not rewrite the round-13 verifier record `corpus/lessons/round-13-verifier-spotcheck.md`.
10. **`SCORECARD.md`**: Round 14 declared block at lines 457–483 (uncommitted; commit before baseline). Afterwards append `## Round 14 — committed measurements and author verdicts` on the round-13 pattern (`SCORECARD.md:367–423`).
11. **`LOG.md`**: round-14 entry (not yet present in this seat's read).

## 7. Required report sections and exact paths

- `.ufo/waves/round-14/w1/reports/ScribeClaims.md` (this seat's rendered report; Report trailer).
- `.ufo/waves/round-14/w1/ScribeClaims.md` (this file, findings).
- `.ufo/waves/round-14/w1/reports/` for the other seats' rendered reports.
- Final L1 report should carry, in order: axes; declared claims with pinned revision; baseline table with source lines; measurement matrix with UNRUN/PREDICTED/PRIOR labels; census before/after with exit codes; harm watch (selftest, file plane, regression re-cut, frozen re-freeze, navigation); R13-V1..V3 disposition; gaps G1–G13; tool records (none so far).

## 8. Gaps, contradictions and owner actions

- **G1 Pre-registration uncommitted.** `SCORECARD.md:457–483` is working-tree only. Owner: L1. Action: commit before baseline.
- **G2 C2 score formula unpinned.** Owner: L1. Action: state `10 × n ÷ 3` (or other) in SCORECARD before measurement.
- **G3 Literal diagnostic token unpinned.** The measure counts "non-regular"; no seat pins the exact FAIL detail string. Owner: GateImplement and MeasureBuild jointly; L1 arbitrates.
- **G4 Symlink policy unpinned.** `-f` follows symlinks. Round 13 said directory/symlink policy is not claimed. Owner: ParserIntent and GateRecon outputs; L1 states the policy in the report.
- **G5 U5 note filename unpinned.** No seat's Change names it. `measure.py` discovers by header, so the name does not block the counter, but the row `used-by` and README row need it. Owner: L1 pins before the note lands.
- **G6 README frontier stale.** `corpus/README.md:93–94` says output management is still open; this becomes false once the note lands. Owner: ScribeFrontier draft; L1 applies in the same change.
- **G7 Pins go stale by design.** `GateImplement` edits the gate, so the round-13 regression pin (`87910c39…`) and frozen gate SHA (`037b05dc…`) will not match. The gate forbids editing pins before L1 re-cut. Owner: L1. Action: re-cut regression; re-freeze or label frozen verify. Label the mismatch as owed, not as harm.
- **G8 Navigation requires a README row.** Without it, navigation stays 27/27 while a note exists unindexed; the navigation counter would then report a missing row. Owner: L1.
- **G9 R13-V1..V3 application unassigned.** BoundaryPrecision drafts erratum text; ReviewResolver verifies. No seat's Change applies the text to the U4 note. Owner: L1 assigns.
- **G10 Baseline inheritance.** Round-13 values are at `95cbc41`; HEAD is `873ff08`. Owner: MeasureBuild measures at the pinned revision; do not carry 27/27, 310/310, 29/29 forward unmeasured.
- **G11 Order of writes.** `used-by` must point to an existing file (E11), so the U5 note must exist before its S047/S048 rows are marked `mined` or the census fails. Owner: L1 orders the commit.
- **G12 Collision check.** S047/S048 URLs are unverified against existing rows (E04/W04). Owner: SourceInventory (scout).
- **G13 Feature behaviour.** The U5 note must not claim advertised output or HDR behaviour; EvidenceChain's three-row table is the guard. Owner: EvidenceChain.

## 9. Tool records

None installed or updated by this seat. No `pacman`, `uv`, `cargo`, or `npm` action taken.
