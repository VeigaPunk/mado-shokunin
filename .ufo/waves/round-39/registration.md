# mado round 39 — registration (frozen before any round-39 data)

Base: `08be4eb7fd13358ed29b096e8924005d46ac409c` (lane tip at round start; attempt 1; the
watchdog shows no `lane-dead-no-report mado round=39` before this launch). This file, the
round-start receipts (`receipts/`), the inherited round-38 seat reports (resolved closed),
and the C1 re-registration material land in one freeze commit; any later change to a
counter, the frozen manifest or a declared target is a new predicate and the claim it
belongs to then fails as declared.

## Lowest-axis rule

`python3 -I quality/check-axis-scores.py --repo . --rev master` at the base prints
`navigation published=55/55`, `calibration published=50/50`, `operability published=12/12`,
`MADO_AXIS: checked=3 mismatched=0` (`receipts/axis-base.txt`) — every published axis ties
at its maximum, so each is a lowest axis; C1 works `calibration`. The stagnation nudge does
not apply: capability rows entered in rounds 37 and 38, inside the lane's window of N=3.

## Routed defects being worked (round-38 non-author closure, §6)

1. **Re-register the C1 repaired predicate** — C1 below. The round-38 pair as frozen failed
   (`frozen × frozen = 18/19`); the landed pair's 19/19 is a new predicate, re-registered
   here with a fresh freeze.
2. Correct the fleet round-38 report's refuted addendum-5 refinement (the "frozen pair
   19/19 at freeze rev" sentence, refuted by the lane's own errata c46f868/f551b70) in
   this round's report as an erratum naming the superseded text.
3. Regenerate `receipts/eventq-live-ss.txt`-style evidence as a census-only snapshot
   (SentSocketSafety HIGH — the committed full `ss -xpa` table carries unrelated pids) and
   commit a standalone after-receipt for the eventq counter.
4. Uncommitted round-38 seat reports (`w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md`)
   — inherited as uncommitted lane-authored work; committed in the freeze commit and named
   in the report.
5. SCORECARD "2 refused" → 3 staleness (round-38 lesson correction) fixed in the records
   update.

## C1 — calibration: the repaired discrimination pair is re-registered and shown to discriminate

- **Predicate:** `quality/check-r38-discrimination.py` plus the re-frozen manifest
  `.ufo/waves/round-39/c1/manifest.json` (`MANIFEST-r39-v1`, a byte copy of the repaired
  round-38 landed manifest at base, whose frozen `c1-duprow` control applied the registry
  row *inside* `## Registry`), with the uncontested counters `quality/counters/c1-r38-event-ground.py`
  and `quality/counters/c2-r38-eventq.py` unchanged at base.
- **Counting command:**
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev <rev>`
- **Before** (measured at base): the round-38 frozen manifest (`receipts/manifest-frozen-r38.json`)
  with the same counters prints `controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1
  (`receipts/c1-redbefore.txt`); the sole failing control is `c1-duprow` (expected MISSED,
  observed MET — the append-at-file-end row is outside the counter's `## Registry` parser).
- **Target:** the re-frozen manifest scores `controls=19 correct=19/19 verdict=TARGET_MET`,
  exit 0, measured at the freeze commit (and at the data tip).
- **Kill rule:** anything other than `correct=19/19` at the freeze commit is a miss, reported
  as an honest stop; no target narrowing.
- **Residual (declared):** fully fabricated, self-consistent artifacts (invented lineage
  phrases, invented inode triples) can still pass — the accept-path tradeoff the round-37/38
  clause tests already recorded; re-registration does not make live truth provable from
  committed bytes.

## C2 — operability (capability acquisition): the config-option ownership table tool

- **Deliverable:** `tools/mado-options.py` — static resolver of the config-tree option table
  (all non-bind/non-animation/non-workspace/non-rule `key = value` settings) through the
  Hyprland source graph, with last-declarer ownership resolution and an optional
  `--getoption <json>` live-value merge that reproduces the divergence vocabulary
  (`agreement` / `agreement*` / `live-default` / `mismatch` / `config-only`). Strict
  regular-file policy; no compositor, socket or network; Python stdlib only.
- **Predicate `PRED-C3-r39-v1`:** the docstring of `quality/counters/c3-r39-options.py`;
  the code is the same sentence.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>`
- **Before:** at base `tools/mado-options.py` does not exist (measured:
  `ls tools/mado-options.py` → exit 2) and the counter reports `tool=absent` exit 1.
- **Target:** `fixtures=N/N tool=present verdict=TARGET_MET`, exit 0, at the data commit.
- **Kill rule:** anything other than TARGET_MET at the data tip is a miss; no narrowing.

## C3 — coverage (sourced): the config-option ownership ground is admitted

- **Deliverables:** `corpus/knowledge/config-option-table-r39.md`, plus `corpus/SOURCES.md`
  rows S218 (Hyprland configuration/hyprlang option-syntax documentation, opened this round)
  and S219 (`own-work` row for the options tool, opened this round); both `mined`, both with
  Gate lines in the round lesson binding a committed receipt by sha256 and a located quote.
- **Predicate `PRED-C4-r39-v1`:** docstring of `quality/counters/c4-r39-options-entry.py`.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>`
- **Before:** at base no such entry exists and no row S218/S219 exists → `admitted=0/1
  verdict=TARGET_MISSED`, exit 1.
- **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0.
- **Kill rule:** as C2.

## Assimilation (rides C3/§10; no extra claim)

Package `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only). One theme: **the
dispatcher surface and request-socket resolution** — adopt the deferred amendment
`amendments/corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` (round-38
lesson: "an adoptable ... amendment, ~54 rows of real unheld ground ... deferred to round
39"). The amendment is appended as a dated section to the held
`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` (never replacing it), each
cited source re-opened this round (the 0.56.0 Dispatchers page → row S220; the held
`HyprCtl.cpp` row S018 gets `used-by` extended). The staged register remains
unassimilated; only the rows the admitted amendment cites are appended.
considerthese/2026-10-24.md proposal 4 (the config-option table, "who owns each key, checked
against getoption") is the mined proposal C2 implements; considerthese/2026-10-25.md
proposal 3 (watch M37-5 by name) is the C1 re-registration.

## Harm watch (every claim)

- `tools/mado-verify.sh --selftest` stays `MADO_SELFTEST: 460/460` (receipt
  `receipts/selftest-base.txt`).
- `quality/check-index.py` stays complete and only gains the new entry row
  (`receipts/nav-base.txt` baseline 55/55).
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exit 0 at
  round end (`receipts/census-before.txt` baseline exit 0).
- No config tree, compositor state, service, sibling lane or fleet-repo path is written;
  the lane's jj/git index is only touched by the lane helper.
