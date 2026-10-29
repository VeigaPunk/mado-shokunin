import os, subprocess, sys, time
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_blow3"
os.makedirs(BASE, exist_ok=True)
conf=os.path.join(BASE,"hyprland.conf")
# ~1 MiB config: 30000 self-source lines
with open(conf,"w") as f:
    for _ in range(30000): f.write("source = hyprland.conf\n")
print("config size", os.path.getsize(conf))
t0=time.time()
try:
    r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=900)
    print("rc=",r.returncode,"elapsed=%.1fs"%(time.time()-t0),"stdout bytes",len(r.stdout))
    print(r.stdout.decode()[:200])
except subprocess.TimeoutExpired:
    print("TIMEOUT 900s")
