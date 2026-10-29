# Dispatcher strings on Hyprland 0.56.2: what a bind stores past the key field, the map a press looks in, and the socket verb that reuses it

This entry picks up after the match. `corpus/knowledge/hyprland-bind-key-match-r50.md` settled
which keysym a bind's key field is compared against and which modifier mask the comparison uses;
this entry follows the remaining two fields of `bind = MODS, KEY, dispatcher, arg` - the name that
selects a callable out of one table, the tail that is handed to that callable unmodified, the two
names the press path handles differently (`submap`, `pass`), and the request verb that enters the
same table without a key event at all.

There is no argument grammar to state, and the entry's first job is to refuse one: the bind path
never splits its argument, the socket path splits it at the first space and nowhere else, and every
remaining decision about what an argument means belongs to the individual dispatcher.

source: [ref] - Hyprland 0.56.2 dispatcher map, its declared type and the press-time call - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp - code - the 71-name population in the constructor, the map's declared shape, the find-and-call in the press path, the mouse prefix, and the submap break - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: [ref] - Hyprland 0.56.2 legacy dispatcher translator, the implementation table and the per-dispatcher splitters - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp - code - how a name resolves to an implementation, and how five of those implementations read the one string they are given - `Bad dispatcher`(Hyprland-legacy-DispatcherTranslator.cpp:32)
source: [ref] - Hyprland 0.56.2 hyprctl dispatch request, the socket path into the same table - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp - code - the request's strip and first-space split, the Lua branch that returns before the table, the lookup, and the one-line reply - `m_dispatchers.find(DISPATCHSTR)`(Hyprland-HyprCtl.cpp:1149)
source: [ref] - Hyprland 0.56.2 submap action and action state - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp - code - the submap writer for a reset, an empty and a named argument, the refusal of an unregistered name, and the press/release marker the special handlers read - `Cannot set submap`(Hyprland-ConfigActions.cpp:1681)
source: [ref] - Hyprland 0.56.2 legacy bind dispatcher field, extraction, lowercasing, parse-time check - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp - code - how the dispatcher word and its argument are taken off a bind line and validated before any press - `m_dispatchers.find(HANDLER)`(Hyprland-legacy-ConfigManager.cpp:1594)
source: [ref] - Hyprland 0.56.2 dispatch result struct and its defaults - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/SharedDefs.hpp - code - the three fields a dispatcher returns and what an empty return means for the event - `passEvent = false`(Hyprland-SharedDefs.hpp:53)
held (cited, not re-registered, registry rows only): [ref] through [ref], the same two Hyprland files this entry reads past their round-50 regions; [ref], the wiki Binds page at the 0.56.2-era revision
lane: mado-shokunin. round: 51. wave: w1. base: 6ca8c559a4a3d6d361101592116eea2bc7452437.
verified-at: 2026-10-27
recheck: on-release - when Hyprland leaves `0.56.2` (`efb50993`) re-pull [ref]-[ref] and re-read the constructor table, the dispatch site, `run` and its map, `dispatchRequest`, and `setSubmap`/`pass`
ground: the bind parser, the flag alphabet and the key field were settled at corpus/knowledge/bind-table-r25.md:38 and corpus/knowledge/keybind-rule-semantics.md:73, and the match chain at corpus/knowledge/hyprland-bind-key-match-r50.md:57-124; this entry adds no second account of matching and treats the press-time submap comparison only as the gate it is

## Pin manifest

All paths relative to `.ufo/waves/round-51/fetch/`; Hyprland pins at commit `efb50993780079460b0cbed1363e2166a2de1d9f`, the host's running build (`hyprland 0.56.2-4`, a read-only package query).

| pin | file | row |
|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | [ref] |
| Hyprland-KeybindManager.hpp | src/managers/KeybindManager.hpp | [ref] |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | [ref] |
| Hyprland-legacy-DispatcherTranslator.hpp | src/config/legacy/DispatcherTranslator.hpp | [ref] |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | [ref] |
| Hyprland-ConfigActions.cpp | src/config/shared/actions/ConfigActions.cpp | [ref] |
| Hyprland-ConfigActions.hpp | src/config/shared/actions/ConfigActions.hpp | [ref] |
| Hyprland-legacy-ConfigManager.cpp | src/config/legacy/ConfigManager.cpp | [ref] |
| Hyprland-SharedDefs.hpp | src/SharedDefs.hpp | [ref] |
| Hyprland-ConfigManager.cpp | src/config/ConfigManager.cpp | - |
| Hyprutils-VarList.hpp | include/hyprutils/string/VarList.hpp | - |
| Hyprutils-VarList.cpp | src/string/VarList.cpp | - |
| Hyprutils-VarList2.cpp | src/string/VarList2.cpp | - |
| wiki-Using-hyprctl.md | content/Configuring/Using-hyprctl.md | - |
| wiki-Dispatchers.md | content/Configuring/Dispatchers.md | - |

Digests for the checksum manifest: `Hyprland-KeybindManager.cpp` 39334 B 975 lines sha256 `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40`; `Hyprland-KeybindManager.hpp` 191 lines `cee22c13d413ab389803e0eb87a6fcefadedea885cee4457b56ae351228dd1e0`; `Hyprland-legacy-DispatcherTranslator.cpp` 35997 B 868 lines `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771`; `Hyprland-legacy-DispatcherTranslator.hpp` 22 lines `438c1e662f5c9fa4d5821fbab251113c66562dd452d1844f965c294bb3444e87`; `Hyprland-HyprCtl.cpp` 97582 B 2346 lines `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`; `Hyprland-ConfigActions.cpp` 71407 B 1772 lines `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`; `Hyprland-ConfigActions.hpp` 122 lines `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073`; `Hyprland-legacy-ConfigManager.cpp` 90963 B 2184 lines `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`; `Hyprland-SharedDefs.hpp` 1915 B 60 lines `0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`; `Hyprland-ConfigManager.cpp` 2597 B 82 lines `c10dc1ce6602a854121a79fb0192c9f43aa836a35f9acb98ff1789541b01f366`; `Hyprutils-VarList.cpp` 38 lines `b02df8d688519366e7f20de5c3c44d21c3832316e8262ced0d295e129b166a36`; `Hyprutils-VarList.hpp` 65 lines `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43`; `Hyprutils-VarList2.cpp` 126 lines `b8cacea741b2d6260ad6618be00e37bc01c4d092e655a7557f7cfbadb76cf26d`; `wiki-Using-hyprctl.md` 315 lines `3489a75da5f0865d56deda13412c67af905d8507a4bc51367d96952e55ab3545`; `wiki-Dispatchers.md` 313 lines `39d0747a34bf013d62f8d70d4e1259cf084510e38c17bb4dc1e3245095c1f494`.

The four pins whose row cell is `-` carry no registry row (the rows seat rejected them under rule 4,
`w1/ScrRowsDispatch/rows.md` §4) and are cited only in the Limits section, never for a mechanism
claim. `Hyprland-KeybindManager.cpp` and `Hyprland-legacy-ConfigManager.cpp` are byte-identical to
the round-50 pins, so rows [ref]/[ref] stay theirs; this entry opens no row for either file.

## Held ground

These facts were on the lane's ground at the round base and are reused, never re-argued: the field
shape of a bind line and its capped split, the comma carried by the last field, the host's
submap-free bind plane, the two dispatcher names documented across both config eras, the round-50
parse account, and the file-presence rule that decides which config language a directory selects.

held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ARG,numbArgs
held: corpus/knowledge/bind-table-r25.md:52 keys=dispatcher
held: corpus/knowledge/keybind-rule-semantics.md:73 keys=params,comma-separated
held: corpus/knowledge/keybind-rule-semantics.md:55 keys=submap
held: corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md:48 keys=submap,pass,send_shortcut
held: corpus/knowledge/hyprland-bind-key-match-r50.md:57 keys=CVarList,numbArgs
held: corpus/knowledge/hyprland-config-era-r12.md:41 keys=hyprland.lua,hyprland.conf

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| what a bind stores for its dispatcher and its argument | step 2 | sourced |
| whether the dispatcher name is case-sensitive | step 2 | sourced: no, the parser folds it |
| whether a name is validated when the config is read or when a key is pressed | step 2, step 3 | sourced: at read; the press path only logs |
| which table a press looks in and what an entry is | step 1, step 3 | sourced: 71 names, one forwarder |
| whether the bind path splits its argument | step 2, step 7 | sourced: no |
| what governs an argument's meaning | step 7 | sourced: the individual dispatcher, five read |
| what `pass` does to the event and to focus | step 6 | sourced |
| where the current submap lives, who writes it, what refuses a write | step 5 | sourced |
| why a `submap` bind fires alone | step 5 | sourced |
| how the socket verb reaches the same code and what it replies | step 8 | sourced |
| why a `pass` issued over the socket differs from a `pass` bind | step 8 | sourced |
| which branch the socket verb takes on this host | step 9 | sourced plus one read-only host observation |
| what happens on key repeat or long press | step 3 | mechanism sourced; consequence `[INF]` |

## The chain

1. **Seventy-one names, one forwarder, two tables.** The keybind manager's constructor fills its
   table from a brace list running from `{`exec`,` (Hyprland-KeybindManager.cpp:42) to
   `releaseinputcapture` (Hyprland-KeybindManager.cpp:112), giving all 71 names the same closure:
   `m_dispatchers[name] = [n = std::string(name)](std::string args) -> SDispatchResult { return
   Config::Legacy::translator()->run(n, args); };` (Hyprland-KeybindManager.cpp:113). The member is
   a string-keyed function table and nothing else
   `std::unordered_map<std::string, std::function<SDispatchResult(std::string)>> m_dispatchers;`
   (Hyprland-KeybindManager.hpp:137). Behind it the translator holds a second table, also 71
   entries and also a name-to-function map
   `std::unordered_map<std::string, std::function<SDispatchResult(const std::string&)>> m_dispMap;`
   (Hyprland-legacy-DispatcherTranslator.hpp:19), filled at
   Hyprland-legacy-DispatcherTranslator.cpp:797-867; its entry point refuses an unknown name before
   calling anything `if (!m_dispMap.contains(d))` / `Bad dispatcher`
   (Hyprland-legacy-DispatcherTranslator.cpp:31-32) and otherwise calls the mapped function
   (Hyprland-legacy-DispatcherTranslator.cpp:34). Measured over both pins on 2026-10-27: the two
   lists carry the same 71 names in different order, so the inner refusal cannot be reached from a
   keybind - only from a caller that names the translator directly.

2. **What the bind line leaves behind.** The dispatcher word is taken by position
   `auto HANDLER = ARGS[2 + DESCR_OFFSET + DEVICE_OFFSET];`
   (Hyprland-legacy-ConfigManager.cpp:1584), and everything after it becomes the stored argument in
   one piece `const auto COMMAND = mouse ? HANDLER : ARGS[3 + DESCR_OFFSET + DEVICE_OFFSET];`
   (Hyprland-legacy-ConfigManager.cpp:1586) - no comma is touched again at this point. With the `m`
   flag the word is replaced by the literal and the written word moves into the argument
   `HANDLER = "mouse";` (Hyprland-legacy-ConfigManager.cpp:1589). The name is folded to lower case
   in place before use `std::ranges::transform(HANDLER, HANDLER.begin(), ::tolower);`
   (Hyprland-legacy-ConfigManager.cpp:1592) - so `EXEC` and `exec` are one dispatcher while the
   argument keeps its bytes - and it is checked against the very table a press will consult
   `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);`
   (Hyprland-legacy-ConfigManager.cpp:1594). A miss rejects the line, naming the word in the message
   (Hyprland-legacy-ConfigManager.cpp:1598); the accepted pair is stored on the bind as `handler`
   and `arg` (Hyprland-legacy-ConfigManager.cpp:1624-1631), beside the submap it was written under
   (Hyprland-legacy-ConfigManager.cpp:1633). A dispatcher name is thus a config-time commitment: an
   unknown one never reaches a key press.

3. **Three places call the table.** The press path dispatches collected hits from a second loop whose
   lookup rewrites the name for mouse binds
   `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`
   (Hyprland-KeybindManager.cpp:785) - which is why an `m`-flag bind reports `mouse` in
   `hyprctl binds` - and a miss there is only a log line `Invalid handler in a keybind!`
   (Hyprland-KeybindManager.cpp:799), because step 2 already refused it. Two timer callbacks bypass
   the press path and call the closure with the stored string: the long-press timer
   `DISPATCHER->second(m_lastLongPressKeybind->arg);` (Hyprland-KeybindManager.cpp:131) and the
   repeat timer `DISPATCHER->second(k->arg);` (Hyprland-KeybindManager.cpp:154). Neither writes the
   press field of step 4, whose value there is the cleared sentinel; `[INF]` a repeated or long-held
   `pass` bind therefore replays both key edges rather than the edge that fired.

4. **What the callable receives.** Two things, and one of them is process-wide state. Before the call
   the press edge is written into it
   `Config::Actions::state()->m_passPressed = sc<int>(pressed);`
   (Hyprland-KeybindManager.cpp:804); after the call it is cleared
   `Config::Actions::state()->m_passPressed = -1;` (Hyprland-KeybindManager.cpp:814); the declared
   meaning is three-valued
   `int m_passPressed = -1; // -1 = dynamic (press+release), 0 = released, 1 = pressed`
   (Hyprland-ConfigActions.hpp:114). The argument arrives exactly as stored
   `res = DISPATCHER->second(k->arg);` (Hyprland-KeybindManager.cpp:812), with one textual
   exception: the mouse handler gets a one-character edge prefix glued in front
   `res = DISPATCHER->second((pressed ? "1" : "0") + k->arg);`
   (Hyprland-KeybindManager.cpp:810) and strips it on arrival (Hyprland-legacy-DispatcherTranslator.cpp:676).
   The return value has three fields with forgiving defaults `bool passEvent = false;` /
   `bool success = true;` / `std::string error;` (Hyprland-SharedDefs.hpp:53-55), so a dispatcher
   that returns nothing counts as a success that does not swallow the event - the deprecated
   `setignoregrouplock` returns exactly nothing (Hyprland-legacy-DispatcherTranslator.cpp:861). The
   press path folds that into its own count `res.passEvent |= !found;`
   (Hyprland-KeybindManager.cpp:842), and an inhibitor may still turn the result into a failure
   (Hyprland-KeybindManager.cpp:845-851).

5. **`submap`: captured when written, written when dispatched.** A bind carries the submap that was
   current when its line was parsed (Hyprland-legacy-ConfigManager.cpp:1633, from the keyword write
   at :1797-1798), and a press copies the live value into the event
   `.submapAtPress = getCurrentSubmap()` (Hyprland-KeybindManager.cpp:396); `getCurrentSubmap` is a
   pure read of one string `return SSubmap{.name = Config::Actions::state()->m_currentSubmap};`
   (Hyprland-KeybindManager.cpp:599), whose members default empty
   (Hyprland-KeybindManager.hpp:25-26). The gate compares those two names with the same universal
   escape the modifier mask has `((k->submap.name != key.submapAtPress.name) && !k->submapUniversal)`
   (Hyprland-KeybindManager.cpp:652). At dispatch time the only writer is the `submap` action: the
   reset and empty forms write empty `Config::Actions::state()->m_currentSubmap = "";`
   (Hyprland-ConfigActions.cpp:1666), and a named form is written only after a scan of the bind list
   finds a bind carrying it `Config::Actions::state()->m_currentSubmap = submap;`
   (Hyprland-ConfigActions.cpp:1674), otherwise the call fails and says why
   `Cannot set submap` (Hyprland-ConfigActions.cpp:1681). A submap therefore exists because some
   bind named it: switching to any other name is an error string, not a state change. Two ordering
   rules ride on this dispatcher - it marks the event consumed and breaks, once while hits are
   still being collected (Hyprland-KeybindManager.cpp:775-778) and once after the call
   (Hyprland-KeybindManager.cpp:816-819), so it is dispatched alone; and a bind whose submap carries
   a reset target switches after its own dispatcher returns, but only if that dispatcher left the
   name untouched `if (k->handler != "submap" && !k->submap.reset.empty()) {` /
   `if (submapBefore == submapAfter)` / `Config::Actions::setSubmap(k->submap.reset);`
   (Hyprland-KeybindManager.cpp:820-823).

6. **`pass`: the handler that presses the key again elsewhere.** `ActionResult
   Actions::pass(std::optional<PHLWINDOW> w)` (Hyprland-ConfigActions.cpp:1465) resolves its
   argument as a window selector, points keyboard focus - or pointer focus when the last event was a
   button - at that window, re-sends the modifier state, then replays the code recorded on the event
   (Hyprland-KeybindManager.cpp:386) as press only, release only, or both, chosen by the
   three-valued field of step 4: `if (S.m_passPressed == 1) {` (Hyprland-ConfigActions.cpp:1487),
   `} else if (S.m_passPressed == 0) {` (Hyprland-ConfigActions.cpp:1492), and a branch that sends
   both edges in one call (Hyprland-ConfigActions.cpp:1499-1500). `pass` is one of the five names
   the press path handles specially
   `const bool SPECIALDISPATCHER = k->handler == "global" || k->handler == "pass" || k->handler ==
   "sendshortcut" || k->handler == "mouse" || k->releasePending;`
   (Hyprland-KeybindManager.cpp:782); a pressed one is remembered
   `m_pressedSpecialBinds.emplace_back(k);` (Hyprland-KeybindManager.cpp:795) and forgotten on its
   release (Hyprland-KeybindManager.cpp:793). The same field is the other two special handlers'
   input: `global` forwards it to the client (Hyprland-ConfigActions.cpp:1634), and `mouse` reads it
   as its only notion of pressed `const bool PRESSED =
   Config::Actions::state()->m_passPressed == 1;` (Hyprland-ConfigActions.cpp:1640), degrading to
   `MBIND_INVALID` otherwise (Hyprland-ConfigActions.cpp:1643). `sendkeystate` is the one dispatcher
   that writes the field itself, saving and restoring it around its work
   (Hyprland-ConfigActions.cpp:1603-1615).

7. **No shared grammar: each dispatcher reads the tail its own way.** Nothing re-tokenises
   `k->arg` between steps 2 and 4; the split happens inside whichever implementation the name
   selected, and the pinned table shows at least four different readings. `sendshortcut` demands
   exactly three comma-separated fields and rejects anything else `CVarList2 ARGS(args, 3);` /
   `if (ARGS.size() != 3)` (Hyprland-legacy-DispatcherTranslator.cpp:532-535), so a fourth comma in
   its tail is a config-time error rather than part of the argument. `setprop` takes three
   space-separated fields and rejoins what follows `CVarList2 vars(args, 3, ' ');`
   (Hyprland-legacy-DispatcherTranslator.cpp:773). `alterzorder` cuts once at the first comma
   (Hyprland-legacy-DispatcherTranslator.cpp:684). `mouse` strips exactly one character
   (Hyprland-legacy-DispatcherTranslator.cpp:676). `exec` does not split at all and hands the tail
   to the process executor (Hyprland-legacy-DispatcherTranslator.cpp:48-51). The contrast with the
   bind line is the point: there the field count is fixed by the parser and the final field keeps
   its commas (held, `bind-table-r25.md:38` and `keybind-rule-semantics.md:73`), so `exec` receives
   `foo, bar` intact while `sendshortcut` receiving the same shape would refuse it. An argument's
   grammar is a property of one dispatcher, and a claim about "the" argument grammar would be
   false against these pins.

8. **The socket verb is the same table behind a different front door.** One registered request
   command serves it (Hyprland-HyprCtl.cpp:2036). Its body drops the command word
   (Hyprland-HyprCtl.cpp:1128), hands a Lua config to `eval` and returns before the table is touched
   (Hyprland-HyprCtl.cpp:1130-1141), and otherwise cuts the remainder at the first space only:
   everything before it is the name, everything after it is the argument
   (Hyprland-HyprCtl.cpp:1143-1147). The lookup and the call are the bind path's
   `m_dispatchers.find(DISPATCHSTR)` (Hyprland-HyprCtl.cpp:1149) followed by the call and a one-line
   reply, `ok` or the dispatcher's own error text (Hyprland-HyprCtl.cpp:1153-1157), with an unmapped
   name reported as `Invalid dispatcher` (Hyprland-HyprCtl.cpp:1151). Three consequences follow from
   the code alone. First, the argument is as raw here as it is for a bind, so the same dispatcher
   sees the same string through either door. Second, this path never performs the write at
   Hyprland-KeybindManager.cpp:804, so the field keeps its `-1` default: a `pass` issued this way
   always takes the both-edges branch of step 6, and a `mouse` issued this way takes the degraded
   branch at Hyprland-ConfigActions.cpp:1643. Third, a submap switch through the socket still has to
   name a submap some bind carries, by step 5's refusal.

9. **Which branch this host takes.** The socket body tests the configured manager's type before the
   table (Hyprland-HyprCtl.cpp:1130), and that type is set by which config file the directory holds
   - the held rule is that a `hyprland.lua` selects the Lua manager and its absence leaves
   `hyprland.conf` in charge (`corpus/knowledge/hyprland-config-era-r12.md:41`). This host's config
   directory holds `hyprland.conf` with no `hyprland.lua` (read-only listing of `~/.config/hypr`,
   2026-10-27), so the Lua guard does not fire and `hyprctl dispatch <name> <args>` takes step 8's
   space-split branch. The pinned documentation for the verb describes only the branch this host
   does not run (pins `wiki-Using-hyprctl.md:53-61` and `wiki-Dispatchers.md:83-84`, no registry
   row - see Limits), so a reader following the page would write a Lua expression where this
   compositor expects a name.

## State claims (criterion 100)

Each host consequence above names its symbol and cites the write, not a read; a read-only cite
appears only where the claim concerns the value a write pins.

| state | attr | value claimed | setter cite | kind |
|---|---|---|---|---|
| `m_dispatchers` | entries | 71, all one forwarder | Hyprland-KeybindManager.cpp:113 | insert in constructor |
| `SKeybind::arg` | bytes | the raw tail of the bind line | Hyprland-legacy-ConfigManager.cpp:1586 via :1624-1631 | aggregate construction |
| `SKeybind::submap` | name | submap current at parse | Hyprland-legacy-ConfigManager.cpp:1633 and :1797 | aggregate construction, keyword write |
| `m_passPressed` | value | 1 press, 0 release, -1 between | Hyprland-KeybindManager.cpp:804 and :814 | assignment |
| `m_currentSubmap` | name | empty or a carried name | Hyprland-ConfigActions.cpp:1666 and :1674 | assignment |
| `m_lastCode` | code | key code of the dispatched event | Hyprland-KeybindManager.cpp:386 | assignment |

## Observations

**OBS** [ref]: `m_dispatchers[name] = [n = std::string(name)](std::string args) ->
SDispatchResult` (Hyprland-KeybindManager.cpp:113) - the outer table carries no per-name behaviour;
a dispatcher is a string and a function.
**OBS** [ref]: `Bad dispatcher` (Hyprland-legacy-DispatcherTranslator.cpp:32) - the inner refusal
exists but is unreachable from a keybind, which the outer table already validated. The lane now
carries three distinct failure strings for a bad name, one per path: `does not exist` at parse
time (Hyprland-legacy-ConfigManager.cpp:1598), `Bad dispatcher` if the translator is called
directly, and `Invalid dispatcher` from the socket (Hyprland-HyprCtl.cpp:1151); a message quoted
from one path does not identify the other two.
**OBS** [ref]: `Invalid dispatcher, requested` (Hyprland-legacy-ConfigManager.cpp:1598) - a bad
dispatcher name is a config error, caught where the line is read.
**OBS** [ref]: `return res.success ? "ok" : res.error;` (Hyprland-HyprCtl.cpp:1157) - the socket
answer is the dispatcher's own text, so an action failure is readable from a shell.
**OBS** [ref]: `setSubmap` (Hyprland-ConfigActions.cpp:1664) - the switch is one process-wide string,
which is why every keyboard sees it.
**OBS** [ref]: `success = true` (Hyprland-SharedDefs.hpp:54) - returning nothing is a success.

Census of the pinned bytes: pins=15 rows_cited=6 ([ref]-[ref]) held_rows_cited=2 ([ref], [ref])
dispatcher_names=71 translator_entries=71 call_sites=3 special_handlers=5 argument_grammars_read=5
socket_verbs_touching_the_table=1.

## Limits

- Nothing was pressed and nothing was dispatched: no key event, no `hyprctl` call, no reload. The
  mechanisms are read from the pins at `efb50993`; the host facts used are one directory listing
  (`~/.config/hypr` without a `.lua` file), the installed package version (`hyprland 0.56.2-4`,
  read-only query) and the round-50 bind receipt.
- The repeat and long-press consequences in step 3 are `[INF]`: neither callback writes the press
  field, and whether `pass` accepts being combined with the repeat or long-press flags at all was
  not traced.
- Five dispatchers' readings were read (sendshortcut, setprop, alterzorder, mouse, exec); the other
  66 entries were counted, not read, so "each dispatcher reads its own way" is established for those
  five and `[INF]` beyond them.
- The doc-vs-code gap around the verb's argument is left out of the mechanism: the shipped man page
  (`pin Hyprland-docs-hyprctl.1.rst:22-34`, no registry row) says an argument must be present, while
  `HyprCtl.cpp:1145-1147` still calls the dispatcher with an empty argument when no space follows
  the name. The code is what the entry claims; the page is a documentation finding only.
- The construction that selects the manager (`pin Hyprland-ConfigManager.cpp:40` and `:50`, no
  registry row) is not cited for step 9; that step rests on the held config-era rule plus the host's
  file listing, because the rows seat rejected a row for that file as a restatement of a held fact.
- The bind line's capped split is stated behaviourally (the last field keeps its commas, held) and
  not from the splitter's source: the pinned `hyprutils` (tag `v0.14.2`, commit `a21e87b8`, the
  version the host package reports as `0.14.2-1`) shows the cap implemented in `CVarList`
  (`pin Hyprutils-VarList.cpp:20-21`) but not implemented in `CVarList2`, whose `construct` never
  reads its `lastArgNo` parameter (`pin Hyprutils-VarList2.cpp:21-102`). No registry row exists for
  hyprutils, so that reading is not used for any claim; it matters only as the reason
  `sendshortcut`'s three-field test counts every comma rather than the last three groups.
- The Lua config path (`src/config/lua/`, `hl.dispatch`) was not read; steps 8 and 9 establish only
  that the branch exists, that it returns before the table, and that this host does not take it.
- `Config::Actions::state()` is treated as one process-wide object because every call site reaches
  it through the same accessor; where it is instantiated was not read.
- Two of the 71 names point at differently named functions (`focuswindowbyclass` at
  `::focuswindow`, `signal` at `::signalactive`); the aliasing table was not read further.
- A socket-issued submap switch and a `submap` bind are described as equivalent writes because both
  reach `Actions::setSubmap`; no receipt shows the socket path switching a submap on this host,
  whose bind plane carries none (held, `keybind-rule-semantics.md:55`).

## Errata (round 51 w2; append-only source-truth correction)

The w2 locator review (`.ufo/waves/round-51/w2/RevC2EntryTruth/entry-truth.md`, especially
§§2–9) found several statements broader than their cited code lines. These corrections supersede
the earlier wording; no runtime dispatch or host manager state was measured.

- **Bind argument preservation and splitter behavior.** The direct Hyprland pin at
  `ConfigManager.cpp:1584-1598` supports selecting `HANDLER`, assigning the `COMMAND` expression,
  lowercasing the handler and checking the map. The assignment alone does not prove comma or byte
  preservation. Any preservation claim is held knowledge from `bind-table-r25.md:38` and
  `keybind-rule-semantics.md:73`, not a new [ref]/[ref] source result. The inspected
  `CVarList2(args, 3)` call and `ARGS.size() != 3` return establish a dispatcher-time result for
  `sendshortcut`; they do not establish its delimiter semantics or a config-time error. The
  previous “fourth comma” and “config-time error” descriptions are withdrawn.
- **Mouse serialization.** `KeybindManager.cpp:785` selects the dispatch-map key for a mouse bind;
  it does not establish what `hyprctl binds` serializes. The previous serialization explanation is
  withdrawn.
- **Special path count.** The expression at `KeybindManager.cpp:782` names four special dispatcher
  strings (`global`, `pass`, `sendshortcut`, `mouse`) and also tests the boolean `releasePending`;
  it is not five special dispatcher names.
- **Submap scope.** `ConfigActions.cpp:1664-1682` shows reset/empty writes and a scan before a
  nonempty named target is accepted. Thus only a nonempty named target requires a registered bind
  carrying that submap; reset and empty bypass the scan. The previous universal “submap exists
  because a bind named it” sentence is withdrawn. The cited path demonstrates `setSubmap` writes,
  not an exhaustive census of every possible state writer.
- **Socket argument and pass state.** `HyprCtl.cpp:1143-1157` proves the socket path splits at its
  first space and invokes the same dispatcher map; bind and socket ingress can supply different
  strings. `dispatchRequest` itself does not assign `m_passPressed`, but that does not prove the
  process-wide field is always `-1` at every invocation. The both-edge `pass` consequence is
  limited to an ordinary idle/default state; no universal socket-state claim is made. Likewise,
  the named-submap scan applies to nonempty names, not reset/empty forms.
- **Host branch.** The `~/.config/hypr` directory listing is an on-disk observation only; it does
  not establish which manager a running instance selected (explicit startup path and process-start
  timing remain open). The previous running-host branch conclusion and unregistered wiki-branch
  contrast are withdrawn. This entry claims the source-level Lua guard and legacy path, not the
  current instance's selected branch.
- **Evidence table.** The earlier “sourced: no bind split,” “sourced: why socket pass differs,”
  and “sourced plus host observation” labels are narrowed by the corrections above. The remaining
  claim is the pinned source-level parse/lookup/call path and the explicitly held context; no key
  event, socket request, runtime dispatcher result, or UI effect is claimed.
