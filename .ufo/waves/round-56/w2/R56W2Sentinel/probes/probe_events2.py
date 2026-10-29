import os, subprocess, sys, time, resource
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_evt2"
os.makedirs(BASE, exist_ok=True)
W=BASE+"/wide"; os.makedirs(W, exist_ok=True)
M=200
for i in range(M): os.makedirs(W+("/d%04d"%i), exist_ok=True)
conf=os.path.join(BASE,"hyprland.conf")
L=5000
with open(conf,"w") as f:
    for _ in range(L): f.write("source = wide/*\n")
print("config bytes", os.path.getsize(conf), "dirs", M)
t0=time.time()
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=300)
print("rc=%s elapsed=%.2fs stdout=%.1f MB"%(r.returncode,time.time()-t0,len(r.stdout)/1e6))
print("events count:", r.stdout.count(b"MADO_WATCH: SKIP"))
