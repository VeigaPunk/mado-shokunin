# RevReceipts — round-35 control-receipt reproduction

Reviewer seat: w1. Re-run executed 2026-10-24 against lane tip `19e4ab3171c1540c40d6b12097745af98053b07d` (`round-35: freeze C1 and C2 predicates, the clause ledger, the control receipts and the re-issued blob ledger`).

## Method

For each committed receipt `controls/<name>.txt`: extracted the recorded `$` command line, the recorded `PRED-*` stdout line, and the recorded `exit=N`; re-ran the command verbatim from the repo root; compared fresh stdout and exit code byte-for-byte against the recorded pair. Counters and frozen specs used exactly as committed — `.ufo/waves/round-35/c1/count.py` + `c1/frozen.json` for the eleven c1 controls, `.ufo/waves/round-35/c2/count.py` + the scratch frozen spec named in the receipt for `c2-donothing`.

## Results

| Control | Recorded | Re-run | Match |
|---|---|---|---|
| golden | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0 | identical | YES |
| c1-digest | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-donothing | `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-entry-symlink | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-quote-absent | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-quote-long | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-recheck-prose | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-row-duplicate | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-row-extra-field | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c1-status-queued | `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` exit 1 | identical | YES |
| c2-donothing | `uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED` exit 1 | identical | YES |

**Findings: none.** All 11 receipts reproduce byte-for-byte on stdout; every recorded exit code agrees with the counter's actual exit code. No control produced stderr output on re-run.

## Caveats (observations, not failures)

- `c2-donothing` is not self-contained: its command reads `--frozen /fast/scratch/mado-r35/c2-donothing/frozen.json` (which in turn points `clause_ledger` at `/fast/scratch/mado-r35/c2-donothing/clauses.json`). Both files are uncommitted scratch bytes outside the repo. They exist today and reproduce; if `/fast/scratch` is wiped the receipt becomes non-reproducible and the counter exits 2 (`error=frozen-missing`), not 1.
- `c2-donothing`'s `ledger_tip_ok=1` re-verified live: the counter ran `git rev-parse dff394109f3cc3d851309ad7c67dd3b35b46adf2:<path>` for all seven frozen blobs and every returned id matched `c2/frozen.json`. So the receipt additionally confirms the r34 tip and all seven blob ids are still resolvable in this clone.
