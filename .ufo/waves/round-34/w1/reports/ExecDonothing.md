# ExecDonothing — r34 C1 do-nothing control

## Task

Rebuild the do-nothing control in scratch: `corpus/SOURCES.md` as of the
pre-data freeze commit `3420e827bd7b21b1374b23245526554ffd20d096`, the two
frozen fetch blobs `S201.bin`/`S202.bin` copied as regular files, and **no**
knowledge entry. Run the committed r34 C1 counter with `--root` at that tree.
Required verdict: `TARGET_MISSED`. Committed counter/controls untouched.

## Tree

Root: `.ufo/waves/round-34/scratch/ExecDonothing/tree` (fresh `mkdir -p`)

```
corpus/SOURCES.md                                  regular, 163765 bytes, nlink=1 — byte-equal to commit blob (cmp -s vs git show)
.ufo/waves/round-34/fetch/S201.bin                 regular, 6550 bytes, nlink=1, sha256=799bf02f6d18ae04… (matches c1/frozen.json)
.ufo/waves/round-34/fetch/S202.bin                 regular, 8324 bytes, nlink=1, sha256=5df496eb3cfe5cae… (matches c1/frozen.json)
corpus/knowledge/waybar-module-text-route-r25.md   ABSENT — entry deliberately not added
```

The freeze-commit registry contains **no** `S201`/`S202` rows
(`git show 3420e82:corpus/SOURCES.md | grep -E 'S20[12]'` → rc=1), so even the
two correctly-fetched blobs cannot close a cite.

## Command and output

```
python3 .ufo/waves/round-34/c1/count.py \
  --root .ufo/waves/round-34/scratch/ExecDonothing/tree \
  --frozen .ufo/waves/round-34/c1/frozen.json
```

stdout:

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
```

exit code: `1`

## Result

`TARGET_MISSED` as required — counter agrees with the committed control
receipt `.ufo/waves/round-34/controls/c1-donothing.txt` (`exit=1`, identical
counts). Mechanism: `entry_bytes is None` → `entry_closed=False`; each id also
fails `rows_for()` (no registry row → `len(rows)==0≠1`) and `found==quote` (no
gate-quote line), so `open_cites=2`, `closed_rows=0`, `closed_entries=0`. The
control isolates "did the round's own changes close the cites": a pre-data
tree with valid fetch bytes still misses.

## Scope notes

- Committed files untouched: `c1/count.py`, `c1/frozen.json`, all of
  `controls/` — writes only under `scratch/ExecDonothing/` and this report.
- No installs; `git show`, `cp -p`, `cmp`, `stat`, stdlib Python only.
