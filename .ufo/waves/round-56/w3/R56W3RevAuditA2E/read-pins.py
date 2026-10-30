import hashlib
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = '0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
FETCH = '.ufo/waves/round-56/fetch/'
RANGES = {
    'Hyprland-MiscFunctions.cpp': [(61, 83)],
    'Hyprland-HyprCtl.cpp': [(1164, 1279), (2028, 2028)],
    'man7-inotify.7.html': [(85, 99), (168, 189), (225, 228), (258, 262), (293, 310), (313, 319)],
    'Hyprland-ConfigWatcher.cpp': [(21, 111)],
    'Hyprland-legacy-ConfigManager.cpp': [(1802, 1855)],
}
for name, ranges in RANGES.items():
    blob = subprocess.check_output(['git', '-C', LANE, 'show', REV + ':' + FETCH + name])
    print('\n### ' + name + ' sha256=' + hashlib.sha256(blob).hexdigest())
    lines = blob.decode().splitlines()
    for start, end in ranges:
        for number in range(start, min(end, len(lines)) + 1):
            print(str(number) + ': ' + lines[number - 1])
    if name == 'Hyprland-ConfigWatcher.cpp':
        for token in ('ev->mask', 'ev->name', 'IN_Q_OVERFLOW'):
            hits = [str(n) for n, line in enumerate(lines, 1) if token in line]
            print('LITERAL_SEARCH ' + token + ': ' + (','.join(hits) or 'NO HITS'))
    if name == 'Hyprland-MiscFunctions.cpp':
        body = '\n'.join(lines[60:83])
        for token in ('getpwnam', 'getpwuid', 'realpath'):
            print('LITERAL_SEARCH absolutePath ' + token + ': ' + ('HIT' if token in body else 'NO HITS'))
entry = subprocess.check_output(['git', '-C', LANE, 'show', REV + ':corpus/knowledge/hyprland-config-autoreload-r56.md']).decode()
print('\n### ENTRY selected rows and prose')
for n, line in enumerate(entry.splitlines(), 1):
    if any(line.startswith('| ' + row + ' |') for row in ('K25','K26','K27','K28','K29','K30','E01')) or (18 <= n <= 75) or (132 <= n <= 143):
        print(str(n) + ': ' + line)
