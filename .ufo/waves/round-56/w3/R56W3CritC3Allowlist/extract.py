import subprocess, re, hashlib, json, os
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"
REV="0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
def show(rev,path):
    r=subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    return r.stdout.decode("utf-8",errors="replace")
tsv=show(REV,".ufo/waves/round-56/c3-name-only.tsv")
rows=[l.split("\t") for l in tsv.split("\n") if l.strip()]
out=[]
for s,entry,sha,reason in rows:
    blob=show(REV,entry)
    lines=blob.split("\n")
    # fence tracking
    infence=False; fence=None; tok=re.compile(r'(?<![A-Za-z0-9])'+re.escape(s)+r'(?![0-9])')
    cite=[]
    for i,l in enumerate(lines,1):
        m=re.match(r'^( {0,3})(`{3,}|~{3,})',l)
        if m:
            f=m.group(2)[0]
            if not infence:
                infence=True; fence=f
            elif f==fence:
                infence=False; fence=None
            continue
        if infence: continue
        if tok.search(l): cite.append((i,l))
    joined="\n".join(l for _,l in cite)
    calc=hashlib.sha256(joined.encode()).hexdigest()
    out.append(dict(S=s,entry=entry,sha_frozen=sha,sha_calc=calc,sha_ok=(calc==sha),reason=reason,cite=cite,nlines=len(lines)))
json.dump(out,open("/fast/scratch/hyaku/mado-r56/R56W3CritC3Allowlist/cite.json","w"),indent=1)
for o in out:
    print("="*100)
    print(o["S"],o["entry"],"sha_ok=",o["sha_ok"], "ncites=",len(o["cite"]))
    print("REASON:",o["reason"][:300])
    for i,l in o["cite"]:
        print(f"  L{i}: {l}")
