#!/usr/bin/env python3
"""Reachability receipt for seat ExecBindsLive: does each live bind fire on the host keymap?

Method: build an xkb_state from the compiled host keymap, set depressed mods = the bind's modmask
(Hyprland's modmask uses the XKB real modifier bit positions, 1 Shift .. 128 Mod5), then read
xkb_state_key_get_one_sym for every keycode. Hyprland accepts a press whose keysym equals either
xkb_keysym_from_name(key, NO_FLAGS) or xkb_keysym_from_name(key, CASE_INSENSITIVE) (KeybindManager.cpp:710-724)
and requires depressed mods == modmask (KeybindManager.cpp:652, InputManager.cpp:1711).
"""
import ctypes, json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
KEYMAP = os.path.join(S, 'keymap-br.xkb')

MODBITS = [(1, 'Shift'), (2, 'Lock'), (4, 'Control'), (8, 'Mod1', 'Alt'), (16, 'Mod2', 'NumLock'),
           (32, 'Mod3'), (64, 'Mod4', 'Super'), (128, 'Mod5', 'LevelThree')]


def modnames(mask):
    if mask == 0:
        return '[]'
    return '[' + ' '.join(b[1] for b in MODBITS if mask & b[0]) + ']'


lib = ctypes.CDLL('libxkbcommon.so.0')
lib.xkb_context_new.restype = ctypes.c_void_p
lib.xkb_context_new.argtypes = [ctypes.c_int]
lib.xkb_keymap_new_from_string.restype = ctypes.c_void_p
lib.xkb_keymap_new_from_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
lib.xkb_state_new.restype = ctypes.c_void_p
lib.xkb_state_new.argtypes = [ctypes.c_void_p]
lib.xkb_state_update_mask.argtypes = [ctypes.c_void_p] + [ctypes.c_uint32] * 6
lib.xkb_state_key_get_one_sym.restype = ctypes.c_uint32
lib.xkb_state_key_get_one_sym.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.xkb_keymap_min_keycode.restype = ctypes.c_uint32
lib.xkb_keymap_min_keycode.argtypes = [ctypes.c_void_p]
lib.xkb_keymap_max_keycode.restype = ctypes.c_uint32
lib.xkb_keymap_max_keycode.argtypes = [ctypes.c_void_p]
lib.xkb_keymap_key_get_name.restype = ctypes.c_char_p
lib.xkb_keymap_key_get_name.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.xkb_keysym_from_name.restype = ctypes.c_uint32
lib.xkb_keysym_from_name.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.xkb_keysym_get_name.restype = ctypes.c_int
lib.xkb_keysym_get_name.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_size_t]

ctx = lib.xkb_context_new(0)
km = lib.xkb_keymap_new_from_string(ctx, open(KEYMAP, 'rb').read(), 2, 0)
st = lib.xkb_state_new(km)
LO, HI = lib.xkb_keymap_min_keycode(km), lib.xkb_keymap_max_keycode(km)


def kn(kc):
    n = lib.xkb_keymap_key_get_name(km, kc)
    return n.decode() if n else '?'


_maps = {}


def symmap(mask, locked=0):
    key = (mask, locked)
    if key not in _maps:
        lib.xkb_state_update_mask(st, mask, 0, locked, 0, 0, 0)
        _maps[key] = {kc: lib.xkb_state_key_get_one_sym(st, kc) for kc in range(LO, HI + 1)}
    return _maps[key]


def symname(v):
    if not v:
        return 'NoSymbol'
    b = ctypes.create_string_buffer(256)
    lib.xkb_keysym_get_name(v, b, 256)
    return b.value.decode()


binds = json.load(open(os.path.join(S, 'binds.json')))
keymap_sha = __import__('hashlib').sha256(open(KEYMAP, 'rb').read()).hexdigest()

R = []
A = R.append
A('# ExecBindsLive — does every live bind fire on the host keymap? (round 49 w1)')
A('#')
A(f'# keymap: xkbcli-compile-keymap --layout br --options compose:caps, sha256 {keymap_sha}')
A('# method: libxkbcommon 1.13.2 via ctypes — xkb_state_update_mask(state, depressed=bind modmask, 0, locked=0,')
A('#         0, 0, group 0) then xkb_state_key_get_one_sym(state, keycode) for keycode %d..%d.' % (LO, HI))
A('#         A press fires the bind iff its translated keysym equals xkb_keysym_from_name(key, NO_FLAGS) or')
A('#         xkb_keysym_from_name(key, CASE_INSENSITIVE) AND depressed mods == bind modmask.')
A('#         (Hyprland: KeybindManager.cpp:652 exact modmask; :710-724 either keysym; InputManager.cpp:1711')
A('#         depressed-only modmask; KeybindManager.cpp:369 which state.)')
A('# level/modifier rows per keysym are in bind-keys.txt (pinned how-to-type).')
A('')
summary = {'FIRES': 0, 'DEAD': 0, 'DUPLICATE': 0}
seen = {}
seen_dup = {}
dead = []
for i, b in enumerate(binds):
    k = b['key']
    if k.startswith(('mouse', 'switch:')):
        continue
    if b['keycode'] != 0 and k == '':
        kc = b['keycode']
        ok = LO <= kc <= HI
        summary['FIRES' if ok else 'DEAD'] += 1
        A(f'bind[{i:3d}] code:{kc} ({kn(kc)}) modmask={b["modmask"]:3d} {modnames(b["modmask"]):26s} -> '
          f'{"FIRES on keycode " + str(kc) + " " + kn(kc) if ok else "DEAD: keycode outside the keymap"}')
        continue
    ident = (b['modmask'], k, b['keycode'])
    dupof = seen.get(ident)
    if dupof is None:
        seen[ident] = i
    elif ident not in seen_dup:
        seen_dup[ident] = i
    cands = {v for v in (lib.xkb_keysym_from_name(k.encode(), 0), lib.xkb_keysym_from_name(k.encode(), 1)) if v}
    m = symmap(b['modmask'])
    hits = [(kc, kn(kc)) for kc, s in m.items() if s in cands]
    cap = symmap(b['modmask'], locked=2)  # CapsLock locked: letters become upper case while modmask stays depressed-only
    caphits = [(kc, kn(kc)) for kc, s in cap.items() if s in cands and (kc, kn(kc)) not in hits]
    if hits:
        summary['FIRES'] += 1
        dupnote = ''
        if dupof is not None:
            summary['DUPLICATE'] += 1
            dupnote = f' — DUPLICATE of bind[{dupof}]; both fire (bindsHit collects every match)'
        A(f'bind[{i:3d}] {k:22s} modmask={b["modmask"]:3d} {modnames(b["modmask"]):26s} -> FIRES from '
          + ', '.join(f'{kc} {n} ({symname(m[kc])})' for kc, n in hits) + dupnote)
        if caphits:
            A('        also with CapsLock locked: ' + ', '.join(f'{kc} {n} ({symname(cap[kc])})' for kc, n in caphits))
    else:
        summary['DEAD'] += 1
        dupnote = f' (also a duplicate of bind[{dupof}])' if dupof is not None else ''
        dead.append((i, k, b['modmask'], 'no keycode yields it under this mask' + dupnote))
        A(f'bind[{i:3d}] {k:22s} modmask={b["modmask"]:3d} {modnames(b["modmask"]):26s} -> DEAD: no keycode '
          f'yields {" / ".join(f"0x{v:04x} {symname(v)}" for v in sorted(cands))} with depressed mods == this mask')
        for mask in (0, 1, 4, 8, 64, 65, 68, 72, 73, 76):
            h = [(kc, kn(kc)) for kc, s in symmap(mask).items() if s in cands]
            if h:
                A(f'        produced under modmask {mask:3d} {modnames(mask)}: '
                  + ', '.join(f'{kc} {n}' for kc, n in h))
A('')
A('# mouse and switch binds: no keysym comparison (hyprctl `mouse` is true only for the mouse:N forms;')
A('# mouse_up/mouse_down are reported with mouse=false)')
for i, b in enumerate(binds):
    if b['key'].startswith(('mouse', 'switch:')):
        k = b['key']
        shape = k if k.startswith('mouse') else ':'.join(k.split(':')[:2]) + ':<name>'
        A(f'bind[{i:3d}] {shape:20s} modmask={b["modmask"]:3d} {modnames(b["modmask"]):26s} mouse={b["mouse"]}')
A('')
A(f'# summary: key/code binds = {summary["FIRES"] + summary["DEAD"]}; fire = {summary["FIRES"]} '
  f'(of which {summary["DUPLICATE"]} are duplicates of an earlier bind and fire in addition to it); '
  f'cannot fire = {summary["DEAD"]}')
A('# dead binds:')
for i, k, mask, why in dead:
    A(f'#   bind[{i}] {k} modmask={mask} {modnames(mask)} — {why}')
open(os.path.join(OUT, 'bind-reachability.txt'), 'w', encoding='utf-8').write('\n'.join(R) + '\n')
print(summary)
for d in dead:
    print(d)
