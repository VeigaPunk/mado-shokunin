# RerunControlsV2 (w2, round 43) — C2 v2 controls + forgery harness re-run

Attacked: `receipts/ctl-c2-v2.txt`, `ctl/v2-forgeries/forge-v2.log`, `ctl/v2-forgeries/more-v2.log`.
**Verdict: not falsified — byte-identical reproduction at HEAD `2a3707c`.**

- Controls: `CTL_C2: controls=74 correct=74/74`, rc 0; all 74 lines identical to the committed receipt (2 `P-*` must be
  1/1, 72 mutants 0/1). Only difference: the committed logs carry an `exit=0` line appended by the invoking shell.
- Forge: `6/15` admitted, identical; admitted = `P-genuine, A1, A2, D1, E2, H1`; rejected =
  `B1, B2, C1, C2, E1, F1, F2, G1, G2`.
- More: `X1-index-row-lie` admitted, `X3` and `X2` rejected, all three probes P-safe and target-killing — identical.
- Fixture dumps: 60/60 files byte-identical (`diff -r` empty).
- Inputs unchanged since the v2 freeze `496340d` (counter sha256 `9a83407…` at data commit and HEAD; no commits touched
  `ctl/`, the counter or `fetch/`); python 3.14.8; suite deterministic across two runs.
- Teeth: an always-admit scorer collapses the suite to `2/74`, so the tally is load-bearing. The v1 counter also scores
  74/74 on the same fixtures — the v2 evidence in that receipt is its clause column (23 lines, only `i:1→i:0`, `ok`
  unchanged), so the 74/74 alone does not evidence the added `i+` clause.
- Residual reproduced, as registered: six claim-binding forgeries still pass.

Full report, receipts, patched copies (`copy-patch.diff` = the whole delta) and `verify.sh`/`verify.out`:
`.ufo/waves/round-43/w2/RerunControlsV2/`.
