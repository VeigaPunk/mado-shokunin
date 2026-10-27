# mado round 49 - lesson (seat draft; the L1 integrates)

## Gate

Candidates considered: the bind-match plane of the C2 claim.

- **S352 admit**, tier A, code. URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened 2026-10-27; quote `const auto         KEYCODE = e.keycode + 8;` (`fetch/Hyprland-KeybindManager.cpp:367`). every later keymap call uses the +8 keycode.
- **S352 admit**, tier A, code. URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened 2026-10-27; quote `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` (`fetch/Hyprland-KeybindManager.cpp:369`). the compared sym is chosen by the per-device switch at the call site.
- **S352 admit**, tier A, code. URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened 2026-10-27; quote `const auto KBKEY      = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);` (`fetch/Hyprland-KeybindManager.cpp:710`). the first lookup of a press is exact.
- **S352 admit**, tier A, code. URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened 2026-10-27; quote `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)` (`fetch/Hyprland-KeybindManager.cpp:724`). a press must equal the exact or the case-insensitive resolution.
- **S352 admit**, tier A, code. URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened 2026-10-27; quote `if (!IGNORECONDITIONS && ((modmask != k->modmask && !k->ignoreMods)` (`fetch/Hyprland-KeybindManager.cpp:652`). the modifier compare is inequality of the whole mask.
- **S353 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c`; opened 2026-10-27; quote `bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);` (`fetch/libxkbcommon-src-keysym.c:242`). case-insensitivity is one bit and nothing else is honoured.
- **S354 admit**, tier A, own-work. Source opened this round: the read-only capture `.ufo/waves/round-49/receipts/live-binds-r49.txt`; access date 2026-10-27; binds=192, option int 0. It is the host-specific execution result, not an upstream source.
- **S357 admit**, tier A, own-work. Source opened this round: `control-unused-row.txt`; access date 2026-10-27. A side note.

No held row's status, recheck or used-by changed; S303, S317 and S319 are cited, not re-registered.
