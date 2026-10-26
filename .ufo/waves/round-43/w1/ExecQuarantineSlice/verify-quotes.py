#!/usr/bin/env python3
"""Re-grep every quote and every structural claim in
.ufo/waves/round-43/assimilation/quarantine-verdicts.md. Exits non-zero on a miss."""
import glob, hashlib, os, re, subprocess, sys

W = os.path.dirname(os.path.abspath(__file__))
REG = '/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md'
APP = '/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md'
KN = '/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/'
LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
R5 = '/home/vgpnk/Projects/shokuknow/lanes/mado/round5/SOURCES-PROPOSED.md'
SLICE = os.path.join(W, 'quarantine-slice.raw')

fails = []
def check(ok, label):
    print(('PASS  ' if ok else 'FAIL  ') + label)
    if not ok:
        fails.append(label)

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

# 1. quotes: (file, line, substring, max_words)
QUOTES = [
    (REG, 349, 'the cited source could not be fetched, so no quote was checked', 25),
    (REG, 351, 'the gate block named no locator, so no quote was checked', 25),
    (REG, 141, 'cited source, companion URLs and local artifacts were all checked; the quote is in none of them', 25),
    (APP, 20, 'The direct URL answers HTTP 521 to a plain client; the body was retrieved through a reader proxy', 25),
    (KN + 'glyph-and-geometry-r31.md', 28, "the codemap entry and the producer's branch structure (round 5's row S216)", 25),
    (KN + 'glyph-and-geometry-r31.md', 36, "The host's rule imposes the same size (round 5's row S219)", 25),
    (KN + 'gkeep-size-to-real-size-r11.md', 63, "reports (round 10's S281)", 25),
    (KN + 'gkeep-size-to-real-size-r11.md', 62, 'the same variable the compositor', 25),
    (R5, 22, 'omarchy weather-icon helper', 25),
    (APP, 52, 'omarchy weather-icon helper', 25),
    (R5, 25, 'host gkeep window rules', 25),
    (LANE + '/PROVINCE.md', 76, 'documentation written in a localized channel', 25),
]
for path, ln, sub, cap in QUOTES:
    lines = open(path, encoding='utf-8').read().splitlines()
    ok = ln <= len(lines) and sub in lines[ln - 1]
    check(ok, 'quote @ %s:%d (%d words) present' % (os.path.basename(path), ln, len(sub.split())))
    check(len(sub.split()) <= cap, 'quote @ %s:%d within %d words' % (os.path.basename(path), ln, cap))

# 2. slice file
raw = open(SLICE, 'rb').read()
check(sha(SLICE) == 'd9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d', 'slice sha256')
lines = open(SLICE, encoding='utf-8').read().splitlines()
check(len(lines) == 13, 'slice has 13 data rows (got %d)' % len(lines))
check(all(re.match(r'^\s*S\d{3}`?\s', l) for l in lines), 'every slice line carries an S-id')
check(sum(1 for l in lines if '`' in l.split()[0]) == 7, '7 slice ids carry the register typo backtick')
check(sum(1 for l in lines if l.split()[1] == '`payload-absent`') == 6, '6 payload-absent rows')
check(sum(1 for l in lines if 'could not be fetched' in l) == 2, '2 could-not-be-fetched rows')
check(sum(1 for l in lines if 'named no locator' in l) == 5, '5 gate-block rows')
check(open(SLICE, encoding='utf-8').read() == open(os.path.join(
    LANE, '.ufo/waves/round-43/assimilation/quarantine-slice'), encoding='utf-8').read(),
    'assimilation copy is byte-identical')

# 3. register untouched
check(sha(REG) == '5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833', 'register sha256')
check(len(open(REG, encoding='utf-8').read().splitlines()) == 375, 'register has 375 lines')

# 4. joins, recomputed
out = subprocess.run([sys.executable, os.path.join(W, 'join-evidence.py')],
                     capture_output=True, text=True, check=True).stdout
check('IDJOIN\tEMPTY' in out, 'id-level join is empty')
check("URLJOIN\t['https://blog.csdn.net/2301_76324845/article/details/149787804']" in out,
      'source-level join is exactly the CSDN URL')
check('REGWIDE\tregister_rows_citing_any_theme_source\t1' in out, 'register-wide source join = 1')
check('REGWIDE\tregister_rows_with_id_equal_to_cited_id\t0' in out, 'register has no row with a cited id')

theme = sorted(glob.glob(KN + 'gkeep-*.md')) + [KN + 'glyph-and-geometry-r31.md']
check(len(theme) == 11, 'theme set is 11 files')
srcids = set()
src_lines = 0
for f in theme:
    for ln in open(f, encoding='utf-8'):
        if re.match(r'^source:', ln):
            src_lines += 1
            m = re.search(r'\bS(\d{3})\b', ln)
            if m:
                srcids.add('S' + m.group(1))
check(src_lines == 26, '26 source: lines (%d)' % src_lines)
cited = set()
for f in theme:
    for ln in open(f, encoding='utf-8'):
        cited |= {'S' + m.group(1) for m in re.finditer(r'\bS(\d{3})\b', ln)}
check(len(srcids) == 25, '25 distinct source-line ids (%d)' % len(srcids))
check(len(cited) == 28, '28 distinct ids cited overall (%d)' % len(cited))
check(cited - srcids == {'S216', 'S219', 'S281'}, 'inline-only ids are S216, S219, S281 (%s)' % sorted(cited - srcids))

# 5. the +17 offset for every source-bearing slice row
reg_lines = open(REG, encoding='utf-8').read().splitlines()
staged = {}
for ln in open(APP, encoding='utf-8'):
    if ln.startswith('| S'):
        f = [x.strip() for x in ln.split('|')]
        m = re.match(r'S(\d+)', f[1])
        if m:
            staged['S' + m.group(1)] = f[2]
def doc_of(text):
    m = re.search(r'(https?://\S+|/home/\S+|lanes/\S+)', text)
    return m.group(1).rstrip('.,') if m else ''
doc2staged = {}
for sid, src in staged.items():
    d = doc_of(src)
    if d:
        doc2staged.setdefault(d, sid)
offsets = {}
for ln in reg_lines:
    if '`mado`' not in ln or len([x for x in ln.split('|')]) < 6:
        continue
    f = [x.strip() for x in ln.split('|')]
    rid, src = f[3].rstrip('`'), f[5]
    d = doc_of(src)
    if d and d in doc2staged:
        offsets[rid] = int(doc2staged[d][1:]) - int(rid[1:])
check(len(offsets) == 8, '8 source-bearing slice rows mapped (%d)' % len(offsets))
check(set(offsets.values()) == {17}, 'every offset is +17 (%s)' % offsets)

# 6. lane-registry collisions among the cited ids
lane_ids = set(re.findall(r'^\| (S\d{3,}) \|', open(LANE + '/corpus/SOURCES.md', encoding='utf-8').read(), re.M))
coll = sorted(cited & lane_ids)
check(coll == ['S216', 'S219', 'S281', 'S284', 'S285', 'S286', 'S287'],
      '7 cited ids name a lane row (%s)' % coll)
for sid, subject in [('S216', 'Compositor.cpp'), ('S284', 'FocusGrab.cpp'), ('S285', 'quickshell'),
                     ('S286', 'xdg-desktop-portal-hyprland'), ('S287', 'issues/565')]:
    row = [l for l in open(LANE + '/corpus/SOURCES.md', encoding='utf-8') if l.startswith('| ' + sid + ' |')][0]
    check(subject.lower() in row.lower(), 'lane %s subject is %s' % (sid, subject))

# 7. fetch evidence
stub1, stub2 = os.path.join(W, 'csdn-2301_76324845.body'), os.path.join(W, 'csdn-lxyoucan.body')
check(os.path.getsize(stub1) == 2263 and sha(stub1).startswith('93cf2a5a'), 'S199 stub: 2263 B / 93cf2a5a')
check(os.path.getsize(stub2) == 2167 and sha(stub2).startswith('413000dd'), 'S200 stub: 2167 B / 413000dd')
check('window.onload' in open(stub1, encoding='utf-8', errors='replace').read(), 'stub 1 is the JS challenge, not an article')
proxy = os.path.join(W, 'proxy-149787804.txt')
check(os.path.getsize(proxy) == 71957 and sha(proxy).startswith('81a5e78a'), 'proxy body: 71957 B / 81a5e78a')
check(open(proxy, encoding='utf-8').read().startswith('Title:'), 'proxy body starts with a Title line')
check('windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$' in open(proxy, encoding='utf-8').read().splitlines()[159],
      'proxy body carries the staged row\'s quoted rule at line 160')
r41 = LANE + '/.ufo/waves/round-41/w1/ExecQuarantineSlice/sources/csdn-149787804-via-r.jina.ai.txt'
check(os.path.getsize(r41) == 72130 and sha(r41).startswith('d9b9ebe8'), 'round-41 proxy body: 72130 B / d9b9ebe8')

# 8. the two named files' citation lines
r9 = open(KN + 'gkeep-rendered-geometry-chain-r9.md', encoding='utf-8').read().splitlines()
r11 = open(KN + 'gkeep-size-to-real-size-r11.md', encoding='utf-8').read().splitlines()
check([re.search(r'\bS(\d{3})\b', r9[i - 1]).group(0) for i in range(8, 14)] ==
      ['S284', 'S285', 'S286', 'S287', 'S292', 'S293'], 'r9 source ids at lines 8-13')
check([re.search(r'\bS(\d{3})\b', r11[i - 1]).group(0) for i in range(11, 16)] ==
      ['S302', 'S303', 'S304', 'S305', 'S310'], 'r11 source ids at lines 11-15')

# 9. r9/r11 host artifacts are campaign-only
check(os.path.exists('/home/vgpnk/Projects/shokuknow/lanes/mado/round9/fetch/gkeep-geometry-chain.txt'),
      'round-9 chain artifact exists in the campaign checkout')
check(os.path.exists('/home/vgpnk/Projects/shokuknow/lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt'),
      'round-11 artifact exists in the campaign checkout')
hits = subprocess.run(['bash', '-c',
    'find %s -name gkeep-geometry-chain.txt -o -name host-gkeep-rule-and-path.txt' % LANE],
    capture_output=True, text=True).stdout.strip()
check(hits == '', 'neither artifact exists in the lane tree')

print()
print('FAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
