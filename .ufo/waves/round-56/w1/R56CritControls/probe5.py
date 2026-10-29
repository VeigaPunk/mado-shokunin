import subprocess, re
R="/home/vgpnk/Projects/shokunin/mado-shokunin"; B="13f0acbe3a15da2d9c08357a576d91dcadc85273"
def git(*a): return subprocess.run(["git","-C",R,*a],capture_output=True).stdout.decode("utf-8","replace")
ls=git("ls-tree","-r","--name-only",B,"--","corpus/knowledge").split()
ents=sorted(p for p in ls if re.fullmatch(r"corpus/knowledge/[^/]+\.md",p))
inline=listform=none=0; dangling_list=[]
for e in ents:
    L=git("show",f"{B}:{e}").split("\n")[:15]
    src=[i for i,l in enumerate(L) if l.startswith("source:")]
    if not src: none+=1; continue
    i=src[0]
    if re.search(r"S[0-9]{3,}",L[i]): inline+=1
    else:
        listform+=1
        items=[l for l in L[i+1:i+6] if re.match(r"\s+-\s+S[0-9]{3,}",l)]
        if items: dangling_list.append(e)
print("entries",len(ents),"source-line inline ids:",inline,"bare source: + YAML list:",listform,"no source line in first 15:",none)
print("first 15 lines: list-form entries with ids only on list items:",len(dangling_list))
