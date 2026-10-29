import re,subprocess,sys,os
repo,rev=sys.argv[1],sys.argv[2]
def git(*a):
    return subprocess.run(["git","-C",repo,*a],capture_output=True,check=True).stdout.decode()
ents=[l.split('\t',1)[1] for l in git("ls-tree","--full-tree",rev,"corpus/knowledge/").splitlines() if l.split()[1]=="blob" and l.endswith(".md") and l.split('\t',1)[1].count('/')==2]
ids_re=re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
rows={}
for l in git("show",f"{rev}:corpus/SOURCES.md").splitlines():
    if ids_re.match(l):
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        assert len(c)==11,(c[0],len(c))
        rows[c[0]]=c
cite_re=re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
def cites(text):
    out=set();fence=None
    for l in text.splitlines():
        m=re.match(r"^ {0,3}(```|~~~)",l)
        if m:
            fence = None if fence==m.group(1) else (fence or m.group(1)); continue
        if fence is None: out|=set(cite_re.findall(l))
    return out
def src(text):
    s=set()
    for l in text.splitlines()[:15]:
        if l.startswith("source:"): s|=set(cite_re.findall(l))
    return s
C={p:cites(git("show",f"{rev}:{p}")) for p in ents}
U={sid:set(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md",c[10])) for sid,c in rows.items()}
missing=sum(1 for p in ents for s in C[p] if s in rows and p not in U[s])
extra=sum(1 for sid in rows for p in U[sid] if p not in C or sid not in C[p])
dang=sum(1 for p in ents for s in src(git("show",f"{rev}:{p}")) if s not in rows)
print(f"entries={len(ents)} rows={len(rows)} missing={missing} extra={extra} dangling={dang}")
