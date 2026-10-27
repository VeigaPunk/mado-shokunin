#!/usr/bin/env python3
"""Generate read-only receipts for seat ExecBindsLive (round 49 w1). No writes outside argv[1]."""
import ctypes, hashlib, json, os, re, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
KEYMAP = os.path.join(S, 'keymap-br.xkb')
JUDGE = '/usr/lib/xkbcommon/xkbcli-how-to-type'
ENV = {'PATH': '/usr/bin', 'HOME': os.path.join(S, 'home'), 'XDG_CONFIG_HOME': os.path.join(S, 'xdg')}

MODBITS = [(1, 'Shift'), (2, 'Lock'), (4, 'Control'), (8, 'Mod1'), (16, 'Mod2'),
           (32, 'Mod3'), (64, 'Mod4'), (128, 'Mod5')]


def modnames(mask):
    if mask == 0:
        return '[]'
    return '[' + ' '.join(n for b, n in MODBITS if mask & b) + ']'


lib = ctypes.CDLL('libxkbcommon.so.0')
lib.xkb_keysym_from_name.restype = ctypes.c_uint32
lib.xkb_keysym_from_name.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.xkb_keysym_get_name.restype = ctypes.c_int
lib.xkb_keysym_get_name.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_size_t]


def sym(name, flags):
    return lib.xkb_keysym_from_name(name.encode(), flags)


def symname(v):
    b = ctypes.create_string_buffer(256)
    lib.xkb_keysym_get_name(v, b, 256)
    return b.value.decode()


def howto(value):
    p = subprocess.run([JUDGE, f'--keymap={KEYMAP}', '--disable-compose', '--keysym', f'0x{value:04x}'],
                       capture_output=True, text=True, env=ENV, input='')
    return p


ROW = re.compile(r'^(\d+)\s+(\S+)\s+(\d+)\s+(.*?)\s+(\d+)\s+\[(.*?)\]\s*$')


def rows_of(stdout):
    out = []
    for line in stdout.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        mods = m.group(6).split()
        out.append({'keycode': int(m.group(1)), 'keyname': m.group(2), 'layout': int(m.group(3)),
                    'layout_name': m.group(4).strip(), 'level': int(m.group(5)), 'mods': mods})
    return out


binds = json.load(open(os.path.join(S, 'binds.json')))
raw_sha = hashlib.sha256(open(os.path.join(S, 'binds.json'), 'rb').read()).hexdigest()
raw2_sha = hashlib.sha256(open(os.path.join(S, 'binds2.json'), 'rb').read()).hexdigest()
keymap_sha = hashlib.sha256(open(KEYMAP, 'rb').read()).hexdigest()


def form(b):
    k = b['key']
    if k.startswith('mouse'):
        if re.match(r'^mouse:\d+$', k):
            return 'mouse:<button>'
        if k.startswith('mouse:'):
            return 'mouse:' + k.split(':', 1)[1]
        return 'mouse:' + k.split('_', 1)[1]
    if k.startswith('switch:'):
        return ':'.join(k.split(':')[:2]) + ':<name>'
    if k == '' and b['keycode'] != 0:
        return 'code:N'
    if k == '':
        return '<empty>'
    return 'keysym-name'


# keycode -> key name from the compiled keymap
kcnames = {}
for line in open(KEYMAP, encoding='utf-8'):
    m = re.match(r'\t<(\w+)>\s*=\s*(\d+);', line)
    if m:
        kcnames[int(m.group(2))] = m.group(1)

# ---------------- binds-shape.txt ----------------
lines = []
A = lines.append
A('# ExecBindsLive — live binds shape (round 49 w1)')
A('#')
A('# command: hyprctl binds -j')
A('# capture 1: 2026-10-27T04:35Z (UTC), capture 2: 2026-10-27T04:38:35Z (UTC)')
A(f'# raw JSON bytes: {os.path.getsize(os.path.join(S, "binds.json"))}')
A(f'# raw JSON sha256: {raw_sha}')
A(f'# recapture sha256: {raw2_sha}  ({"identical" if raw_sha == raw2_sha else "CHANGED between captures"})')
A('# raw JSON is NOT committed: it carries dispatcher args, descriptions and the switch device name.')
A('# fields kept per bind: key, keycode, modmask, mouse, catch_all, submap (+ dispatcher name only).')
A('')
A(f'binds: {len(binds)}')
from collections import Counter
forms = Counter(form(b) for b in binds)
A('by key form: ' + ', '.join(f'{k}={v}' for k, v in sorted(forms.items())))
A(f'keycode field: non-zero for {sum(1 for b in binds if b["keycode"] != 0)} binds; distinct values: '
  + ', '.join(f'{k}({kcnames.get(k, "?")})' for k in sorted({b["keycode"] for b in binds if b["keycode"]})))
A(f'mouse field: true={sum(1 for b in binds if b["mouse"])} false={sum(1 for b in binds if not b["mouse"])}')
A(f'catch_all: true={sum(1 for b in binds if b["catch_all"])}')
A('submap: ' + str(dict(Counter(b['submap'] or '<none>' for b in binds))))
A('modmask histogram (bit names: 1 Shift,2 Lock,4 Control,8 Mod1,16 Mod2,32 Mod3,64 Mod4,128 Mod5):')
for mask, n in sorted(Counter(b['modmask'] for b in binds).items()):
    A(f'  {mask:3d} {modnames(mask):28s} {n}')
A('modmask notes: 0 present with numlock_by_default=true on the host (locked mods are not in the bind '
  'modmask: Hyprland uses MODS.depressed only). No mask carries 16 (Mod2/NumLock) or 2 (Lock).')
A('')
A('per-bind shape (index | key form | keycode | keyname | modmask names | mouse | catch_all | submap | dispatcher):')
for i, b in enumerate(binds):
    A(f'{i:3d} | {form(b):18s} | {b["keycode"]:3d} | {kcnames.get(b["keycode"], "-"):5s} | '
      f'{b["modmask"]:3d} {modnames(b["modmask"]):30s} | {str(b["mouse"]):5s} | {str(b["catch_all"]):5s} | '
      f'{b["submap"] or "<none>":8s} | {b["dispatcher"]}')
open(os.path.join(OUT, 'binds-shape.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

# ---------------- keysym resolution + how-to-type ----------------
names = sorted({b['key'] for b in binds if form(b) == 'keysym-name'})
res = {}
for n in names:
    res[n] = {'up': sym(n, 0), 'lower': sym(n, 1)}

howto_cache = {}


def judge(value):
    if value not in howto_cache:
        howto_cache[value] = howto(value)
    return howto_cache[value]


out = []
B = out.append
B('# ExecBindsLive — every keysym the live binds name, joined to the host keymap (round 49 w1)')
B('#')
B('# keymap: compiled by /usr/lib/xkbcommon/xkbcli-compile-keymap --layout br --options compose:caps')
B('#         env -i PATH=/usr/bin HOME/XDG_CONFIG_HOME in scratch; bytes %d; sha256 %s'
  % (os.path.getsize(KEYMAP), keymap_sha))
B('# judge:  /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=<keymap> --disable-compose --keysym 0x<val>')
B('# host input config: kb_layout = br, kb_options = compose:caps, numlock_by_default = true '
  '(~/.config/hypr/input.conf:10,11,18); kb_variant/kb_model unset.')
B('# name resolution: libxkbcommon 1.13.2 xkb_keysym_from_name via ctypes — NO_FLAGS (0) and '
  'CASE_INSENSITIVE (1). Live bind names are upper-case; the judge is case-sensitive, so the join')
B('# resolves each name the way Hyprland does and then queries the judge by numeric keysym.')
B(f'# distinct keysym-form bind names: {len(names)}')
B('')
for n in names:
    v0, v1 = res[n]['up'], res[n]['lower']
    B('=' * 78)
    B(f'bind name: {n}')
    B(f'  xkb_keysym_from_name("{n}", 0)                    -> 0x{v0:04x}' + (f' ({symname(v0)})' if v0 else ' (NoSymbol)'))
    B(f'  xkb_keysym_from_name("{n}", CASE_INSENSITIVE)     -> 0x{v1:04x}' + (f' ({symname(v1)})' if v1 else ' (NoSymbol)'))
    for tag, v in (('noflags', v0), ('case-insensitive', v1)):
        if not v:
            continue
        p = judge(v)
        B(f'  --- how-to-type --keysym 0x{v:04x}  [{tag}] rc={p.returncode}')
        for line in p.stdout.rstrip('\n').splitlines():
            B('  | ' + line)
        if p.stderr:
            for line in p.stderr.rstrip('\n').splitlines():
                B('  ! ' + line)
    B('')
open(os.path.join(OUT, 'bind-keys.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')

# ---------------- reachability ----------------
R = []
C = R.append
C('# ExecBindsLive — bind reachability on the host keymap (round 49 w1)')
C('#')
C('# Model (pinned sources, receipts/upstream-pins.txt): Hyprland compares the press modmask to the bind')
C('# modmask by EQUALITY (KeybindManager.cpp:652) and the modmask is depressed mods only (InputManager.cpp:1711),')
C('# so a level that needs a modifier the bind line does not name cannot fire that bind.')
C('# A bind fires on a keysym row iff (row mods minus Lock, the locked Caps state) is a subset of the bind modmask.')
C('# level 1 = base level of how-to-type; level >= 2 needs an extra modifier held.')
C('')
reach = {}
for i, b in enumerate(binds):
    f = form(b)
    if f != 'keysym-name':
        continue
    vals = [v for v in (res[b['key']]['up'], res[b['key']]['lower']) if v]
    rows = []
    for v in vals:
        rows += rows_of(judge(v).stdout)
    ok, extra_only, absent = [], [], []
    for r in rows:
        real = {m for m in r['mods'] if m != 'Lock'}
        need = 0
        for b_, nm in MODBITS:
            if nm in real:
                need |= b_
        if need & ~b['modmask'] == 0:
            ok.append(r)
        else:
            extra_only.append(r)
    state = 'FIRES' if ok else ('UNREACHABLE' if rows else 'NO-ROW')
    reach[i] = (state, ok, rows)
    C(f'bind[{i:3d}] {b["key"]:22s} modmask={b["modmask"]:3d} {modnames(b["modmask"]):26s} -> {state}')
    if state == 'FIRES':
        for r in ok:
            C(f'      fires on keycode {r["keycode"]:3d} {r["keyname"]:5s} layout {r["layout"]} '
              f'level {r["level"]} [{",".join(r["mods"]) if r["mods"] else ""}]')
    if state == 'UNREACHABLE' or state == 'NO-ROW':
        for r in rows:
            C(f'      row unreachable for this mask: keycode {r["keycode"]:3d} {r["keyname"]:5s} '
              f'level {r["level"]} [{",".join(r["mods"]) if r["mods"] else ""}]')
    # secondary paths: same keysym reachable only with a modifier the bind does not name
    sec = [(r, b_['mods']) for r, b_ in zip(rows, rows)]
    secs = [r for r in extra_only if r['level'] >= 1]
    if secs:
        C(f'      also produced by (extra modifier held, does NOT fire this bind): '
          + '; '.join(f'{r["keycode"]}/{r["keyname"]} level {r["level"]} [{" ".join(r["mods"])}]' for r in secs))
C('')
# code: binds
C('# code:N binds (no keysym; matched by xkb keycode only, KeybindManager.cpp:687-689)')
for i, b in enumerate(binds):
    if form(b) == 'code:N':
        C(f'bind[{i:3d}] code:{b["keycode"]:3d} ({kcnames.get(b["keycode"], "?")}) modmask={b["modmask"]:3d} '
          f'{modnames(b["modmask"])} -> FIRES on that keycode when depressed mods == {b["modmask"]}')
C('')
C('# mouse and switch binds (not key-sym matched)')
for i, b in enumerate(binds):
    if form(b).startswith(('mouse', 'switch')):
        C(f'bind[{i:3d}] {form(b):16s} modmask={b["modmask"]:3d} {modnames(b["modmask"])} mouse={b["mouse"]} '
          f'keycode={b["keycode"]}')
open(os.path.join(OUT, 'bind-reachability.txt'), 'w', encoding='utf-8').write('\n'.join(R) + '\n')

# summary counts
summ = Counter(v[0] for v in reach.values())
print('keysym binds:', len(reach), dict(summ))
print('level>=2-only:', [binds[i]['key'] for i, v in reach.items() if v[0] in ('UNREACHABLE', 'NO-ROW')])
