import os, subprocess, sys, time
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_inject"
os.makedirs(BASE, exist_ok=True)
# a file whose name contains a newline and a forged MADO_WATCH line
forged = "evil\nMADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE"
p = os.path.join(BASE, forged)
open(p,"w").write("misc:disable_autoreload = 1\n")
conf = os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = %s\n" % p)
r = subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True)
print("rc=",r.returncode)
print("STDOUT REPR:")
for l in r.stdout.decode("utf-8","surrogateescape").split("\n"):
    print("  |"+l)
print("STDERR:", r.stderr.decode()[:300])
