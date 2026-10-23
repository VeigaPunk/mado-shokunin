author: mado

# Round 24 — repair-first routing, rule attribution route, capability re-demonstration

Base: lane tip `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`. Registration `.ufo/waves/round-24/registration.md` (landed
`8efd00af`; C1 counter v2 `c9b76646`; C2 counter and manifest `4f21d995`; control receipts `464a0245`, all before any data
seat). Claims: C1 coverage (Hyprland window-rule attribution route), C2 calibration (SCORECARD capability table versus
frozen re-demonstration). Unless a full path is given, `w1/`, `w2/`, `controls/` and `evidence/` resolve under
`.ufo/waves/round-24/`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M24-1 | counter design | C1 counter v1 (`d9fec1d3`, sha256:`2fc366ab…2291`) reached `TARGET_MET` on two pre-data controls: real on-topic quotes beside unsupported claims (`controls/CtlC1LabelShortcut.md`) and real off-topic pinned lines that happen to contain a topic word (`controls/CtlC1OffTopic.md`) | the pre-freeze control wave (operator 01:05Z directive) | v2 (`c9b76646`) adds the claim-anchor clause before any data seat; v2 scores both controls 0 (`PASS_ROW=0`, `claim-not-anchored-to-quote`), so the fix is shown able to fail on the exact shapes that beat v1. |
| M24-2 | counter design (residual) | v2 is still met by true but non-attribution rule lines: `w1/reports/RevRegistration.md` H1 (generic wiki rule sentences, `PASS_ROW=6 … TARGET_MET`) and `w1/reports/CritC1Predicate.md` (udev "rules" lines from one wiki page registered under three ids, also commented-out rows) | none of the twelve controls; found by wave-1 reviewer and critic during data | Not fixed this round: the C1 predicate is frozen and is not amended after data. Next counter must count distinct sha256 documents rather than ids, require a rule-context term (window rule, layer rule, getprop, rule name) instead of bare `rule`/`match`, strip HTML comments before reading rows, and check the quote lies inside the row's anchor span. Wave 2 judged each landed row's attribution relevance by hand (see `## Wave-2 dispositions`). |
| M24-3 | report chronology | `inherited/r23-post-close-*.md` (from `w1/reports/ScribeLessonMistake.md`): two round-23 seat reports were rewritten after the round-23 tip `fa819d56` (mtimes 09:23 and 09:27 −03 vs tip 09:12:44) and a third (`ScribeRejectSweep.md`) was never committed; the closure reviewed the committed tip | none | Round 24 kept the late copies as evidence and reverted the round-23 paths to their committed bytes. Proposed check (not built, so not counted as a fix): before filing, every assigned report path exists at the filed tip and its sha256 equals the seat's final copy; it would fail on this sample (`ScribeRejectSweep.md` absent). |
| M24-4 | coordination | during the control wave the round-24 L1 sent a one-character message (`x`) to `agent://all`; the tool reported delivery to 101 peers, including Main and seats of other lanes, and Main and many seats replied asking for the full question | the round contract ("never `agent://all`") — a written rule with no tool guard | Acknowledged to Main the same minute; no further broadcast. No tool fix: the write device has no lane scope guard. |

## Gate

Start census, command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`, exact output (receipt `evidence/sources-start.txt`):

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
census rc=0
```

### New SOURCES rows (opened 2026-10-23 by wave-1 seats; fetched bytes `fetch/S###.bin`)

| id | URL | opened | located quote (≤25 words; whitespace-collapsed) | status |
|---|---|---|---|---|
| S153 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp | 2026-10-23 | "void CRuleEngine::registerRule(SP<IRule>&& rule) { m_rules.emplace_back(std::move(rule)); }" (6 words; row A1) | mined |
| S154 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.hpp | 2026-10-23 | "const std::vector<SP<IRule>>& rules(); private: std::vector<SP<IRule>> m_rules;" (6 words; row A2) | mined |
| S155 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | 2026-10-23 | "if (!wr->matches(m_window.lock(), true)) continue; if (wr->isExecRule()) { m_execRules.emplace_back(wr); continue; } applyStaticRule(wr); const auto RES = applyDynamicRule(wr);" (16 words; row A3) | mined |
| S156 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.hpp | 2026-10-23 | "std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};" (6 words; row A7) | mined |
| S157 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.cpp | 2026-10-23 | "case RULE_PROP_TAG: if (!engine->match(w->m_ruleApplicator->m_tagKeeper)) return false; break;" (7 words; row A9) | mined |
| S158 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | 2026-10-23 | "const auto tags = w->m_ruleApplicator->m_tagKeeper.getTags();" (5 words; row A10) | mined |
| S159 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsConfigRules.cpp | 2026-10-23 | "if (!name.empty()) self->m_luaWindowRules[name] = rule; Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));" (6 words; row A12) | mined |
| S160 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.cpp | 2026-10-23 | "rule->setEnabled(lua_toboolean(L, 2)); Desktop::Rule::ruleEngine()->updateAllRules();" (3 words; row A13) | mined |
| S161 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp | 2026-10-23 | "query.className = Internal::tableOptStr(L, idx, "class"); query.title = Internal::tableOptStr(L, idx, "title"); query.tag = Internal::tableOptStr(L, idx, "tag");" (15 words; row —) | queued |
| S162 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | 2026-10-23 | "m_config->addSpecialCategory("windowrule", {.key = "name"});" (4 words; row A15) | mined |
| S163 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.cpp | 2026-10-23 | "if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);" (4 words; row A17) | mined |
| S164 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | 2026-10-23 | "Rule workspace matched by {}, {} applied." (7 words; row A18) | mined |
| S165 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md | 2026-10-23 | "hl.window_rule({ name? = string, match = { prop = some_prop_value, }, effect = some_effect_value, })" (15 words; row A19) | mined |
| S166 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/layer-rules.md | 2026-10-23 | "Layer rules also return a handle with `set_enabled()`/`is_enabled()`:" (8 words; row A23) | mined |
| S167 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md | 2026-10-23 | "workspacerules - gets the list of defined workspace rules" (9 words; row A24) | mined |
| S168 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md | 2026-10-23 | "_All_ props must match for a rule to be applied." (10 words; row A25) | mined |

All sixteen pins: Hyprland tag `v0.56.2` = commit `efb50993780079460b0cbed1363e2166a2de1d9f` (host `hyprctl version`
names the same commit); hyprland-wiki commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`. S161 is `queued` (its only
quote cell contains `||`, which breaks a markdown table row; the tag filter it shows is restated in the note's prose).

Status, recheck and used-by changes on pre-existing rows: none.

### Opened but not registered

Wave-1 seats opened and hashed further pinned files that the note does not cite; they are not rows:
`desktop/rule/Rule.cpp` (SrcRuleBase), `desktop/rule/Rule.hpp` (SrcRuleBase), `desktop/rule/RuleWithEffects.hpp` (SrcRuleBase), `desktop/rule/windowRule/WindowRule.hpp` (SrcWindowRule), `desktop/rule/windowRule/WindowRuleEffectContainer.cpp` (SrcEffectContainer), `desktop/rule/windowRule/WindowRuleEffectContainer.hpp` (SrcEffectContainer), `desktop/rule/effect/EffectContainer.hpp` (SrcEffectContainer), `config/lua/objects/LuaWindowRule.hpp` (SrcLuaRules), `desktop/rule/layerRule/LayerRuleEffectContainer.cpp` (SrcLayerRule), `desktop/rule/layerRule/LayerRule.cpp` (SrcLayerRule), `desktop/rule/layerRule/LayerRuleApplicator.hpp` (SrcLayerRule), `desktop/rule/layerRule/LayerRuleEffectContainer.hpp` (SrcLayerRule), `desktop/rule/layerRule/LayerRule.hpp` (SrcLayerRule), `desktop/view/Window.hpp` (SrcWindowView), `configuring/core/rules/workspace-rules.md` (WikiLayerRules), `contributing-and-debugging/_index.md` (WikiDebugging), `crashes-and-bugs/_index.md` (WikiDebugging), `configuring/core/config-options.md` (WikiDebugging), `configuring/core/environment-variables.md` (WikiDebugging); plus the WikiTags (2), SrcMatchEngine (12), SrcRuleLogSweep (17), ScoutAttributionSweep (22) and
ScoutWikiEra (25) receipts under `fetch/w1/` (used for negative sweeps and era checks, cited by report path).

## Routed defects of `round-23-verifier-spotcheck.md` §7

1. Stale "note does not yet exist" — corrected append-only at the end of `lessons/round-23.md` (lane `d9fec1d3`).
2. README withdrawal pointer — appended to `corpus/README.md` round-23 section (`d9fec1d3`).
3. Lesson-23 M23-4, M23-5, M23-7 without criteria — QUALITY criteria 33–35 (`39c59630`), checks
   `quality/check-registration-order.py` (red on round 23, exit 1; receipt `quality/m23-4-7-red-green.txt`) and
   `quality/check-receipt-provenance.py` (red on the committed round-23 `l1-attacks.sh`, 5 reasons; green on a corrected
   fixture; receipt `quality/m23-5-red-green.txt`).
4. sha256 labels — every sha256 in round-24 files and the report carries `sha256:`.
5. S149 anchor — see `## Wave-2 dispositions` (the re-opened blob places the sentence on a different span than the closure stated).
6. r23 regression fixtures — frozen as a registered population: `carry/` (28 fixtures, `carry/manifest.json`, base run
   `carry/base-run.txt`, classifier sha256:`cd9da20c…ea84` unchanged).
7. H2 precision 166/175 — not repaired; L0 question at fleet `.ufo/l0-questions.md:103` still open. C2's status table now
   records its effect on the `tripwire evidence marker` capability (L 15/18).
