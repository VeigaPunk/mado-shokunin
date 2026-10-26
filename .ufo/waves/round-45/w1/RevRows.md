# RevRows-2 seat report (round 45 w1) — FINAL

Seat: review draft registry rows S302-S310 + Gate lines built by
`.ufo/waves/round-45/l1-draft/build-pos.py` against CORPUS.md contract v1
(§ SOURCES.md), the pinned receipt bytes, and held rows S158/S162.

Full findings: `.ufo/waves/round-45/w1/RevRows/review.md` (row | verdict | fix).

## Verdict

**All nine rows PASS; no blocking defect.** Four optional nits/strengthenings
listed in review.md § Findings summary (S307 disabled-outputs corroboration via
wiki-Monitors.md:23-26; S303 v2 range 788-893; S302 "empty or auto" wording;
S307 anchor start 223).

## Checks performed (evidence in .ufo/waves/round-45/w1/RevRows/receipts/)

- URL re-fetch: all 9 row URLs re-fetched 2026-10-26; sha256 all equal the
  frozen pins (`refetch-sha256.txt` vs `fetch-sha256.txt`); row URLs byte-equal
  the counter's PINS_URL table.
- Anchor ranges: every named function located by grep -n and confirmed inside
  its claimed range — parseMode 110 / parsePosition 145 / parseScale 193 /
  parseTransform 213; handleMonitor 1293-1387 / handleMonitorv2 788-880; add
  37-42 / get 44-117; CMonitorRule fields exactly 41-69; applyMonitorRule
  exactly 719-1082 / matchesStaticSelector exactly 1201-1211 / descriptions
  250-256; getMonitorData JSON inside 224-288 / monitorsRequest 313-345;
  arrange 16 + explicit 21-38 + auto 61-101; isNumber 46 / isNumber2 50-84;
  wiki General 6 / colour 240-260 (sdr_eotf 253) / Monitor v2 292
  (`locators.txt`).
- Teaches cells: each clause verified against the pinned bytes (citations in
  review.md), including the census-line values 60 / 1 / 1/120 / 89 / 5 / 8.
- Gate quotes: all 9 occur exactly once (whitespace-normalized) in their own
  receipt, in no other cited receipt, 3-25 words (`quotes-check.txt`); counter
  clause g locator lines match the entry's citations.
- S158/S162 cross-scope: scopes and anchor ranges disjoint from S303/S307 —
  new rows justified; census emits exactly the declared W04s and nothing
  worse; counter clause e admits.
- Positive control: clone of freeze 22a8dedd in scratch, build-pos applied,
  committed e6dc808bf265bcefab05d982eff5da15c5d3003e (4 files +113);
  `scripts/sources-census.sh validate` exit 0 `file ok` (`census-pos.txt`);
  frozen counter `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET` exit 0
  (`c2-counter-pos.txt`).
- Wiki anchor date 2026-04-20 verified via GitHub commit API
  (2026-04-20T16:33:26Z).

## Tooling record

No tool installed or updated (pacman untouched). Used only: curl (re-fetch),
system python3 (quote checker), read-only git, the fleet census script, and
the frozen counter.

## Safety

Writes confined to `.ufo/waves/round-45/w1/RevRows/` (review.md + receipts/)
and this report file. Lane untouched (read-only git only). Scratch
/fast/scratch/hyaku/mado-r45/RevRows deleted after receipts were copied.
