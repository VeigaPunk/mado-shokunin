import os, subprocess, sys, time, resource
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_blow2"
os.makedirs(BASE, exist_ok=True)
N=2000
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = hyprland.conf\n"*N)
print("config size", os.path.getsize(conf))
t0=time.time()
try:
    r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=600)
    print("rc=",r.returncode,"elapsed=%.2fs"%(time.time()-t0),"stdout bytes",len(r.stdout))
    print(r.stdout.decode()[:200])
except subprocess.TimeoutExpired:
    print("TIMEOUT 600s -> unbounded work")
