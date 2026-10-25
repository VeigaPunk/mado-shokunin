# MutPtrNoSetup — mutation-tester report (mado round 36 wave 1)

## Assignment
> Mutate the C2 gate in /tmp: remove the `setup_ok` conjunct from the verdict. Show that a tree with no round-36 sections then exits 0 (the absence-is-a-pass defect the gate was built to prevent), with the exit code.

## Mutant
Single behavior-bearing change in a scratch copy of the gate: the `setup_ok` conjunct is removed from `met` (the verdict boolean). In the current production bytes this is line 196 of `quality/check-evidence-pointers.py` (`setup_ok` inside the `met = (...)` tuple, lines 195–202); after the edit `met` reads:

```python
    met = (
        dangling35_closed == 1
        and len(dangling36) == 0
        and inherited_dirty == 0
        and scratch_disposition_ok == 1
        and tip_axis_transcript == 1
    )
```

The exact edit hunk (third hunk of `diff -u production scratch`): `- setup_ok` / `- and dangling35_closed == 1` replaced by `+ dangling35_closed == 1`. The other two diff hunks (docstring clause about superseded `old`-side pointers; `superseded_old` exclusion in `dangling36`) are NOT mine — the production gate changed on disk while my probe ran (a sibling builder is iterating; see Evidence note 1). Both probe generations were run against the file bytes current at that moment, and the finding is identical in both.

## Method
1. Read the gate and its frozen spec (`C2/frozen.json`, `PRED-C2-r36-v1`).
2. Built a minimal synthetic git repo at `/tmp/mutptrnosetup/repo` (base commit `c231affa2fe128db31593e9bd055d06f40c42933`, tip = HEAD of `master`) whose tree satisfies every observable EXCEPT the round-36 section presence the `setup_ok` conjunct checks:
   - `LOG.md` has a `## Round 35` section (no `## Round 36`), citing the two superseded pointers `.ufo/waves/round-35/scratch/SimplifyCounter/` and `.ufo/waves/round-35/scratch/MutC1Drop/mutants/`, and both resolve as tracked files.
   - `SCORECARD.md` has a `## Round 35` section (no `## Round 36`).
   - `corpus/lessons/round-36.md` exists and names the scratch disposition `tracked paths=2`.
   - `quality/receipts/axis-c231affa2fe128db31593e9bd055d06f40c42933.txt` exists with `MADO_AXIS: rev=c231affa… mismatched=0`.
   - No file under the ten `INHERITED_PATHS` (clean `git status --porcelain`).
3. Ran the pristine gate and the mutant on the same tree (`--repo /tmp/mutptrnosetup/repo --rev master --branch master`), captured exit codes.
4. Ran the mutant on a second synthetic branch `r36tip` that ALSO has Round-36 sections (control: mutant still passes a fully-met tree).
5. Restored exact pristine bytes and re-ran (restoration evidence).

## Results

### Pristine gate on the no-round-36 tree (baseline)
```
PRED-PTR-r36-v1 rev=master pointers_r35=2 dangling_r35=0 dangling_r35_closed=1 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=2 scratch_disposition_ok=1 tip_axis_transcript=1 setup=missing-r36-sections verdict=TARGET_MISSED
tip_axis: quality/receipts/axis-c231affa2fe128db31593e9bd055d06f40c42933.txt@c231affa2fe128db31593e9bd055d06f40c42933
EXIT=1
```

### Mutated gate on the SAME no-round-36 tree (defect shown)
```
PRED-PTR-r36-v1 rev=master pointers_r35=2 dangling_r35=0 dangling_r35_closed=1 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=2 scratch_disposition_ok=1 tip_axis_transcript=1 setup=missing-r36-sections verdict=TARGET_MET
tip_axis: quality/receipts/axis-c231affa2fe128db31593e9bd055d06f40c42933.txt@c231affa2fe128db31593e9bd055d06f40c42933
EXIT=0
```

The gate itself still prints `setup=missing-r36-sections` — it *knows* the sections are absent — yet with the conjunct removed the verdict flips to `TARGET_MET` and exit code 0. This is exactly the absence-is-a-pass defect the gate was built to prevent (frozen predicate: "Absence is never a pass: missing round-36 sections print `setup=missing-r36-sections`, force `TARGET_MISSED` and exit 1").

### Control: mutant on the fully-met tree (has Round-36 sections) — still exits 0
```
PRED-PTR-r36-v1 rev=r36tip pointers_r35=2 dangling_r35=0 dangling_r35_closed=1 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=2 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
EXIT=0
```
Confirms the mutant is a minimal removal, not a global always-pass.

## Verdict
**KILLED.** The detector (the gate itself) distinguishes pristine from mutant on the no-round-36 tree: pristine exits 1 (`TARGET_MISSED`), mutant exits 0 (`TARGET_MET`), Identical environment, identical tree, only the `setup_ok` conjunct differs. The `setup_ok` conjunct is load-bearing for the absence-is-a-pass invariant.

## Evidence
1. **Production bytes changed mid-probe.** First gate copy (sha256 `74ce7a05d2360ddf7d135fa2a6997c0cbaa48bd6989e4d06603d11fe1dfd2a53`) matched production at copy time; a later `diff -u` showed production had meanwhile gained a docstring clause and the `superseded_old` exclusion in `dangling36` (production sha256 now `d1ba71e96715c3f7ce04a0b2e1758a3cc782884b6fa919db96107e01cb2d59dc`). `git status --porcelain -- quality/check-evidence-pointers.py` printed nothing: the change is committed, not a dirty working tree. I re-baselined on the current bytes (`/tmp/mutptrnosetup/gate2.py`, sha256 `d1ba71e9…`, identical to production) and re-ran both generations; the finding and the exit codes are identical. The `setup_ok` conjunct is present at line 196 in current bytes.
2. **Hashes** — first generation: pristine `74ce7a05…`, mutant `e3b9fbfb12bfacb37e17a45f88bb004bd6676e9978d86d3786a0f7f00a44fdd6`. Second generation: pristine `d1ba71e9…`, mutant at run time `83E5` snapshot; restoration verified.
3. **Restoration** — after the mutant run, `cp production gate2.py` restored exact pristine bytes (sha256 `d1ba71e9…` matches production again), and the restored gate on the no-round-36 tree exits 1 (`TARGET_MISSED`) — the same output as the baseline. Production file was never modified (work only in `/tmp/mutptrnosetup/`).
4. **File pointers** — verdict tuple `quality/check-evidence-pointers.py:195-202` (current bytes), `setup_ok` computation `:137-141`, con- `:196`. Diff hunk for the edit: `@@ -193,8 +190,7 @@` (first generation) / `@@ -196,8 +…` context (second generation), removing `setup_ok` and its `and`.
5. **No tools installed** (no new binaries; only `cp`/`diff`/`sha256sum`/`git` already present).
6. **Synthetic fixture** lives at `/tmp/mutptrnosetup/repo` (base `c231affa…`, tip = HEAD); no writes anywhere under LANE except this report.
