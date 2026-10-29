import os, subprocess, sys
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_ansi"
os.makedirs(BASE, exist_ok=True)
name = "a\x1b[31mRED\x1b[0m\x07b.conf"     # ANSI + BEL in the filename
open(os.path.join(BASE,name),"w").write("x = 1\n")
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = *.conf\n")
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True)
print("rc=",r.returncode)
print("RAW:"); print(repr(r.stdout))
