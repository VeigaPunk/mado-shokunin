import json, subprocess, sys, os
FXR="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fixtures/c2"
TOOL="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool4/mado-watchplan.py"
ok=0
for n in sorted(os.listdir(FXR)):
    d=os.path.join(FXR,n)
    args=[a.replace("{FX}",d) for a in json.load(open(d+"/args.json"))]
    p=subprocess.run(["python3","-I",TOOL]+args,capture_output=True,cwd="/fast/scratch/hyaku/mado-r56/R56ExecTool4")
    eo=open(d+"/expected.out","rb").read(); erc=int(open(d+"/expected.rc").read().strip())
    good = p.stdout==eo and p.returncode==erc
    ok+=good
    print(n,"PASS" if good else "FAIL",p.returncode,erc, p.stderr.decode()[:200])
    if not good: print(p.stdout.decode()); print("--exp"); print(eo.decode())
print(ok,"/18")
