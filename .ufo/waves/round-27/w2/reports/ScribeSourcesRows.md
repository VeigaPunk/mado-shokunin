# ScribeSourcesRows — round 27 source-row findings

## Behavior and findings

Prepared `.ufo/waves/round-27/drafts/sources-rows.md` from the four completed w1 opener reports. Assigned S178–S182 after the observed S177 final registry row, with one pinned raw URL per new row and the registry's 11-cell header. Each new row has `corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py` as `used-by`. The draft also contains one located quote per new row for the lesson's `## Gate` table and the exact old→new `used-by` cell values for S158 and S162.

No exact candidate URL duplicates an existing SOURCES entry: the `functions.grep` search over `corpus/SOURCES.md`, pattern `Workspace-Rules.md|WorkspaceRuleManager.cpp|ComplexDataTypes.hpp|ParserUtils.cpp|MiscFunctions.cpp`, returned `No matches found`. No candidate was rejected as a duplicate. S158 and S162 are existing URLs, so they receive only the requested `used-by` extensions; their anchor cells remain unchanged under the registry rule.

New row assignment and source provenance:

- S178 — Hyprland wiki `content/Configuring/Workspace-Rules.md`; opener report `.ufo/waves/round-27/w1/reports/SrcWikiWsRules.md`; fetch artifact `.ufo/waves/round-27/fetch/SrcWikiWsRules.bin`, SHA-256 `486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62`, 4,786 bytes.
- S179 — Hyprland `src/config/shared/workspace/WorkspaceRuleManager.cpp`; opener report `.ufo/waves/round-27/w1/reports/SrcWsRuleCode.md`; fetch artifact `.ufo/waves/round-27/fetch/SrcWsRuleCode.bin`, SHA-256 `06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10`, 2,672 bytes.
- S180 — Hyprland `src/config/shared/complex/ComplexDataTypes.hpp`; opener report `.ufo/waves/round-27/w1/reports/SrcWsRuleLegacy.md`; fetch artifact `.ufo/waves/round-27/fetch/SrcWsRuleLegacy-ComplexDataTypes.hpp.bin`, SHA-256 `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`, 6,116 bytes.
- S181 — Hyprland `src/config/shared/parserUtils/ParserUtils.cpp`; opener report `.ufo/waves/round-27/w1/reports/SrcBoolAndExec.md`; fetch artifact `.ufo/waves/round-27/fetch/SrcBoolAndExec.bin`, SHA-256 `86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0`, 5,902 bytes.
- S182 — Hyprland `src/helpers/MiscFunctions.cpp`; opener report `.ufo/waves/round-27/w1/reports/SrcBoolAndExec.md`; fetch artifact `.ufo/waves/round-27/fetch/SrcBoolAndExec-MiscFunctions.bin`, SHA-256 `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`, 29,785 bytes.

The source-openers' reports record their raw-URL fetch commands and quote-validation outcomes. This scribe read those reports and registry rows but did not rerun their fetches or quote checks. The draft's five quotes are the located excerpts reported by the openers; they are source statements, not runtime observations.

## Commands and gates

Actions in this scribe pass: read `.ufo/waves/round-27/registration.md`, the four w1 reports, `corpus/SOURCES.md` (including S158, S162, S177), and use `functions.grep` on `corpus/SOURCES.md` with the pattern above. The duplicate search returned no matches. No shell command, source fetch, C1/C2 counter, oracle, build, test, live compositor query, or coredump check was run by this scribe. Gate and runtime behavior therefore remain unmeasured here.

The opener reports provide the following distinct evidence, not execution evidence from this pass: `SrcWikiWsRules.md` reports all four quote checks true; `SrcWsRuleCode.md` reports all four quote checks passed and a Hyprland coredump count of 1338 before/after; `SrcWsRuleLegacy.md` reports eight quote checks passed and 1338 before/after; `SrcBoolAndExec.md` reports four quote checks passed after correcting a first checker syntax error and 1338 before/after. No C1/C2 gate was run by those source-opener seats, per their reports.

## Touched surfaces and limits

Created only `.ufo/waves/round-27/drafts/sources-rows.md` and this report. `corpus/SOURCES.md`, source artifacts, lesson, and product files were not changed. Row content, hashes, anchors, quotes, and opener outcomes are transcribed from the completed w1 reports; no independent network/source verification was performed. No tool was installed. The rows support the documented/source-code claims in the workspace-rules lesson and tool attribution; they do not establish runtime behavior.

Report: `.ufo/waves/round-27/w2/reports/ScribeSourcesRows.md`
Draft: `.ufo/waves/round-27/drafts/sources-rows.md`
