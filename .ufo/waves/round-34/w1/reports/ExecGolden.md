# ExecGolden — r34 C1 golden control tree rebuilt from lane committed bytes

## What was done

Rebuilt the golden control tree from the lane's own committed bytes (each source
confirmed present at `HEAD` via `git cat-file -e`, materialized with `git show HEAD:<path>`)
under `.ufo/waves/round-34/scratch/ExecGolden/golden/`, preserving relative paths:

- `corpus/SOURCES.md`
- `corpus/knowledge/waybar-module-text-route-r25.md`
- `.ufo/waves/round-34/fetch/S201.bin`
- `.ufo/waves/round-34/fetch/S202.bin`

## Counter run

Command (cwd = lane root):

```
python3 -I .ufo/waves/round-34/c1/count.py \
  --root .ufo/waves/round-34/scratch/ExecGolden/golden \
  --frozen .ufo/waves/round-34/c1/frozen.json
```

stdout:

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
```

exit=0

Byte-identical to the recorded receipt `.ufo/waves/round-34/controls/c1-golden.txt`.

## File-type / nlink confirmation

`stat -c '%n %F %h'` over every copied file:

```
.ufo/waves/round-34/scratch/ExecGolden/golden/corpus/knowledge/waybar-module-text-route-r25.md regular file 1
.ufo/waves/round-34/scratch/ExecGolden/golden/corpus/SOURCES.md regular file 1
.ufo/waves/round-34/scratch/ExecGolden/golden/.ufo/waves/round-34/fetch/S201.bin regular file 1
.ufo/waves/round-34/scratch/ExecGolden/golden/.ufo/waves/round-34/fetch/S202.bin regular file 1
```

All four: regular file, nlink=1. No symlinks, no hardlinks (fresh files written by
`git show` redirect, not `cp --link`).

## Note — divergence from controls/golden is cosmetic

`build-controls.py::write_tree` synthesizes `SOURCES.md` and the entry note
(`SOURCES`/`ENTRY_TEXT` fixtures, lines 26–40), so the committed real files hash
differently from `controls/golden/`'s copies:

| file | lane HEAD sha256 | controls/golden sha256 |
|---|---|---|
| corpus/SOURCES.md | fbbf365c6f1a1aaa2a7d4ffb62ffdec6063807e973da34c45f394d35511dd657 | 1ed42b9d2ba0e41f2337273ab03dd94caaeb8cc2ed687e97326ff6652a651b4b |
| corpus/knowledge/waybar-module-text-route-r25.md | 1236017410947e74f7dd679a6a8e2c93219ce915834d00a482b775ad76133e3f | 5ebb5ee753fa54b5d944606aec38b7ca260e4f632fa593cf76d0f33359cb6e8a |
| fetch/S201.bin | 799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e | identical |
| fetch/S202.bin | 5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846 | identical |

The predicate still closes: the real `SOURCES.md:203-204` rows carry the single
`used-by` token `corpus/knowledge/waybar-module-text-route-r25.md` for S201/S202,
the real entry carries the exact `gate-quote:` lines (:12-13) matching
`frozen.json` quotes, and the fetched blobs sha256-match and embed each quote —
`closed_entries=1 closed_rows=2 open_cites=0`. Verified by execution above, not
by fixture comparison.
