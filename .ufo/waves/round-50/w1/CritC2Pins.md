# CritC2Pins — round-50 re-fetch and census review

Status: blocked on absence of round-50 candidate rows/pins. I inspected the round-50 wave directory; it contains no candidate registry/rows or fetch directory yet. The only identifiable proposals are round-49 `candidate/rows.md` S352–S363 and `round-49/fetch/` (15 pins). Round-50 claim requires those rows to be reopened this round under round-50 pins/receipts, and the assignment explicitly requires checking the newly appended candidate registry. I will not treat old bytes or absent artifacts as a successful re-fetch/census.

Evidence:
- `claims.md:14-19` says rows are opened/appended this round and compared byte-for-byte with round-49 pins.
- `corpus/lessons/round-49-verifier-spotcheck.md:97-103` records prior S359-only re-fetch and census; it does not establish current-round validation of S352–S363.
- Round-50 directory listing (read tool) showed `w1/` seat outputs, claims, receipts, and assimilation only; no candidate rows/fetch or registry copy.
- Prior proposal is `.ufo/waves/round-49/candidate/rows.md` (S352–S363); old pins are `.ufo/waves/round-49/fetch/` (15 files). No fresh URLs, hashes, locators, quotes, or census outputs were produced, so these checks remain unverified.

Verdict: no finding about source correctness; insufficient current-round artifacts to verify the requested pin equality, line/quote anchors, census schema/date fields/duplicate scope/used-by, or `sources-census.sh validate --file`. Smallest safe correction: provide the round-50 candidate rows/registry and round-50 fetch copies/receipt; then re-fetch each commit/tag URL and run the mandated validator against a scratch copy. Do not claim these checks passed until those outputs exist.
