# ReopenLegacy — re-open of w1 `SrcWsRuleLegacy.md`

Re-opened every source URL and quote in `.ufo/waves/round-27/w1/reports/SrcWsRuleLegacy.md` (three URLs, nine quoted excerpts) and checked both SOURCES.md proposals it makes. Fresh curl fetches, sha256/byte/line comparison with the report's rows, whitespace-collapsed substring relocation of every quote in python, anchor-range checks against the fetched bytes, and a state check of the proposals against the live inventory. All checks ran 2026-10-23.

## What I did (exact commands)

Fetches (one per URL, all completed without stdout or error):

```sh
timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp -o /fast/scratch/hyaku/mado-r27/reopen/ReopenLegacy-ConfigManager.cpp.bin
timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp -o /fast/scratch/hyaku/mado-r27/reopen/ReopenLegacy-ComplexDataTypes.hpp.bin
timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/types/CssGapValue.hpp -o /fast/scratch/hyaku/mado-r27/reopen/ReopenLegacy-CssGapValue.hpp.bin
```

- `sha256sum` + `wc -c -l` on each fetch.
- Python (stdlib): whitespace-collapse each fetched file and each quoted excerpt; substring test over the full collapsed file; sliding-window per-line relocation; whole-line equality for the seven single-line quotes; dumps of `ConfigManager.cpp:333-347,604-614,1672-1684,1712-1724,1776-1792`, `ComplexDataTypes.hpp:76-122`, `CssGapValue.hpp:20-35` to verify the anchor and behavior claims.
- Coredump watch: `timeout 30 coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland` → `1338` before, `1338` after, delta `0`. No Hyprland process was started.
- Cross-check: `sha256sum` of the w1 lane artifacts `.ufo/waves/round-27/fetch/SrcWsRuleLegacy.bin`, `SrcWsRuleLegacy-ComplexDataTypes.hpp.bin`, `SrcWsRuleLegacy-CssGapValue.hpp.bin`.
- SOURCES.md: read header, full S162 row (`corpus/SOURCES.md:174`), rows S166–S182 and the addendum quote table (`:178-201`), checked for rows beyond S182, and globbed `corpus/knowledge/` for the proposed used-by target.

## Row verdicts

```
REOPEN S162 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp sha=match quotes=3/3 located — agree
REOPEN candidate-row https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp sha=match quotes=4/4 located — agree
REOPEN CssGapValue.hpp https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/types/CssGapValue.hpp sha=match quotes=2/2 located — agree
```

Digests, byte counts, and line counts — fresh fetch = w1 report row = w1 lane fetch artifact (three-way identical):

| URL | sha256 (all three sources) | bytes | lines |
|---|---|---|---|
| ConfigManager.cpp | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90,963 | 2,184 |
| ComplexDataTypes.hpp | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` | 6,116 | 178 |
| CssGapValue.hpp | `5780a6e1565ddc845e01924ed5155a547f31ab9a52c204c7a0428c5d043c3511` | 1,047 | 35 |

The S162 row's inventory digest and byte count (`corpus/SOURCES.md:174`: `sha256:9db68cf4…, 90963 B`) also match.

### Quote relocation (9/9 located; path:line is in the fetched bytes)

- `src/config/legacy/ConfigManager.cpp:1678` — `const auto FIRST_DELIM = value.find_first_of(',');` — whole line matches.
- `src/config/legacy/ConfigManager.cpp:1719` — `wsRule.m_gapsIn->parseGapData(varlist);` — whole line matches.
- `src/config/legacy/ConfigManager.cpp:1781` — `CVarList2 rulesList(std::string(rules), 0, ',', true);` — whole line matches.
- `src/config/shared/complex/ComplexDataTypes.hpp:84` and `:85` — the two- and three-arg constructor lines — whole lines match.
- `src/config/shared/complex/ComplexDataTypes.hpp:94-95` — the `toInt` lambda sits entirely on line 95 (line 94 is the `parseGapData` signature); contained in the stated range.
- `src/config/shared/complex/ComplexDataTypes.hpp:114-116` — the WARN log sits on line 115 and the four-token construction on line 116 (line 114 is `default: {`); contained in the stated range.
- `src/config/values/types/CssGapValue.hpp:26` and `:33` — whole lines match.

### Anchor and behavior claims verified against the fresh bytes

- `ConfigManager.cpp:335-343` is the static Hyprlang callback wrapper (`handleWorkspaceRules(const char*, const char*)`) delegating to `Config::Legacy::mgr()->handleWorkspaceRules` and calling `setError` on failure.
- `ConfigManager.cpp:609` is `m_config->registerHandler(&::handleWorkspaceRules, "workspace", {false});` — the keyword registration the report names.
- `ConfigManager.cpp:1676-1792` is `CConfigManager::handleWorkspaceRules`: split at the first comma (`:1678`), `trim` + `getWorkspaceIDNameFromString` (`:1680-1682`), rules = remainder after the first comma (`:1684`); the `gapsin:`/`gapsout:` branches build a space-separated `CVarList2` (`:1716`, `:1722`, separator `' '`), construct `CCssGapData` and call `parseGapData` inside `try` (`:1717-1719`), and `catch (...)` returns the workspace-rule error (`:1720`); on success the resolved name and ID are recorded (`:1788-1789`) and `Config::workspaceRuleMgr()->replaceOrAdd(std::move(wsRule))` is called (`:1791`).
- `ComplexDataTypes.hpp:80-120`: `CCssGapData` constructors map 1 token → all four sides (`:83`), 2 → vertical/horizontal (`:84`), 3 → top/horizontal/bottom (`:85`), 4 → top/right/bottom/left (`:86`); every token converts through `std::stoi` via the `toInt` lambda (`:95`); the default branch warns `"Too many arguments provided for gaps."` and constructs from the first four tokens (`:115-116`).
- `CssGapValue.hpp` exposes `const Config::CCssGapData& value() const;` (`:26`) and stores `Config::CCssGapData m_default;` (`:33`); it defines no `parseGapData`, so the report's "supporting declaration, not a parser candidate" holds.

## Proposal status

- **S162 used-by extension** — applied in the lane: `corpus/SOURCES.md:174` used-by now reads `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md` — exactly the three-doc old value the report quotes plus the proposed append. The row's anchor cell is untouched, as proposed.
- **Candidate new row** — integrated as **S180** (`corpus/SOURCES.md:192`) with the same URL, kind `code`, tier `A`, anchor `src/config/shared/complex/ComplexDataTypes.hpp:80-120 @ efb5099…, sha256:95733223…, 6116 B`, opened `2026-10-23`, status `mined`, recheck `on-release`. Two trivial wording deltas from the proposal ("called by"→"used by"; "integer fields"→"integer values", "…left values"→"…left gaps") and the integrated used-by adds `tools/mado-wsrules.py` beyond the proposal. Integrator latitude; substance identical. The report's guess "assign an ID at integration" was correct practice: S178/S179 landed from sibling reports first.
- The report's context claims hold: the SOURCES.md header does say only `status`, `recheck`, `used-by` change in place; the inventory did end at S177 when the report inspected it (S177 is still the last row before the S178–S182 block); the `CssGapValue.hpp` path still has no inventory row.
- The inventory addendum quote table's S180 row quotes `ComplexDataTypes.hpp:84` — the same line this re-open located.

## Findings

**MINOR — dangling used-by target (integration in flight, not a w1-report defect).** `corpus/knowledge/workspace-rules-r27.md` does not exist in the lane at re-open time, while the used-by cells of S158, S162 and S178–S182 already point at it. The SOURCES.md header requires used-by changes logged old→new in that round's lesson, and `corpus/lessons/` has no round-27 lesson yet. Both are expected to resolve before closure; the knowledge document must land (and the lesson log its used-by changes) or the provenance chain dangles.

**INFO — inventory moved under this re-open.** `corpus/SOURCES.md` grew from 417 to 427 lines between two reads during this run: rows S178–S182 and the addendum quote table landed concurrently (a scribe/integration seat is live). All w1 report statements were checked true for their stated inspection time, and the landed S180/S162 states match the proposals; line numbers in this report are valid for the 427-line snapshot.

## Residual risk and verification gaps

- Only the three rows named in `SrcWsRuleLegacy.md` were re-opened; S178, S179, S181, S182 are sibling seats' rows and out of scope (their URLs were not fetched).
- I did not reconstruct the pre-edit used-by from repository history; the observed post-state (exactly the three quoted docs plus the append) corroborates the report's claimed old value.
- No tool was installed or upgraded (none needed); no C1/C2 counter, suite, or compositor was run; every process I started was wrapped in `timeout` and has exited.
