#!/usr/bin/env python3
"""calibrate-anchors.py — round 50, w2 seat ScrQuoteVerify2 (calibration note, read-only).

Same anchor-coverage rule as verify-quotes-committed.sh, applied to three entries that
predate round 50, to show how often a knowledge entry cites a pin line outside the anchor
cell of every registry row that names that pin file. Committed bytes only (`git show`).
"""
import re, subprocess

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = 'b4a79843cc2545bbe800db9322e58f6e00436629'

def blob(p):
    return subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{p}'],
                          capture_output=True, text=True, check=True).stdout

reg = blob('corpus/SOURCES.md').split('## Registry', 1)[1].split('\n## ', 1)[0]
rows = {}
for r in reg.splitlines():
    m = re.match(r'\|\s*(S\d+)\s*\|', r)
    if m:
        rows[m.group(1)] = r.split('|')

def anchors(row):
    return row[6]

def covers(f, line, acell):
    if re.search(re.escape(f) + r' whole file', acell):
        return True
    for m in re.finditer(r'([A-Za-z0-9._-]+):(\d+)(?:-(\d+))?', acell):
        if m.group(1).split('/')[-1] != f:
            continue
        lo = int(m.group(2)); hi = int(m.group(3) or m.group(2))
        if lo <= line <= hi:
            return True
    return False

anchor_files = {m.group(1).split('/')[-1]
                for r in rows.values()
                for m in re.finditer(r'([A-Za-z0-9._-]+):\d+', anchors(r))}

for path in ('corpus/knowledge/hyprland-input-devices-r46.md',
             'corpus/knowledge/keybind-rule-semantics.md',
             'corpus/knowledge/bind-table-r25.md',
             'corpus/knowledge/hyprland-bind-key-match-r50.md'):
    txt = blob(path)
    cites = []
    for i, l in enumerate(txt.splitlines(), 1):
        for m in re.finditer(r'([A-Za-z0-9._-]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?', l):
            f = m.group(1).split('/')[-1]
            if f in anchor_files:
                cites.append((i, f, int(m.group(2)), int(m.group(3) or m.group(2))))
    unc = [c for c in cites
           if not any(all(covers(c[1], x, anchors(r)) for x in range(c[2], c[3] + 1))
                      for r in rows.values())]
    print(f'{path}: cites_whose_file_a_row_anchors={len(cites)} uncovered={len(unc)}')
    for c in unc:
        print(f'  entry:{c[0]} {c[1]}:{c[2]}' + (f'-{c[3]}' if c[3] != c[2] else ''))
