#!/usr/bin/env python3
"""Re-run of the RevRowsUsedBy mutation battery on the CURRENT lane bytes.

Original battery: .ufo/waves/round-35/scratch-evidence/RevRowsUsedBy/evidence.txt
(sha256 3dd4a384…, written 03:43 from the 03:36 observation). That run's tree is
gone; this one is a re-run on the bytes that exist now, kept separate so the
report can say which number came from which state.
"""
import pathlib, re, shutil, subprocess, sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
E = LANE / '.ufo/waves/round-35/scratch-evidence/RevRowsUsedBy'
BASE = E / 'base-now'
COUNTER = str(LANE / '.ufo/waves/round-35/c1/count.py')
FROZEN = str(LANE / '.ufo/waves/round-35/c1/frozen.json')
SIDS = [f'S20{i}' for i in range(3, 10)] + ['S210']
R12 = 'corpus/knowledge/idle-lock-never-asked-r12.md'
R14 = 'corpus/knowledge/idle-lock-chain-armed-r14.md'
R15 = 'corpus/knowledge/idle-lock-offered-in-the-bar-r15.md'
RECEIPTS = [f'S20{i}' for i in range(3, 10)] + ['S210']

def make_base():
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / 'corpus/knowledge').mkdir(parents=True)
    (BASE / '.ufo/waves/round-35/fetch').mkdir(parents=True)
    shutil.copy(LANE / 'corpus/SOURCES.md', BASE / 'corpus/SOURCES.md')
    for f in (R12, R14, R15):
        shutil.copy(LANE / f, BASE / f)
    for s in RECEIPTS:
        shutil.copy(LANE / f'.ufo/waves/round-35/fetch/{s}.receipt.txt',
                    BASE / f'.ufo/waves/round-35/fetch/{s}.receipt.txt')

def score(root):
    p = subprocess.run(['python3', '-I', COUNTER, '--root', str(root),
                        '--frozen', FROZEN], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()

def build(name, fn):
    d = E / ('m-' + name)
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(BASE, d)
    fn(d)
    rc, out = score(d)
    print(f'{name:26} exit={rc} {out}')

def edit(path, f):
    p = pathlib.Path(path)
    p.write_text(f(p.read_text()))

def drop_source(entry, sid):
    def f(d):
        edit(d / entry, lambda t: '\n'.join(
            l for l in t.splitlines() if not l.startswith(f'source: {sid} ')) + '\n')
    return f

def retag_source(entry, sid, new):
    def f(d):
        edit(d / entry, lambda t: t.replace(f'source: {sid} ', f'source: {new} ', 1))
    return f

def add_source(entry, line, after):
    def f(d):
        def g(t):
            ls = t.splitlines()
            i = max(j for j, l in enumerate(ls) if l.startswith(after))
            ls.insert(i + 1, line)
            return '\n'.join(ls) + '\n'
        edit(d / entry, g)
    return f

def rowop(sid, idx, val):
    def f(d):
        def g(t):
            out = []
            for l in t.splitlines():
                m = re.match(r'^ {0,3}\|\s*(S[0-9]+)\s*\|', l)
                if m and m.group(1) == sid:
                    parts = l.split('|')
                    parts[idx + 1] = f' {val} '
                    l = '|'.join(parts)
                out.append(l)
            return '\n'.join(out) + '\n'
        edit(d / 'corpus/SOURCES.md', g)
    return f

def allrows(idx, val):
    return lambda d: [rowop(s, idx, val)(d) for s in SIDS]

def main():
    make_base()
    rc, out = score(BASE)
    print(f'{"base-now (unmutated)":26} exit={rc} {out}')
    tests = [
        ('src-drop-S204', drop_source(R12, 'S204')),
        ('src-retag-S204-S999', retag_source(R12, 'S204', 'S999')),
        ('src-add-S204-r15', add_source(R15, 'source: S204 - scratch-mutant', 'source: S210')),
        ('src-drop-all-S205', drop_source(R14, 'S205')),
        ('opened-1999', allrows(8, '1999-01-01')),
        ('opened-future', allrows(8, '2099-01-01')),
        ('opened-garbage', allrows(8, 'not-a-date')),
        ('opened-empty', allrows(8, '')),
        ('recheck-banana', rowop('S205', 9, 'banana')),
        ('recheck-zero-d', rowop('S205', 9, '0d')),
        ('recheck-space', rowop('S205', 9, 'on change')),
        ('recheck-empty', rowop('S205', 9, '')),
        ('status-Mined', rowop('S205', 7, 'Mined')),
        ('status-queued', rowop('S205', 7, 'queued')),
        ('usedby-dupe', rowop('S206', 10, 'corpus/knowledge/idle-lock-offered-in-the-bar-r15.md, corpus/knowledge/idle-lock-offered-in-the-bar-r15.md')),
        ('usedby-reorder', rowop('S206', 10, 'corpus/knowledge/idle-lock-offered-in-the-bar-r15.md')),
        ('usedby-lesson', rowop('S209', 10, 'corpus/lessons/round-35.md')),
        ('usedby-dotprefix', rowop('S203', 10, './corpus/knowledge/idle-lock-never-asked-r12.md')),
        ('usedby-absolute', rowop('S203', 10, '/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/idle-lock-never-asked-r12.md')),
    ]
    for name, fn in tests:
        build(name, fn)

if __name__ == '__main__':
    main()
