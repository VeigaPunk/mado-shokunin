# ScoutWikiEra — C1 era check: latest-git wiki (c66e8de2) against Hyprland v0.56.2 (efb50993)

Seat: scout (leaf). Role: resolve one unknown from source evidence. Question: which rule/tag/attribution
features does the wiki at commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` document that are absent from, or
different in, the source at Hyprland tag `v0.56.2` = commit `efb50993780079460b0cbed1363e2166a2de1d9f`
(the version the host runs)?

Observation and inference are separated below. Nothing here was executed against the live host, so host
behaviour stays **[UNK]**.

## Pins and era

| Item | Value |
| --- | --- |
| Wiki HEAD | `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`, committed 2026-10-22 14:52:44 +0200 |
| Wiki Lua rewrite | `cba1dbc` "major wiki restructure, minor fixes, rewording (#1616)", 2026-08-29 23:00:25 +0200 |
| Source tag | `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, commit date 2026-08-05 14:13:21 +0000 |
| Gap | wiki bytes are ~2.5 months newer than the pinned source; the Lua rule API the wiki documents already exists in v0.56.2 |

Local clones (read-only, never written):
`/fast/scratch/hyaku/mado-r24/src/hyprland-wiki` and `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`.
Every cited clone file was verified byte-identical (sha256) to a raw fetch at the pinned URL.

Base URLs for all receipts:
- W = `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af`
- S = `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f`

## What I did (exact commands, read-only)

```sh
git -C /fast/scratch/hyaku/mado-r24/src/hyprland-wiki rev-parse HEAD
git -C /fast/scratch/hyaku/mado-r24/src/hyprland-wiki log -3 --format='%H %ci %s'
git -C /fast/scratch/hyaku/mado-r24/src/hyprland-wiki log --format='%h %ci %s' -S'no_glow' -- content
git -C /fast/scratch/hyaku/mado-r24/src/hyprland-wiki log --format='%h %ci %s' -S'no_wobble' -- content
git -C /fast/scratch/hyaku/mado-r24/src/hyprland-wiki log --format='%h %ci %s' -S'no_xdg_drags' -- content
git -C /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 describe --tags
git -C /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 log -1 --format='%H %ci %s' v0.56.2
grep -rin 'wobble'      /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 | wc -l
grep -rin 'no_glow'     /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 | wc -l
grep -rin 'no_wobble'   /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 | wc -l
grep -rin 'no_xdg_drags' /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 | wc -l
grep -rin 'xdg.drag'    /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 | wc -l
grep -rn 'animationstyle' /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2/src | wc -l
grep -c 'RULE_PROP_NAMESPACE' /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2/src/desktop/rule/windowRule/WindowRule.cpp
```

Set comparisons (python3, run in `/fast/scratch/hyaku/mado-r24`): extracted the wiki effect-table names,
prop-table names, layer-effect names and workspace-field names from the markdown, extracted
`EFFECT_STRINGS` from the two effect containers, `MATCH_PROP_STRINGS` from `Rule.cpp`, and
`WORKSPACE_RULE_FIELDS` from `LuaBindingsConfigRules.cpp`, then printed the set differences (results in the
table and sweeps below). Also extracted `PROP == "..."` names from `Actions::setProp` and compared them to
the wiki's 42 dynamic effects.

Fetch receipts (one `curl -fsSL <raw URL> -o` per file, then `sha256sum` and `wc -c`):

| # | URL | sha256 | bytes | receipt |
| --- | --- | --- | --- | --- |
| 1 | W/content/configuring/core/rules/window-rules.md | sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95 | 16200 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-1.bin |
| 2 | W/content/configuring/core/rules/layer-rules.md | sha256:a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836 | 2129 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-2.bin |
| 3 | W/content/configuring/core/rules/workspace-rules.md | sha256:0d6fd4ab4477082d4681aacc7639b1f1c22fac4e3582dc049b19385660721074 | 2954 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-3.bin |
| 4 | W/content/configuring/core/advanced-configuration/using-hyprctl.md | sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0 | 8239 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-4.bin |
| 5 | W/content/configuring/core/dispatchers.md | sha256:80fccbf1ec5632d0979125d6df7f7a395391af85760952733bd2134c6dffe6ff | 12860 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-5.bin |
| 6 | S/src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp | sha256:21e0bd3e23dd50d1e3f278a66331ea4ba2bf602cf1e2a847968239c8e7542c46 | 2577 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-6.bin |
| 7 | S/src/desktop/rule/Rule.cpp | sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e | 6835 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-7.bin |
| 8 | S/src/desktop/rule/windowRule/WindowRule.cpp | sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78 | 19588 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-8.bin |
| 9 | S/src/desktop/rule/layerRule/LayerRule.cpp | sha256:f3e05eafeed061471fee843842db18127b905d2847faa738e763f4355f3c9bca | 3948 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-9.bin |
| 10 | S/src/config/shared/actions/ConfigActions.cpp | sha256:a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637 | 71407 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-10.bin |
| 11 | S/src/config/lua/bindings/LuaBindingsConfigRules.cpp | sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9 | 61617 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-11.bin |
| 12 | S/src/config/lua/objects/LuaWindowRule.cpp | sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a | 2223 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-12.bin |
| 13 | S/src/debug/HyprCtl.cpp | sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa | 97582 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-13.bin |
| 14 | S/src/helpers/TagKeeper.cpp | sha256:9c2507e2f1d8a5c5ca1afb28c66cb09540555ea182b5d7bfaacd66ef7b6ab9ef | 1353 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-14.bin |
| 15 | S/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b | 27092 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-15.bin |
| 16 | S/src/managers/KeybindManager.cpp | sha256:8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40 | 39334 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-16.bin |
| 17 | S/src/config/lua/bindings/LuaBindingsInternal.hpp | sha256:83630401a5b3d2cd99ec42705a7b70b0fdd73ddb3989c561a4316d15d72f0edd | 15901 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-17.bin |
| 18 | S/src/desktop/rule/matchEngine/TagMatchEngine.cpp | sha256:d30318effb1528cc7452f45e53a972fbea893958af99419fea9bcfc6b4e7fb23 | 297 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-18.bin |
| 19 | S/src/config/lua/bindings/LuaBindingsDispatchers.cpp | sha256:a109eeb982856e0fe2ac9d88c29115a09984511787e19a20e7b4804e14a9d4de | 53992 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-19.bin |
| 20 | S/src/desktop/view/Window.cpp | sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded | 124226 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-20.bin |
| 21 | S/src/desktop/rule/Engine.cpp | sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6 | 1478 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-21.bin |
| 22 | S/src/config/legacy/ConfigManager.cpp | sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b | 90963 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-22.bin |
| 23 | S/src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp | sha256:75a96873da1465d4a4c7dc151ae0224cb13a4b3865506fb67f2440cd3b1ab053 | 2783 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-23.bin |
| 24 | S/src/helpers/TagKeeper.hpp | sha256:ea9559b297ceae73f517a05bb79b33ae62daa0a0de32d68604e15b12ad266e95 | 427 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-24.bin |
| 25 | S/src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp | sha256:753fa6fa508ded8d927ca44cf13bfbca79b98e77ea0026fcbf5dc6e0c62c774f | 1017 | .ufo/waves/round-24/fetch/w1/MadoR24.ScoutWikiEra-25.bin |

Clone-vs-fetch identity: sha256 of each clone file at the same path equals the fetched sha256 (verified for all
25). No installs, no git/jj writes, no hyprctl calls, no host or config changes were made.

## Findings — wiki statement vs v0.56.2 source

Wiki paths are under `content/` of the wiki clone; source paths under `src/` of the v0.56.2 clone. Line numbers
are from the fetched bytes (identical to the clones).

| # | Wiki statement (path:line) | v0.56.2 source evidence (path:line) | Verdict |
| --- | --- | --- | --- |
| 1 | Documents dynamic effect `no_glow` as a bool that disables glow (window-rules.md:159) | `EFFECT_STRINGS` in WindowRuleEffectContainer.cpp:12-73 has no `no_glow`; enum in WindowRuleEffectContainer.hpp:12-73 has no entry; whole-tree case-insensitive sweep 0 hits (glow itself exists: 161 hits for decoration config and `CHyprInnerGlowDecoration`) | absent |
| 2 | Documents dynamic effect `no_wobble` (window-rules.md:165) | `EFFECT_STRINGS` lacks it; whole-tree sweep for `wobble` is 0 hits, so the concept is absent, not merely the rule | absent |
| 3 | Documents dynamic effect `no_xdg_drags` (window-rules.md:166) | `EFFECT_STRINGS` lacks it; tree sweeps for `no_xdg_drags` and `xdg.drag` are 0 hits; no `NO_XDG_DRAGS` enum member in WindowRuleEffectContainer.hpp | absent |
| 4 | "All dynamic effects can be set with `set_prop()`" (window-rules.md:182); dispatchers.md:216 repeats that props are any dynamic effects | `Actions::setProp` whitelist at ConfigActions.cpp:732-863 rejects `tag`, `confine_pointer` and `tonemap` (none of the three has a `PROP ==` branch) and answers "Invalid prop name" at :864; `border_color` exists only as `active_border_color`/`inactive_border_color`, which dispatchers.md:224-228 calls read-only aliases | different (wiki statement is overbroad at this pin) |
| 5 | "dynamic tags are cleared when the dispatcher is called" (window-rules.md:238) | `Actions::tag` (ConfigActions.cpp:633-643) calls `applyTag(tagStr)` with the default `dynamic = false` (TagKeeper.hpp:9) and then `propertiesChanged(RULE_PROP_TAG)`; `propertiesChanged` calls `resetProps` (WindowRuleApplicator.cpp:547-552), whose dynamic-tag erase (WindowRuleApplicator.cpp:66-73) removes only entries whose stored rule property mask intersects `RULE_PROP_TAG`. A dynamic tag created by a rule that matched only `class` is not removed; there is no unconditional clear | different |
| 6 | "Only named rules can be dynamically changed, enabled, or disabled" (window-rules.md:330) | `hlWindowRule` always pushes a handle after parsing (LuaBindingsConfigRules.cpp:1273), named or not; `set_enabled`/`is_enabled` are exposed for every handle (LuaWindowRule.cpp:32-67) and call `IRule::setEnabled` (Rule.cpp:112-118) | different (source allows enable/disable on unnamed handles) |
| 7 | The rule syntax block shows only `name?`, `match` and effects (window-rules.md:8-18) | The parser also reads a boolean `enabled` field (LuaBindingsConfigRules.cpp:1184-1190), and does the same for layer and workspace rules (:1294, :644); `name`, `enabled`, `match` are the three skipped keys in the effect loop (:1237) | different (source field undocumented) |
| 8 | getprop note: "If `animationstyle` is unset, `(unset)` is returned" (using-hyprctl.md:204) | getprop's accepted token is `animation` (HyprCtl.cpp:1555-1560, returns `(unset)` via `valueOr`); lowercase `animationstyle` occurs 0 times in src (the C++ member is camel-case `animationStyle`, 26 hits). `hyprctl getprop <win> animationstyle` falls through to "prop not found" (HyprCtl.cpp:1644) | different (property name) |
| 9 | Tag examples dispatch Lua strings, e.g. `hyprctl dispatch 'hl.dsp.window.tag({ tag = "+code" })'` (window-rules.md:243-248) | `dispatchRequest` only evaluates the argument as Lua when `Config::mgr()->type() == CONFIG_LUA` (HyprCtl.cpp:1126-1141); otherwise it looks up a legacy dispatcher name, where the tag operation is `tagwindow` (KeybindManager.cpp:82) | different (the example works only on a Lua config; on legacy config the spelling is different) |
| 10 | `namespace` is listed only as a layer-rule prop (layer-rules.md:28) | `MATCH_PROP_STRINGS` includes `namespace` (Rule.cpp:44); only `CLayerRule::matches` enforces it (LayerRule.cpp:107-110). `CWindowRule::matches` has no `RULE_PROP_NAMESPACE` case (0 hits; switch at WindowRule.cpp:376-476), so `hl.window_rule` accepts `namespace` in `match` but ignores it | same for layers; source quirk: the window-rule string is inert, the wiki's omission is accurate |
| 11 | Layer-rule effect table (10 effects, layer-rules.md:32-43) | `EFFECT_STRINGS` in LayerRuleEffectContainer.cpp:12-26 is exactly those 10 names; `static_assert ... == 11` with the none sentinel | same |
| 12 | Workspace-rule field table (16 fields incl. `layout_opts`, workspace-rules.md:25-42) | `WORKSPACE_RULE_FIELDS` (LuaBindingsConfigRules.cpp:196-228) has 15 of them; `layout_opts` is handled as a special-cased table at :670-705, then merged into the rule | same |
| 13 | "Dynamic tags have a suffix of `*`" and "Check window tags with `hyprctl clients`" (window-rules.md:231-233) | `CTagKeeper::applyTag` appends `*` when `dynamic` is true (TagKeeper.cpp:10-20); `isTagged` matches the bare name or name plus `*` when non-strict (TagKeeper.cpp:6), and `CTagMatchEngine` uses the default non-strict call (TagMatchEngine.cpp:11-12); `hyprctl clients` emits a `tags` array from `getTagsData` (HyprCtl.cpp:346-354, :415) | same |
| 14 | Window-rule Lua API `hl.window_rule({ name?, match = {...}, effect... })` (window-rules.md:6-18) | Registered as `window_rule` on the Lua config manager (LuaBindingsConfigRules.cpp:1397); parses name, enabled, match props from `MATCH_PROP_STRINGS` and effects from the effect container (:1160-1275). The same release also carries the legacy hyprlang `windowrule` v3 parser with `match:`-prefixed props (ConfigManager.cpp:590-655), which the current wiki page does not document | same API; source additionally keeps the legacy surface |

## Attribution surface (the C1 question)

Observation (bytes):
- The wiki contains no rule-attribution text. `grep -rni 'attribut' content` returns exactly 1 hit, and it is
  unrelated (the word "attribute" in a NixOS/Home Manager packaging sentence at
  content/nix/contributing-and-debugging.md:20).
- v0.56.2 exposes no "which rule applied this property" surface that I could find: `dispatchGetProp`
  (HyprCtl.cpp:1463-1644) accepts a fixed list of 42 property names and returns only the current value
  (or "prop not found" at :1644); the `clients` JSON exposes the applied `tags` array (HyprCtl.cpp:346-354,
  :415) but no rule identifier; the only matched-rule log line in `src` is a DEBUG message for workspace
  rules (Window.cpp:2187, "Rule workspace matched by ..."); `IRule::name()` is used only to unregister a rule
  (Engine.cpp:22).
- So at this pin the closest observable attribution markers are: applied values via `hyprctl getprop`, the
  dynamic-tag array via `hyprctl clients`, and debug-log lines. Tags distinguish static from dynamic by the
  trailing `*` stored in `CTagKeeper`, but nothing in the output names the producing rule.

Inference (labelled): the wiki's silence and the source's value-only getprop mean a note on "rule attribution"
can source what upstream *offers to tell* (values plus tags, no rule identity) but cannot source a claim that
Hyprland attributes an effect to a named rule at v0.56.2.

## Negative sweeps (command and output)

Run against `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`:

```
$ grep -rin 'wobble' . | wc -l
0
$ grep -rin 'no_glow' . | wc -l
0
$ grep -rin 'no_wobble' . | wc -l
0
$ grep -rin 'no_xdg_drags' . | wc -l
0
$ grep -rin 'xdg.drag' . | wc -l
0
$ grep -rn 'animationstyle' src | wc -l
0
$ grep -c 'RULE_PROP_NAMESPACE' src/desktop/rule/windowRule/WindowRule.cpp
0
$ grep -c 'RULE_PROP_NAMESPACE' src/desktop/rule/layerRule/LayerRule.cpp
1
$ grep -rn -- '\.name()\|->name()' src/desktop/rule | wc -l
1
$ grep -rni 'matched' src | grep -c 'Log::logger.*[Rr]ule'
1
$ grep -rin 'ruleName\|appliedRule\|matchedRule' src | wc -l
5
```

The single `IRule::name()` call site is Engine.cpp:22. The single rule-related "matched" log is
Window.cpp:2187; the other two `Log::logger` "matched" hits are a "mismatched format" message in Monitor.cpp
and an input-capture id in InputCapture.cpp. All 5 `ruleName`/`appliedRule` hits are XKB keyboard rule names
(IKeyboard.cpp/.hpp and InputManager.cpp:1286), unrelated to window/layer rules.

Set-difference output (programmatic, as described in "What I did"):

```
WIKI-ONLY effects (window rules): ['no_glow', 'no_wobble', 'no_xdg_drags']
SRC-ONLY effects: []
SRC-ONLY match props: ['namespace']
layer: wiki-only set() after removing 'namespace' (a prop row, not an effect) ; src-only {'__internal_none','__internal_last_static'}
workspace: wiki-only {'layout_opts'} ; src-only set()   # layout_opts is special-cased in the parser
wiki dynamic effects NOT settable via set_prop: ['border_color','confine_pointer','no_glow','no_wobble','no_xdg_drags','tag','tonemap']
```

Note on the last line: `border_color` is covered by the documented read-only `active_border_color` /
`inactive_border_color` aliases (dispatchers.md:224-228); `no_glow`, `no_wobble` and `no_xdg_drags` do not
exist in v0.56.2 at all, so the effective set_prop gap is `tag`, `confine_pointer`, `tonemap`.

## Inference and unresolved

- [INFERENCE] The wiki was rewritten to the Lua API at `cba1dbc` (2026-08-29), after the v0.56.2 cut, but the
  Lua `hl.window_rule`/`hl.layer_rule`/`hl.workspace_rule` bindings already ship in v0.56.2. The era gap is
  therefore partial: API shape matches; effect inventory and a few semantics do not.
- [INFERENCE] `no_xdg_drags` was documented 2026-07-24 (`c8c6b5d`) and `no_wobble` 2026-08-05 12:09Z
  (`4b4bad4`), both before the tag commit (14:13Z same day), yet neither exists in the tag tree. This is
  consistent with docs being merged ahead of the corresponding source PR, or the feature living outside this
  tree; the wiki bytes do not say which.
- [INFERENCE] The getprop token difference (`animationstyle` in the wiki vs `animation` in v0.56.2) may be a
  rename after the tag; at the tag the older name is the only accepted one.
- [UNK] Host behaviour: I did not call hyprctl, so whether the host config is Lua or legacy (which governs
  whether the wiki's `hyprctl dispatch 'hl.dsp...'` example works) is unknown. Host runs 0.56.2 per the
  assignment; that does not tell us its config manager type.
- [UNK] Latest-git Hyprland source was not opened (only the wiki at latest-git and the source at v0.56.2 were
  pinned), so these absences are established for v0.56.2 only, not for current master.

## What the bytes do NOT establish

- They do not establish that `no_glow`, `no_wobble` or `no_xdg_drags` are absent from current Hyprland master;
  only that they are absent from `efb5099` (v0.56.2).
- They do not establish runtime behaviour of any host: getprop's fall-through to "prop not found" is read from
  code, not executed.
- They do not establish that the wiki page is "wrong" in intent; a docs-ahead-of-release ordering is equally
  consistent with the observed bytes.

## Candidate claim rows for the C1 note (proposals only, not scored here)

Each quote was checked to be a whitespace-collapsed substring of the bytes in the named receipt, word count
≤25, and contains a rule-topic word. These are proposals for the note owner; I did not run
`.ufo/waves/round-24/c1/count.py` and I did not write `corpus/SOURCES.md` (draft rows are below).

| A1 | All dynamic effects can be set with the `set_prop` dispatcher, per the window-rules page. | S? | "All dynamic effects can be set with [`set_prop()`](../../dispatchers#set_prop)." |
| A2 | Only named rules can be dynamically changed or disabled according to the window-rules page. | S? | "Only named rules can be dynamically changed, enabled, or disabled." |
| A3 | To add a static tag, use the `hl.dsp.window.tag` dispatcher, the page says. | S? | "To add a static tag, use `hl.dsp.window.tag` dispatcher." |
| A4 | The getprop page says the property argument is any which can be set with `set_prop`. | S? | "Where `window` is as described [here](../../dispatchers#parameter-explanation), and `property` is any which can be set with [set_prop](../../dispatchers/#set_prop)." |

Provenance for A1-A3: receipt 1 (window-rules.md, sha256:9ecff146…, lines 182, 330, 235). Provenance for A4:
receipt 4 (using-hyprctl.md, sha256:95d8b842…, line 200). A1, A2/A4 claims are doc statements; note that A1's
content is contradicted by the v0.56.2 code for `tag`, `confine_pointer` and `tonemap` (finding 4), so it
should only be used as "the page says", never as a statement about behaviour.

## Draft SOURCES rows (proposals, `S?` placeholders)

One row per fetched file, in the 11-cell shape from the source-opener contract. These are drafts for the note
owner to merge; nothing was written to `corpus/SOURCES.md` and no id was assigned. Status is `mined`, date
`2026-10-23`, used-by the C1 note, recheck `on-release`.

| S? | Window Rules wiki page at c66e8de2 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md | docs | A | window-rule Lua syntax, props, static and dynamic effects, tags, named handles | content/configuring/core/rules/window-rules.md:1-343 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95, 16200 B | Lua window-rule surface as documented at wiki HEAD | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Layer rules wiki page at c66e8de2 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/layer-rules.md | docs | A | layer-rule props, effects and handle | content/configuring/core/rules/layer-rules.md:1-77 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836, 2129 B | layer-rule surface as documented at wiki HEAD | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Workspace Rules wiki page at c66e8de2 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/workspace-rules.md | docs | A | workspace-rule fields and examples | content/configuring/core/rules/workspace-rules.md:1-66 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:0d6fd4ab4477082d4681aacc7639b1f1c22fac4e3582dc049b19385660721074, 2954 B | workspace-rule field list as documented at wiki HEAD | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | using-hyprctl wiki page at c66e8de2 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md | docs | A | getprop section and property notes | content/configuring/core/advanced-configuration/using-hyprctl.md:192-206 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B | getprop argument and return-value wording at wiki HEAD | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Dispatchers wiki page at c66e8de2 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/dispatchers.md | docs | A | set_prop and clear_tags entries, read-only prop note | content/configuring/core/dispatchers.md:120,214-228 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:80fccbf1ec5632d0979125d6df7f7a395391af85760952733bd2134c6dffe6ff, 12860 B | set_prop scope and aliases at wiki HEAD | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | window-rule effect string table at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp | code | A | EFFECT_STRINGS names for static and dynamic effects | src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp:10-73 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:21e0bd3e23dd50d1e3f278a66331ea4ba2bf602cf1e2a847968239c8e7542c46, 2577 B | exact window-rule effect names at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | rule base and match-prop strings at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Rule.cpp | code | A | MATCH_PROP_STRINGS, match engines, IRule enable and name | src/desktop/rule/Rule.cpp:18-45,78-160 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e, 6835 B | match-prop strings and rule identity at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | window-rule matching at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.cpp | code | A | CWindowRule::matches switch | src/desktop/rule/windowRule/WindowRule.cpp:376-476 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78, 19588 B | which match props window rules actually enforce at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | layer-rule matching at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRule.cpp | code | A | namespace match case | src/desktop/rule/layerRule/LayerRule.cpp:107-110 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:f3e05eafeed061471fee843842db18127b905d2847faa738e763f4355f3c9bca, 3948 B | layer namespace enforcement at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | config actions at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp | code | A | Actions::tag body, Actions::setProp whitelist | src/config/shared/actions/ConfigActions.cpp:633-643,732-864 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637, 71407 B | tag dispatch semantics and set_prop accepted names at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua rule bindings at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsConfigRules.cpp | code | A | window, layer and workspace rule parsers, layout_opts, registration | src/config/lua/bindings/LuaBindingsConfigRules.cpp:196-228,644-705,1160-1400 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9, 61617 B | Lua rule API parsing at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua window-rule handle at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.cpp | code | A | set_enabled and is_enabled methods | src/config/lua/objects/LuaWindowRule.cpp:32-67 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a, 2223 B | rule handle methods at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | hyprctl implementation at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | code | A | dispatch, getprop, clients tags, layers | src/debug/HyprCtl.cpp:346-354,415,1126-1158,1463-1644 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa, 97582 B | getprop and clients tag output at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | tag keeper at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/TagKeeper.cpp | code | A | isTagged, applyTag dynamic suffix, removeDynamicTag | src/helpers/TagKeeper.cpp:3-52 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9c2507e2f1d8a5c5ca1afb28c66cb09540555ea182b5d7bfaacd66ef7b6ab9ef, 1353 B | static versus dynamic tag storage at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | window-rule applicator at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | code | A | dynamic tag reset, tag effect, propertiesChanged | src/desktop/rule/windowRule/WindowRuleApplicator.cpp:63-73,160-166,547-552 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b, 27092 B | when dynamic tags are removed and reapplied at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | legacy dispatcher registry at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp | code | A | dispatcher name list including tagwindow | src/managers/KeybindManager.cpp:78-90 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40, 39334 B | legacy tag dispatcher spelling at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua dynamic effect descriptors at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsInternal.hpp | code | A | confine_pointer and other dynamic effect descriptors | src/config/lua/bindings/LuaBindingsInternal.hpp:100-110 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:83630401a5b3d2cd99ec42705a7b70b0fdd73ddb3989c561a4316d15d72f0edd, 15901 B | dynamic effects exposed to set_prop at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | tag match engine at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/TagMatchEngine.cpp | code | A | CTagMatchEngine::match | src/desktop/rule/matchEngine/TagMatchEngine.cpp:7-13 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d30318effb1528cc7452f45e53a972fbea893958af99419fea9bcfc6b4e7fb23, 297 B | tag matching strictness at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Lua dispatchers at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsDispatchers.cpp | code | A | dsp_tagWindow, dsp_setProp and registrations | src/config/lua/bindings/LuaBindingsDispatchers.cpp:623-660,1000-1060 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:a109eeb982856e0fe2ac9d88c29115a09984511787e19a20e7b4804e14a9d4de, 53992 B | tag and set_prop Lua dispatchers at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | window implementation at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | code | A | workspace matched log, suppress-event parsing | src/desktop/view/Window.cpp:2187,2203-2218 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded, 124226 B | closest rule-attribution log and suppress-event names at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | rule engine at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp | code | A | registerRule, unregisterRule, updateAllRules | src/desktop/rule/Engine.cpp:14-40 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6, 1478 B | rule ordering and name use at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | legacy config manager at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | code | A | windowrule v3 special category and match props | src/config/legacy/ConfigManager.cpp:590-655,894-930 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B | legacy hyprlang rule parser at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | window-rule effect enum at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp | code | A | eWindowRuleEffect members | src/desktop/rule/windowRule/WindowRuleEffectContainer.hpp:12-73 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:75a96873da1465d4a4c7dc151ae0224cb13a4b3865506fb67f2440cd3b1ab053, 2783 B | effect enum inventory at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | tag keeper header at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/TagKeeper.hpp | code | A | isTagged, applyTag, removeDynamicTag signatures | src/helpers/TagKeeper.hpp:8-12 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:ea9559b297ceae73f517a05bb79b33ae62daa0a0de32d68604e15b12ad266e95, 427 B | applyTag dynamic default at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | layer-rule effect string table at v0.56.2 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp | code | A | EFFECT_STRINGS names | src/desktop/rule/layerRule/LayerRuleEffectContainer.cpp:12-29 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:753fa6fa508ded8d927ca44cf13bfbca79b98e77ea0026fcbf5dc6e0c62c774f, 1017 B | exact layer-rule effect names at the tag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Verdict

VERDICT: 9 of 14 checked surfaces differ at v0.56.2 — `no_glow`, `no_wobble` and `no_xdg_drags` are documented
but absent from the tag; `set_prop` scope, dynamic-tag clearing, named-only handles and Lua-gated `hyprctl
dispatch` are stated differently by the wiki than the v0.56.2 code; `animationstyle` is not an accepted
getprop token (source: `animation`); `enabled` is accepted by source but undocumented. Layer-rule effects,
workspace-rule fields, dynamic-tag suffix/clients visibility and the Lua rule API shape match. v0.56.2 exposes
no rule-origin attribution; host behaviour remains [UNK].
