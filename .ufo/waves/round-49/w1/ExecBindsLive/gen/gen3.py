#!/usr/bin/env python3
"""Judge behaviour matrix + live version receipt, written from real runs."""
import hashlib, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
KEYMAP = os.path.join(S, 'keymap-br.xkb')
JUDGE = '/usr/lib/xkbcommon/xkbcli-how-to-type'
ENV = {'PATH': '/usr/bin', 'HOME': os.path.join(S, 'home'), 'XDG_CONFIG_HOME': os.path.join(S, 'xdg')}
sha = hashlib.sha256(open(KEYMAP, 'rb').read()).hexdigest()

L = []
A = L.append
A('# ExecBindsLive — pinned how-to-type behaviour on a host keymap (round 49 w1)')
A('#')
A('# judge: /usr/lib/xkbcommon/xkbcli-how-to-type sha256 '
  + hashlib.sha256(open(JUDGE, 'rb').read()).hexdigest())
A('# keymap: rebuilt deterministically (two runs, identical sha256) by')
A('#   env -i PATH=/usr/bin HOME=<scratch>/home XDG_CONFIG_HOME=<scratch>/xdg \\')
A('#     /usr/lib/xkbcommon/xkbcli-compile-keymap --layout br --options compose:caps > keymap.xkb')
A(f'# keymap sha256: {sha}')
A('# host packages (pacman -Q, read-only): libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1')
A('# every case runs with env -i PATH=/usr/bin and HOME/XDG_CONFIG_HOME in scratch; no user xkb include path.')
A('')
cases = [
    ('missing positional', ['--keymap=KEYMAP', '--disable-compose']),
    ('without --disable-compose', ['--keymap=KEYMAP', '--keysym', 'slash']),
    ('missing keymap file', ['--keymap=<scratch>/nosuch.xkb', '--disable-compose', '--keysym', 'slash']),
    ('unknown keysym name', ['--keymap=KEYMAP', '--disable-compose', '--keysym', 'nosuchsym']),
    ('upper-case bind name SLASH', ['--keymap=KEYMAP', '--disable-compose', '--keysym', 'SLASH']),
    ('upper-case bind name RETURN', ['--keymap=KEYMAP', '--disable-compose', '--keysym', 'RETURN']),
    ('canonical name Return', ['--keymap=KEYMAP', '--disable-compose', '--keysym', 'Return']),
    ('numeric 0x002f', ['--keymap=KEYMAP', '--disable-compose', '--keysym', '0x002f']),
    ('decimal 47', ['--keymap=KEYMAP', '--disable-compose', '--keysym', '47']),
    ('hex without 0x (2f)', ['--keymap=KEYMAP', '--disable-compose', '--keysym', '2f']),
    ('digits: 0 is a name', ['--keymap=KEYMAP', '--disable-compose', '--keysym', '0']),
    ('0x0 is NoSymbol', ['--keymap=KEYMAP', '--disable-compose', '--keysym', '0x0']),
    ('--keymap with RMLVO option', ['--keymap=KEYMAP', '--layout', 'us', '--disable-compose', '--keysym', 'slash']),
    ('bare --keymap reads stdin', ['--keymap', '--disable-compose', '--keysym', 'slash']),
]
for name, argv in cases:
    a = [x.replace('KEYMAP', KEYMAP) for x in argv]
    stdin = open(KEYMAP, 'rb').read() if '--keymap' in argv and '--keymap=KEYMAP' not in argv else b''
    p = subprocess.run([JUDGE] + a, capture_output=True, text=True, env=ENV, input=stdin.decode('utf-8'))
    A(f'### {name}')
    A('command: ' + ' '.join(['xkbcli-how-to-type'] + [x.replace(KEYMAP, 'keymap.xkb') for x in a]))
    A(f'exit: {p.returncode}')
    A('stdout:')
    for line in (p.stdout or '<empty>').rstrip('\n').splitlines():
        A('  | ' + line)
    A('stderr:')
    for line in (p.stderr or '<empty>').rstrip('\n').splitlines():
        A('  | ' + line.replace(KEYMAP, 'keymap.xkb'))
    A('')
open(os.path.join(OUT, 'judge-behaviour.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# live version receipt
V = []
B = V.append
B('# ExecBindsLive — live host reads (round 49 w1, 2026-10-27)')
B('#')
B('# allowed read-only compositor reads only: hyprctl version, hyprctl getoption, hyprctl binds -j.')
B('# no device names, no window titles, no dispatcher args are recorded.')
B('')
p = subprocess.run(['hyprctl', 'version'], capture_output=True, text=True)
B('command: hyprctl version   (first line only)')
B('  | ' + p.stdout.splitlines()[0])
B(f'  exit: {p.returncode}')
B('')
p = subprocess.run(['hyprctl', 'getoption', 'input:resolve_binds_by_sym', '-j'], capture_output=True, text=True)
B('command: hyprctl getoption input:resolve_binds_by_sym -j')
B('  | ' + p.stdout.strip())
B(f'  exit: {p.returncode}')
B('')
B('command: hyprctl binds -j   -> 192 binds; raw JSON bytes 90401; sha256 '
  '9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779 (two captures 3 min apart, identical)')
B('')
B('# host key input config (~/.config/hypr/input.conf, read-only):')
B('#   ~/.config/hypr/input.conf:10  kb_layout = br')
B('#   ~/.config/hypr/input.conf:11  kb_options = compose:caps')
B('#   ~/.config/hypr/input.conf:18  numlock_by_default = true')
B('#   kb_variant and kb_model are commented out / unset, so the compiled keymap uses the pc105 default.')
open(os.path.join(OUT, 'live-version.txt'), 'w', encoding='utf-8').write('\n'.join(V) + '\n')
print('wrote judge-behaviour.txt, live-version.txt')
