# RevRows — review of draft rows S302–S310 and the Gate (round 45 w1)

Seat RevRows-2, 2026-10-26. Reviewed object: the `ROWS` and `QUOTES` tables in
`.ufo/waves/round-45/l1-draft/build-pos.py` (applied to a scratch clone of the freeze
22a8dedd; the applied registry rows are receipt `receipts/SOURCES-pos.md`, the applied
Gate `receipts/lesson-pos.md`). Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md`
§ SOURCES.md (contract v1). Held rows compared: S158 (`corpus/SOURCES.md:170`),
S162 (`corpus/SOURCES.md:174`).

Method and receipts (all under `.ufo/waves/round-45/w1/RevRows/receipts/`):

- Every locator cited below was computed with `grep -n` on the pinned bytes —
  `locators.txt` (147 lines). No locator was typed from memory.
- Every row URL was re-fetched on 2026-10-26 and sha256-compared — `refetch-sha256.txt`:
  all nine digests equal the frozen pins in `receipts/fetch-sha256.txt`. The row URLs are
  byte-identical to the counter's `PINS_URL` table (c2-r45-monitor-entry.py:97-107).
- Every Gate quote was whitespace-normalized and searched across all nine receipts —
  `quotes-check.txt`: each occurs exactly once in its own receipt, in no other cited
  receipt, and is 3–25 words.
- Positive control built and scored: census `validate` exit 0 (`file ok`), counter
  `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET` exit 0 at rev e6dc808bf265bcefab05d982eff5da15c5d3003e
  (`census-pos.txt`, `c2-counter-pos.txt`).

## Row verdicts

| row | verdict | fix |
|---|---|---|
| S302 | PASS | none (one wording nit, optional) |
| S303 | PASS | none (one range nit, optional) |
| S304 | PASS | none |
| S305 | PASS | none |
| S306 | PASS | none |
| S307 | PASS | optional strengthening of one teaches clause (below) |
| S308 | PASS | none |
| S309 | PASS | none |
| S310 | PASS | none |

### S302 — Parser.cpp — PASS

- kind `code`, tier `A` (source code), scope names the parsed fields + host version — contract-conformant.
- Anchors exact: `parseMode` at Hyprland-Parser.cpp:110, `parsePosition` at :145,
  `parseScale` at :193, `parseTransform` at :213 (next function `parseBitdepth` :229) —
  the three ranges 110-143 / 145-191 / 193-227 each contain their named function.
- Teaches vs bytes: rate read only under `value.contains("@")` — quote at :134
  (`m_rule.m_refreshRate = stof(...)`); auto position leaves the sentinel
  (`m_rule.m_offset = Vector2D(-INT32_MAX, -INT32_MAX)` at :147); auto scale sets
  `m_rule.m_scale = -1` at :195; `m_rule.m_scale < 0.25F` → `m_rule.m_scale = 1` at
  :203-205. All three teaches clauses grounded.
- Nit (optional): the teaches says "positions and scales starting auto stay unset" — an
  *empty* field also stays unset/auto (Parser.cpp:146, :194); the entry §1 states both.
  Wording could read "empty or `auto`-prefixed".

### S303 — legacy ConfigManager.cpp — PASS

- Anchors exact: `handleMonitor` at :1293, body ends :1387 (next definition
  `handleBezier` at :1389); `handleMonitorv2` (per-output overload) at :788, ends :880
  (the 13-line forwarding overload starts :881). Both ranges contain their function.
- Teaches vs bytes: exactly eight keys in the key loop — `ARGS[argno] == "` at
  :1352 (mirror), :1355 (bitdepth), :1358 (cm), :1361 (sdrsaturation), :1364
  (sdrbrightness), :1367 (transform), :1370 (vrr), :1373 (icc); any other key returns
  `"invalid syntax at ..."` at :1378, *before* `monitorRuleMgr()->add(...)` at :1384 —
  "rejects the whole line before the rule is added" grounded.
- Cross-scope with S162: justified as a new row (see §Cross-scope below).
- Nit (optional): the anchor range 788-880 excludes the trivial forwarding overload
  `handleMonitorv2()` at :881-893; extending to 788-893 would cover both overloads.

### S304 — MonitorRuleManager.cpp — PASS

- Anchors exact: `add` at :37 (body to :42; `get` at :44), `get` at :44 (body to :117;
  `all()` at :119).
- Teaches vs bytes: `std::erase_if(m_rules, ... e.m_name == x.m_name ...)` at :38 then
  append — one rule per selector string; reverse walk at :96 returns the first match —
  newest wins; forward loop for `r.m_name.empty()` at :104; built-in default fallback at
  :108-116 ("No rules configured. Using the default hardcoded one.", resolution
  `Vector2D{}`, offset sentinel, scale -1). All grounded.

### S305 — MonitorRule.hpp — PASS

- Anchor exact: the field block is exactly :41-69 — `m_autoDir` at :41 through
  `m_vrr` at :69 (class keyword at :34; the anchor names the *fields*, which sit wholly
  inside the range).
- Teaches vs bytes: `m_refreshRate = 60` at :46 (Gate quote), `m_scale = -1` at :45,
  offset sentinel `Vector2D(-INT32_MAX, -INT32_MAX)` at :44. Grounded.

### S306 — Monitor.cpp — PASS

- Anchors exact: `applyMonitorRule` at :719, body ends :1082 (next definition
  `scheduleModeRetry` at :1084); `matchesStaticSelector` exactly :1201-1211 (body closes
  at :1211, next definition `position()` at :1213); description block :250-256
  (`m_shortDescription` built from make/model/serial at :255-256).
- Teaches vs bytes: closeness sort then the met-test —
  `!DELTALESSTHAN(bestMode->pixelSize.x, ..., 1) || ... || !DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1)`
  at :836-837 (1 px and 1 Hz); scale correction `float searchScale = std::round(m_scale * 120.0);`
  at :1001 (Gate quote) with the search loop `for (size_t i = 1; i < 90; ++i)` at :1010 —
  the 1/120 step and 89 steps. Grounded.

### S307 — HyprCtl.cpp — PASS (one optional strengthening)

- Anchors: `getMonitorData` defined at :223; the JSON template sits inside 224-288
  (`"description": "{}"` :234, `"physicalHeight": {}` :241, `"refreshRate": {:.5f},`
  :242, short-description argument at :277); `monitorsRequest` at :313, body to :345
  (next definition at :347). Ranges inside the line count; the named content is covered.
- Teaches vs bytes: five decimals at :242 ✓; description is the short
  make-model-serial form (HyprCtl passes `m_shortDescription` at :277; Monitor.cpp:255-256
  builds it) ✓; the `all` branch at :315-321 with the `allMonitors()`/`monitors()`
  ternaries at :327/:335 ✓.
- Optional strengthening: the teaches clause "monitors all lists disabled outputs too" —
  the HyprCtl pin grounds the *branch* (all vs normal), but the disabled-inclusion
  *semantics* of `allMonitors()` vs `monitors()` is not in any pin; it is corroborated by
  the wiki pin inside S310's anchored range — wiki-Monitors.md:23-26 "To list all
  available monitors (active and inactive): hyprctl monitors all". The entry §4 cites
  only Hyprland-HyprCtl.cpp:313-321 for this sentence; adding wiki-Monitors.md:23-26
  would make it fully sourced. Not required by the counter (clause j passes).
- Nit (optional): the anchor could start at :223 to include the function signature.

### S308 — MonitorPositionController.cpp — PASS

- Anchors exact: `arrange` at :16; explicit block :21-38 (`explicitPosition()` check
  :24, `m->moveTo(*POS)` :27 — Gate quote starts :27); auto-direction switch :65-97
  inside 61-101 (`moveTo(newPosition)` :98).
- Teaches vs bytes: the explicit loop runs to completion before the auto loop over the
  remaining monitors — "placed exactly as written before any auto placement" grounded.

### S309 — hyprutils String.cpp — PASS

- Anchor exact: `isNumber` at :46, `isNumber2` at :50, body ends :84
  (`replaceInString` at :86) — range 46-84 contains both.
- Teaches vs bytes: minus allowed only at index 0 (`if (i == 0 && str.at(i) == '-') {`
  :59 — Gate quote); one `.` allowed, not first, not twice (:66-74); last character must
  be a digit (`return isdigit(str.back()) != 0;` :83). Grounded.

### S310 — wiki Monitors.md — PASS

- Anchors: `## General` at :6 with the line format at :11 (Gate quote) — range 5-30
  covers the format, the example and the `hyprctl monitors all` note (:23-26); colour
  keys range 240-260 contains the sdr_eotf sentence at :253; Monitor v2 range 290-310
  contains the `## Monitor v2` heading at :292.
- Revision: the anchor's "(2026-04-20)" verified against the GitHub commit API —
  ecc06f3b authored 2026-04-20T16:33:26Z (checked 2026-10-26).
- Teaches vs bytes: format at :11; option keys in :173-270; sdr_eotf documented at :253;
  "the 0.56.2 line handler does not accept" — the handler key loop
  (Hyprland-legacy-ConfigManager.cpp:1352-1373) has no sdr_eotf, and only the monitorv2
  path reads it (:819). Grounded.

## Cross-scope repeats of S158/S162 — new rows justified, keep both

- **S303 vs S162** (same URL, src/config/legacy/ConfigManager.cpp @ efb5099): S162's
  scope is "Hyprlang-era legacy windowrule keyword handlers, named special-category
  reconstruction, and reload traversal" with anchors :419-451, :590-623, :893-968,
  :2016-2093 — none of which covers the monitor handler (:788-880, :1293-1387). S303's
  scope (monitor line grammar) is disjoint. Citing S162 instead would leave the monitor
  handler unanchored. **New row justified.**
- **S307 vs S158** (same URL, src/debug/HyprCtl.cpp @ efb5099): S158's scope is
  "`clients` JSON tags, `getprop` property response, `layers` output, registered
  rule-list commands" with anchors :346-484, :613-630, :647-723, :1463-1645, :2003-2044 —
  none covers getMonitorData (:223-292) or monitorsRequest (:313-345). **New row
  justified.**
- Empirically: the census emits exactly W04 (not E04) for S303 and S307 — same URL
  across scopes — and the counter's clause e admits them (`clause=e ... 1` in
  `c2-counter-pos.txt`), matching the registration's declaration.

## Gate (QUOTES) — grounded

All nine Gate quotes verified (`quotes-check.txt`): exactly one normalized occurrence in
the own receipt, zero in any other cited receipt, 3–25 words each (S303's is exactly 3
tokens). The counter's computed locator lines (134, 1345, 38, 46, 1001, 241, 27, 59, 11 —
`clause=g` in `c2-counter-pos.txt`) match the entry's cited locators.

Note on my own receipt: `quotes-check.txt` start lines for S303/S306/S308/S309 read one
line early (1344/1000/26/58) where a blank line precedes the quote — an artifact of my
checker's boundary rule; the counter's values (1345/1001/27/59) are the correct content
lines and match the entry. Grounding verdicts are unaffected.

Gate line shape (receipt + sha256 + quote, no URL/date) matches the round-44 practice
verbatim (`corpus/lessons/round-44.md:31-34`); the URL and access date live in the row's
`source`/`opened` cells. No fix.

## Positive control, census, counter

- Clone of the freeze at `/fast/scratch/hyaku/mado-r45/RevRows/tmp.xOrTsIOXzo`
  (toplevel asserted = clone dir; detached at 22a8dedd; deleted after receipts were
  copied). `build-pos.py` applied: 4 files changed, 113 insertions; commit
  e6dc808bf265bcefab05d982eff5da15c5d3003e.
- `scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md`: exit 0, final
  line `file ok`. New warnings are exactly the two declared W04s (S303, S307). Pre-existing
  warnings (W04 S030/S042/S045/S097/S119/S120/S121, W01 S277) are untouched base state —
  append-only discipline, not round-45 rows.
- `quality/counters/c2-r45-monitor-entry.py --repo <clone> --rev HEAD --base 0c89478a...`:
  clauses a–j all pass, `admitted=1/1 verdict=TARGET_MET`, exit 0.

## Contract conformance sweep (all rows)

kind enum (code×8, docs×1) ✓; tier A for source code and official project docs
(community-never-A n/a) ✓; scope cells name the claim each tier applies to ✓; anchors
carry exact line ranges + revision (commit hash / tag / commit date), never a bare
homepage ✓; teaches one grounded learner benefit each ✓; status `mined` with used-by =
the entry, which exists in the control (census E11 clean) ✓; opened 2026-10-26 = the L1's
fetch date per the registration ✓; recheck `90d` ✓; ids S302–S310 sequential after S301,
no duplicates (census E02/E03 clean) ✓; no `|` inside cells (builder asserts 12 pipes per
row) ✓; rows inserted directly after the last registry row, before `## Paths` (E12 safe)
✓; the entry's census line values each verified against the pins — default_refresh=60
(MonitorRule.hpp:46), refresh_tolerance=1 (Monitor.cpp:837), scale_step=1/120
(Monitor.cpp:1001), scale_search=89 (Monitor.cpp:1010, i<90),
json_refresh_decimals=5 (HyprCtl.cpp:242), line_keys=8 (legacy ConfigManager
:1352-1373) ✓.

## Findings summary

No blocking defect in S302–S310 or the Gate. Optional items, in priority order:

1. S307 teaches "monitors all lists disabled outputs too" — cite wiki-Monitors.md:23-26
   in the entry §4 alongside Hyprland-HyprCtl.cpp:313-321 (the semantics is otherwise
   name-inferred from `allMonitors()`).
2. S303 anchor could read 788-893 to include the forwarding `handleMonitorv2()` overload.
3. S302 teaches could read "empty or `auto`-prefixed" for position/scale.
4. S307 anchor could start at :223 to include the signature.

None of these blocks admission; the counter and census pass as built.
