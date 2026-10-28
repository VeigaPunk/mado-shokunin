import os, resource, subprocess, sys
S="/fast/scratch/hyaku/mado-r55/R55W2SentTool"; T=S+"/tool/mado-kbdopts.py"; P=S+"/probe"
def rss(tag): print(tag, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, flush=True)
rss("start")
import importlib.util
spec=importlib.util.spec_from_file_location("r55h", S+"/harness/r55_ctl_c2.py"); hm=importlib.util.module_from_spec(spec); spec.loader.exec_module(hm)
rss("after harness import")
for depth in (5000, 20000, 50000, 100000):
    p=P+"/d.json"; open(p,"w").write('{"option":"input:repeat_rate","int":30,"x":'+"["*depth+"]"*depth+"}\n")
    r=subprocess.run([sys.executable,"-I",T,"--config",P+"/ok.conf","--getoption",p],capture_output=True)
    print("depth",depth,"rc",r.returncode,r.stdout[-40:])
p=P+"/badutf.json"; open(p,"wb").write(b'{"option":"input:repeat_rate","int":30,"x":"\xff\xfe"}\n')
r=subprocess.run([sys.executable,"-I",T,"--config",P+"/ok.conf","--getoption",p],capture_output=True); print("invalid utf8 inside JSON string: rc",r.returncode,r.stdout[-60:])
p=P+"/badutf2.json"; open(p,"wb").write(b'{"option":"input:repeat_rate","int":30}\xff\n')
r=subprocess.run([sys.executable,"-I",T,"--config",P+"/ok.conf","--getoption",p],capture_output=True); print("invalid utf8 outside JSON: rc",r.returncode,r.stdout[-60:])
