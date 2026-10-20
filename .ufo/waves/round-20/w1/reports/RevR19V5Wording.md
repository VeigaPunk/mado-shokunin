# RevR19V5Wording — Correct the OM10 assertion count

## Findings

### Low — SCORECARD and round-19 report repeat the incorrect “ten” count

`SCORECARD.md:1225-1226` says “the ten old OM10 assertions were replaced by OM10A/B; no other prior assertion lost.” The closure at `corpus/lessons/round-19-verifier-spotcheck.md:88` gives the measured correction: exactly **nine old labeled assertion occurrences (eight distinct)** disappeared, all OM10, and were replaced by **OM10A six + OM10B eight**. It explicitly identifies “ten old assertions” as a counting defect.

**Draft replacement for the SCORECARD sentence and the repeated round-19 report sentence:**

> Gate selftest 389 → 460: exactly nine old labeled assertion occurrences (eight distinct), all OM10, were replaced by OM10A (six) and OM10B (eight); no shared label disappeared.

The read-only round-19 report repeats the incorrect wording at `.ufo/reports/round-19/mado.md:109-110` (“the ten old OM10 assertions were replaced by OM10A/B, no other assertion lost”), so it needs the same count correction. The exact-phrase search across that report and `LOG.md` found the phrase in the report only. `LOG.md:1302-1304` has a related but non-counting shorthand, “OM9/OM10,” among routed fixes; it does not repeat the “ten old OM10 assertions” claim.

**Evidence captured:**

- Read `SCORECARD.md:1225-1226`: `Gate selftest 389 → 460: the ten old OM10 assertions were replaced by OM10A/B; no other prior assertion lost.` SHA-256 `0139a1a403d4a0e431106e9d7fe70009daa86b7016e7dbbc81292d4593e62914`.
- Read closure `round-19-verifier-spotcheck.md:88`: `Exactly nine old labeled assertion occurrences (eight distinct) disappeared, all OM10, replaced by OM10A six + OM10B eight.` SHA-256 `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0`.
- Read report `.ufo/reports/round-19/mado.md:108-113`; the count appears on lines 109-110. SHA-256 `117207f08ad75747c5583175f76ff775ff5bb7cf91e34c0c557532213c0c57c9`.
- Case-insensitive exact-phrase search (`ten old OM10 assertions|ten old assertions|ten OM10 assertions`) across the report and `LOG.md`: report line 109 matched; no `LOG.md` match. A broader `OM10` search in `LOG.md` returned line 1303 (`OM9/OM10, PIN re-cut, 389/389, regression 10/10`). `LOG.md:1302-1304` SHA-256 `27f6bb64e3ba816b31fba1fc35968b08916829c206cbccb5eb86a449cce56769`.

## Residual risk and verification gaps

This review did not independently enumerate the assertion labels; the corrected counts and replacement split are taken from the cited round-19 closure. The report and SCORECARD remain unchanged; this deliverable records a proposed correction only.

## Limits

No selftest, source-label census, or other round-19 gate was executed.

## Installs

None.
