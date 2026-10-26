# Replay — SimpContract (round 43 w1)

Frozen inputs read only (sha256 above): the counter, the reference, the round-42 controls, the round-43
receipts. Nothing in the lane was edited; this directory is the only write.

## Pins

| file | sha256 |
|---|---|
| `quality/counters/c1-r42-geometry.py` | see `SHA256SUMS` |
| `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` | `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` |
| `.ufo/waves/round-42/ctl/run-c1-controls.py` | see `SHA256SUMS` |
| `.ufo/waves/round-43/receipts/ctl-c1.txt` | see `SHA256SUMS` |

Interpreter: `/usr/bin/python3` 3.14.8. No tool was installed; no pacman; no compositor verb was run; no
network; the reference is imported in-process (`importlib` on the `.txt`), so no bwrap is needed and no
sandbox-free scoring of the real tool is implied.

## Run (in this order, ~2 min total)

```
mkdir -p /fast/scratch/hyaku/mado-r43/SimpContract
cd /fast/scratch/hyaku/mado-r43/SimpContract
cp <seat>/scripts/*.py .
python3 probes.py       > probes.out.json    # 65 pair rows; prints ROWS=65 OK=65 BAD=0
python3 fixtures_scan.py > fixture-scan.txt  # replays all 37 fixtures; prints fixtures=37/37
python3 analyze.py      > analyze.txt        # per-dimension coverage + unexecuted reference lines
python3 equivalence.py  > equivalence.txt    # 11 variants; prints VARIANTS=11 OK=11
python3 deadproof.py    > deadproof.txt      # overlap matrix, token table, free-pass scan
python3 quotegate.py    > quote-gate.txt     # 31 quotes re-grepped from the frozen files
rm -rf /fast/scratch/hyaku/mado-r43/SimpContract
```

`fixtures_scan.py` must run before `analyze.py` (the latter reads `fixscan/fixtures.json`).

## What the receipts in `evidence/` are

- `probes.json` — 65 rows: contract sentence, the two inputs' rc/last line/sha256, expected vs got.
- `equivalence.txt` — corpus size, reference outcome histogram, the 11 variant verdicts and sample diffs.
- `deadproof.txt` — C14 overlap matrix (incl. `/proc/kcore`, mode-000 files), the JSON-number token table,
  and the fixture free-pass scan (7 dimensions, all at 0).
- `fixture-scan.txt` — 37/37 in-process replay, 149 reference source lines executed.
- `fixture-dimensions.txt` — per-dimension hit lists over the 107 fixture runs.
- `order-matrix.json`, `P*.json`, `V2-*.json` — machine-readable copies of the same.
- `quote-gate.txt` — every quote in `dead-weight.md` re-grepped from the frozen sources (31/31, all ≤ 25 words).

Paths printed inside the receipts are the scratch paths of the run (`/fast/scratch/...`, `S/`, `D/`); they
are labels, not citable files. The citable artifacts are the receipts themselves and the frozen pins.
