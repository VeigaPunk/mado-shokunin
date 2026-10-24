author: mado
date: 2026-10-24

# mado round 29 — registration (frozen before any data seat of this round)

Lane repo: /home/vgpnk/Projects/shokunin/mado-shokunin. Paths without a leading
`tools/`, `quality/` or `corpus/` prefix resolve under `.ufo/waves/round-29/`.

Base: lane tip `f652ca99c64631a72e06a7d2f6ffa1708794f65e` (round-28 closure:
rejected-honest-stop; non-author spotcheck `f652ca99`, same commit — the
integrator-committed spotcheck lesson).

## Routed queue (round-28 closure, this round's priority)

The round-28 verifier spotcheck routed four items to round 29 (quoted from
`corpus/lessons/round-28-verifier-spotcheck.md`):

1. "r29 pre-data registration must fix the count-v4 guard pin to the committed
   bytes (`635ae788…`) and smoke-run the composite once at freeze, committing
   the full output (QUALITY 38)."
2. "r29 must either preserve registered ephemeral inputs through adjudication or
   adopt the named-committed-receipt basis (QUALITY 39)." — this round ADOPTS the
   named-committed-receipt basis (see C1 leg 1 and the policy record in C2 R2);
   the two open L0 questions of round 28 are answered-by-implementation and remain
   open for operator overrule.
3. "commit receipts for the standalone leg runs next round (41/41 green; mutant
   0/2) — quoted-only evidence does not meet this lane's receipt convention."
4. "Residual §6.6 tenth record defect (docstring-citation overclaim): real,
   unclaimed, carried by the lane to r29 intent (RevengerNineDefects.md) — keep
   it on the routed queue." (`corpus/lessons/round-27-verifier-spotcheck.md`
   item 6: the round-27 report sentence "the tool's docstring and the knowledge
   entry cite them [S178–S182]" overclaims — the docstring cites upstream source
   filenames, only the knowledge entry frontmatter cites the S-ids.)

The round-28 claim records are NOT reopened: the r28 composite predicate
(`PRED-C1-r28 verdict=TARGET_MET`) stands missed at `77cdda86` with its
committed receipt; this round registers NEW predicates (`PRED-C1-r29`,
`PRED-C2-r29`) on repaired, re-frozen counters. The r28 frozen bytes
(`.ufo/waves/round-28/c1/count.py` and its `3d7d301f…` pin) are never edited;
the repaired counter lives at `.ufo/waves/round-29/c1/count.py`.

## Claims

**C1 — operability: the round-28 mutation composite is repaired and re-frozen as
a committed-bytes gate with zero vacuous legs.** Surface moved: the composite
counter gains (a) the count-v4 guard pin corrected from the never-matching
`3d7d301f…` to the committed bytes `635ae788fd897c8f…71a1` (M28-1), so the
boolword-v5 leg prints real tallies instead of `normal=missing mutant=missing`;
(b) leg `h1-rotation` re-based per QUALITY 39 from the cleaned ephemeral H1
directory (`/fast/scratch/hyaku/mado-r27/heldout`, M28-2) to the committed w2
receipt `.ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md`, named here at
data time as this leg's verification basis, owner: mado (the H1 bytes are
unrecoverable; preservation through adjudication is impossible retroactively —
the receipt basis is adopted instead, exactly the alternative QUALITY 39 names).
The composite is smoke-run once at freeze with its full output committed
(QUALITY 38). The standalone boolword-v5 runs (normal 41/41, mutant 0/2) gain
committed receipts (routed item 3). The command that shows it unmoved:
`python3 -I .ufo/waves/round-29/c1/count.py <REV>` at this registration commit.

**PRED-C1-r29** (frozen): At REV, `python3 -I .ufo/waves/round-29/c1/count.py REV`
exits 0 and prints `PRED-C1-r29 verdict=TARGET_MET`. Six legs, each over
committed bytes at REV:

1. `h1-receipt` — the committed bytes at REV of
   `.ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md` name
   `h_killed=18/18` with `verdict=TARGET_MET` on the new-suite run, carry the
   monotone verdict, and read each of `held-c1v2-node-subset`,
   `held-c1v2-missing-version-guard`, `held-c1v2-extra-output-segment` as
   `rc=1 KILLED`. (Verification basis per QUALITY 39; the ephemeral H1
   directory is absent and is not re-run.)
2. `boolword-v5` — `.ufo/waves/round-28/c1/count-v5.py REV --seed 28c1a8c0ffee0001`
   prints `PRED-C1-r28-v5 cases_pass=41/41 boolword_pass=2/2 verdict=TARGET_MET`,
   exit 0; the same command with `--tool-file
   .ufo/waves/round-28/c1/ref-mutants/exactbool-tool.py` prints
   `boolword_pass=0/2 verdict=TARGET_MISSED`, exit 1; the counter's guard pin
   for the frozen count-v4.py bytes matches the committed
   `635ae788fd897c8f…71a1`.
3. `h2-rotate` — the frozen round-27 counter on the committed round-28 set
   `../round-28/c2/heldout2/` with seal `../round-28/c2/heldout2-seal.txt`
   prints `verdict=TARGET_MET` (seal byte-equal at REV).
4. `refpub-kills` — the same counter on the committed public reference set
   `../round-28/c1/refpub/` with seal `../round-28/c1/refpub-seal.txt` prints
   `h_killed==h_valid` with `h_valid>=9` and `h_min_per_subject>=2`.
5. `q36-witness` — `bash quality/q36-successor-run.sh` exits 0 against the
   committed checker and `quality/q36-successor-receipts.txt` names both
   survivors.
6. `q37-open-ended` — `python3 -I quality/check-population.py --registration
   .ufo/waves/round-27/registration.md .ufo/waves/round-27/evidence/c2-after-0b53bd86.txt`
   exits 0 printing `verdict=PASS`; the frozen round-26 artifact keeps sha256
   `803e0096…d0f64`.

Legs 2–6 re-state the round-28 leg rules verbatim (same frozen subjects,
seals, seeds and predicates); the only rule changes are the guard-pin bytes
(leg 2 guard) and the leg-1 verification basis, both declared in the routed
queue before this round's data. The composite's AND-bit predicate sentence is
identical in plan, counter and receipt: "exit 0 and prints
`PRED-C1-r29 verdict=TARGET_MET`".

**C2 — calibration (lowest active scored axis): the four routed round-28
defects are repaired in committed records.** Surface moved: R1 — the guard-pin
repair is recorded with its red-before control receipt (the unrepaired
composite printing `verdict=TARGET_MISSED` with `normal=missing mutant=missing`,
committed under `controls/` before data); R2 — the ephemeral-input preservation
policy is adopted and recorded at data time: this registration names the
committed receipt basis and its owner (QUALITY 39, final sentence); R3 — the
standalone boolword-v5 receipts are committed under `evidence/`; R4 — the §6.6
tenth record defect is repaired by an append-only erratum in `SCORECARD.md`
(the round-27 section) naming the correct citation location of S178–S182.
The command that shows it unmoved: `python3 -I .ufo/waves/round-29/c2/count.py
<REV>` at this registration commit.

**PRED-C2-r29** (frozen): At REV, `python3 -I .ufo/waves/round-29/c2/count.py
REV` exits 0 and prints `CHECK R1..R4 PASS` and
`PRED-C2-r29 verdict=TARGET_MET`. At the registration commit it prints
`R1 R2 PASS` / `R3 R4 FAIL` (2 of 4 unresolved: the v5 receipts and the
§6.6 erratum land with the data commit); the do-nothing control
`C2K1-donothing` is scored at base `f652ca99` (no round-29 record exists
there) and prints `R1..R4 FAIL`, `verdict=TARGET_MISSED`, exit 1.

**Lowest-axis selection.** The latest bounded calibration score is the literal
lesson-citation rubric (QUALITY criteria citing lessons / all criteria;
SCORECARD round-24 row; unchanged as a side effect of round 28's criteria
38–40, re-measured this round) — the lowest active scored axis. Operability's
hermetic pass fraction is 10.0000; coverage's U-route sits at its finite
documentary ceiling as a harm watch. Calibration is lowest, so C2 works it;
C1 is the operability claim. Distinct axes, causally separable: C2 verifies
record facts (receipts, errata, registration text) that do not require the
composite to run green, and C1 verifies the running gate without requiring
the record repairs.

## Kill rule and controls (before data)

A control that meets a target under its frozen counter forces redesign of that
claim before data. Receipts under `controls/`, committed with the freeze:

- `C1K1-r28composite` — the do-nothing control for C1: the UNREPAIRED
  round-28 composite (`.ufo/waves/round-28/c1/count.py`, pin `3d7d301f…`) at
  base must MISS (`boolword-v5 … normal=missing mutant=missing`,
  `PRED-C1-r28 verdict=TARGET_MISSED`, exit 1) because the claimed work (pin
  repair + receipt basis) is exactly what it skips. Receipt
  `controls/C1K1-r28composite.txt`.
- `C1K2-pinonly` — the pin repaired but leg 1 still demanding the ephemeral H1
  directory (`controls/C1K2-pinonly-count.py`, a declared variant skipping only
  the receipt-basis change) must MISS on leg `h1-rotation` (`rc=2 no-tally`,
  `PRED-C1-r29 verdict=TARGET_MISSED`, exit 1). Receipt
  `controls/C1K2-pinonly.txt`.
- `C2K1-donothing` — the frozen C2 counter at this registration commit with no
  record repair must print `R1..R4 FAIL` / `verdict=TARGET_MISSED`, exit 1.
  Receipt `controls/C2K1-donothing.txt`.

## Data rule

- Smoke run (QUALITY 38): after the freeze commit, the composite is run once
  at the freeze commit and its full output committed at
  `evidence/c1-freeze-smoke-<freeze-hash>.txt`. A leg printing `missing` or
  SETUP_ERROR without its declared command failing is a freeze defect: fix and
  re-freeze before any data seat is created.
- Standalone v5 receipts: `.ufo/waves/round-28/c1/count-v5.py <final-content-rev>
  --seed 28c1a8c0ffee0001` and the same with `--tool-file
  .ufo/waves/round-28/c1/ref-mutants/exactbool-tool.py`, full outputs committed at
  `evidence/v5-standalone-normal.txt` and `evidence/v5-standalone-mutant.txt`
  (routed item 3).
- Measurement: C1 and C2 are measured once at the round's final content commit
  with the frozen counters; receipts committed under `evidence/`.
- `count-v5.py` may read only the committed synthetic HOME
  `../round-28/c1/synthetic-home/`; the operator's live `$HOME` is never read.
- Every suite run stays inside the frozen counters' sandboxes; the oracle
  build pins (`227a74af…`, `1f3d7036…`) are verified before receipt runs.

## Sourced claim (frontier step)

C1's public-reference leg method (mutants authored against the suite's actual
probe discriminators, M28-3's equivalent-mutant class) rests on a new
`corpus/SOURCES.md` row S184 opened this round: Schuler & Zeller, "Covering
and Uncovering Equivalent Mutants" (STVR 2013), opened at the DOI reader with
title-level grounding, tier A scoped to the equivalent-mutant question —
the same treatment S183 received in round 28. The round-29 lesson `## Gate`
records URL, access date and the located quote.

## Host safety

No compositor state, config tree or sibling repo is written. Pacman
transactions are paused host-wide; no tool install this round. Wave seats
would run under the same sandbox and read-only substrate rules as round 28.

## Saturation / axes

Saturation line 9.0 on every scored sub-axis; stagnation window N=3. A
capability row enters only if the composite runs end-to-end green at the
measured commit (no new capability is pre-claimed). No axis is retired or
split.
