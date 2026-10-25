# ScrReportDraft — round-40 seat report

Status: DONE. Deliverable written; no claim verdict stated by this seat.

## Deliverable

`.ufo/waves/round-40/w1/ScrReportDraft/report-skeleton.md` (11,776 B, 130 `<<...>>` evidence
slots). Section order as the assignment requires, verified by
`grep -n '^#' report-skeleton.md`:

1. `## Work performed` (`:11`) — opens by naming the two frozen claims: C1 operability
   (capability acquisition, `--live`/`--hyprctl`/`--probe`, `PRED-C1-r40-v1`, target 13/13, base
   0/13) and C2 coverage (sourced, `hyprlang`/getoption native-forms entry, `PRED-C2-r40-v1`
   clauses a–h, target 1/1, base 0/1); then work items, swarm line, planner line.
2. `### Seat-role mix` (`:54`) — placeholders inside Work performed, as in the round-39 model.
3. `## Landed changes` (`:92`).
4. `## Before → after measurements` (`:102`) — C1, C1 controls, C2, C2 controls, Harm watch.
5. `## Sources & frontier` (`:137`).
6. `## Trend verdicts` (`:158`) — expansion / quality / discernment.
7. `## SHONEN` (`:166`) — one line per box of the lane `SHONEN.md`, four lines
   (`:170`–`:173`), each `[~]` with an historical pointer plus a round-40 pointer slot and an
   explicit `[ ]`-with-reason alternative.
8. Trailer lines: `Stale-lane:`, `Tool installs:`, `Open L0 questions:` (each a slot).

## What is grounded (not slotted) in the skeleton

- Header hashes: freeze `5e7e88525cc539563de7746361b2650802e81809`, base
  `9fc511ddce708327377161202f358ce37dc266ba` (40 hex chars; `.ufo/waves/round-40/registration.md:3`;
  `git log --oneline -3` in the lane shows `5e7e885 round-40: freeze …` on top of
  `9fc511d round-39 verifier spot-check`).
- Wave spec/dispatch commit `e2b51d3b3f79768282914d57c1fa32cc85dcb06a` (64 seats) —
  `git show --stat --oneline e2b51d3` lists `w1-spec.json`, `w1-dispatch.json`,
  `make-w1-spec.py`, `w1-run.err`.
- Declared seat-role mix and per-role seat names — `python3 -I` over
  `.ufo/waves/round-40/w1-spec.json` `items[].role`/`items[].name`:
  executor 20, scribe 12, reviewer 8, scout 6, connector 5, critic 4, mutation-tester 4,
  revenger 2, sentinel 2, simplifier 1 = 64. Only the "declared" column is filled; landed / dead /
  residual are slots.
- C1 before: `PRED-C1-r40-v1 clauses=a:1 b:0 g:1 k:0`, `fixtures=0/13 tool=present
  verdict=TARGET_MISSED`, exit 1, base selftest `71/71` — `receipts/c1-before-base.txt`.
- C2 before: `clauses=a:0 … h:0 admitted=0`, `admitted=0/1 verdict=TARGET_MISSED`, exit 1 —
  `receipts/c2-before-base.txt`.
- Harm-watch baseline `MADO_SELFTEST: 460/460` — `receipts/selftest-base.txt`.
- Census baseline: `mado ok`, W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277,
  exit 0 — `receipts/census-before.txt`.
- Control summaries `CTL_C1: controls=18 correct=18/18` (`receipts/ctl-c1.txt:19`, with
  `REF-reachability 13/13 → TARGET_MISSED` at `:1` and `BASE-tool 0/13` at `:2`) and
  `CTL_C2: controls=21 correct=21/21` (`receipts/ctl-c2.txt:22`, `P-fabricated-self-consistent
  1/1` at `:1`) — both asserted by registration.md and re-checked in the receipt files.
- SHONEN box text and historical pointers — `SHONEN.md:5,7,9,11`.

## What is deliberately left as a slot

Every after-measurement (C1/C2 at data commit and tip, exit codes, wave control re-runs), every
commit row past the freeze/spec, harm-watch after values, round-end census and row counts,
assimilation/quarantine/collision results, considerthese mining, the three trend verdicts, the four
round-40 SHONEN pointers, and the Stale-lane / Tool installs / Open L0 lines. No verdict was
invented and no check was rerun to decorate the skeleton.

## Touched surfaces

- Wrote `.ufo/waves/round-40/w1/ScrReportDraft/report-skeleton.md` (new).
- Wrote `.ufo/waves/round-40/w1/ScrReportDraft.md` (new; this report).
- Read-only: `registration.md`, round-39 fleet report, `SHONEN.md`, `w1-spec.json`, the four base
  receipts, `receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`, `git log/show` in the lane.
- No product file, counter, control, registry, index, LOG or seat report of another seat was
  edited; no git/jj mutation; no compositor verb run; no install.

## Out of scope / findings for the L1

- The skeleton is a shape, not a report: it does not satisfy the round-40 reporting obligation
  until the L1 fills the slots and the after receipts exist.
- The round-39 model's "Erratum" section has no round-40 counterpart in the skeleton (none was
  routed); if D2's corrected note needs one, the L1 adds it after "Work performed".
- The base hash is 40 hex chars as written in `registration.md:3`; quote it from the registration,
  not from this report's prose.

Tool installs: none. No subagent dispatch, no background jobs.
