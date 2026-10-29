import subprocess,sys,time
open("/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p4/root/hg.conf","w").write("source = /usr/*/*/*/*/*/*\n")
t0=time.time()
try:
    r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p4/root/hg.conf"],capture_output=True,timeout=60)
    print("rc=%s elapsed=%.2fs stdout=%d bytes events=%d"%(r.returncode,time.time()-t0,len(r.stdout),r.stdout.count(b"MADO_WATCH")))
    print(r.stdout.split(b"\n")[-2][:200])
except subprocess.TimeoutExpired:
    print("TIMEOUT 60s on /usr/*/*/*/*/*/* (no cap on glob work)")
