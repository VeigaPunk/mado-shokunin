import re,subprocess,hashlib,sys,os
L="/home/vgpnk/Projects/shokunin/mado-shokunin"
REV="13f0acbe3a15da2d9c08357a576d91dcadc85273"
def g(args): 
    return subprocess.run(["git","-C",L]+args,capture_output=True,check=True).stdout
def blob(path): return g(["cat-file","blob",f"{REV}:{path}"]).decode("utf-8")
ents=[]
for line in g(["ls-tree","-r","--name-only",REV,"--","corpus/knowledge/"]).decode().split("\n"):
    if line and re.fullmatch(r"corpus/knowledge/[^/]+\.md",line): ents.append(line)
print("entries",len(ents))
cite_re=re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
fence=re.compile(r"^ {0,3}(```|~~~)")
def cites(text):
    out=set(); infence=False
    for ln in text.split("\n"):
        if fence.match(ln): infence=not infence; continue
        if infence: continue
        out|=set(cite_re.findall(ln))
    return out
src=blob("corpus/SOURCES.md").split("\n")
rows=[]
for ln in src:
    if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",ln):
        cells=ln.strip().strip("|").split("|")
        rows.append((cells[0].strip(),cells))
ids={r[0] for r in rows}
print("rows",len(rows), "cellcounts", sorted({len(c) for _,c in rows}))
usedby={}
for rid,cells in rows:
    usedby[rid]=set(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md",cells[10] if len(cells)>10 else ""))
pairs=set()
for e in ents:
    for s in cites(blob(e)):
        if s in ids: pairs.add((s,e))
print("PAIRS(base)",len(pairs))
missing=sorted((s,e) for (s,e) in pairs if e not in usedby.get(s,set()))
print("missing(base, all pairs)",len(missing))
def h(lst): return hashlib.sha256("".join(f"{s}|{e}\n" for s,e in lst).encode()).hexdigest()
print("sha(missing 65-ish)",h(missing))
print("sha(all PAIRS(base))",h(sorted(pairs)))
open("/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/base-missing.tsv","w").write("".join(f"{s}\t{e}\n" for s,e in missing))
open("/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/base-pairs.tsv","w").write("".join(f"{s}\t{e}\n" for s,e in sorted(pairs)))
