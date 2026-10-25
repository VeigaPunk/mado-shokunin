# ExecSymlink — additional link-type controls, round-35 w1

Scoped check: build two trees under
`.ufo/waves/round-35/scratch/ExecSymlink/`, each cloned from the committed
`controls/golden` tree with a single link-type mutation, then run the frozen
counter `.ufo/waves/round-35/c1/count.py` against
`.ufo/waves/round-35/c1/frozen.json` (`PRED-C1-r35-v1`).

These are **additional** controls. The committed control set in
`controls/` is untouched; the new trees live only in `scratch/`.

The counter's `read_regular()` admits a path only when every component
lstat's non-symlink and the final file is `S_ISREG` with `st_nlink == 1`.
The two mutations isolate those clauses:

- **(a) `c1-entry-hardlink`** — `corpus/knowledge/idle-lock-never-asked-r12.md`
  given `nlink=2` via `ln` to a sibling name `idle-lock-never-asked-r12.alias.md`
  inside the tree. Both names resolve to the same inode (`nlink=2`, verified).
  Expected: entry rejected → S203,S204 open → `closed_entries=2 closed_rows=6
  open_cites=2`.
- **(b) `c1-receipt-symlink`** — `.ufo/waves/round-35/fetch/S203.receipt.txt`
  replaced by a symlink `S203.receipt.txt -> S203.receipt.real.txt` (relative;
  target is a regular file in the same directory whose sha256 still equals the
  spec digest `1b7fa87f…dd1646`, so the bytes the path names are unchanged).
  Expected: receipt rejected on the `S_ISLNK` walk → S203 open →
  `closed_entries=2 closed_rows=7 open_cites=1`.

## Results

| control | mutation | command output | verdict | exit |
|---------|----------|----------------|---------|-----:|
| `c1-entry-hardlink` | entry `nlink=2` | `closed_entries=2 closed_rows=6 open_cites=2` | TARGET_MISSED | 1 |
| `c1-receipt-symlink` | receipt `S_ISLNK` | `closed_entries=2 closed_rows=7 open_cites=1` | TARGET_MISSED | 1 |

Sanity re-run of the unmodified golden tree at write time:
`closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `exit=0`.
Frozen counter and spec are stable; only the mutation drives the miss.

## Failures

None. Both controls missed the target exactly as predicted, with the
expected cite signatures: the hardlink control drops the whole entry
(S203+S204 → 2 open cites), the receipt-symlink control drops only the
cites anchored on the symlinked receipt (S203 → 1 open cite).

## Method

```
cp -a controls/golden scratch/ExecSymlink/c1-entry-hardlink
ln <tree>/corpus/knowledge/idle-lock-never-asked-r12.md \
   <tree>/corpus/knowledge/idle-lock-never-asked-r12.alias.md   # nlink 1→2

cp -a controls/golden scratch/ExecSymlink/c1-receipt-symlink
mv  <tree>/.ufo/waves/round-35/fetch/S203.receipt.txt \
    <tree>/.ufo/waves/round-35/fetch/S203.receipt.real.txt
ln -s S203.receipt.real.txt \
    <tree>/.ufo/waves/round-35/fetch/S203.receipt.txt           # relative symlink
```

Run (from repo root, the committed control convention):

```
python3 -I .ufo/waves/round-35/c1/count.py \
  --root .ufo/waves/round-35/scratch/ExecSymlink/<tree> \
  --frozen .ufo/waves/round-35/c1/frozen.json
```

Invariant evidence: `stat` showed `nlink=2` on both hardlink names;
`stat` showed `symbolic link` on `S203.receipt.txt` and `regular file` under
`stat -L`; `sha256sum` of `S203.receipt.real.txt` =
`1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646`, matching
`frozen.json` `receipts.S203.sha256`.

Complementarity: `c1-entry-hardlink` exercises the `st_nlink != 1` clause
(distinct miss signature `open_cites=2` from the committed
`c1-entry-symlink` control's `S_ISLNK` miss at `open_cites=1`);
`c1-receipt-symlink` exercises `S_ISLNK` on a **receipt** path, a slot the
committed set covers only on the entry side.
