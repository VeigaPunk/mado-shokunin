# AtkEraWiki — attack on the era caveat for A19–A26 (S165–S168)

Seat: leaf critic, read-only. No lane edits except this file; no lane/fleet git or jj; no dispatch,
keyword or reload; no `~/.config` or service changes; no installs (none needed). Host reads used:
`hyprctl version`, `hyprctl workspacerules`, `hyprctl -j workspacerules`, `hyprctl configerrors`,
`hyprctl --help` only.

Attacked item: the era caveat at `corpus/knowledge/rule-attribution-r24.md:89-90` ("the wiki commit
is latest-git documentation and shows Lua `hl.window_rule()` syntax (A19); the host runs 0.56.2 with
`configProvider: hyprlang` … Wiki rows are `[INF-docs]` for this host") and the ordering sentence it
feeds at `:27` ("named rules first, then anonymous, top to bottom, last match wins (A21, A25, A26)").
Question: for each of A19–A26, does the v0.56.2 source behave as the pinned wiki (c66e8de) says?

Method: re-opened every quoted row in its committed fetch bytes; re-read the pinned v0.56.2 tree
(`/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`, HEAD `efb50993780079460b0cbed1363e2166a2de1d9f`
= `v0.56.2`); read the wiki clone; probed the live host with the allowed read verbs; and fetched the
same four Hyprland files from `hyprwm/Hyprland` `main` to separate *era drift* from *doc-vs-code
mismatch* (local copies under `/fast/scratch/hyaku/mado-r24/w2/era/`, fetched 2026-10-23).

## 0. Era baseline — the caveat's framing is wrong in one axis

- **[OBS] Era gap is real.** The wiki pin `c66e8de` is the wiki clone's HEAD, dated
  `2026-10-22 14:52:44 +0200`; v0.56.2 was built `Wed Aug 5 14:13:21 2026` (`hyprctl version`).
  So the docs are ~2½ months newer than the pinned source, as the note says.
- **[SRC] But v0.56.2 is not Lua-less.** `src/config/ConfigManager.cpp:16-57` selects
  `Lua::CConfigManager` whenever the main config path ends `.lua` (`:33`, `:45`) and
  `Legacy::CConfigManager` otherwise. `hl.window_rule` and `hl.layer_rule` are registered in that
  build (`src/config/lua/bindings/LuaBindingsConfigRules.cpp:1397-1398`). So A19/A22/A23 are
  *verifiable against v0.56.2 source*, not merely docs-ahead-of-code. The operative split is
  **provider** (the host is hyprlang), not era.
- **[OBS] Latest `main` has dropped the provider A26 describes.** Fetched today:
  `src/config/legacy/ConfigManager.cpp` → HTTP 404; `src/config/ConfigManager.cpp` on main
  instantiates `Lua::CConfigManager` on both branches; `src/desktop/rule/Engine.cpp` is
  byte-for-byte the v0.56.2 shape (append-only `m_rules`); the main applicator's `readStaticRules`
  is unchanged. So the 2026-10-22 wiki sentence has no implementation on main, and on v0.56.2 it
  holds only for the hyprlang provider (see A26).

## 1. Row-by-row verdicts

| row | wiki statement (pinned bytes) | v0.56.2 behavior | verdict |
|---|---|---|---|
| A19 | `hl.window_rule({ name?, match, effect })` syntax block (S165:9-15) | `name` optional, `enabled` optional, `match` table, effects as **top-level** keys; a literal `effect` key is rejected | holds (schematic) |
| A20 | dynamic effects re-evaluated on matching-property change (S165:316) | `propertiesChanged` re-applies dynamic effects for rules whose own mask intersects; call sites exist for all window props | holds |
| A21 | top-to-bottom, last match takes precedence (S165:318) | true on a full static read (map/reload); **false after a partial dynamic re-eval** (later matching rule is skipped) | **partial** |
| A22 | dynamic tags `*`; check with `hyprctl clients` (S165:230-233) | `CTagKeeper::applyTag(..., true)` appends `*`; `clients` prints `tags`; dispatcher exists | holds |
| A23 | layer rules return `set_enabled()`/`is_enabled()` handle (S166:69-70) | `HL.LayerRule` metatable exposes both; `hl.layer_rule` returns the handle | holds |
| A24 | `workspacerules` gets the list of defined workspace rules (S167:245) | verb exists and lists workspace rules, but empty set → `unknown request`; quoted line is **not** v0.56.2 help text | **partial** |
| A25 | _All_ props must match (S168:16) | `CWindowRule::matches` returns false on every failing prop; layer rules same for namespace | holds |
| A26 | named rules evaluated first, then anonymous (S168:14) | hyprlang: yes (hoisted by `reloadRules`); Lua: **no** (registered at call order, no hoist) | **partial** |

### A19 — holds, but the syntax block is not copyable

**[SRC]** `LuaBindingsConfigRules.cpp:1167-1273`: `name` is read only if it is a string and may be
empty (`:1178-1182`), `enabled` is optional (`:1184-1188`), `match` is a table mapped through
`matchPropFromString` (`:1199-1215`), and every other string key is looked up as an effect name
(`:1229-1245`). Anything that is not an effect errors `unknown field` (`:1246`). **[OBS]** `"effect"`
is not in the effect registry (`src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp:11-72`),
so `effect = some_effect_value` copied literally from S165:9-15 yields
`hl.window_rule: unknown field 'effect'` in v0.56.2. The block is schematic — `name?` is not valid
Lua — and the page's own examples (S165:253-302) use flat effect keys, which v0.56.2 accepts
exactly (`no_blur`, `tag`, `opacity`, `border_color`, …). The row's documentary claim is true; the
note should not let a reader copy the metavariable form.

### A20 — holds

**[SRC]** `CWindowRuleApplicator::propertiesChanged` (`WindowRuleApplicator.cpp:547-590`) resets
only effects whose stored mask intersects and then re-applies `applyDynamicRule` (`:81-…`) for rules
whose own mask intersects. Trigger sites cover the window props the wiki names: title/class
(`view/Window.cpp:1485`), focus (`state/FocusState.cpp:131,189,201`), floating
(`layout/target/WindowTarget.cpp:294`), workspace (`state/GlobalWindowController.cpp:71`,
`desktop/Workspace.cpp:567`), group (`view/Group.cpp:314,322,333`), fullscreen
(`managers/fullscreen/FullscreenController.cpp:465,488`, `.../handler/FullscreenHandler.cpp:168`),
pin (`config/shared/actions/ConfigActions.cpp:259`), tag (`:639,652`), modal
(`protocols/XDGDialog.cpp:38`), xdg_tag (`protocols/XDGTag.cpp:22`), and `RULE_PROP_ALL` on map
(`view/Window.cpp:2497`). The layer path carries a FIXME (`layerRule/LayerRuleApplicator.cpp:133`)
but the quoted sentence says "window", so it is not touched by A20.

### A21 — partial: precedence is not invariant under partial re-evaluation

**[SRC] Full read holds.** `readStaticRules` (`WindowRuleApplicator.cpp:483-536`) walks
`ruleEngine()->rules()` in registration order and applies static then dynamic effects per rule
(`:497-508`); each dynamic effect writes at `PRIORITY_WINDOW_RULE` (`opacity` case `:151-159`), and
`COverridableVar` stores one value per priority (`types/OverridableVar.hpp:72-74`), so the last
matching rule's value wins at map/reload. `Engine::registerRule` only appends
(`desktop/rule/Engine.cpp:14-16`); no sort/partition exists (`Rule.cpp:20,49` sorts descriptor
tables only).

**[SRC] Counterexample, using the page's own worked example** (S165:320-326: float→0.5 rule first,
class=kitty→0.8 rule second; prose says a floating kitty gets 0.5):

1. A kitty window **maps while floating**: `CWindow::mapWindow` calls `readStaticRules`
   (`view/Window.cpp:2052,2277`); both rules match and are applied in order, so alpha = **0.8** —
   the prose's 0.5 is wrong for this path.
2. A kitty **becomes floating later**: `propertiesChanged(RULE_PROP_FLOATING)`
   (`WindowTarget.cpp:294`) re-applies only rules whose *own* mask intersects `:563`; the float
   rule is re-applied (0.5) and the later kitty rule is **skipped** because its mask is `class`.
   Result 0.5 — the prose's number, but reached by skipping the last match, i.e. by violating the
   sentence.
3. Worse, the reset mask is the **last writer's** mask (`m_alpha.second = rule->getPropertiesMask()`,
   `:156-158`), so the effect is not cleared for a prop the last rule never matched.

So "the _last_ match takes precedence" is exact only on a full static read; after a partial
property re-eval the winner is the last *re-applied* matching rule. The note's operational
sentence at `:27` inherits this and needs the qualifier.

### A22 — holds

**[SRC]** `helpers/TagKeeper.cpp:10-16`: `applyTag(tag, dynamic)` appends `*` when dynamic and not
already suffixed; `:3-8` matches `tag` against `tag*` for non-strict matches; `:50-52` removes
`s + "*"`. **`[SRC]`** `debug/HyprCtl.cpp:347` reads `m_tagKeeper.getTags()` and `:415` emits
`"tags": [{}]` in the clients JSON. The wiki's surrounding dispatcher text is also v0.56.2-real:
`hl.dsp.window.tag` is bound at `LuaBindingsDispatchers.cpp:1002,1378`.

### A23 — holds

**[SRC]** `config/lua/objects/LuaLayerRule.cpp:37-66`: `layerRuleSetEnabled` calls
`rule->setEnabled` + `updateAllRules` (`:41`), `layerRuleIsEnabled` pushes the flag (`:51-58`), and
the index exposes `set_enabled` / `is_enabled` (`:62-64`). `hl.layer_rule` returns the handle
(`LuaBindingsConfigRules.cpp:1277-1390`, `CLuaLayerRule::push` at `:1388`). This is a Lua-provider
fact, not an era fact: the code is in the v0.56.2 tree.

### A24 — partial: route exists, but its plain-text form is an error string on this host

**[SRC]** `debug/HyprCtl.cpp:2005` registers `workspacerules`; `:613-633` iterates
`Config::workspaceRuleMgr()->getAllWorkspaceRules()`. **[OBS] live, this host (0.56.2, pin):**

```
$ hyprctl workspacerules
unknown request
$ hyprctl -j workspacerules
[]
```

Cause: `getReply` returns `"unknown request"` whenever the handler's result string is empty
(`HyprCtl.cpp:2124`), and the normal-format handler emits nothing for zero rules; the JSON form
still emits `[]`. So the verb is present, the host simply defines **zero workspace rules**, and the
plain-text form is indistinguishable from an unknown command. The note's route row (`:21`) presents
`hyprctl workspacerules` as a usable v0.56.2 probe without this caveat.

**[OBS] The quoted line is not v0.56.2 text.** The pinned wiki says
`workspacerules       - gets the list of defined workspace rules` (S167:245). v0.56.2's own help
string is `workspacerules      → Lists all workspace rules` (`hyprctl/src/Strings.hpp:62`), and the
live client's `--help` prints exactly that v0.56.2 line. A24 is documentary-accurate for the wiki
pin, but it must not be read as a v0.56.2 string.

### A25 — holds

**[SRC]** `WindowRule.cpp:376-…`: `CWindowRule::matches` iterates every match engine and returns
`false` on the first mismatch; `IRule::canMatch` (`Rule.cpp:124-126`) refuses an empty match set and
disabled rules; `CLayerRule::matches` (`layerRule/LayerRule.cpp:96-…`) is the same shape for
`namespace`. The one soft spot — `RULE_PROP_EXEC_TOKEN` skips its check when
`allowEnvLookup == false` (`WindowRule.cpp`, exec-token case) — is unreachable for non-exec rules,
and exec rules are excluded from `propertiesChanged` (`WindowRuleApplicator.cpp:554-558`) while
`readStaticRules` passes `true`. No counterexample found.

### A26 — partial: true for the host's hyprlang provider, false for the provider the wiki documents

**[SRC] hyprlang (host) — holds.** `CConfigManager::reloadRules`
(`src/config/legacy/ConfigManager.cpp:946-966`) clears the engine, registers named `windowrule`
blocks first (`:950`; category keyed on `name`, `:591`), then named `layerrule` blocks (`:955`),
then all inline keyword rules in file order (`:961-963`). Inline keyword rules are constructed
without a name (`handleWindowrule` `makeShared<CWindowRule>()` `:2016-2019`;
`handleLayerrule` `:2056-2060`) and runtime `hyprctl keyword` anonymous rules are appended last
(`:2050-2052`). Named-before-anonymous is therefore a property of this provider's registration
order, not of the engine.

**[SRC] Lua (the syntax the page documents) — fails.** `hl.window_rule` registers the rule at the
moment the script calls it (`LuaBindingsConfigRules.cpp:1190-1196`; layer equivalent
`:1300-1306`); the Lua config manager only clears the engine and the name maps
(`config/lua/ConfigManager.cpp:702-707`) and executes the script (`:746`) — there is no reorder
pass, and the engine appends (`Engine.cpp:14-16`). Therefore a script that writes an anonymous rule
before a named one evaluates **anonymous first**, the opposite of S168:14. Named-first is not a
property the wiki's own `hl.window_rule` path implements in v0.56.2.

**[OBS] main confirms the direction of travel:** the hyprlang provider is gone from main
(`src/config/legacy/ConfigManager.cpp` 404; main `ConfigManager.cpp` is Lua-only), while main's
`hl.window_rule` still registers at call time and main's applicator still iterates registration
order. So the sentence survives in the 2026-10-22 docs but has no implementation on main either.

## 2. Quote and provenance check

All eight quotes are verbatim (whitespace-collapsed) in their committed fetch bytes — A19/A20/A21/
A22 in `S165.bin`, A23 in `S166.bin`, A24 in `S167.bin`, A25/A26 in `S168.bin` — and the fetch
sha256s match the SOURCES cells: `9ecff146…` (S165), `a513798f…` (S166), `95d8b842…` (S167),
`46fee4db…` (S168). The rows are documentary-accurate. Every defect below is in the note's
caveat/ordering prose, not in the quotes.

## 3. Impact

- **C1:** no claim row is falsified; `PASS_ROW` membership for A19–A26 is unaffected by this
  report (quotes and provenance hold). What fails is the *use* of those rows: the caveat calls all
  wiki rows `[INF-docs]` for this host when five of eight are directly source-verifiable in v0.56.2
  (A19/A20/A22/A23/A25) and one (A26) is provider-dependent in the opposite direction to the
  caveat's framing.
- **Attribution thesis:** `:27`'s "reading the declared files in that order" is sound only at a
  full read and only inside one provider; after a partial re-eval an earlier rule's value can
  persist (A21 counterexample).
- **C2:** unaffected.

## 4. Smallest safe correction (note text only; no SOURCES edit needed)

1. Replace `:89-90` with: v0.56.2 ships both config providers (`ConfigManager.cpp:16-57`, `.lua`
   selects Lua); the wiki documents the Lua syntax; the host's provider is hyprlang, so wiki rows
   are *provider-scoped* for this host, not `[INF-docs]` against v0.56.2.
2. Amend `:27`: "named rules first …" → "(hyprlang provider)" and "last match wins" → "last match
   wins on a full static read; partial property re-evaluation re-applies only rules whose own match
   mask intersects, so an earlier rule's value can persist".
3. In the route row `:21`, add: with zero workspace rules the plain form prints `unknown request`
   (`HyprCtl.cpp:2124`); use `hyprctl -j workspacerules` (`[]`). A24's quoted usage line is
   post-v0.56.2 wording; v0.56.2 help says "Lists all workspace rules" (`Strings.hpp:62`).
4. Under A19, state that `effect = …` in the syntax block is a metavariable; effects are top-level
   keys and a literal `effect` key is rejected.

## 5. Limits

- hyprlang itself is not in the clone (no `subprojects/hyprlang`; system `hyprlang 0.6.8`), so the
  relative order *among* named rules (`listKeysForSpecialCategory`) is unverified; only the
  named-vs-anonymous split is proven from `reloadRules`.
- No mutation, dispatch, keyword or reload ran; there is no live test of A21/A26 here, only source
  reading plus the wiki example.
- The host-provider claim is inherited from the round-12 note; `hyprctl systeminfo`/`status` is not
  in my allowed verbs. `hyprctl configerrors` returning empty is consistent with a parsing hyprlang
  config, not proof.
- The `main` fetch is corroboration, not authority: main is one day newer than the wiki pin, and
  main's file set can change after this report.
- No tools installed or updated.

VERDICT: partial — five of eight rows hold against the pinned v0.56.2 source (A19 as a schematic
syntax block, A20, A22, A23, A25); A21's "last match takes precedence" holds only on a full static
read and the page's own floating-kitty example is path-dependent (a kitty that maps floating gets
0.8, not the documented 0.5); A24's verb exists and lists workspace rules, but on this host the
plain-text form prints `unknown request` for the empty set and the quoted usage line postdates
v0.56.2; A26's named-first ordering holds for the host's hyprlang provider (named blocks hoisted by
`reloadRules`) but not for the Lua `hl.window_rule` path the wiki documents (registration is call
order; latest main has no hyprlang provider and no hoisting at all). The era caveat therefore
mis-frames the risk as era-only and lists only A19; the real axis is provider selection plus one
precedence invariant, and the note's ordering sentence needs the provider and full-read qualifiers.

Report: .ufo/waves/round-24/w2/reports/AtkEraWiki.md
