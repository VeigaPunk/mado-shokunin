# MutEntryQuotes — report (mado round 41, w2)

Task: attack the landed entry/README/registry/lesson bytes at DATA `07f2641696b5ac73de1404ea737a9f27e9819aa1`
with single-token mutations scored by `quality/counters/c2-r41-focus-entry-v2.py`; report what the
predicate cannot protect and give the reviewer script that catches the scriptable subset.

**Status: COMPLETE.** Full matrix, findings and reproduction commands:
`.ufo/waves/round-41/w2/MutEntryQuotes/matrix.md`. Deliverables in the same directory:
`reviewer_check.py` (the script), `mutate.py` (driver), `results.json`, `review.json` (raw verdicts).

## Result

- Baseline pristine tree: `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET` (detector valid).
- **53 mutants: 43 ADMITTED / 10 killed.** All 10 controls died on their expected clauses
  (X01→b, X02→h, X03→g, X04/X05/X06→c, M01→f, X07/X08→d+g), so the 43 survivors are genuine
  coverage gaps: free prose numbers, registry receipt-metadata numbers (sizes/lines/sha256),
  OBS→INF label flips, registry kind/tier cell swaps, recheck scalars (entry `90d`, held S037
  `on-release`), ADMIT/REFUSE staged-path swaps, and lesson Gate prose numbers.
- Reviewer script `reviewer_check.py` (13 mechanical checks over receipts/freeze/BASE) catches
  **36 of 43** survivors on mutated trees and reports exactly one violation on pristine bytes —
  the finding below. True human-only escapes: E10, E16, R16, L05, L06 (plus R15 weakly catchable
  via a w1 artifact, and R11 which is a repair).

## F-1 — DATA defect (fix before the round lands)

`corpus/SOURCES.md:235` (S286 scope cell) says "which **nine** it binds" and its anchor lists nine
bind branches; the pinned receipt `xdph-PortalManager.cpp` has **ten** `INTERFACE ==` branches
(`zwlr_foreign_toplevel_manager_v` missing from the list). Entry §3 (line 69) says "ten" — the
registry row contradicts entry and receipt. Repro:

```
git show 07f2641:corpus/SOURCES.md | sed -n 235p
git show 07f2641:.ufo/waves/round-41/fetch/xdph-PortalManager.cpp | grep -c 'INTERFACE =='   # 10
```

The sweep's R11 mutant ("nine"→"ten") is the only edit that restores registry↔receipt agreement,
corroborating the defect. L1 action: correct the S286 scope/anchor cells.

## Restoration

Mutations lived only in the disposable scratch clone `/tmp/mutentryq/clone` (reset to DATA before
the sweep, worktree restored after every run). Post-sweep evidence: `git diff 07f2641 -- corpus/`
empty; sha256 of all four worktree files equal to their DATA blobs (entry `4c08fc83…`, SOURCES
`768b839f…`, lesson `d8417b86…`, README `f3515b7b…`). Lane tracked files untouched; scratch
removed after artifacts were copied to the seat directory.

Tooling record: no installs (system python3 + git only); pacman untouched; no host services,
sockets or input touched; no mutating git in the lane or fleet.
