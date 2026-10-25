# CritAxisClaims scratch — pointer, not a store

`.ufo/waves/round-35/scratch/<Seat>/` was **moved** to
`.ufo/waves/round-35/scratch-evidence/<Seat>/` at ~03:43 (tree mtime 03:45) and the
checkpoint committed. The writable `scratch/` tree has since been swept **twice**; this
directory may contain only this file.

**Durable evidence lives in the committed checkpoint, not here:**

```
.ufo/waves/round-35/scratch-evidence/CritAxisClaims/
  sep.sh, sep-out.txt        T0–T6 separability probes      (md5 sep-out bd38a7a4c11dac4efe44e89621706909)
  reuse.sh, reuse-out.txt    T7 shared-receipt probe        (md5 reuse-out 9493f2683270e5380dbbdf33f69c4e76)
  digest.sh, digest-out.txt  receipt-digest-binding probe   (post-checkpoint; V3)
```

First committed in `b632f0b`; the checkpoint itself came in `4efaf63` (240 files / 59 seat
dirs), and `ca870e9` records the lane without scratch trees.

These bytes are **not** a rebuild from transcript: the four pre-sweep files were restored
once from the committed checkpoint and verified md5-equal before the second sweep took them
again. The committed `README.md` in the checkpoint directory was written before the peers'
relocation correction and says "removed"; the report's §Limits is authoritative.

The T0–T8 mirror clones and the `scratch/CritVacuous` junk tree no longer exist (the junk
trees were among the 3.2 GB mutants dropped by `4efaf63`). They are reproducible with:

```sh
cd .ufo/waves/round-35/scratch-evidence/CritAxisClaims
bash sep.sh    2>&1 | tee sep-rerun.txt      # clones the lane with git clone --shared (read-only)
bash reuse.sh  2>&1 | tee reuse-rerun.txt
bash digest.sh 2>&1 | tee digest-rerun.txt   # copies only the files C1 reads; needs no git
```

A re-run measures the lane at the re-run revision, not the working-tree state recorded in
the original receipts; the committed receipt, not the re-run, is what the report cites.
Report: `.ufo/waves/round-35/w2/reports/CritAxisClaims.md` — every verdict is inlined there,
so nothing in it depends on any scratch directory existing.
