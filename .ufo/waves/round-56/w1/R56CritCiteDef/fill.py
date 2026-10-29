import json, subprocess, os, sys, re
D=sys.argv[1]; REV="13f0acbe3a15da2d9c08357a576d91dcadc85273"; REPO="/home/vgpnk/Projects/shokunin/mado-shokunin"
env={"PATH":os.environ.get("PATH","/usr/bin:/bin"),"HOME":D,"TMPDIR":D,"LC_ALL":"C"}
def show(p): return subprocess.run(["git","-C",REPO,"show",f"{REV}:{p}"],env=env,capture_output=True,check=True).stdout.decode("utf-8")
d=json.load(open("/fast/scratch/hyaku/mado-r56/R56CritCiteDef/git-env/data.json"))
add={}
for s,e in d["pairs"]: add.setdefault(s,[]).append(e)
src=show("corpus/SOURCES.md").split("\n"); out=[]
for ln in src:
    if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",ln):
        parts=[c for c in ln.strip()[1:-1].split("|")]
        sid=parts[0].strip()
        if sid in add:
            cur=parts[10].strip()
            new=", ".join(([cur] if cur not in ("—","") else [])+add[sid])
            parts[10]=" "+new+" "
            ln="|"+"|".join(parts)+"|"
    out.append(ln)
os.makedirs(os.path.join(D,"corpus/knowledge"),exist_ok=True)
os.makedirs(os.path.join(D,"corpus"),exist_ok=True)
open(os.path.join(D,"corpus/SOURCES.md"),"w",encoding="utf-8").write("\n".join(out))
for e in d["entries"]:
    open(os.path.join(D,e),"w",encoding="utf-8").write(show(e))
print("filled rows:",len(add),"pairs:",sum(len(v) for v in add.values()))
