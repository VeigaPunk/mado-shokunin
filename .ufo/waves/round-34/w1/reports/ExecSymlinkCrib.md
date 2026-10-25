# ExecSymlinkCrib — r34 C1 symlink crib

## Task

Rebuild the symlink crib under scratch: entry and both fetch blobs as symlinks,
SOURCES.md as a regular copy; run the committed r34 C1 counter with `--root` at
the crib. Expected verdict: `TARGET_MISSED`. Do not edit the committed counter
or controls.

## Crib

Root: `.ufo/waves/round-34/scratch/ExecSymlinkCrib/crib` (fresh, `rm -rf` then rebuilt)

```
corpus/SOURCES.md                                  regular file, 164674 bytes — copy of lane corpus/SOURCES.md
corpus/knowledge/waybar-module-text-route-r25.md   symlink -> /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-module-text-route-r25.md
.ufo/waves/round-34/fetch/S201.bin                 symlink -> /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/fetch/S201.bin
.ufo/waves/round-34/fetch/S202.bin                 symlink -> /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/fetch/S202.bin
```

All three symlink targets are regular files that resolve; the lane SOURCES.md
copy is the lane's real 164674-byte registry (not a fixture), so both S201 and
S202 rows exist in it.

## Command and output

```
python3 .ufo/waves/round-34/c1/count.py \
  --root .ufo/waves/round-34/scratch/ExecSymlinkCrib/crib \
  --frozen .ufo/waves/round-34/c1/frozen.json
```

stdout:

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
```

exit code: `1`

## Result

`TARGET_MISSED` as required — no counter defect. Mechanism: `read_regular()`
(`c1/count.py:40-66`) lstats every path component and returns `None` on
`stat.S_ISLNK` for any of them, so the symlink entry and both symlink fetch
blobs are each unreadable at their final component. `entry_bytes is None` →
`entry_closed=False`; each id fails on `blob is not None` and the empty entry
yields no gate-quote → `open_cites=2`, `closed_rows=0`, `closed_entries=0`.

Consistent with the committed control `.ufo/waves/round-34/controls/c1-symlink-crib.txt`
(same counts, `exit=1`); the committed control crib symlinks only the fetch
blobs, while this scratch crib additionally symlinks the entry — outcome identical.

## Scope notes

- Committed files untouched: `c1/count.py`, `c1/frozen.json`, all of
  `controls/` — verified by no writes outside `scratch/ExecSymlinkCrib/` and
  this report.
- Nothing installed; stdlib Python only.
