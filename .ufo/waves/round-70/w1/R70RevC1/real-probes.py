import hashlib, os, subprocess, tempfile
S='/fast/scratch/hyaku/mado-r70/R70RevC1'
R='/home/vgpnk/Projects/shokunin/mado-shokunin'
REV='5144a6b5f43225d8021a469f4d24c19558026b9e'
D=tempfile.mkdtemp(prefix='fixture.',dir=S)
def git(*args,identity=False):
    cmd=['git','-C',D]
    if identity: cmd += ['-c','user.name=r70rev','-c','user.email=r70rev@example.invalid','-c','commit.gpgsign=false']
    p=subprocess.run(cmd+list(args),capture_output=True,check=True); return p.stdout.decode().strip()
git('init','-q'); assert git('rev-parse','--show-toplevel')==D
for rel in ['quality/counters/c3-r56-used-by.py','quality/check-tool-ledger.py','tools/mado-receipt-citecheck.py']:
    p=subprocess.run(['git','-C',R,'show',REV+':'+rel],capture_output=True,check=True)
    os.makedirs(os.path.dirname(D+'/'+rel),exist_ok=True); open(D+'/'+rel,'wb').write(p.stdout)
template=open(R+'/.ufo/waves/round-70/proto/fixture-lane.tmpl').read()
cases=[(m,template.replace('__MODE__',m)) for m in ('genuine','crash','garbage')]
summ=lambda x: "printf 'MADO_LANDING_COUNTERS_SELFTEST: %s assertions passed\\n'"%x
for name,body in [('exit-zero',summ('1/2')+'; exit 0'),('negative',summ('-1/2')+'; exit 1'),('huge',summ('999999999999999999999999/1')+'; exit 1'),('huge-total',summ('0/999999999999999999999999')+'; exit 1'),('pass-last',summ('0/2')+'; '+summ('2/2')+'; exit 1'),('fail-last',summ('2/2')+'; '+summ('0/2')+'; exit 1'),('stderr-only',summ('0/2')+' >&2; exit 1')]:
    cases.append((name,template.replace('__MODE__','synthetic').replace("    crash) exit 2 ;;",'    synthetic) '+body+' ;;\n    crash) exit 2 ;;')))
for name,lane in cases:
    open(D+'/quality/landing-counters.sh','w').write(lane)
    git('add','-A'); git('commit','-qm',name,identity=True); rev=git('rev-parse','HEAD')
    for version in ('r69','r70'):
        scratch=S+'/real-'+name+'-'+version; os.makedirs(scratch,exist_ok=True)
        cmd=['python3','-I',S+'/'+version+'.py','--repo',D,'--rev',rev,'--scratch-root',scratch]
        p=subprocess.run(cmd,capture_output=True)
        out=(p.stdout+p.stderr).decode(errors='replace'); open(S+'/'+name+'-'+version+'.log','w').write(out)
        print('COMMAND:', ' '.join(cmd),'rc='+str(p.returncode))
        for line in out.splitlines():
            if 'MUTANT M-Z ' in line or 'LANDING_CONTROLS:' in line: print(line)
