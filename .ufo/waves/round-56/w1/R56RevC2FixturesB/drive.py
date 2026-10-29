import json,subprocess,sys,os
FXD, EXPORT_ROOT, INTERP = sys.argv[1], sys.argv[2], sys.argv[3]
ok=0; total=0
for i in range(10,19):
    f="F%02d"%i
    fx=os.path.join(FXD,f)
    args=[a.replace("{FX}",fx) for a in json.load(open(os.path.join(fx,"args.json")))]
    p=subprocess.run(["python3","-I",INTERP]+args,cwd=EXPORT_ROOT,capture_output=True,env={"PATH":"/usr/bin:/bin","LC_ALL":"C"})
    exp_out=open(os.path.join(fx,"expected.out"),"rb").read()
    exp_rc=int(open(os.path.join(fx,"expected.rc")).read().strip())
    total+=1
    good = p.stdout==exp_out and p.returncode==exp_rc
    ok+=good
    print(f, "PASS" if good else "FAIL", "rc=%d exp=%d"%(p.returncode,exp_rc))
    if not good:
        print("--- got:\n"+p.stdout.decode()+ "--- stderr:"+p.stderr.decode()); print("--- exp:\n"+exp_out.decode())
print("pass %d/%d"%(ok,total))
