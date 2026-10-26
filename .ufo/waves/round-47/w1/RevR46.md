# RevR46 — round-46 landed-state review (round 47 w1)

Reviewed the round-46 landed state at base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`
(round-46 closure commit; data tip `edc1478` is its ancestor), non-author, leaf seat.

## Re-measurements (all reproduce)

- C1 `PRED-C1-r46-v3` at the base rev: `fixtures=110/110 generated=150/150 selftest=ok
  readonly=ok tool=present verdict=TARGET_MET` exit 0, fresh nonce `seeds=46,1121157060`
  (differs from all three committed receipts' nonces — four independent nonces pass).
  Receipt: `receipts/c1-rerun-r47.txt` (this seat dir).
- C2 `PRED-C2-r46-v2` at the base rev: `clauses a-k all 1 admitted=1/1 verdict=TARGET_MET`
  exit 0. Receipt: `receipts/c2-rerun-r47.txt`.
- Tool selftest from committed bytes (`git cat-file blob 60edb66:tools/mado-devices.py`,
  sha256 `3a803689…`): `MADO_DEVICES_SELFTEST: 59/59 passed` exit 0.
- `.ufo/waves/round-46/w1-results.json`: seats=66, n=66, nulls=0.

## SCORECARD Round 46 vs receipts

Every cell traces: C1/C2 before-after strings verbatim (`c1-v3-before-base.txt`,
`c1-after-data.txt`, `c2-v2-before-base.txt`, `c2-after-data.txt`, `c2-tip.txt`); controls
`ctl-c1-v3.txt` PASS 0 of 40 exit 0 and `ctl-c2-v2.txt` PASS wrong 0 of 22 exit 0; live run
`live-devices-host-r46.txt` keyboards=10 agree=9 virtual=1 mice=4 OK exit 0 with tool sha256
`3a803689…`; report's v1 controls (0 of 23; P + 14 rejected = wrong 0 of 15); knowledge 62→63;
SOURCES 252→262 (+10/−0); SCORECARD +29 pure append; session-material findings=115 with exactly
18 FINDING lines in round-46 files; M46-1..16, QUALITY 87-90, LOG bullets, PROVINCE +15, ten
pins, ScoutRecheck — all present. Fleet report commit `b25732fc` by the lane identity after the
lane tip. No discrepancy found in any SCORECARD Round 46 number.

## Defects beyond R1-R4 (all citation-layer; details in review.md)

- **D1 (LOW)** — `SCORECARD.md:2646` cites `receipts/axis-data.txt` "re-derived at `1001bda`…
  navigation 63/63; calibration 77/77", but that receipt at that rev reads `mismatched=2`,
  STALE×2, `exit=1`; the MATCH rows are `axis-tip.txt` at `9879964`. Rounds 40/41 named the
  records commit in this line (`SCORECARD.md:2493`, `:2521`); rounds 45/46 dropped the clause
  (`:2617`, `:2646`). The round report discloses the window honestly.
- **D2 (LOW-MED)** — `SKILL.md:2129/:2134/:2137` cite bare `receipts/synthetic-verdicts.txt`;
  the file exists only at `.ufo/waves/round-46/w1/ScrSkill/receipts/`, not in
  `.ufo/waves/round-46/receipts/` which the same section cites full-path at `:2121`. Only three
  bare `receipts/` citations in all of SKILL.md — dangling under the section's own convention.
- **D3 (LOW-MED)** — `SKILL.md:2134` quotes "an unmodelled line can change any expectation" at
  `mado-devices.py:87`; the quote is at `tools/mado-devices.py:98-99` (`:87` is the
  mouse-factor/MATCHED sentence). Same class as routed R4-F1.

## Observations (not defects)

- The landed tool is byte-identical to the C1 counter's reference model (blob `2f7c5288…` for
  both `tools/mado-devices.py` and `.ufo/waves/round-46/v2/mado-devices.py`), so clause g's
  150/150 is tautological for this tool — inside the counter's declared residuals
  (`quality/counters/c1-r46-devices-v3.py:57-63`); discriminative weight is on clause f/r, the
  w1 independent rebuilds, and the closure's live check. Flagged for the L1's freeze.
- Discernment extended: re-fetched S319/S322 pins byte-identical to their Gate sha256s, quotes
  at the counter's locators (:113, :41) — 7 gate admits re-opened total with the closure's 5/5,
  0 disagreements. Pins stored at `receipts/pins/` with URLs (review.md §5).

## Verdict

Round 46 re-verifies at `60edb66`; three new citation-layer defects (D1 LOW, D2/D3 LOW-MED),
none in R1-R4, none touching claim substance. No axis harmed; runs read-only; no tool installs.

Full detail: .ufo/waves/round-47/w1/RevR46/review.md

Report: .ufo/waves/round-47/w1/RevR46.md
