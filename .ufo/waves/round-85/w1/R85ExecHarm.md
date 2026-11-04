# R85ExecHarm — round-85 harm watch report

Seat: R85ExecHarm (w1, harm watch). Date: 2026-11-04.
Revision run: `3905311c75a39c5710413105865c0a1a7dd0116a` — lane HEAD, equals the frozen freeze
revision (base `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`). Every command below was actually
executed at that revision; no verdict here is predicted or inherited.

## Verdicts (details and unfiltered outputs in receipts/harm-watch-r85.txt)

| # | gate | command | exit | final summary line | verdict |
|---|------|---------|------|--------------------|---------|
| 1 | note index | `python3 -I quality/check-index.py --repo . --rev 3905311c…` | 0 | `MADO_INDEX: rev=3905311c… indexed=104/104 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | GREEN |
| 2 | instrument ledger | `python3 -I quality/check-tool-ledger.py --repo . --rev 3905311c…` | **1** | `LEDGER: population=156 ledger_rows=154 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=3905311c…` | **RED** |
| 3 | standing selftest | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` | GREEN |
| 4 | axis scores | `python3 -I quality/check-axis-scores.py --repo . --rev 3905311c…` | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=3905311c…` (navigation 104/104, calibration 86/86, operability 12/12, all MATCH) | GREEN |
| 5 | source census | `…/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado<TAB>ok</home/…/corpus/SOURCES.md>` + 54× W04 + 1× W01 known warnings | GREEN |

The ledger checker is `quality/check-tool-ledger.py` (the lane's instrument-ledger gate; located
via `grep -rl "ledger" quality/*.py`; its summary prints `ledger_rows=N/N … uncovered=N`, matching
the round-84 form).

## RED gate — which and why

`quality/check-tool-ledger.py` at the frozen revision reports **uncovered=2**:

```
LEDGER-ROW reason=uncovered path=quality/counters/c1-r85-identity-causes.py detail=no-row
LEDGER-ROW reason=uncovered path=quality/counters/c2-r85-status-classes.py detail=no-row
```

Both are the round-85 scoring instruments committed by the freeze commit itself. Diagnostic: the
same checker at base `5f174ca…` is `population=154 ledger_rows=154 uncovered=0 …
verdict=TARGET_MET` (exit 0) — retained as block [6] of the receipt. So the freeze commit added
+2 instruments and +0 ledger rows in `quality/tool-ledger.md`; the declaration's harm-watch line
"the instrument ledger stays N/N with zero uncovered" does not hold at the frozen revision. This
seat owns no ledger file, so the red is reported, not suppressed and not repaired here: whoever
closes the wave must add one row per counter to `quality/tool-ledger.md` (checker rule: row must
carry a real description and an accountability pointer naming the row file's basename).

All other standing gates hold their declared values (index 104/104 zero missing/dangling/dup;
selftest 460/460; axis mismatched=0; census exit 0 with its known warning classes).

## Misroot sweep

`git -C /home/vgpnk/Projects/shokunin status --porcelain` → exit 0, 17 lines, recorded verbatim in
`receipts/misroot-sweep-r85.txt`. Notable: untracked stray file `after` directly at the fleet root
(misroot candidate for operator/closure; untouched by this seat), plus pre-existing
`.scratch/` churn and ` M .ufo/reports/round-84/kama.md` from other sessions. No mado-shokunin
path appears in the fleet checkout's porcelain; the lane resolves its own HEAD at the freeze
revision.

## Files written by this seat

- `.ufo/waves/round-85/receipts/harm-watch-r85.txt` — six blocks (5 gates + base diagnostic),
  each with exact command, cwd, exit code, final summary line, and full unfiltered output; the
  census block is byte-identical to the raw tool output (diff-verified after correcting two
  mistranscribed lines, S370/S371).
- `.ufo/waves/round-85/receipts/misroot-sweep-r85.txt` — exact command, exit code, verbatim 17-line
  porcelain output (diff-verified), plus recorded observations.
- `.ufo/waves/round-85/w1/R85ExecHarm.md` — this report.

## Scope notes / honesty

- This seat ran the harm watch only; the C1/C2 counters themselves were not run here (not in this
  seat's assignment), so this report says nothing about cases/mutants outcomes.
- No config tree, compositor state, sibling repo or operator file written; no pacman transaction;
  no mutating git command anywhere. Scratch `/fast/scratch/hyaku/mado-r85/R85ExecHarm` removed at
  teardown; its contents are preserved verbatim inside the receipts.
