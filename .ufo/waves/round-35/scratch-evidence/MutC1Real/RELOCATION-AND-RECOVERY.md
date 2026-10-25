# MutC1Real evidence — relocated to scratch-evidence, originals restored from `4efaf63`

Status: **relocated, not deleted.** At ~03:45 the wave runner moved
`.ufo/waves/round-35/scratch/<Seat>/` to `.ufo/waves/round-35/scratch-evidence/<Seat>/` and
committed the evidence files as `4efaf63`. This directory is my seat's evidence copy.

Authoritative report (durable locus, includes the full 28-run transcript as an appendix):
`.ufo/waves/round-35/w2/reports/MutC1Real.md`

## Files here and their sha256 (all verified equal to the `4efaf63` blobs)

```
ee68b1b31a66600716e0d0de4f44860496b90a8ead9c87c8211ba5c8f14cfdf9  results.json        19355 B
69924f3ff67995b5c49066cb9a830e22911329c637f0163553a349e4da341295  run.log              3809 B
3bca9cdff43da6b4126dbc34d73823bf706d6a2e58bd23da0b4517862ca699a1  driver.py           15895 B
78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6  counter-pristine.py  7882 B
dcc4f33faf13cc64fbe86b3c846196a7d7f2ace73ccf74ab1f1edc9195a7185b  verify-deltas.json   1008 B
fa9753cd41bc5571d08a453e05c48bf4c3e4e6594de025711e3c256a75c12a98  lane-before.sha256   1600 B
b9025f261a4d754a11f2aa62fea9b0987a396e1b1f9430448b16438f9a9fdb83  lane-snapshot-v1.sha256 1600 B
992c0e0362c42095f54c8b12fd21dc89128d6a24ec6a1f968c5bcbcac651e58c  lane-snapshot-v2.sha256 1600 B
```

`results.json` and `run.log` are the measured outputs; `driver.py` is the measured script.
`counter-pristine.py` is byte-identical to `.ufo/waves/round-35/c1/count.py`.

## What the checkpoint does NOT carry

The commit message for `4efaf63` drops the 3.2 GB mutant trees, so `root/` (the pristine v2
snapshot) and `arms/` (11 A counters, 13 B trees, 2 C trees) are gone. They are deterministically
rebuildable:

```sh
cd .ufo/waves/round-35/scratch-evidence/MutC1Real
mkdir -p root/.ufo/waves/round-35
R=/home/vgpnk/Projects/shokunin/mado-shokunin
cp -a "$R/corpus" root/corpus
cp -a "$R/.ufo/waves/round-35/fetch" root/.ufo/waves/round-35/fetch
cp -a "$R/.ufo/waves/round-35/c1" root/.ufo/waves/round-35/c1
# restore the exact v2 entry (the lane has since appended a second errata block):
head -c 3586 "$R/corpus/knowledge/idle-lock-never-asked-r12.md" \
  > root/corpus/knowledge/idle-lock-never-asked-r12.md
sha256sum root/corpus/knowledge/idle-lock-never-asked-r12.md   # must print 7f27ced0…
python3 -I driver.py    # rebuilds arms/, results.json, run.log
```

The truncation is exact: the live file is the v2 bytes plus an append, and truncating to 3586
bytes reproduces `7f27ced0…` (verified). The other 14 artifacts still match `lane-snapshot-v2.sha256`
byte-for-byte in the lane.

## Working-tree damage found and repaired

Two files had been clobbered after the checkpoint (a re-created `scratch/` dir was merged in, and
one failed re-run redirected into it): `driver.py` held a 15893 B transcript rebuild of mine and
`run.log` held a 156 B failed-run log. Both were restored **byte-exactly from `4efaf63`**
(15895 B / 3809 B) and re-verified against the committed blobs. The transcript rebuild was then
discarded: a rebuilt file is not the bytes that were measured, and `scratch/` is swept repeatedly.
