import os, subprocess, sys
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_ctrl"
os.makedirs(BASE, exist_ok=True)
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = /tmp\x1b[31mEVIL\n")
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf],capture_output=True)
print("rc=",r.returncode); print(repr(r.stdout)); print("ERR",r.stderr.decode()[:200])
