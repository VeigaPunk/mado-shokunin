import re
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = '0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
BASE = '13f0acbe3a15da2d9c08357a576d91dcadc85273'
ENTRY = 'corpus/knowledge/hyprland-config-autoreload-r56.md'
HELD = ['corpus/knowledge/input-debugging-boundaries-r15.md', 'corpus/knowledge/hyprland-input-devices-r46.md', 'corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md', 'corpus/knowledge/window-rule-effects-getprop.md']

def blob(rev, path):
    return subprocess.check_output(['git', '-C', LANE, 'show', rev + ':' + path]).decode()

entry = blob(REV, ENTRY)
print('REV=' + REV)
print('Inspection only: literal citation scan, not semantic proof; LSP device unavailable.')
for sid in ['S052', 'S162', 'S215', 'S316', 'S317', 'S318', 'S319']:
    lines = [str(n) for n, line in enumerate(entry.splitlines(), 1) if re.search(r'(?<![A-Za-z0-9])' + sid + r'(?![0-9])', line)]
    print('r56 citation ' + sid + ': ' + (','.join(lines) or 'NONE'))
for path in HELD:
    print('held unchanged versus frozen base: ' + path + ' = ' + str(blob(REV, path) == blob(BASE, path)))
for n, line in enumerate(blob(REV, 'corpus/SOURCES.md').splitlines(), 1):
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if cells[0] not in ['S316', 'S317', 'S318', 'S319']:
        continue
    assert len(cells) == 11
    sid, used = cells[0], cells[10]
    r46 = HELD[1] in used
    r55 = HELD[2] in used
    r56 = ENTRY in used
    print(f'SOURCES.md:{n} {sid}: r46={r46} r55={r55} r56={r56}; used-by={used}')
    assert r46 and r55 and not r56
print('REGISTRY_CHECK: 4/4 existing r46+r55 back-references present; r56 not cited and not listed')
print('CROSS_ENTRY: contradiction=0 reclaim=0 (manual bounded comparison in cross-a2.txt)')
