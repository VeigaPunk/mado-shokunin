# Mado round 24 wave 1 — SrcRuleBase

## Scope and outcome

Opened the three requested Hyprland files from the pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f` (tag `v0.56.2`) and saved the fetched bytes under `.ufo/waves/round-24/fetch/w1/`. The observations below are limited to those bytes. No host/compositor state was queried, and this report does not establish which rule caused any effect on the running host.

## Behavior observed in the pinned bytes

**Observation — rule identity.** `IRule` has a `name()` accessor and a protected constructor taking an optional name; `Rule.cpp` initializes `m_name` from that argument and returns `m_name` from `name()` (`Rule.hpp:63-67, 78-80`; `Rule.cpp:86-88, 142-144`). Its declared `eRuleType` distinguishes window from layer (`Rule.hpp:39-42`); this is a type discriminator, not a per-rule index. `IRule` also stores a property mask, enabled flag, match-engine map, and exec-rule data (`Rule.hpp:73-87`).

**Observation — effects held by the wrapper.** `CRuleWithEffects<TEffect, RULE_TYPE>` implements `type()` by returning `RULE_TYPE` (`RuleWithEffects.hpp:12-21`). A successful `addEffect` stores a `TEffect` with key, original raw result, and parsed value in `m_effects`, and adds the key to `m_effectSet`; a parse error is returned before either insertion (`:23-32`). `effects()` and `effectsSet()` expose const references to the vector and set (`:34-40`). `addParsedEffect` stores the supplied key/raw/value and adds its key to the set (`:47-52`). The declarations expose an effect record/container, not evidence of a runtime-applied effect or its cause.

**Interpretation, bounded to these three files.** The `rule idx` text in `Rule.cpp:93` is in the diagnostic for the `registerMatch(eRuleProperty p, ...)` property-engine lookup (`:90-95`); the logged value is converted from `eRuleProperty`. It is not evidence here of a distinct rule-instance index. I found no rule identity index or source-line member/accessor in the three opened files. This is not a claim about other Hyprland files or runtime behavior.

## Fetches and receipts

The three fetch commands all returned success with no stdout/stderr. Exact commands:

```text
timeout 45s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Rule.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-1.bin
timeout 45s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Rule.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-2.bin
timeout 45s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/RuleWithEffects.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-3.bin
```

Checksum and size command:

```text
timeout 10s sha256sum .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-1.bin .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-2.bin .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-3.bin && timeout 10s wc -c .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-1.bin .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-2.bin .ufo/waves/round-24/fetch/w1/MadoR24.SrcRuleBase-3.bin
```

Observed receipts:

| File | sha256 | Bytes | Relevant line anchors |
|---|---|---:|---|
| `MadoR24.SrcRuleBase-1.bin` | `sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e` | 6835 | 86-106, 128-168 |
| `MadoR24.SrcRuleBase-2.bin` | `sha256:2a6fd2d17a3ef7ebc7434be12022ff5b486a6b6039576cb4bdb1b68806178dec` | 3505 | 13-42, 47-88 |
| `MadoR24.SrcRuleBase-3.bin` | `sha256:0c9d2b181c7ce3d219dacc77e1b143593c6b6ac6ef63ea8611ee78850b22a55a` | 1711 | 11-57 |

## C1 row candidates

`S?` is provisional; the integration owner assigns source IDs and writes `corpus/SOURCES.md`. These six rows were checked locally against the fetched bytes: whitespace-collapsed quote occurs in the decoded file, quote has a C1 rule-topic token, claim has at least eight words, and the frozen claim-anchor check succeeds. The checker reported `quote_present=True`, `topic=True`, `anchored=True` for A1–A6; quote word counts were 6, 1, 4, 3, 14, and 23 respectively. These are row candidates, not counted `PASS_ROW`s: no SOURCES entries, note rows, or counted C1 run were produced here.

Rule.cpp (`:93`, `:132`):

| A1 | The diagnostic text says `RULE_ENGINES` does not contain a rule idx. | S? | "RULE_ENGINES does not contain rule idx" |
| A2 | The implementation delegates matching to an engine by calling `match` on its stored engine. | S? | "m_matchEngines[p]->match(s)" |

Rule.hpp (`:68-69`):

| A3 | The interface provides a string-based `matches` overload accepting an `eRuleProperty` selector. | S? | "matches(eRuleProperty, const std::string& s);" |
| A4 | A separate boolean `matches` overload also takes an `eRuleProperty` selector. | S? | "matches(eRuleProperty, bool b);" |

RuleWithEffects.hpp (`:11-16`):

| A5 | The `CRuleWithEffects` template derives from `IRule` within the `Desktop::Rule` namespace. | S? | "namespace Desktop::Rule { template <typename TEffect, eRuleType RULE_TYPE> class CRuleWithEffects : public IRule {" |
| A6 | The effect wrapper exposes `effectType` and `storageType` aliases tied to its `TEffect` parameter. | S? | "namespace Desktop::Rule { template <typename TEffect, eRuleType RULE_TYPE> class CRuleWithEffects : public IRule { public: using effectType = TEffect; using storageType = TEffect::storageType;" |

## Draft SOURCES rows

Each row has 11 cells; IDs remain `S?` for integration. No `|` occurs inside a cell.

| S? | Rule.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Rule.cpp | code | A | IRule name, property match-engine registration and delegation | src/desktop/rule/Rule.cpp:86-106,128-144 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e, 6835 B | Name accessor/initialization and match-engine behavior; diagnostic wording for missing property engine | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Rule.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Rule.hpp | code | A | IRule interface, discriminant and stored state | src/desktop/rule/Rule.hpp:13-88 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:2a6fd2d17a3ef7ebc7434be12022ff5b486a6b6039576cb4bdb1b68806178dec, 3505 B | Window/layer type, match APIs, name and property/match/exec storage | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | RuleWithEffects.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/RuleWithEffects.hpp | code | A | Effect-bearing rule template and effect storage/access | src/desktop/rule/RuleWithEffects.hpp:11-57 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:0c9d2b181c7ce3d219dacc77e1b143593c6b6ac6ef63ea8611ee78850b22a55a, 1711 B | Effect template aliases and rule type; parsing, vector of effect records, and distinct effect-key set | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Sweep, gates, and touched surfaces

For the negative identity-field finding, searched the three fetched files with `functions.grep` pattern `(?i)\b(index|line|source)\b|\bidx\b|m_[A-Za-z_]*(index|line|source|idx)`. It returned a match only at `Rule.cpp:93` (`rule idx`); the surrounding context was lines 92-95. In the source declarations, that `p` is an `eRuleProperty`, as noted above. This sweep is bounded to these three files.

- **C1 local row checks:** all six candidates passed the quote/topic/claim-anchor checks described above.
- **Round gates not run:** counted C1 counter, note/index target, C2 counter, no-harm guards, source census. No round-level target verdict is asserted.
- **Touched surfaces:** three fetched receipt files listed above and this report only. No product corpus file, `corpus/SOURCES.md`, counters, source clones, or host state was changed.
- **Out of scope:** C2 calibration; documenting actual applied-effect attribution on the host; broader Hyprland source sweep.

**Verdict:** 3/3 pinned source fetches succeeded and all 6 proposed claim rows passed row-local citation checks. Round-level C1 `TARGET_MET` and C2 are **NOT RUN**; no broader verdict is claimed.
