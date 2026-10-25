# MutC1Counter — sha256-bypass mutant detection report

Date: 2026-10-24. Wave: round-33/w1. Scope: leaf member, no subagent dispatch.

## Mutation

- Copied `.ufo/waves/round-33/c1/count.py` → `.ufo/waves/round-33/scratch/MutC1Counter/count.py`.
- One-line deletion (line 85): removed `and digest == fetch["sha256"]` from the `ok` conjunction.
  The mutant accepts a gate-quote even when the fetch blob's sha256 does not match the digest
  frozen in `c1/frozen.json`. `hashlib` import left in place (harmless; digest still computed but unused).
- Lane counter `.ufo/waves/round-33/c1/count.py` unchanged (verified by diff below — only the mutant differs).

```
$ diff .ufo/waves/round-33/c1/count.py .ufo/waves/round-33/scratch/MutC1Counter/count.py
85d84
<                 and digest == fetch["sha256"]
```

## Detection evidence — control: `.ufo/waves/round-33/controls/hash-mismatch`

Original (must miss — it does):

```
$ python3 .ufo/waves/round-33/c1/count.py --root .ufo/waves/round-33/controls/hash-mismatch --frozen .ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=1 closed_rows=3 open_cites=1 verdict=TARGET_MISSED
exit=1
```

Mutant (prints TARGET_MET — mutation is behaviourally detected):

```
$ python3 .ufo/waves/round-33/scratch/MutC1Counter/count.py --root .ufo/waves/round-33/controls/hash-mismatch --frozen .ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET
exit=0
```

## Result

DETECTED. The hash-mismatch control flips the mutant from `TARGET_MISSED` (exit 1) to
`TARGET_MET` (exit 0): one corrupted fetch blob (S189, carried from round-32) becomes a closed
cite under the mutant, lifting closed_entries 1→2, closed_rows 3→4, open_cites 1→0. The
sha256 clause in the original is the only thing holding that cite open — the control pins it.
