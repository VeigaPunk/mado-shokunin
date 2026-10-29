import os, subprocess, sys, time, resource
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_blow"
os.makedirs(BASE, exist_ok=True)
# A self-sourcing file with N source lines; each parse re-reads the file.
N=4
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = hyprland.conf\n"*N)
t0=time.time()
try:
    r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=300)
    print("rc=",r.returncode,"elapsed=%.2fs"%(time.time()-t0))
    print("STDOUT bytes:",len(r.stdout))
    print(r.stdout.decode()[:400])
    print("...TAIL:", r.stdout.decode()[-300:])
except subprocess.TimeoutExpired:
    print("TIMEOUT 300s")
