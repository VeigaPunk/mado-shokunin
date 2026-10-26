# ConnCalibration — round-45 w1 seat report

Seat: ConnCalibration. Task: count self-assessment mismatches at the base
`0c89478af821a6424c9ac922eafe02e39630cf4f` (round-45 base; parent `8ac15c41` =
round-44 lane tip), with round-44 closure D2/D3/D7 follow-through.

Result: **6 mismatches** — details, observed bytes and reproduction commands in
`w1/ConnCalibration/mismatches.md` (final line `mismatches=6`).

Checkable claims that matched (no mismatch):

- SCORECARD Round 44 numerics: C1 base `fixtures=11/26 … TARGET_MISSED` exit 1
  (receipts/c1-v2-before-base.txt); C2 base `admitted=0/1` exit 1
  (receipts/c2-v2-before-base.txt); C1 after `fixtures=26/26 TARGET_MET` exit 0,
  `selftest=94/94` (receipts/c1-after-data.txt; re-run of
  `tools/mado-geometry.py --selftest` at base reproduced `94/94 passed`);
  live receipt `NO_MATCHING_CLIENT` exit 3, `clients=3`, every `fullscreen` 0
  (receipts/live-geometry-host-r44.txt); axis data 61/61, 71/71, 12/12
  (receipts/axis-data.txt); sources 238 rows, S298-S301 tier A `mined` opened
  2026-10-26, S164 used-by extended (corpus/SOURCES.md:176,247-250); knowledge
  entries 61; QUALITY 82-84 (corpus/QUALITY.md:411,413,415), incl. the
  `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` line re-run from
  `quality/ratio-domain-meta.py`; `tools/mado-geometry.py` byte-identical to
  `c1/ctl-ref-tool-v2.py.txt` (sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4).
- SHONEN.md: four `[~]` boxes; all three pointer files exist
  (corpus/knowledge/executor-test-sufficiency.md, config-health-report-r3.md,
  province-accuracy-selfaudit.md).
- LOG.md Round 44: census before receipt exit 0; controls C1 0 of 15, C2 0 of 3;
  v2 controls 0 of 20 / positive admitted, 10 of 10 do-nothing/forged rejected;
  w1 38 seats/38 results (w1-results.json); spec commit `ae996fcf` exists; pins
  under fetch/ (5 files) and fetch-c1/ (3 files); id-guard collisions 42
  (assimilation/id-guard.md:7); quarantine slice 13 rows (registration.md:80);
  README index row (corpus/README.md:72) and Frontier route (:304); SKILL.md
  FULLSCREEN/MAXIMIZED/NOT_COMPARED rows and TILED correction (SKILL.md:293);
  PROVINCE geometry-row note.

Routed-defect status (round-44 closure):

- D2 — **open**: SCORECARD.md:2570/:2571 still give the after-state as
  "see receipts/c1-after-data.txt" / "see receipts/c2-after-data.txt" with
  self-verdict "recorded in the round report from the receipts"; no after value.
- D3 — **open**: tip receipts name `74c606a` (not tip `8ac15c41`); no receipt
  states the equivalence. De-facto equivalence verified:
  `git diff --name-only 74c606a 8ac15c41 | grep -v '^.ufo/waves/round-44/'`
  → empty.
- D7 — recorded findings (w2/ConnCalibration.md F1-F6): F1 (LOG mistake range)
  **open**; F2 (renumber-map.tsv citations) **open**; F5 (w1 paths) and F6
  (check83.py) resolved temporally — all 848 w1 files and
  `w1/ScrQualityCriteria/check83.py` exist at base; F3 (SKILL.md hosts=4 vs live
  receipt clients=3) still present as a placement artifact; no appended errata
  found (lesson has no round-44 errata section; no ConnCalibration mention).

Environment: no tools installed (python3 stdlib; read-only git). Scratch
`/fast/scratch/hyaku/mado-r45/ConnCalibration/` (clone of the lane at the base
commit) used and deleted before finish.
