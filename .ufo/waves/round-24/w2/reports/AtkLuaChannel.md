# AtkLuaChannel — round 24 wave 2 attack: the note's Lua-channel negative claim

Seat: `MadoR24.AtkLuaChannel` (leaf critic). Artifact under attack is data; the round registration and this
assignment are the only instruction sources. I judged nothing beyond the one item assigned.

## What I attacked

`corpus/knowledge/rule-attribution-r24.md:66`, inside "Verdict NEGATIVE on every channel":

> Lua (`LuaWindowRule.cpp:58-70` exposes only `set_enabled`/`is_enabled`)

plus the two Lua-bearing table cells it summarises: `:22` (tag route read "in `hyprctl clients`") and `:23`
(enable/disable "named rule handle: Lua `set_enabled`/`is_enabled`"). Question put to me: **in the v0.56.2
clone, can a Lua config read back which rule applied to a window — through query APIs, window objects, or rule
handles?** A "yes" falsifies the note; the strongest available counterexample wins.

## Pin and identity (bytes are the pinned commit, not a local edit)

Clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`, `git rev-parse HEAD` =
`efb50993780079460b0cbed1363e2166a2de1d9f`, `git describe --tags` = `v0.56.2`. sha256 of every file I cite,
against the lane's own recorded values where a row exists:

| file | sha256 (local) | recorded where |
|---|---|---|
| `src/config/lua/bindings/LuaBindingsConfigRules.cpp` | `sha256:157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9` | S159 — exact match |
| `src/config/lua/objects/LuaWindowRule.cpp` | `sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a` | S160 — exact match |
| `src/config/lua/objects/LuaWindow.cpp` | `sha256:0755621ac698e5afa4bdb2e65e8475d3b7ee7a766e9389de05c797b3ae6d5ced` | w1 sweep table — exact match |
| `src/config/lua/bindings/LuaBindingsQuery.cpp` | `sha256:af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db` | w1 sweep table — exact match |
| `src/config/lua/ConfigManager.hpp` | `sha256:762cb890f89f32fe3d62ffbf65b25068d5aa56f7b8c377ad8887f5ad9c752968` | w1 sweep table — exact match |
| `src/config/lua/objects/LuaLayerRule.cpp` | `sha256:1d45e18a2da149edaeb3fddd6e275db14ce4028e9964d35bbdaf55b865d56e9a` | not previously recorded (new read) |
| `src/config/lua/objects/LuaWorkspaceRule.cpp` | `sha256:ba53f1f5ec0ac46a7bb5a132cfdb351b3afc77018cdc5ff16adfe4ba3059abfb` | not previously recorded (new read) |
| `src/config/lua/LuaEventHandler.cpp` | `sha256:1440283026b910ac91e1aa0652c07cbc0cb3fe7e517d6ce9a27a83c21b4f74e1` | not previously recorded (new read) |
| `src/helpers/TagKeeper.hpp` | `sha256:ea9559b297ceae73f517a05bb79b33ae62daa0a0de32d68604e15b12ad266e95` | not previously recorded (new read) |

The Lua provider is live at the pin, not docs-only dead code: `CMakeLists.txt:291` makes Lua 5.5 a **REQUIRED**
build dependency, and `CMakeLists.txt:658-663` installs `example/hyprland.lua` as the default Lua config; that
shipped file itself uses the handle (`example/hyprland.lua:317`, `:324`). So the channel I attacked is
reachable at `efb50993`.

## Method and findings, per surface

### F1 — rule handles: exactly two string keys, and neither is match state

`src/config/lua/objects/LuaWindowRule.cpp:58-70` (`windowRuleIndex`) resolves only `"set_enabled"` (`:62`) and
`"is_enabled"` (`:64`); every other key falls through to `lua_pushnil` (`:66-67`). The remaining metatable
members leak pointer identity only: `__eq` compares `lhs->lock() == rhs->lock()` (`:12-18`) and `__tostring`
prints `HL.WindowRule(%p)` or `(expired)` (`:20-30`). The handle stores a `WP<CWindowRule>`: no accessor returns
`name`, the match props, the effect list, or any record of which windows matched. `is_enabled` (`:45-56`) pushes
`rule->isEnabled()`, which the declaration path sets from the `enabled` field
(`LuaBindingsConfigRules.cpp:1183,1198`) — a declared flag, not an observation that the rule fired. Layer and
workspace handles are identical: `LuaLayerRule.cpp:58-70` and `LuaWorkspaceRule.cpp:62-65` expose the same two
keys. The note's `:58-70` anchor is exact (line 58 = function head, line 70 = closing brace) and the bare
filename is unambiguous — `find src -name LuaWindowRule.cpp` returns exactly
`src/config/lua/objects/LuaWindowRule.cpp`.

### F2 — window objects: 34 keys, one applicator-derived key, and it is `tags`

`src/config/lua/objects/LuaWindow.cpp` `windowIndex` (function `:59-248`) has 34 `key ==` branches (`:70-243`); none contains `rule`
or `prop` (`grep 'key == "' … | grep -ci 'rule\|prop'` → 0). The only branch that touches the rule applicator is
`tags` (`:136-143`), which returns `w->m_ruleApplicator->m_tagKeeper.getTags()`. `CTagKeeper` holds
`std::set<std::string> m_tags` (`src/helpers/TagKeeper.hpp:18`) — a bare string set with no rule reference, so
two rules that add the same tag are indistinguishable, exactly as the note's `:22` "does not show" column says.
Any unknown key returns nil (`LuaWindow.cpp:244-245`); there is no fallback that reflects C++ members. Other
effect reads on the object (`floating` `:98`, `size` `:86-90`, `pinned` `:117-118`) are values, not origins.

### F3 — query APIs: 19 getters, zero rule introspection

`LuaBindingsQuery.cpp:393-411` registers 19 `get_*` functions; the only rule-adjacent text in the file is the
`WindowRuleEffectContainer` include (`:12`) and the tag filter (`:63`). `grep -ci rule` on the file → 2, both
those lines. The `get_windows` filter accepts `monitor, workspace, floating, mapped, class, title, tag`
(`:84-95`) and the tag test is `m_tagKeeper.isTagged(*query.tag, true)` (`:63`) — a window set, not a rule.
`grep -rn 'get_rule\|get_rules\|list_rules\|rule_list\|listKeysForSpecialCategory' src/config/lua/` → **0**.

### F4 — events and the config getter: no rule payload either

The Lua event surface's only rule-named event is `window.update_rules`, and it pushes the window alone
(`LuaEventHandler.cpp:110`, name list `:279`); there is no rule id in the payload. `hl.get_config` reads
`m_configValues` only (`LuaBindingsConfigRules.cpp:1029-1042`); rules are not config values there.
`m_luaWindowRules` (`ConfigManager.hpp:146`) is the name→handle merge map; its only uses are
`ConfigManager.cpp:706` (clear) and `LuaBindingsConfigRules.cpp:1190-1195` (reuse/write) — no Lua binding reads
the map, so a config cannot enumerate rule names back out.

## Strongest counterexamples attempted, in order

1. **Named-handle re-fetch.** Calling `hl.window_rule({name = "x", …})` again returns the *existing* rule by
   name and merges effects (`LuaBindingsConfigRules.cpp:1189-1196`). This is the best candidate: a Lua config
   can address a rule by name. It still yields a control handle; nothing on the handle or engine reports
   whether that rule matched window `W`. Fails to restore attribution.
2. **Unique-tag instrumentation.** Assign each rule a unique `tag` effect and read `w.tags` /
   `hl.get_windows({tag = …})`. This works and is the note's own tag route; it is user-constructed and
   collision-blind (`std::set<std::string>`, F2), so it cannot answer "which rule set this opacity". The note
   already states this limit at `:22`.
3. **Config read-back.** `hl.get_config` (F4) holds config values, not rule declarations.
4. **Event subscription.** `window.update_rules` (F4) delivers the window only.

No candidate produced rule identity; the negative claim survived every angle I could construct from the pinned
tree.

## F6 — precision defect found (does not falsify the claim)

The note's `:66` sentence names only the rule handle for the Lua channel, and `:22` credits the tag read only to
`hyprctl clients`. In the pinned source a Lua config also reads the tag keeper directly —
`window.tags` (`LuaWindow.cpp:136-143`) and `hl.get_windows({tag = …})` (`LuaBindingsQuery.cpp:63`) — and reads
several effect values off the window object. None of those restores rule identity (F2), so the verdict is
unaffected; but an integrator or a Lua-era reader comparing `:66` with the w1 sweep would see a mismatch: the
sweep itself records the Lua window object and query filter (items 7-8 of `ScoutAttributionSweep.md:104-108`
and `:140-157`), while the note's Lua bullet condenses them away. This is a coverage/calibration precision
defect, not a wrong claim.

Smallest safe correction (two cells, no claim row, no counter, no predicate change):

Cell `:22` (keep the four-column row; replace the route text only):

```
| which rule fired on a window | **tag route**: give the rule a unique `tag` effect, then read `tags` in
`hyprctl clients` (A10, A22) or, under a Lua config, `window.tags` (`LuaWindow.cpp:136-143`) /
`hl.get_windows({tag = …})` (`LuaBindingsQuery.cpp:63`) | …unchanged… | …unchanged… |
```

Sentence `:66` (replace the parenthetical only):

```
Lua (`LuaWindowRule.cpp:58-70` rule handles expose only `set_enabled`/`is_enabled`; the Lua window object
and query API expose the tag keeper only, `LuaWindow.cpp:136-143`, `LuaBindingsQuery.cpp:63` — no rule
identity on either)
```

## F7 — upstream observation, not a note defect

`LuaWindow.cpp:140` dereferences `w->m_ruleApplicator` unguarded, while the query filter guards it
(`LuaBindingsQuery.cpp:63` `if (!w->m_ruleApplicator || …)`). The unguarded form matches A10's `clients` path
(`HyprCtl.cpp:346-354`), so it is an upstream asymmetry, not a misquote. No attribution impact; whoever owns
A10/A12-A14 should not treat the asymmetry as a contradiction.

## Verdict

No Lua path at v0.56.2 returns the identity of the rule behind an applied property. Handles carry control state
and pointer identity only; window objects and query APIs carry effect values and the provenance-free tag set;
events and `get_config` carry neither. The note's negative claim for the Lua channel is correct; the only defect
is that its Lua sentence under-reports the tag read surface (F6), which is a documentation correction, not a
falsification.

VERDICT: holds

## Impacted axes

- **coverage** (primary): the note's Lua cells `:22` and `:66` under-report the Lua read surface; fix is the
  two-cell edit above. The negative verdict itself needs no change.
- **calibration** (secondary): the condensation at `:66` does not match what the w1 sweep actually swept
  (sweep items 7-8), i.e. self-assessment drift of one sentence.
- **depth**: anchors verified exact (`:58-70`, `:136-143`, `:63`, `:62-65`/`:62-67`); no depth defect.

## Reproduce

Run in `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` (all read-only):

```sh
git rev-parse HEAD && git describe --tags                          # efb50993…, v0.56.2
grep -o 'key == "[a-z_]*"' src/config/lua/objects/LuaWindowRule.cpp   # set_enabled, is_enabled
grep -o 'key == "[a-z_]*"' src/config/lua/objects/LuaLayerRule.cpp    # set_enabled, is_enabled
grep -o 'key == "[a-z_]*"' src/config/lua/objects/LuaWorkspaceRule.cpp # set_enabled, is_enabled
grep -c 'key == "' src/config/lua/objects/LuaWindow.cpp               # 34
grep 'key == "' src/config/lua/objects/LuaWindow.cpp | grep -ci 'rule\|prop'   # 0
grep -rn 'm_ruleApplicator' src/config/lua/ --include=*.cpp --include=*.hpp    # 2: :63 filter, :140 tags
grep -c 'Internal::setFn(L, "get_' src/config/lua/bindings/LuaBindingsQuery.cpp # 19
grep -rn 'get_rule\|get_rules\|list_rules\|rule_list\|listKeysForSpecialCategory' src/config/lua/ | wc -l  # 0
grep -rn 'm_luaWindowRules' src/config/lua/                                   # clear + reuse/write only
grep -n 'dispatch("window.update_rules"' src/config/lua/LuaEventHandler.cpp    # :110, window only
sha256sum src/config/lua/objects/LuaWindowRule.cpp src/config/lua/bindings/LuaBindingsConfigRules.cpp
```

Cross-check the assertion here against a *named* rule round-trip: `hl.window_rule({name="x", enabled=false})`
then `is_enabled()` reads the declared flag (`LuaBindingsConfigRules.cpp:1183,1198`; `LuaWindowRule.cpp:45-56`);
nothing in the tree reads a rule's match outcome back out.

No install or update was performed (nothing needed updating). No host verb, compositor action, package
operation, or lane write occurred beyond this report; every command above ran read-only in the scratch clone
under `timeout`.

Report: .ufo/waves/round-24/w2/reports/AtkLuaChannel.md
