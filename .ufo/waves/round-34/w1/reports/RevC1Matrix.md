# RevC1Matrix — frozen PRED-C1-r34-v1 re-run, round-34 w1

Re-ran the frozen round-34 coverage counter over the lane tree and every committed
control tree. Counter and controls untouched (read-only execution).

- Counter: `.ufo/waves/round-34/c1/count.py`
- Frozen spec: `.ufo/waves/round-34/c1/frozen.json`
- Command shape: `python3 -I <count.py> --root <TREE> --frozen <frozen.json>`
- Run date: 2026-10-24

## Results

| # | Tree (`--root`) | stdout | Exit |
|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/mado-shokunin` (lane root) | `PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | 0 |
| 2 | `…/round-34/controls/golden` | `PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | 0 |
| 3 | `…/round-34/controls/symlink-crib` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 4 | `…/round-34/controls/entries-only` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 5 | `…/round-34/controls/rows-only` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 6 | `…/round-34/controls/extra/symlink-entry` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 7 | `…/round-34/controls/extra/symlink-parent` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 8 | `…/round-34/controls/extra/symlink-sources` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |
| 9 | `…/round-34/controls/extra/used-by-prefix` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |

`…` = `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves`.

## Extra committed control directory (not in the enumerated set)

`controls/symlink-entry/` is a real directory committed on disk (contains `.ufo/`,
`corpus/`, `held-entry.md`) — distinct from `controls/extra/symlink-entry`. Ran for
completeness; same frozen spec:

| # | Tree (`--root`) | stdout | Exit |
|---|---|---|---|
| 10 | `…/round-34/controls/symlink-entry` | `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 |

## Observations

- Lane root meets the frozen target exactly: `closed_entries=1 closed_rows=2 open_cites=0`
  → `TARGET_MET`, exit 0. Identical to the `golden` control.
- Every non-golden control misses identically: all counters at zero except
  `open_cites=2` → `TARGET_MISSED`, exit 1. Uniform negative result; no control
  produced a partial count.
- No stderr output and no exit-2 (usage/error) results on any run.
