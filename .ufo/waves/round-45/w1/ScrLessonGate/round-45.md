# round 45 — the monitor-rule chain: Gate, registry changes, search log

This round's lesson covers C2 (`corpus/knowledge/hyprland-monitor-rule-r45.md`). `## Mistakes` is
ScrMistakes' section and is deliberately absent here. Every line below that begins `GATE ` is in the column-0 form
PRED-C2-r45 clause d parses (the form `l1-draft/build-pos.py` emits); each quote was re-verified today against
`.ufo/waves/round-45/fetch/` with the frozen counter's own matching (`.ufo/waves/round-45/w1/ScrLessonGate/quote-verify.txt`,
`ALL_QUOTES_OK=1`: pin sha256 match, one word-bounded occurrence, comment-stripped match, distinct quote) and located
with `grep -n` (`.ufo/waves/round-45/w1/ScrLessonGate/gate-greps.txt`). No locator in this file was typed by hand.
The nine `GATE` lines are byte-identical to the lines `l1-draft/build-pos.py` emits for the same pins
(`gate-line-match.txt`, `GATE_LINES_IDENTICAL=1`). Draft-stage provenance only: the three receipts named in this
paragraph sit in `.ufo/waves/round-45/w1/ScrLessonGate/`; the L1 may trim this paragraph when integrating.

## Gate

Fifteen candidates were screened for the C2 question — *at the host's Hyprland 0.56.2 (efb50993), what carries the
chain from a `monitor =` line to `hyprctl monitors all -j`?* — nine admitted as new rows S302-S310, six rejected.
The admission test is the one the counter can enforce: the primary file at the host's revision carries the claim,
and one <= 25-word quote from it binds to one receipt byte-for-byte (clause d), under a scope no held row owns
(clause e).

| # | candidate | verdict | reason |
|---|---|---|---|
| 1 | `src/config/shared/monitor/Parser.cpp` @ efb50993 | admitted S302 | the parseMode / parsePosition / parseScale bodies the entry cites are here; the rate-after-`@` and the sub-0.25 scale reset are entry claims |
| 2 | `src/config/legacy/ConfigManager.cpp` @ efb50993 | admitted S303 | `handleMonitor` owns the line grammar, the disable/transform/addreserved modifiers and the key loop |
| 3 | `src/config/shared/monitor/MonitorRuleManager.cpp` @ efb50993 | admitted S304 | rule storage, erase-on-add and reverse lookup are the "which rule wins" answer |
| 4 | `src/config/shared/monitor/MonitorRule.hpp` @ efb50993 | admitted S305 | the rule field defaults; the 60 Hz default is the answer to "what does `WxH` without `@R` request" |
| 5 | `src/output/Monitor.cpp` @ efb50993 | admitted S306 | mode closeness, the 1/120 scale search and `matchesStaticSelector` are all in this file |
| 6 | `src/debug/HyprCtl.cpp` @ efb50993 | admitted S307 | the `monitors` request and every JSON field the entry lists are printed here |
| 7 | `src/state/MonitorPositionController.cpp` @ efb50993 | admitted S308 | explicit-position placement; the entry's position claim is this function |
| 8 | `src/string/String.cpp` @ hyprutils v0.14.2 | admitted S309 | the parsers' number test; v0.14.2 is the version the host reports at run time |
| 9 | `content/Configuring/Monitors.md` @ wiki ecc06f3 | admitted S310 | the documented line format and the documented `sdr_eotf` key the handler does not read |
| 10 | held S158 (same HyprCtl.cpp URL) reused instead of S307 | rejected | its frozen anchor cell covers 346-484, 613-630, 647-723, 1463-1645, 2003-2044 — coverage of :242 and :313-321 is 0, and cells 1-9 of a held row are byte-frozen |
| 11 | held S162 (same legacy ConfigManager.cpp URL) reused instead of S303 | rejected | its anchor cell covers 419-451,590-623,893-968,2016-2093 — coverage of :1293-1387 is 0; its scope cell is windowrule handlers, not the monitor line |
| 12 | the same wiki page at `main` | rejected | `main` serves no such file today (HTTP 404); only the pinned commit returns the page (HTTP 200, sha256 `f2ac7025…04b9`, identical to the pin) |
| 13 | a live `hyprctl monitors all -j` dump on this host as a row | rejected | not reproducible and session material is shape-only (`SKILL.md:343`); the host observation rides the entry as §6 with its receipt, not as a source row |
| 14 | `src/output/Monitor.hpp` | rejected | declarations only; every code claim is carried by Monitor.cpp (S306) or MonitorRule.hpp (S305), and no clause-j surface needs it |
| 15 | hyprlang 0.6.8 parser sources | rejected | one hop removed: the grammar is in S303's handler (:1345), and the number test the parsers call is hyprutils (Parser.cpp:197/214/265 → hyprutils-String.cpp:46-47) |

### Admitted, with URL, access date and located quote

All nine opened 2026-10-26 (the L1's fetch; each pin's bytes were re-hashed today — `quote-verify.txt`, every
`pin_match=1`).

- **S302** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/monitor/Parser.cpp`
  — quote `m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));` at `Hyprland-Parser.cpp:134`
  (grep -n). Row anchor `Hyprland-Parser.cpp:110-143 parseMode, :145-191 parsePosition, :193-227 parseScale and parseTransform`.
  Why: the four positional fields of the line are parsed in this file; the `@`-gated rate read is what makes S305's default matter.
- **S303** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`
  — quote `parser.parseMode(std::string(ARGS[1])); parser.parsePosition(std::string(ARGS[2])); parser.parseScale(std::string(ARGS[3]));`
  at `Hyprland-legacy-ConfigManager.cpp:1345-1347` (grep -n found the first call at :1345; the counter's collapsed match
  starts at :1345). Row anchor `:1293-1387 handleMonitor, :788-880 handleMonitorv2`. Why: field order and arity are a
  handler decision; the same range holds the key loop and the invalid-syntax return.
- **S304** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/monitor/MonitorRuleManager.cpp`
  — quote `std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` at `Hyprland-MonitorRuleManager.cpp:38`
  (grep -n). Row anchor `:37-42 add, :44-117 get`. Why: erase-then-append is the whole "newest match wins" mechanism;
  without it the lookup order would be a guess.
- **S305** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/monitor/MonitorRule.hpp`
  — quote `float m_refreshRate = 60;` at `Hyprland-MonitorRule.hpp:46` (grep -nE for the aligned declaration). Row
  anchor `:41-69 class CMonitorRule fields`. Why: the 60 Hz default is written into the field here, not
  into a comment in a .cpp; the header is where a rule gets its defaults.
- **S306** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/output/Monitor.cpp`
  — quote `float searchScale = std::round(m_scale * 120.0);` at `Hyprland-Monitor.cpp:1001` (grep -nE for the aligned
  declaration). Row anchor `:719-1082 applyMonitorRule, :1201-1211 matchesStaticSelector, :250-256 descriptions`. Why:
  the 1/120 correction is computed here; the same function holds the closeness bound (`:836-837`: 1 px in each axis, 1 Hz refresh).
- **S307** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
  — quote `"physicalHeight": {}, "refreshRate": {:.5f},` at `Hyprland-HyprCtl.cpp:241-242` (`grep -n '"refreshRate": {:.5f},'`
  returns :242; the collapsed match starts at :241). Row anchor `:224-288 getMonitorData JSON, :313-345 monitorsRequest`.
  Why: five decimals and the field set are printed here, so the JSON half of the join is not inferred from docs.
- **S308** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/state/MonitorPositionController.cpp`
  — quote `m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);` at `Hyprland-MonitorPositionController.cpp:27-29`
  (grep -n found the first statement at :27). Row anchor `:16-38 explicit positions, :61-101 auto directions`. Why:
  "placed as written" is an ordering claim, and the erase from the auto list is what makes the ordering hold.
- **S309** `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/String.cpp` — quote
  `if (i == 0 && str.at(i) == '-') {` at `hyprutils-String.cpp:59` (grep -n). Row anchor `hyprutils-String.cpp:46-84 isNumber and isNumber2`.
  Why: v0.14.2 is not a convenience pin — the host reports `Hyprutils: built against 0.14.2, system has 0.14.2`
  (`candidates-evidence.txt` §C), and `isNumber` delegates to `isNumber2` (:46-47), so the row's description ("the
  number test Hyprland's scale and transform parsers call") is literal: Parser.cpp:197, :214 and :265 call `isNumber`.
- **S310** `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Monitors.md`
  — quote `monitor = name, resolution, position, scale` at `wiki-Monitors.md:11` (grep -n). Row anchor `:5-30 General, :240-260 colour keys, :290-310 Monitor v2`.
  Why: the docs are the only place the documented format can be quoted; the entry's divergence claim pairs this row
  with S303 (the key loop has no `sdr_eotf`; `sdr_eotf` is registered only for `monitorv2`, ConfigManager.cpp:576).

### Rejected, with the evidence that rejected them

- **Held-row reuse (candidates 10, 11)** — `verify_gate.py` computes the coverage with the counter's own range
  semantics: `S158 anchor covers HyprCtl.cpp:242 -> 0`, `:313-321 -> 0`, `S162 anchor covers ConfigManager.cpp:1293-1387 -> 0`
  (`candidates-evidence.txt` §D). Clause c freezes cells 1-9 of a held row, so the anchor cannot be widened; a new
  row with a new scope is the only form that can carry these lines. The shared URL is the census's W04 case, not an
  error: the scope cells differ (`S307 scope equals S158 scope -> 0`, `S303 scope equals S162 scope -> 0`).
- **Wiki at `main` (candidate 12)** — `main` returns HTTP 404 for `content/Configuring/Monitors.md`; the pinned commit
  returns 200 with 10563 bytes and sha256 `f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9`, equal to the
  pin (`candidates-evidence.txt` §A). A row pointing at a moving ref could not supply a quote that survives clause d.
- **Live host dump as a row (candidate 13)** — the dump would carry the output description and the exact running
  state; the lane's session-material rule keeps such dumps shape-only, and a re-run at scoring time is not
  guaranteed. The observation is entry §6 with `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, which is
  evidence for one host fact, not a source row.
- **`Monitor.hpp` (candidate 14)** — no claim in the entry is a declaration: mode choice, scale search, selector
  match and JSON printing all sit in the admitted .cpp files.
- **hyprlang sources (candidate 15)** — the line grammar is parsed by the handler (S303:1345), and the numeric test is
  hyprutils (S309); hyprlang would add a generic value parser the entry never cites.

GATE S302 receipt=.ufo/waves/round-45/fetch/Hyprland-Parser.cpp sha256=616468fd0576d8b201ef00cd69289234f0ffb1c3137ae2a0ac954fabe37dd589 quote="m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));"
GATE S303 receipt=.ufo/waves/round-45/fetch/Hyprland-legacy-ConfigManager.cpp sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="parser.parseMode(std::string(ARGS[1])); parser.parsePosition(std::string(ARGS[2])); parser.parseScale(std::string(ARGS[3]));"
GATE S304 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRuleManager.cpp sha256=17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016 quote="std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });"
GATE S305 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRule.hpp sha256=b01d31a16d5fb413ead28f46825381f36a70c29b86eceb58cd633dcbf031a2f5 quote="float m_refreshRate = 60;"
GATE S306 receipt=.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp sha256=9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927 quote="float searchScale = std::round(m_scale * 120.0);"
GATE S307 receipt=.ufo/waves/round-45/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote=""physicalHeight": {}, "refreshRate": {:.5f},"
GATE S308 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorPositionController.cpp sha256=3b705388fa53aef77c5e8c6f6307c94dab08b5dae9460bab427d648359b5ae49 quote="m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);"
GATE S309 receipt=.ufo/waves/round-45/fetch/hyprutils-String.cpp sha256=a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac quote="if (i == 0 && str.at(i) == '-') {"
GATE S310 receipt=.ufo/waves/round-45/fetch/wiki-Monitors.md sha256=f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9 quote="monitor = name, resolution, position, scale"

## Registry changes

`corpus/SOURCES.md` (`## Registry`, 238 rows at the freeze) gains nine rows after S301 and loses none:

| id | status | opened | recheck | used-by |
|---|---|---|---|---|
| S302-S310 (each of the nine) | absent → `mined` | — → `2026-10-26` | — → `90d` | — → `corpus/knowledge/hyprland-monitor-rule-r45.md` |

Cells 1-7 per id, as generated by `l1-draft/build-pos.py` (row columns: id, source, kind, claim class, scope,
anchor, evidence): kind `code` for S302-S309 and `docs` for S310; class `A` for all nine; the source URLs and anchor
cells are the ones quoted in the Gate blocks above; the evidence cells state the one-line claim each row binds,
as in `corpus/knowledge/hyprland-monitor-rule-r45.md` (parsing, rule choice, mode/scale, JSON fields, docs divergence).
Insertion point: after S301 (`corpus/SOURCES.md:250`), rows land at :251-:259.

No held row changes status, recheck or used-by:

- S158 (`HyprCtl.cpp`, mined since 2026-10-23, recheck `on-release`, scope "`clients` JSON tags …"): `mined` → `mined`,
  `on-release` → `on-release`, used-by unchanged — the new entry cites S307, not S158, and the anchor cell was not
  extended (it cannot be: cell 6 is frozen).
- S162 (`legacy ConfigManager.cpp`, mined since 2026-10-23, recheck `on-release`, scope "Hyprlang-era legacy windowrule
  keyword handlers …"): `mined` → `mined`, `on-release` → `on-release`, used-by unchanged.

Verified on a scratch clone of the freeze with `l1-draft/build-pos.py` applied: `git diff --stat` shows 4 files,
113 insertions, 0 deletions; `corpus/SOURCES.md` row count 238 → 247; no deleted content line.

`corpus/README.md` gains one index row (no row → one row), inserted after the round-44 row at :72, landing at :73:

| index entry | status cell | sources cell |
|---|---|---|
| `knowledge/hyprland-monitor-rule-r45.md` (MADO-R45-1, round 45) | draft | S302-S310 |

## Search log

**Q1 — which files carry the chain from the `monitor =` line to `hyprctl monitors all -j` at efb50993?**
Searched: the nine pinned raw files (Hyprland `src/config`, `src/output`, `src/state`, `src/debug` at efb50993; hyprutils
at v0.14.2; the wiki at ecc06f3), a live HTTP probe of the wiki at `main` for the rejected candidate, and the lane's
base registry (238 rows, topped at S301) for an existing row on the same surface. Identified 12, screened 12, included 9
(S302-S310), excluded 3 (wiki at `main` — HTTP 404 today; `Monitor.hpp` — declarations only; hyprlang sources — one
hop removed, the grammar is in S303 and the number test in S309). Stop rationale: every layer of the chain — line
grammar, field parsing, rule storage/lookup, mode and scale application, position placement, JSON printing, the
numeric test, the docs — has exactly one primary file at one pinned revision, and that revision is the host's
(`hyprctl version` reports commit efb50993 and Hyprutils 0.14.2). The remaining unknowns (a rule without `@` running
at the nearest-60 Hz mode; a fractional scale being corrected) need a config change, which is operator-owned, so no
further source can close them.

**Q2 — reuse the held rows S158/S162, or add new rows?** Searched: the registry's `## Registry` rows for both URLs,
their anchor and scope cells, and the frozen counter's clause c/e semantics. Identified 2, screened 2, included 0,
excluded 2. Stop rationale: the held anchors cover none of the cited lines (:242, :313-321, :1293-1387), the anchor
cell is frozen, and the scopes are windowrule/`clients` scopes; new rows S307/S303 with their own scope are the only
form clause c admits, and clause e's same-scope test is what separates this URL reuse from a duplicate-location error
(census W04).

**Q3 — can the host's live dump be a source row?** Searched: the lane's session-material rule and the entry's §6
host observation. Identified 1, screened 1, included 0, excluded 1. Stop rationale: a dump is not reproducible, would
carry the output description, and duplicates what the code pins already establish; it stays an entry observation with
its receipt.
