import os, subprocess, sys, time
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_evt"
os.makedirs(BASE, exist_ok=True)
W=BASE+"/wide"; os.makedirs(W, exist_ok=True)
N=20000
for i in range(N):
    os.makedirs(W+("/d%05d"%i), exist_ok=True)
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = wide/*\n")
t0=time.time()
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=300)
print("rc=%s elapsed=%.2fs stdout=%d bytes (input file: %d bytes, %d dirs)"%(r.returncode,time.time()-t0,len(r.stdout),os.path.getsize(conf),N))
print("head:",r.stdout[:160])
