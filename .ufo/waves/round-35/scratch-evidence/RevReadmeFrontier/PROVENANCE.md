# RevReadmeFrontier evidence — provenance and hazard map

Written 2026-10-25 by seat `L1Mado35.RevReadmeFrontier` after the scratch relocation. Read this before
citing any file in this directory.

## What happened to the directory

`.ufo/waves/round-35/scratch/` was **moved** (not deleted) to `.ufo/waves/round-35/scratch-evidence/` at
03:43–03:45, 59 seat dirs intact. A second sweep then removed re-created `scratch/` dirs at 03:46, and this
seat's 03:46 rebuild was moved onto the already-relocated directory, **replacing** the files it contained.

## Which file is real

| path here | sha256 | 249/254 L | status |
|---|---|---|---|
| `README.audited.rev4.md` | `de5b885a793f5a773ab1dc69016ea38e185e8f77b920d2ad7b300bc7c6310ac6` | 254 | **correct** — exact bytes of `corpus/README.md` at revision 4; also the committed blob `13269b3a…` at HEAD |
| `README.audited.md` (on disk) | `7547ccfe435a6a2b6c6f4742997e5999df69a6b4e08da3a2b6122ae00f72dada` | 249 | **DO NOT CITE** — this seat's partial reconstruction (two of four reverse hunks applied before the second sweep), committed at HEAD as blob `afd6dff5…` |

The audited snapshot itself (sha `3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f`, 249 L) is
intact in the checkpoint commit:

```
git cat-file -p 4efaf63:.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/README.audited.md | sha256sum
→ 3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f
```

The on-disk `7547ccfe…` copy was left as HEAD has it so the worktree stays clean; it is a transcript
reconstruction, not evidence, and the hash above is how you tell the two apart.

## Mirrors are gone

`mirror/`, `mirror2/` and `mirror4/` were not carried into the checkpoint (the relocated directory was
replaced). The `check-index` verdict does not depend on them: it was re-run on a fresh copy outside the lane,

```
rsync -a --exclude=.git --exclude=.ufo ./ /tmp/rr35-mirror/
python3 -I quality/check-index.py --root /tmp/rr35-mirror
MADO_INDEX: root=/tmp/rr35-mirror indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   exit=0
```
with `/tmp/rr35-mirror/corpus/README.md` sha `de5b885a…`.

## Durable locus

`.ufo/waves/round-35/w2/reports/RevReadmeFrontier.md` is the record: it quotes every audited sentence by line,
every gate command with its exit code, and the retraction of its own F7 error. This directory is a
convenience copy; treat the report as the evidence.
