import os, subprocess, sys
BASE=b"/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_nu3"
os.makedirs(BASE, exist_ok=True)
name = b"sec-\xff\xfe-retweird.conf"
open(BASE + b"/" + name, "wb").write(b"x = 1\n")
open(BASE + b"/hyprland.conf","wb").write(b"source = sec-*.conf\n")
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",(BASE+b"/hyprland.conf").decode()],capture_output=True)
print("rc=",r.returncode)
print("RAW bytes:", r.stdout)
print("STDERR:", r.stderr.decode("utf-8","surrogateescape")[:300])
