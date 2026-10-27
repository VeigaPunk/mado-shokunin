import importlib.util, json, os, shutil
S="/fast/scratch/hyaku/mado-r48/CritC1OneByte"; R=S+"/repo/r48"
def load(n,p):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr=load("ctr",R+"/quality/counters/c1-r48-terminal-cache.py")
FX={f["id"]:f for f in json.loads(open(R+"/quality/counters/c1-r48-fixtures.json","rb").read())}
box=ctr.Box(S+"/work", R+"/tools/mado-terminal.py")
WD=S+"/work/dbg3"; shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
case=FX["W-02"]; root=WD+"/r"
ctr.prepare(box, root, case, "C.UTF-8")
print("cache_host:", ctr.cache_host(root), os.path.isfile(ctr.cache_host(root)))
env=ctr.case_env(case, root, "C.UTF-8", "scored")
print("env XDG_CACHE_HOME", env.get("XDG_CACHE_HOME"))
p=box.argv(root, env, True, ["explain"])
print("bwrap argv:", " ".join(p[:40]))
import subprocess
r=subprocess.run(p, capture_output=True, env={"PATH":"/usr/bin"})
print("rc",r.returncode)
print(r.stdout.decode()[:2000])
