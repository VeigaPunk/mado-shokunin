import re,subprocess,sys,json
D="/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/m1"; R=D+"/repo"
def g(a,cwd=R): return subprocess.run(["git","-C",cwd]+a,capture_output=True,check=True).stdout.decode("utf-8")
rev="28fc86ac2359ec27406d8a2c63bef82ea6e947ed"; base="13f0acbe3a15da2d9c08357a576d91dcadc85273"
cite_re=re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
fence=re.compile(r"^ {0,3}(```|~~~)")
def cites(text):
    out=set(); inf=False
    for ln in text.split("\n"):
        if fence.match(ln): inf=not inf; continue
        if inf: continue
        out|=set(cite_re.findall(ln))
    return out
def pairs(rv):
    ents=[l for l in g(["ls-tree","-r","--name-only",rv,"--","corpus/knowledge/"],R).split("\n") if re.fullmatch(r"corpus/knowledge/[^/]+\.md",l)]
    src=g(["show",f"{rv}:corpus/SOURCES.md"],R).split("\n")
    ids=set(re.findall(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|",x)[0] for x in src if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",x))
    P=set()
    for e in ents:
        t=g(["show",f"{rv}:{e}"],R)
        for s in cites(t):
            if s in ids: P.add((s,e))
    return P,ents,ids
Pb,_,_=pairs(base); Pr,ents,ids=pairs(rev)
src=g(["show",f"{rev}:corpus/SOURCES.md"],R)
ub={}
for ln in src.split("\n"):
    if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",ln):
        cells=ln.strip().strip("|").split("|")
        ub[cells[0].strip()]=set(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md",cells[10]))
allow=set(tuple(l.split("\t")[:2]) for l in open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/c3-name-only.tsv").read().strip().split("\n"))
base_missing=set((s,e) for (s,e) in Pb if e not in ub.get(s,set()) )
# candidates: used at rev, not allow, not base-missing, single S occurrence in entry
cand=[]
for (s,e) in sorted(Pr):
    if e in ub.get(s,set()) and (s,e) not in allow and (s,e) not in base_missing:
        t=g(["show",f"{rev}:{e}"],R)
        if len(re.findall(r"(?<![A-Za-z0-9])"+s+r"(?![0-9])",t))==1:
            cand.append((s,e))
print("candidates",len(cand), cand[:5])
s,e=cand[0]
print("CHOSEN",s,e, "in PairsBase:", (s,e) in Pb, "in base_missing:", (s,e) in base_missing)
open(D+"/chosen.json","w").write(json.dumps({"s":s,"e":e}))
# mutate entry: replace the single S token
t=g(["show",f"{rev}:{e}"],R)
t2=re.sub(r"(?<![A-Za-z0-9])"+s+r"(?![0-9])", s[0]+"---", t)
open(R+"/"+e,"w",encoding="utf-8").write(t2)
# mutate registry: remove e from row s cell 11
srcl=src.split("\n"); out=[]
for ln in srcl:
    if re.match(r"^ {0,3}\|\s*"+s+r"\s*\|",ln):
        cells=ln.split("|")
        # cells list includes empty leading/trailing; find the cell index holding used-by (11th after strip)
        inner=ln.strip()
        parts=inner.strip("|").split("|")
        assert len(parts)==11, len(parts)
        parts[10]=re.sub(r"\s*"+re.escape(e)+r"\s*,?", "", parts[10]).strip().strip(",").strip()
        ln="| "+" | ".join(p.strip() for p in parts)+" |"
        print("NEW ROW:",ln[:400]); print("OLD USEDBY:",sorted(ub[s]))
    out.append(ln)
open(R+"/corpus/SOURCES.md","w",encoding="utf-8").write("\n".join(out))
print("git status:"); print(g(["status","--short"],R))
