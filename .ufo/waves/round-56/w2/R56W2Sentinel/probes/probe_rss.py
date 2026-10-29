import os, subprocess, sys, time, resource
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_rss"
os.makedirs(BASE, exist_ok=True)
W=BASE+"/wide"; os.makedirs(W, exist_ok=True)
for i in range(500): os.makedirs(W+("/d%04d"%i), exist_ok=True)
conf=os.path.join(BASE,"hyprland.conf")
L=5000
with open(conf,"w") as f:
    for _ in range(L): f.write("source = wide/*\n")
print("config bytes", os.path.getsize(conf))
t0=time.time()
p = subprocess.Popen([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],stdout=subprocess.PIPE)
out,_ = p.communicate()
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print("rc=%s elapsed=%.2fs stdout=%.1f MB peak_child_RSS=%.1f MB events=%d"%(
    p.returncode, time.time()-t0, len(out)/1e6, ru.ru_maxrss/1024, out.count(b"MADO_WATCH: SKIP")))
