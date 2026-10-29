import subprocess, re, sys, json
R="/home/vgpnk/Projects/shokunin/mado-shokunin"; B="13f0acbe3a15da2d9c08357a576d91dcadc85273"; C="3423ae285676c2a10273000f4519163472b443db"
def git(*a): return subprocess.run(["git","-C",R,*a],capture_output=True).stdout
def show(rev,p): return git("show",f"{rev}:{p}").decode("utf-8","replace")
ls = git("ls-tree","-r","--name-only",B,"--","corpus/knowledge").decode().split()
ents = sorted(p for p in ls if re.fullmatch(r"corpus/knowledge/[^/]+\.md",p))
print("entries base:",len(ents)); print("first 3 sorted:",ents[:3])
first=ents[0]; txt=show(B,first); L=txt.split("\n")
print("first entry source lines (1-based, within 15):",[ (i+1,l[:120]) for i,l in enumerate(L[:15]) if l.startswith("source:")])
print("first entry source lines anywhere:",[ (i+1,l[:100]) for i,l in enumerate(L) if l.startswith("source:")])
reg = show(B,"corpus/SOURCES.md").split("\n")
rows=[]
for l in reg:
    if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",l):
        cells=l.strip().strip("|").split("|")
        rows.append((cells[0].strip(),len(cells),cells))
print("registry rows:",len(rows),"cellcounts:",sorted({r[1] for r in rows}))
print("S001 present:",[r[0] for r in rows if r[0]=="S001"], "S001 usedby:", [r[2][10].strip()[:200] for r in rows if r[0]=="S001"])
# CITE per entry at base
fence=re.compile(r"^ {0,3}(```|~~~)")
def cites(text):
    out=[];infence=False;cnt={}
    for i,l in enumerate(text.split("\n")):
        if fence.match(l): infence=not infence; continue
        if infence: continue
        for t in re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])",l):
            cnt.setdefault(t,[]).append(i+1)
    return cnt
allcites={}
for e in ents: allcites[e]=cites(show(B,e))
regids={r[0] for r in rows}
pairs=[(s,e) for e in ents for s in allcites[e] if s in regids]
print("CITE pairs with registry id:",len(pairs))
print("first entry cites:",{k:v for k,v in allcites[first].items()})
# candidate for fenced-cite: exactly once on non-fence line
cands=[(s,e,v[0]) for e in ents for s,v in sorted(allcites[e].items()) if s in regids and len(v)==1]
print("fenced-cite candidates (exactly-once, registry id):",len(cands), "first 3:",sorted(cands)[:3])
# which entries cite S001..
print("entries with no citation of a registry id (base):", sum(1 for e in ents if not any(s in regids for s in allcites[e])))
# does first entry cite anything in registry
print("first-entry registry cites:",[s for s in allcites[first] if s in regids])
# dangling check: source tokens in first 15 lines
src=[]
for l in L[:15]:
    if l.startswith("source:"): src+=re.findall(r"S[0-9]{3,}",l)
print("first entry SRC tokens:",src, "in registry?", [s in regids for s in src])
