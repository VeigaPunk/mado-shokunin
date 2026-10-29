import os, subprocess, sys
BASE=b"/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_nu"
os.makedirs(BASE, exist_ok=True)
name = b"conf-\xff\xfe.conf"
p = BASE + b"/" + name
open(p,"wb").write(b"misc:disable_autoreload = 1\n")
conf = BASE + b"/hyprland.conf"
open(conf,"wb").write(b"source = *\n")
r = subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf.decode()],capture_output=True)
print("rc=",r.returncode)
print("RAW STDOUT bytes:")
print(r.stdout)
print("decoded:", r.stdout.decode("utf-8","surrogateescape"))
print("STDERR:", r.stderr.decode()[:400])
