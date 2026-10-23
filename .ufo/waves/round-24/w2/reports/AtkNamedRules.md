# AtkNamedRules — wave-2 critic, named-rule rows and statements

Seat: `MadoR24.AtkNamedRules` (critic). Item attacked: claim rows **A12–A16** of
`corpus/knowledge/rule-attribution-r24.md` and the note's statements about named rules —
the table row at `:23`, the ordering sentence at `:27-29`, and the negative-sweep bullet
"Unnamed hyprlang inline rules" at `:72-74`. Lane tip reviewed: `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`;
round base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`.

Pins and reads (all read-only): Hyprland clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`
(`git rev-parse HEAD` = `efb50993780079460b0cbed1363e2166a2de1d9f`), committed fetch bytes under
`.ufo/waves/round-24/fetch/`, and the note/SOURCES/wave-1 reports in the lane. No git/jj writes,
no host mutation, no packages or tools installed, no counter run. The lane's frozen C1 counter was
not re-run — this is a document/source review, not a re-score.

## Verdict

**VERDICT: partial** — A12–A16 all hold (quotes verbatim in the committed bytes, line anchors
correct, claims accurate); the note's *named-rule prose* has four defects: one wrong reader claim,
one unresolvable path anchor, one unqualified static-effect claim in the enable/disable row, and
one provider-blind ordering sentence. None of them changes the article's headline negative (no
window→rule-name attribution channel), and none makes any of A12–A16 an unsupported row.

## 1. A12–A16: all five rows hold

Every quote was re-checked by whitespace collapse against the committed `.bin` byte-for-byte
(Python, run this seat), and each `.bin` was `cmp`-identical to the pinned clone file.

| row | source | quote in bytes | claim vs source | anchor |
|---|---|---|---|---|
| A12 | S159 `LuaBindingsConfigRules.cpp` | yes (6 words) | holds | line 1194–1196, inside S159's `1167-1198` |
| A13 | S160 `LuaWindowRule.cpp` | yes (3 words) | holds | lines 40–41, inside S160's `12-80` |
| A14 | S160 `LuaWindowRule.cpp` | yes (16 words) | holds | lines 56–63, inside S160's `12-80` |
| A15 | S162 `legacy/ConfigManager.cpp` | yes (4 words) | holds | line 591, inside S162's `590-623` |
| A16 | S162 `legacy/ConfigManager.cpp` | yes (7 words) | holds | line 950, inside S162's `893-968` |

Provenance: `sha256:157c3e45…` (S159), `sha256:02f70f04…` (S160), `sha256:9db68cf4…` (S162) all
match the SOURCES cells; `cmp` printed `same:` against
`src/config/lua/bindings/LuaBindingsConfigRules.cpp`, `src/config/lua/objects/LuaWindowRule.cpp`
and `src/config/legacy/ConfigManager.cpp` respectively.

Claim-by-claim source check:

- **A12 holds.** `LuaBindingsConfigRules.cpp:1189-1196`: a hit on
  `!name.empty() && m_luaWindowRules.contains(name)` reuses the cached rule; otherwise
  `makeShared<CWindowRule>(name)` (1193), `m_luaWindowRules[name] = rule` (1195), then
  `registerRule(...)` (1196). Store-before-register is literally true. The row's quote is
  contiguous at 1194–1196 and does not pretend to show the reuse branch.
- **A13 holds.** `LuaWindowRule.cpp:40-41` is exactly `setEnabled(lua_toboolean(L, 2))` +
  `ruleEngine()->updateAllRules()`; the setter returns zero results.
- **A14 holds.** `LuaWindowRule.cpp:56-63`; live rule ⇒ one boolean result, dead rule ⇒ nil.
- **A15 holds.** `src/config/legacy/ConfigManager.cpp:591` is
  `m_config->addSpecialCategory("windowrule", {.key = "name"});`.
- **A16 holds.** Same file `:950`, inside `reloadRules()`, iterating
  `listKeysForSpecialCategory("windowrule")`.

## 2. Answers to the four questions put to this seat

### Q1 — Are hyprlang inline `windowrule = …` lines really unnamed? **Yes.**

`handleWindowrule` (`ConfigManager.cpp:2016-2055`) constructs the rule with the default
constructor: `:2019` `SP<Desktop::Rule::CWindowRule> rule = makeShared<Desktop::Rule::CWindowRule>();`.
`CWindowRule(const std::string& name = "")` (`WindowRule.hpp:52`) forwards to
`IRule(name)` (`Rule.cpp:86`), so `m_name` is `""`. The parser at `:2024-2047` accepts only
`match:<prop> value` elements and effect names; a bare `name` token has no space and fails with
"missing a value", and `name foo` fails with "invalid field type name". The rule goes to
`m_keywordRules` (`:2050`) and is registered in `reloadRules` (`:961-963`) or immediately for
dynamic keywords (`:2051-2052`), still unnamed. The `windowrulev2`/`layerrulev2` handlers
(`:431-435`, `:449-453`) only return deprecation errors. No inline naming path exists.

### Q2 — Are block rules keyed by `name`? **Yes, in the legacy manager.**

`:591` declares the special category with key `name`; `reloadRules` iterates those keys (`:950`)
and `addRuleFromConfigKey(name)` constructs `makeShared<CWindowRule>(name)` (`:898`). So the
category key becomes `IRule::m_name`. (What the file does not establish — and S162's own cell
says so — is hyprlang's block grammar and whether `name` is mandatory. The note's sentence
"block rules are keyed by `name`" is a statement about this manager's keying, which is exactly
what the bytes show.)

### Q3 — Are Lua names cached? **Yes, with a one-config-generation lifetime.**

`Config::Lua::CConfigManager::m_luaWindowRules` is
`std::unordered_map<std::string, SP<Desktop::Rule::CWindowRule>>`
(`src/config/lua/ConfigManager.hpp:146`; the member is in the `public:` section that starts at
`:54`). It is populated at `LuaBindingsConfigRules.cpp:1195` and consulted at `:1190`; it is
cleared on Lua config reload at `src/config/lua/ConfigManager.cpp:706`, immediately after
`ruleEngine()->clearAllRules()` at `:702`, before the guarded `pcall` at `:746`. So the "cache"
is per config generation, not a persistent name registry — consistent with A12 and with the
SrcLuaRules report's own caveat.

### Q4 — Is there any read path from a window to the names of rules that matched it? **No upstream export; only an in-process recomputation.**

Enumerated and re-checked in the pinned tree:

- Applicator state holds no rule reference. `WindowRuleApplicator.hpp:41-141`: dynamic values are
  `COverridableVar` + a property mask; `m_dynamicTags` pairs tag→mask; `m_otherProps` keeps
  `{idx, propMask, effect}`. `m_execRules` (`:148`) is **private**, exec-only, cleared each read,
  and the applied exec rules are unregistered (`WindowRuleApplicator.cpp:517-522`).
- `CWindow` stores only `UP<CWindowRuleApplicator> m_ruleApplicator` (`Window.hpp:236`).
- Lua handle exposes only `set_enabled`/`is_enabled` (`LuaWindowRule.cpp:58-70`, keys at
  `:62-65`); `__tostring` prints `%p`; no name read-back.
- Lua window object: the only rule-derived key is `tags` (`LuaWindow.cpp:140`); query filters
  test `m_tagKeeper.isTagged` (`LuaBindingsQuery.cpp:63`).
- `hyprctl clients` JSON carries `tags` (`HyprCtl.cpp:347`, emitted `:433`) and no rule identity;
  `getprop` renders `prop.valueOrDefault()` (`:1548-1553`); the verb table (`:2003-2043`) contains
  no window/layer rule listing — `workspacerules` (`:2005`) is workspace rules only.
- Events: `Event<PHLWINDOW> updateRules` (`EventBus.hpp:91`), emitted with the window only
  (`WindowRuleApplicator.cpp:589`).
- Logs: 15 `Log::logger->log` calls under `src/desktop/rule/`, none containing `name` (grep).
  The one "Rule workspace matched by {}, {} applied." line passes the *window* and
  `static_.workspace` (`Window.cpp:2187`), not a rule name.

**Strongest counterexample found, and why it does not overturn the note:** `CRuleEngine::rules()`
is public (`Engine.hpp`; `Engine.cpp:54-56`) and `CWindowRule::matches(PHLWINDOW, bool)` is public
(`WindowRule.hpp:65`), with `IRule::name()` public (`Rule.hpp:63`). Any in-process consumer
(core code or a C++ plugin compiled against these headers) can iterate the engine's rules, call
`matches(window)` and read the names of rules matching *now*. That is a recomputation, not a
record of what applied a value: it cannot see which rule produced the current value, it depends on
present window state, and exec rules that already fired are gone from `m_rules`. So "no upstream
channel maps an applied property back to the rule" survives. The note's Limits paragraph hedges
plugins but names the wrong mechanism (the applicator's registered props); the actual mechanism is
the public rule vector + public `matches`/`name`. Smallest fix: replace that parenthetical with the
engine-list recomputation and state explicitly that it yields "matches now", not provenance.

## 3. Defects in the note's named-rule prose

### D1 (wrong reader claim, `:72`) — "`IRule::name()` is read only by the engine and the Lua registry"

Mechanically wrong on the Lua half. A whole-tree sweep (grep `->name()` in `src/`, filtered for
rule/config-value labels) returns exactly one rule-name reader:
`src/desktop/rule/Engine.cpp:22`, inside `CRuleEngine::unregisterRule(const std::string&)` — and
that overload has **no in-tree caller** (the only call is the `SP<IRule>` overload at
`WindowRuleApplicator.cpp:521`). The Lua registry never calls `name()`: the map key is the local
`name` string parsed from the table at `LuaBindingsConfigRules.cpp:1177-1180` and stored at
`:1195`. The handle's `__index` exposes no name at all (`LuaWindowRule.cpp:58-70`).

Effect: the sentence implies Lua can read a name off a rule; it cannot. Smallest safe correction:

> `IRule::name()` has one in-tree reader, `CRuleEngine::unregisterRule(const std::string&)`
> (no in-tree caller); the Lua registry is keyed by the table's `name` string at creation and
> no binding reads `name()` back.

### D2 (broken anchor, `:74`) — "`legacy/ConfigManager.cpp:2019`"

The file is `src/config/legacy/ConfigManager.cpp`; there is no top-level `legacy/` directory in
the v0.56.2 tree (`find . -name ConfigManager.cpp` → `src/config/ConfigManager.cpp`,
`src/config/legacy/ConfigManager.cpp`, `src/config/lua/ConfigManager.cpp`). The line number is
right and its content is the unnamed-rule evidence:
`SP<Desktop::Rule::CWindowRule> rule = makeShared<Desktop::Rule::CWindowRule>();` at `:2019`.
The same shorthand is carried in the wave-1 report
`.ufo/waves/round-24/w1/reports/ScoutAttributionSweep.md` ("Candidate 1"). Smallest fix: prefix
`src/config/`. (Not a counted-row defect; A15/A16's anchors are full paths and correct.)

### D3 (unqualified claim, table row `:23`) — "enable or disable a rule to test it … whether the effect disappears when the rule is off"

A13 holds, but the inference in the row overstates what `set_enabled` demonstrates.

- `windowRuleSetEnabled` → `setEnabled` + `updateAllRules` (`LuaWindowRule.cpp:32-43`, calls at
  `:40-41`).
- `updateAllRules` calls `propertiesChanged(RULE_PROP_ALL)` on mapped windows (`Engine.cpp:34-48`).
- `propertiesChanged` (`WindowRuleApplicator.cpp:547-589`) resets *dynamic* override vars, dynamic
  tags and `m_otherProps` through `resetProps` (`:37-79`), then re-applies dynamic rules only. It
  never calls `readStaticRules`.
- Static effects write the separate `static_` struct (`applyStaticRule`, `:378-469`), which is
  reset only by `static_ = {}` in `readStaticRules` (`:487`). `readStaticRules` is called only from
  `CWindow::mapWindow` (`Window.cpp:2277`) and `CWindow::commitWindow` (`:2720`, pre-read).

Therefore, on an already-mapped window, disabling a rule reverts **dynamic** effects immediately,
but **static** effects (float, size, center, pin, fullscreen, workspace, …) persist until a
remap/reload — the wiki says the same for static effects ("evaluated once when the window is
opened and never again", S165). Additionally, this route is Lua-manager-only: `hyprctl eval`
returns "eval is only supported with the lua config manager" (`HyprCtl.cpp:1111-1112`), and the
config manager is selected by file extension (`.lua` → Lua, else legacy,
`src/config/ConfigManager.cpp:33-51`); the note's host runs hyprlang. Smallest safe correction:
"What it shows: whether the *dynamic* effect disappears when the rule is off (static effects only
after a remap/reload) — Lua configs only." A13 itself needs no change.

### D4 (provider-blind ordering, `:27-29`) — "named rules first, then anonymous, top to bottom, last match wins"

The named-first half is a **legacy-manager registration-order artifact**, not an engine property:

- Legacy: `reloadRules()` registers named `windowrule` blocks, then named `layerrule` blocks, then
  the anonymous `m_keywordRules` vector (`ConfigManager.cpp:946-967`). Named-before-anonymous
  therefore holds for hyprlang configs.
- Lua: `.lua` configs select `Config::Lua::CConfigManager` (`src/config/ConfigManager.cpp:33-51`).
  `hl.window_rule` calls `registerRule` at the point of declaration
  (`LuaBindingsConfigRules.cpp:1196`); there is no sorting pass (`grep sort` over
  `src/desktop/rule` and `src/config/lua` finds only match-prop/engine tables and config paths).
- Application order is `ruleEngine()->rules()` insertion order
  (`WindowRuleApplicator.cpp:492` and `:554`), and `COverridableVar::set` overwrites at equal
  priority (`OverridableVar.hpp:72-74`), so a later-registered rule wins.

Source-level counterexample (not run on the host): in a `.lua` config, declare an anonymous
`hl.window_rule{...}` and then a named `hl.window_rule{name = "n", ...}` with the same effect; the
named rule registers later, applies later, and wins — the opposite of A26's "all named rules are
evaluated first". The note's synthesis and its "reading the declared files in that order" advice
are therefore true for hyprlang and false for Lua. Smallest safe correction: scope the sentence to
the hyprlang provider and add one clause that the Lua provider evaluates in call order (named-first
is not enforced there). A26 itself is unchanged — it is a faithful "the wiki states" row.

## 4. Adjacent observation (not a defect in A12–A16; no action requested here)

`addLayerRuleFromConfigKey` (`src/config/legacy/ConfigManager.cpp:919-923`) returns early when the
`layerrule` block's `enable` is *set by the user and non-zero* — inverted relative to the window
path at `:894-896` (`== 0`). Consequences in v0.56.2: `layerrule { name = x; enable = 1; … }` is
skipped, while `enable = 0` is registered. This sits next to A23 (layer handles), not A12–A16, and
the note does not claim anything about layer `enable`; flagged only because it is in the same
named-block reconstruction path the note cites.

## 5. Impacted axes and blast radius

- **C1 coverage (note correctness):** no counted row fails. A12–A16 each pass quote, topic,
  claim-anchor and line-anchor checks against byte-identical receipts. The counter's
  `PASS_ROW`/`TARGET_MET` result is unaffected by D1–D4. The findings are against the note's prose,
  which the registration explicitly leaves to wave-2 re-reading ("the counter cannot judge whether
  a claim is supported").
- **Attribution thesis:** unchanged. Q4 confirms there is no window→matched-rule-name export;
  D1/D3/D4 narrow what the named-rule routes can show but do not revive an attribution channel.
- **QUALITY / anchors:** D2 is a resolvable-to-unresolvable path in prose; D1 is a false reader
  claim. Both are cheap text fixes, no re-scoring.
- **No-harm guards:** untouched — no file outside this report was written.

## 6. Commands that produced the evidence

```sh
# rows vs committed bytes (Python, whitespace-collapse; all True; word counts 6,3,16,4,7)
# anchor/hash cross-check
sha256sum .ufo/waves/round-24/fetch/S159.bin S160.bin S162.bin
cmp fetch/S162.bin src/config/legacy/ConfigManager.cpp   # same
cmp fetch/S159.bin src/config/lua/bindings/LuaBindingsConfigRules.cpp   # same
cmp fetch/S160.bin src/config/lua/objects/LuaWindowRule.cpp   # same
# source checks (clone, read-only)
grep -rn 'm_luaWindowRules' src/
grep -rn '\->name()' src/          # one rule reader: Engine.cpp:22
grep -rn 'unregisterRule' src/     # name overload: no caller
grep -rn 'addSpecialCategory\|listKeysForSpecialCategory' src/config/legacy/ConfigManager.cpp
grep -rn 'recheckStaticRules\|readStaticRules' src/
grep -rn 'sort\|stable_sort' src/desktop/rule src/config/lua
grep -rn 'configProvider' src/ ; sed -n '15,55p' src/config/ConfigManager.cpp
sed -n '1110,1113p' src/debug/HyprCtl.cpp
```

Report: `.ufo/waves/round-24/w2/reports/AtkNamedRules.md`
