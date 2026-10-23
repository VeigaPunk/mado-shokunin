# Round 24 C1 source opener — layer-rule application

## Behavior observed

Pinned Hyprland source at `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2) shows `CLayerRuleApplicator::propertiesChanged` resetting properties, scanning rule-engine entries, filtering to `RULE_TYPE_LAYER` and intersecting property masks, then applying only rules whose `matches(m_ls.lock())` succeeds. It emits the layer `updateRules` event afterward. `applyDynamicRule` iterates a matched rule's effects and writes the static values at window-rule override priority; dynamic custom-effect entries retain an effect index, property mask, and effect string. The relevant implementation anchors are `LayerRuleApplicator.cpp:32-38,40-65,127-154` and `LayerRuleApplicator.hpp:25-34`.

This establishes layer-rule matching/application and a layer update event. It does not establish whether another upstream interface can identify to an operator which rule produced an applied effect. No inference about the existence or absence of such an interface is made here. Host behavior remains [UNK].

## Draft claim rows

`S?` is provisional. Integration assigns final `S###` IDs; these rows were not added to the note or `SOURCES.md` by this seat.

### `LayerRuleApplicator.cpp`

| A1 | The applicator's dynamic-rule path iterates over each element from `rule->effects`. | S? | "for (const auto& effectData : rule->effects()) {" |
| A2 | A layer rule is applied dynamically only after the associated surface passes `wr->matches`. | S? | "if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);" |

### `LayerRuleEffectContainer.cpp`

| A3 | The source comment says if we change the rules, we get reminded to update the strings. | S? | "// This is here so that if we change the rules, we get reminded to update // the strings." |
| A4 | The translation unit statically asserts that `LAYER_RULE_EFFECT_LAST_STATIC` equals 11. | S? | "// This is here so that if we change the rules, we get reminded to update // the strings. static_assert(LAYER_RULE_EFFECT_LAST_STATIC == 11);" |

### `LayerRule.cpp`

| A5 | When integer parsing fails, `numericParseError` is included in an error formatted with effect name and raw input. | S? | "return std::unexpected(std::format(\"{} rule \\\"{}\\\" failed with: {}\", effectName, raw, numericParseError(parsed.error())));" |
| A6 | The `above_lock` parser reports a `rule` failure with its raw input and numeric parse error. | S? | "return std::unexpected(std::format(\"above_lock rule \\\"{}\\\" failed with: {}\", raw, numericParseError(parsed.error())));" |

### `LayerRuleApplicator.hpp`

| A7 | The header says plugins may read props that were dynamically registered. | S? | "// This struct holds props that were dynamically registered. Plugins may read this." |
| A8 | The class declares `resetProps` with a property mask and override priority argument. | S? | "void propertiesChanged(std::underlying_type_t<eRuleProperty> props); void resetProps(std::underlying_type_t<eRuleProperty> props, Types::eOverridePriority prio = Types::PRIORITY_WINDOW_RULE);" |

### `LayerRuleEffectContainer.hpp`

| A9 | The namespace declaration names `Desktop::Rule` as this header's nested namespace. | S? | "namespace Desktop::Rule {" |
| A10 | The `eLayerRuleEffect` enumeration is declared inside `Desktop::Rule` with `uint8_t` as its underlying type. | S? | "namespace Desktop::Rule { enum eLayerRuleEffect : uint8_t {" |

### `LayerRule.hpp`

| A11 | The header defines `LayerRuleEffectValue` as a variant containing monostate, boolean, integer, float, and string alternatives. | S? | "namespace Desktop::Rule { using LayerRuleEffectValue = std::variant<std::monostate, bool, int64_t, float, std::string>;" |
| A12 | The header declares a `matches` method taking a parameter of type `PHLLS`. | S? | "bool matches(PHLLS w);" |

## Draft SOURCES rows

Each row has the required 11 cells. The `used-by` destination is the planned C1 note; final source IDs and SOURCES integration remain for the lane integrator.

| S? | LayerRuleApplicator.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.cpp | code | A | layer-rule application and matched effects | src/desktop/rule/layerRule/LayerRuleApplicator.cpp:40-149 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba, 6193 B | filters layer rules and property masks, applies matched effects, emits layer updateRules | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | LayerRuleEffectContainer.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp | code | A | layer effect string table and static boundary | src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp:27-29 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:753fa6fa508ded8d927ca44cf13bfbca79b98e77ea0026fcbf5dc6e0c62c774f, 1017 B | comments on updating effect strings when rules change and asserts the last static effect value | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | LayerRule.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRule.cpp | code | A | layer-rule parse diagnostics | src/desktop/rule/layerRule/LayerRule.cpp:27,43 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:f3e05eafeed061471fee843842db18127b905d2847faa738e763f4355f3c9bca, 3948 B | parse errors include effect name or above_lock rule, raw value, and numeric parse reason | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | LayerRuleApplicator.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.hpp | code | A | applicator property and plugin-visible declarations | src/desktop/rule/layerRule/LayerRuleApplicator.hpp:22-23,31-34 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:f62c45a977fa6dd5c4dcef245e791c56a33dc4a136ea2704696f6312f406b0fe, 3844 B | declares property-change/reset operations and describes dynamically registered properties readable by plugins | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | LayerRuleEffectContainer.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleEffectContainer.hpp | code | A | layer effect type declaration and namespace | src/desktop/rule/layerRule/LayerRuleEffectContainer.hpp:8-9 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d9b85eb9fee97d40b74dd54f3e417cd9e1e30e306667942d4cb451804498cb7d, 881 B | places the layer-effect enum in Desktop::Rule and declares its uint8_t base | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | LayerRule.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRule.hpp | code | A | layer-rule value type and match declaration | src/desktop/rule/layerRule/LayerRule.hpp:10-11,30 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:549a1a47e13afb9e2f8e1140e575996129da84c2bc8affbc4dced459beffea16, 1125 B | defines the typed layer-rule effect value and declares its match method | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Fetch provenance and outcomes

The six raw fetches below were each run under `timeout 30s sh -c` with `curl -fsSL`, followed by `sha256sum` and `wc -c`. The resulting bytes are staged under `.ufo/waves/round-24/fetch/w1/` with the listed names. Full absolute command and captured output are recorded here.

```sh
timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-1.bin'
9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-1.bin
6193 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-1.bin

timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-2.bin'
753fa6fa508ded8d927ca44cf13bfbca79b98e77ea0026fcbf5dc6e0c62c774f  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-2.bin
1017 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-2.bin

timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRule.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-3.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-3.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-3.bin'
f3e05eafeed061471fee843842db18127b905d2847faa738e763f4355f3c9bca  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-3.bin
3948 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-3.bin

timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-4.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-4.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-4.bin'
f62c45a977fa6dd5c4dcef245e791c56a33dc4a136ea2704696f6312f406b0fe  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-4.bin
3844 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-4.bin

timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleEffectContainer.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-5.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-5.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-5.bin'
d9b85eb9fee97d40b74dd54f3e417cd9e1e30e306667942d4cb451804498cb7d  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-5.bin
881 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-5.bin

timeout 30s sh -c 'curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRule.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-6.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-6.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-6.bin'
549a1a47e13afb9e2f8e1140e575996129da84c2bc8affbc4dced459beffea16  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-6.bin
1125 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLayerRule-6.bin
```

The candidate-row Python check used the frozen C1 `TOPIC_RE`, `collapse`, and `anchored` semantics from `c1/count.py` (lines 37, 46-56), plus `collapse(quote) in collapse(decoded_bytes)`. Result: all 12 draft rows met the quote-topic, <=25-word, exact-byte, >=8-word claim, and anchor checks. This is row-level preflight only, not a counted C1 result: `S?` IDs are provisional, no knowledge note or SOURCES rows were integrated, and the frozen counter was not run.

## Gates, touched surfaces, and limits

- **Source gate:** 12/12 draft rows pass the local row-level Python preflight described above.
- **C1 overall gate:** unrun; this seat does not claim `PASS_ROW` or `TARGET_MET`.
- **C2, no-harm guards, builds, tests, and host probes:** not run; outside this source-opener assignment.
- **Touched surfaces:** created this report and six staged raw fetch files under `.ufo/waves/round-24/fetch/w1/`. Read the registration, frozen C1 counter predicate, and the local scratch-clone directory listing to identify filenames. No clone, product source, corpus note, `SOURCES.md`, host configuration, or compositor state was modified. No tools or packages were installed.
- **Known limit:** the evidence is pinned code, not runtime observation. It establishes the layer-rule matching/application path and the emitted layer update event, not which rule a user-facing facility reports as the cause of an effect.

VERDICT: source-opener complete; integration and the counted C1 verdict remain pending.
