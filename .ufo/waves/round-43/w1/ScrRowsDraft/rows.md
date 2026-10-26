# Rows S290-S299 — draft for `corpus/SOURCES.md` (round 43, wave w1)

Seat: `ScrRowsDraft`. Drafted 2026-10-26 against the frozen registration
(`.ufo/waves/round-43/registration.md`, freeze `b2e2efd`, base `a35cfdf`).
Deliverable: ten 11-column rows, `status mined`, `opened 2026-10-26`, used-by
`corpus/knowledge/hyprland-gkeep-geometry-r43.md` — table rows only in `rows-block.txt`,
this file for the reasoning. Nothing outside this seat directory was written.

Schema (as the Registry table declares): `| id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by |`. Every drafted row parses as NF=13 / 11 cells, and no cell
contains `|` (`awk -F'|'` over the block: NF=13 on all ten).

## 1. Decision log

**1a. Upstream locations: the tag form, not the commit form.** The L1 fetched all seven Hyprland
files from `raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/<path>`, so the tag URL is the URL
that actually served the pinned bytes. Two of the seven already have registry rows under the
*commit*-form URL of the same bytes:

| held row | location it holds | shares bytes with |
|---|---|---|
| S155 | `…/Hyprland/efb5099…/src/desktop/rule/windowRule/WindowRuleApplicator.cpp` (anchor `:378-509`) | S291 |
| S158 | `…/Hyprland/efb5099…/src/debug/HyprCtl.cpp` (anchor `:346-484`) | S296 |
| S018 | `github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp` (docs-facing form) | S296 |

`grep -c` per path over the lane registry: `RegexMatchEngine.cpp` 0, `DefaultFloatingAlgorithm`
0, `Target.cpp` 0, `WindowTarget.cpp` 0, `GeometricMovableAnimated` 0, `WindowRuleApplicator` 2
(S155 + S156 `.hpp`), `HyprCtl.cpp` 2 (S018 + S158).

Decision: **new rows** for all ten, with the tag-form location. Reasons and the cost:
- The tag form is a different location token from every held row, so census E04 (URL+scope) and
  the C2 counter's clause e (location token unique across rows) both hold. Proved:
  `census-mutants.txt` probe B rewrites S291's source URL to the commit form and the census goes
  clean (no E04) *because* the two tokens differ — i.e. the separation is the tag, not the scope text.
- Cost, stated plainly: S291 overlaps S155's `:378-509` anchor and S296 overlaps S158's `:346-484`.
  The new rows narrow their anchors to what the gkeep entry needs (`:421-428` size/`:389-395`
  float/`:429-433` center; `:395`, `:427-428`, `:447-448`), which S155/S158 cover only as part of
  a range. **Reversal (now withdrawn):** dropping S291/S296 and appending the entry to S155's/S158's
  used-by cell is mechanically admissible to this counter (a held id's clause-c branch keeps cells
  1-9 byte-equal and cell 10 only gains items; the three own-work ids clause h requires are
  untouched). It is withdrawn for this round on evidence from the other seats, not on counter
  grounds: `ScrEntryA` reports the entry's chain needs S291 (where the size rule is stored) and S296
  (where `clients -j` prints the goal), and clause c is per *cited* id, so a held-id citation would
  force the entry's id tokens, its `GATE` lines and their receipts to be rewritten in lockstep with
  this block — a coordinated rewrite the entry author rules out. S291 and S296 therefore stay.

**1b. Own-work locations** are repo paths under this round's fetch dir, so the last path component
equals the receipt file name (counter clause e containment, both directions). The three own-work
rows are the three rows clause h requires: `host-gkeep.conf`, `host-clients-r43.json`,
`gkeep-ui-excerpt.py`, kind `own-work`, tier A.

**1c. recheck.** The seven upstream code rows carry `on-release` (symbolic; the census reports the
cadence and never judges it overdue). The three own-work rows are dated snapshots of a moving host,
so they carry an ISO date `2027-01-24` (opened + 90 days).

**1d. Anchors.** Every anchor is a line range in the receipt plus the tag/commit and the receipt's
sha256 and byte size, following the S155/S283-289 shape. The line numbers were read out of the
pinned receipts with `nl -ba`, not carried over from round-42 prose — the round-42 prose's
`Hyprland-HyprCtl.cpp:394-395,412-413` and `:10-16` locators were the routed defect, and the
round-43 values re-derived here are `:427-428`/`:448` (JSON and plain branches of the `size` array)
and `:7-8`/`:16` (`negative:` prefix, `FullMatch` comparison).

Anchored facts, each at a locator inside a pinned receipt:

| row | locator | fact used |
|---|---|---|
| S290 | `RegexMatchEngine.cpp:6-13,15-17` | `negative:` is stripped and the result of `FullMatch` is compared against the negation flag |
| S291 | `WindowRuleApplicator.cpp:421-428` | `size` stores an `SExpressionVec2` (or clears it when empty) in `static_.size` |
| S291 | `WindowRuleApplicator.cpp:389-395,429-433` | `float` sets `static_.floating`, `center` clears position and sets `static_.center` |
| S292 | `DefaultFloatingAlgorithm.cpp:49-66` | first-map branch evaluates `static_.size` and overwrites the box width/height |
| S292 | `DefaultFloatingAlgorithm.cpp:16,34-38,79-84` | 640x400 fallback, work-area centring, `center` rule re-centres |
| S293 | `Target.cpp:10-18,64-74` | the target stores and rounds the box it is handed; last floating size kept separately |
| S294 | `WindowTarget.cpp:36-40,69-78,297-304,306-396` | floating branch hands the box to the window; desired geometry is the client's geometry clamped by min/max |
| S295 | `GeometricMovableAnimated.cpp:8-33` | `GEOMETRIC_GOAL` returns `goal()`, `GEOMETRIC_CURRENT` returns `value()` |
| S296 | `HyprCtl.cpp:395,427-428,447-448` | both output branches print `w->size(GEOMETRIC_GOAL)` |
| S297 | `host-gkeep.conf:2-4` | three rules on one class regex: `float on`, `center on`, `size 420 500` |
| S298 | `host-clients-r43.json:3,18,33,48` (62 lines) | four client objects, all tiled, 1720x1414, no gkeep |
| S299 | `gkeep-ui-excerpt.py:6,33` | `application_id="org.omarchy.gkeep"`, `set_default_size(420, 500)` |

## 2. Verification

**2a. Each upstream URL serves the pinned bytes** — `url-fetch-check.txt`: seven `curl` fetches,
HTTP 200, sha256 equal to `receipts/fetch-sha256.txt` for all seven (MATCH 7/7).

**2b. Each own-work receipt is what its row says** — `own-work-check.txt`:
- `host-gkeep.conf` is byte-identical to the live `~/.config/hypr/gkeep.conf` (`cmp` clean, 264 B,
  `wc -l -c` reports `5 264` on both sides, sha256 `3726e488…` both sides). Correction, 2026-10-26:
  the first draft of S297's anchor said "4 lines" (content lines only); `wc -l` counts 5 because the
  file ends with an empty line 5 (`od -c` tail `$ \n \n`), reported by `ScrSkillProvince` and
  re-measured here in `host-conf-lines.txt`. The anchor now reads `5 lines (4 content plus an empty
  line 5, wc -l -c reports 5 264)`; byte count and sha256 were already right.
- `gkeep-ui-excerpt.py` is exactly the two header lines plus `sed -n '446,$p'` of
  `~/Projects/gkeep/gkeep/ui.py` (488 lines, full-file sha256 `07a3c4a5…` matching the header);
  the diff against a freshly cut excerpt shows only those two header lines, no body difference —
  the round-42 extra blank line is gone and the header's `446-488 (end of file)` is true.
- `host-clients-r43.json` matches a live read-only `hyprctl clients -j` on class, size, floating
  and mapped for all four clients; no `org.omarchy.gkeep` client is open. The file is 62 lines and
  the four objects start at the `address` keys on lines 3, 18, 33 and 48, so the first draft's
  range `:3-60` was replaced by those four locators (it stopped one line short of the fourth
  object's closing brace); the 711 B size and sha256 were already right. `hyprctl version`
  confirms Hyprland 0.56.2 at commit `efb5099…`, the tag the seven upstream rows name.

**2c. No location is already a row** — `clause-e-check.txt`: for all ten, the source cell's last
whitespace token is unique across the registry and its last path component contains/ is contained
by the receipt file name (`clause-e-parity: PASS`). This is the same rule the C2 counter applies in
clause e, recomputed here over the appended mirror.

**2d. Census validate** — `census-validate.txt`, mirror = lane-shaped scratch tree (corpus copy +
symlinks to the lane's other top-level paths, so the pre-existing rows' used-by paths resolve):
`file ok … exit=0`, with only the eight warnings the unchanged registry already produces
(seven W04 cross-scope URL repeats, one W01 tier-C row). Run on the untouched file first for the
baseline: the same eight warnings, exit 0 — so the ten rows add no finding.

Mirror caveat, stated because it is scaffolding: `corpus/knowledge/hyprland-gkeep-geometry-r43.md`
does not exist in the lane yet (the C2 author owns it), so E11 would fire for the ten rows' used-by
against a real file. The mirror therefore holds a one-line placeholder at that path. The mirror was
deleted with the scratch tree; `rows-block.txt` is the reproducible delta.

**2e. The validator can fail** — `census-mutants.txt`, two probes in the scratch mirror:
- A: S290 copied verbatim as S300 inside the table → `E04 S300 duplicate url … within scope …`,
  exit 1. So "no duplicate location" is a real check here, not an unfalsifiable claim.
- B: S291 copied as S300 with the tag rewritten to the commit → `file ok`, exit 0, which is the
  measured basis for §1a's claim that the tag and the commit are distinct location tokens.
- the restored mirror passes again (`file ok`, exit 0).

## 3. Limits

- The mirror validated the census; the C2 counter was **not** run (it scores a committed entry,
  which does not exist yet). Clause parity for e is recomputed by my own script in
  `clause-e-check.txt`; clauses b-d, f-i are the C2 author's and the L1's to satisfy.
- Rows are drafted, not appended: `corpus/SOURCES.md` is untouched (it is outside this seat's
  write scope). The L1 appends `rows-block.txt` at the end of the Registry table (after S289,
  before the blank line preceding `## Paths`).
- The row-level overlap with S155/S158 (§1a) is a judgement call the L1 can reverse cheaply; the
  reversal cost is two row deletions plus one used-by edit.
- S298's teaches says a closed gkeep means the join reports nothing. That is a shape claim about a
  dump with no gkeep entry, not a measured run of the C1 tool (which does not exist yet).
