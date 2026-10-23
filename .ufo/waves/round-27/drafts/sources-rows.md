# Round 27 workspace-rule SOURCES rows

Prepared from the four w1 source-opener reports. These rows use the `corpus/SOURCES.md` 11-cell header; each new source cell contains one URL. IDs continue after S177. The `used-by` value for every new row is `corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S178 | Hyprland Wiki Workspace Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md | docs | A | Hyprlang-era workspace selector syntax and existing-workspace limit, assignment form, gap shorthand keys, and on-created-empty rule | content/Configuring/Workspace-Rules.md:13-19,38-55,84-101,103-113 @ ecc06f3b6605e453c0ad533d979fccbefff788ef, sha256:486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62, 4786 B | Documents selector-property spacing and the existing-workspace boundary, assignment syntax, gapsin/gapsout keys, and the on-created-empty trigger | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |
| S179 | Hyprland v0.56.2 workspace rule manager — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp | code | A | Exact-selector replace-or-add and aggregation of static-selector matches in the workspace rule manager | src/config/shared/workspace/WorkspaceRuleManager.cpp:25-32,34-52 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10, 2672 B | Reuses an enabled rule only for an exact selector-string match; workspace lookup separately merges every enabled matching static selector | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |
| S180 | Hyprland v0.56.2 CCssGapData parser — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp | code | A | Four-sided gap parsing used by legacy workspace-rule gapsin and gapsout | src/config/shared/complex/ComplexDataTypes.hpp:80-120 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B | Maps one to four integer values to CSS-like top/right/bottom/left gaps; the default branch warns and constructs from the first four tokens | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |
| S181 | Hyprland v0.56.2 shared integer parser — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp | code | A | Legacy workspace-rule boolean-like values routed through ParserUtils::parseInt | src/config/shared/parserUtils/ParserUtils.cpp:134-149 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0, 5902 B | Maps lowercase true/on/yes and false/off/no prefixes, handles 0x values, and falls back to signed integer parsing | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |
| S182 | Hyprland v0.56.2 workspace command normalizer — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp | code | A | The command string prepared for legacy on-created-empty workspace rules | src/helpers/MiscFunctions.cpp:478-513 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9, 29785 B | Trims the command, supplies or replaces its workspace inline rule, and emits the bracketed rule block followed by the command | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |

## Located quotes for the lesson's `## Gate` table

Each excerpt is copied from its opener report's whitespace-collapsed quote check; excerpts are at most 25 words. These are pinned-source statements, not runtime measurements.

| id | located quote (source path:line) |
|---|---|
| S178 | `workspace selectors can only match _existing_ workspaces.` — `content/Configuring/Workspace-Rules.md:47` |
| S179 | `mergedRule.mergeLeft(*rule);` — `src/config/shared/workspace/WorkspaceRuleManager.cpp:45` |
| S180 | `CCssGapData(int64_t vertical, int64_t horizontal) : m_top(vertical), m_right(horizontal), m_bottom(vertical), m_left(horizontal) {};` — `src/config/shared/complex/ComplexDataTypes.hpp:84` |
| S181 | `if (val.starts_with("true") || val.starts_with("on") || val.starts_with("yes"))` — `src/config/shared/parserUtils/ParserUtils.cpp:138` |
| S182 | `rules = "[" + workspaceRule + "]";` — `src/helpers/MiscFunctions.cpp:506` |

## Existing-row used-by extensions

Only the `used-by` cell changes; existing anchor cells remain unchanged under the registry's in-place edit rule.

- S158: `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md` → `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md`
- S162: `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md` → `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md`

## URL collision review

The five candidate URLs above were searched against `corpus/SOURCES.md`; no matches were found. No candidate duplicates an existing registry URL, and no candidate was rejected as a duplicate. Existing S158 and S162 URLs are handled only through the `used-by` extensions above.
