# AtkSocketChannel — attack on the note's socket2 / plugin-bus negative claim

**Attacked.** `corpus/knowledge/rule-attribution-r24.md:66-68`, the negative-sweep bullet:

> socket2 (35 event names, none for rules), logs, the window object (`OverridableVar.hpp:153` keeps one
> optional value per override priority; `getPriority()` is not exported) and the plugin bus (`updateRules`
> carries the window only). Verdict NEGATIVE on every channel.

and the per-property row at `:24` ("neither is exported by hyprctl, Lua or socket2"). Source of the
inventory: `.ufo/waves/round-24/w1/reports/ScoutAttributionSweep.md` (channel table row "socket2 IPC
events", sweep 6). Question put to me: enumerate every event name in v0.56.2 (`EventManager` postEvent
sites, `EventBus.hpp`) and say whether any carries a rule identity or a match result.

## Pins and bytes

- Code: `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`, `git rev-parse HEAD` =
  `efb50993780079460b0cbed1363e2166a2de1d9f`, `git describe --tags --exact-match` = `v0.56.2`.
- The two files the claim rests on hash to the bytes the sweep recorded:
  `src/event/EventBus.hpp` sha256:`bfb8be17d84a0d8e7f10a0d61bcdc2b2e67378d139aaae8a484bebd96f62eede`
  and `src/managers/EventManager.cpp`
  sha256:`eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` — both identical to the
  sweep's table, so this attack measures the same bytes, not a lookalike.
- Wiki: `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`; event table in
  `content/ipc/_index.md` (44 rows).
- Read-only throughout: no lane file edited but this report; no git/jj write; no host commands.

## 1. Complete socket2 inventory at the pin

Method: a balanced-parenthesis parse of every `postEvent(` call in `src/**/*.cpp`, excluding the
definition; all 76 call sites pass a **string-literal** event name (balanced parse: 76 calls, 76 literals,
0 non-literal). `grep -rn "g_pEventManager->postEvent" src/ | wc -l` → **76**; the 78-line
`grep -rn "postEvent("` match count also picks up the declaration `EventManager.hpp:17` and the
definition `EventManager.cpp:163`. The sweep's "77 call sites" is the definition counted as a call.

Distinct emitted names: **45**. Grouped by data shape, with the rule question answered per group:

| event name(s) | data the emitter frames | rule identity / match result? |
|---|---|---|
| `workspace`, `workspacev2` | workspace name / id+name | no |
| `createworkspace`, `createworkspacev2` | name / id+name | no |
| `destroyworkspace`, `destroyworkspacev2` | name / id+name | no |
| `renameworkspace` | id,new name | no |
| `changeworkspaceid` | old id,new id | no |
| `moveworkspace`, `moveworkspacev2` | name,mon / id,name,mon | no |
| `focusedmon`, `focusedmonv2` | mon,workspace / mon,workspace id | no |
| `activespecial`, `activespecialv2` | workspace,mon / id,name,mon | no |
| `activewindow`, `activewindowv2` | class,title / address | no |
| `openwindow` | address,workspace name,class,title | no |
| `closewindow`, `kill`, `urgent` | address | no |
| `movewindow`, `movewindowv2` | address,ws / address,id,name | no |
| `windowtitle`, `windowtitlev2` | address / address,title | no |
| `fullscreen` | 0/1 | no |
| `changefloatingmode` | address,0/1 | no |
| `pin` | address,pin state | no |
| `minimized` | address,0/1 | no |
| `togglegroup` | 0/1,address(es) | no |
| `moveintogroup`, `moveoutofgroup` | address | no |
| `lockgroups` | 0/1 | no |
| `openlayer`, `closelayer` | namespace | no |
| `submap` | submap name | no |
| `activelayout` | keyboard name,layout | no |
| `monitoradded`, `monitoraddedv2`, `monitorremoved`, `monitorremovedv2` | id,name,description | no |
| `screencast`, `screencastv2` | state,owner[,name] | no |
| `configreloaded` | empty | no |
| `bell` | address or empty | no |
| `custom` | caller-supplied string | no (core never writes a rule id; see sweep candidate 10) |

Full alphabetical list (45): `activelayout activespecial activespecialv2 activewindow activewindowv2 bell
changefloatingmode changeworkspaceid closelayer closewindow configreloaded createworkspace
createworkspacev2 custom destroyworkspace destroyworkspacev2 focusedmon focusedmonv2 fullscreen kill
lockgroups minimized monitoradded monitoraddedv2 monitorremoved monitorremovedv2 moveintogroup
moveoutofgroup movewindow movewindowv2 moveworkspace moveworkspacev2 openlayer openwindow pin
renameworkspace screencast screencastv2 submap togglegroup urgent windowtitle windowtitlev2 workspace
workspacev2`.

Payload audit: scanning the **full argument text** of all 76 calls for `rule|tag|getPropertiesMask|
m_ruleApplicator` (case-insensitive) gives **0 hits**. No event name contains `rule`. No event's data
carries a tag set either, so socket2 offers neither rule identity nor the tag route (tags are in
`hyprctl clients`, claim A10, not on the event stream).

## 2. Counterexample — the note's "35" is an inventory undercount

The sweep's own command reproduces its 35, and provably misses 10 emitted names. Run in the clone:

```
grep -rhoE 'SHyprIPCEvent[[:space:]]*\{[[:space:]]*(\.event[[:space:]]*=[[:space:]]*)?"[a-zA-Z0-9]+"' src --include=*.cpp \
  | sed -E 's/.*"([a-zA-Z0-9]+)"/\1/' | sort -u | wc -l
→ 35
```

Correct extraction over the same tree (postEvent-literal parse) → **45**. Set difference (missed by the
sweep, present in the pin):

`bell changefloatingmode changeworkspaceid createworkspace createworkspacev2 destroyworkspace
destroyworkspacev2 kill renameworkspace togglegroup`

Three syntactic forms evade the regex, all live code:

1. **Deduced brace init, no `SHyprIPCEvent` token** — `g_pEventManager->postEvent({.event = "createworkspace", …})`
   in `src/desktop/Workspace.cpp:72,73,81,82,543,560` → `createworkspace(v2)`, `destroyworkspace(v2)`,
   `renameworkspace`, `changeworkspaceid`.
2. **Parenthesised brace init** `SHyprIPCEvent({…})` — `src/desktop/view/Group.cpp:66,82` (`togglegroup`),
   `src/managers/input/InputManager.cpp:953` (`kill`), `src/layout/LayoutManager.cpp:47`
   (`changefloatingmode`).
3. **Multi-line literal** — `.event = "bell"` on the line after `SHyprIPCEvent{` in
   `src/protocols/XDGBell.cpp:16,26,38,46` (`bell`).

Consequence: the sentence a reader can refute with one grep sits in the note's evidence paragraph. The
sweep's own stated caveat ("a mechanism spelled without that token would evade the sweep") does not
cover this — the 10 names are ordinary `rule`-free events missed by call **syntax**, not spelling. The
missed names do not rescue attribution (none is rule-bearing), so the conclusion survives; the numeral
and the method do not.

For the record, the wiki's 44-row event table is not the pin's emission set either: 43 names are shared,
the wiki list adds `ignoregrouplock` (documented but **not emitted** at the pin — `setignoregrouplock` is
a deprecated no-op, `DispatcherTranslator.cpp:861`, `KeybindManager.cpp:106`, no postEvent), and the pin
adds `custom` (`ConfigActions.cpp:1269`, the `event(string)` dispatcher) and `changeworkspaceid`. So
35, 44 and 45 are three different sets; only 45 is what v0.56.2 actually emits.

## 3. Plugin event bus (`src/event/EventBus.hpp`)

69 declared `Event`/`Cancellable` members, plus the plugin-defined `m_events.plugin` map and
`CCustomEvent::m_event`. Full list by section:

- top: `ready tick start exit`
- `window`: `create open openEarly openLate destroy close kill active urgent title class_ pin fullscreen
  floating updateRules moveToWorkspace`
- `layer`: `opened closed updateRules`
- `view`: `create destroy`
- `input.mouse`: `move button axis`; `input.keyboard`: `key layout focus`; `input.tablet`: `axis button
  proximity tip`; `input.touch`: `cancel down up motion`
- `render`: `preChecks pre stage`; `screenshare`: `state`; `gesture.swipe`: `begin end update`;
  `gesture.pinch`: `begin end update`
- `monitor`: `newMon destroyMon preAdded added preRemoved removed preCommit focused layoutChanged`
- `workspace`: `moveToMonitor active specialActive created removed`
- `config`: `preReload reloaded props_refreshed`; `keybinds`: `submap`
- `plugin`: `pluginEventAdded pluginEventRemoved` (+ the dynamic `plugin` map)

Exactly two carry a rule word: `window.updateRules` (`EventBus.hpp:91`, `Event<PHLWINDOW>`) and
`layer.updateRules` (`:98`, `Event<PHLLS>`). Their payloads are the view handle and nothing else. Both are
emitted **unconditionally** after a re-evaluation pass, not per match:
`CWindowRuleApplicator::recheckStaticRules()` ends with
`Event::bus()->m_events.window.updateRules.emit(m_window.lock())`
(`WindowRuleApplicator.cpp:589`, inside the function starting `:526`), and
`CLayerRuleApplicator::propertiesChanged()` ends with
`Event::bus()->m_events.layer.updateRules.emit(m_ls.lock())` (`LayerRuleApplicator.cpp:153`, function
starts `:127`). A subscriber learns "rules were re-read for this view", never which rule matched, whether
any matched, the property mask, or a match count. Every other bus event carries device/input/view/
monitor/workspace/config data — no `IRule`, no rule name, no rule index, no boolean "matched".

Adjacent channels checked because they could break the claim:

- Lua event bridge: `LuaEventHandler.cpp:110` forwards `window.updateRules` as `window.update_rules`
  with **one argument, the window** (`CLuaWindow::push(L, w)`); the layer variant is not even forwarded.
- Deprecated plugin hook path: `HyprlandAPI::registerCallbackDynamic` is stubbed — it returns `nullptr`
  and both hook lines are commented out (`PluginAPI.cpp:36-45`), so no named-hook path can carry a rule
  instead.
- Plugin API types: `grep -rn "IRule\|CWindowRule\|CLayerRule\|ruleName" src/plugins/` → 0 hits (the only
  "rule" tokens are `PERMISSION_RULE_*` permission modes). `HyprlandAPI::addEvent`
  (`PluginAPI.cpp:501-510`) only registers plugin-authored `CCustomEvent`s; core registers none.
- Events that a rule effect can *cause* (`window.floating`, `window.pin`, `window.fullscreen`) still
  carry the window handle only — an effect, not a cause.

So the plugin-bus half of the sentence is accurate, and slightly understated: there are two `updateRules`
events, not one, and both carry only the view.

## Verdict

The negative conclusion holds on both channels over the complete inventory: **0 of 45** socket2 events
and **0 of 69** declared bus events carry a rule identity or a match result (the two `updateRules`
events carry the view handle only, emitted unconditionally). But the note's parenthetical **"35 event
names" is false at the pin** — the real count is **45**, the sweep's own command reproduces the
undercount, and it misses 10 live, rule-free event names by call syntax; its "77 call sites" also counts
the function definition (76 real sites). The sentence needs correction even though its conclusion stands.

VERDICT: partial

## Impacted axes

- **depth** (primary): a one-grep-refutable numeral sits in the note's evidence paragraph
  (`rule-attribution-r24.md:67`), and the cited sweep hand-counts an incomplete surface.
- **coverage** (C1's axis): the note is the C1 artifact, but the negative sweep is explicitly prose, not
  a counted row. `c1/count.py` parses only `| A<n> | … | S### | "quote" |` rows (ROW_RE, `count.py:38`)
  and has no reference to the sweep or the number (grep for `sweep|35|Negative` in `count.py` → none), so
  PASS_ROW 23/26 and the landed receipts are unaffected. This is note accuracy, not target movement.
- **operability** (secondary): the sweep command is the runnable artifact; it runs and prints 35, but it
  does not enumerate the surface it claims to enumerate.
- No calibration, freshness or adjacency impact; no `tools/` change is involved.

## Smallest safe correction

1. `corpus/knowledge/rule-attribution-r24.md:67`: "35 event names" → "45 event names (76 `postEvent` call
   sites at the pin), none for rules". Line `:24` ("neither is exported by hyprctl, Lua or socket2")
   stays as written — it is supported.
2. `ScoutAttributionSweep.md` (channel table + sweep 6): replace the `SHyprIPCEvent`-only regex with a
   parse that also accepts `postEvent({.event = …})`, `SHyprIPCEvent({…})` and literals on a continuation
   line; correct 35 → 45 and "77 call sites" → 76 (exclude the definition); record the 10 previously
   missed names as rule-free. Optionally one sentence separating the wiki table (44 rows; includes
   `ignoregrouplock`, which the pin does not emit) from the pin's 45 (adds `custom`,
   `changeworkspaceid`), so a later reviewer does not "fix" the number to 44.
3. No claim row, SOURCES row, predicate, control, manifest or counter changes; the C1 receipts stand.

## Residual / bounds

- Host behaviour beyond `hyprctl version` (read by wave 1, not by me) is `[UNK]`; claims here are bounded
  to `efb50993` (v0.56.2), read from the pinned clone only.
- A third-party plugin can of course invent its own attribution channel from `m_otherProps` / the
  `updateRules` event; that is the note's own `[INFERENCE]` limit, not upstream attribution, and nothing
  in this sweep contradicts it.
- No tool installs or updates were needed this run; nothing was installed.
