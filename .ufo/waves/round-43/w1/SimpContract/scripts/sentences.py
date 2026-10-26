import ast, re, sys, json
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"
cnt=open(LANE+"/quality/counters/c1-r42-geometry.py").read()
ref=open(LANE+"/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt").read()
def doc(src):
    m=ast.parse(src)
    return ast.get_docstring(m, clean=False)
cd, rd = doc(cnt), doc(ref)
def sents(t):
    # split on sentence enders followed by whitespace, keeping order; normalize whitespace
    t = re.sub(r"[ \t]+", " ", t)
    parts = re.split(r"(?<=[.:])\s+(?=[A-Z\"`(])", t)
    out=[]
    for p in parts:
        # further split on "; " only when it starts a new clause? no: keep
        p=" ".join(p.split())
        if p: out.append(p)
    return out
cs, rs = sents(cd), sents(rd)
json.dump({"counter":cs,"ref":rs}, open("sentences.json","w"), indent=1)
print("counter sentences:", len(cs), "ref sentences:", len(rs))
for i,s in enumerate(cs,1): print("C%02d %s"%(i,s))
