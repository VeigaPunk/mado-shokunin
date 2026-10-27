# Routed D1 / D4 procedures

## D1 — final two-wave WAVE-DONE receipt

`quality/check-wave-done.py` scans committed bytes at `--rev`; `--round N` selects `.ufo/waves/round-N` and validates results identity against that number. It does not mutate the repo. The checker can be run twice, once per wave, but each invocation scans the entire round, not an individually selected wave. Therefore wait until both w1 and w2 results files (and their ready/dispatch evidence) are committed at the final integration tip. Resolve that tip to its full commit hash and run:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git rev-parse HEAD
python3 -I quality/check-wave-done.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev <FINAL_INTEGRATION_HASH> --round 51
python3 -I quality/check-wave-done.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev <FINAL_INTEGRATION_HASH> --round 51
```

Capture each complete output and exit status as separate receipts, e.g. `receipts/wave-done-r51-w1.txt` and `receipts/wave-done-r51-w2.txt` (label run intent; both summaries necessarily report the same whole-round score). Require exit 0 and `MADO_WAVE_DONE: round=51 waves=2 settled=2 verdict=OK` for both. Commit both receipts before writing/committing the report, and cite only the committed receipt(s) and their exact integration commit. Never cite a run performed before both result files landed or a hash that is not the final integration tip.

## D4 / M50-9 — round-51 fetch checksum convention

Round-50 `.ufo/waves/round-50/fetch/SHA256SUMS` contains a self-entry: `bb21f728cd1c6f1c59af9ecee0f0bf8360b42bb581985d12ab66611210054d07  SHA256SUMS`. A manifest cannot verify its own checksum; do not copy this row. Keep only one row per fetched payload, each digest computed from that payload, with paths relative to the fetch directory. The round-51 manifest design is:

```text
<sha256-of-payload-1>  <payload-1-relative-path>
<sha256-of-payload-2>  <payload-2-relative-path>
...
```

No `SHA256SUMS` row, no digest for the manifest itself, and no checksum manifest self-reference. Store the eventual corrected bytes at `.ufo/waves/round-51/fetch/SHA256SUMS` in the integration; this seat artifact documents the convention only and does not alter round 50.
