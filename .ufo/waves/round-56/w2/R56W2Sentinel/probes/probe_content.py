import os, subprocess, sys
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_content"
os.makedirs(BASE, exist_ok=True)
SECRET="SUPERSECRETVALUE-abc123"
sec=os.path.join(BASE,"secret.conf")
open(sec,"w").write("# %s\nmisc:disable_autoreload = 1\n" % SECRET)
# also a file whose 'source' line embeds a secret
sec2=os.path.join(BASE,"secret2.conf")
open(sec2,"w").write("source = /%s\n" % SECRET)
conf=os.path.join(BASE,"hyprland.conf")
open(conf,"w").write("source = secret.conf\nsource = secret2.conf\n")
r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True)
out=r.stdout.decode("utf-8","surrogateescape")
print("rc=",r.returncode)
print(out)
print("SECRET in stdout?", SECRET in out)
print("SECRET in stderr?", SECRET in r.stderr.decode("utf-8","surrogateescape"))
