# RevengerPriorDefects — round-32 spot-check defects 1–12 vs round-33 dispositions

Seat: revenger, wave 1, round 33 (leaf — no dispatch). Checkpoint 2026-10-24, wave 1 in
flight; lane HEAD `9a46ccf3282117f960b8d53cd71599a91f388ee3`, round-33 report not yet filed.
Scope respected: nothing under `corpus/lessons/round-32-verifier-spotcheck.md` or
`.ufo/reports/round-32/` was edited. Full per-defect table with evidence pointers:
`.ufo/waves/round-33/scratch/RevengerPriorDefects/checklist.md`.

## Method

Disposition read from three resolvable surfaces only, no inference from intent:
1. committed round-33 repair artifacts (`9a46ccf3282117f960b8d53cd71599a91f388ee3` diff),
2. the frozen round-33 registration and its control set,
3. the dispatched wave-1 seat prompts under `.ufo/waves/round-33/w1/prompts/` plus live
   worktree/repo state (`git status --porcelain`, `grep r33-claim-verdict SCORECARD.md`,
   `grep check-axis-scores SKILL.md`).
Every hash cited was re-verified with `git rev-parse` and ancestry-checked at write time.

## Dispositions

- **D1 falsified SCORECARD C1 row — FROZEN repair routed, append pending.** Claim C2
  (`PRED-C2-r33-v1`, committed `c2/count.py` + registration §C2) freezes the correction:
  an append-only `r33-claim-verdict: r32-C1 cited_entries=7 verdict=honest-stop
  rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047` line, machine-checked against the frozen
  round-32 counter. The line is not yet in `SCORECARD.md`; landing it is the C2 claim itself.
- **D2 report timeline — ERRATUM routed** via `ScribeErrata` (corrected data-commit
  attribution: `f5910876486943d967e6994e21ccddb9aee4f249` 20:22:50, not 20:05:38).
- **D3 "187 MB" — ERRATUM routed** via `ScribeErrata` (11.6 MB / 554 blobs committed at
  `f5910876…`, 130 files / 2.7 MB deleted at `48f9fe09…`). The LOG round-32 note itself is
  append-only and still carries the wrong figure; correction must land as a new entry.
- **D4 gate unregistered — OPEN.** `check-axis-scores` has no row in `SKILL.md` `## Gate
  registry` (grep-verified) and no seat is routed to add one. Only defect with no routing.
- **D5 K2 control receipts — FROZEN repair in flight.** `ExecK2Receipts` reproduces the
  three missing controls through `quality/check-axis-scores.py` (stale→`mismatched>=1`,
  re-derived→`0`, perturbed 41/41→40/41→`1`); uncommitted at checkpoint.
- **D6 undisclosed DEAD verdicts — SPLIT.** Control-coverage half routed (receipt 5(c));
  disclosure half routed (`CriticC2Shadow` re-checks the rfind defect). The rfind-locator
  repair to `quality/check-axis-scores.py` is NOT routed — the checking seat is explicitly
  read-only on it. Locator half OPEN.
- **D7 five round-30 leftovers — OPEN, routed.** `ScoutRound30` + `ReviewRound30` produce
  independent commit/revert recommendations; the 5 paths remain dirty in the worktree
  (3 modified, 2 untracked, `git status --porcelain` at checkpoint); L1 resolves before
  round end.
- **D8 budget claim — ERRATUM routed** (36m52s wall, under `ROUND_MAXTIME=170m`).
- **D9 base short hash — ERRATUM routed**; true base `256222890d935212874a09751ff9b7869943c2d7`
  re-verified, ancestor of the r32 tip.
- **D10 omitted commits — ERRATUM routed** (`b1b740d16875b91ac37546b2958d5b016db97c06`,
  `50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c`).
- **D11 S189 quarantine wording — ERRATUM routed** (cleared-then-adopted flow).
- **D12 missing pre-freeze junk control — FROZEN repair, LANDED.** Committed control set in
  `9a46ccf…` includes `controls/c1-junk.txt` + `RECEIPT.md`, scored 2026-10-24 before any
  corpus append (junk → `TARGET_MISSED` exit 1; golden → `TARGET_MET` exit 0), per
  registration §C1.

## Tally

Landed frozen repair 1 (D12) · frozen repair routed/pending 2 (D1, D5) · split routed/open 1
(D6) · routed-unresolved 1 (D7) · report-only errata routed 6 (D2, D3, D8, D9, D10, D11) ·
still open, unrouted 1 (D4).

## Residual risks

- D1's repair is only as good as the C2 append landing this round; if the round stops before
  it, D1 regresses to OPEN. `grep r33-claim-verdict SCORECARD.md` is the binary check.
- D3/D8/D9 errata exist only as a seat brief right now (`ScribeErrata` scratch in flight);
  they become real when the round-33 report files them.
- D4 and the D6 locator half are the two repairs nothing this round edits; both are
  `quality/check-axis-scores.py` lifecycle items (registration + locator) and would fit one
  small routed seat.
