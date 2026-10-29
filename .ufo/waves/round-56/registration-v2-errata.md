# Round 56 — registration v2 errata (written after integration, before wave 2; disclosed, not a predicate change)

`registration-v2.md` and `frozen-tables-v2.json` stay byte-identical (commit `323a69c9`). Two integration facts the report repeats:

**E12 — `lost` is defined over the 65 base-missing pairs.** `registration-v2.md` §C3-v2 says `lost` counts pairs of PAIRS(base) that left
PAIRS(rev), "its sorted `S###|path` lines ... have sha256 `c3.base_pairs_sha256`". The frozen hash `630007b0…` was computed over the 65
pairs the v1 `missing` count found at the base revision, not over all 381 pairs of PAIRS(base) (`frozen-tables-v2.json` c3 carries
`base_pair_count: 65`). The first run of the integrated counter failed closed on the hash ("base pairs hash differs from the frozen
value"), which is the registered behaviour; the counter was then aligned to the frozen value: `lost` = base-missing pairs (entry path not in
used-by at the base) that are no longer in PAIRS(rev). Deleting the 65 citations is therefore caught; deleting a citation of one of the other
316 pairs is not (it cannot reduce `missing`). The integration counter is `quality/counters/c3-r56-used-by.py` (`base_pairs`).

**E13 — used-by separator.** The registry's `used-by` cell is comma-separated (census E11 splits on commas); the first integration of the
41 filled pairs joined appended paths with spaces, which the census reported as E11 "used-by path missing on disk" (23 rows). Fixed
before wave 2 (`corpus/SOURCES.md` at `0ff41272`); the counters' regexes accept both separators, so only the census could see it.
**E14 — the bare `content` leg.** The first integrated C1 counter printed a bare `content` leg when `e<33`; the registered leg grammar has none
(registration-v2 E5: "the name `content` is not a leg") and the C1 harness refused the line (8/12). The counter no longer prints it
(`28fc86ac`); `content=<e>/33` carries the shortfall.
