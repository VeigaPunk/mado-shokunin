# MutPtrDisposition — round-36 C2 gate disposition equality-drop mutation probe

Date: 2026-10-25. Seat: mado leaf (w1), mutation-tester, lane-bound. Scope: one
mutation probe on the C2 gate `quality/check-evidence-pointers.py`
(`PRED-PTR-r36-v1`) — drop the `tracked paths=N` equality in the scratch
disposition clause so that any mention of `.ufo/waves/round-35/scratch` passes.
The mutant and the fixture repo live under `/tmp/mutptrdisposition/` (assignment
declares the /tmp copy as the mutation target; `/tmp` is in scratch scope). The
committed production gate was never modified: `git status --porcelain --
quality/check-evidence-pointers.py` is empty; sha256 `d1ba71e96715c3f7ce04a0b2e1758a3cc782884b6fa919db96107e01cb2d59dc`
(before and after). Mutant copy sha256 `af4e7d041cdcfe24557e228ee2936dce53f9194e4d7c58bef19d5dd3facb2189`.

## Mutant

One exact-string replacement. `DISPOSITION` regex remains defined but unused.

```diff
--- quality/check-evidence-pointers.py
+++ /tmp/mutptrdisposition/check-evidence-pointers.mutant.py
     scratch_disposition_ok = 0
     for line in lesson.splitlines():
         if ".ufo/waves/round-35/scratch" in line:
-            m = DISPOSITION.search(line)
-            if m and int(m.group(1)) == scratch_count:
-                scratch_disposition_ok = 1
-                break
+            scratch_disposition_ok = 1
+            break
```

## Detector

Same bounded detector on pristine and mutant bytes: `python3 -I <gate> --repo
/tmp/mutptrdisposition/repo --rev HEAD --branch master`, cwd = fixture repo root.
Exit 0 = TARGET_MET, 1 = TARGET_MISSED.

Baseline on the real lane (read-only, honest gate): `PRED-PTR-r36-v1 rev=HEAD
pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0
inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1
setup=ok verdict=TARGET_MET` rc=0.

## Fixture repo (`/tmp/mutptrdisposition/repo`)

Two commits on `master`: (1) seed commit whose `HEAD` sha1 becomes the axis-rev;
(2) all gate-relevant records. Committed tree:

- `LOG.md` — `## Round 35` section cites the two superseded pointers
  `.ufo/waves/round-35/scratch/SimplifyCounter/` and
  `.ufo/waves/round-35/scratch/MutC1Drop/mutants/`; `## Round 36` section carries
  the D5 correction pairs (old → new, new sides resolve: files committed under
  `scratch-evidence/SimplifyCounter/`, `scratch-evidence/MutC1Drop/mutants/`).
- `SCORECARD.md` — same relative-35/36 sections.
- `corpus/lessons/round-36.md` — D8 disposition line naming the scratch path with
  the **wrong count** `tracked paths=7` (actual tracked at the revision: 10).
- `quality/receipts/axis-453c2cdcb4d2a4f270100f7a849ff1d524461684.txt` —
  `MADO_AXIS: mismatched=0 rev=453c2cdcb4d2a4f270100f7a849ff1d524461684`; the
  axis sha is an ancestor (the seed commit).
- Ten `.ufo/waves/round-35/scratch/` files (8 under `probe/`, 1 under
  `RevQuoteS203/`, 1 under `RevQuoteS205/`) → `scratch_tracked=10`; statuses of
  the INHERITED_PATHS committed and clean → `inherited_dirty=0`.

Every non-disposition observable is at target, so the fixture isolates the
disposition clause.

## Results — honest vs mutant, verbatim

Scenario A (wrong count present, `tracked paths=7` vs 10):

```text
=== HONEST ===
PRED-PTR-r36-v1 rev=HEAD pointers_r35=2 dangling_r35=2 dangling_r35_closed=1 pointers_r36=4 dangling_r36=0 inherited_dirty=0 scratch_tracked=10 scratch_disposition_ok=0 tip_axis_transcript=1 setup=ok verdict=TARGET_MISSED
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: quality/receipts/axis-453c2cdcb4d2a4f270100f7a849ff1d524461684.txt@453c2cdcb4d2a4f270100f7a849ff1d524461684
rc=1
=== MUTANT ===
PRED-PTR-r36-v1 rev=HEAD pointers_r35=2 dangling_r35=2 dangling_r35_closed=1 pointers_r36=4 dangling_r36=0 inherited_dirty=0 scratch_tracked=10 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: quality/receipts/axis-453c2cdcb4d2a4f270100f7a849ff1d524461684.txt@453c2cdcb4d2a4f270100f7a849ff1d524461684
rc=0
```

Scenario B (no count field at all — "any mention" extreme):

```text
=== HONEST (no count field) ===
PRED-PTR-r36-v1 rev=HEAD pointers_r35=2 dangling_r35=2 dangling_r35_closed=1 pointers_r36=4 dangling_r36=0 inherited_dirty=0 scratch_tracked=10 scratch_disposition_ok=0 tip_axis_transcript=1 setup=ok verdict=TARGET_MISSED
… rc=1
=== MUTANT (no count field) ===
PRED-PTR-r36-v1 rev=HEAD pointers_r35=2 dangling_r35=2 dangling_r35_closed=1 pointers_r36=4 dangling_r36=0 inherited_dirty=0 scratch_tracked=10 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
… rc=0
```

## Verdict

**MUTANT SURVIVED** — coverage finding, not a contract change. The honest gate
rejects a disposition carrying a wrong count (`scratch_disposition_ok=0` →
TARGET_MISSED, rc=1); the equality-drop mutant accepts it
(`scratch_disposition_ok=1` → TARGET_MET, rc=0), flipping the verdict on the same
fixture bytes. The mutant also accepts a disposition with no `tracked paths=`
field at all, so the kill is not just an off-by-one: the clause now reduces to a
substring presence test. The `tracked paths=N` equality is therefore load-bearing
for the disposition observable — a wrong count in the disposition line cannot be
distinguished from a correct one without it.

## Restoration evidence

Production file untouched: `git status --porcelain -- quality/check-evidence-pointers.py`
prints nothing (rc=0); sha256 before and after `d1ba71e96715c3f7ce04a0b2e1758a3cc782884b6fa919db96107e01cb2d59dc`.
The mutant lives only at `/tmp/mutptrdisposition/check-evidence-pointers.mutant.py`
(disposable scratch, per assignment). Fixture repo at `/tmp/mutptrdisposition/repo`
(current `HEAD` = scenario-A fixture; scenario B is an extra commit, test-only).
No lane file was written outside this report; no tool installs were needed.
