import os, subprocess, sys
WORK="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/bw2"
STAGE=WORK+"/stage-1/F01"
os.makedirs(STAGE+"/tree", exist_ok=True)
os.makedirs(WORK+"/c2-export-XXXX/fixtures/c2/F01", exist_ok=True)
open(WORK+"/c2-export-XXXX/fixtures/c2/F01/expected.out","w").write("SECRET ANSWER KEY\n")
PROG=WORK+"/probe.py"
open(PROG,"w").write('''
import os
for p in ["/fast/scratch/hyaku/mado-r56/R56W2Sentinel/bw2","/fast/scratch/hyaku/mado-r56/R56W2Sentinel","/fast/scratch/hyaku/mado-r56","/fast/scratch/hyaku","/fast/scratch","/fast"]:
    try: print("LIST",p,os.listdir(p)[:12])
    except Exception as e: print("block",p,type(e).__name__)
try:
    print("KEY:",open("/fast/scratch/hyaku/mado-r56/R56W2Sentinel/bw2/c2-export-XXXX/fixtures/c2/F01/expected.out").read())
except Exception as e: print("key blocked",e)
''')
cmd=["/usr/bin/bwrap","--unshare-all","--die-with-parent","--ro-bind","/usr","/usr","--symlink","usr/lib","/lib",
     "--symlink","usr/lib64","/lib64","--symlink","usr/bin","/bin","--dev","/dev",
     "--ro-bind",STAGE,STAGE,"--ro-bind",PROG,PROG,"--tmpfs","/w","--chdir","/w",
     "/usr/bin/python3","-I",PROG]
env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":WORK,"TMPDIR":WORK,"LC_ALL":"C.UTF-8","LANG":"C.UTF-8"}
r=subprocess.run(cmd,env=env,capture_output=True,timeout=60)
print("rc",r.returncode); print(r.stdout.decode()); print("ERR",r.stderr.decode()[:300])
