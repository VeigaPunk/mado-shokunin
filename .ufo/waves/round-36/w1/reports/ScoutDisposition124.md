# ScoutDisposition124 — D8 scratch-tree disposition facts

Measured at lane HEAD `345fc38` (2026-10-25 05:01:12 -0300); verified identical at
`master` (`fe55a90`, same tree object `9025975`) and at the freeze commit
`dbf8b57`. All commands ran from LANE root.

## 1. Miss count (D8 claim "tracked paths=124")

```
$ git ls-tree -r --name-only HEAD .ufo/waves/round-35/scratch | wc -l
124
```

PASS. Exactly 124 tracked paths at HEAD, master, and the freeze commit. Per-seat
breakdown:

```
$ git ls-tree -r --name-only HEAD .ufo/waves/round-35/scratch | awk -F/ '{print $4}' | sort | uniq -c
    124 scratch
```

- `scratch/RevC1Tip/` — 123 files
  - `repro.out` (9088 B, blob `3bb07a7`) — original run transcript
  - `tree/` (12 files) — clean baseline copy of corpus + fetch receipts + c1
  - `headtree2/` (15 files) — HEAD snapshot (c1 clauses/count/frozen + 8 receipts + corpus)
  - mutants `m1`–`m5`, `m8`, `m9` (12 files each) and `m7` (11 files)
  - `m6` is absent — `reproduce.sh` never built it (it is not a loss; D8's
    "m1–m9" shorthand is off by one: m6 never existed)
- `scratch/CritAxisClaims/README.md` — 1 file (stale placeholder, see §3)

## 2. Size claim (D8 "2.2 MB")

```
$ git ls-tree -rl HEAD .ufo/waves/round-35/scratch | awk '{s+=$4} END {printf "%.3f MiB (%d bytes)\n", s/1048576, s}'
1.871 MiB (1962263 bytes)
```

FINDING. Actual sum-of-blob-bytes = 1,962,263 ≈ 1.87 MiB ≈ 2.0 MB decimal. D8's
2.2 MB overstates by ~10%; the round-35 lesson quoted the same 2.2 MB. Same order of
magnitude; not a fact error that changes any decision.

## 3. Structure and staleness

- `CritAxisClaims/README.md` (blob `bc2656c`, 2067 B) is a **stale placeholder**:
  it says the whole scratch tree was removed by a 03:45 external sweep and that the
  writable scratch tree "may contain only this file". That contradicts the actual tree
  (124 files, all still tracked). The durable CritAxisClaims evidence lives in
  `scratch-evidence/CritAxisClaims/` with a different README (blob `0344816`).
  This README is cited by no record as a pointer: grep of LOG.md, SCORECARD.md, and
  lessons finds no `scratch/CritAxisClaims` citation outside scratch-evidence prose.
- `RevC1Tip/repro.out` is a unique transcript (not duplicated in scratch-evidence:
  `final.out` there is only the verdict trailer; `evidence*.txt` differ). It is not
  cited as a pointer anywhere.

## 4. Mutant integrity (all byte-verified against tree baseline)

Every mutant differs from `tree/` by exactly its one declared mutation; all other
files are blob-identical to `tree/` (which is itself blob-identical to the live
receipts/corpus at HEAD):

| mutant | mutation | evidence |
|---|---|---|
| m1 | S206 receipt tampered (`TAMPER: bytes changed after freeze` appended) | diff tree vs m1 S206.receipt.txt: one added 2-line block; other 7 receipts identical |
| m2 | S206 row status `mined`→`queued` | diff SOURCES: exactly 1 row, 1 token |
| m3 | S207 gate-quote padded to 26 words | blob `f8dabe7` in knowledge file, all else identical |
| m4 | S208 row used-by extra foreign entry | diff SOURCES: exactly 1 row changed |
| m5 | S205 quote not a receipt substring | blob `5d88f86` in knowledge file |
| m7 | S209 receipt deleted (11 files) | S209.receipt.txt absent; 7 receipts identical |
| m8 | S210 anchor digest zeroed (`0`×64) | diff SOURCES: exactly 1 receipt-sha256 cell |
| m9 | S206 row moved out of `## Registry` | diff SOURCES: row removed at 208, re-added after 425 |

## 5. Regenerability

`scratch-evidence/RevC1Tip/reproduce.sh` (committed at `0e871c7`) regenerates
`tree`, `headtree2`, and mutants m1–m5, m7–m9 deterministically from HEAD bytes; the
run outputs (`evidence.txt`, `evidence2.txt`, `evidence3.txt`, `final.out`,
`census-ab.txt`) are committed there. So every mutant fixture is reproducible; the
only non-regenerable byte is `repro.out` (9 KB, uncited).

## 6. Gate interaction (`quality/check-evidence-pointers.py`, HEAD)

- `scratch_count = len(files ∩ .ufo/waves/round-35/scratch/*)` = 124 at HEAD.
- The gate requires the round-36 lesson to name a disposition with `tracked paths=124`.
  Current lesson (`corpus/lessons/round-36.md` § Scratch disposition) already says
  "**retained** … tracked paths=124" and the keyword regex (`retained|retain|…`)
  accepts it. Gate condition is satisfied as-shipped.
- If the tree is pruned/deleted, the count changes and the lesson must be updated in
  the same change, or `scratch_disposition_ok=0` → TARGET_MISSED.
- Caveat: commit `7d708cf` ("no scratch tree left" claim) is the commit that actually
  *added* the 124 files; `ae34886` (which claimed no scratch tree) did not delete them.
  The current tree is the recorded state and the lesson matches it.

## 7. Verdicts

- D8 count "tracked paths=124": **PASS** (exactly 124, three revisions checked).
- D8 size "2.2 MB": **finding** — actual 1.87 MiB (1,962,263 bytes); overstated ~10%.
- D8 "m1–m9": **finding** — m6 never existed; m7 has 11 files (S209 receipt deleted,
  which is its declared mutation).
- Mutant integrity: **PASS** — each mutant is baseline + exactly one declared mutation.
- Disposition recommendation: **retain as-is** (count 124) matches the gate and the
  lesson; retention additionally preserves verbatim re-run fidelity of the committed
  scratch-evidence transcripts. Deletion would be defensible (all mutant claims are
  regenerable) but would require editing the lesson count in the same change. The
  stale `CritAxisClaims/README.md` is harmless to the gate (uncited) but is the one
  file that would be cleanly deletable without touching the lesson, were cleanup ever
  wanted.

## 8. Any/scratch

No tools installed (nothing needed beyond git/coreutils). No files written outside
this report.
