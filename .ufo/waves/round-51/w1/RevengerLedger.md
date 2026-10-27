# RevengerLedger — how the two tools fell out of the wave-seat tool ledger (round 51, w1, root cause)

Status: complete. Ledger root cause reconstructed from committed bytes; invariant derived and
mapped to `PRED-C1-r51`. No lane file edited, no host probe, no compositor socket.

## Deliverables

- `.ufo/waves/round-51/w1/RevengerLedger/ledger-rootcause.md`
- `.ufo/waves/round-51/w1/RevengerLedger/receipts/r49-checker-at-r51-base.txt`
- `.ufo/waves/round-51/w1/RevengerLedger/receipts/r49-emit-refusal-at-r51-base.txt`
- `.ufo/waves/round-51/w1/RevengerLedger/receipts/population-counts.txt`

## Findings (short form)

1. **The artifact** is `.ufo/waves/round-49/w1/ScrToolLedger/{ledger.md,check-ledger.py}`, committed
   `dd2e827e`, emitted from and defaulted to `03e4ae76` (round-49 base).
2. **Enumeration was correct** (`check-ledger.py:329` tree-derived per `--rev`); **declaration was a
   static literal** (`:59-146`, `:330`); **generation cannot populate** (`:362`, `emit()` `:510-518`,
   hardcoded "round-49 base" prose at `:518`); **detection is
   fail-closed** (`:331-336`). Re-run at `6ca8c559` reproduces both problems, exit 1.
3. **Exact escape step**: the ledger is scoped to a *commit* while claiming a *class*. Three
   instances, each arithmetically complete at its own commit: r47 ledger (`9bddd6ac`, 14/14) →
   `tools/mado-terminal.py` at `0c699605`; r49 ledger (`dd2e827e`, 15/15) → `tools/mado-keysym.py`
   at `430d2569` **8 s later**; → `tools/mado-hostguard.py` at `906178b6` (r50 data).
4. **Amplifiers**: `--rev` defaults to the stale emit rev (`:673`→`:49`); no gate or seat ever runs
   the checker (r49 seat §8 admit; r50 `RevLedgerR50` finding 2; only `SCORECARD.md:2772` mentions
   it outside `.ufo/`); and the population predicate is `tools/` only — at `6ca8c559` the C1 union
   is 79 files and the ledger names 15, with 0 of 62 quality-plane instruments (three of which were
   also born in `906178b6`; at the ledger's own commit `dd2e827e` the predicate already excluded
   15 `quality/*.py` + 42 counters, none named — `receipts/population-counts.txt`).
5. **Not seat knowledge**: the r49 dispatch pinned `03e4ae76` in the seat's task text
   (`w1-spec.json`, `ScrToolLedger`), and keysym did not exist at emit time.
6. **The round-50 remedy reproduced the mechanism** ("move `BASE` off `03e4ae76` to the round-50
   base"): re-pinning a constant is instance 3 of the same defect.

## Invariant (L1–L6, §6 of the root-cause file)

L1 population from the tree at scoring time with no default revision; L2 fail-closed in both
directions (`uncovered`, `dangling`); L3 scope = the instrument plane (`tools/`, `quality/*.py`,
`quality/counters/*.py`), not one directory; L4 a consumer runs it at the scoring revision and
commits the receipt there (D1 applied to the ledger); L5 growth is a landing obligation the gate
forces; L6 non-vacuity at the round base. Mapped term-by-term to `PRED-C1-r51` in §6.

## Residual weakness for the freeze

An explicit but stale `--rev` still yields a clean exit. Only L4 (the gate's choice of revision)
contains that; the counter alone cannot.

## Verification run by this seat (read-only)

- `python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --repo . --rev 6ca8c559… --ledger <r49 ledger>` → 2 problems, exit 1.
- same checker `--emit` at `6ca8c559` → refuses, exit 1, emits no partial ledger.
- `git ls-tree`/`git log` counts at `03e4ae76`, `8ae47b95`, `74782d39`, `6ca8c559`, `9bddd6ac`, `dd2e827e`.
- No pacman; no tool installed or upgraded for this seat (Python 3 stdlib + git only).
- Scratch `/fast/scratch/hyaku/mado-r51/RevengerLedger/` used as `TMPDIR`; deleted at seat end.

Report: .ufo/waves/round-51/w1/RevengerLedger.md
