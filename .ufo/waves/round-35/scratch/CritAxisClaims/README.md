# CritAxisClaims scratch — restored from the committed evidence checkpoint

`.ufo/waves/round-35/scratch/<Seat>/` was **moved** to
`.ufo/waves/round-35/scratch-evidence/<Seat>/` at ~03:43 (tree mtime 03:45) and the
checkpoint committed. A later sweep removed the writable `scratch/` tree again.

This directory's four original files were **not** rebuilt from memory: they were restored
byte-identically from the committed checkpoint

```
.ufo/waves/round-35/scratch-evidence/CritAxisClaims/
at  b632f0b  (round-35: the last two seat reports, the seats' revised reports, and the
              scratch-evidence checkpoint; checkpoint introduced in 4efaf63)
```

| File | md5 | Provenance |
|---|---|---|
| `sep.sh` | — | the script run at the working tree during wave 2 |
| `sep-out.txt` | `bd38a7a4c11dac4efe44e89621706909` | verbatim receipt of that run (T0–T6), md5-equal to the checkpoint copy |
| `reuse.sh` | — | the shared-receipt probe (T7) |
| `reuse-out.txt` | `9493f2683270e5380dbbdf33f69c4e76` | verbatim receipt of that mutant, md5-equal to the checkpoint copy |
| `digest.sh` / `digest-out.txt` | — | **new**, post-checkpoint probe (V3: receipt bytes unbound to the frozen digest); not in `4efaf63` |

The T0–T8 mirror clones and the `scratch/CritVacuous` junk tree no longer exist (the junk
trees were among the 3.2 GB mutant trees dropped by the checkpoint commit). They are
reproducible from `sep.sh` / `reuse.sh` / `digest.sh`, which clone the lane with
`git clone --shared` (read-only against the lane) or copy only the files C1 reads, and
mutate only the copy.

Durable evidence pointer for the report:
`.ufo/waves/round-35/scratch-evidence/CritAxisClaims/` (committed), plus the verdicts
inlined in `w2/reports/CritAxisClaims.md`. The report body, not scratch, is the locus: the
scratch tree is not stable (a second sweep already removed the re-created dirs once).

Reproduce:
```sh
cd .ufo/waves/round-35/scratch/CritAxisClaims
bash sep.sh    2>&1 | tee sep-rerun.txt
bash reuse.sh  2>&1 | tee reuse-rerun.txt
bash digest.sh 2>&1 | tee digest-rerun.txt
```
A re-run measures the lane as it stands at the re-run revision, not necessarily the
working-tree state recorded in the original receipts; that is why the committed receipt,
not the re-run, is cited.
