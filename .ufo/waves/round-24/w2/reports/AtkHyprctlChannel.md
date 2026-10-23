# AtkHyprctlChannel — attack on the note's "no window-rule or layer-rule listing verb"

**Attacked claim.** `corpus/knowledge/rule-attribution-r24.md:21` (table row *which rules exist*):
"there is no window-rule or layer-rule listing verb (sweep below)"; restated at `:64-65`
("the only rule-listing verb is `workspacerules`, `:2005`"). The note's negative sweep does not
enumerate the registry, so this seat enumerates it from the pinned source and tests the claim
against every registered command.

**Question tested.** Using the v0.56.2 clone, does any registered hyprctl command return
(a) window-rule or layer-rule identity, (b) a window/layer rule list, or (c) rule match results?

**Verdict: the claim holds.** 39 registered commands; none returns window-rule or layer-rule
identity, a window/layer rule list, or a window/layer match result. The strongest counterexample
(`systeminfo -c`, which returns raw config bytes containing rule lines) is a config dump, not a
rule listing, and the note's own route cell already names "config bytes only". Details below.

## Pins and provenance

- Clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`; `git log -1 --format=%H` →
  `efb50993780079460b0cbed1363e2166a2de1d9f`; `VERSION` → `0.56.2`.
- `sha256sum src/debug/HyprCtl.cpp` → `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`,
  `wc -c` → `97582` — equal to S158's recorded `sha256:798b7c6c…` and `97582 B`. The clone file is the
  source the note cites.
- Registration block: constructor `CHyprCtl::CHyprCtl()` opens `:2003`, registrations run
  `:2004-2043`, socket start `:2044`. S158's anchor `:2003-2044` covers it exactly.
- Anchor check on the note's own citations: `workspacerules` registration is `:2005` (correct);
  `getprop` registration is `:2032` (correct); `:1548-1553` is the generic `windowPropToString`
  lambda (`prop.valueOrDefault()`), while A11's opacity path is `:1565-1566` via `alphaToString`
  `:1493-1505` — the sweep anchor is the right handler but the less exact inner anchor (minor
  precision note, not a falsifier).

## Enumeration — all 39 registrations at v0.56.2

Command `registerCommand` call sites: 39 in the constructor, and the only other call site in the
tree is the plugin extension point `src/plugins/PluginAPI.cpp:422-428`
(`HyprlandAPI::registerHyprCtlCommand`) — no built-in plugin registers one. Split: 21 exact-match
(`exact = true`) and 18 prefix-matched (`exact = false`, including `reloadshaders`, which uses a
designated initializer); `eval` and `repl` share `evalRequest`, so 38 distinct handlers.

Rule class: **W** = workspace-rule list only; **E** = rule-*effect* state only; **C** = config/option
text; **L** = log text; **M** = mutator/protocol; **—** = no rule data.

| reg line | command | handler anchor | returns | class |
|---|---|---|---|---|
| 2004 | `workspaces` | `workspacesRequest :592` | workspace state | — |
| 2005 | `workspacerules` | `workspaceRulesRequest :613`, data `:522-548` | **workspace**-rule records (`workspaceString`, `enabled`, `monitor`, `defaultName`, gaps/border/rounding/shadow, `onCreatedEmpty`) | **W** |
| 2006 | `activeworkspace` | `:579` | active workspace | — |
| 2007 | `clients` | `clientsRequest :458` → `getWindowData :376-455`; tags `getTagsData :346-354`, field `:415` | window state, incl. `tags` (tag-keeper effect state) | E |
| 2008 | `kill` | `:1281` | kill mode / dispatcher | M |
| 2009 | `activewindow` | `:633` | window state, incl. `tags` | E |
| 2010 | `layers` | `layersRequest :647-723` | layer surfaces: `levels` → `namespace`, `pid`, alpha, geometry — no layer-rule field | — |
| 2011 | `version` | `:1089` | build info | — |
| 2012 | `devices` | `:748`; xkb `"rules"` field `:788`, `:799` | keyboards/mice; `rules` here is the **xkb** rule set (homonym, see below) | — |
| 2013 | `splash` | `:1287` | splash text | — |
| 2014 | `cursorpos` | `:1291` | cursor coordinates | — |
| 2015 | `binds` | `:1026` | bind list | — |
| 2016 | `globalshortcuts` | `:1000` | global shortcuts | — |
| 2017 | `systeminfo` | `:1097-1108`; `-c` appends `:1101-1105` | system info; with the `c` flag, raw **config file text** (legacy only) | **C** |
| 2018 | `animations` | `:927` | animation/bezier values | C |
| 2019 | `rollinglog` | `:987-998` | log ring text | **L** |
| 2020 | `configerrors` | `:725-745` | parse-error strings | C |
| 2021 | `locked` | `:1967` | lock boolean | — |
| 2022 | `descriptions` | `:1979` → `ConfigValues.cpp:149-157` | config options/descriptions/values | C |
| 2023 | `submap` | `:1983` | current submap | — |
| 2024 | `status` | `:1093` → `SystemInfo.cpp:29-64` | `configProvider`, `backend` | — |
| 2026 | `reloadshaders` | `:1991` | shader reload | M |
| 2027 | `monitors` | `:313` | monitor state | — |
| 2028 | `reload` | `:1260`; `updateAllRules` `:2146` | config reload | M |
| 2029 | `plugin` | `:1815-1884` | load/unload/list plugin metadata | M |
| 2030 | `notify` | `:1892` | notification | M |
| 2031 | `dismissnotify` | `:1947` | dismiss | M |
| 2032 | `getprop` | `:1463-1645`; renderers `:1493-1505`, `:1548-1553`; opacity `:1565-1566` | applied property value (`valueOrDefault`) | E |
| 2033 | `seterror` | `:1434` | error string | M |
| 2034 | `switchxkblayout` | `:1359` | xkb layout | M |
| 2035 | `output` | `:1760` | fake output create/destroy | M |
| 2036 | `dispatch` | `:1126` | run a dispatcher | M |
| 2037 | `keyword` | `:1160`; rule keywords `:1237-1246` | set keyword (window/layer rules reload) | M |
| 2038 | `setcursor` | `:1335` | cursor theme | M |
| 2039 | `getoption` | `:1647-1732` | one config option value | C |
| 2040 | `decorations` | `:1734-1758` | decoration names/priorities | — |
| 2041 | `[[BATCH]]` | `:1309` | runs any of the above, chunked | M |
| 2042 | `eval` | `:1110-1124` (Lua only `:1111-1112`) | Lua evaluation | M |
| 2043 | `repl` | `:1110-1124` | Lua REPL/eval | M |

### Counts

- **39** named registrations = 21 exact + 18 prefix; 38 distinct handlers.
- Commands returning **window-rule or layer-rule identity / list / match**: **0**.
- Commands returning **workspace-rule** records: **1** (`workspacerules`).
- Commands returning rule-**effect** state: **3** (`clients`, `activewindow` tags; `getprop` values).
- Commands returning config/option text: **5** (`systeminfo`, `animations`, `configerrors`,
  `descriptions`, `getoption`); log text: **1** (`rollinglog`).
- Mutators/protocol: **15**; no-rule-data: **14** (1+3+5+1+15+14 = 39).
- Source-level cross-check: `grep -ic rule src/debug/HyprCtl.cpp` → 71 hits; the only rule-engine
  reads are `getTagsData :346-354`, `getWorkspaceRuleData`/`workspaceRulesRequest :522-630`, the
  getprop applicator block `:1463-1645`, and the xkb homonym `:788-800`/`:888-892`; the only
  `ruleEngine()` call is the mutating `updateAllRules()` at `:2146`. No command calls
  `ruleEngine()->rules()`.

## Strongest counterexamples tested (and why none falsifies)

1. **`systeminfo -c` returns rule text.** The client's `-c/--config` flag
   (`hyprctl/src/main.cpp:420-421`) prefixes `c`; the server parses flags at `HyprCtl.cpp:2091-2092`
   (`sysInfoConfig = true`) and `systemInfoRequest` (`:1101-1105`) appends
   `Config::mgr()->getConfigString()`. In legacy mode that reads every tracked config path verbatim
   (`src/config/legacy/ConfigManager.cpp:687-704`), and `m_configPaths` includes `source`-expanded
   files (`:1836`), so `windowrule = …` and `layerrule = …` lines appear. This is the one hyprctl
   route that returns rule *declarations* over the socket — but it is a config-file dump, not a rule
   enumeration: it does not list the registered rule objects, excludes rules added by `keyword`, and
   in Lua mode it returns `"Not supported under lua"` (`src/config/lua/ConfigManager.cpp:1069-1071`).
   It cannot identify which rule matched. The note's route cell already says "config bytes only", so
   the substance is consistent; the negative sentence should name this path so "config bytes" is not
   read as "filesystem only".
2. **`eval`/`repl` (Lua).** Registered only as Lua evaluation and gated to the Lua config manager
   (`:1111-1112`). No Lua rule enumeration exists to call: `m_luaWindowRules`
   (`src/config/lua/ConfigManager.hpp:146`) is read only for name-keyed reuse
   (`LuaBindingsConfigRules.cpp:1190-1195`); the rule userdata exposes `set_enabled`/`is_enabled`
   only (`LuaWindowRule.cpp:58-70`); `LuaBindingsQuery.cpp:393` registers `get_windows` (window
   filters), not rules. On the host's hyprlang provider `eval` would refuse outright.
3. **`devices` "rules" homonym.** `"rules": "…"` at `:788`/`:799` is `m_currentRules.rules` — the
   **xkb** keyboard rules. A naive text sweep of hyprctl output for "rules" hits this first; it is
   not a window/layer rule list. Worth knowing, not a falsifier.
4. **`rollinglog` match text.** The ring returns log text (`:987-998`). The only rule-match line in
   the tree is A18's workspace-rule `"Rule workspace matched by {}, {} applied."`
   (`src/desktop/view/Window.cpp:2187`, DEBUG). Window/layer rule application logs no name (the
   note cites SrcRuleLogSweep: 15 log calls, none printing a rule name). So at most a **workspace**
   match line, exactly as the note qualifies — not window/layer.
5. **Client help/usage is not the registry.** `hyprctl/hyprctl.usage` and `hyprctl/src/Strings.hpp`
   list `instances` and `layouts`, and `setprop`; the server registers none of them. `instances` is
   handled client-side (`hyprctl/src/main.cpp:483-486`), `hyprpaper`/`hyprsunset` go to other
   sockets, `layouts` has no implementation anywhere in the tree (`grep -rn layouts src/ hyprctl/src/`
   → only help strings at `Strings.hpp:35`, `hyprctl.usage:80`). Enumerating the usage text instead
   of `HyprCtl.cpp:2004-2043` would produce both false positives and false negatives; the note's use
   of the registration line is the correct method.
6. **Live checks (read verbs from the allowed list only, 2026-10-23).**
   - `hyprctl -j workspacerules | jq length` → **0** on a host whose note-recorded host join says it
     declares 82 rule sites (77 inline + 3 block `windowrule`, 2 `layerrule`). The only rule-listing
     verb lists a different rule family and is empty — direct proof it does not list window/layer rules.
   - `hyprctl -j clients | jq '{n:length, has_rules:(.[0]|has("rules")), has_tags:(.[0]|has("tags")),
     has_rule:(.[0]|has("rule"))}'` → `{"n":4,"has_rules":false,"has_tags":true,"has_rule":false}`
     (keys only; no titles or tag values read). Window objects carry tag **effects**, no rule field.
   - `hyprctl getoption windowrule` → `no such option`; `hyprctl getoption layerrule` → `no such
     option`. Rules are not config options, so the option reader cannot reach them.
   - `hyprctl -j layers | jq 'keys, (.[keys[0]]|keys)'` → `["DP-1"]`, `["levels"]` — layer output is
     per-monitor levels of surfaces; no layer-rule key anywhere in the JSON.

## Verdict

`VERDICT: holds` — of 39 registered hyprctl commands at `efb50993` (HyprCtl.cpp
`sha256:798b7c6c…`, 97,582 B), zero returns window-rule or layer-rule identity, a window/layer rule
list, or window/layer match results. Exactly one returns workspace-rule records (`workspacerules`,
`:2005`), which the note already says. The nearest thing to a counterexample, `systeminfo -c`,
returns raw config files (legacy only), not a rule set, and cannot attribute an applied value to a
rule. The note's negative claim is correct; its sweep is thin (no enumeration, no mention of the
config-dump path) but its conclusion survives the full enumeration.

## Impacted axes and smallest safe correction

- **coverage**: C1's note is a coverage artifact and this sentence is part of the frontier answer;
  the claim is confirmed, so the axis is unharmed. The sentence is prose, not one of the counted
  A1-A26 rows — the C1 counter is unaffected either way.
- **depth**: the enumeration strengthens the claim; the recommendation below closes the one
  interpretive gap (`systeminfo -c`) and the inner-anchor imprecision (`:1548-1553` vs the opacity
  branch `:1565-1566`).
- **calibration**: unaffected — no capability table or self-assessment is involved.
- **Smallest safe correction** (one clause, prose only, no counted row touched): after "there is no
  window-rule or layer-rule listing verb (sweep below)" add "— `systeminfo -c` in legacy configs
  replays the raw config files, rule lines included, but returns config bytes, not a rule list, and
  is unsupported under Lua". Optionally retarget the sweep's getprop citation from `:1548-1553` to
  `:1463-1645` (or add `:1565-1566`) so the opacity row's own anchor matches its path.

## Bounds honoured

Read-only throughout: source reads in the scratch clone, `sha256sum`/`wc`/`grep`/`awk`; live reads
limited to the allowed verbs `version`-class (not needed), `clients`, `getprop`-class (not needed),
`getoption`, `layers`, `workspacerules` — all wrapped in `timeout 10`; only JSON key lists, lengths
and two option lookups were printed, never window titles, tag values or class values. No writes
outside this report; no git/jj write command; no packages installed or updated (`none` this seat);
no subagent dispatched.
