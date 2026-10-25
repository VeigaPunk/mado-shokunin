# ExecSelftestAfter

- Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && bash tools/mado-verify.sh --selftest`
- Result: exit 0; output exactly `MADO_SELFTEST: 460/460 assertions passed`, matching `.ufo/waves/round-39/receipts/selftest-base.txt`.
- Captured output: `.ufo/waves/round-39/w1/ExecSelftestAfter/selftest-after.txt` (no gate blob printed).
- Evidence: shell command completed successfully; captured result file contains the exact one-line output. No other file was written by this seat.