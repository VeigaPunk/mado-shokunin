import importlib.util, json, os
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n,p):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr=load("ctr",R+"/quality/counters/c1-r48-terminal-cache.py"); tool=load("tool",R+"/tools/mado-terminal.py")
FX={f["id"]:f for f in json.loads(open(R+"/quality/counters/c1-r48-fixtures.json","rb").read())}
fid="v2-wd-01-exec-firstword"; case=FX[fid]
root=S+"/work/fast/"+fid+"/r"
data=open(ctr.cache_host(root),"rb").read()
print("cache line1 %r" % data.split(b"\n")[0])
et=ctr.case_env(case,root,"C.UTF-8","scored")
cwd=os.getcwd(); os.chdir(root)
r=tool.Resolver(et)
r.t=lambda *a,**k: None
print("gen_hash  %r" % r.gen_hash())
print("cmp %r" % (r.gen_hash()==data.split(b"\n")[0].decode("latin-1")))
os.chdir(cwd)
