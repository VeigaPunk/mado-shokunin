# ScrRowsDraft — registry rows S290-S299 (round 43, w1)

Seat scope: draft the ten 11-column rows for `corpus/SOURCES.md` from the ten receipts the L1 pinned
in `.ufo/waves/round-43/fetch/`, check each location against the lane registry, and validate the
result with `scripts/sources-census.sh validate`. Lane repo `mado-shokunin`, base `a35cfdf`, freeze
`b2e2efd`. No subagent dispatched (leaf). No product file, counter, control, registration or fetch
receipt was edited; nothing outside `.ufo/waves/round-43/w1/ScrRowsDraft/` was written.

## Behavior delivered

- `rows-block.txt` — the ten table rows, table rows only, NF=13 (11 cells), no `|` inside a cell.
  They append at the end of the `## Registry` table (after S289, before the blank line above
  `## Paths`).
- `rows.md` — decision log, per-row anchored facts, verification and limits.
- Receipts: `url-fetch-check.txt`, `own-work-check.txt`, `clause-e-check.txt`,
  `census-validate.txt`, `census-mutants.txt`.

Row summary: S290 `RegexMatchEngine.cpp` (flag inversion + `FullMatch`), S291 `WindowRuleApplicator.cpp`
(size/float/center stored in `static_`), S292 `DefaultFloatingAlgorithm.cpp` (first-map size
evaluation), S293 `Target.cpp` (box store), S294 `WindowTarget.cpp` (desired geometry from the client),
S295 `GeometricMovableAnimated.cpp` (goal vs current), S296 `HyprCtl.cpp` (`size` is `GEOMETRIC_GOAL`),
S297 `host-gkeep.conf`, S298 `host-clients-r43.json`, S299 `gkeep-ui-excerpt.py` (own-work, kind
`own-work`, tier A). All `mined`, opened `2026-10-26`, used-by
`corpus/knowledge/hyprland-gkeep-geometry-r43.md`; recheck `on-release` for the seven upstream rows and
`2027-01-24` for the three own-work rows.

## Gates run

1. **URL serves the receipt** — seven `curl` fetches of the tag-form URLs (`v0.56.2`), HTTP 200 and
   sha256 equal to `receipts/fetch-sha256.txt` for all seven: `url-fetch-check.txt` (MATCH 7/7).
2. **Own-work receipts true to their rows** — `own-work-check.txt`: `host-gkeep.conf` byte-identical
   to the live `~/.config/hypr/gkeep.conf` (`cmp` clean, 264 B, `3726e488…`); `gkeep-ui-excerpt.py` is
   exactly `sed -n '446,$p'` of the 488-line `ui.py` (full-file `07a3c4a5…`) plus its two header lines,
   no body diff; `host-clients-r43.json` matches a live read-only `hyprctl clients -j` on
   class/size/floating/mapped for all four clients, no gkeep window, `hyprctl version` = 0.56.2 at
   `efb5099…`.
3. **Location uniqueness and clause-e containment** — `clause-e-check.txt`: ten of ten locations
   unique and their last path component containing/contained by the receipt file name
   (`clause-e-parity: PASS`).
4. **Census validate, exit 0 required and obtained** — `census-validate.txt`:
   `cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`
   → the eight warnings the untouched registry already emits (seven W04, one W01), `file ok`, `exit=0`.
   Baseline on the real file before the rows: the same eight warnings, exit 0. Re-run on the final
   row bytes after the two anchor corrections below: same eight warnings, `exit=0`.
5. **The duplicate check can fail** — `census-mutants.txt`: S290 copied as S300 → `E04 … within
   scope …`, exit 1; S291 copied with the tag rewritten to the commit → `file ok`, exit 0 (the measured
   basis for the tag-vs-commit separation); restored mirror → `file ok`.

## Held rows and the decision taken

`grep -c` over the lane registry per path: `RegexMatchEngine.cpp` 0, `DefaultFloatingAlgorithm` 0,
`Target.cpp` 0, `WindowTarget.cpp` 0, `GeometricMovableAnimated` 0, `WindowRuleApplicator` 2 (S155
plus the S156 `.hpp`), `HyprCtl.cpp` 2 (S018 and S158). Two of the ten receipts therefore already
have a row over the same bytes at the same commit, under the **commit-form** URL:

- **S155** `…/efb5099…/src/desktop/rule/windowRule/WindowRuleApplicator.cpp`, anchor `:378-509`.
- **S158** `…/efb5099…/src/debug/HyprCtl.cpp`, anchor `:346-484`; **S018** the `github.com/blob/…`
  docs-facing form of the same file.

Decision: **new rows S291 and S296 at the tag-form URL** (the URL the L1 actually fetched), with
narrower anchors (`:421-428`, `:389-395`, `:429-433`; `:395`, `:427-428`, `:447-448`). The tag token
differs from every held row's token, so census E04 and counter clause e both hold — proved by mutant
B, not asserted. Cost stated: these two rows overlap S155's and S158's ranges. The dedupe reversal
(delete S291/S296, cite S155/S158, add their used-by items) is mechanically admissible to the counter
— clause c keeps a held id's cells 1-9 byte-equal and only adds used-by items — but it is withdrawn on
`ScrEntryA`'s evidence: the entry's chain needs S291 (rule storage) and S296 (the `clients -j` goal
field), and clause c is per cited id, so a held-id citation forces the entry's ids, `GATE` lines and
receipts to be rewritten in lockstep. S291 and S296 stay as drafted.

## Findings

- **Two draft anchor errors, both corrected before handoff.** (a) S297 said `4 lines, 264 B` for
  `host-gkeep.conf`; `wc -l -c` reports `5 264` on both the receipt and the live host copy — four
  content lines plus a trailing empty line 5 (`od -c` tail `$ \n \n`). Reported by `ScrSkillProvince`
  (and earlier by `ScrEntryA`), re-measured here in `host-conf-lines.txt`; the anchor now says
  `5 lines (4 content plus an empty line 5, wc -l -c reports 5 264)`. (b) S298 said `:3-60` for a
  62-line file whose four client objects start at lines 3, 18, 33, 48; `:3-60` stopped one line
  short of the fourth object's closing brace, so the anchor now cites those four `address` locators.
  Byte counts and sha256 in both anchors were already right.
- **Round-42 prose locator defect confirmed independently**: the `size` field of `clients` is at
  `Hyprland-HyprCtl.cpp:427-428` (JSON branch) and `:448` (plain branch), not `:394-395,412-413`;
  `Hyprland-RegexMatchEngine.cpp:7-8` holds the `negative:` test and `:16` holds the `FullMatch`
  comparison, not `:10-16`. Both ranges were read from the pinned receipts with `nl -ba`.
- **The excerpt regeneration is clean**: the round-43 `gkeep-ui-excerpt.py` differs from a freshly cut
  `sed -n '446,$p'` only by its two header lines; the round-42 extra blank line is gone.
- **Rule and client request give the same number on this host** (420x500 in `host-gkeep.conf:4` and
  `set_default_size(420, 500)` at `gkeep-ui-excerpt.py:33`), which is why S299's teaches says an
  agreement cannot tell which value produced the reported size. This is a fact about the host pair,
  not a measurement of the window — no gkeep window was open.
- **Census weakness worth knowing for the integrator**: E04 only fires on identical URL *and* scope
  text, so a duplicate location under different scope prose passes the census; the C2 counter's
  clause e is the stricter check (exact location token). The drafted rows satisfy the stricter rule.

## Out of scope / not run

- The C2 counter (`quality/counters/c2-r43-gkeep-entry.py`) was **not** run: it scores a committed
  entry that does not exist yet. Clause-e parity was recomputed by my own script instead; clauses
  b-d and f-i are the C2 author's and the L1's.
- `corpus/SOURCES.md` was **not** modified (outside this seat's write scope; the L1 appends
  `rows-block.txt`).
- No tool installed, no package transaction, no host mutation; compositor reads were limited to
  `hyprctl version` and `hyprctl clients -j`.
- Scratch `/fast/scratch/hyaku/mado-r43/ScrRowsDraft/` (2.7 MB) was deleted after the receipts were
  copied here. The mirror's only non-reproducible part is a one-line placeholder
  `corpus/knowledge/hyprland-gkeep-geometry-r43.md` inserted **in the mirror** so E11 would not fire
  on a used-by path the C2 author has not written yet; that placeholder was never a lane file.

## Artifacts (`mado-shokunin/.ufo/waves/round-43/w1/`)

- `ScrRowsDraft/rows-block.txt` — the ten rows (deliverable).
- `ScrRowsDraft/rows.md` — decisions, anchored facts, limits.
- `ScrRowsDraft/url-fetch-check.txt` — 7/7 HTTP 200 + sha256 MATCH.
- `ScrRowsDraft/own-work-check.txt` — host config, excerpt, live clients census.
- `ScrRowsDraft/host-conf-lines.txt` — `wc -l -c` = `5 264` for the receipt and the live host copy,
  `od -c` tail, `cmp` clean (the S297 line-count correction).
- `ScrRowsDraft/clause-e-check.txt` — uniqueness + containment, PASS (re-run on the final bytes).
- `ScrRowsDraft/census-validate.txt` — `file ok`, `exit=0`.
- `ScrRowsDraft/census-mutants.txt` — E04 probe fires, tag-vs-commit probe clean.
- `ScrRowsDraft.md` — this report.

Report: .ufo/waves/round-43/w1/ScrRowsDraft.md
