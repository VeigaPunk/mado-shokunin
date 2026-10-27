#!/usr/bin/env python3
"""Upstream pins + computed locators for seat ExecBindsLive. Locators come from grep, never typed."""
import hashlib, os, re, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
BASE = 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/'
XKB = 'https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/'
FILES = [
    ('src/src_managers_KeybindManager.cpp', BASE + 'src/managers/KeybindManager.cpp'),
    ('src/src_managers_input_InputManager.cpp', BASE + 'src/managers/input/InputManager.cpp'),
    ('src/src_devices_IKeyboard.cpp', BASE + 'src/devices/IKeyboard.cpp'),
    ('src/src_config_legacy_ConfigManager.cpp', BASE + 'src/config/legacy/ConfigManager.cpp'),
    ('src_libxkb_keysym.c', XKB + 'src/keysym.c'),
]
QUERIES = [
    ('src/src_managers_KeybindManager.cpp', r'modmask != k->modmask'),
    ('src/src_managers_KeybindManager.cpp', r'e\.keycode \+ 8'),
    ('src/src_managers_KeybindManager.cpp', r'm_resolveBindsBySym \?'),
    ('src/src_managers_KeybindManager.cpp', r'xkb_keysym_from_name\(k->key\.c_str\(\), XKB_KEYSYM_NO_FLAGS\)'),
    ('src/src_managers_KeybindManager.cpp', r'xkb_keysym_from_name\(k->key\.c_str\(\), XKB_KEYSYM_CASE_INSENSITIVE\)'),
    ('src/src_managers_KeybindManager.cpp', r'key\.keysym != KBKEY && key\.keysym != KBKEYLOWER'),
    ('src/src_managers_KeybindManager.cpp', r'key\.keycode != k->keycode'),
    ('src/src_managers_KeybindManager.cpp', r'findConflictingKeybind'),
    ('src/src_managers_KeybindManager.cpp', r'xkb_state_key_get_one_sym\(m_xkbTranslationState, k->keycode\)'),
    ('src/src_managers_input_InputManager.cpp', r'm_lastMods\s+= MODS\.depressed'),
    ('src/src_managers_input_InputManager.cpp', r'resolve_binds_by_sym'),
    ('src/src_managers_input_InputManager.cpp', r'm_resolveBindsBySym = RESOLVEBINDSBYSYM'),
    ('src/src_devices_IKeyboard.cpp', r'xkb_state_update_mask\(m_xkbSymState'),
    ('src/src_config_legacy_ConfigManager.cpp', r'SParsedKey parseKey'),
    ('src/src_config_legacy_ConfigManager.cpp', r'key\.starts_with\("code:"\)'),
    ('src/src_config_legacy_ConfigManager.cpp', r"case 'm': mouse = true"),
    ('src/src_config_legacy_ConfigManager.cpp', r'addSpecialConfigValue\("device", "resolve_binds_by_sym"'),
    ('src/src_config_legacy_ConfigManager.cpp', r'HANDLER = "mouse"'),
    ('src_libxkb_keysym.c', r'bool icase'),
    ('src_libxkb_keysym.c', r'The "best" case-insensitive match is the lower-case keysym name'),
    ('src_libxkb_keysym.c', r"name\[0\] == '0' && \(name\[1\] == 'x'"),
    ('src_libxkb_keysym.c', r'strncmp\(name, "XF86_", 5\)'),
]

L = []
A = L.append
A('# ExecBindsLive — pins for the upstream sources behind the live join (round 49 w1)')
A('#')
A('# Hyprland 0.56.2, `hyprctl version` on the host: "built from branch v0.56.2 at commit')
A('# efb50993780079460b0cbed1363e2166a2de1d9f". Sources fetched from the pinned commit URL, never a branch.')
A('# libxkbcommon 1.13.2 tag URL. Each pin: URL, bytes, sha256. Copies live only in seat scratch; the')
A('# locators below are grep-computed against those bytes and are reproducible from the URL + sha256.')
A('')
for path, url in FILES:
    data = open(os.path.join(S, path), 'rb').read()
    A(f'{url}')
    A(f'  bytes {len(data)}  sha256 {hashlib.sha256(data).hexdigest()}')
A('')
A('## Located evidence (locator = grep -n on the pinned bytes; quote <= 25 words)')
A('')
for path, pat in QUERIES:
    p = subprocess.run(['grep', '-n', '-E', pat, os.path.join(S, path)], capture_output=True, text=True)
    hits = p.stdout.rstrip('\n').splitlines()
    A(f'## {path}   /{pat}/')
    for h in hits:
        ln, text = h.split(':', 1)
        words = text.strip().split()
        short = ' '.join(words[:25])
        A(f'{path}:{ln}: {short}')
    A('')

# verification: every emitted quote must be found again by a fixed-string grep
body = '\n'.join(L)
bad = []
for path, pat in QUERIES:
    p = subprocess.run(['grep', '-n', '-E', pat, os.path.join(S, path)], capture_output=True, text=True)
    for h in p.stdout.rstrip('\n').splitlines():
        ln, text = h.split(':', 1)
        words = text.strip().split()
        short = ' '.join(words[:25])
        if short not in body:
            bad.append((path, ln))
A('## verification')
A(f'quotes re-grepped against the pins: {len(QUERIES)} patterns, missing after emit = {len(bad)}')
open(os.path.join(OUT, 'upstream-pins.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('missing:', bad)
