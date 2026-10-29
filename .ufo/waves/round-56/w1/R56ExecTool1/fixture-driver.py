import json,subprocess,sys,os,shutil
R,T,S=sys.argv[1:4]
fx=R+'/fixtures/c2'
exp=S+'/export'; shutil.rmtree(exp,ignore_errors=True); os.makedirs(exp)
# export with symlinks preserved
subprocess.check_call(['cp','-a',fx,exp+'/c2'])
ok=0
for f in sorted(os.listdir(exp+'/c2')):
    d=exp+'/c2/'+f
    args=[a.replace('{FX}',d) for a in json.load(open(d+'/args.json'))]
    p=subprocess.run(['python3','-I',T]+args,cwd=exp,capture_output=True)
    eo=open(d+'/expected.out','rb').read().replace(b'{FX}',d.encode())
    erc=int(open(d+'/expected.rc').read().strip())
    good=p.stdout==eo and p.returncode==erc
    ok+=good
    print(f,'PASS' if good else 'FAIL','rc',p.returncode,'exp',erc)
    if not good:
        print(p.stdout.decode(),p.stderr.decode()); print(eo.decode())
print(ok,'/ 18')
