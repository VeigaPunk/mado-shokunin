#!/usr/bin/env python3
"""CritEntryContent: recompute every locator the C2 draft and its OBS block claim.

Each row: (label, file, claimed-lines, needle). needle is grepped literally in the
pinned file; the printed line is COMPUTED by grep, never typed. A needle that spans
a newline cannot match (grep works line by line), which is exactly the test applied
to the two OBS quotes that were written as reflowed sentences.
"""
import re
import sys
from pathlib import Path

FETCH = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch")

# (label, file, claimed range, needle, expectation)
# expectation: "in" = needle must occur inside the claimed range,
#              "any" = needle must occur somewhere (line reported for comparison)
ROWS = [
    ("step1 continuation", "hyprlang-config.cpp", (44, 66), "static std::expected<std::string, eGetNextLineFailure> getNextLine", "in"),
    ("step1 continuation append", "hyprlang-config.cpp", (44, 66), "line += nextLine;", "in"),
    ("step1 ## collapse", "hyprlang-config.cpp", (674, 700), "line       = line.substr(0, commentPos + 1) + line.substr(commentPos + 2);", "in"),
    ("step1 ## escaped flag", "hyprlang-config.cpp", (674, 700), "escaped     = true;", "in"),
    ("step1 valueName join", "hyprlang-config.cpp", (0, 0), "valueName += c + ':';", "any"),
    ("step2 device category", "Hyprland-ConfigManager.cpp", (518, 540), 'addSpecialCategory("device", {"name"});', "in"),
    ("step2 device first value", "Hyprland-ConfigManager.cpp", (518, 540), 'addSpecialConfigValue("device", "sensitivity", {0.F});', "in"),
    ("step2 device last value", "Hyprland-ConfigManager.cpp", (518, 540), 'addSpecialConfigValue("device", "pressure_range_max", Hyprlang::FLOAT{-1.0});', "in"),
    ("step2 bracket cut", "hyprlang-config.cpp", (291, 320), "const auto CATKEY       = valueName.substr(L + 1, R - L - 1);", "in"),
    ("step2 bracket setFrom", "hyprlang-config.cpp", (291, 320), "PCAT->values[sc->key].setFrom(CATKEY);", "in"),
    ("step2 category push (block form)", "hyprlang-config.cpp", (0, 0), "impl->categories.push_back(line);", "any"),
    ("step2 first-value error", "hyprlang-config.cpp", (420, 440), "special category's first value must be the key.", "in"),
    ("step2 reset on last close", "hyprlang-config.cpp", (885, 899), 'impl->currentSpecialKey      = "";', "in"),
    ("step2 reset null", "hyprlang-config.cpp", (885, 899), "impl->currentSpecialCategory = nullptr;", "in"),
    ("step2 merge existing key", "hyprlang-config.cpp", (0, 0), "existingKeyValue != impl->currentSpecialKey", "any"),
    ("step3 six names first", "Hyprland-InputManager.cpp", (1213, 1238), 'getDeviceString(devname, "kb_file", "input:kb_file");', "in"),
    ("step3 six names last", "Hyprland-InputManager.cpp", (1213, 1238), 'getDeviceString(devname, "kb_options", "input:kb_options");', "in"),
    ("step3 layout lookup", "Hyprland-InputManager.cpp", (1226, 1231), 'getDeviceString(devname, "kb_layout", "input:kb_layout");', "in"),
    ("step3 join key is hlName", "Hyprland-InputManager.cpp", (0, 0), "auto       devname = pKeyboard->m_hlName;", "any"),
    ("step3 set-by-user test", "Hyprland-ConfigManager.cpp", (1115, 1123), "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())", "in"),
    ("step3 deviceConfigExists", "Hyprland-ConfigManager.cpp", (1196, 1201), "return m_config->specialCategoryExistsForKey(\"device\", copy.c_str());", "in"),
    ("step3 deviceConfigExists space", "Hyprland-ConfigManager.cpp", (1196, 1201), "std::ranges::replace(copy, ' ', '-');", "in"),
    ("step3 EMPTY marker read", "Hyprland-ConfigManager.cpp", (1156, 1168), "if (VAL == STRVAL_EMPTY)", "in"),
    ("step3 default layout", "Hyprland-ConfigValues.cpp", (271, 276), 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",', "in"),
    ("step3 default rest", "Hyprland-ConfigValues.cpp", (271, 276), 'MS<String>("input:kb_rules", "Appropriate XKB keymap parameter", STRVAL_EMPTY,', "in"),
    ("step3 did not change", "Hyprland-InputManager.cpp", (1270, 1280), "Not applying config to keyboard, it did not change.", "in"),
    ("step4 setKeymap call", "Hyprland-InputManager.cpp", (1282, 1295), "pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});", "in"),
    ("step4 kb_file order", "Hyprland-IKeyboard.cpp", (87, 96), "if (!m_xkbFilePath.empty()) {", "in"),
    ("step4 kb_file file read", "Hyprland-IKeyboard.cpp", (87, 96), "m_xkbKeymap = xkb_keymap_new_from_file(CONTEXT, KEYMAPFILE, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS);", "in"),
    ("step4 names fallback", "Hyprland-IKeyboard.cpp", (87, 96), "xkb_keymap_new_from_names2(CONTEXT, &XKBRULES, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS);", "in"),
    ("step4 kb_file relative", "Hyprland-IKeyboard.cpp", (0, 0), "absolutePath(m_xkbFilePath, Config::mgr()->currentConfigPath());", "any"),
    ("step4 fallback overlay", "Hyprland-IKeyboard.cpp", (101, 116), "Invalid keyboard layout passed.", "in"),
    ("step4 fallback layout us", "Hyprland-IKeyboard.cpp", (101, 116), 'm_currentRules.layout  = "us";', "in"),
    ("step5 mouse fields", "Hyprland-HyprCtl.cpp", (765, 772), '"scrollFactor": {:.2f}', "in"),
    ("step5 keyboard rules", "Hyprland-HyprCtl.cpp", (785, 802), '"rules": "{}",', "in"),
    ("step5 keyboard options", "Hyprland-HyprCtl.cpp", (785, 802), '"options": "{}",', "in"),
    ("step5 active_keymap", "Hyprland-HyprCtl.cpp", (785, 802), '"active_keymap": "{}",', "in"),
    ("step5 main field", "Hyprland-HyprCtl.cpp", (785, 802), '"main": {}', "in"),
    ("step5 capsLock field", "Hyprland-HyprCtl.cpp", (785, 802), '"capsLock": {},', "in"),
    ("step5 scroll clamp", "Hyprland-InputManager.cpp", (1376, 1383), "if (Config::mgr()->deviceConfigExplicitlySet(devname, \"scroll_factor\"))", "in"),
    ("step5 scroll clamp arg", "Hyprland-InputManager.cpp", (1376, 1383), 'getDeviceFloat(devname, "scroll_factor", "input:scroll_factor"), 0.F, 100.F', "in"),
    ("step5 scroll nullopt", "Hyprland-InputManager.cpp", (1379, 1383), "m->m_scrollFactor = std::nullopt;", "in"),
    ("step5 global scroll", "Hyprland-ConfigValues.cpp", (290, 300), 'MS<Float>("input:scroll_factor", "Multiplier added to scroll movement for external mice.", 1, {.min = 0, .max = 2,', "in"),
    ("step6 vk prefix", "Hyprland-protocols-VirtualKeyboard.cpp", (11, 30), 'std::string name = "hl-virtual-keyboard";', "in"),
    ("step6 vk option", "Hyprland-protocols-VirtualKeyboard.cpp", (11, 30), 'CConfigValue<Config::INTEGER>("misc:name_vk_after_proc");', "in"),
    ("step6 vk early return", "Hyprland-protocols-VirtualKeyboard.cpp", (11, 30), "if (!*PVKNAMEPROC)", "in"),
    ("step6 vk unknown", "Hyprland-protocols-VirtualKeyboard.cpp", (11, 30), 'name += "unknown";', "in"),
    ("step6 vk option default", "Hyprland-ConfigValues.cpp", (0, 0), 'MS<Bool>("misc:name_vk_after_proc", "Name virtual keyboards after the processes that create them.", true),', "any"),
    ("step6 override flag", "Hyprland-VirtualKeyboard.cpp", (36, 44), "m_keymapOverridden = true;", "in"),
    ("step6 override early return", "Hyprland-IKeyboard.cpp", (60, 64), "Ignoring setKeymap: keymap is overridden", "in"),
    ("step6 currentRules assignment", "Hyprland-IKeyboard.cpp", (0, 0), "m_currentRules          = rules;", "any"),
    ("step7 normalizer signature", "Hyprland-MiscFunctions.cpp", (777, 789), "std::string deviceNameToInternalString(const std::string& in) {", "in"),
    ("step7 comma", "Hyprland-MiscFunctions.cpp", (777, 789), "case ',': return '-';", "in"),
    ("step7 lower", "Hyprland-MiscFunctions.cpp", (777, 789), "default: return sc<char>(std::tolower(ch));", "in"),
    ("step7 duplicate suffix", "Hyprland-InputManager.cpp", (2119, 2131), "auto makeNewName = [&]() { return (proposedNewName.empty() ? \"unknown-device\" : proposedNewName) + (dupeno == 0 ? \"\" : (\"-\" + std::to_string(dupeno))); };", "in"),
    ("step7 dedupe domain", "Hyprland-InputManager.cpp", (2119, 2131), "[&](const auto& other) { return other->m_hlName == makeNewName(); }) != m_hids.end())", "in"),
    ("step7 wiki copy", "wiki-Keywords.md", (79, 79), 'The `name` can be easily obtained by checking the output of `hyprctl devices`.', "in"),
    ("step7 wiki override", "wiki-Keywords.md", (64, 70), "ONLY values explicitly changed will be", "in"),
    ("step7 wiki block open", "wiki-Keywords.md", (73, 74), "device {", "in"),
    ("step7 wiki normalized example", "wiki-Keywords.md", (110, 111), "name = royuan-akko-multi-modes-keyboard-b", "in"),
    ("main flag read", "Hyprland-HyprCtl.cpp", (0, 0), '(k->m_active ? "true" : "false")', "any"),
    ("main flag switchxkblayout", "Hyprland-HyprCtl.cpp", (0, 0), 'if (KB == "main" || KB == "active" || KB == "current") {', "any"),
    ("main flag cleared", "Hyprland-InputManager.cpp", (0, 0), "k->m_active = false;", "any"),
    ("main flag clear caller", "Hyprland-InputManager.cpp", (0, 0), "disableAllKeyboards(false);", "any"),
    ("config errors stored", "Hyprland-ConfigManager.cpp", (0, 0), "m_configErrors = result.getError();", "any"),
    ("keyword handler", "Hyprland-HyprCtl.cpp", (0, 0), 'registerCommand(SHyprCtlCommand{"keyword", false, dispatchKeyword});', "any"),
]

# Quotes the OBS block writes as one line: these MUST match a single pinned line.
OBS_QUOTES = [
    ("S316", "Hyprland-InputManager.cpp", 1229, 'const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");'),
    ("S317", "Hyprland-ConfigManager.cpp", 1119, "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"),
    ("S318", "Hyprland-ConfigValues.cpp", 272, 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",'),
    ("S319", "Hyprland-IKeyboard.cpp", 113, 'm_currentRules.layout = "us";'),
    ("S320", "Hyprland-HyprCtl.cpp", 769, '"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}'),
    ("S321", "Hyprland-MiscFunctions.cpp", 782, "case ',': return '-';"),
    ("S322", "Hyprland-VirtualKeyboard.cpp", 41, "m_keymapOverridden = true;"),
    ("S323", "Hyprland-protocols-VirtualKeyboard.cpp", 12, 'std::string name = "hl-virtual-keyboard";'),
    ("S324", "hyprlang-config.cpp", 435, "special category's first value must be the key."),
    ("S325", "wiki-Keywords.md", 67, "It's worth noting that ONLY values explicitly changed will be overwritten."),
]

DEVICE_KEYS_FILE = "Hyprland-ConfigManager.cpp"


def lines_of(name):
    return (FETCH / name).read_text(errors="replace").splitlines()


def grep_all(name, needle):
    return [i + 1 for i, line in enumerate(lines_of(name)) if needle in line]


def main():
    out = []
    out.append("CRIT-ENTRY-CONTENT: locator and quote recomputation")
    out.append("pins: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch/")
    out.append("")

    out.append("## 1. claimed locators")
    bad = 0
    for label, name, (lo, hi), needle, expect in ROWS:
        hits = grep_all(name, needle)
        if expect == "any":
            verdict = "PRESENT" if hits else "ABSENT"
            where = ",".join(str(h) for h in hits) or "-"
        else:
            inside = [h for h in hits if lo <= h <= hi]
            verdict = "IN" if inside else ("OUT" if hits else "ABSENT")
            where = ",".join(str(h) for h in hits) or "-"
            if verdict != "IN":
                bad += 1
        out.append(f"{label}: {name}:{lo}-{hi} needle-hits={where} -> {verdict}")
    out.append("")
    out.append(f"locators out of range: {bad}")
    out.append("")

    out.append("## 2. OBS quotes against the claimed single line")
    for tag, name, claimed, quote in OBS_QUOTES:
        hits = grep_all(name, quote)
        single = claimed in hits
        out.append(f"{tag}: claimed {name}:{claimed} quote-grep-hits={','.join(str(h) for h in hits) or 'NONE'} -> {'SINGLE-LINE-OK' if single else 'NOT-ONE-LINE'}")
    out.append("")

    out.append("## 3. device special-category value count")
    dev = [i + 1 for i, line in enumerate(lines_of(DEVICE_KEYS_FILE)) if 'addSpecialConfigValue("device"' in line]
    out.append(f"addSpecialConfigValue(\"device\", ...) calls: {len(dev)} at {DEVICE_KEYS_FILE}:{dev[0]}-{dev[-1]} (contiguous={dev == list(range(dev[0], dev[-1] + 1))})")
    out.append("")
    out.append("## 4. host reads used for counterexamples (read-only, projected)")
    out.append("hyprctl version -> 0.56.2 built from v0.56.2 at efb50993780079460b0cbed1363e2166a2de1d9f")
    out.append("hyprctl devices -j cross-tab (is_virtual_keyboard, main): {(False, False): 9, (True, True): 1}")
    out.append("hyprctl devices -j distinct (layout, active_keymap, active_layout_index, rules, model, variant, options):")
    out.append("  ('br', 'Portuguese (Brazil)', 0, '', '', '', 'compose:caps') x 10 keyboards")
    out.append("hyprctl devices -j keyboard fields: active_keymap, active_layout_index, address, capsLock, layout, main, model, name, numLock, options, rules, variant")
    out.append("hyprctl devices -j mice fields: address, defaultSpeed, name, scrollFactor")
    out.append("no device name, window title, serial or home path appears above")
    text = "\n".join(out) + "\n"
    outdir = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/CritEntryContent")
    (outdir / "locators.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
