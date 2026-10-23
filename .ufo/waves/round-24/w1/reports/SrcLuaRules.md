# SrcLuaRules — round 24 wave 1 source-opener report

## Scope and findings

Opened only the three assigned Hyprland source files at commit `efb50993780079460b0cbed1363e2166a2de1d9f`. The binding registers `hl.window_rule` (line 1397) and accepts a Lua table. It initializes a `name`, reads the table's `name` field when `lua_isstring` succeeds (1177–1181), and reads `enabled` separately. On a non-empty name, `self->m_luaWindowRules` is the binding's name-keyed cache: a hit reuses that rule pointer; otherwise it constructs a `CWindowRule` with the name, stores it under that key, and registers it with the rule engine (1189–1198). It schedules a refresh, pushes the selected rule through `CLuaWindowRule::push`, then returns one Lua result (1271–1274).

The Lua userdata wrapper supports equality by comparing the two locked rule references (LuaWindowRule.cpp:12–17). Its index function exposes `set_enabled` and `is_enabled` (58–69); the setter changes a live rule's enabled state and calls `updateAllRules` (32–42), while the query returns nil if the weak reference has expired and otherwise returns a boolean (45–55). `push` stores a `WP<CWindowRule>` in userdata (76–80). The header declares the wrapper's setup and push API (LuaWindowRule.hpp:7–10).

**Inference, scoped to these bytes:** a script can retain a returned handle in a Lua variable, call its enabled methods, and compare handles for underlying rule identity. A script can also reach the same cached rule by calling `hl.window_rule` with the same non-empty name while that manager cache is in use; separate userdata wrapping the same rule compare equal according to the wrapper's equality function. The name is a key in this config-manager cache, not evidence here of a global or persistent identity across config-manager lifetimes.

**Not established:** these source bytes do not demonstrate host-side application of any particular rule effect, how a running compositor reports attribution, or behavior during config reload. Host behavior remains [UNK]. No negative claim about the absence of an attribution interface is made.

## Proposed claim rows

`S?` is provisional in this handoff; the integration owner assigns distinct final source IDs. Quotes below were copied from the captured source bytes and whitespace-collapsed for the table cell.

| A1 | A non-empty name reuses its cached `CWindowRule`; otherwise the binding creates one. | S? | "SP<Desktop::Rule::CWindowRule> rule; if (!name.empty() && self->m_luaWindowRules.contains(name)) { rule = self->m_luaWindowRules[name]; } else { rule = makeShared<Desktop::Rule::CWindowRule>(name); }" |
| A2 | For non-empty names, `m_luaWindowRules` stores each rule by name before engine registration. | S? | "if (!name.empty()) self->m_luaWindowRules[name] = rule; Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));" |
| A3 | The binding passes its selected `rule` to `CLuaWindowRule::push` and returns one result. | S? | "Objects::CLuaWindowRule::push(L, rule); return 1;" |
| A4 | Lua equality for two window-rule handles compares their locked rule objects via `lock`. | S? | "static int windowRuleEq(lua_State* L) { const auto* lhs = sc<WP<Desktop::Rule::CWindowRule>*>(luaL_checkudata(L, 1, MT)); const auto* rhs = sc<WP<Desktop::Rule::CWindowRule>*>(luaL_checkudata(L, 2, MT)); lua_pushboolean(L, lhs->lock() == rhs->lock()); return 1;" |
| A5 | The setter applies the supplied boolean to the rule and calls `updateAllRules`. | S? | "rule->setEnabled(lua_toboolean(L, 2)); Desktop::Rule::ruleEngine()->updateAllRules();" |
| A6 | For a live rule, this pushes its `isEnabled` flag as one Lua boolean result. | S? | "const auto rule = ref->lock(); if (!rule) { lua_pushnil(L); return 1; } lua_pushboolean(L, rule->isEnabled()); return 1;" |
| A7 | This header includes the desktop `WindowRule.hpp` declaration that its wrapper refers to. | S? | "#include \"../../../desktop/rule/windowRule/WindowRule.hpp\"" |
| A8 | The wrapper declares `push` with an `SP` parameter referring to a `CWindowRule`. | S? | "static void        push(lua_State* L, const SP<Desktop::Rule::CWindowRule>& rule);" |

Python checked each final proposed row against the captured decoded bytes using whitespace collapse, the frozen counter's topic-word pattern and anchor rule, the 25-word quote limit, and the 8-word claim minimum. Final output: A1–A8 each `quote=PASS`, `topic=PASS`, and `claim-anchor=PASS`; quote lengths were 16, 6, 4, 25, 3, 16, 2, and 7 whitespace-separated words respectively. Earlier drafts had `claim not anchored` for A2, A4, and A5; those claims were revised before this final pass. This is a local row check, not the frozen counted C1 counter.

## Draft SOURCES rows

These are the required 11-cell rows, with provisional `S?` IDs. Each row's source locator includes anchors in the fetched file, the pinned commit, `sha256:` digest, and byte count.

| S? | Lua config window-rule bindings — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsConfigRules.cpp | code | A | Lua window-rule table fields, name-keyed reuse and returned handle | src/config/lua/bindings/LuaBindingsConfigRules.cpp:1167-1198,1271-1274,1392-1399 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9, 61617 B | The binding reads the name field, caches named rules, registers new rules and returns a Lua wrapper | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua window-rule userdata implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.cpp | code | A | Lua window-rule handle equality and enabled methods | src/config/lua/objects/LuaWindowRule.cpp:12-80 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a, 2223 B | The userdata compares locked rule references, exposes enabled operations and wraps a weak rule reference | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua window-rule wrapper declaration — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.hpp | code | A | Lua wrapper declaration and core window-rule dependency | src/config/lua/objects/LuaWindowRule.hpp:4-11 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:f114a41cf6f98c5f5bae1227b00337e3c3a944ac6c611379dddf1078a9fd49f2, 350 B | The wrapper declares setup and push for a CWindowRule handle | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Provenance, commands, gates, and touched surfaces

The three ordinary raw fetches succeeded; `curl -fsSL` was silent and the command continued through hash and byte-count output. Exact command:

```sh
timeout 30s mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 60s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsConfigRules.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-1.bin && timeout 60s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-2.bin && timeout 60s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-3.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-{1,2,3}.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-{1,2,3}.bin
```

Observed output:

```text
157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9  .../MadoR24.SrcLuaRules-1.bin
02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a  .../MadoR24.SrcLuaRules-2.bin
f114a41cf6f98c5f5bae1227b00337e3c3a944ac6c611379dddf1078a9fd49f2  .../MadoR24.SrcLuaRules-3.bin
61617 .../MadoR24.SrcLuaRules-1.bin
2223 .../MadoR24.SrcLuaRules-2.bin
350 .../MadoR24.SrcLuaRules-3.bin
64190 total
```

- C1: source opening and the local 8-row quote/topic/anchor checks completed. No frozen `c1/count.py` counted-mode run was performed; C1 target and note indexing remain unmeasured here.
- C2: not in this source-opener assignment; no C2 counter run.
- No build, tests, host commands, package/tool installs, git/jj writes, or changes to product code, `SOURCES.md`, the C1 note, or corpus files.
- Only assigned source captures and this report were written. No sweep for global negative claims was needed; none is made.

## Verdict and artifacts

**Verdict:** Assigned Lua rule sources opened from the pinned commit; 8/8 proposed rows passed the local v2 quote/topic/anchor checks. This is not a frozen C1 `TARGET_MET` verdict.

Artifacts:
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-1.bin`
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-2.bin`
- `.ufo/waves/round-24/fetch/w1/MadoR24.SrcLuaRules-3.bin`
- `.ufo/waves/round-24/w1/reports/SrcLuaRules.md`
