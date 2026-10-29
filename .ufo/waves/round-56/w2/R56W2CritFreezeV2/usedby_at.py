import subprocess,re,sys
L="/home/vgpnk/Projects/shokunin/mado-shokunin"
def rows(rev):
    t=subprocess.run(["git","-C",L,"show",f"{rev}:corpus/SOURCES.md"],capture_output=True,check=True).stdout.decode()
    out={}
    for ln in t.split("\n"):
        if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",ln):
            c=[x.strip() for x in ln.strip().strip("|").split("|")]; out[c[0]]=c[10] if len(c)>10 else ""
    return out
b=rows("13f0acbe"); f=rows("323a69c9"); a=rows("2aa347b1")
print("used-by cells changed base->2aa347b1:",sum(1 for k in b if b[k]!=a.get(k)))
print("used-by cells changed base->323a69c9 (freeze v2):",sum(1 for k in b if b[k]!=f.get(k)))
