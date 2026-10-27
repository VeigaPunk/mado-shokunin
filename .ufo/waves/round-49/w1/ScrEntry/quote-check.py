#!/usr/bin/env python3
"""Recompute every locator quoted in hyprland-bind-key-match-r49.md.

For each (pin, locator, quote) it greps the pinned copy for the quote with -n,
checks the computed line falls inside the locator range, checks the quote is at
most 25 words, and checks the entry carries the exact form `quote`(pin:a[-b]).
Exit status 0 only when every check passes.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "hyprland-bind-key-match-r49.md")
PINS = os.path.join(HERE, "pins")

Q = [
    # Hyprland legacy hyprlang bind parser (S353)
    ("Hyprland-legacy-ConfigManager.cpp", "607", 'm_config->registerHandler(&::handleBind, "bind", {true});'),
    ("Hyprland-legacy-ConfigManager.cpp", "1541", 'default: return "bind: invalid flag";'),
    ("Hyprland-legacy-ConfigManager.cpp", "1555", "const auto ARGS     = CVarList(value, numbArgs);"),
    ("Hyprland-legacy-ConfigManager.cpp", "1567", "if (multiKey) {"),
    ("Hyprland-legacy-ConfigManager.cpp", "1483", "return {.keycode = std::stoi(key)};"),
    ("Hyprland-legacy-ConfigManager.cpp", "1484", 'else if (key.starts_with("code:") && isNumber(key.substr(5)))'),
    ("Hyprland-legacy-ConfigManager.cpp", "1489", "return {.key = key};"),
    ("Hyprland-legacy-ConfigManager.cpp", "1617", "SParsedKey parsedKey = parseKey(KEY);"),
    ("Hyprland-legacy-ConfigManager.cpp", "1616", "if ((!KEY.empty()) || multiKey) {"),
    ("Hyprland-legacy-ConfigManager.cpp", "1620", "Catchall not allowed outside of submap!"),
    ("Hyprland-legacy-ConfigManager.cpp", "1603", "Invalid mod, requested mod"),
    ("Hyprland-legacy-ConfigManager.cpp", "1624", "g_pKeybindManager->addKeybind(SKeybind{parsedKey.key,"),
    # Hyprland bind matcher (S352)
    ("Hyprland-KeybindManager.cpp", "710", "const auto KBKEY      = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);"),
    ("Hyprland-KeybindManager.cpp", "711", "const auto KBKEYLOWER = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_CASE_INSENSITIVE);"),
    ("Hyprland-KeybindManager.cpp", "724", "if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)"),
    ("Hyprland-KeybindManager.cpp", "713", "if (KBKEY == XKB_KEY_NoSymbol && KBKEYLOWER == XKB_KEY_NoSymbol) {"),
    ("Hyprland-KeybindManager.cpp", "367", "const auto         KEYCODE = e.keycode + 8;"),
    ("Hyprland-KeybindManager.cpp", "369", "pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState"),
    ("Hyprland-KeybindManager.cpp", "370", "const xkb_keysym_t internalKeysym = xkb_state_key_get_one_sym(pKeyboard->m_xkbState, KEYCODE);"),
    ("Hyprland-KeybindManager.cpp", "377", "handleInternalKeybinds(internalKeysym)"),
    ("Hyprland-KeybindManager.cpp", "928-942", "bool CKeybindManager::handleInternalKeybinds(xkb_keysym_t keysym) {"),
    ("Hyprland-KeybindManager.cpp", "293", "m_xkbTranslationState = nullptr;"),
    ("Hyprland-KeybindManager.cpp", "332", "m_xkbTranslationState = xkb_state_new(PKEYMAP);"),
    ("Hyprland-KeybindManager.cpp", "311", "const auto        PCONTEXT   = xkb_context_new(XKB_CONTEXT_NO_FLAGS);"),
    ("Hyprland-KeybindManager.cpp", "224", 'if (mods.contains("SHIFT"))'),
    ("Hyprland-KeybindManager.cpp", "236", 'if (mods.contains("SUPER") || mods.contains("WIN") || mods.contains("LOGO") || mods.contains("MOD4") || mods.contains("META"))'),
    ("Hyprland-KeybindManager.cpp", "652", "modmask != k->modmask && !k->ignoreMods"),
    ("Hyprland-KeybindManager.cpp", "671", "} else if (!k->sMkKeys.empty() && key.keyName.empty()) {"),
    ("Hyprland-KeybindManager.cpp", "694", "if (key.keyName != k->key)"),
    ("Hyprland-KeybindManager.cpp", "697", "if (key.keycode != k->keycode)"),
    ("Hyprland-KeybindManager.cpp", "699", "} else if (k->catchAll) {"),
    ("Hyprland-KeybindManager.cpp", "189", "m_keybinds.emplace_back(KEYBIND);"),
    ("Hyprland-KeybindManager.cpp", "634", "for (auto& k : m_keybinds) {"),
    ("Hyprland-KeybindManager.cpp", "855", "void CKeybindManager::shadowKeybinds(const xkb_keysym_t& doesntHave, const uint32_t doesntHaveCode) {"),
    ("Hyprland-KeybindManager.cpp", "874", "const auto KBKEYUPPER = xkb_keysym_to_upper(KBKEY);"),
    ("Hyprland-KeybindManager.cpp", "867", 'if (k->handler == "global" || k->transparent)'),
    ("Hyprland-KeybindManager.cpp", "773", "bindsHit.emplace_back(k);"),
    ("Hyprland-KeybindManager.cpp", "728", "if (pressed && k->release && !SPECIALDISPATCHER) {"),
    ("Hyprland-KeybindManager.cpp", "747", "} else if (!k->release && !SPECIALDISPATCHER) {"),
    ("Hyprland-KeybindManager.cpp", "738", "if (key.modmaskAtPressTime != modmask && !k->ignoreMods) {"),
    ("Hyprland-KeybindManager.cpp", "488", 'const auto KEY_NAME = "mouse:" + std::to_string(e.button);'),
    ("Hyprland-KeybindManager.cpp", "461", '{.keyName = "mouse_down"'),
    ("Hyprland-KeybindManager.cpp", "537", '{.keyName = "switch:" + switchName'),
    # libxkbcommon keysym.c (S355)
    ("xkbcommon-keysym.c", "252", "size_t pos = keysym_name_perfect_hash(name);"),
    ("xkbcommon-keysym.c", "268", 'The "best" case-insensitive match is the lower-case keysym name.'),
    ("xkbcommon-keysym.c", "305", "if (*name == 'U' || (icase && *name == 'u')) {"),
    ("xkbcommon-keysym.c", "325", "else if (name[0] == '0' && (name[1] == 'x' || (icase && name[1] == 'X'))) {"),
    ("xkbcommon-keysym.c", "338", 'if (strncmp(name, "XF86_", 5) == 0 ||'),
    # ks_tables.h (S356)
    ("xkbcommon-ks_tables.h", "3", "This file comes from libxkbcommon and was generated by update-keysyms-names-handling.py"),
    # libxkbcommon state.c (S362)
    ("xkbcommon-state.c", "1345", "const xkb_layout_index_t layout = xkb_state_key_get_layout(state, kc);"),
    ("xkbcommon-state.c", "112", "/* If we don't find an explicit match the default is 0. */"),
    ("xkbcommon-state.c", "116", "return (entry) ? entry->level : 0;"),
    ("xkbcommon-state.c", "91", "type->entries[i].mods.mask == mods"),
    # Hyprland InputManager (S354)
    ("Hyprland-InputManager.cpp", "1224", 'getDeviceInt(devname, "resolve_binds_by_sym", "input:resolve_binds_by_sym")'),
    ("Hyprland-InputManager.cpp", "1241", "pKeyboard->m_resolveBindsBySym = RESOLVEBINDSBYSYM;"),
    ("Hyprland-InputManager.cpp", "1711", "m_lastMods         = MODS.depressed;"),
    ("Hyprland-InputManager.cpp", "1887-1889", "uint32_t CInputManager::getModsFromAllKBs() {"),
    # ConfigValues (S318, held)
    ("Hyprland-ConfigValues.cpp", "278", 'MS<Bool>("input:resolve_binds_by_sym", "Determines how keybinds act when multiple layouts are used.", false,'),
    # IKeyboard.cpp (S319, held)
    ("Hyprland-IKeyboard.cpp", "118", "updateXKBTranslationState(m_xkbKeymap);"),
    ("Hyprland-IKeyboard.cpp", "214", "if (keymap) {"),
    ("Hyprland-IKeyboard.cpp", "382", "xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group);"),
    ("Hyprland-IKeyboard.cpp", "422", "xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, m_modifiersState.group);"),
    ("Hyprland-IKeyboard.cpp", "18", "constexpr static std::array<const char*, 8> MODNAMES = {"),
    ("Hyprland-IKeyboard.cpp", "139", "m_modIndexes[i] = xkb_map_mod_get_index(m_xkbKeymap, MODNAMES[i]);"),
    ("Hyprland-IKeyboard.cpp", "360", "uint32_t modMask = m_modifiersState.depressed | m_modifiersState.latched;"),
    # IKeyboard.hpp (S363)
    ("Hyprland-IKeyboard.hpp", "13-22", "HL_MODIFIER_SHIFT = (1 << 0),"),
    ("Hyprland-IKeyboard.hpp", "21", "HL_MODIFIER_MOD5  = (1 << 7),"),
    ("Hyprland-IKeyboard.hpp", "100-101", "same as static but gets layouts"),
    # wiki Binds (S359)
    ("wiki-Binds.md", "40", "for all the keysyms. The name you should use is the segment after"),
    ("wiki-Binds.md", "42", "If you want to bind by a keycode, you can put it in the KEY position with"),
    ("wiki-Binds.md", "49", "This will bind <key>SUPER</key> + <key>t</key> since <key>t</key> is keycode 28."),
    ("wiki-Binds.md", "81", "Cannot be shadowed by other binds."),
    ("wiki-Binds.md", "82", "Will ignore modifiers."),
    ("wiki-Binds.md", "111", 'hl.bind("SUPER + mouse:272", hl.dsp.exec_cmd("amongus"))'),
    ("wiki-Binds.md", "144", "hl.bind(\"switch:on:[switch name]\""),
    ("wiki-Binds.md", "155", "### Multiple binds to one key"),
    ("wiki-Binds.md", "462", "The first layout defined in the input section will be the one used for binds by"),
    ("wiki-Binds.md", "469", "In that case, binds will activate when the symbol"),
    # wiki Variables (S360)
    ("wiki-Variables.md", "219", "If false, keybinds will always act as if the first specified layout is active."),
]


def qwords(q):
    return len(q.split())


def check(pin, loc, quote):
    path = os.path.join(PINS, pin)
    problems = []
    if not os.path.isfile(path):
        return [f"pin missing: {pin}"]
    text = open(path, encoding="utf-8", errors="replace").read().splitlines()
    hits = [i + 1 for i, line in enumerate(text) if quote in line]
    if not hits:
        problems.append(f"quote not found in {pin}: {quote[:60]}")
    else:
        if "-" in loc:
            a, b = (int(x) for x in loc.split("-"))
            ok = [h for h in hits if a <= h <= b]
        else:
            a = int(loc)
            ok = [h for h in hits if h == a]
        if not ok:
            problems.append(f"locator {pin}:{loc} does not cover computed line(s) {hits}")
    if qwords(quote) > 25:
        problems.append(f"quote longer than 25 words ({qwords(quote)}): {quote[:60]}")
    return problems, hits


def main():
    entry = open(ENTRY, encoding="utf-8").read()
    bad = 0
    for pin, loc, quote in Q:
        res = check(pin, loc, quote)
        if isinstance(res, list):
            problems, hits = res, []
        else:
            problems, hits = res
        form = "`%s`(%s:%s)" % (quote, pin, loc)
        if form not in entry:
            problems.append("entry does not carry the form %s" % form[:100])
        status = "PASS" if not problems else "FAIL"
        if problems:
            bad += 1
        print("%s %s:%s hits=%s w=%d %s" % (status, pin, loc, hits, qwords(quote), quote[:52]))
        for p in problems:
            print("      " + p)
    print("\n%d quotes checked, %d failed" % (len(Q), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
