# Seat-local re-implementation of registration §C3 definitions (read-only, git objects at --rev).
import re, subprocess, sys, os, argparse
ap=argparse.ArgumentParser(); ap.add_argument("--repo",required=True); ap.add_argument("--rev",required=True); ap.add_argument("--work",required=True)
a=ap.parse_args()
os.makedirs(a.work,exist_ok=True)
env={"PATH":os.environ.get("PATH","/usr/bin:/bin"),"HOME":a.work,"TMPDIR":a.work,"LC_ALL":"C"}
def git(*x):
    r=subprocess.run(["git","-C",a.repo,*x],env=env,capture_output=True)
    if r.returncode!=0: sys.exit(2)
    return r.stdout.decode("utf-8","replace")
ents=[]
for ln in git("ls-tree","-r",a.rev,"--","corpus/knowledge").splitlines():
    meta,p=ln.split("\t",1); mode,typ,_=meta.split()
    if typ=="blob" and mode in("100644","100755") and re.fullmatch(r"corpus/knowledge/[^/]+\.md",p): ents.append(p)
rows={}
for ln in git("show",f"{a.rev}:corpus/SOURCES.md").split("\n"):
    if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|",ln):
        parts=[c.strip() for c in ln.strip()[1:-1].split("|")]
        if len(parts)!=11: sys.exit(2)
        rows[parts[0]]=parts
fence=re.compile(r"^ {0,3}(```|~~~)")
def cites(t):
    out=set(); inf=False; fc=None
    for ln in t.split("\n"):
        m=fence.match(ln)
        if m:
            if not inf: inf=True; fc=m.group(1)
            elif m.group(1)==fc: inf=False
            continue
        if not inf: out|=set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])",ln))
    return out
def src(t):
    out=set()
    for ln in t.split("\n")[:15]:
        if ln.startswith("source:"): out|=set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])",ln))
    return out
CITE={}; SRC={}
for e in ents:
    t=git("show",f"{a.rev}:{e}"); CITE[e]=cites(t); SRC[e]=src(t)
USED={s:set(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md",rows[s][10])) for s in rows}
missing=[(s,e) for e in ents for s in CITE[e] if s in rows and e not in USED[s]]
extra=[(s,p) for s in USED for p in USED[s] if p not in ents or s not in CITE.get(p,set())]
dangling=[(e,s) for e in ents for s in SRC[e] if s not in rows]
m,x,d=len(missing),len(extra),len(dangling)
verdict="TARGET_MET" if (m,x,d)==(0,0,0) else "TARGET_MISSED"
mis=",".join(n for n,v in [("missing",m),("extra",x),("dangling",d)] if v) or "none"
print(f"MADO_USED_BY: rev={a.rev} entries={len(ents)} rows={len(rows)} missing={m} extra={x} dangling={d} verdict={verdict} missed={mis}")
sys.exit(0 if verdict=="TARGET_MET" else 1)
