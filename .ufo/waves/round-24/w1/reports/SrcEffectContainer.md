# SrcEffectContainer source-opener report

## Scope and provenance

Opened the three Hyprland v0.56.2 pinned source files relevant to `src/desktop/rule/windowRule/WindowRuleEffectContainer.*` and the direct `src/desktop/rule/effect/` entry. The requested upstream pin is commit `efb50993780079460b0cbed1363e2166a2de1d9f`. The report contains observations from those fetched bytes, provisional C1 rows, and SOURCES row drafts; `S?` is deliberately provisional for integration.

## Exact fetch and receipt

Executed this command (successful fetches are evidenced by the subsequent checksums and byte counts):

```sh
timeout 60s bash -c 'mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-1.bin && curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-2.bin && curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/effect/EffectContainer.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-3.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-*.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-*.bin'
```

Observed output:

```text
21e0bd3e23dd50d1e3f278a66331ea4ba2bf602cf1e2a847968239c8e7542c46  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-1.bin
75a96873da1465d4a4c7dc151ae0224cb13a4b3865506fb67f2440cd3b1ab053  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-2.bin
1b995f1bdb45719b457c9015fff818b7a6a79201e41a74684b2b9f1e99d3bc00  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-3.bin
  80 2577 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-1.bin
  83 2783 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-2.bin
  82 2483 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-3.bin
 245 7843 total
```

## Findings

### Direct observations from the pinned bytes

- `WindowRuleEffectContainer.cpp:7-10` implements `Rule::windowEffects()` with a function-local `static SP<CWindowRuleEffectContainer>` initialized by `makeShared`, then returns that shared pointer.
- `WindowRuleEffectContainer.hpp:9-73` declares the `eWindowRuleEffect` enum. It gives `NONE` value zero, labels the `FLOAT` through `SCROLLING_WIDTH` group `// static`, labels the following `ROUNDING` through `CONFINE_POINTER` group `// dynamic`, then declares `WINDOW_RULE_EFFECT_LAST_STATIC`.
- `WindowRuleEffectContainer.cpp:12-72` contains an ordered `EFFECT_STRINGS` vector: `__internal_none`, lower-case string names for the enum effects, and `__internal_last_static`. The adjacent source has a comment about updating the strings when rules change and `static_assert(WINDOW_RULE_EFFECT_LAST_STATIC == 58)` at line 76. The container constructor at lines 78-80 passes that vector as the generic container's initial keys.
- `EffectContainer.hpp:19-23` selects `storageType` as the enum's underlying type when that type is at least two bytes, otherwise `uint16_t`; its constructor moves `defaultKeys` into `m_keys` and records `m_originalSize` from the initial vector size.
- `EffectContainer.hpp:28-35` implements registration by checking capacity, searching `m_keys` for an equal name and returning that existing index if found, otherwise appending the name and returning its index. At capacity it returns `0`.
- `EffectContainer.hpp:37-50` unregisters by replacing the selected key (or the first equal key found by name) with `DEFAULT_MISSING_KEY`; an out-of-range numeric ID is ignored. `:53-67` returns the missing-key string for an out-of-range numeric lookup, linearly searches names for the string-view overload and returns an optional index or `nullopt`. `:69-76` exposes the key vector by const reference and defines `isEffectDynamic(i)` as `i >= m_originalSize`.

### Interpretation and limits

The enum's `// dynamic` label is not itself the generic container's test for an effect registered dynamically. The generic method's own comment defines dynamic as added after construction, and its implementation tests the index against the original key-vector size. In this window-rule container, the constructor supplies the built-in string vector as initial keys, including strings corresponding by ordering to the enum's `// dynamic` group. Therefore the source supports distinguishing the enum's labeled group from the container's post-construction dynamic-registration classification. This conclusion uses the enum/string ordering and constructor data; the source does not document runtime callers or observed registrations.

These files establish key storage, lookup, registration, and the enum/string mapping only. They do not establish when an effect is applied, which rule caused any applied effect, whether a compositor/client currently has one, or host behavior; host behavior remains `[UNK]`. No negative existence claim is made.

## Provisional C1 claim rows

The following six excerpts were checked against their fetched source bytes using Python: whitespace-collapsed quote is a substring of whitespace-collapsed UTF-8 source, the quote has at most 25 words and matches the frozen topic regex, and each claim has at least eight words plus a v2 anchor. The first A2 candidate omitted the literal `//` between adjacent source comments and failed substring validation; it was corrected to the excerpt below. The final six checks all passed. All `S?` values are placeholders for L1 to replace with final source IDs.

### `WindowRuleEffectContainer.cpp` — provisional `S?`

| A1 | The `Rule::windowEffects` function returns a function-local shared window-rule effect container. | S? | "SP<CWindowRuleEffectContainer> Rule::windowEffects() { static SP<CWindowRuleEffectContainer> container = makeShared<CWindowRuleEffectContainer>(); return container; }" |
| A2 | A compile-time assertion checks the boundary named `WINDOW_RULE_EFFECT_LAST_STATIC` against 58. | S? | "the rules, we get reminded to update // the strings. static_assert(WINDOW_RULE_EFFECT_LAST_STATIC == 58);" |

### `WindowRuleEffectContainer.hpp` — provisional `S?`

| A3 | The enum assigns zero to `WINDOW_RULE_EFFECT_NONE` in the window-rule effect namespace. | S? | "namespace Desktop::Rule { enum eWindowRuleEffect : uint8_t { WINDOW_RULE_EFFECT_NONE = 0," |
| A4 | The enum places its static label immediately before `WINDOW_RULE_EFFECT_FLOAT` in source order. | S? | "namespace Desktop::Rule { enum eWindowRuleEffect : uint8_t { WINDOW_RULE_EFFECT_NONE = 0, // static WINDOW_RULE_EFFECT_FLOAT," |

### `EffectContainer.hpp` — provisional `S?`

| A5 | The `IEffectContainer` template statically requires its template parameter to be an enum. | S? | "namespace Desktop::Rule { template <typename T> class IEffectContainer { static_assert(std::is_enum_v<T>);" |
| A6 | The rule-namespaced container declares `DEFAULT_MISSING_KEY` as a `std::string` field. | S? | "namespace Desktop::Rule { template <typename T> class IEffectContainer { static_assert(std::is_enum_v<T>); protected: const std::string DEFAULT_MISSING_KEY =" |

## SOURCES row drafts

Each row has the requested eleven cells. No `SOURCES.md` row was written; identifiers remain provisional for integration.

| S? | WindowRuleEffectContainer.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp | code | A | window-rule container accessor and built-in effect strings | src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp:7-10,12-80 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:21e0bd3e23dd50d1e3f278a66331ea4ba2bf602cf1e2a847968239c8e7542c46, 2577 B | shared container initialization, ordered string keys, and static-boundary assertion | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | WindowRuleEffectContainer.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp | code | A | window-rule effect enum and labeled groups | src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp:8-83 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:75a96873da1465d4a4c7dc151ae0224cb13a4b3865506fb67f2440cd3b1ab053, 2783 B | enum values, static/dynamic labels, and sentinel | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | EffectContainer.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/effect/EffectContainer.hpp | code | A | generic effect-key storage and registration | src/desktop/rule/effect/EffectContainer.hpp:12-80 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:1b995f1bdb45719b457c9015fff818b7a6a79201e41a74684b2b9f1e99d3bc00, 2483 B | key indexing, lookup, unregister behavior, and post-construction dynamic test | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Gates, touched surfaces, and out of scope

- The pinned raw fetches, hashes, byte counts, line anchors, and final quote/anchor checks are evidenced above. The host clock date for these fetches is `2026-10-23`.
- Touched surfaces: this report and the three listed `.bin` receipt files under `.ufo/waves/round-24/fetch/w1/`. No source checkout or host state was changed. No tool was installed or updated.
- `corpus/knowledge/rule-attribution-r24.md`, `corpus/SOURCES.md`, and `corpus/README.md` were not edited. The counted C1 predicate, C2, builds, tests, host commands, and compositor behavior were not run or assessed by this source-opener seat.

**Verdict:** Three pinned source files were fetched and inspected; six provisional C1 rows and three SOURCES row drafts are recorded here, with final quote-substring, topic, word-count, and anchor checks passing. This is source-opener evidence only, not a C1 target verdict.

## Artifacts

- `.ufo/waves/round-24/w1/reports/SrcEffectContainer.md`
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-1.bin`
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-2.bin`
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcEffectContainer-3.bin`
