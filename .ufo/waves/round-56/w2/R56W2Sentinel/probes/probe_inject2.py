import os, subprocess, sys
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_inj2"
os.makedirs(BASE, exist_ok=True)
forged = "evil\nMADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE"
p = os.path.join(BASE, forged)
open(p,"w").write("misc:disable_autoreload = 1\n")
conf = os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = *\n")
r = subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True)
print("rc=",r.returncode)
print("RAW STDOUT:")
print(r.stdout.decode("utf-8","surrogateescape"))
print("--- line count:", len(r.stdout.decode('utf-8','surrogateescape').split("\n")))
