# ExecSizes — untracked-path byte census (mado-shokunin)

## Method

- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` → 27 `??` entries.
- Per path: `du -sb` (bytes, includes dir inode sizes) and `find <p> -type f | wc -l`.
- Table written to `.ufo/waves/round-34/scratch/ExecSizes/sizes.tsv` — columns: `bytes<TAB>file_count<TAB>path`.
- Nothing deleted.

## Totals

- **Total bytes across 27 untracked paths: 496,631,943** (≈ 473.6 MiB)
- **Largest single path: `.ufo/waves/round-33/scratch/ExecK2Receipts/` — 495,961,904 bytes, 30,892 files** (99.87 % of total)
- **Round-33 leftovers: 19 paths, 496,297,611 bytes**
- **Round-34 artifacts: 8 paths, 334,332 bytes**

## Composition

- Round-33 leftovers = 6 `controls/` fixture dirs + 13 `scratch/` dirs. One scratch tree (ExecK2Receipts) is ~99.9 % of all untracked bytes; every other path combined is ≈ 670 KB.
- Round-34 artifacts = 2 assimilation files, 2 wave-spec scripts/JSONs, `dispatch-w1.sh`, `scratch/`, `w1/`.

## Caveats

- Live tree: sibling wave-1 workers are writing under `.ufo/waves/round-34/scratch/` and `w1/`; those two rows grew between measurement and this report (scratch went 4→13 files during the pass). Round-33 rows are stable.
- `sizes.tsv` is counted inside the `scratch/` row of itself only up to measurement time; self-inclusion is inherent.
