import re, glob, os, sys
lane, oldf, newf = sys.argv[1:4]
def cites(t):
    out=set(); inf=False; ch=None
    for l in t.splitlines():
        m=re.match(r'^ {0,3}(`{3,}|~{3,})',l)
        if m:
            if not inf: inf=True; ch=m.group(1)[0]
            elif m.group(1)[0]==ch: inf=False
            continue
        if not inf: out |= set(re.findall(r'(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])',l))
    return out
ents={}
for p in sorted(glob.glob(lane+'/corpus/knowledge/*.md')):
    if os.path.isfile(p) and not os.path.islink(p): ents['corpus/knowledge/'+os.path.basename(p)]=open(p,encoding='utf-8',errors='replace').read()
def reg(path):
    rows={}
    for l in open(path,encoding='utf-8').read().split('\n'):
        if re.match(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|',l):
            c=l.strip()[1:-1].split('|'); assert len(c)==11
            rows[c[0].strip()]=re.findall(r'corpus/knowledge/[A-Za-z0-9_.-]+\.md',c[10])
    return rows
def count(rows):
    m=x=d=0
    C={e:cites(t) for e,t in ents.items()}
    for e,cs in C.items():
        for s in cs:
            if s in rows and e not in rows[s]: m+=1
        for l in ents[e].split('\n')[:15]:
            if l.startswith('source:'):
                for s in re.findall(r'(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])',l):
                    if s not in rows: d+=1
    for s,ps in rows.items():
        for p in ps:
            if p not in ents or s not in C[p]: x+=1
    return len(ents),len(rows),m,x,d
for n,f in (('old',oldf),('new',newf)):
    print(n,'entries=%d rows=%d missing=%d extra=%d dangling=%d'%count(reg(f)))
# cell-level diff
O=open(oldf,'rb').read().split(b'\n'); N=open(newf,'rb').read().split(b'\n')
assert len(O)==len(N)
chg=[];other=0
for i,(a,b) in enumerate(zip(O,N)):
    if a==b: continue
    ca=a.split(b'|'); cb=b.split(b'|')
    ok = len(ca)==len(cb) and ca[:11]==cb[:11] and ca[12:]==cb[12:] and ca[11]!=cb[11] and cb[11].lstrip().startswith(ca[11].strip())
    chg.append((ca[1].strip().decode(),ok)); other+= (not ok)
print('changed lines',len(chg),'bad (other than cell11 append):',other, 'unique ids',len({c[0] for c in chg}))
