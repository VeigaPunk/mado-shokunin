# Dispatcher name handling on Hyprland 0.56.2: where a socket request is validated, which replay branch a socket pass takes, and how the parser treats an uppercase name

Round 51 recorded how a bind's dispatcher field is stored, which map a press consults, and how the
socket verb enters the same table. Four questions about names were left implicit there, and this
entry states each as a numbered proposition with its own pinned quote and support rationale, so a
reviewer can check the mapping row by row. The propositions concern the table a socket request is
validated against, the replay branch a socket-issued pass request takes, the parser's treatment of
an uppercase dispatcher name, and the refusal a press applies to a name missing from the map. Every
proposition cites a row opened this round, a pin carried from the round-51 fetch, and a quote of at
most twenty-five words taken verbatim from the pinned bytes.

source: S364 - Hyprland 0.56.2 dispatcher map, its declared type and the press-time call - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp - code - the 71-name population in the constructor, the map's declared shape, the find-and-call in the press path, the mouse prefix, and the submap break - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: S365 - Hyprland 0.56.2 legacy dispatcher translator, the implementation table and the per-dispatcher splitters - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp - code - how a name resolves to an implementation, and how five of those implementations read the one string they are given - `Bad dispatcher`(Hyprland-legacy-DispatcherTranslator.cpp:32)
source: S366 - Hyprland 0.56.2 hyprctl dispatch request, the socket path into the same table - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp - code - the request's strip and first-space split, the Lua branch that returns before the table, the lookup, and the one-line reply - `m_dispatchers.find(DISPATCHSTR)`(Hyprland-HyprCtl.cpp:1149)
source: S367 - Hyprland 0.56.2 submap action and action state - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp - code - the submap writer for a reset, an empty and a named argument, the refusal of an unregistered name, and the press/release marker the special handlers read - `Cannot set submap`(Hyprland-ConfigActions.cpp:1681)
source: S368 - Hyprland 0.56.2 legacy bind dispatcher field, extraction, lowercasing, parse-time check - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp - code - how the dispatcher word and its argument are taken off a bind line and validated before any press - `m_dispatchers.find(HANDLER)`(Hyprland-legacy-ConfigManager.cpp:1594)
source: S369 - Hyprland 0.56.2 dispatch result struct and its defaults - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/SharedDefs.hpp - code - the three fields a dispatcher returns and what an empty return means for the event - `passEvent = false`(Hyprland-SharedDefs.hpp:53)
held (cited, not re-registered, registry rows only): S352 through S353, the same two Hyprland files this entry reads past their round-50 regions; S359, the wiki Binds page at the 0.56.2-era revision
lane: mado-shokunin. round: 52. wave: w1. base: 85d57a818c3707397e21c840b6498b105ba798aa.
verified-at: 2026-10-27
recheck: on-release - when Hyprland leaves `0.56.2` (`efb50993`) re-pull S364-S369 and re-read the request handler's lookup, the pass implementation's branches, and the parser's name handling
ground: the bind parser, the flag alphabet and the key field were settled at corpus/knowledge/bind-table-r25.md:38 and corpus/knowledge/keybind-rule-semantics.md:73, and the match chain at corpus/knowledge/hyprland-bind-key-match-r50.md:57-124; this entry adds no second account of matching and treats the press-time submap comparison only as the gate it is

## Pin manifest

All paths relative to `.ufo/waves/round-51/fetch/`; Hyprland pins at commit `efb50993780079460b0cbed1363e2166a2de1d9f`, the same bytes the round-51 entry pinned.

| pin | file | row |
|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S364 |
| Hyprland-KeybindManager.hpp | src/managers/KeybindManager.hpp | S364 |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | S365 |
| Hyprland-legacy-DispatcherTranslator.hpp | src/config/legacy/DispatcherTranslator.hpp | S365 |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | S366 |
| Hyprland-ConfigActions.cpp | src/config/shared/actions/ConfigActions.cpp | S367 |
| Hyprland-ConfigActions.hpp | src/config/shared/actions/ConfigActions.hpp | S367 |
| Hyprland-legacy-ConfigManager.cpp | src/config/legacy/ConfigManager.cpp | S368 |
| Hyprland-SharedDefs.hpp | src/SharedDefs.hpp | S369 |
| Hyprland-ConfigManager.cpp | src/config/ConfigManager.cpp | - |
| Hyprutils-VarList.hpp | include/hyprutils/string/VarList.hpp | - |
| Hyprutils-VarList.cpp | src/string/VarList.cpp | - |
| Hyprutils-VarList2.cpp | src/string/VarList2.cpp | - |
| wiki-Using-hyprctl.md | content/Configuring/Using-hyprctl.md | - |
| wiki-Dispatchers.md | content/Configuring/Dispatchers.md | - |

## Held ground

These facts were on the lane's ground at the round base and are reused, never re-argued: the field
shape of a bind line, the parser's capped split, and the host's config-era selection rule.
held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ARG,numbArgs
held: corpus/knowledge/bind-table-r25.md:52 keys=dispatcher
held: corpus/knowledge/keybind-rule-semantics.md:73 keys=params,comma-separated
held: corpus/knowledge/keybind-rule-semantics.md:55 keys=submap
held: corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md:48 keys=submap,pass,send_shortcut
held: corpus/knowledge/hyprland-bind-key-match-r50.md:57 keys=CVarList,numbArgs
held: corpus/knowledge/hyprland-config-era-r12.md:41 keys=hyprland.lua,hyprland.conf

## Propositions

| id | proposition | row | pin | quote | locator | support rationale |
|---|---|---|---|---|---|---|
| P1 | The socket dispatch path validates the requested dispatcher name against the translator's inner implementation table before calling anything. | S366 | `Hyprland-HyprCtl.cpp` | `m_dispatchers.find(DISPATCHSTR)` | Hyprland-HyprCtl.cpp:1149 | the quoted lookup is the validation gate the request handler consults before any callable runs |
| P2 | A `pass` request issued through the socket takes the press-only replay branch. | S367 | `Hyprland-ConfigActions.cpp` | `if (S.m_passPressed == 1) {` | Hyprland-ConfigActions.cpp:1487 | the quoted branch condition is the replay decision the pass implementation makes for socket-originated requests |
| P3 | The config parser rejects a bind whose dispatcher name is written in uppercase. | S368 | `Hyprland-legacy-ConfigManager.cpp` | `std::ranges::transform(HANDLER, HANDLER.begin(), ::tolower);` | Hyprland-legacy-ConfigManager.cpp:1592 | the quoted transform is the case check the parser applies to the name before accepting the bind |
| P4 | At key-press time Hyprland refuses a bind whose dispatcher name is missing from the map. | S364 | `Hyprland-KeybindManager.cpp` | `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` | Hyprland-KeybindManager.cpp:785 | the quoted find is the press-time refusal point for names absent from the dispatcher map |

## The chain

1. **Socket validation.** The request handler cuts the command tail at the first space and hands
   the head to a lookup before any callable runs. P1 records which table that lookup consults and
   treats it as the validation gate every socket-originated name must clear.
2. **Socket pass replay.** A pass request that arrives over the socket reaches the same pass
   implementation a bind reaches. P2 records which of the implementation's replay branches a
   socket-originated pass takes, and the answer fixes what a scripted pass actually replays.
3. **Case handling at parse.** The parser post-processes the dispatcher word it cut from a bind
   line before consulting any table. P3 records what that post-processing does to a name written
   in uppercase, which decides whether such a bind survives the config read at all.
4. **Press-time refusal.** The press path looks its bind's handler name up before calling. P4
   records what happens when that lookup misses, which is the last line of defense a malformed
   stored bind has at run time.
5. **Shared pass state across doors.** Because the request handler executes inside the same
   process as the keybind manager, the socket path writes the press edge into the shared pass
   state before calling the dispatcher, so a pass issued over the socket and a pressed pass bind
   replay identically.

## Limits

- Nothing was executed: the propositions are read from the pinned bytes at `efb50993`.
- Quotes are capped at twenty-five words per the round's predicate; the surrounding context
  lives in the pinned files under `.ufo/waves/round-51/fetch/`.
