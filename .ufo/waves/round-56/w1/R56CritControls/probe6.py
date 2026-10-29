import subprocess, re
R="/home/vgpnk/Projects/shokunin/mado-shokunin"; B="13f0acbe3a15da2d9c08357a576d91dcadc85273"
def git(*a): return subprocess.run(["git","-C",R,*a],capture_output=True).stdout.decode("utf-8","replace")
reg=set(re.findall(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|",git("show",f"{B}:corpus/SOURCES.md"),re.M))
ls=git("ls-tree","-r","--name-only",B,"--","corpus/knowledge").split()
ents=sorted(p for p in ls if re.fullmatch(r"corpus/knowledge/[^/]+\.md",p))
none=[]
for e in ents:
    T=git("show",f"{B}:{e}").split("\n"); L=T[:15]
    if not any(l.startswith("source:") for l in L): none.append((e,[l[:60] for l in T[:4]]))
    else:
        i=[k for k,l in enumerate(L) if l.startswith("source:")][0]
        if not re.search(r"S[0-9]{3,}",L[i]):
            ids=[m for l in T[i+1:i+8] for m in re.findall(r"S[0-9]{3,}",l)]
            print("list-form",e,"ids",ids,"nonregistry",[x for x in ids if x not in reg])
print("entries without source: line in first 15:",len(none))
for e,h in none[:3]: print(e,h)
print("sources-like keys in those:",sum(1 for e,_ in none if any(re.match(r"(?i)sources?\b", l) for l in git("show",f"{B}:{e}").split("\n")[:40])))
