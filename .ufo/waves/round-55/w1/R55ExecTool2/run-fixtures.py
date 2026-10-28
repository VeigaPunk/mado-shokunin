import json,subprocess,sys,os
L='/home/vgpnk/Projects/shokunin/mado-shokunin'
T=sys.argv[1]
F=L+'/.ufo/waves/round-55/fixtures/c2'
ok=0
for n in sorted(os.listdir(F)):
    d=F+'/'+n
    args=json.load(open(d+'/args.json'))
    p=subprocess.run(['python3','-I',T]+args,cwd=L,capture_output=True)
    eo=open(d+'/expected.out','rb').read(); erc=int(open(d+'/expected.rc').read().strip())
    good=p.stdout==eo and p.returncode==erc
    ok+=good
    print(n,'PASS' if good else 'FAIL',p.returncode,erc, p.stderr[:200])
    if not good:
        print(' ARGS',args);print(' GOT',p.stdout.decode());print(' EXP',eo.decode())
print(ok,'/18')
