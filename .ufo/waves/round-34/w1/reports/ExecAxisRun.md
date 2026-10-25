# ExecAxisRun — axis gate against lane HEAD (non-selftest mode)

## Command used

```
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin
```

Non-selftest mode = omitting `--selftest`. The gate's real CLI
(`main()`, check-axis-scores.py:248-291) takes `--repo` (lane repo, default `.`)
and `--rev` (default: resolves repo `HEAD`). Both defaults fit: `--repo` pointed
at the lane root, no `--rev` so it resolved HEAD itself. No `--selftest` flag was
passed — that flag runs fixtures, not the lane state.

## MADO_AXIS line (verbatim)

```
MADO_AXIS: checked=3 mismatched=0 rev=fa7ba11346116672352b5d41494141c5c4d738d0
```

## Full output

stdout:
```
MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=fa7ba11346116672352b5d41494141c5c4d738d0
```

stderr: empty. Exit code: `0`.

## Reading

- All three axes (navigation, calibration, operability) MATCH: the fractions
  published in SCORECARD.md at HEAD equal what the gate re-derives from
  `quality/check-index.py` (navigation, operability) and
  `.ufo/waves/round-31/c2/count.py` (calibration) at that rev.
- Checked rev `fa7ba11346116672352b5d41494141c5c4d738d0` is the lane's HEAD at run
  time (2026-10-24).
- Capture file: `.ufo/waves/round-34/scratch/ExecAxisRun/run.txt`.

Gate not edited. No defects observed in this run.
