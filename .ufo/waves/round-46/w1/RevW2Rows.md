# RevW2Rows — round-45 w2 re-open of rows S302-S315 (round 46 w1, 2026-10-26)

Scope executed: all 14 rows S302-S315 re-fetched today, sha256'd, compared against the row's
hash cell (corpus/SOURCES.md:251-264), `.ufo/waves/round-45/receipts/fetch-sha256.txt` and the
frozen receipt files under `.ufo/waves/round-45/fetch/`; each round-45 Gate quote
(corpus/lessons/round-45.md:16-29) located in its receipt at a computed line; anchor ranges and
teaches checked against receipt content.

## Method (all locators computed, none typed)

- Re-fetch: `curl -fsS` of each row URL into scratch, sha256sum, `cmp -s` against the frozen
  round-45 receipt file. Fetch time 2026-10-26T20:44Z. Fresh copies mirrored to
  `.ufo/waves/round-46/w1/RevW2Rows/receipts/` (14 files).
- Verifier: `.ufo/waves/round-46/w1/RevW2Rows/verify-rows.py` (in this seat dir) parses the rows
  and the GATE lines, whitespace-normalizes quotes, maps char offsets to line numbers, and dumps
  evidence windows to `w2-windows.txt` (1696 lines) + machine summary `w2-summary.json`.
  Teaches cross-checks were additional `grep -n` runs, all shown below with receipts.

## Per-row results

| row | SOURCES.md | bytes equal | Gate quote found at | quote in anchor range | teaches |
|-----|-----------|-------------|--------------------|-----------------------|---------|
| S302 | :251 | y (all 4 comparisons) | Hyprland-Parser.cpp:134 | y (110-143 parseMode) | y |
| S303 | :252 | y | Hyprland-legacy-ConfigManager.cpp:1299 | y (1293-1387 handleMonitor) | y |
| S304 | :253 | y | Hyprland-MonitorRuleManager.cpp:38 | y (37-42 add) | y |
| S305 | :254 | y | Hyprland-MonitorRule.hpp:46 | y (41-69 CMonitorRule) | y |
| S306 | :255 | y | Hyprland-Monitor.cpp:1001 | y (719-1082 applyMonitorRule) | y |
| S307 | :256 | y | Hyprland-HyprCtl.cpp:241-242 | y (224-288 getMonitorData) | y |
| S308 | :257 | y | Hyprland-MonitorPositionController.cpp:27-29 | y (16-38 explicit) | y |
| S309 | :258 | y | hyprutils-String.cpp:59 | y (46-84 isNumber/isNumber2) | y |
| S310 | :259 | y | wiki-Monitors.md:11 | y (5-30 General) | y (nuance below) |
| S311 | :260 | y | Hyprland-MonitorState.cpp:112+114 (splice) | y (109-125 add) | y (nuance below) |
| S312 | :261 | y | Hyprland-macros.hpp:40 | y (40 DELTALESSTHAN) | y |
| S313 | :262 | y | hyprutils-Vector2D.hpp:39-40 | y (36-41 scalar operators) | y |
| S314 | :263 | y | hyprutils-VarList2.hpp:18 | y (9-18 ctor) | y |
| S315 | :264 | y | aquamarine-DRM.cpp:2101 | y (2096-2104 description) | y |

"bytes equal (all 4)" = fresh fetch sha256 equals (a) the row's `sha256:` cell, (b) the
fetch-sha256.txt entry, (c) the GATE line sha256, and (d) byte-identical (`cmp -s`) to the frozen
round-45 receipt file. No drift: the round-45 w2 data is exactly what upstream serves today.

All anchor ranges are in bounds and contain their labels: parseMode/parsePosition/parseScale/
parseTransform (Parser.cpp:110/145/193/213), handleMonitor (ConfigManager.cpp:1293) and
handleMonitorv2 (:788), add/get (MonitorRuleManager.cpp:37/44), CMonitorRule (:41),
applyMonitorRule (Monitor.cpp:719), matchesStaticSelector (:1201), descriptions (:250-252),
getMonitorData (HyprCtl.cpp:224), monitorsRequest (:313), explicit/auto arrange blocks
(MonitorPositionController.cpp:21-37 / 61-101), isNumber/isNumber2 (String.cpp:46/50),
General/Monitor v2 (wiki-Monitors.md:6/292), allMonitors/monitors (MonitorState.cpp:49/53),
DELTALESSTHAN (macros.hpp:40), Vector2D doubles (:21-22), CVarList2 ctor (VarList2.hpp:18),
parseEDID + description (DRM.cpp:1911/2101).

## Teaches evidence (receipt:line, quoted snippets ≤ 25 words)

- **S302** — rate only after `@`: `if (value.contains("@"))` guards `m_refreshRate` assignment
  (Parser.cpp:133-134, quote at :134). auto positions/scales stay unset: empty/`auto*` offset
  becomes the sentinel `Vector2D(-INT32_MAX, -INT32_MAX)` (:146-147), auto scale `-1` (:194-195).
  `if (m_rule.m_scale < 0.25F)` … `m_rule.m_scale = 1` (:203-205).
- **S303** — exactly eight keys in the post-scale loop: mirror, bitdepth, cm, sdrsaturation,
  sdrbrightness, transform, vrr, icc (ConfigManager.cpp:1352-1374); any other key returns
  `"invalid syntax at"` (:1377-1378) **before** `Config::monitorRuleMgr()->add(...)` (:1383).
  Quote at :1299 is the ARGS[1] pre-dispatch.
- **S304** — one rule per selector: `std::erase_if(m_rules, … e.m_name == x.m_name)` then
  emplace (:38-39); newest wins: reverse-view first `matchesStaticSelector` hit (:96-99); else
  first `m_name.empty()` rule (:103-106); else hardcoded fallback (:108-116). Quote at :38.
- **S305** — defaults in class CMonitorRule: offset sentinel, `m_scale = -1`,
  `m_refreshRate = 60` (:44-46). Quote at :46.
- **S306** — closest mode within 1 px and 1 Hz: DELTALESSTHAN on x, y and refreshRate with
  delta 1 (Monitor.cpp:836-837); 1/120 step search `std::round(m_scale * 120.0)` (:1001-1012,
  quote at :1001); `m_shortDescription = trim(std::format("{} {} {}", make, model, serial))`
  (:255-256).
- **S307** — `vars[1] == "all"` switches to `allMonitors()` (HyprCtl.cpp:320, 327, 335), which
  per S311 holds disabled outputs too; `"refreshRate": {:.5f}` (:242, quote at :241-242);
  description key (:234) is fed `m->m_shortDescription` (:276) = the short make-model-serial form.
- **S308** — explicit offsets are placed first: `m->moveTo(*POS)` (:24-29, quote at :27-29);
  only afterwards the auto loop over "all non-explicitly placed monitors" (:60-101).
- **S309** — `-` only at i==0 (:59-62); one inner dot via `decimalParsed` (:66-77);
  `return isdigit(str.back())` (:83). Quote at :59.
- **S310** — `monitor = name, resolution, position, scale` (:11, quote); option keys documented
  incl. sdr_eotf (:253, :261, :319 — :253 inside the 240-260 anchor). Cross-check: sdr_eotf has 0
  hits in Parser.cpp and is NOT in the 8-key `monitor =` line loop (ConfigManager.cpp:1352-1374),
  so the line handler rejects it — but the `monitorv2` handler DOES accept it
  (ConfigManager.cpp:819-831, registered :576). The row says "line handler", which is accurate;
  precision note recorded.
- **S311** — `m_realMonitors.emplace_back(mon)` (:114) precedes the `if (!mon->m_enabled)
  return` (:122-123); the active list is filtered to enabled non-mirrors by the layoutChanged
  listener (:33-44). Gate quote is a disclosed splice: halves at :112 and :114 (blank :113
  elided), both inside anchor 109-125. Nuance: the monitorAdded listener appends unconditionally
  (:26-27), so the enabled/mirror filter is applied on layout changes, not at insertion.
- **S312** — `#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))` (:40): strict
  less-than on the absolute difference. Quote at :40.
- **S313** — `double x = 0; double y = 0;` (:21-22) and `operator/(const double& a)` (:39-40,
  quote at :39-40).
- **S314** — ctor defaults `delim = ',', … removeEmpty = false` (VarList2.hpp:18, quote at :18):
  comma default, empty fields kept.
- **S315** — EDID make/model/serial parsed (:1919-1938, PNP mapping :1921-1925);
  `output->description = std::format("{} {} {} ({})", make, model, serial, szName)` (:2101,
  quote); `szName` is the connector name `format("{}-{}", name, connector_type_id)` (:1776).

## Findings

1. **No drift, no falsification.** All 14 rows: bytes identical to today's upstream, Gate quotes
   at their locators, anchors in bounds, teaches supported. The round-45 w2 material
   (S302-S315) survives re-open; closure D1's missing falsification run would have passed.
2. **S310 precision (no row change needed).** "an sdr_eotf key the 0.56.2 line handler does not
   accept" is true for the `monitor =` line handler but the `monitorv2` handler accepts it
   (receipts above). The row's anchor 290-310 (Monitor v2) already gestures at this; the sdr_eotf
   v2 table row sits at wiki line 319, just outside that anchor.
3. **S311 teaches simplification (no row change needed).** "the active list holds enabled outputs
   that mirror nothing" is the layoutChanged-maintained invariant (:33-44); the monitorAdded
   listener inserts without the filter (:26-27).
4. **Cosmetic, round-45 receipt file:** `.ufo/waves/round-45/receipts/fetch-sha256.txt` lines
   10, 12, 13 carry a `fetch/` name prefix the other 11 lines lack. Names still resolve; hashes
   all correct.

## Residual risk / gaps

- Content equality is against the pinned upstream commits/tags; if a ref moved, curl followed the
  same URL text — all 14 still hash-identical to round-45, so no ref moved for these pins.
- Teaches judgments are source-level (receipts); no live-compositor check was in scope for this
  seat, and none was run (allowed reads list untouched).
- No tools installed (curl/sha256sum/cmp/python3 system binaries only).

Scratch `/fast/scratch/hyaku/mado-r46/RevW2Rows/` deleted after mirroring receipts into this
seat dir.
