# R67RevLanding — adversarial review of C2 (round 67, wave 1)

Reviewer seat: R67RevLanding. Scope: the frozen C2 claim
(`.ufo/waves/round-67/claims-declaration-r67.md`, commit 061dc329). All runs in
`/fast/scratch/hyaku/mado-r67/R67RevLanding/*` (removed before yield). Lane
untouched except this report file. No tools installed. Child invocations used a
GIT_*-scrubbed env (`PATH/HOME/TMPDIR/LC_ALL` only) per L1's masking warning.

## Drafts reviewed (sha256)
- `w1/R67ExecLanding/draft/quality/landing-counters.sh` — `4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9`
- `w1/R67ExecChildren/draft/quality/counters/c3-r56-used-by.py` — `f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f` (base+1 line: `"GIT_NO_REPLACE_OBJECTS": "1",`)
- `w1/R67ExecChildren/draft/quality/check-tool-ledger.py` — `1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb` (base+1 line: `env["GIT_NO_REPLACE_OBJECTS"] = "1"`)
- `w1/R67ExecChildren/draft/tools/mado-receipt-citecheck.py` — `3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0` (base+key `GIT_NO_REPLACE_OBJECTS="1"` in the ls-tree env)
- `w1/R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py` — `26523d116885fc806011fe277fc01bfe2d6247922d84231244206982ad573138`

## Check 1 — frozen M-Z recipe kills the draft instrument; restore green
Recipe: delete `[ "$citations" -gt 0 ] && ` once (needle count in draft: 1).
- `bash mz.sh --selftest --scratch-root stB` → **rc 1 (killed)**. Firing assertions:
  `SELFTEST FAIL 43: citecheck zero citations refused want=2 got=0`,
  `FAIL 45: zero-citation guard occurs exactly once want=1 got=0`,
  `FAIL 46: zero-citation guard sits inside marker_valid want=1 got=0` (59/62).
  Mutant sha256 `a6255a00262cc2f1790f813927dd5fa8ed9910e74d1ec19a8662e88df0fe0118`.
- Restore (unmutated draft): `--selftest` → **rc 0, 62/62**.

## Check 2 — is the new `zero` shim case what kills M-Z? (kill matrix)
- A draft as-is → rc 0 (62/62). B draft+M-Z → rc 1 (zero case fires, above).
- C zero case removed, inventory kept (`f0e0efe2256b3627e7749e164a5de63a7ad9c4204e03c4b9c6a47aa1d5a29413`) → rc 0 (60/60): removing the case does not break the green path.
- D case removed + M-Z (`14f48c6f124db028ac816d428bbfa63cd99215eb7ec71fcc9cea5968cf2736b8`) → **rc 1**, killed by the structural inventory assertions only (`guard occurs exactly once`, `sits inside marker_valid`).
**Finding (note, not defect):** the M-Z kill is overdetermined. The frozen Z scenario (zero-citation marker must force non-green) is genuinely present and fires (B#43, want=2 got=0 — i.e. with the guard deleted the zero marker yields GREEN rc 0), but the two guard-inventory assertions kill M-Z independently. Frozen kill rule (nonzero on exact mutant, zero on unmutated) holds in every composition.

## Check 3 — frozen M-R recipe on the child guard
Recipe: delete the added `GIT_NO_REPLACE_OBJECTS` env key line (usedby child; mutant sha256 `68b34e3c…` ≡ base bytes, as expected — the guard is the only diff).
- Module-level, identical fixture+override: draft `check()` → rc 0 `TARGET_MET`; mutant → rc 1 `TARGET_MISSED missing=4` (reads forged registry blob under planted `refs/replace`).
- Script-form against a scratch clone of the lane at 061dc329 (blob replace on `freeze:corpus/SOURCES.md`, all 372 used-by cells blanked): draft → **rc 0 `TARGET_MET`** (reads real); mutant → **rc 1 `TARGET_MISSED missing=414`** (reads forged).
- L1's tree shape on the citecheck child (real tree lacks `corpus/docs/target.md`; root-tree replacement adds it): before replace draft=mutant=rc 1 `TARGET_MISSED missing=1`; after replace draft **stays rc 1 MISSED** (real), mutant → **rc 0 `TARGET_MET resolved=1 missing=0`** (forged) — exactly the hazard the control credits as a kill (`forged_credit` in the counter).

## Check 4 — baseline soundness: base child reads forged on the same fixture
Base bytes (0b28ffb4 `c3-r56-used-by.py`) on the blob fixture: real → rc 0 `TARGET_MET`; with planted blob replace → **rc 1 `TARGET_MISSED missing=4`** (`BASE_CHILD_READS_FORGED=True`). Git layer under the child's own env shape: unguarded `cat-file` returns forged bytes, `GIT_NO_REPLACE_OBJECTS=1` returns real bytes (`UNGUARDED_READS_FORGED=True`, `GUARDED_READS_REAL=True`). The frozen baseline line `child_env_read=forged guarded_read=real` is reproducible at the actual child layer, not only at the git layer. **The R control is sound; the baseline claim stands.**

## Check 5 — green-path invariance
- Ledger child selftest: draft rc 0 54/54; base rc 0 54/54.
- Citecheck child selftest: draft rc 0 12/12; base rc 0 12/12.
- Draft instrument selftest: rc 0 62/62.
- Real four-leg landing at 061dc329 with the draft tree (draft instrument + draft children, scratch-assembled): **rc 0 GREEN** — nav `indexed=78/78 coverage=10.0000/10`, usedby `entries=78 rows=372 … TARGET_MET`, ledger `population=108 ledger_rows=108 … TARGET_MET`, citecheck (explicit clean scope `.ufo/waves/round-65/receipts`) `files=8 citations=10 resolved=10 … TARGET_MET`. Default round-67 scope is infeasible at the freeze (`citecheck path missing: …/round-67/receipts`, rc 2 setup) because the receipts dir does not exist yet — named, not a verdict change.

## Check 6 — public behavior restrictions
- External citecheck paths refused: `--citecheck-paths /etc` → rc 2 `citecheck paths must be inside repository for dirty guard`.
- `--round` required: rc 2 `--round N required (positive integer)`.
- Exit map unchanged: GREEN=0 (real run), RED=1 / ERROR=2 (selftest matrix: red/crash/skip/duplicate per leg, 62/62).
- Child output not renamed: all diffs vs base touch only the guard lines and the selftest shim's new zero branch; `MADO_USED_BY:`/`LEDGER:`/`MADO_CITECHECK:` formats and citecheck `VERSION r64-v1` unchanged.
- Layer binding (L1's point, confirmed): the citecheck tool **alone** prints `citations=0 resolved=0 missing=0 … TARGET_MET rc 0` for a missing/empty scope; the zero-citation refusal binds **only at the instrument `marker_valid` layer** (assertion 43), which is where the frozen Z control binds.

## Counter itself (`c2-r67-landing-controls.py`)
- `--selftest` → rc 0, `45/45 assertions passed`.
- At the freeze (pre-cutover): rc 1, `selftest=0 mz=fail mr=fail killed=0/2 baseline=0/2 verdict=TARGET_MISSED` — matches the frozen baseline semantics; no false green on the do-nothing tip.
- End-to-end candidate measurement (scratch repo committing the four draft files at their canonical paths, rev `d50af44b8dde4d6bf15db0f3f0a15b854c9d2364`): rc 0, `selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET`. Its R control targets the citecheck child with the tree-replacement fixture and `child_env` with inherited `GIT_*` scrubbed — consistent with my independent reproduction.

## Verdict
**C2 control set: SOUND as bounded.** Both frozen mutants are killed by the candidate controls and by the counter end-to-end; the unmutated candidate stays green everywhere; the base child demonstrably reads forged bytes, so the baseline (killed=0/2) is honestly stated; public behavior and the exit map are unchanged. M-Z's kill is overdetermined (zero case + inventory assertions) — within the frozen kill rule. Notes for L1: (1) the usedby child's own selftest is cwd-dependent — 15/16 rc 1 with cwd outside the lane vs 16/16 inside, failing assertion silent (no FAIL line); identical on base bytes, pre-existing, not part of the C2 predicate (the instrument selftest shims the children and is cwd-independent); (2) the counter can only measure committed revisions — my candidate run used a scratch fixture repo, so the landed TARGET_MET must be reproduced at the lane rev post-integration.

Cleanup: my importlib byproduct `w1/R67ExecChildren/draft/quality/counters/__pycache__/` (created 21:35:46, from loading their draft) removed; sibling drafts otherwise untouched. Scratch removed before yield.
