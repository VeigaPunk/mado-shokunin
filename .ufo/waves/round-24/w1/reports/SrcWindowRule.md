# SrcWindowRule — round 24, wave 1 source opener

## Scope and outcome

Opened the pinned Hyprland v0.56.2 `WindowRule.cpp` and `WindowRule.hpp` source bytes to document window-rule effect fields and matching entry points. Both raw fetches succeeded. Seven proposed claim rows passed local quote checks against the fetched bytes: four from the implementation and three from the header. The `S?` source IDs are placeholders for integration; this seat did not allocate final `S###` IDs or edit the C1 knowledge note or `SOURCES.md`.

## Findings

**Observed in the pinned implementation:** `CWindowRule::matches` returns false if `canMatch()` is false, then iterates match engines by property. A tag property is matched against the window rule applicator's tag keeper. An xdg-tag property fails if the optional tag is absent or the engine does not match it. The exec-token branch breaks without matching when `allowEnvLookup` is false. Relevant anchors are `WindowRule.cpp:376-378,407-409,451-453,456-458`.

**Observed in the pinned header:** `WindowRuleEffectValue` is a variant of primitive, string, structured rule, and expression-vector alternatives. `SWindowRuleEffect` has a key, raw string, and value. `CWindowRule` derives from `CRuleWithEffects<SWindowRuleEffect, RULE_TYPE_WINDOW>` and declares `matches(PHLWINDOW w, bool allowEnvLookup = false)`. Relevant anchors are `WindowRule.hpp:34-46`.

These are observations of pinned source bytes, not live compositor behavior. They do not establish which rule produced any applied host effect, whether a particular rule matches at runtime, or layer-rule behavior. No negative existence claim is made and no repository/source sweep was run.

## Proposed C1 claim rows

### WindowRule.cpp

| A1 | The `CWindowRule::matches` entry point returns false when `canMatch()` rejects the candidate. | S? | "bool CWindowRule::matches(PHLWINDOW w, bool allowEnvLookup) { if (!canMatch()) return false;" |
| A2 | The `RULE_PROP_TAG` matcher tests the rule applicator tag keeper and rejects a failed engine match. | S? | "case RULE_PROP_TAG: if (!engine->match(w->m_ruleApplicator->m_tagKeeper)) return false; break;" |
| A3 | For `RULE_PROP_XDG_TAG`, an absent optional tag or failed engine match makes this rule return false. | S? | "case RULE_PROP_XDG_TAG: if (!w->xdgTag().has_value() || !engine->match(*w->xdgTag())) return false;" |
| A4 | When environment lookup is disabled, the `RULE_PROP_EXEC_TOKEN` branch skips its matcher instead of rejecting the window. | S? | "case RULE_PROP_EXEC_TOKEN: if (!allowEnvLookup) break;" |

### WindowRule.hpp

| A5 | The `WindowRuleEffectValue` variant includes primitive values, strings, structured rule values, and expression vectors. | S? | "using WindowRuleEffectValue = std::variant<std::monostate, bool, int64_t, float, std::string, std::vector<std::string>, SFullscreenStateRule, SOpacityRule, SBorderColorRule, Math::SExpressionVec2>;" |
| A6 | The `CWindowRule` type derives from `CRuleWithEffects` with window-rule effect and rule-type template arguments. | S? | "class CWindowRule : public CRuleWithEffects<SWindowRuleEffect, RULE_TYPE_WINDOW>" |
| A7 | Each `SWindowRuleEffect` stores an effect key, raw string, and `WindowRuleEffectValue` payload. | S? | "struct SWindowRuleEffect { using storageType = CWindowRuleEffectContainer::storageType; using valueType = WindowRuleEffectValue; CWindowRuleEffectContainer::storageType key = WINDOW_RULE_EFFECT_NONE; std::string raw; WindowRuleEffectValue value; };" |

## Proposed SOURCES rows

| S? | Hyprland v0.56.2 WindowRule.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.cpp | code | A | CWindowRule property matcher, including tag, xdg-tag, and exec-token branches | src/desktop/rule/windowRule/WindowRule.cpp:376-378,407-409,451-453,456-458 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78, 19588 B | CWindowRule::matches gate and property matching | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 WindowRule.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.hpp | code | A | Window-rule effect data layout, variant alternatives, and CWindowRule base | src/desktop/rule/windowRule/WindowRule.hpp:34-46 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:12cf28cc2aab0126a52ed61b7dcabd77ec6aebb643846883cd4d439e1603853a, 2468 B | Effect value alternatives, key/raw/value fields, and CWindowRule base type | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Provenance and commands

Fetched bytes are stored at the requested receipts. Each command exited successfully; the following are the exact fetch commands and the observed `sha256sum` / `wc -c` output.

```sh
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin
7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin
19588 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin

timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin
12cf28cc2aab0126a52ed61b7dcabd77ec6aebb643846883cd4d439e1603853a  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin
2468 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin
```

The exact quote-validation command was:

```sh
python3 -I -c 'import pathlib,re; root=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1"); cases=[("SrcWindowRule-1.bin","The `CWindowRule::matches` entry point returns false when `canMatch()` rejects the candidate.","bool CWindowRule::matches(PHLWINDOW w, bool allowEnvLookup) { if (!canMatch()) return false;"),("SrcWindowRule-1.bin","The `RULE_PROP_TAG` matcher tests the rule applicator tag keeper and rejects a failed engine match.","case RULE_PROP_TAG: if (!engine->match(w->m_ruleApplicator->m_tagKeeper)) return false; break;"),("SrcWindowRule-1.bin","For `RULE_PROP_XDG_TAG`, an absent optional tag or failed engine match makes this rule return false.","case RULE_PROP_XDG_TAG: if (!w->xdgTag().has_value() || !engine->match(*w->xdgTag())) return false;"),("SrcWindowRule-1.bin","When environment lookup is disabled, the `RULE_PROP_EXEC_TOKEN` branch skips its matcher instead of rejecting the window.","case RULE_PROP_EXEC_TOKEN: if (!allowEnvLookup) break;"),("SrcWindowRule-2.bin","The `WindowRuleEffectValue` variant includes primitive values, strings, structured rule values, and expression vectors.","using WindowRuleEffectValue = std::variant<std::monostate, bool, int64_t, float, std::string, std::vector<std::string>, SFullscreenStateRule, SOpacityRule, SBorderColorRule, Math::SExpressionVec2>;"),("SrcWindowRule-2.bin","The `CWindowRule` type derives from `CRuleWithEffects` with window-rule effect and rule-type template arguments.","class CWindowRule : public CRuleWithEffects<SWindowRuleEffect, RULE_TYPE_WINDOW>"),("SrcWindowRule-2.bin","Each `SWindowRuleEffect` stores an effect key, raw string, and `WindowRuleEffectValue` payload.","struct SWindowRuleEffect { using storageType = CWindowRuleEffectContainer::storageType; using valueType = WindowRuleEffectValue; CWindowRuleEffectContainer::storageType key = WINDOW_RULE_EFFECT_NONE; std::string raw; WindowRuleEffectValue value; };")]; norm=lambda s:" ".join(s.split()); texts={f:norm((root/f).read_bytes().decode("utf-8")) for f,c,q in cases}; topic=re.compile(r"rule|rules|windowrule|layerrule|getprop|prop|tag|match",re.I); checks=[(f,len(q.split()),len(c.split()),norm(q) in texts[f] and bool(topic.search(q)) and any(len(i)>=4 and i in norm(q) for i in re.findall(r"`([^`]+)`",c))) for f,c,q in cases]; assert all(nq<=25 and nc>=8 and ok for f,nq,nc,ok in checks),checks; [print(f"{f}: quote_words={nq}, claim_words={nc}, PASS") for f,nq,nc,ok in checks]; print(f"PASS: {len(checks)} quotes found whitespace-collapsed in fetched bytes; anchors, topic words, lengths pass")'
```

Observed validation output: `SrcWindowRule-1.bin` quote/claim word counts were 10/11, 7/15, 8/15, and 5/16; `SrcWindowRule-2.bin` counts were 13/13, 6/13, and 20/11. All seven quote-substring, rule-topic, quote-length, claim-length, and backticked-identifier anchor checks passed.

## Gates, surfaces, and limits

- **Passed here:** raw fetches for both pinned files; SHA-256 and byte counts recorded; all seven candidate quotes verified against fetched bytes after whitespace collapse and met the local topic/length/anchor checks.
- **Not run / not claimed:** C1 counted counter, C2 calibration counter, repository-wide SOURCES validation, tests, or any live-host check. No C1/C2 acceptance verdict is implied by this source opener.
- **Touched surfaces:** created this report and the two specified fetch receipts only. No source code, corpus note, SOURCES table, host settings, display/compositor state, services, packages, or git/jj state were changed. No tool was installed or updated.
- **Out of scope:** wiki documentation, layer rules, effect application/attribution beyond these two source files, and host runtime behavior.

**VERDICT: source opener complete; the seven claim rows and two SOURCES rows are proposals only, and C1/C2 gates remain unrun.**

## Artifact paths

- `.ufo/waves/round-24/w1/reports/SrcWindowRule.md`
- `.ufo/waves/round-24/fetch/w1/SrcWindowRule-1.bin`
- `.ufo/waves/round-24/fetch/w1/SrcWindowRule-2.bin`
