# RevRowsUsedBy — evidence relocation and recovery record

Written 2026-10-25 after the round-35 scratch move.

## What happened

`.ufo/waves/round-35/scratch/RevRowsUsedBy/` was moved (not deleted) to
`.ufo/waves/round-35/scratch-evidence/RevRowsUsedBy/` at ~03:43, along with 58 other
seat dirs. The move carried **top-level files only**: my `snapshot/` dir and the
`m-*` / `n-*` / `base*` mutation trees did not arrive. The old `scratch/` path was then
re-populated by other seats and swept again; it is not a stable locus.

## Surviving files (byte-unchanged from the run that measured them)

```
sha256  file
4940a6be7456feddbcd4162efce7be20c6ac77087cafccfcf8f4a7840091b20e  census-mut.txt
3dd4a384b11a5e399ac35b2b3bf80f347cd85417566712ebae56d381e3913caa  evidence.txt
4d0cb16b57bf35bfa2f784e9abe6ddacc65dbccbb362333eb8dcfe6db872f7d6  mutate.py
425dbcfef4f661ac88a3a2405726fb9d85933c8392037704b8fbbb74139f006e  run.sh
f46715bbf3ee57287311a1df61a3f59a6093eddb1f5445ee67467701dfd17357  snapshot.sha256
7743e8fb0f29a010532213474d61513d5361a654056eba5ca624b528ff967206  usedby-table.txt
```

`evidence.txt` is the 03:36-observation transcript; `snapshot.sha256` pins the five
files it snapshotted.

## Recovery of the snapshot bytes (recovered, not rebuilt)

`snapshot/SOURCES.md` was recovered byte-exact from the jj snapshot commit `d2b6972`
(2026-10-25T03:30:31) with `jj file show -r d2b6972 corpus/SOURCES.md`. Its sha256 is
`848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80` — identical to the
`SOURCES.md` line in `snapshot.sha256`. It is the bytes this seat measured.

`snapshot/idle-lock-chain-armed-r14.md` (`583c708c…`) and
`snapshot/idle-lock-offered-in-the-bar-r15.md` (`82c08a46…`) were copied from the live
tree and also match their `snapshot.sha256` lines: both entries were unchanged between
the 03:36 observation and 03:49.

`snapshot/r12.post-0341.md` (`0bcef21f…`) is the **current** r12 entry, not the 03:36
bytes (`7f27ced0…`). The 03:36 r12 bytes are not recoverable: jj `d2b6972` predates the
entry (it reads empty), and the file was rewritten at 03:41. The rewrite touched only
the `### Errata` body; the `source:` lines, `recheck:` line and `gate-quote:` lines this
seat cites are identical in both states (compared in the transcript and against
`snapshot/r12.post-0341.md`).

`snapshot/README.post-0340.md` (`de5b885a…`) is the current README; the 03:36 README
(`3bb9865f…`) is likewise not recoverable. The one README line this seat quoted at 03:36
is quoted in the report from the transcript and the current line is shown beside it.

## Re-run on current bytes

`run-now.py` + `evidence-now.txt` (recorded 03:48:48) rebuild `base-now` from the live
tree and re-run the whole mutation battery. These are **re-runs**, not the original
measurements; the report states which number came from which. The mutation code is
identical to the surviving `mutate.py` (same edits, same counter, same frozen spec).

## The rule applied here

A rebuilt file is not the bytes that were measured. Recovered bytes are labelled
recovered and carry the sha that proves it; re-runs are labelled re-runs. Nothing that
was not measured is presented as measured.
