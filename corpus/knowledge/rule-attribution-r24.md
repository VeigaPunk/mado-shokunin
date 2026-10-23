source: S153, S154, S155, S156, S157, S158, S159, S160, S162, S163, S164, S165, S166, S167, S168 (opened 2026-10-23; Hyprland v0.56.2 = commit efb50993780079460b0cbed1363e2166a2de1d9f, hyprland-wiki commit c66e8de21f5ecdc4bc5e278e7d94800ea10957af)
verified-at: 2026-10-23 (pinned upstream bytes; host read verbs `hyprctl version` and `hyprctl clients -j` key list only)
recheck: on-release (Hyprland tag after v0.56.2, or a wiki change to content/configuring/core/rules/)
covers: rule attribution (corpus/README.md frontier, round-12 bullet "Still open: rule *attribution*")
author: mado (round 24; claim rows drafted by wave-1 source seats, integrated by the L1)

# Rule attribution in Hyprland 0.56.2 — what upstream lets you see

**Question.** A window shows an effect (opacity, float, size, a tag). Which window or layer rule produced it,
and what does Hyprland 0.56.2 offer to tell? The round-12 note
[`window-rule-effects-getprop.md`](window-rule-effects-getprop.md) settled the *effect* read (`hyprctl getprop`
returns the applied value, no rule name); [`keybind-rule-semantics.md`](keybind-rule-semantics.md) holds the
declared ordering semantics. This entry covers the remaining frontier item: *attribution*.

**Answer (documentary, v0.56.2).** No upstream channel maps an applied property back to the rule that set it.
What exists is narrower:

| Want | Route in v0.56.2 | What it shows | What it does not show |
|---|---|---|---|
| applied value of one property | `hyprctl getprop <window> <property>` (A11) | the applicator's current value | which rule, or whether a rule set it at all |
| which rules exist | config bytes only; `hyprctl workspacerules` lists **workspace** rules (A24) | declared rules | there is no window-rule or layer-rule listing verb (sweep below) |
| which rule fired on a window | **tag route**: give the rule a unique `tag` effect, then read `tags` in `hyprctl clients` (A10, A22) | the tag set the applicator's tag keeper holds (A9, A10) | provenance when two rules add the same tag; dynamic tags carry a `*` suffix (A22) |
| enable or disable a rule to test it | named rule handle: Lua `set_enabled`/`is_enabled` (A12–A14; layer rules A23) | whether the effect disappears when the rule is off | this mutates compositor state — operator only, never a mado probe |
| per-property origin | applicator stores a value plus a **rule-property mask** and a priority class (A5–A8) | which *match properties* a setting came through, and that it was a window rule | the rule's identity; neither is exported by hyprctl, Lua or socket2 |
| logs | none name a rule; the one matched-by log line is the workspace-rule path (A18) | — | window/layer rule identity |

Ordering still decides which value wins: named rules first, then anonymous, top to bottom, last match wins (A21,
A25, A26). Attribution by reasoning therefore means reading the declared files in that order; it is an inference,
not an observed fact.

## Claim rows (each quote re-opens verbatim in its pinned bytes; counted by `.ufo/waves/round-24/c1/count.py`)

| id | claim | source | quote |
|---|---|---|---|
| A1 | The `registerRule` implementation appends each supplied rule to `m_rules`. | S153 | "void CRuleEngine::registerRule(SP<IRule>&& rule) { m_rules.emplace_back(std::move(rule)); }" |
| A2 | The header declares a `rules` accessor and keeps `m_rules` as the engine's private vector. | S154 | "const std::vector<SP<IRule>>& rules(); private: std::vector<SP<IRule>> m_rules;" |
| A3 | The static pass calls `matches` before applying static and dynamic effects for matching non-exec rules. | S155 | "if (!wr->matches(m_window.lock(), true)) continue; if (wr->isExecRule()) { m_execRules.emplace_back(wr); continue; } applyStaticRule(wr); const auto RES = applyDynamicRule(wr);" |
| A4 | The static read function loops over `ruleEngine()->rules()` after clearing prior static state. | S155 | "bool CWindowRuleApplicator::readStaticRules(bool preRead) { if (!m_window) return false; static_ = {}; m_execRules.clear(); bool tagsWereChanged = false; for (const auto& r : ruleEngine()->rules()) {" |
| A5 | The handler passes `PRIORITY_WINDOW_RULE` as the second argument when setting allows-input. | S155 | "m_allowsInput.first.set(std::get<bool>(value), Types::PRIORITY_WINDOW_RULE);" |
| A6 | The alpha field stores `rule->getPropertiesMask()` in its companion mask slot. | S155 | "m_alpha.second = rule->getPropertiesMask();" |
| A7 | Each generated property pairs a `COverridableVar` value with a rule-property mask. | S156 | "std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};" |
| A8 | Dynamic tags use `m_dynamicTags` to pair each tag string with a property mask. | S156 | "std::vector<std::pair<std::string, std::underlying_type_t<eRuleProperty>>> m_dynamicTags;" |
| A9 | The `RULE_PROP_TAG` matcher tests the rule applicator tag keeper and rejects a failed engine match. | S157 | "case RULE_PROP_TAG: if (!engine->match(w->m_ruleApplicator->m_tagKeeper)) return false; break;" |
| A10 | Each `clients` JSON entry includes its tags, sourced from that window's `m_ruleApplicator` tag keeper. | S158 | "const auto tags = w->m_ruleApplicator->m_tagKeeper.getTags();" |
| A11 | The `getprop` opacity branch tests `PROP` and passes the selected window's `m_ruleApplicator` alpha to `alphaToString`. | S158 | "if (PROP == "opacity") return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);" |
| A12 | For non-empty names, `m_luaWindowRules` stores each rule by name before engine registration. | S159 | "if (!name.empty()) self->m_luaWindowRules[name] = rule; Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));" |
| A13 | The setter applies the supplied boolean to the rule and calls `updateAllRules`. | S160 | "rule->setEnabled(lua_toboolean(L, 2)); Desktop::Rule::ruleEngine()->updateAllRules();" |
| A14 | For a live rule, this pushes its `isEnabled` flag as one Lua boolean result. | S160 | "const auto rule = ref->lock(); if (!rule) { lua_pushnil(L); return 1; } lua_pushboolean(L, rule->isEnabled()); return 1;" |
| A15 | This file declares the special `windowrule` category with `name` as its key. | S162 | "m_config->addSpecialCategory("windowrule", {.key = "name"});" |
| A16 | This loop traverses `windowrule` names returned by the special-category key-list API. | S162 | "for (const auto& name : m_config->listKeysForSpecialCategory("windowrule")) {" |
| A17 | A layer rule is applied dynamically only after the associated surface passes `wr->matches`. | S163 | "if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);" |
| A18 | CWindow log text says `Rule workspace matched by` and contains two `{}` placeholders before `applied`. | S164 | "Rule workspace matched by {}, {} applied." |
| A19 | The documented `hl.window_rule` syntax shows optional `name`, `match`, and `effect` fields. | S165 | "hl.window_rule({ name? = string, match = { prop = some_prop_value, }, effect = some_effect_value, })" |
| A20 | The wiki says effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes. | S165 | "Effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes." |
| A21 | The wiki states effects are processed top to bottom, and the _last_ match takes precedence. | S165 | "Effects are processed top to bottom, and the _last_ match takes precedence." |
| A22 | The page states dynamic tags have a suffix of `*` and tells readers to check window tags with `hyprctl clients`. | S165 | "Window tags can be static or dynamic. Dynamic tags have a suffix of `*`. Check window tags with `hyprctl clients`." |
| A23 | The page says layer rules return a handle exposing `set_enabled()` and `is_enabled()` controls. | S166 | "Layer rules also return a handle with `set_enabled()`/`is_enabled()`:" |
| A24 | `workspacerules` is documented to list defined workspace rules. | S167 | "workspacerules       - gets the list of defined workspace rules" |
| A25 | The wiki states: _All_ props must match for a rule to be applied. | S168 | "_All_ props must match for a rule to be applied." |
| A26 | Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones. | S168 | "Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones." |

## Negative sweeps (who said it, and how)

- **No attribution channel.** Wave-1 seat ScoutAttributionSweep swept the v0.56.2 tree per channel: hyprctl
  (`getprop` renders the applicator value, `src/debug/HyprCtl.cpp:1548-1553`; the only rule-listing verb is
  `workspacerules`, `:2005`), Lua (`LuaWindowRule.cpp:58-70` exposes only `set_enabled`/`is_enabled`), socket2
  (35 event names, none for rules), logs, the window object (`OverridableVar.hpp:153` keeps one optional value per
  override priority; `getPriority()` is not exported) and the plugin bus (`updateRules` carries the window only).
  Verdict NEGATIVE on every channel. Report `.ufo/waves/round-24/w1/reports/ScoutAttributionSweep.md`.
- **Logs.** SrcRuleLogSweep: 15 log calls under `src/desktop/rule/`, none prints a rule name; five are TRACE-gated
  (`HYPRLAND_TRACE`). Report `.ufo/waves/round-24/w1/reports/SrcRuleLogSweep.md`.
- **Unnamed hyprlang inline rules.** `IRule::name()` is read only by the engine and the Lua registry; inline
  `windowrule = …` lines are registered unnamed, block rules are keyed by `name` (A15, A16). Source:
  ScoutAttributionSweep (`legacy/ConfigManager.cpp:2019`).

These sweeps are lane observations over the pinned clone, not upstream statements; they are not counted rows.

## Host join (read-only, 2026-10-23; ScoutHostRules)

`hyprctl version` first line names commit `efb50993…` (the pin). The live plane declares 82 rule sites (77 inline
`windowrule`, 3 block `windowrule`, 2 `layerrule`); 3 named block rules (`geforce`, `jetbrains-focus`,
`moonlight`), all from omarchy defaults; 21 rule lines carry a `tag` effect. `hyprctl clients -j`: 4 windows,
`tags` present on 4/4 (only the key list was read, never tag values or titles). So the tag route is available on
this host; which rule produced a given tag is still not observed. Report
`.ufo/waves/round-24/w1/reports/ScoutHostRules.md`.

## Limits and unknowns

- Era: the wiki commit is latest-git documentation and shows Lua `hl.window_rule()` syntax (A19); the host runs
  0.56.2 with `configProvider: hyprlang` (round-12 config-era note). Wiki rows are `[INF-docs]` for this host.
- Host behaviour is `[UNK]`: no rule was toggled, no dispatch or reload ran, no tag value was read.
- A plugin could record matches itself (the applicator keeps dynamically registered props readable by plugins);
  none is installed here — `[INFERENCE]`, not checked.

## Provenance of rows

- A1: drafted by wave-1 seat `SrcRuleEngine` (`.ufo/waves/round-24/w1/reports/SrcRuleEngine.md`)
- A2: drafted by wave-1 seat `SrcRuleEngine` (`.ufo/waves/round-24/w1/reports/SrcRuleEngine.md`)
- A3: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A4: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A5: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A6: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A7: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A8: drafted by wave-1 seat `SrcWindowRuleApplicator` (`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`)
- A9: drafted by wave-1 seat `SrcWindowRule` (`.ufo/waves/round-24/w1/reports/SrcWindowRule.md`)
- A10: drafted by wave-1 seat `SrcHyprCtl` (`.ufo/waves/round-24/w1/reports/SrcHyprCtl.md`)
- A11: drafted by wave-1 seat `SrcHyprCtl` (`.ufo/waves/round-24/w1/reports/SrcHyprCtl.md`)
- A12: drafted by wave-1 seat `SrcLuaRules` (`.ufo/waves/round-24/w1/reports/SrcLuaRules.md`)
- A13: drafted by wave-1 seat `SrcLuaRules` (`.ufo/waves/round-24/w1/reports/SrcLuaRules.md`)
- A14: drafted by wave-1 seat `SrcLuaRules` (`.ufo/waves/round-24/w1/reports/SrcLuaRules.md`)
- A15: drafted by wave-1 seat `SrcLegacyConfig` (`.ufo/waves/round-24/w1/reports/SrcLegacyConfig.md`)
- A16: drafted by wave-1 seat `SrcLegacyConfig` (`.ufo/waves/round-24/w1/reports/SrcLegacyConfig.md`)
- A17: drafted by wave-1 seat `SrcLayerRule` (`.ufo/waves/round-24/w1/reports/SrcLayerRule.md`)
- A18: drafted by wave-1 seat `SrcWindowView` (`.ufo/waves/round-24/w1/reports/SrcWindowView.md`)
- A19: drafted by wave-1 seat `WikiWindowRules` (`.ufo/waves/round-24/w1/reports/WikiWindowRules.md`)
- A20: drafted by wave-1 seat `WikiWindowRules` (`.ufo/waves/round-24/w1/reports/WikiWindowRules.md`)
- A21: drafted by wave-1 seat `WikiWindowRules` (`.ufo/waves/round-24/w1/reports/WikiWindowRules.md`)
- A22: drafted by wave-1 seat `WikiWindowRules` (`.ufo/waves/round-24/w1/reports/WikiWindowRules.md`)
- A23: drafted by wave-1 seat `WikiLayerRules` (`.ufo/waves/round-24/w1/reports/WikiLayerRules.md`)
- A24: drafted by wave-1 seat `WikiHyprctl` (`.ufo/waves/round-24/w1/reports/WikiHyprctl.md`)
- A25: drafted by wave-1 seat `WikiDebugging` (`.ufo/waves/round-24/w1/reports/WikiDebugging.md`)
- A26: drafted by wave-1 seat `WikiDebugging` (`.ufo/waves/round-24/w1/reports/WikiDebugging.md`)
