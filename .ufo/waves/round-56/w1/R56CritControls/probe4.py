import json, subprocess, shutil, re
from pathlib import Path
SC=Path("/fast/scratch/hyaku/mado-r56/R56CritControls"); W=SC/"x/.ufo/waves/round-56"; T=json.load(open(W/"frozen-tables.json"))
ROOT=SC/"probe_export2"
def export(strip):
    if ROOT.exists(): shutil.rmtree(ROOT)
    shutil.copytree(W/"fixtures"/"c2", ROOT/"fixtures"/"c2", symlinks=True)
    shutil.copytree(W/"fixtures"/"c2"/"F01", ROOT/"fixtures"/"c2-holdout"/"H01", symlinks=True)  # synthetic layout-twin, not the sealed set
    shutil.copytree(W/"ctl", ROOT/"ctl"); shutil.copy(SC/"sib-expected.py", ROOT/"ctl"/"sib-expected.py")
    if strip:
        for p in list(ROOT.rglob("expected.*"))+list(ROOT.rglob("note.txt")): p.unlink()
def run(stub, fxdir, fx):
    args=[a.replace("{FX}",str(fxdir)) for a in json.load(open(W/"fixtures"/"c2"/fx/"args.json"))]
    p=subprocess.run(["python3","-I",str(ROOT/"ctl"/stub),*args],cwd=ROOT,capture_output=True,env={"PATH":"/usr/bin:/bin"})
    eo=fxdir/"expected.out"; ec=fxdir/"expected.rc"
    # expected lives in the LANE copy (ground truth), not in the export under test
    gt=W/"fixtures"/"c2"/fx
    return p.stdout==(gt/"expected.out").read_bytes() and p.returncode==int((gt/"expected.rc").read_text().strip())
fxs=sorted(d.name for d in (W/"fixtures"/"c2").iterdir() if d.is_dir())
for strip in (False,True):
    export(strip)
    res=[run("sib-expected.py", ROOT/"fixtures"/"c2"/f, f) for f in fxs]
    h=run("sib-expected.py", ROOT/"fixtures"/"c2-holdout"/"H01", "F01")
    print(f"sibling-reader strip={strip}: committed {sum(res)}/18, synthetic-layout-twin {int(h)}/1")
# Quote-echo vs placeholder: lexical legs only (row grammar, quote, tok, num, length, uniqueness)
def toks(s): return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}",s))
def digs(s): return set(re.findall(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])",s))
def legs(variant):
    rows=T["c1"]["k"]+T["c1"]["h"]; props={}; ok={"row":0,"quote":0,"tok":0,"num":0,"len":0}
    for r in rows:
        K=r["id"].startswith("K")
        if variant=="placeholder":
            p=(f"placeholder proposition text for row {r['id']}, not a claim about any source line" if K else f"placeholder host proposition {r['id']}, not a read")
        else:  # quote-echo: copy the frozen quote and pad it to the length floor
            p=f"{r['quote']} (row {r['id']} restates the frozen quote line)"
        minlen=40 if K else 20
        allowed=digs(r["quote"])|{str(r["line"]),"0","1","2","3"}|{str(x["line"]) for x in rows if x["pin"]==r["pin"]}
        ok["row"]+=1  # row grammar is independent of proposition text in this sketch
        ok["quote"]+=1
        ok["len"]+= len(p)>=minlen and p==p.strip() and p not in props.values()
        ok["tok"]+= bool(toks(p)&toks(r["quote"]))
        ok["num"]+= digs(p)<=allowed
        props[r["id"]]=p
    return ok
for v in ("placeholder","quote-echo"):
    o=legs(v); print(v, {k:f"{n}/33" for k,n in o.items()}, "content(tok&num)=", "n/a per-row computed separately")
