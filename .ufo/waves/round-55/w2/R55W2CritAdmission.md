# R55W2CritAdmission — report (round 55, wave w2, falsify: admission audit)

Deliverables: `.ufo/waves/round-55/w2/R55W2CritAdmission/admission.md` (verdict table, admission per claim, residual risks, commands).
Receipts: `.ufo/waves/round-55/w2/R55W2CritAdmission/receipts/` (exact outputs; `receipts.sh` re-runs them). Attack inputs:
`.ufo/waves/round-55/w2/R55W2CritAdmission/attacks/`.

## What was attacked
- C1: counter line and harness against the frozen v1 sentence and the v2 errata; the K16 row v2 changed; the K14/K17 registry
  anchors; the proposition-content gap (attack k1).
- C2: counter/harness line, hold-out commitment (v1 vs v2 vs freeze), the live host run, the numlock provenance change.
- C3: counter/harness line, C3-CTL-5 change, the lexical `p23` leg (attacks p23 and token salad) and the P23 text against
  pin lines 1554-1576.
- Harm watch: selftest, navigation index, census. Freeze files and the v1→v2 table diff.

## Verdicts (short; full table in admission.md §1)
- C1 counter and harness: SURVIVES. Measured lines are the frozen sentences at `57584ed6`.
- C1 content: BROKEN as a verifier. Placeholder K01 proposition → `TARGET_MET` (k1).
- C1 K16 row: BROKEN. v2 quote lost the `!VAL` absence half; proposition still claims it.
- C1 K14/K17 registry anchors: BROKEN in the registry; counter silent; entry declares it.
- C2 counter/harness: SURVIVES. Hold-out commitment identical in v1 and v2 (not re-sealed). Host spot check AGREE.
- C2 numlock range: v2 corrects a false source attribution in v1. No behaviour change.
- C3 counter/harness: SURVIVES. C3-CTL-5 changed in v2 to a stricter `stale` leg; the v1-shaped control still fails.
- C3 P23 text: correct against the pin on manual reading. The predicate: BROKEN as a verifier. A flipped `== 0` arm and a token-salad P23 both → `TARGET_MET`.
- Harm: selftest 460/460, index 70/70, census rc 0 with E=0. Freeze files byte-identical to `54dacbd8`; the only table change is the K16 quote plus `rev_rule`.

## Admission
Mechanically, all three claims verify under their frozen predicates and no axis is harmed. As content, C1 and C3 are verified
only as quote-identity and token presence; the operator rules on whether that satisfies "every claim verifies".

## Commands and outputs
See `receipts/receipts.sh` and `receipts/*.txt`. Key lines:
- `MADO_KBD_ENTRY: rev=57584ed6… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (rc 0)
- `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`
- `MADO_P19_FIX: rev=57584ed6… prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none` (rc 0)
- `MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK`
- `MADO_R55_C2: rev=57584ed6… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`
- `MADO_SELFTEST: 460/460 assertions passed`; `MADO_INDEX: … indexed=70/70 missing=0 dangling=0 duplicates=0`; census rc 0.
- attack k1 → `MADO_KBD_ENTRY: rev=bb09bc23… … verdict=TARGET_MET missed=none`
- attack p23 → `MADO_P19_FIX: rev=17339591… … p23=ok … verdict=TARGET_MET missed=none`
- attack token salad → `MADO_P19_FIX: rev=28ff7cab… … p23=ok … verdict=TARGET_MET missed=none`
- v1-shaped C3 control (c5) → `MADO_P19_FIX: rev=0aed79c3… … p23=bad … verdict=TARGET_MISSED missed=p23,stale` (rc 1)

## Ran / did not run
- Ran: all frozen counters and harnesses at `57584ed6` (scratch `--work`); selftest and index on an export of the rev; census
  on an export root with `shokunin.conf`; read-only host verbs (`hyprctl version`, `hyprctl getoption … -j`, `hyprctl devices -j`,
  reading `~/.config/hypr/input.conf`); `mado-kbdopts.py` on the real input.conf with a scratch getoption file; scratch clones
  for three attacks and one token-salad attack (one committed mutation per clone; toplevel asserted; counters run unchanged).
- Did not run: sentence-to-pin entailment audit beyond the manual P23 check; base-rev census comparison; `check-freeze-order.py`;
  any hold-out fixture read beyond the frozen harness's own use.
- Writes: only the deliverable directory under `.ufo/waves/round-55/w2/` and scratch. No tracked-file edits, no git/jj mutation
  in the lane or fleet repo, no commits, no subagents, no config or compositor change. Scratch removed before yield.
- Tooling: nothing installed. The pacman guard was not touched.
