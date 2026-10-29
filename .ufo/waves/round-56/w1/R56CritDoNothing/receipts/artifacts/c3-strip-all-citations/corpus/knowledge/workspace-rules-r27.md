---
source:
  - [ref]
  - [ref]
  - [ref]
  - [ref]
  - [ref]
  - [ref]
  - [ref]
verified-at: 20022a652d201af52c899c4492a7f71be0136b80 (PRED-C1-r27-v4 41/41, seed 4cfdf858277ad362, evidence/c1-after-20022a65.txt)
recheck: `python3 -I .ufo/waves/round-27/c1/count-v4.py REV`
---

# Hyprland v0.56.2 workspace rules and table

## Scope

The implementation details below are pinned to Hyprland v0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`. The selector-property descriptions are from the pinned hyprlang-era wiki, and are documentation rather than a runtime measurement. [[ref], `content/Configuring/Workspace-Rules.md:13-48`]

## Measurement status (round 27)

The `[INF]` markers below record what the static source reports alone did not locate. They are superseded as capability claims by the round-27 measurement: `tools/mado-wsrules.py` at `20022a65` reproduces Hyprland v0.56.2's `hyprctl workspacerules -j` byte-for-byte, entry-by-entry, on BASE + 40 generated cases (41/41, seed `4cfdf858277ad362`, `evidence/c1-after-20022a65.txt`), which establishes the emitted schema (member order `workspaceString, enabled, monitor, default, persistent, gapsIn, gapsOut, borderSize, border, rounding, decorate, shadow, defaultName, onCreatedEmpty`; unset members omitted; gaps `[top,right,bottom,left]`; bools as JSON bools; `enabled` always `true`), merge-in-place with first-seen order, and the `on-created-empty` `[workspace X] cmd` prefix.

## Selector grammar

The documented assignment form is `workspace = WORKSPACE, RULES`; the workspace field is mandatory and `RULES` contains one or more rules. The v0.56.2 handler splits at the first comma, trims the first field, resolves it to a workspace identifier/name, and treats the remainder as the comma-separated rule list. [[ref], `content/Configuring/Workspace-Rules.md:38-48`; [ref], `src/config/legacy/ConfigManager.cpp:1676-1686,1781-1784`]

The wiki describes selector properties separated by spaces, with no spaces inside a property. Its forms are `r[A-B]` for an inclusive workspace-ID range; `s[bool]` for special status; `n[bool]`, `n[s:string]`, or `n[e:string]` for named-workspace status/name-prefix/name-suffix; `m[monitor]` for a monitor; `w[(flags)A-B]` or `w[(flags)X]` for inclusive or exact window counts; and `f[-1]`, `f[0]`, `f[1]`, or `f[2]` for fullscreen state. Window-count flags documented there are `t` (tiled), `f` (floating), `g` (groups), `v` (visible), and `p` (pinned). [[ref], `content/Configuring/Workspace-Rules.md:18-36`]

The wiki says selectors can match only already-created workspaces. Separately, the pinned manager tests enabled rules with `matchesStaticSelector` when looking up rules for a workspace. These anchors establish a static-selector path, not a complete account of selectors that might change dynamically. [[ref], `content/Configuring/Workspace-Rules.md:15-16,44-48`; [ref], `src/config/shared/workspace/WorkspaceRuleManager.cpp:34-52`]

## Rule keys and parsing

The legacy wiki's rule table documents `monitor`, `default`, `gapsin`, `gapsout`, `bordersize`, `border`, `shadow`, `rounding`, `decorate`, `persistent`, `on-created-empty`, `defaultName`, `layout`, and `animations`. The pinned v0.56.2 handler recognizes those applicable keys and also has a `layoutopt` branch; its key is singular `animation:` (the wiki table spells `animations:s`). For the implementation's accepted branches and storage fields, see the handler lines cited below. [[ref], `content/Configuring/Workspace-Rules.md:84-101`; [ref], `src/config/legacy/ConfigManager.cpp:1713-1774`]

`gapsin:` and `gapsout:` split their values on spaces and parse them as CSS-like gap data. One integer applies to all sides; two mean vertical/horizontal; three mean top/horizontal/bottom; four mean top/right/bottom/left. The default branch for more than four values warns and constructs from the first four. [[ref], `src/config/legacy/ConfigManager.cpp:1715-1726`; [ref], `src/config/shared/complex/ComplexDataTypes.hpp:80-117`]

`bordersize:` is converted with `std::stoi`. The `border:`, `shadow:`, `rounding:`, `decorate:`, `default:`, and `persistent:` values go through `ParserUtils::parseInt`; the first three are stored in inverted `m_no*` fields, while the latter three are assigned directly. [[ref], `src/config/legacy/ConfigManager.cpp:1727-1750`; [ref], `src/config/shared/parserUtils/ParserUtils.cpp:134-149`]

That integer parser recognizes lowercase prefixes `true`, `on`, and `yes` as 1, and `false`, `off`, and `no` as 0; it also handles `0x` input and otherwise parses a signed integer. The boolean-like rule keys therefore do not use a strict true/false-only grammar or restrict integer values to 0 and 1. [[ref], `src/config/shared/parserUtils/ParserUtils.cpp:134-149`; [ref], `src/config/legacy/ConfigManager.cpp:1731-1750`]

The `on-created-empty:` branch passes the remainder to `cleanCmdForWorkspace` using the resolved workspace name. The helper trims the command; if it begins with a bracketed rule block, it replaces each rule starting with `workspace` with `workspace NAME`, or appends that rule if none exists. Without a bracketed block, it creates `[workspace NAME]`; it then joins the block and command with a space. An empty trimmed command returns no value, which the handler treats as a workspace-rule parse failure. [[ref], `src/config/legacy/ConfigManager.cpp:1706-1711,1753-1755`; [ref], `src/helpers/MiscFunctions.cpp:478-512`]

`layoutopt:` requires a further colon and stores its name/value pair; `layout:` stores a layout string; `animation:` stores an animation-style string. The handler has no final unknown-key error branch in the cited assignment chain. [[ref], `src/config/legacy/ConfigManager.cpp:1756-1776`]

## Merge and enabled rules

When a new parsed rule has the same exact selector string as an existing enabled rule, `replaceOrAdd` calls `mergeLeft` on that existing object instead of appending a new one; if no such enabled exact-string match exists, it adds a rule. At workspace lookup, the manager skips disabled rules, checks each remaining selector with `matchesStaticSelector`, and merges every match into the result. This describes storage and lookup merging; the allowed source report does not establish field-by-field conflict precedence inside `mergeLeft`. [[ref], `src/config/shared/workspace/WorkspaceRuleManager.cpp:21-52`]

## Config line → table effect

| Config line | Pinned parser / manager effect | JSON-table effect located in the allowed source material |
| --- | --- | --- |
| `workspace = SELECTOR, RULES` | Parses the selector and rule list, then calls `replaceOrAdd`. An enabled rule with the exact same selector string is merged in place; otherwise a new rule is added. [[ref], `src/config/legacy/ConfigManager.cpp:1676-1686,1781-1792`; [ref], `src/config/shared/workspace/WorkspaceRuleManager.cpp:21-32]` | The [ref] source-opening report says `workspaceRulesRequest` iterates workspace rules. It does not enumerate the JSON row members or establish output ordering. [[ref], `src/debug/HyprCtl.cpp:613-620`; [INF] exact row shape/order not located in the allowed report text.]
| `gapsin:...`, `gapsout:...` | Stores expanded gap data in `m_gapsIn` or `m_gapsOut`. [[ref], `src/config/legacy/ConfigManager.cpp:1715-1726`; [ref], `src/config/shared/complex/ComplexDataTypes.hpp:80-117]` | [INF] Exact JSON member names and omission rules for these fields are not located in the allowed source reports/fetch bins.
| `bordersize:...` | Parses an integer into `m_borderSize`. [[ref], `src/config/legacy/ConfigManager.cpp:1727-1730]` | [INF] Exact JSON member name and omission rule are not located in the allowed source reports/fetch bins.
| `border:...`, `shadow:...`, `rounding:...`, `decorate:...`, `default:...`, `persistent:...` | Parses integer/boolean-like values and stores the fields described above. [[ref], `src/config/legacy/ConfigManager.cpp:1731-1750`; [ref], `src/config/shared/parserUtils/ParserUtils.cpp:134-149]` | [INF] The source report does not enumerate their JSON member names or establish whether values are emitted as booleans, numbers, or omitted fields.
| `monitor:...`, `defaultName:...`, `layoutopt:...`, `layout:...`, `animation:...` | Stores monitor, default-name, layout-option, layout, or animation-style data. [[ref], `src/config/legacy/ConfigManager.cpp:1743-1774]` | [INF] Their JSON exposure or omission is not located in the allowed source reports/fetch bins.
| `on-created-empty:COMMAND` | Cleans the command and stores the result in `m_onCreatedEmptyRunCmd`. [[ref], `src/config/legacy/ConfigManager.cpp:1753-1755`; [ref], `src/helpers/MiscFunctions.cpp:478-512]` | The [ref] source-opening report specifically says the optional stored command is serialized under JSON key `onCreatedEmpty`. Whether the absent optional is omitted, emitted as null, or handled another way is [INF]. [[ref], `src/debug/HyprCtl.cpp:522-548]`
| Enabled/disabled state | The manager considers only enabled rules for exact-selector replacement and workspace lookup. [[ref], `src/config/shared/workspace/WorkspaceRuleManager.cpp:25-47]` | [INF] The allowed report text does not establish a JSON `enabled` member, its value/type, or whether disabled rules appear in the command output.

**JSON evidence limit.** The allowed [ref] report identifies the serializer range and confirms the `onCreatedEmpty` key, and identifies the request's rule iteration. It does not quote the rest of `getWorkspaceRuleData`; therefore the complete exact JSON object shape, field omission behavior, `enabled` output, and table ordering remain [INF] here rather than inferred from parser member names. [[ref], `src/debug/HyprCtl.cpp:522-548,613-620`; [INF] serializer details not located in the allowed report text.]

## Open items

- **Lua-era behavior:** [INF] None of the allowed source reports or fetched bins locates Lua-era workspace-rule parsing or establishes compatibility with it.
- **Runtime `hyprctl keyword workspace`:** [INF] The allowed material locates legacy config registration and static handler behavior, but not the runtime keyword dispatch path or whether it constructs the same table.
- **Dynamic selectors:** The wiki documents existing-workspace selectors and the manager uses `matchesStaticSelector`; [INF] the allowed sources do not establish dynamic selector forms or update semantics beyond those anchors. [[ref], `content/Configuring/Workspace-Rules.md:15-19,44-48`; [ref], `src/config/legacy/ConfigManager.cpp:608-610`; [ref], `src/config/shared/workspace/WorkspaceRuleManager.cpp:34-52`]
- **Exact emitted table schema:** [VERIFIED via measurement at 20022a65] the emitted member order and omission behavior are exactly `workspaceString, enabled, monitor, default, persistent, gapsIn, gapsOut, borderSize, border, rounding, decorate, shadow, defaultName, onCreatedEmpty` (unset members omitted), as enforced entry-by-entry by the frozen comparator in `.ufo/waves/round-27/c1/count-v4.py`.

[VERIFIED] The note semantics were confirmed by measurement: `verified-at: 20022a65` passed PRED-C1-r27-v4 41/41 (seed 4cfdf858277ad362, `evidence/c1-after-20022a65.txt`); on-created-empty behavior (`[workspace X] cmd` with no leading colon) is exercised by the counter population's ONEMPTY cases.