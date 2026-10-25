# RevReportShape — report-shape attack, mado round 35 (wave 2)

Seat: `L1Mado35.RevReportShape`. Mode: read-only. Wrote only under
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/RevReportShape/` plus this report.
Tool installs: **none** (pure `python3` stdlib + coreutils).

Target: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-35/mado.md`
(the fleet path; `.../mado-shokunin/../.ufo/reports/round-35/mado.md` resolves to the same file).

## Axes attacked

- A1 section presence and order (prompt §4 lines 99–120).
- A2 one evidence pointer per section (prompt §4 lines 104–119).
- A3 marker rule: placeholder text, missing required sections, no evidence pointers (lines 121–124).
- A4 report extras: canonical `Stale-lane` line and tool installs (lane-addendum.md:196).
- A5 SHONEN line parity against the lane's own `SHONEN.md` boxes (line 118).

## Behavior

The target does not exist. I therefore could not review report text; I verified the absence four
independent ways, and — so the finding is actionable rather than a bare "file missing" — built a
shape checker that encodes the contract and calibrated it until it both passes and fails correctly.

## Gates (command and exit code)

Absence — run 2026-10-25T03:36 -03, re-checked 03:38:13 (still `test -f` exit 1),
transcript `scratch/RevReportShape/absence.out`:

| # | Command | Result |
|---|---|---|
| 1 | `test -f /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/mado.md` | **exit 1** |
| 2 | `git -C /home/vgpnk/Projects/shokunin log --oneline --all -- .ufo/reports/round-35/mado.md \| wc -l` | **0** (never committed on any ref) |
| 3 | `git -C /home/vgpnk/Projects/shokunin ls-files .ufo/reports/round-35/` | exit 0, 8 lanes (chousa, kake, kama, kotodama, kumitate, mori, tameshi, tsukuroi) — **mado absent** |
| 4 | `cat /home/vgpnk/Projects/shokunin/.ufo/state/mado.report-baseline` | `35 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — that digest is `sha256` of the **empty byte stream** (`printf '' \| sha256sum`, verified), i.e. the driver's own record that the round-35 report was missing at attempt-2 launch |
| 5 | `grep -c 'lane-dead-no-report mado round=35' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | **1** (attempt 1, 03:23:08); attempt 2 launched 03:23:38 |

Mechanical predicate — `scripts/shokunin-watchdog.sh:140-163` (`report_of`) and `:302-318`
(`report_sources_conformance`), transcribed into the checker:

- `report_of`: `[ -f "$f" ] || return 1` → **fails on line 148 before any other test**. If a file
  were present at the same path, `:151-155` would still require its digest to differ from the
  empty-stream baseline (`35 e3b0c442…b855`), so an empty or unchanged file can never close the round.
- Remaining `report_of` clauses: a SHONEN heading or `**SHONEN**` list marker, and
  `wc -c >= MIN_REPORT_BYTES` (default 400, `:54`).
- `report_sources_conformance`: for a child lane, requires a `^#{1,6}\s+Sources\s*&\s*frontier`
  heading; absence is logged as `sources-conformance-defect`, which is a conformance defect and
  **not** a relaunch trigger (`:302-306`).

Shape checker — `scratch/RevReportShape/check-report-shape.py`, run with `python3 -I`:

```
python3 -I .ufo/waves/round-35/scratch/RevReportShape/check-report-shape.py \
  /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/mado.md --shonen SHONEN.md
→ DEFECT A.exists: report absent or unreadable: [Errno 2] No such file or directory
→ SHAPE_DEFECTS defects=1      exit 1
```

Calibration, transcript `scratch/RevReportShape/matrix-final.out` (6 SHAPE_OK, 6 SHAPE_DEFECTS —
a checker that cannot pass is worthless, so both directions are shown):

| Report | Verdict | Why |
|---|---|---|
| `round-34/mado.md` (lane precedent) | SHAPE_OK exit 0 | positive control |
| `round-35/kama.md` | SHAPE_OK exit 0 | sibling, in-band round |
| `round-35/tameshi.md` | SHAPE_OK exit 0 | sibling |
| `round-35/mori.md` | SHAPE_OK exit 0 | sibling, bold `**Stale-lane**:` / `**Tool installs**:` labels |
| `round-35/tsukuroi.md` | SHAPE_OK exit 0 | sibling, `Tool installs:` mid-line |
| `round-35/chousa.md` | SHAPE_OK exit 0 | sibling |
| **`round-35/mado.md`** | **SHAPE_DEFECTS exit 1** | absent |
| `round-33/mado.md` | SHAPE_DEFECTS exit 1 | genuine: `Stale-lane` line is `none. Respawn-per-round. No round 34 was started.` — canonical clause missing |
| fixtures/neg-placeholder | 3 defects | `TODO` at line 8, missing pointer, no stale line |
| fixtures/neg-nopointer | 6 defects | every section pointer-free |
| fixtures/neg-order | 1 defect | SHONEN hoisted above Work performed |
| fixtures/neg-shonen-2 | 1 defect | 2 SHONEN lines vs 4 `SHONEN.md` boxes |

Two calibration corrections were made during the run and are recorded, not hidden: the first
draft's stale-line regex rejected tameshi/mori (bold decoration) and its tool-installs regex
rejected tsukuroi (label not at line start). Both were regex faults on my side; fixed, then the
six positive controls pass. Their initial output is in `scratch/RevReportShape/matrix.out`.

## Defect list (target report only; nothing edited)

**D1 — BLOCKING, marker rule.** The report artifact is absent: `test -f …` exit 1, never committed
on any ref, and the driver's baseline is the empty-stream digest. Under prompt §4 lines 121–124 a
report with missing required sections other than *Sources & frontier* and *Trend verdicts* "counts
as the round **failed**"; here every section is missing, so the exemption clause cannot apply.
If this state stands at round end, the round fails and is relaunched.

**D2 — A1, `Work performed` missing.** Must open by naming the round's 1–3 declared claims and
their target axes/capability (line 104), then one bullet per work item with a path:line, command
output, or commit hash.

**D3 — A1, `Landed changes` missing.** Must tie every change to a `LOG.md` entry **and** the commit
hash carrying it (line 107).

**D4 — A1/A2, `Before → after measurements` missing.** Must carry one row per claim with the
counting command and the commit measured against (line 109).

**D5 — A1/A2, `Sources & frontier` missing.** Conformance item, not a marker predicate
(watchdog `:302-318`). Content owed: `SOURCES.md` rows before→after with the counting command, rows
added by tier, rows touched old→new, frontier rows advanced (line 111).

**D6 — A1/A2, `Trend verdicts` missing.** Conformance item. Owed: one verdict each for
`expansion`, `quality`, `discernment` ∈ {improved, harmed, unchanged, unprovable-but-better}, with
evidence and no scalar (line 116).

**D7 — A1/A2, `SHONEN` missing.** Owed: one line per box of `mado-shokunin/SHONEN.md` (4 boxes),
`[x]` only with a named non-author verifier, `[~]` with a resolvable pointer, `[ ]` if untouched
(line 118). The checker's parity test is `J.shonen`, currently 0/4.

**D8 — A2/A3, zero evidence pointers.** The marker rule names "no evidence pointers" as a failure
condition (line 121). Because the file is absent, the whole artifact contributes none.

**D9 — A4, report extras missing.** No canonical `Stale-lane` line and no tool-install record.
The canonical sentence required is `Stale-lane: respawn-per-round driver; no other mission of this
lane is open.` — the same sentence, bold decoration aside, in
`round-35/{kama,mori,tsukuroi,chousa,tameshi}.md`; the lane's own precedent `round-34/mado.md:274`
carries it with a leading `none — `. Tool installs must be stated even when none
(lane-addendum.md:196).

**D10 — A3, placeholder clause is undecidable, not satisfied.** With no bytes there is no
placeholder to find; a later write must be re-checked with `G.placeholder` before the claim
"no placeholder text" can be made.

Derived, not independent: D2–D10 all follow from D1. They are listed separately because each is a
separate acceptance item the write must satisfy, and each has its own checker code.

## Pre-write risk found in this wave (affects the future report's pointers)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` lists `?? .ufo/waves/round-35/` at the
**fleet root**, containing one file:
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-35/w2/reports/RevLogEvidence.md` (16 K tree, 1 file).
The lane's wave-2 evidence lives at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/w2/reports/`,
so this is a seat misroot of exactly the kind prompt §3 describes ("a relative path such as
`.ufo/waves/...` lands in the FLEET repo").

Why it is a report defect and not just tidiness: if the round report cites `.ufo/waves/round-35/w2/reports/RevLogEvidence.md`
as an evidence pointer, that path resolves under the fleet root, is untracked, and can never be
committed by `jj-lane.sh commit … -- <lane-relative path>` (§4 commit order, and the report must
cite lane hashes). The report's misroot-sweep line would also be false if it claims the fleet root
is clean. Fix belongs to the L1 (copy byte-exact into the lane path, `cmp`, delete the fleet copy,
record under `## Mistakes`); this seat is read-only and did not touch it.

## Known limits of this check

- The checker is mine, not the driver's. Its two driver-derived predicates are transcribed from
  `scripts/shokunin-watchdog.sh:140-163` and `:302-318`; its §4 predicates are regexes over headings,
  pointers, verdict tokens and placeholders. It proves **shape**, never claim truth or that a cited
  commit carries the cited bytes.
- The evidence-pointer detector accepts path:line, a path with a code/doc extension, a 7–40 char
  hex run, a backticked span, or a `S###` registry id. Prose-only evidence ("Census exit 0",
  "two reviewers agreed") is not counted as a pointer, which is stricter than §4's wording and can
  produce a false defect if the L1 writes evidence without naming an artifact.
- SHONEN parity is a box count against `SHONEN.md`, not a judgment that each `[x]` has a genuine
  named non-author verifier — that stays a reviewer duty.
- The checker cannot see that a report was written *after* the lane tip it cites; that temporal
  check is out of scope here.

## Out of scope

Claim truth, the frozen counters' TARGET_MET outputs, `SOURCES.md` row content and quote fidelity,
sibling-lane report defects (round-33's stale line is recorded above only as checker calibration),
and any edit of the report, the lane corpus, or the fleet repo.

## Touched surfaces

- Created: `mado-shokunin/.ufo/waves/round-35/scratch/RevReportShape/check-report-shape.py`,
  `…/matrix.out`, `…/matrix-final.out`, `…/absence.out`, `…/fixtures/{neg-placeholder,neg-nopointer,neg-order,neg-shonen-2}.md`.
- Created: this file, `mado-shokunin/.ufo/waves/round-35/w2/reports/RevReportShape.md`.
- Read only: the fleet report tree, `.ufo/state/mado.report-baseline`, `.ufo/watchdog.log`,
  `scripts/shokunin-watchdog.sh`, `scripts/hyaku/lane-addendum.md`, `.ufo/prompts/mado-round-35.md`,
  six reports, five `SHONEN.md` files.
- Not modified: the target report (absent, not created), any lane corpus file, counters, controls,
  `SOURCES.md`, the fleet repo, any sibling lane.

## Acceptance the L1 can run after the write

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/RevReportShape/check-report-shape.py \
  /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/mado.md --shonen \
  /home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md
```
Expect `SHAPE_OK defects=0` exit 0, plus `wc -c` ≥ 400 and a digest differing from
`e3b0c442…b855` (both already inside the checker via `B.size`; the digest half is the driver's).
