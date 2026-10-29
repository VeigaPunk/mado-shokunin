import hashlib, json, os, re, sys
LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
PIN = LANE + '/.ufo/waves/round-56/fetch/'
OUT = LANE + '/.ufo/waves/round-56/w1/R56ScribeSourcesB'
SCRATCH = '/fast/scratch/hyaku/mado-r56/R56ScribeSourcesB'
ACCESS = '2026-10-28'
REV = 'efb50993780079460b0cbed1363e2166a2de1d9f'
ENTRY = 'corpus/knowledge/hyprland-config-autoreload-r56.md'
T = json.load(open(LANE + '/.ufo/waves/round-56/frozen-tables.json'))
C1 = T['c1']
assert hashlib.sha256(open(LANE + '/.ufo/waves/round-56/frozen-tables.json', 'rb').read()).hexdigest() == 'd50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af'
assert C1['rows'] == {'S383':'Hyprland-ConfigWatcher.cpp','S384':'Hyprland-ConfigValues.cpp','S385':'Hyprland-PropRefresher.cpp','S386':'Hyprland-EventLoopManager.cpp','S387':'Hyprland-legacy-ConfigManager.cpp','S388':'Hyprland-MiscFunctions.cpp','S389':'Hyprland-HyprCtl.cpp','S390':'man7-inotify.7.html'}

ROWS = [
 dict(id='S383', pin='Hyprland-ConfigWatcher.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 inotify config watcher - watch registration, masks and symlink canonical watch',
      scope='watch registration, event masks and the autoreload gate in CConfigWatcher::update and setWatchList',
      teaches='update() gives an empty watch list when misc:disable_autoreload is non-zero, else setWatchList replaces the watches with one per config path; file masks are IN_CLOSE_WRITE and IN_DONT_FOLLOW, directories add create, delete and move bits, and symlinks get a canonical-target watch.',
      recheck='on-release', gate_line=34),
 dict(id='S384', pin='Hyprland-ConfigValues.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 config value table - misc:disable_autoreload declaration',
      scope='the default, description and refresh tag of the misc:disable_autoreload option declaration',
      teaches='misc:disable_autoreload is declared as a Bool option defaulting to false, and its declaration carries the REFRESH_CONFIG_WATCHER refresh tag.',
      recheck='on-release', gate_line=492),
 dict(id='S385', pin='Hyprland-PropRefresher.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 prop refresher - scheduled config-watcher refresh branch',
      scope='the branch of the scheduled property refresh that calls the config watcher update',
      teaches='When REFRESH_CONFIG_WATCHER is tripped, refreshProp calls the config watcher update().',
      recheck='on-release', gate_line=148),
 dict(id='S386', pin='Hyprland-EventLoopManager.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 event loop manager - config watcher inotify fd source and dispatch',
      scope='registration of the watcher inotify fd into the wayland event loop and the callback that drains it',
      teaches='enterLoop registers the watcher inotify fd as a readable wayland event source, and that source callback calls onInotifyEvent().',
      recheck='on-release', gate_line=128),
 dict(id='S387', pin='Hyprland-legacy-ConfigManager.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 legacy config manager - watcher reload callback, config path list and source glob',
      scope='the watcher callback that reloads, the configPaths list, and source= glob and regular-file handling',
      teaches='The watcher callback logs and calls reload(), postConfigReload schedules a REFRESH_ALL refresh, configPaths is cleared and reseeded with the main config path, and handleSource globs source= entries and keeps only regular files.',
      recheck='on-release', gate_line=1080),
 dict(id='S388', pin='Hyprland-MiscFunctions.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 misc functions - absolutePath for home and relative config paths',
      scope='absolutePath resolution of a leading tilde and of relative config paths',
      teaches='absolutePath replaces a leading ~ with the HOME environment value and joins a relative path to the directory of the file being parsed.',
      recheck='on-release', gate_line=65),
 dict(id='S389', pin='Hyprland-HyprCtl.cpp', kind='code', tier='A',
      title='Hyprland 0.56.2 hyprctl keyword and reload requests - disable_autoreload refresh and reload call',
      scope='the keyword branch that refreshes the watcher for misc:disable_autoreload and the reload request',
      teaches='A keyword whose text contains misc:disable_autoreload calls the watcher update(), and the reload request calls Config::mgr()->reload() unless it ends in full-reset.',
      recheck='on-release', gate_line=1223),
 dict(id='S390', pin='man7-inotify.7.html', kind='docs', tier='B',
      title='Linux man-pages 6.19 inotify(7) manual page',
      scope='the IN_CLOSE_WRITE event and the IN_DONT_FOLLOW watch-mask definitions',
      teaches='IN_CLOSE_WRITE reports a file opened for writing being closed, and IN_DONT_FOLLOW stops inotify_add_watch from dereferencing a symbolic link.',
      recheck='90d', gate_line=186),
]
assert [r['id'] for r in ROWS] == ['S%d' % i for i in range(383, 391)]

def url_for(r):
    if r['pin'].startswith('man7'):
        return 'https://man7.org/linux/man-pages/man7/inotify.7.html'
    return 'https://raw.githubusercontent.com/hyprwm/Hyprland/%s/%s' % (REV, C1['pin_suffix'][r['pin']])

def locators(lines):
    lines = sorted(set(lines))
    out = []
    i = 0
    while i < len(lines):
        j = i
        while j + 1 < len(lines) and lines[j + 1] == lines[j] + 1:
            j += 1
        out.append(str(lines[i]) if i == j else '%d-%d' % (lines[i], lines[j]))
        i = j + 1
    return ','.join(out)

def in_locators(line, loc):
    for part in loc.split(','):
        a, _, b = part.partition('-')
        a = int(a); b = int(b) if b else a
        if a <= line <= b:
            return True
    return False

rows_md, gate_rows, report = [], [], []
for r in ROWS:
    pin = r['pin']
    path = PIN + pin
    data = open(path, 'rb').read()
    sha = hashlib.sha256(data).hexdigest()
    assert sha == C1['pin_sha256'][pin], pin
    ks = [k for k in C1['k'] if k['pin'] == pin]
    assert ks and all(k['sid'] == r['id'] for k in ks), (pin, [k['sid'] for k in ks])
    lines_text = data.decode('utf-8').split('\n')
    for k in ks:
        assert k['quote'] in lines_text[k['line'] - 1], (k['id'], k['line'])
    lines = [k['line'] for k in ks]
    url = url_for(r)
    base = C1['pin_suffix'][pin].split('/')[-1]
    if pin.startswith('man7'):
        loc = locators(lines)
        anchor = '%s:%s @ man-pages 6.19 (footer 2026-02-14); %d B sha256 %s; pin .ufo/waves/round-56/fetch/%s' % (base, loc, len(data), sha, pin)
    else:
        loc = locators(lines)
        anchor = '%s:%s @ %s; %d B sha256 %s; pin .ufo/waves/round-56/fetch/%s' % (base, loc, REV, len(data), sha, pin)
    for l in lines:
        assert in_locators(l, loc), (r['id'], l, loc)
    title = r['title'] + ' - ' + url
    cells = [r['id'], title, r['kind'], r['tier'], r['scope'], anchor, r['teaches'], 'mined', ACCESS, r['recheck'], ENTRY]
    assert len(cells) == 11
    for c in cells:
        assert '|' not in c and '\\' not in c, (r['id'], c)
        assert '\n' not in c
    assert title.endswith(url) and url.endswith('/' + C1['pin_suffix'][pin]) or pin.startswith('man7')
    rows_md.append('| ' + ' | '.join(cells) + ' |')
    gl = r['gate_line']
    gq = [k for k in ks if k['line'] == gl]
    assert gq, (r['id'], gl)
    quote = gq[0]['quote']
    assert len(quote.split()) <= 25, quote
    assert quote in lines_text[gl - 1]
    gate_rows.append((r['id'], url, ACCESS, '%s:%d' % (pin, gl), quote, len(quote.split()), sha, len(data), loc, len(ks), len(r['teaches'].split())))

os.makedirs(OUT, exist_ok=True)
os.makedirs(SCRATCH, exist_ok=True)
open(OUT + '/rows.md', 'w').write('\n'.join(rows_md) + '\n')
open(SCRATCH + '/rows.md', 'w').write('\n'.join(rows_md) + '\n')
g = ['# Gate — S383..S390 (round-56 w1, R56ScribeSourcesB)', '',
     'Access date for every row: %s. Each quote was matched byte-for-byte to the stated line of the pin file (checked by script against the bytes on disk; the pin sha256 was re-hashed and equals `frozen-tables.json` `c1.pin_sha256`; Hyprland pins at commit %s).' % (ACCESS, REV), '',
     '| row | URL | accessed | pin:line | located quote (words) | pin sha256 | pin bytes | anchor locators | K rows covered |',
     '|---|---|---|---|---|---|---|---|---|']
for (rid, url, acc, pl, q, nw, sha, nb, loc, nk, tw) in gate_rows:
    g.append('| %s | %s | %s | %s | `%s` (%d) | %s | %d | %s | %d |' % (rid, url, acc, pl, q, nw, sha, nb, loc, nk))
g.append('')
g.append('Teaches cell word counts (one sentence each): ' + ', '.join('%s=%d' % (x[0], x[10]) for x in gate_rows))
open(OUT + '/gate.md', 'w').write('\n'.join(g) + '\n')
print('\n'.join(rows_md))
print('\n'.join(g))
