import json, subprocess, sys, os, glob
lane="/home/vgpnk/Projects/shokunin/mado-shokunin"
tool=lane+"/.ufo/waves/round-55/w1/R55ExecTool4/mado-kbdopts.py"
p=0
for d in sorted(glob.glob(lane+"/.ufo/waves/round-55/fixtures/c2/F*")):
    args=json.load(open(d+"/args.json"))
    r=subprocess.run(["python3","-I",tool]+args,cwd=lane,capture_output=True)
    eo=open(d+"/expected.out","rb").read(); erc=int(open(d+"/expected.rc").read())
    ok = r.stdout==eo and r.returncode==erc
    p+=ok
    print(os.path.basename(d),"PASS" if ok else "FAIL", "rc=%d"%r.returncode, "stderr=%r"%r.stderr if r.stderr else "")
    if not ok:
        print("  expected rc",erc,eo); print("  got",r.stdout)
print("%d/18"%p)
