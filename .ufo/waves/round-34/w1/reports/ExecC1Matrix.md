# ExecC1Matrix — r34 PRED-C1-r34-v1 control matrix

## Driver

One loop over each tree, exact command shape per spec:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/c1/count.py \
  --root <tree> \
  --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/c1/frozen.json
```

`--root` values: `lane` = lane repo root (`/home/vgpnk/Projects/shokunin/mado-shokunin`); all other rows
= `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/<tree>`.

## Artifact

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/scratch/ExecC1Matrix/matrix.tsv`
— header + one row per tree; columns `tree`, `exit_code`, `stdout`. stderr was empty on every run.

## matrix.tsv (verbatim)

```tsv
tree	exit_code	stdout
lane	0	PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
controls/golden	0	PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
controls/symlink-crib	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/entries-only	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/rows-only	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/extra/symlink-entry	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/extra/symlink-parent	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/extra/symlink-sources	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/extra/used-by-prefix	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
controls/symlink-entry	1	PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
```

## Path correction

The enumeration lists `controls/extra/symlink-entry`, but that path does not exist on disk;
the symlink-entry control tree actually lives at `controls/symlink-entry` (verified with
`ls -la` of `controls/` and `controls/extra/` — `extra/` holds only `symlink-parent`,
`symlink-sources`, `used-by-prefix`). The literal row was still run: `count.py` degrades
gracefully on a missing/unreadable root (`read_regular` returns `None` → all cites open →
`TARGET_MISSED`, exit 1). The correction row `controls/symlink-entry` is appended as a 10th
row so the matrix covers the intended control too.

## Observations

- `TARGET_MET` (exit 0) on exactly two trees: `lane` and `controls/golden`.
- Every control tree misses identically: `closed_entries=0 closed_rows=0 open_cites=2`,
  exit 1 — both cites fail atomically, not partially.
- A missing root is indistinguishable from a fully-broken tree by output alone
  (same `0/0/2` line); the `controls/extra/symlink-entry` row demonstrates this.
