# R5R6Corrections — append-only correction drafts

Date: 2026-10-23

## Findings

1. Round-25 R8 line 85 overstates the repair: `round-25/quality/` contains only `check-control-receipts.py` and the two Q36 receipts. The non-author spot-check says the QUALITY 33–35 survivors `MutCheckRegOrder` and `MutCheckReceipt` were not hardened and remain open (`corpus/lessons/round-25-verifier-spotcheck.md:138-141,207-208`); the round-25 lesson agrees (`corpus/lessons/round-25.md:89-90`). The requested directory listing and path-limited history are recorded below.

   **Exact paragraph to append to `.ufo/waves/round-25/registration.md`:**

   > Correction (2026-10-23): R8's disposition above is inaccurate: no hardened MutCheckRegOrder or MutCheckReceipt checks landed under `round-25/quality/`. That directory contains only `check-control-receipts.py` and `q36-red-round24.txt` / `q36-green-round25.txt`; the QUALITY 33–35 survivors MutCheckRegOrder and MutCheckReceipt were not hardened this round and remain open.

2. The before-v4 receipt ends with `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED` (evidence line 49), and has no `exit=` line. `round-25/c1/count.py:298` returns `0 if met else 1`; therefore the exit status corresponding to the receipt's recorded `TARGET_MISSED` verdict is 1. This is derived from the receipt and code, not directly recorded in the receipt. No round-26 lesson was present under `corpus/lessons/` when checked, so this is a draft for its end, not an edit to that lesson or the receipt.

   **Exact note to append to the end of the round-26 lesson:**

   > Correction note (2026-10-23): The before-v4 receipt `.ufo/waves/round-25/evidence/c1-before-v4-41cc04c8.txt` ends with `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED` and contains no `exit=` line. The counter's return branch at `.ufo/waves/round-25/c1/count.py:298` returns 1 for a non-met predicate, so the receipt's exit status is 1 as derived from its recorded verdict and the counter code. The receipt itself remains unchanged.

## Commands and observed outcomes

Ran from `/home/vgpnk/Projects/shokunin`:

```sh
timeout 20s prlimit --as=4000000000 -- ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/quality/ && timeout 20s prlimit --as=4000000000 -- git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --oneline -- .ufo/waves/round-25/quality/
```

The `ls -la` output listed exactly `check-control-receipts.py`, `q36-green-round25.txt`, and `q36-red-round24.txt` (plus `.` and `..`). The path-limited log output was:

```text
9022467 round-25: C1 measurement receipts at ef94763c (v4 TARGET_MET 41/41; v1-v3 reported); PROVINCE tool row; C2 exploratory ledger '## Current state (round 25)'; Q36 green on round 25; residual call spec
2896dc4 round-25: routed repairs R1-R6 (QUALITY 36 + control-receipt check red on round 24; A18 in-row correction; S161 and receipt-chronology corrections; SCORECARD stale-row pointers); wave a3w1 spec
```

Read and cross-checked: `.ufo/waves/round-25/registration.md:85`; `corpus/lessons/round-25-verifier-spotcheck.md:138-141,207-208`; `corpus/lessons/round-25.md:89-90`; `.ufo/waves/round-25/evidence/c1-before-v4-41cc04c8.txt:1-49`; `.ufo/waves/round-25/c1/count.py:295-298`. The receipt's final line is the `TARGET_MISSED` verdict; it does not contain an exit-status line.

## Surfaces, gates, and limits

- **Written surface:** this report only: `.ufo/waves/round-26/w1/reports/R5R6Corrections.md`.
- **Proposed append targets (not edited):** `.ufo/waves/round-25/registration.md` and the end of the round-26 lesson.
- **Untouched:** the historical C1 receipt and counter, along with all other lane files.
- **Gate/evidence:** directory contents and path-limited history were checked with the exact bounded command above; the receipt and counter return branch were read. No counter, test, build, or other runtime was run. The before-receipt exit status is derived, not an observed `exit=` line.
- **Out of scope:** appending either correction, rewriting the receipt, and editing product code.
