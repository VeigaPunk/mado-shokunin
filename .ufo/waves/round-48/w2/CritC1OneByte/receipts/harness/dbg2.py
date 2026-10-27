import importlib.util, json, os, shutil, subprocess
S="/fast/scratch/hyaku/mado-r48/CritC1OneByte"; R=S+"/repo/r48"
def load(n,p):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr=load("ctr",R+"/quality/counters/c1-r48-terminal-cache.py")
FX={f["id"]:f for f in json.loads(open(R+"/quality/counters/c1-r48-fixtures.json","rb").read())}
box=ctr.Box(S+"/work", R+"/tools/mado-terminal.py")
WD=S+"/work/dbg2"; shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
for fid in ("W-02","W-14"):
    case=FX[fid]; root=WD+"/"+fid+"/r"
    ctr.prepare(box, root, case, "C.UTF-8")
    data=open(ctr.cache_host(root),"rb").read()
    print("===",fid,case["class"],"state_field=",case.get("state"),"args=",case["args"],"after=",json.dumps(case.get("after") or {})[:160])
    for i,ln in enumerate(data.split(b"\n"),1): print("  %2d %r"%(i,ln))
    env=ctr.case_env(case,root,"C.UTF-8","scored")
    rc,out,err=box.run(root,env,True,["explain"])
    print("  explain rc=%d tail=%r"%(rc,out.split("MADO_TERM_TRACE")[-1][-200:]))
    print("  pin", ctr.oracle_side(box,case,root,"C.UTF-8"))
