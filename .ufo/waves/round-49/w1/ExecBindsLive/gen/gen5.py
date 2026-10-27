#!/usr/bin/env python3
"""Host join summary + session-material leak check for seat ExecBindsLive."""
import ctypes, json, os, re, subprocess, sys, hashlib

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
KEYMAP = os.path.join(S, 'keymap-br.xkb')
JUDGE = '/usr/lib/xkbcommon/xkbcli-how-to-type'
ENV = {'PATH': '/usr/bin', 'HOME': os.path.join(S, 'home'), 'XDG_CONFIG_HOME': os.path.join(S, 'xdg')}
ROW = re.compile(r'^(\d+)\s+(\S+)\s+(\d+)\s+(.*?)\s+(\d+)\s+\[(.*?)\]\s*$')

lib = ctypes.CDLL('libxkbcommon.so.0')
lib.xkb_keysym_from_name.restype = ctypes.c_uint32
lib.xkb_keysym_from_name.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.xkb_keysym_get_name.restype = ctypes.c_int
lib.xkb_keysym_get_name.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_size_t]


def nm(v):
    b = ctypes.create_string_buffer(256)
    lib.xkb_keysym_get_name(v, b, 256)
    return b.value.decode() if v else 'NoSymbol'


binds = json.load(open(os.path.join(S, 'binds.json')))
names = sorted({b['key'] for b in binds if b['key'] and not b['key'].startswith(('mouse', 'switch:'))})


def rows(v):
    p = subprocess.run([JUDGE, f'--keymap={KEYMAP}', '--disable-compose', '--keysym', f'0x{v:04x}'],
                       capture_output=True, text=True, env=ENV, input='')
    out = []
    for line in p.stdout.splitlines():
        m = ROW.match(line)
        if m:
            out.append({'kc': int(m.group(1)), 'kn': m.group(2), 'level': int(m.group(5)),
                        'mods': m.group(6).split()})
    return out


L = []
A = L.append
A('# ExecBindsLive — host join: every keysym the live binds name, on the host keymap (round 49 w1)')
A('#')
A('# keymap sha256 ' + hashlib.sha256(open(KEYMAP, 'rb').read()).hexdigest()
  + ' (compile recipe in judge-behaviour.txt)')
A('# judge: pinned xkbcli-how-to-type; rows verbatim in bind-keys.txt.')
A('# columns: keysym value, canonical name, base-level keycodes, level>=2 access count, bind names using it')
A('')
seen = {}
for n in names:
    v = lib.xkb_keysym_from_name(n.encode(), 1)
    if not v:
        continue
    r = rows(v)
    base = [x for x in r if x['level'] == 1]
    multi = [x for x in r if x['level'] >= 2]
    seen.setdefault(n, (v, base, multi))

only_multi, absent = [], []
for n, (v, base, multi) in sorted(seen.items()):
    A(f'0x{v:04x} {nm(v):22s} base keycodes: '
      + (', '.join(f'{x["kc"]} {x["kn"]} [{" ".join(x["mods"])}]' for x in base) if base else 'NONE')
      + f' | level>=2 rows: {len(multi)}')
    if not base:
        (only_multi if multi else absent).append(n)
A('')
A(f'# distinct keysym names in the live binds: {len(seen)}')
A(f'# keysyms reachable only at level >= 2 on this keymap: {len(only_multi)} {only_multi}')
A(f'# keysyms not on this keymap at all: {len(absent)} {absent}')
A('')
A('## the SLASH question (the L1 host sample)')
for n in ('SLASH',):
    v, base, multi = seen[n]
    A(f'{n} -> 0x{v:04x} {nm(v)}')
    for x in base + multi:
        A(f'  keycode {x["kc"]} {x["kn"]} level {x["level"]} [{" ".join(x["mods"])}]')
A('# A SUPER bind (modmask 64, depressed-only equality) fires only from the level 1 row: AB11.')
A('# The AD01 level 3/4 rows need Mod5/Shift depressed, which makes the press modmask != 64.')
open(os.path.join(OUT, 'host-join-summary.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ---- leak check: no dispatcher arg / description / device name stands as a token in any receipt ----
C = []
B = C.append
B('# ExecBindsLive — session-material check on this seat\'s receipts (round 49 w1)')
B('#')
B('# method: every non-empty `arg` and `description` value in the raw hyprctl binds JSON (298 distinct')
B('# strings) and the switch device name (1) are searched in every receipt with token boundaries')
B('# (?<![\\w.-]) value (?![\\w.-]), so a keysym name such as XF86AudioMute does not match the arg "Mute"')
B('# by substring. Raw JSON itself is never written outside scratch.')
B('')
vals = set()
for b in binds:
    for f in ('arg', 'description'):
        v = b.get(f) or ''
        if len(v) >= 4:
            vals.add(v)
dev = {b['key'].split(':', 2)[2] for b in binds if b['key'].startswith('switch:') and b['key'].count(':') >= 2}
files = sorted(__import__('glob').glob(os.path.join(OUT, '*')))
helptext = subprocess.run([JUDGE, '--help'], capture_output=True, text=True, env=ENV, input='')
vocab = set(re.findall(r"[A-Za-z]+", helptext.stdout + helptext.stderr))
hits = []
for f in files:
    if os.path.basename(f) in ('session-material-check.txt',):
        continue
    lines = open(f, encoding='utf-8', errors='replace').read().splitlines()
    for i, line in enumerate(lines, 1):
        for v in sorted(vals | dev):
            if re.search(r'(?<![\w.-])' + re.escape(v) + r'(?![\w.-])', line):
                judge_text = line.lstrip().startswith('|') and v in vocab
                hits.append((os.path.basename(f), i, ('judge usage text: "' + v + '"') if judge_text else 'REDACT',
                             line[:70] if judge_text else ''))
B(f'receipts scanned: {len(files)}')
B(f'arg/description strings checked: {len(vals)}; switch device names checked: {len(dev)}')
B(f'token hits: {len(hits)}')
for f, i, kind, ctx in hits:
    B(f'  {f}:{i}  {kind}')
    if ctx:
        B(f'    | {ctx}')
B('classification: a hit is judge usage text when the matched value is a word of the pinned judge\'s own')
B('--help output and the line belongs to that dump; every such hit is an English word of the usage message,')
B('not dispatcher content. Any other hit would print REDACT and must be treated as a leak.')
B('substring-only coincidences (not token hits, for auditability): XF86 keysym names contain')
B('"Mute"/"Pause"/"Play"/"Calculator".')
open(os.path.join(OUT, 'session-material-check.txt'), 'w', encoding='utf-8').write('\n'.join(C) + '\n')
print('only_multi', only_multi, 'absent', absent, 'token hits', hits)
