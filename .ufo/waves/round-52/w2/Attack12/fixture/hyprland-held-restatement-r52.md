# Held-ground restatement control (round 52, attack fixture)

This entry exists only as an attack fixture: every proposition restates a fact already admitted in
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, re-anchored to newly numbered rows. It adds
no new mechanism, no new byte, and no new scope beyond the lines the round-51 entry already cites.

source: S374, S375
verified-at: 2026-10-27
recheck: none - fixture

Propositions P01-P04 restate round-51 facts. Sources S374 and S375 are the rows this entry opens.

## Proposition map

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|
| P01 | All dispatcher names in the keybind table forward to the legacy translator through one closure. | S374 | Hyprland-KeybindManager.cpp:113 | `m_dispatchers[name] = [n = std::string(name)](std::string args) -> SDispatchResult { return Config::Legacy::translator()->run(n, args); };` | direct | The lambda body calls the translator run with the name and the argument. |
| P02 | The press path invokes the stored handler with the stored argument string. | S374 | Hyprland-KeybindManager.cpp:812 | `res = DISPATCHER->second(k->arg);` | direct | The found dispatcher is called with the bind argument unchanged. |
| P03 | The press field is reset to the between-events sentinel after the handler returns. | S374 | Hyprland-KeybindManager.cpp:814 | `Config::Actions::state()->m_passPressed = -1;` | direct | The assignment follows the call and restores the sentinel value. |
| P04 | The sendshortcut implementation rejects a tail that does not split into exactly three fields. | S375 | Hyprland-legacy-DispatcherTranslator.cpp:531-535 | `if (ARGS.size() != 3) return {.success = false, .error = "sendshortcut: invalid args"};` | direct | The size test and error return form the rejection gate. |
