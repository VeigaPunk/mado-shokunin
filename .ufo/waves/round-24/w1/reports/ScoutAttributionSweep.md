# Scout — rule attribution sweep (round 24, wave 1)

Seat: `MadoR24.ScoutAttributionSweep`. Question put to me: does upstream v0.56.2 offer ANY
mechanism that maps an applied window property back to the rule that set it (rule name or index
stored per effect, hyprctl / Lua / IPC / logs / window object)?

**Verdict: NO.** In Hyprland v0.56.2 at `efb50993` no channel carries the identity of the rule
behind an applied effect. The only per-property provenance is a *priority class*
(`layout`, `workspace rule`, `window rule`, `set prop`) with no rule name and no rule index, and
it is not exposed by any read path. Rule *names* exist and are used solely as control handles
(unregister / enable-disable), never attached to effects. Negative per channel below, each with
the sweep command and its hit count.

Scope of the claim: only the bytes at the two pins, read-only. Host behaviour beyond
`hyprctl version` is `[UNK]`; I dispatched nothing and changed nothing.

## Pins, reads, receipts

- Code pin: Hyprland tag `v0.56.2` = `efb50993780079460b0cbed1363e2166a2de1d9f`
  (clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`, `git log -1` prints
  `efb50993780079460b0cbed1363e2166a2de1d9f (grafted, HEAD, tag: v0.56.2)`).
- Wiki pin: `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`
  (clone `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki`).
- Host check (read verb only): `timeout 10 hyprctl version` → `Hyprland 0.56.2 built from branch
  v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`, exit 0. The host binary is
  the pinned commit, so the pin is the running code, not a lookalike.
- Fetch receipts (all `curl -fsSL <raw URL> -o .ufo/waves/round-24/fetch/w1/ScoutAttributionSweep-<name>.bin`,
  all `cmp`-identical to the pinned clone file — 19 of 19 code files compared, 3 of 3 wiki files
  compared; `same:` printed for each):

| file | bytes | sha256 |
|---|---|---|
| content/configuring/core/rules/_index.md | 953 | `sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789` |
| content/configuring/core/rules/window-rules.md | 16200 | `sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95` |
| content/configuring/core/advanced-configuration/using-hyprctl.md | 8239 | `sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0` |
| src/desktop/types/OverridableVar.hpp | 5510 | `sha256:4d111c95b15133ca8f6f8a579fe36f9652a7298d031c45d84d83576670c06501` |
| src/desktop/rule/windowRule/WindowRuleApplicator.cpp | 27092 | `sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b` |
| src/desktop/rule/windowRule/WindowRuleApplicator.hpp | 9865 | `sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44` |
| src/desktop/rule/windowRule/WindowRule.hpp | 2468 | `sha256:12cf28cc2aab0126a52ed61b7dcabd77ec6aebb643846883cd4d439e1603853a` |
| src/desktop/rule/Rule.hpp | 3505 | `sha256:2a6fd2d17a3ef7ebc7434be12022ff5b486a6b6039576cb4bdb1b68806178dec` |
| src/desktop/rule/Rule.cpp | 6835 | `sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e` |
| src/desktop/rule/Engine.hpp | 707 | `sha256:ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19` |
| src/desktop/rule/Engine.cpp | 1478 | `sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6` |
| src/desktop/rule/layerRule/LayerRuleApplicator.cpp | 6193 | `sha256:9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba` |
| src/desktop/view/Window.hpp | 23988 | `sha256:1f60b8ff0bc6b5a48af5c03cb2cac1108db677efc70b4424b56ef6f1f2d1cc81` |
| src/event/EventBus.hpp | 7264 | `sha256:bfb8be17d84a0d8e7f10a0d61bcdc2b2e67378d139aaae8a484bebd96f62eede` |
| src/managers/EventManager.cpp | 6479 | `sha256:eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` |
| src/debug/HyprCtl.cpp | 97582 | `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` |
| src/config/legacy/ConfigManager.cpp | 90963 | `sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| src/config/lua/ConfigManager.hpp | 9805 | `sha256:762cb890f89f32fe3d62ffbf65b25068d5aa56f7b8c377ad8887f5ad9c752968` |
| src/config/lua/bindings/LuaBindingsConfigRules.cpp | 61617 | `sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9` |
| src/config/lua/bindings/LuaBindingsQuery.cpp | 12451 | `sha256:af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db` |
| src/config/lua/objects/LuaWindow.cpp | 9636 | `sha256:0755621ac698e5afa4bdb2e65e8475d3b7ee7a766e9389de05c797b3ae6d5ced` |
| src/config/lua/objects/LuaWindowRule.cpp | 2223 | `sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a` |

Cross-check of independence: siblings fetched the same URLs separately and got identical bytes —
`SrcWindowRuleApplicator-1.bin` = `fec33f9a…`, `WikiWindowRules-1.bin` = `9ecff146…`,
`WikiHyprctl-1.bin` = `95d8b842…`, `SrcHyprCtl-1.bin` = `798b7c6c…`,
`SrcLegacyConfig-1.bin` = `9db68cf4…`, `SrcLuaRules-1.bin` = `157c3e45…`,
`SrcRuleBase-1.bin` = `257687ef…`, `SrcRuleBase-2.bin` = `2a6fd2d1…`,
`SrcWindowRule-2.bin` = `12cf28cc…`, `SrcWindowView-1.bin` = `1f60b8ff…`.

## Channel verdicts

| Channel | Verdict | Strongest evidence |
|---|---|---|
| hyprctl verbs (`clients`, `getprop`, `getoption`, `layers`, `rollinglog`, `configerrors`) | **NEGATIVE** — value/state only | `HyprCtl.cpp:1548-1553` renders `prop.valueOrDefault()`; no verb lists window or layer rules; the only `*rules*` verb is `workspacerules` |
| Lua config API (`hl.*`, rule objects, window objects) | **NEGATIVE** — handle control only, no reverse lookup | `LuaWindowRule.cpp:58-70` exposes only `set_enabled` and `is_enabled`; `LuaBindingsQuery.cpp:392-411` registers 19 getters, none rule-bearing; `LuaWindow.cpp` has 34 index keys, none rule/prop provenance |
| socket2 IPC events | **NEGATIVE** — 35 event names, none rule-bearing | event inventory sweep below; `EventManager.cpp:163` `postEvent` only frames name and data supplied by callers; no call site supplies a rule id |
| logs (`rollinglog`, stdout, TRACE) | **NEGATIVE** — effect and property indices only | 15 `Log::logger->log` sites under `src/desktop/rule/`, 0 printing `name()` or `m_name` |
| window object / applicator state | **NEGATIVE, with one coarse positive** — priority class per property | `OverridableVar.hpp:153` `m_values[PRIORITY_END]`; `getPriority()` `:121-128`; no caller outside `Window.cpp:2419-2420` and no export |
| plugin/internal event bus | **NEGATIVE** — payload is the window, not the rule | `EventBus.hpp:91` `Event<PHLWINDOW> updateRules`, emitted `WindowRuleApplicator.cpp:589` |

### Candidates found (each with what it does and does not carry)

1. `IRule::name()` — declared `src/desktop/rule/Rule.hpp:63`, defined `Rule.cpp:142`, stored
   `Rule.hpp:78` (`std::string m_name = ""`). Set from the legacy special-category key
   (`src/config/legacy/ConfigManager.cpp:898` `makeShared<CWindowRule>(name)`) or the Lua table
   field `name` (`src/config/lua/bindings/LuaBindingsConfigRules.cpp:1177-1196`). Consumed only by
   `CRuleEngine::unregisterRule(name)` (`Engine.cpp:22`) and the Lua registry
   `m_luaWindowRules` (`src/config/lua/ConfigManager.hpp:146`). Legacy `windowrule = …` creates
   an **unnamed** rule (`legacy/ConfigManager.cpp:2019` `makeShared<CWindowRule>()`); exec rules
   are named `__exec_rule` (`WindowRule.cpp:481`). Carries: a control handle. Does not carry: any
   link to an applied effect.
2. `Types::COverridableVar<T>` — `src/desktop/types/OverridableVar.hpp`: `m_values` is
   `std::array<std::optional<T>, PRIORITY_END>` (`:153`) indexed by `eOverridePriority`
   (`:24-31`); `getPriority()` (`:121-128`) returns the winning class only. Every value-carrying
   effect write in `applyDynamicRule` passes `Types::PRIORITY_WINDOW_RULE` (e.g. `:118`, `:123`,
   `:128`, `:153-155`); tag effects append `(tag, propMask)` to `m_dynamicTags` (`:162`) instead,
   and static effects go to the `static_` struct. `set_prop` writes `PRIORITY_SET_PROP`
   (`src/config/shared/actions/ConfigActions.cpp:705-780`).
   Carries: which *layer* won. Does not carry: which rule in that layer.
3. `SCustomPropContainer{idx, propMask, effect}` — declared `WindowRuleApplicator.hpp:65-69`,
   filled `WindowRuleApplicator.cpp:97-108`. Carries: the effect's raw string and the match-prop
   mask (`rule->getPropertiesMask()`). Does not carry: the rule's name or an ordinal.
4. `m_dynamicTags` (`WindowRuleApplicator.hpp:183`) — `vector<pair<string, propMask>>`. Carries:
   tag value plus mask. Does not carry: producing rule.
5. `hyprctl clients` `tags` field — `HyprCtl.cpp:346-354` (`m_tagKeeper.getTags()`), emitted at
   `:433` and `:452`. Carries: the aggregate tag list, which may be the *effect* of a `tag` rule.
   Does not carry: which rule added the tag.
6. `hyprctl getprop` — handler `HyprCtl.cpp:1463`, value rendering `:1548-1553`, registration
   `:2032`. Carries: the effective value (or `(unset)`), reported by a wiki caveat list that names
   only defaults (`using-hyprctl.md:204-206`). Does not carry: match condition, rule name or order.
7. Lua rule handle — `LuaWindowRule.cpp:58-70` (`set_enabled`, `is_enabled` only),
   `tostring` prints the pointer (`:20-30`). Carries: on/off control. Does not carry: name read-back,
   effect list, or which windows it matched.
8. Lua window object — `LuaWindow.cpp` 34 `__index` keys (`:70-242`), `tags` at `:136`. Carries:
   derived state. Does not carry: rule identity or priority.
9. `Event::bus()->m_events.window.updateRules` — `EventBus.hpp:91`, emitted at
   `WindowRuleApplicator.cpp:589`. Carries: the window. Does not carry: the rule or the diff.
10. socket2 `custom` — `src/config/shared/actions/ConfigActions.cpp:1269` posts user-supplied
    `data`. Carries: whatever a caller writes; core never writes a rule id there. [INFERENCE] a
    plugin could invent such a channel, but that is not upstream attribution.
11. `hyprctl configerrors` — parse-time only: `addRuleFromConfigKey` returns the effect's own error
    text (`legacy/ConfigManager.cpp:906-912`), and the rule key is not prepended. Carries: a bad
    effect value. Does not carry: a rule identifier that survives to applied state.

## Sweeps (commands and outputs, verbatim)

All run in `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` (read-only).

1. hyprctl verb inventory — 40 `registerCommand` lines (2 are the member-function definitions at
   `:2054`, `:2058`), verbs: `workspaces workspacerules activeworkspace clients kill activewindow
   layers version devices splash cursorpos binds globalshortcuts systeminfo animations rollinglog
   configerrors locked descriptions submap status reloadshaders monitors reload plugin notify
   dismissnotify getprop seterror switchxkblayout output dispatch keyword setcursor getoption
   decorations [[BATCH]] eval repl`.
   ```
   $ grep -n 'registerCommand' src/debug/HyprCtl.cpp | grep -o '"[^"]*rule[^"]*"'
   "workspacerules"
   ```
   One rule-ish verb, and it is workspace-rule listing (`:572`), not window or layer rules.

2. What HyprCtl reads of rule state — `grep -c "rule" src/debug/HyprCtl.cpp` → **53**; of those
   **43** are `m_ruleApplicator->…` value reads, 4 are xkb keyboard "rules" (`:788`, `:799`,
   `:888`, `:891` — two pairs), 2 are workspace-rule (`:572`, `:2005`), 2 are keyword-string checks
   (`:1237`, `:1240`), 1 include (`:60`), 1 `updateAllRules()` on config reload (`:2146`).
   43 + 10 = 53; the 10 non-applicator lines are exactly these; none exposes rule identity.

3. Lua query surface —
   ```
   $ grep -c 'Internal::setFn(L, "get_' src/config/lua/bindings/LuaBindingsQuery.cpp
   19
   $ grep -ci 'rule' src/config/lua/bindings/LuaBindingsQuery.cpp
   2
   ```
   The 2 hits are the effect-container include (`:12`) and `w->m_ruleApplicator->m_tagKeeper`
   in the tag filter (`:63`). There is no `get_rules` / `list_rules`
   (`grep -rn 'get_rule\|get_rules\|list_rules' src/config/lua/` → 0 hits).

4. Lua window object —
   ```
   $ grep -c 'key == "' src/config/lua/objects/LuaWindow.cpp
   34
   $ grep 'key == "' src/config/lua/objects/LuaWindow.cpp | grep -ci 'rule\|prop'
   0
   ```

5. Lua rule object — `grep -o 'key == "[a-z_]*"' src/config/lua/objects/LuaWindowRule.cpp` →
   `set_enabled`, `is_enabled`. Nothing else.

6. socket2 event inventory —
   ```
   $ grep -rhoE 'SHyprIPCEvent[[:space:]]*\{[[:space:]]*(\.event[[:space:]]*=[[:space:]]*)?"[a-zA-Z0-9]+"' src --include=*.cpp | sed -E 's/.*"([a-zA-Z0-9]+)"/\1/' | sort -u | wc -l
   35
   $ …same… | grep -ci rule
   0
   ```
   Names: `activelayout activespecial activespecialv2 activewindow activewindowv2 closelayer
   closewindow configreloaded custom focusedmon focusedmonv2 fullscreen lockgroups minimized
   monitoradded monitoraddedv2 monitorremoved monitorremovedv2 moveintogroup moveoutofgroup
   movewindow movewindowv2 moveworkspace moveworkspacev2 openlayer openwindow pin screencast
   screencastv2 submap urgent windowtitle windowtitlev2 workspace workspacev2`.
   `grep -rn 'postEvent(' src --include=*.cpp | wc -l` → 77 call sites, none passing a rule id.

7. Logs —
   ```
   $ grep -rc 'Log::logger->log' src/desktop/rule/*.cpp src/desktop/rule/*/*.cpp | awk -F: '{s+=$2} END {print s}'
   15
   $ grep -rn 'Log::logger->log' src/desktop/rule/ | grep -c 'name()\|m_name\|ruleIdx\|ruleName'
   0
   ```
   The 15 lines print effect/property enum numbers, expression parse failures, and the
   `RULE_ENGINES does not contain rule idx {}` bug line (`Rule.cpp:93`).

8. Name linkage —
   ```
   $ grep -rn 'name()' src/desktop/rule/ | wc -l
   5
   ```
   `Engine.cpp:22` (unregister), `Rule.cpp:142` (definition), `Rule.hpp:63` (declaration), and two
   `DEFINE_PROP` accessors (`WindowRuleApplicator.hpp:80`, `LayerRuleApplicator.hpp:42`) that are
   property getters, not rule names. `rule->name()` appears nowhere: no applicator ever reads it.

9. Priority exposure —
   ```
   $ grep -rn 'getPriority()' src/ | wc -l
   3
   ```
   Definition `OverridableVar.hpp:121` plus `Window.cpp:2419` and `:2420` (one internal
   expression). No hyprctl or Lua path calls it.

10. Window object —
    ```
    $ grep -c 'Rule\|rule' src/desktop/view/Window.hpp
    9
    ```
    Storage is `UP<Desktop::Rule::CWindowRuleApplicator> m_ruleApplicator` (`:236`); the other hits
    are the include (`:22`), a `CWorkspaceRule` forward declaration (`:34`), the unrelated
    `eGroupRules` enum/flag (`:50`, `:59`, `:273`), and two noclosefor comments/fields
    (`:283`, `:383`).

11. Rule enumeration is applicator-local —
    ```
    $ grep -rn 'ruleEngine()->rules()' src/ | wc -l
    4
    ```
    `WindowRuleApplicator.cpp:492`, `:527`, `:554`, `LayerRuleApplicator.cpp:137`. No reader
    outside the applicators, hence no API surface to answer "which rule".

12. git-dir cleanliness: no git or jj write command was run in the lane, the fleet repo, or the
    clones; only `git log -1` in the clone (read).

## Observation, inference, unknown

**Observed (bytes say):**
- Effects are stored as values keyed only by priority class (`OverridableVar.hpp:153`);
  every value-carrying dynamic effect write passes `PRIORITY_WINDOW_RULE`, tag effects store
  `(tag, propMask)` (`WindowRuleApplicator.cpp:162`), and static effects land in `static_`.
- The named-rule facility is documented as a *control* facility: `window-rules.md:330`
  "Only named rules can be dynamically changed, enabled, or disabled." The handle object offers
  `set_enabled` / `is_enabled` and nothing else.
- Rule names are optional in both config eras (`_index.md:8` "Rules can be either named or
  anonymous."; legacy keyword rules are unnamed at `legacy/ConfigManager.cpp:2019`).
- `getprop` renders `prop.valueOrDefault()` (`HyprCtl.cpp:1548-1553`). The wiki describes the verb
  as "Gets a property value of a window" and lists only default-value caveats
  (`using-hyprctl.md:192-206`).
- 35 socket2 event names, 0 rule-bearing; 19 Lua getters, 0 rule-bearing; 15 rule-subsystem log
  statements, 0 printing a rule identity.

**Inference (mine, not in the bytes):**
- Because `m_values` is an array of `optional<T>` indexed by class, two `window rule`s that set the
  same property in sequence are indistinguishable after the fact: the later write overwrites the
  same slot. `[INFERENCE]`
- The documented ordering (`_index.md:14`: named rules first, then anonymous, each top-to-bottom;
  `window-rules.md:318`: "the _last_ match takes precedence") plus overwrite-in-place means the
  observable value can only be attributed by *replaying* the rule set by hand. `[INFERENCE]`
- A plugin could build its own attribution registry through the public `m_otherProps` comment
  ("Plugins may read this", `WindowRuleApplicator.hpp:66`) and the `updateRules` bus event, but it
  would have to record matches itself; upstream gives it no rule id either. `[INFERENCE]`

**Unknown (`[UNK]`) — not established by these bytes:**
- Any host behaviour: whether the running 0.56.2 emits anything extra under
  `debug:*` log flags, or whether an installed plugin adds attribution. No host rule read was run
  beyond `hyprctl version`.
- Whether a later Hyprland version adds attribution. The claim is bounded to `efb50993`.
- Whether a third-party tool parses `hyprctl clients` plus the config to attribute externally; that
  is reconstruction, not an upstream mechanism.
- Layer rules were swept the same way (same `OverridableVar` model, `LayerRuleApplicator.cpp:49-120`),
  but I did not run a separate field-by-field Lua sweep for `LuaLayerSurface`; the conclusion for
  layers rests on the shared applicator/priority model plus the 0-hit socket2/Lua-query sweeps.

## Proposed claim rows for `corpus/knowledge/rule-attribution-r24.md`

Row form is the frozen one; `S?` is a placeholder for the SOURCES id. Every quote was checked
mechanically against the fetched bytes with the counter's own rules (whitespace-collapse,
`<=25` words, `TOPIC_RE`, `claim>=8` words, anchor clause, `ROW_RE` parse) — all six pass:

| row | source file | quote words | claim words | topic | substring | anchored | parses |
|---|---|---|---|---|---|---|---|
| A1 | rules/_index.md:8 | 7 | 16 | yes | yes | yes | yes |
| A2 | rules/_index.md:14 | 17 | 23 | yes | yes | yes | yes |
| A3 | rules/window-rules.md:330 | 10 | 16 | yes | yes | yes | yes |
| A4 | rules/window-rules.md:315 | 14 | 13 | yes | yes | yes | yes |
| A5 | advanced-configuration/using-hyprctl.md:197 | 4 | 17 | yes | yes | yes | yes |
| A6 | src/desktop/rule/windowRule/WindowRuleApplicator.cpp:101 | 3 | 9 | yes | yes | yes | yes |

The six rows, ready to paste (each `|` cell is pipe-free):

| A1 | Rule objects may be anonymous in the documented syntax: `Rules` can be either named or anonymous. | S? | "Rules can be either named or anonymous." |
| A2 | Ordering is not source order alone: rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones. | S? | "Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones." |
| A3 | Runtime toggling requires a name, since only named rules can be dynamically changed, enabled, or disabled. | S? | "Only named rules can be dynamically changed, enabled, or disabled." |
| A4 | Effects labelled dynamic are re-evaluated whenever the matching property of the window changes. | S? | "Effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes." |
| A5 | The documented per-window property read verb is `getprop`, taking a window selector and a single property name. | S? | "hyprctl getprop <window> <property>" |
| A6 | The per-effect container's propMask field is filled from `rule->getPropertiesMask()`. | S? | ".propMask = rule->getPropertiesMask()," |

Note on A6: the quote is a code line; its word count and topic-token compliance come from the
literal `rule->getPropertiesMask()` token, which `TOPIC_RE` matches on `rule` (word boundary at
`-`). A reviewer re-reading the claim against `WindowRuleApplicator.cpp:97-108` will see the
`.propMask` field inside `SCustomPropContainer` — the claim states exactly that and no more.

## Proposed SOURCES rows (11 cells, `S?` placeholder)

| S? | Hyprland wiki — Rules index (props/effects split, named vs anonymous, ordering) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md | docs | A | rule object naming and evaluation order in the v0.56-era Lua rule syntax, and which fields the `hyprctl clients` output reports | content/configuring/core/rules/_index.md:8,14 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789, 953 B | rules may be named or anonymous, and evaluation runs top to bottom with named rules first; `hyprctl clients` reports fullscreen fields, not rule provenance | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland wiki — Window Rules (syntax, effects, dynamic re-evaluation, named-rule control) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md | docs | A | documented window-rule effects and what a rule name is for (enable/disable), including dynamic re-evaluation and last-match precedence | content/configuring/core/rules/window-rules.md:315,318,330 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95, 16200 B | dynamic effects re-evaluate on property change; last match wins; only named rules can be toggled — the name is a control handle, not an attribution tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland wiki — Using hyprctl (getprop section) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md | docs | A | the documented window-property read path: verb spelling, argument shape, and the only caveats the page lists | content/configuring/core/advanced-configuration/using-hyprctl.md:192-206 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B | getprop takes a window and one property and returns a value; the documented caveats are defaults and unset markers, no attribution field | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 — window rule applicator (effect application path) — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | code | A | the apply path: per-effect dispatch, the fields retained per effect, and the absence of a rule identifier in that record | src/desktop/rule/windowRule/WindowRuleApplicator.cpp:81-108,492-509 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b, 27092 B | effects are pushed per rule and stored by key and prop mask; the applicator never reads `rule->name()` | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 — overridable variable storage (priority classes) — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/types/OverridableVar.hpp | code | A | how a resolved property value is stored per window, and what provenance remains after the winning write | src/desktop/types/OverridableVar.hpp:24-31,121-128,152-157 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:4d111c95b15133ca8f6f8a579fe36f9652a7298d031c45d84d83576670c06501, 5510 B | a value is an array of optionals indexed by override priority (layout, workspace rule, window rule, set prop); getPriority returns the class only, so no rule identity survives | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

One row per file, as required. `OverridableVar.hpp` carries no PASS_ROW-able quote by construction:
its only rule-topic tokens are inside identifiers such as `PRIORITY_WINDOW_RULE`, which
`TOPIC_RE`'s word boundary rejects. The note must cite it in prose (or drop it); the six claim
rows above already reach `>=6` from 4 distinct sources (`_index.md`, `window-rules.md`,
`using-hyprctl.md`, `WindowRuleApplicator.cpp`), so the target does not depend on it.

Also required by the counter but outside my seat: a coverage-map line in `corpus/README.md` matching
`^\| \`knowledge/rule-attribution-r24.md\``; without it `TARGET_MET` cannot be reached even at six
passing rows.

## What this does NOT establish

- Not a host measurement: I ran no `hyprctl getprop`/`clients` against the live compositor and did
  not read the operator's rule files. Whether the host's rules collide on the same property is
  `[UNK]` here.
- Not a claim about other versions; `efb50993` only.
- Not a claim that attribution is impossible — only that upstream v0.56.2 stores and exposes no
  such mapping. A downstream tool can reconstruct it by replaying config; upstream does not offer it.
- The negative channel verdicts are bounded by the sweeps printed above (source tree at the pin,
  case-insensitive `rule` token search); a mechanism spelled without that token (for example under
  a different name) would evade the sweep. I widened with `name()`, `getPriority()`,
  `ruleEngine()->rules()` and full socket2/Lua inventories precisely to reduce that risk.
