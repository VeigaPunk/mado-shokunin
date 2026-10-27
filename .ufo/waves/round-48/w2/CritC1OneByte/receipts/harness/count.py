import importlib.util, json, os, shutil, sys
S="/fast/scratch/hyaku/mado-r48/CritC1OneByte"; R=S+"/repo/r48"
def load(n,p):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr=load("ctr",R+"/quality/counters/c1-r48-terminal-cache.py")
FX={f["id"]:f for f in json.loads(open(R+"/quality/counters/c1-r48-fixtures.json","rb").read())}
box=ctr.Box(S+"/work", R+"/tools/mado-terminal.py")
WD=S+"/work/count"; shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
def muts_count(data, al, ins):
    n=9
    for i in range(len(data)):
        for v in al:
            if v!=data[i]: n+=1
    n+=len(data)
    for i in range(len(data)+1):
        n+=len(ins)
    return n
for fid in sys.argv[1:]:
    case=FX[fid]; root=WD+"/"+fid+"/r"
    ctr.prepare(box, root, case, "C.UTF-8")
    data=open(ctr.cache_host(root),"rb").read()
    full=muts_count(data,[0x00,0x0a,0x0d,0x1e,0x1f,0x20,0x41,0xff],[0x0a,0x1e,0x1f,0x20,0x41])
    key=muts_count(data,[0x00,0x0a,0x1e,0x1f,0x41],[0x0a,0x1f])
    print("%-32s cache=%3d full=%4d key=%4d" % (fid, len(data), full, key))
