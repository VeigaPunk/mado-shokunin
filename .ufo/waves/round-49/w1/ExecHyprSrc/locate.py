#!/usr/bin/env python3
"""Compute every locator used by trace.md from the pinned bytes.

Each entry names a regex that must match exactly one (or the nth) line of the
pinned file; the recorded quote must be a verbatim substring of that line.
Writes locators.json, which verify-quotes.py re-checks by line number.
Run from this directory: python3 locate.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FETCH = HERE / "fetch"

# (id, file, regex, quote, nth)
ENTRIES = [
    # ---- config plane: the bind line into SKeybind
    ("C01", "Hyprland-ConfigManager.cpp", r'registerHandler\(&::handleBind, "bind"', 'registerHandler(&::handleBind, "bind", {true});', 1),
    ("C02", "Hyprland-ConfigManager.cpp", r"Config::Legacy::mgr\(\)->handleBind\(COMMAND, VALUE\)", "Config::Legacy::mgr()->handleBind(COMMAND, VALUE);", 1),
    ("C03", "Hyprland-ConfigManager.cpp", r"CConfigManager::handleBind\(const std::string& command", "CConfigManager::handleBind(const std::string& command, const std::string& value)", 1),
    ("C04", "Hyprland-ConfigManager.cpp", r"^SParsedKey parseKey\(const std::string& key\)", "SParsedKey parseKey(const std::string& key)", 1),
    ("C05", "Hyprland-ConfigManager.cpp", r"isNumber\(key\) && std::stoi\(key\) > 9", "if (isNumber(key) && std::stoi(key) > 9)", 1),
    ("C06", "Hyprland-ConfigManager.cpp", r'key\.starts_with\("code:"\)', 'key.starts_with("code:") && isNumber(key.substr(5))', 1),
    ("C07", "Hyprland-ConfigManager.cpp", r'key == "catchall"', 'else if (key == "catchall")', 1),
    ("C08", "Hyprland-ConfigManager.cpp", r"stringToModMask\(ARGS\[0\]\)", "g_pKeybindManager->stringToModMask(ARGS[0]);", 1),
    ("C09", "Hyprland-ConfigManager.cpp", r"KEYSYMS\.emplace_back", "KEYSYMS.emplace_back(xkb_keysym_from_name(splitKey.c_str(), XKB_KEYSYM_CASE_INSENSITIVE), 0);", 1),
    ("C10", "Hyprland-ConfigManager.cpp", r"case 'i': ignoreMods", "case 'i': ignoreMods = true; break;", 1),
    ("C11", "Hyprland-ConfigManager.cpp", r"Invalid catchall", "catchall keybinds are only allowed in submaps.", 1),
    ("C12", "Hyprland-ConfigManager.cpp", r"addKeybind\(SKeybind", "g_pKeybindManager->addKeybind(SKeybind{parsedKey.key,", 1),
    ("C13", "Hyprland-ConfigManager.cpp", r'addSpecialConfigValue\("device", "resolve_binds_by_sym"', 'addSpecialConfigValue("device", "resolve_binds_by_sym", Hyprlang::INT{0});', 1),
    ("C14", "Hyprland-ConfigValues.cpp", r"resolve_binds_by_sym", 'MS<Bool>("input:resolve_binds_by_sym", "Determines how keybinds act when multiple layouts are used."', 1),
    ("C15", "Hyprland-InputManager.cpp", r'getDeviceInt\(devname, "resolve_binds_by_sym"', 'getDeviceInt(devname, "resolve_binds_by_sym", "input:resolve_binds_by_sym");', 1),
    ("C16", "Hyprland-InputManager.cpp", r"m_resolveBindsBySym = RESOLVEBINDSBYSYM", "pKeyboard->m_resolveBindsBySym = RESOLVEBINDSBYSYM;", 1),
    ("C17", "Hyprland-KeybindManager.hpp", r"^using KeybindKey", "using KeybindKey = std::pair<xkb_keysym_t, xkb_keycode_t>;", 1),
    ("C18", "Hyprland-KeybindManager.hpp", r"^struct SKeybind \{", "struct SKeybind {", 1),
    # ---- key event path
    ("K01", "Hyprland-Keyboard.cpp", r"m_keyboardEvents\.key\.emit", "m_keyboardEvents.key.emit(SKeyEvent{", 1),
    ("K02", "Hyprland-Keyboard.cpp", r"updateXkbStateWithKey\(event\.key \+ 8", "updateXkbStateWithKey(event.key + 8, event.pressed);", 1),
    ("K03", "Hyprland-InputManager.cpp", r"onKeyEvent\(event, pKeyboard\)", "g_pKeybindManager->onKeyEvent(event, pKeyboard)", 1),
    ("K04", "Hyprland-KeybindManager.cpp", r"^bool CKeybindManager::onKeyEvent", "bool CKeybindManager::onKeyEvent(std::any event, SP<IKeyboard> pKeyboard) {", 1),
    ("K05", "Hyprland-KeybindManager.cpp", r"e\.keycode \+ 8;", "e.keycode + 8; // Because to xkbcommon it's +8 from libinput", 1),
    ("K06", "Hyprland-KeybindManager.cpp", r"m_resolveBindsBySym \? pKeyboard->m_xkbSymState", "xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);", 1),
    ("K07", "Hyprland-KeybindManager.cpp", r"internalKeysym = xkb_state_key_get_one_sym", "xkb_state_key_get_one_sym(pKeyboard->m_xkbState, KEYCODE);", 1),
    ("K08", "Hyprland-KeybindManager.cpp", r"handleInternalKeybinds\(internalKeysym\)", "handleInternalKeybinds(internalKeysym)", 1),
    ("K09", "Hyprland-KeybindManager.cpp", r"const auto MODS = g_pInputManager->getModsFromAllKBs\(\);", "const auto MODS = g_pInputManager->getModsFromAllKBs();", 1),
    ("K10", "Hyprland-KeybindManager.cpp", r"const auto KEY = SPressedKeyWithMods\{", "const auto KEY = SPressedKeyWithMods{", 1),
    ("K11", "Hyprland-KeybindManager.cpp", r"\.keysym             = keysym,", ".keysym             = keysym,", 1),
    ("K12", "Hyprland-KeybindManager.cpp", r"handleKeybinds\(MODS, KEY, true, pKeyboard, pKeyboard\)", "handleKeybinds(MODS, KEY, true, pKeyboard, pKeyboard).passEvent;", 1),
    ("K13", "Hyprland-KeybindManager.cpp", r"^SDispatchResult CKeybindManager::handleKeybinds", "SDispatchResult CKeybindManager::handleKeybinds(const uint32_t modmask", 1),
    ("K14", "Hyprland-KeybindManager.cpp", r"modmask != k->modmask", "modmask != k->modmask && !k->ignoreMods", 1),
    ("K15", "Hyprland-KeybindManager.cpp", r"sMkKeys\.empty\(\) && key\.keyName\.empty\(\)", "!k->sMkKeys.empty() && key.keyName.empty()", 1),
    ("K16", "Hyprland-KeybindManager.cpp", r"key\.keyName != k->key", "if (key.keyName != k->key)", 1),
    ("K17", "Hyprland-KeybindManager.cpp", r"key\.keycode != k->keycode", "if (key.keycode != k->keycode)", 1),
    ("K18", "Hyprland-KeybindManager.cpp", r"else if \(k->catchAll\)", "} else if (k->catchAll) {", 1),
    ("K19", "Hyprland-KeybindManager.cpp", r"key\.keysym == XKB_KEY_NoSymbol", "if (key.keysym == XKB_KEY_NoSymbol)", 1),
    ("K20", "Hyprland-KeybindManager.cpp", r"XKB_KEYSYM_NO_FLAGS\);", "xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);", 1),
    ("K21", "Hyprland-KeybindManager.cpp", r"XKB_KEYSYM_CASE_INSENSITIVE\);", "xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_CASE_INSENSITIVE);", 2),
    ("K22", "Hyprland-KeybindManager.cpp", r"key\.keysym != KBKEY", "if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)", 1),
    ("K23", "Hyprland-KeybindManager.cpp", r"^uint32_t CKeybindManager::stringToModMask", "uint32_t CKeybindManager::stringToModMask(std::string mods) {", 1),
    ("K24", "Hyprland-KeybindManager.cpp", r"::toupper\);", "std::ranges::transform(mods, mods.begin(), ::toupper);", 1),
    ("K25", "Hyprland-KeybindManager.cpp", r'mods\.contains\("SUPER"\)', 'mods.contains("SUPER")', 1),
    ("K26", "Hyprland-KeybindManager.cpp", r"^void CKeybindManager::updateXKBTranslationState", "void CKeybindManager::updateXKBTranslationState() {", 1),
    ("K27", "Hyprland-KeybindManager.cpp", r"xkb_keymap_new_from_names2\(PCONTEXT, &rules", "xkb_keymap_new_from_names2(PCONTEXT, &rules, XKB_KEYMAP_FORMAT_TEXT_V2,", 1),
    ("K28", "Hyprland-KeybindManager.cpp", r"m_xkbTranslationState = xkb_state_new\(PKEYMAP\)", "m_xkbTranslationState = xkb_state_new(PKEYMAP);", 1),
    ("K35", "Hyprland-KeybindManager.cpp", r'CConfigValue<std::string>\("input:kb_file"\)', 'CConfigValue<std::string>("input:kb_file");', 1),
    ("K29", "Hyprland-KeybindManager.cpp", r'"mouse:" \+ std::to_string', 'const auto KEY_NAME = "mouse:" + std::to_string(e.button);', 1),
    ("K30", "Hyprland-KeybindManager.cpp", r'"switch:on:" \+ switchName', '.keyName = "switch:on:" + switchName', 1),
    ("K31", "Hyprland-KeybindManager.cpp", r'keyName = "mouse_down"', '.keyName = "mouse_down"', 1),
    ("K32", "Hyprland-KeybindManager.cpp", r"m_mkKeys\.emplace", "m_mkKeys.emplace(key.keysym, key.keycode);", 1),
    ("K33", "Hyprland-KeybindManager.cpp", r"^void CKeybindManager::shadowKeybinds", "void CKeybindManager::shadowKeybinds(", 1),
    ("K34", "Hyprland-KeybindManager.cpp", r"for \(const auto& k : bindsHit\)", "for (const auto& k : bindsHit) {", 1),
    # ---- modifier model
    ("M01", "Hyprland-IKeyboard.hpp", r"HL_MODIFIER_SHIFT = \(1 << 0\)", "HL_MODIFIER_SHIFT = (1 << 0),", 1),
    ("M02", "Hyprland-IKeyboard.hpp", r"m_xkbSymState    = nullptr;", "// same as static but gets layouts", 1),
    ("M03", "Hyprland-IKeyboard.hpp", r"m_resolveBindsBySym = false;", "m_resolveBindsBySym = false;", 1),
    ("M04", "Hyprland-IKeyboard.cpp", r"^uint32_t IKeyboard::getModifiers", "uint32_t IKeyboard::getModifiers() {", 1),
    ("M05", "Hyprland-IKeyboard.cpp", r"m_modifiersState\.depressed \| m_modifiersState\.latched", "m_modifiersState.depressed | m_modifiersState.latched;", 1),
    ("M06", "Hyprland-IKeyboard.cpp", r"m_modIndexes\[i\] = xkb_map_mod_get_index", "m_modIndexes[i] = xkb_map_mod_get_index(m_xkbKeymap, MODNAMES[i]);", 1),
    ("M07", "Hyprland-IKeyboard.cpp", r"XKB_MOD_NAME_SHIFT, XKB_MOD_NAME_CAPS", "XKB_MOD_NAME_SHIFT, XKB_MOD_NAME_CAPS, XKB_MOD_NAME_CTRL, XKB_MOD_NAME_ALT", 1),
    ("M08", "Hyprland-IKeyboard.cpp", r"xkb_state_update_mask\(m_xkbSymState, 0, 0, 0, 0, 0, group\)", "xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group);", 1),
    ("M09", "Hyprland-IKeyboard.cpp", r"xkb_state_update_mask\(m_xkbSymState, 0, 0, 0, 0, 0, m_modifiersState\.group\)", "xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, m_modifiersState.group);", 1),
    ("M10", "Hyprland-InputManager.cpp", r"const auto ALLMODS = shareModsFromAllKBs", "const auto ALLMODS = shareModsFromAllKBs(MODS.depressed);", 1),
    ("M11", "Hyprland-InputManager.cpp", r"for hyprland keybinds use", "MODS.depressed; // for hyprland keybinds use; not for sending to seat", 1),
    ("M12", "Hyprland-InputManager.cpp", r"^uint32_t CInputManager::getModsFromAllKBs", "uint32_t CInputManager::getModsFromAllKBs() {", 1),
    # ---- IPC surface
    ("H01", "Hyprland-HyprCtl.cpp", r"modmask: \{\}", "modmask: {}", 1),
    ("H02", "Hyprland-HyprCtl.cpp", r'"modmask": \{\},', '"modmask": {},', 1),
    ("H03", "Hyprland-HyprCtl.cpp", r'"key": "\{\}",', '"key": "{}",', 1),
    # ---- Lua config shares SKeybind
    ("L01", "Hyprland-LuaKeybind.cpp", r"^void Objects::CLuaKeybind::push", "void Objects::CLuaKeybind::push(lua_State* L, const SP<SKeybind>& keybind) {", 1),
    ("L02", "Hyprland-LuaKeybind.cpp", r"new \(lua_newuserdata", "new (lua_newuserdata(L, sizeof(WP<SKeybind>))) WP<SKeybind>(keybind);", 1),
    # ---- libxkbcommon: name resolution and state semantics
    ("X01", "xkbcommon-keysym.c", r"bool icase = \(flags & XKB_KEYSYM_CASE_INSENSITIVE\)", "bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);", 1),
    ("X02", "xkbcommon-keysym.c", r"best.*case-insensitive match is the lower-case", "The \"best\" case-insensitive match is the lower-case keysym name.", 1),
    ("X03", "xkbcommon-keysym.c", r"if \(\*name == 'U'", "if (*name == 'U' || (icase && *name == 'u')) {", 1),
    ("X04", "xkbcommon-xkbcommon.h", r"This function performs Capitalization @ref keysym-transformations\.", "This function performs Capitalization @ref keysym-transformations.", 1),
    ("X05", "xkbcommon-xkbcommon.h", r"^xkb_state_update_mask\(struct xkb_state", "xkb_state_update_mask(struct xkb_state *state,", 1),
    ("X06", "xkbcommon-xkbcommon.h", r"Get the single keysym obtained from pressing a particular key", "Get the single keysym obtained from pressing a particular key in a", 1),
    ("X07", "xkbcommon-how-to-type.c", r"xkb_keymap_key_get_mods_for_level\(", "xkb_keymap_key_get_mods_for_level(", 1),
    ("X08", "xkbcommon-how-to-type.c", r'printf\("%-8u %-9s %-8u %-20s %-7u \[ "', 'printf("%-8u %-9s %-8u %-20s %-7u [ ",', 1),
]


def main() -> int:
    out = []
    bad = []
    for eid, fname, pattern, quote, nth in ENTRIES:
        path = FETCH / fname
        if not path.is_file():
            bad.append((eid, f"missing pin {fname}"))
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [i + 1 for i, line in enumerate(lines) if re.search(pattern, line)]
        if len(hits) < nth:
            bad.append((eid, f"{fname}: pattern {pattern!r} matched {len(hits)} line(s), wanted #{nth}"))
            continue
        lineno = hits[nth - 1]
        line = lines[lineno - 1]
        if quote not in line:
            bad.append((eid, f"{fname}:{lineno} does not contain quote {quote!r}; line={line!r}"))
            continue
        words = len(quote.split())
        if words > 25:
            bad.append((eid, f"quote is {words} words (> 25)"))
            continue
        out.append({"id": eid, "file": fname, "line": lineno, "quote": quote, "words": words})

    (HERE / "locators.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for rec in out:
        print(f"{rec['id']} {rec['file']}:{rec['line']} words={rec['words']}")
    print(f"LOCATED {len(out)}/{len(ENTRIES)}")
    for eid, msg in bad:
        print(f"FAIL {eid}: {msg}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
