# CritAxisClaims scratch — rebuilt after the 03:45 sweep

The whole `.ufo/waves/round-35/scratch/` tree was removed by an external sweep at about
2026-10-25T03:45. This directory was **not** reconstructed from memory: the four files here
were restored byte-identically from the committed checkpoint

```
.ufo/waves/round-35/scratch-evidence/CritAxisClaims/
at  b632f0b  (round-35: the last two seat reports, the seats' revised reports, and the scratch-evidence checkpoint)
```

| File | md5 | Origin |
|---|---|---|
| `sep.sh` | — | the script run at the working tree during wave 2 |
| `sep-out.txt` | `bd38a7a4c11dac4efe44e89621706909` | verbatim receipt of that run (T0–T6) |
| `reuse.sh` | — | the shared-receipt probe (T7) |
| `reuse-out.txt` | `9493f2683270e5380dbbdf33f69c4e76` | verbatim receipt of that mutant |

The T0–T8 mirror clones (and the `t8` stub-counter probe) were not checkpointed and no
longer exist. They are reproducible from the two scripts, which clone the lane with
`git clone --shared` (read-only against the lane) and mutate only the copy. The report
inlines every verdict and exit code, so no claim depends on a mirror surviving; the scripts
and these receipts are the durable evidence pointer.

Durable evidence pointer for the report:
`.ufo/waves/round-35/scratch-evidence/CritAxisClaims/` (committed).

Reproduce:
```sh
cd .ufo/waves/round-35/scratch/CritAxisClaims
bash sep.sh 2>&1 | tee sep-rerun.txt
bash reuse.sh 2>&1 | tee reuse-rerun.txt
```
A re-run measures the lane as it stands at the re-run revision, not necessarily the
working-tree state recorded in `sep-out.txt`; that is why the committed receipt, not the
re-run, is cited.
