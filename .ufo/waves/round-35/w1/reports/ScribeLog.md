# ScribeLog — LOG.md round-35 entry draft (round-35 w1)

Scoped task: draft the LOG.md round-35 entry in the lane's style at
`.ufo/waves/round-35/scratch/ScribeLog/draft.md`. The lane `LOG.md` was NOT
touched (`git status` shows no modification to it). No installs, no mutations
outside my scratch dir and this report.

## Deliverable

`.ufo/waves/round-35/scratch/ScribeLog/draft.md` — one `## Round 35` block in
the house shape (Motivation / Work / Honest notes), modelled on the round-34
entry (`LOG.md:1935-1997`).

## Re-executed evidence the draft cites

| Item | Command / path | Observed |
|---|---|---|
| Freeze commit | `git rev-parse 19e4ab3` | `19e4ab3171c1540c40d6b12097745af98053b07d` |
| C1 predicate frozen | `.ufo/waves/round-35/c1/frozen.json` | `PRED-C1-r35-v1`, targets `closed_entries=3 closed_rows=8 open_cites=0`; sentence identical in `c1/count.py` docstring, `frozen.json`, `registration.md` |
| C2 predicate frozen | `.ufo/waves/round-35/c2/frozen.json` | `PRED-C2-r35-v1`, targets `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1` |
| C1 claim verdict, lane root pre-data | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` | `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1 |
| C2 claim verdict, lane repo | `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` | `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` exit 0 |
| Golden control | `controls/golden.txt` | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0 |
| Ten defect controls | `controls/c1-{donothing,entry-symlink,row-duplicate,row-extra-field,usedby-extra,status-queued,recheck-prose,digest,quote-absent,quote-long}.txt` | all `TARGET_MISSED` exit 1 (donothing `0/0/8`; the other nine `2/7/1`) |
| C2 kill control | `controls/c2-donothing.txt` | `uncovered=1 … verdict=TARGET_MISSED` exit 1 (scratch ledger copy) |
| Clause ledger | `c1/clauses.json` | 10 live clauses, 9 with named controls + `o-nofollow-open` `not-load-bearing`; `retired: r34-word-bound-1-25` |
| Re-issued blob ledger | `ledger/RevFrozenBlobs-r35.md` | seven frozen paths measured at `dff394109f3cc3d851309ad7c67dd3b35b46adf2`, PROVEN |
| Wave dispatch | `w1-taskcall.json`, `seat-plan.tsv`, `dispatch.out` | spawn 64, one batched call, band 64–128; dispatcher launched 64 concurrently |

## Judgment calls made in the draft

- **C1 post-data verdict is a fill-in.** The append has not landed
  (`grep S20[3-9]|S210 corpus/SOURCES.md` → 0 hits; no `idle-lock-*.md` under
  `corpus/knowledge/`). The draft marks `<data commit hash here>` and the
  settled seat counts `<settled counts at closure>` as the only two places
  publication must fill; the pre-data `TARGET_MISSED` line is quoted verbatim.
- **C2 cited as `TARGET_MET` now** because its surface is the frozen ledger
  itself, which landed inside `19e4ab3`. The draft says that is the design.
- Motivation cites the round-34 verifier spotcheck (admit + four routed
  defects) rather than a rejection — this round is a repair round, not a
  retry.

## Out of scope / not exercised

- Post-append C1 score on the lane root; settled wave manifest
  (`w1/exit-codes.tsv` was still empty at write time, `dispatch.out` shows
  launch only).
- SHONEN promotion decisions: draft keeps the `[~]`-on-all-four line from the
  lane convention.
