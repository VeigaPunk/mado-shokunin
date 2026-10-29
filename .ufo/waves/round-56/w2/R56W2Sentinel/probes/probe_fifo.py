import os, subprocess, sys, time
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_fifo"
os.makedirs(BASE, exist_ok=True)
fifo = os.path.join(BASE,"a.fifo")
if not os.path.exists(fifo): os.mkfifo(fifo)
# symlink to /dev/zero (device) and to a FIFO
for n,t in (("zero.link","/dev/zero"),("null.link","/dev/null")):
    lp=os.path.join(BASE,n)
    if not os.path.lexists(lp): os.symlink(t,lp)
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = *\n")
t0=time.time()
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=60)
print("rc=",r.returncode,"elapsed=%.2fs"%(time.time()-t0))
print(r.stdout.decode("utf-8","surrogateescape"))
print("STDERR:",r.stderr.decode()[:300])
