import re, shutil, subprocess, pathlib, sys
S=pathlib.Path('.ufo/waves/round-35/scratch/RevRowsUsedBy')
BASE=S/'base'
COUNTER='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/count.py'
FROZEN='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/frozen.json'
SIDS=[f"S20{i}" for i in range(3,10)]+["S210"]
R12='corpus/knowledge/idle-lock-never-asked-r12.md'
R14='corpus/knowledge/idle-lock-chain-armed-r14.md'
R15='corpus/knowledge/idle-lock-offered-in-the-bar-r15.md'

def build(name, fn):
    d=S/('m-'+name)
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(BASE,d)
    fn(d)
    p=subprocess.run(['python3','-I',COUNTER,'--root',str(d),'--frozen',FROZEN],capture_output=True,text=True)
    out=(p.stdout+p.stderr).strip().replace('\n',' | ')
    print(f"{name:28} exit={p.returncode} {out}")
    return p.returncode,out

def edit(path, f):
    p=pathlib.Path(path); t=p.read_text(); p.write_text(f(t))

def drop_source(entry,sid):
    def f(d):
        def g(t):
            return '\n'.join(l for l in t.splitlines() if not l.startswith(f'source: {sid} '))+'\n'
        edit(d/entry,g)
    return f

def retag_source(entry,sid,new):
    def f(d):
        edit(d/entry, lambda t: t.replace(f'source: {sid} ', f'source: {new} ',1))
    return f

def add_source(entry,line,after=None):
    def f(d):
        def g(t):
            lines=t.splitlines()
            idx=len(lines)-1
            for i,l in enumerate(lines):
                if after and l.startswith(after): idx=i
            lines.insert(idx+1,line)
            return '\n'.join(lines)+'\n'
        edit(d/entry,g)
    return f

def rowop(sid, idx, val):
    def f(d):
        def g(t):
            out=[]
            for l in t.splitlines():
                m=re.match(r"^ {0,3}\|\s*(S[0-9]+)\s*\|",l)
                if m and m.group(1)==sid:
                    parts=l.split('|')
                    # parts[0]='' then cells start at 1
                    parts[idx+1]=f' {val} '
                    l='|'.join(parts)
                out.append(l)
            return '\n'.join(out)+'\n'
        edit(d/'corpus/SOURCES.md',g)
    return f

def allrows(idx, val):
    def f(d):
        def g(t):
            out=[]
            for l in t.splitlines():
                m=re.match(r"^ {0,3}\|\s*(S[0-9]+)\s*\|",l)
                if m and m.group(1) in SIDS:
                    parts=l.split('|'); parts[idx+1]=f' {val} '; l='|'.join(parts)
                out.append(l)
            return '\n'.join(out)+'\n'
        edit(d/'corpus/SOURCES.md',g)
    return f

def chain(d):
    pass

tests=[]
tests.append(('src-drop-S204', drop_source(R12,'S204')))
tests.append(('src-retag-S204-S999', retag_source(R12,'S204','S999')))
tests.append(('src-add-S999-r12', add_source(R12,'source: S999 - scratch-mutant','source: S204')))
tests.append(('src-add-S204-r15', add_source(R15,'source: S204 - scratch-mutant','source: S210')))
tests.append(('src-drop-all-S205', drop_source(R14,'S205')))
def dup(d):
    edit(d/R12, lambda t: t.replace('source: S203 - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run','source: S203 - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run\nsource: S203 - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run',1))
tests.append(('src-dup-S203', dup))
tests.append(('opened-1999', allrows(8,'1999-01-01')))
tests.append(('opened-garbage', allrows(8,'not-a-date')))
tests.append(('opened-future', allrows(8,'2099-01-01')))
tests.append(('opened-empty', allrows(8,'')))
tests.append(('recheck-banana', rowop('S205',9,'banana')))
tests.append(('recheck-zero-d', rowop('S205',9,'0d')))
tests.append(('recheck-space', rowop('S205',9,'on change')))
tests.append(('recheck-empty', rowop('S205',9,'')))
tests.append(('status-Mined', rowop('S205',7,'Mined')))
tests.append(('status-queued', rowop('S205',7,'queued')))
tests.append(('usedby-dupe', rowop('S206',10,'corpus/knowledge/idle-lock-offered-in-the-bar-r15.md, corpus/knowledge/idle-lock-offered-in-the-bar-r15.md')))
tests.append(('usedby-trailing-comma', rowop('S203',10,'corpus/knowledge/idle-lock-never-asked-r12.md,')))
tests.append(('usedby-reorder', rowop('S206',10,'corpus/knowledge/idle-lock-offered-in-the-bar-r15.md')))
tests.append(('usedby-lesson', rowop('S209',10,'corpus/lessons/round-34.md')))
tests.append(('usedby-dotprefix', rowop('S203',10,'./corpus/knowledge/idle-lock-never-asked-r12.md')))
tests.append(('usedby-absolute', rowop('S203',10,'/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/idle-lock-never-asked-r12.md')))
tests.append(('usedby-space-sep', rowop('S203',10,'corpus/knowledge/idle-lock-never-asked-r12.md corpus/knowledge/idle-lock-chain-armed-r14.md')))
tests.append(('usedby-percent', rowop('S203',10,'corpus/knowledge/idle-lock-never-asked-r12.md%00')))
def entryrecheck(d):
    edit(d/R14, lambda t: t.replace('recheck: 90d','recheck: garbage-token',1))
tests.append(('entry-recheck-garbage', entryrecheck))
def entryrecheck2(d):
    edit(d/R15, lambda t: t.replace('recheck: on-change','recheck: 0d',1))
tests.append(('entry-recheck-zero', entryrecheck2))

for name,fn in tests:
    build(name,fn)
