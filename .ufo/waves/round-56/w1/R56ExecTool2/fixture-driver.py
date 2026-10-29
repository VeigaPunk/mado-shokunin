import json,subprocess,os,sys
TOOL='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool2/mado-watchplan.py'
ex='EXPORT_DIR'
base=ex+'/.ufo/waves/round-56/fixtures/c2'
ok=0
for f in sorted(os.listdir(base)):
    d=base+'/'+f
    args=[a.replace('{FX}',d) for a in json.load(open(d+'/args.json'))]
    p=subprocess.run(['python3','-I',TOOL]+args,cwd=ex,capture_output=True)
    exp=open(d+'/expected.out','rb').read(); rc=int(open(d+'/expected.rc').read().strip())
    good = p.stdout==exp and p.returncode==rc
    ok+=good
    print(f,'PASS' if good else 'FAIL', p.returncode, rc)
    if not good:
        print(p.stdout.decode()); print(p.stderr.decode())
print(ok,'/18')
