Draft rows for `SCORECARD.md`, round 34 (2026-10-24, attempt 1), in the
round-33 table style. Predicate id `PRED-C1-r34-v1` / `PRED-C2-r34-v1`; frozen
at `3420e827bd7b21b1374b23245526554ffd20d096`; data commit
`fa7ba11346116672352b5d41494141c5c4d738d0` (`fa7ba11`). Self-verdicts only;
pending the integrator's non-author verification.
Embed hazard: no line of this draft may contain the `r34-s189-line` marker
with a trailing colon followed by a non-`line=169` tail — the C2 counter
scores the LAST matching line and would flip to `TARGET_MISSED` if the
appended rows re-publish `line=128`, `other` or `absent`. The drafted rows
name the marker without that token sequence.


| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage — Waybar event-socket client, frontier → core: one entry `corpus/knowledge/waybar-module-text-route-r25.md` citing S201/S202 (the surface round 33 missed) | before (pre-data control `controls/c1-donothing.txt`, the frozen counter on the lane tree before the entry and rows): `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED`, exit 1; after (lane tree at `fa7ba11`, receipt `w1/reports/ExecC1Matrix.md` matrix.tsv row `lane` + this seat's re-run): `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET`, exit 0 | `python3 -I .ufo/waves/round-34/c1/count.py --root . --frozen .ufo/waves/round-34/c1/frozen.json` | target met on the lane tree, identical line to the golden control. Every committed non-golden control tree (symlink crib/entry/parent/sources, hardlink, rows-only, entries-only, used-by-prefix) misses identically `0/0/2` exit 1 — the round-33 crib shape is closed. Limit: the counter counts closed cites, not content; a missing root prints the same `0/0/2` miss as a fully broken tree (ExecC1Matrix). `TARGET_MET` is not a certification — the round-33 lesson stands; the frozen predicate was not rewritten after seats scored it. |
| C2 calibration — SCORECARD publication versus the pinned S189 fetch: the published queue-cap line must match the measured line of `.ufo/waves/round-32/fetch/S189.bin` (sha256 `eea605df…9540d`) | before (pre-data control `controls/c2-donothing.txt`, lane `SCORECARD.md` before the marker): `published=absent measured=169 mismatch=1 verdict=TARGET_MISSED`, exit 1; after (lane `SCORECARD.md`, receipt `w1/reports/ExecC2Matrix.md` row 1 + `RevC2Matrix.md` row 1 + this seat's re-run): `published=169 measured=169 mismatch=0 verdict=TARGET_MET`, exit 0 | `python3 -I .ufo/waves/round-34/c2/count.py --repo . --scorecard SCORECARD.md --frozen .ufo/waves/round-34/c2/frozen.json` | target met. The sole publication marker added at `SCORECARD.md:2108` by `fa7ba11` publishes `line=169`; ground truth confirmed by `RevC2Truth.md` (sha256 match, line 169 strip-equals the literal, line 128 does not). Kill controls hold: `line=128` card → MISSED (`controls/c2-junk.txt`), no-marker card → MISSED; last-marker-wins proven by `ExecC2Matrix`'s superseded-marker card. Limit: the marker is lane-local — absent from the fleet-root SCORECARD; `measured=169` is invariant, the card alone moves the verdict. |

Receipts and re-runs (non-author seats, read-only executions):
`w1/reports/ExecC1Matrix.md` (10-tree matrix), `w1/reports/RevC1Matrix.md`
(re-run, same 10 results), `w1/reports/ExecC2Matrix.md` (5-card matrix),
`w1/reports/RevC2Matrix.md` (re-run, 5 rows), `w1/reports/RevC2Truth.md`
(ground truth), `w1/reports/RevPredicateText.md` (predicate byte-identical in
`count.py` PREDICATE + docstring, `frozen.json`, `registration.md` — no drift).
Controls: `.ufo/waves/round-34/controls/*.txt`, committed pre-data at `3420e82`.
This seat's own re-runs (2026-10-24, lane HEAD `fa7ba11`): both commands above
printed the `TARGET_MET` lines quoted in the after columns, exit 0.
