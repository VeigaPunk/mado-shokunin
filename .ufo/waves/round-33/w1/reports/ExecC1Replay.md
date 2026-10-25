# ExecC1Replay — PRED-C1-r33-v1 counter replay on lane root and controls

Scope: re-run `count.py --frozen c1/frozen.json` over three roots — lane root,
`controls/junk`, `controls/golden` — without editing the counter; paste every
stdout line and exit code. Both control trees exist (golden is present; nothing
absent to report).

## Run 1 — lane root

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/count.py \
    --root /home/vgpnk/Projects/shokunin/mado-shokunin \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED
EXIT=1
```

## Run 2 — controls/junk

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/count.py \
    --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/controls/junk \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED
EXIT=1
```

## Run 3 — controls/golden

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/count.py \
    --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/controls/golden \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c1/frozen.json
PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET
EXIT=0
```

## Findings

- **Golden is present** and the counter hits the frozen target exactly:
  `closed_entries=2 closed_rows=4 open_cites=0`, exit 0. The counter
  discriminates — it is not vacuously passing or failing.
- **Lane root and junk are byte-identical in output**:
  `closed_entries=0 closed_rows=0 open_cites=4`, exit 1. All 4 frozen cites
  (S190, S191, S197, S189 across `corpus/knowledge/waybar-module-text-route-r25.md`
  and `corpus/knowledge/event-delivery-limits-r26.md`) are open on the lane root,
  so neither entry closes.
- Exit codes match the contract printed in the docstring: 0 = TARGET_MET,
  1 = TARGET_MISSED; no stderr, no exit 2, frozen predicate check passed
  (no `predicate-drift`).
- Note on interpretation: `open_cites` is computed per-cite under `--root`
  (entry gate-quote line + blob sha256 + registry used-by), not from
  `frozen.json` alone — the identical 4 on lane root and junk means the real
  tree currently closes **zero** of the four cites, same as the junk fixture.

Verdict: counter replayed cleanly on all three roots; lane root stands at
TARGET_MISSED (0/2 entries, 0/4 rows, 4 open cites).
