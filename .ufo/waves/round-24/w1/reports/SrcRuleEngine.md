# C1 source opener — rule engine

## Result

Opened the pinned Hyprland `Engine.cpp` and `Engine.hpp` bytes. The pair documents rule registration into a retained vector and the engine's bulk refresh dispatch, but does not show an engine-side per-window record of which rule produced an effect. Four provisional claim rows are supplied below; `S?` is intentionally left for integration to replace. This is a scoped source report, not the complete C1 note or a counted C1 result.

## Source receipts and proposed SOURCES rows

| S? | Hyprland rule engine implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp | code | A | Rule registration, storage cleanup, and window/layer refresh dispatch | src/desktop/rule/Engine.cpp:14-16, 30-47, 54-55 @ efb50993780079460b0cbed1363e2166a2de1d9f; sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6; 1478 B | Registration appends to m_rules; updateAllRules cleans expired exec rules then sends RULE_PROP_ALL property-change notifications to eligible windows and layers; rules() returns m_rules | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland rule engine header — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.hpp | code | A | Rule engine API and private storage declaration | src/desktop/rule/Engine.hpp:11-20 @ efb50993780079460b0cbed1363e2166a2de1d9f; sha256:ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19; 707 B | Declares register/unregister/update/cleanup APIs, a const-vector rules() accessor, and the private m_rules vector | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Proposed claim rows

| A1 | The `registerRule` implementation appends each supplied rule to `m_rules`. | S? | "void CRuleEngine::registerRule(SP<IRule>&& rule) { m_rules.emplace_back(std::move(rule)); }" |
| A2 | The `rules` accessor returns `m_rules` by const reference rather than producing a copy. | S? | "const std::vector<SP<IRule>>& CRuleEngine::rules() { return m_rules; }" |
| A3 | The engine header declares `registerRule` to receive its rule argument by rvalue reference. | S? | "void registerRule(SP<IRule>&& rule);" |
| A4 | The header declares a `rules` accessor and keeps `m_rules` as the engine's private vector. | S? | "const std::vector<SP<IRule>>& rules(); private: std::vector<SP<IRule>> m_rules;" |

Each quote was checked against its fetched file bytes after whitespace collapse. The Python validation also checked the frozen C1 v2 topic-word expression, the 25-word ceiling, the eight-word claim minimum, and the counter's claim-anchor rule. All four rows returned `quote_substring=True`, `quote_words_le_25=True`, `topic_word=True`, `claim_words_ge_8=True`, and `anchor=True`; quote/claim word counts were A1 6/9, A2 7/13, A3 3/13, A4 6/14. This check validates only the proposed rows, not the C1 counter.

## Findings: observation and bounded inference

**Observed in the pinned bytes:** `registerRule` moves a rule into `m_rules` using `emplace_back`. The header declares that member as a private `std::vector<SP<IRule>>`; `rules()` returns a const reference to that vector. Thus the engine stores registrations in vector append order. These files do not establish that rule evaluation or effect application follows that same order.

`updateAllRules()` calls `cleanExecRules()` and then walks windows, skipping those not valid-mapped or hidden, and calls each remaining window's `m_ruleApplicator->propertiesChanged(RULE_PROP_ALL)`. It separately walks layers, skips non-valid-mapped entries, and calls the same property-change method. The engine therefore triggers a bulk refresh through each object's rule applicator; this pair does not show the rule matching/application implementation itself.

The header declares one private data member, `m_rules`, and neither engine file visibly declares an association/history structure between individual rules and windows. A case-insensitive sweep of both fetched files for the whole words `map`, `mapping`, `record`, `recorded`, `attribution`, or `applied` returned no matches. This supports only the bounded finding that this engine source pair does not expose a per-window applied-rule record; it is not a repo-wide claim that Hyprland has no other attribution mechanism.

**Not established:** which matching rule caused a particular applied effect, the detailed applicator evaluation order, what a running host reports, or whether another component exposes this information. Host behavior remains [UNK].

## Commands and outcomes

Fetched both sources with the required raw URLs and pinned commit. Exact commands and subsequent outputs:

```text
timeout 45s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-1.bin
1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-1.bin
1478 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-1.bin

timeout 45s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-2.bin
ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-2.bin
707 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleEngine-2.bin
```

Attribution-state sweep: `functions.grep` over both fetched files with case-insensitive pattern `\b(map|mapping|record|recorded|attribution|applied)\b` returned `No matches found`.

## Gates, touched surfaces, and limits

- Source-level quote/anchor validation passed for all four proposed rows.
- The frozen C1 counted counter was not run; these provisional rows alone do not meet the round target and no verdict is claimed for the integrated note.
- Only the two assigned fetched-byte artifacts and this report were written. `corpus/SOURCES.md`, `corpus/README.md`, and `corpus/knowledge/rule-attribution-r24.md` were not edited. No host-state commands, build, test, package installation, git, or jj operation was run.
- C2, other rule/applicator sources, host behavior, and final source-ID assignment remain outside this scoped opener.

**Verdict:** Source-opener scope complete; both pinned files were fetched and the four proposed claim rows passed local quote checks; the integrated C1 counted gate remains unrun.
