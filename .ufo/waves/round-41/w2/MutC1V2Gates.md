# Seat MutC1V2Gates — w2 — COMPLETE

Attack: the v2 C1 counter's own gates. 26 single-edit mutants of
`quality/counters/c1-r41-globals-v2.py` (frozen DATA 07f26416 blob, byte-identical to the
worktree before and after — sha256 `59e117d8…4c3a63`, `git status` clean on the path) scored
with the committed runner `run-c1-v2-controls.py`. Baseline first: pristine counter = **97/97
correct** (FULL suite, `logs/BASELINE-pristine-full.log`, rc 0). No tracked lane file was
edited; mutants live in the seat dir. Tooling installed: none.

## Result: 10 KILLED (2 degenerate) · 16 SURVIVED

**Killed, with the controls that notice:** V2G02 nproc-lead-drop → K04+M14 (2/2); V2G07 b2
dropped → M39 (2/2); V2G10 NAME_DENY "globals" → K09 (2/2); V2G11 NAME_DENY "__file__" →
K10 (2/3, third draw confirmed; the MISSED draw is the b2 nonce lottery); V2G13 g
import-gate off → C3-cheat-socket-import (2/2, its only detector); V2G17 stub FIFO-check
dropped → M11 (2/2); V2G18 run_piped stdin=DEVNULL → M11 (2/2); V2G21 met ignores clauses →
K05/K06/K08/K09/K10/C1-C4 (2/2); degenerate: V2G03 (journal `if True:` dead-branches the
stub build → P-reference fails 2/2, direct run 33/39 with six `program_ran=False want=True`)
and V2G14 (TOTAL assert crash → P-reference 2/2).

**Survived — no committed control notices (16):** sandbox-prereq check off (V2G01); `ran`
assertion off (V2G04); rc5 accepted for rc2 (V2G05); clause b3 off (V2G06); forced-site rule
off (V2G08); NOT_SITES loosened (V2G09); NAME_DENY "getattr" off — double-covered by the
sys.modules rule (V2G12); MIN_SELFTEST 50→10 (V2G15); clause-b k==n off (V2G16);
gen_sessions_check off (V2G19); ambient GIT_* passthrough (V2G20); fifo0 timeout 20→3600
(V2G22); KILL_NEED 4→2 (V2G23); BASE-lacks-tool precondition off (V2G24); b2/b3 gate
`if cl["b"]` off (V2G25); constant nonce (V2G26). Scope of each survivor claim is its named
battery (P- plus the mechanistically-relevant families, matrix has the per-row argument);
the pristine 97/97 baseline rules out verdict-channel effects.

## Findings for the round

1. **Redundancy is load-bearing in both directions.** The `ran` gate and the
   no-plaintext-journal rule each hide the other's absence: in V2G03's world K02
   (cwd-replay) still MISSED *only* via `program_ran` (log line cited in matrix note 1), and
   V2G04 (ran off) survives because M12's failure rides on rc/stdout. No committed control
   isolates the `ran` gate; a two-edit mutant freeing both would pass K02.
2. **b3 is redundant for the committed controls** (V2G06 survived): b2's flipped copies are
   `ast.unparse`d, so K07's self-fingerprint dies inside b2 already.
3. **Sole-detector map:** M11 is the only detector for *both* stdin gates (V2G17, V2G18);
   C3 the only detector of the import allow/deny gate (V2G13); K09/K10 the only detectors of
   their NAME_DENY entries; M39 the only detector of b2-as-a-whole and blind to KILL_NEED 4→2
   (V2G23 survived — the threshold is untested on (0,4)).
4. **v1 survivor classes still uncovered in v2:** BASE half of clause a (V2G24 = w1 S05),
   ambient GIT_* (V2G20 = w1 S03), nonce freshness (V2G26 = w1 S04), clause-b loosening
   (V2G15/V2G16 ≈ w1 S02). No new detectors were added for them.
5. **The suite has a per-run flake:** one K1-family draw gave MISSED for K10 via b2's
   nonce-chosen teeth failing on a reference-shaped tool — that nonce would flip
   P-reference too (w1 measured ~2/22 full-suite; one instance in 3 draws here).
6. **Bookkeeping:** the committed runner builds **97** controls, not 98 — 4 gen_mutants
   anchors (`N14`, `N24`, `N35`, `N42`) are absent from the v2 reference and print as
   `skipped-patterns-absent`. Also: two concurrent 6-job suites collided on /tmp (ENOSPC)
   producing a P flip indistinguishable from a kill until the log was read (V2G22 draw 1);
   don't run suites concurrently.

## Artifacts

- Matrix (per-mutant edits, batteries, verdicts, notes, commands):
  `.ufo/waves/round-41/w2/MutC1V2Gates/matrix.md`
- Mutants: `.ufo/waves/round-41/w2/MutC1V2Gates/mutants/` (26 files)
- Logs + TSV digests: `.ufo/waves/round-41/w2/MutC1V2Gates/logs/` (74 files)
- Restoration: lane counter sha256 unchanged and equal to the DATA 07f26416 blob; worktree
  clean on that path; /tmp scratch removed after archiving.
