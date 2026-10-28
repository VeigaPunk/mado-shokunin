import os, subprocess, sys, time, resource
S="/fast/scratch/hyaku/mado-r55/R55W2SentTool"; T=S+"/tool/mado-kbdopts.py"; P=S+"/probe"
# worst-case parse content: 1 MiB of short lines (500k lines per file)
lines=P+"/lines1m.conf"; open(lines,"w").write("x\n"*(1048576//2))
for n in (1, 20):
    argv=[]
    for _ in range(n): argv+=["--config", lines]
    t=time.time(); r=subprocess.run([sys.executable,"-I",T,*argv],capture_output=True); el=time.time()-t
    print("short-line 1MiB x%d: rc=%d t=%.2fs stdout=%r"%(n,r.returncode,el,r.stdout[:60]))
# address-space cap: 400 x 1 MiB pairs under ulimit -v 400000 KB (300-400 MB, host-safe)
agg=P+"/agg1m.conf"
argv=[]
for _ in range(400): argv+=["--config", agg]
r=subprocess.run(["bash","-c","ulimit -v 400000; exec \"$@\"","x",sys.executable,"-I",T,*argv],capture_output=True)
print("400 pairs under ulimit -v 400000: rc=%d stdout=%r"%(r.returncode,r.stdout[:80]))
print("stderr last lines:", r.stderr.decode(errors="replace").strip().splitlines()[-2:])
# verify the 400-pair run actually reached MemoryError at the cap by testing 150 pairs (should pass)
argv=[]
for _ in range(150): argv+=["--config", agg]
r=subprocess.run(["bash","-c","ulimit -v 400000; exec \"$@\"","x",sys.executable,"-I",T,*argv],capture_output=True)
print("150 pairs under same cap: rc=%d stdout=%r"%(r.returncode,r.stdout[:60]))
