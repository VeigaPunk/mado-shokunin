# Round 24 wave 1 — WindowRuleApplicator source findings

## Behavior and scoped findings

At the pinned Hyprland v0.56.2 source, `readStaticRules()` clears its prior static state and traverses `ruleEngine()->rules()`. It considers window rules, calls `matches(..., true)`, skips non-matches, queues exec rules, and for other matches calls `applyStaticRule()` followed by `applyDynamicRule()`. Queued exec rules are applied after the ordinary loop. The `recheckStaticRules()` path checks rules against `propsToRecheck` and reapplies matching static rules. On `propertiesChanged()`, the applicator resets affected dynamic properties, filters candidate rules by property/effect masks, calls `matches()`, reapplies dynamic effects, and then updates window/decorations. These observations describe source code paths, not a live compositor run.

For ordinary dynamic effects, handlers set a `COverridableVar` value with `PRIORITY_WINDOW_RULE`; property-mask fields are assigned or ORed from `rule->getPropertiesMask()`. Custom dynamic properties retain an effect index, property mask, and effect string. Dynamic tags are held as tag-string/property-mask pairs. The header's generated dynamic-property layout pairs a `COverridableVar` with a rule-property mask. This is a reset/recheck association with rule-property conditions, not an explicit per-value originating-rule identifier in the inspected fields. The applicator separately has an `m_execRules` vector of `SP<CWindowRule>` objects, but that does not show that ordinary applied property values keep their source rule.

A scoped sweep of the two fetched files found zero occurrences of the explicit lexical markers listed below (`origin`, `sourceRule`, `source_rule`, `ruleId`, `rule_id`, `matchedRule`, `matched_rule`, `originRule`, `origin_rule`). This is not proof that no provenance representation exists elsewhere or under other names; the conclusion is limited to these two files and their visible property state/writes.

The files show traversal of the rule collection and a `PRIORITY_WINDOW_RULE` argument passed to setters. They do not establish `COverridableVar`'s equal-priority/tie-breaking semantics or identify which matching rule wins when several write the same value. That implementation and upstream list construction were not opened. No `getprop`/user-facing attribution behavior or host behavior is established here; host behavior remains [UNK].

## Proposed claim rows

Each row is a draft for `corpus/knowledge/rule-attribution-r24.md`. `S?` is intentionally provisional; the integrating source registrar assigns final S### IDs. The quotes below were checked byte-for-byte after whitespace collapse against the fetched files.

### WindowRuleApplicator.cpp

| A1 | The static pass calls `matches` before applying static and dynamic effects for matching non-exec rules. | S? | "if (!wr->matches(m_window.lock(), true)) continue; if (wr->isExecRule()) { m_execRules.emplace_back(wr); continue; } applyStaticRule(wr); const auto RES = applyDynamicRule(wr);" |
| A2 | The static read function loops over `ruleEngine()->rules()` after clearing prior static state. | S? | "bool CWindowRuleApplicator::readStaticRules(bool preRead) { if (!m_window) return false; static_ = {}; m_execRules.clear(); bool tagsWereChanged = false; for (const auto& r : ruleEngine()->rules()) {" |
| A3 | The handler passes `PRIORITY_WINDOW_RULE` as the second argument when setting allows-input. | S? | "m_allowsInput.first.set(std::get<bool>(value), Types::PRIORITY_WINDOW_RULE);" |
| A4 | The alpha field stores `rule->getPropertiesMask()` in its companion mask slot. | S? | "m_alpha.second = rule->getPropertiesMask();" |

### WindowRuleApplicator.hpp

| A5 | Each generated property pairs a `COverridableVar` value with a rule-property mask. | S? | "std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};" |
| A6 | The custom-property layout exposes the `propMask` member as an eRuleProperty mask. | S? | "std::underlying_type_t<eRuleProperty> propMask = RULE_PROP_NONE;" |
| A7 | Dynamic tags use `m_dynamicTags` to pair each tag string with a property mask. | S? | "std::vector<std::pair<std::string, std::underlying_type_t<eRuleProperty>>> m_dynamicTags;" |
| A8 | The class declares `m_execRules` as a vector of `SP<CWindowRule>` values. | S? | "std::vector<SP<CWindowRule>> m_execRules;" |

## Draft SOURCES rows

These have the requested 11-cell shape; IDs remain provisional until integration. The scope cell marks both as area A/code sources.

| S? | Hyprland v0.56.2 WindowRuleApplicator.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | code | A | Window-rule matching, static and dynamic application, property masks, reset, and setter priority | src/desktop/rule/windowRule/WindowRuleApplicator.cpp:81-84,118-124,151-158,234-235,378-509,547-579 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b, 27092 B | Shows matching/traversal and dynamic property writes with a window-rule priority argument and property-mask bookkeeping; does not establish COverridableVar tie semantics or host behavior | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 WindowRuleApplicator.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.hpp | code | A | Applicator state layout and property/effect tracking | src/desktop/rule/windowRule/WindowRuleApplicator.hpp:25-38,63-72,74-88,140-158 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44, 9865 B | Defines overridable-value/property-mask pairs, custom effect state, tag masks, and a separate exec-rule collection; does not define external override semantics | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Commands, receipts, and gates

The two external source files were fetched only from the required pinned raw URLs to the designated receipt paths. Commands and outputs:

```sh
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin
```

Output: `fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b` and `27092` bytes.

```sh
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-2.bin
```

Output: `334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44` and `9865` bytes.

Python whitespace-collapsed quote check (all eight outputs were `PASS`):

```sh
timeout 30s python3 -I -c 'from pathlib import Path; import re; norm=lambda s: re.sub(r"\s+", " ", s).strip(); files=[(Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin"), ["if (!wr->matches(m_window.lock(), true)) continue; if (wr->isExecRule()) { m_execRules.emplace_back(wr); continue; } applyStaticRule(wr); const auto RES = applyDynamicRule(wr);", "bool CWindowRuleApplicator::readStaticRules(bool preRead) { if (!m_window) return false; static_ = {}; m_execRules.clear(); bool tagsWereChanged = false; for (const auto& r : ruleEngine()->rules()) {", "m_allowsInput.first.set(std::get<bool>(value), Types::PRIORITY_WINDOW_RULE);", "m_alpha.second = rule->getPropertiesMask();"]), (Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-2.bin"), ["std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};", "std::underlying_type_t<eRuleProperty> propMask = RULE_PROP_NONE;", "std::vector<std::pair<std::string, std::underlying_type_t<eRuleProperty>>> m_dynamicTags;", "std::vector<SP<CWindowRule>> m_execRules;"])]; print("\n".join(p.name+" quote "+str(n)+": "+("PASS" if norm(q) in norm(p.read_bytes().decode("utf-8")) else "FAIL") for p,qs in files for n,q in enumerate(qs,1)))'
```

Exact output:

```text
SrcWindowRuleApplicator-1.bin quote 1: PASS
SrcWindowRuleApplicator-1.bin quote 2: PASS
SrcWindowRuleApplicator-1.bin quote 3: PASS
SrcWindowRuleApplicator-1.bin quote 4: PASS
SrcWindowRuleApplicator-2.bin quote 1: PASS
SrcWindowRuleApplicator-2.bin quote 2: PASS
SrcWindowRuleApplicator-2.bin quote 3: PASS
SrcWindowRuleApplicator-2.bin quote 4: PASS
```

Origin-marker sweep command:

```sh
timeout 30s python3 -I -c 'from pathlib import Path; import re; ps=[Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin"),Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-2.bin")]; texts=[p.read_bytes().decode("utf-8") for p in ps]; terms=["origin","sourceRule","source_rule","ruleId","rule_id","matchedRule","matched_rule","originRule","origin_rule"]; print("\n".join(t+": "+str(sum(len(re.findall(re.escape(t),s,re.I)) for s in texts)) for t in terms))'
```

Exact output: `origin: 0`, `sourceRule: 0`, `source_rule: 0`, `ruleId: 0`, `rule_id: 0`, `matchedRule: 0`, `matched_rule: 0`, `originRule: 0`, `origin_rule: 0`.

The round-24 C1 target is `PASS_ROW >= 6` from at least three distinct sources and an indexed note. This scoped report proposes eight rows over two source files only. No final source IDs were allocated here, no C1 counter was run, no SOURCES.md or knowledge note was edited, and these proposals alone do not meet the target. No build, tests, host/compositor commands, git/jj writes, package installs, or other verification were performed.

## Touched surfaces and limits

- Report: `.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`.
- Required raw-byte receipts: `.ufo/waves/round-24/fetch/w1/SrcWindowRuleApplicator-1.bin` and `SrcWindowRuleApplicator-2.bin`.
- No product code, `SOURCES.md`, `corpus/knowledge/rule-attribution-r24.md`, or `corpus/README.md` was edited. The read-only local source clones were not used or modified. No tool was installed.
- Opened only the two requested Hyprland source files for external citations; local registration and report precedent reads provided task/report context, not source evidence. Scope excludes `COverridableVar` implementation, rule-engine construction/order, upstream getprop details, and runtime/host behavior.

**Verdict:** Pinned applicator source provides checked, on-topic draft evidence for match gating, rule traversal, setter priority arguments, and mask-based property state. It does not establish per-property originating-rule retention or tie-breaking; those findings remain scoped as stated. C1 integration and its frozen counter gate remain unrun.