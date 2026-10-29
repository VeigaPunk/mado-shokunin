import os, subprocess, sys
STAGE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/bwstage"
os.makedirs(STAGE+"/tree", exist_ok=True)
open(STAGE+"/tree/hyprland.conf","w").write("x = 1\n")
PROG="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/bwprobe.py"
open(PROG,"w").write('''
import os,sys
print("uid",os.getuid())
for p in ["/etc/shadow","/etc/passwd","/home/vgpnk/.config/hypr","/home/vgpnk/.ssh","/proc/self/environ","/proc/1/environ","/fast/scratch/hyaku/mado-r56","/home/vgpnk/Projects/shokunin/mado-shokunin","/usr","/dev","/tmp","/var","/etc","/root"]:
    try:
        r=os.listdir(p) if os.path.isdir(p) else open(p,"rb").read(20)
        print("READABLE",p,str(r)[:60])
    except Exception as e:
        print("blocked ",p,type(e).__name__,str(e)[:60])
print("cwd",os.getcwd())
print("env",{k:v for k,v in os.environ.items() if k in ("HOME","TMPDIR","PATH")})
''')
cmd=["/usr/bin/bwrap","--unshare-all","--die-with-parent","--ro-bind","/usr","/usr","--symlink","usr/lib","/lib",
     "--symlink","usr/lib64","/lib64","--symlink","usr/bin","/bin","--dev","/dev",
     "--ro-bind",STAGE,STAGE,"--ro-bind",PROG,PROG,"--tmpfs","/w","--chdir","/w",
     "/usr/bin/python3","-I",PROG]
env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":STAGE,"TMPDIR":STAGE,"LC_ALL":"C.UTF-8","LANG":"C.UTF-8"}
r=subprocess.run(cmd,env=env,capture_output=True,timeout=60)
print("rc",r.returncode)
print(r.stdout.decode())
print("ERR",r.stderr.decode()[:500])
