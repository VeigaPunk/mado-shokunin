import os, subprocess, sys, time, resource
for N in (2,3):
    BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/amp%d"%N
    os.makedirs(BASE, exist_ok=True)
    conf=os.path.join(BASE,"hyprland.conf")
    open(conf,"w").write("source = hyprland.conf\n"*N)
    t0=time.time()
    try:
        r=subprocess.run([sys.executable,"-I","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py","--config",conf,"--display-root",BASE],capture_output=True,timeout=300)
        print("N=%d rc=%s elapsed=%.2fs stdout=%d bytes"%(N,r.returncode,time.time()-t0,len(r.stdout)))
        print("   head:", r.stdout[:120])
        print("   tail:", r.stdout[-80:])
    except subprocess.TimeoutExpired:
        print("N=%d TIMEOUT"%N)
