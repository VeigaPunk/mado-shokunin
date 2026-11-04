import argparse, contextlib, importlib.util, io, os, subprocess
S='/fast/scratch/hyaku/mado-r70/R70RevC1'
R='/home/vgpnk/Projects/shokunin/mado-shokunin'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c=load('counter',S+'/rc.py'); h=load('harness',S+'/r70.py')
os.makedirs(S+'/den',exist_ok=True)
a=argparse.Namespace(repo=R,rev='5144a6b5f43225d8021a469f4d24c19558026b9e',base_rev='b37a5aec4ea03f2223d8e09dd5d386d055c24179',scratch_root=S+'/den')
print('AXES: calibration C1; operability C2 (unchanged/out of scope)')
for label,modes in [('truncated',('genuine','crash')),('normal',('genuine','crash','garbage'))]:
    c.MODES=modes; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): ret=c.measure(a)
    print(label,'rc='+str(ret)); print(buf.getvalue(),end='')
saved=c.run_harness
def interrupted(path,prefix,fx,rev,scratch):
    if 'cand-crash' in scratch: raise subprocess.TimeoutExpired(path,900)
    return saved(path,prefix,fx,rev,scratch)
c.run_harness=interrupted
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf): ret=c.measure(a)
except subprocess.TimeoutExpired:
    print('interrupted: TimeoutExpired; no successful return; contract_emitted='+str('MADO_R70_REAL_CHILDREN:' in buf.getvalue()))
c.run_harness=saved
print('absent contract:',c.contract_line(None,0,'a'*40))
print('summary probes: actual _measure_case measurement body, scripted subprocess results')
summary=lambda p,n: 'MADO_LANDING_COUNTERS_SELFTEST: %s/%s assertions passed\n'%(p,n)
cases=[('exit-zero',0,summary(1,2),b''),('negative',1,summary(-1,2),b''),('huge',1,summary(999999999999999999999999,1),b''),('huge-total',1,summary(0,999999999999999999999999),b''),('pass-last',1,summary(0,2)+summary(2,2),b''),('fail-last',1,summary(2,2)+summary(0,2),b''),('twice-failure',1,summary(0,2)*2,b''),('stderr-only',1,'',summary(0,2).encode())]
for name,rc,out,err in cases:
    # _scripted_run only accepts mz_stdout; test stream concatenation directly too.
    merged=out+err.decode(); case={'name':name,'mz_rc':rc,'mz_stdout':merged.encode(),'child_rc':1,'child_marker':h.MISSED_MARKER}
    ret,line=h._measure_case(S+'/scripted',case,'a'*40)
    print('%s rc=%d parsed_failure=%s kill=%s measurement_rc=%d %s'%(name,rc,h.summary_shows_failure(merged),bool(rc!=0 and h.summary_shows_failure(merged)),ret,line))
print('stream merge direct:',h.summary_shows_failure(''+summary(0,2)))
