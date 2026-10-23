# AtkNoHarm — registered no-harm guards at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`

Lane: mado-shokunin (jj-colocated), range `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` → `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`.
All git invocations pinned both revisions explicitly and ran with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset; no write commands, no working-tree mutation. Tooling directive: no installs were needed; nothing installed or updated.

## Guard results

### G1 — `tools/` byte-identity
Command: `git diff --quiet 8e5d9369… 39c5963… -- tools/` → exit 0.
No tracked file under `tools/` differs between base and tip; production instruments untouched.

**VERDICT: holds**

### G2 — r23 C3 counter stays 0
Command: `python3 -I .ufo/waves/round-23/c3/count.py 39c5963…` → `"count": 0`, exit 0.
All five tracked tools (`mado-action-plan.py`, `mado-assessment.py`, `mado-evidence-audit.py`, `mado-tripwire.py`, `mado-verify.sh`) are accounted for by PROVINCE.md table rows; SHONEN box 4 asserted (`- [~]`). Counter v2, reads committed bytes only.

**VERDICT: holds**

### G3 — r23 C2 counter stays 3/3
Command: `python3 -I .ufo/waves/round-23/c2/count.py 39c5963…` (single run, `timeout 900`; counter is `git show`-only, no recursion) → `"count": "3/3"`, exit 0.
foot 8 rows, kitty 9, ghostty 8 resolve against committed SOURCES/note bytes at the pinned rev.

**VERDICT: holds**

### G4 — Sources census exit 0
Command, from the fleet root as registered: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, `mado ok …/corpus/SOURCES.md`.
Only W04 warnings (6 rows: S030/S042/S045/S097/S119/S120/S121 duplicate URL across scopes); per the script contract ("exit 0 clean or warnings") these do not affect the verdict. Script self-describes as read-only.
Caveat (bounded): the census walks the on-disk working tree, which sits one commit ahead (`87429be6`, "round-24: lesson 24 … late wave-1 reports"). That commit touches only `.ufo/waves/round-24/**` bookkeeping, `LOG.md` (+25) and `corpus/lessons/round-24.md`; `git diff --stat 39c5963… 87429be6 -- corpus/SOURCES.md corpus/README.md` is empty, so the census result is valid for the tip's registry.

**VERDICT: holds**

### G5 — numstat removals 0 on guarded files
Command: `git diff --numstat 8e5d9369… 39c5963… -- SCORECARD.md corpus/SOURCES.md LOG.md PROVINCE.md corpus/QUALITY.md`:

```
29	0	SCORECARD.md
6	0	corpus/QUALITY.md
16	0	corpus/SOURCES.md
```

LOG.md and PROVINCE.md: absent from the diff (byte-identical in range). Removal column is 0 for all five; the registration's in-place SOURCES-cell exception is not even exercised (no removed lines anywhere). The single SCORECARD hunk (`@@ -1555,3 +1555,32 @@`) is one appended section, `## Round 24 — registration and C2 re-demonstration (2026-10-23)`; nothing historical was rewritten.

**VERDICT: holds**

### G6 — r12 navigation counter (SCORECARD `### Counting command` fence)
Method: fence extracted from committed bytes (`git show 39c5963…:SCORECARD.md`), run unmodified via `bash -s` with `REV=39c5963…` from the lane root.
Fence sha256: `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — byte-identical at base and tip (instrument unchanged; matches the sha prefix recorded in SCORECARD's own round-1 rubric row).
Output at tip: `indexed=36/39 missing=3 dangling=0 duplicates=0 coverage=9.2308/10`, **exit 1**; missing: `knowledge/terminal-trees-r23.md`, `knowledge/tripwire-binding-boundaries-r21.md`, `knowledge/tripwire-lifetime-recovery-r22.md`.
Same fence at base `8e5d9369…`: `indexed=35/38 missing=3` (same three), exit 1.
Interpretation: exit-1 is pre-existing at the round base, not caused by the round; the wave strictly improves navigation (the new `rule-attribution-r24.md` is indexed, satisfying C1's coverage-map clause) and introduces no dangling or duplicate rows. As a no-harm guard this passes; as an absolute exit-0 check it does not pass at either revision.

**VERDICT: holds (no-harm sense)** — delta vs base non-negative, instrument byte-identical; absolute exit-0 not met at base or tip (pre-existing).

## Overall

All six checks: **no harm attributable to round 24 wave 1 in range `8e5d9369… → 39c5963…`.** The five registered guards hold at the tip; the r12 navigation counter shows no regression (and one improvement) with its exit-1 gap pre-dating the round.

## Residual risk

1. Navigation index has 3 long-standing holes (r21/r22/r23 notes, including the r23 C2 capability note `terminal-trees-r23.md`). Pre-existing and outside round-24's registered guards, but any future "index complete, exit 0" claim will fail until they are routed.
2. Census W04 duplicate-URL-across-scopes warnings (7 rows listed) are contract-clean today; a future tightening of W04 into an E-code would flip this guard.
3. Census is disk-based: its result is pinned to the working tree only while `corpus/SOURCES.md` stays identical to the tip (verified true against `87429be6`; re-verify if the tree moves again before closure).
4. r23 C2/C3 counters read committed bytes only — they validate registry/table structure at the rev, not live re-fetch of source URLs (by design; re-fetch is r24 C1's counted mode).

## Verification gaps

- r23 C2 counter run exactly once (single-shot constraint); it is deterministic over committed bytes, so no variance expected.
- Did not re-open S153–S168 source bytes, C1 claim rows, or the round-24 control receipts — those are sibling seats' scope.
- The 3 missing navigation entries were not traced to the commits that introduced them (pre-base provenance asserted from the base-run result only).
