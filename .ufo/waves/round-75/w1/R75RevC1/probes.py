import argparse, contextlib, io, os, pathlib, runpy, subprocess
from concurrent.futures import ThreadPoolExecutor
S = pathlib.Path('/fast/scratch/hyaku/mado-r75/R75RevC1')
h = runpy.run_path(str(S / 'c1-r75-landing-controls.py'))
b = runpy.run_path(str(S / 'c1-r72-landing-controls.py'))
c = runpy.run_path(str(S / 'c1-r75-harness-witness.py'))
nonce = 'deadbeefdeadbeef'
failed = 'SELFTEST FAIL 1: failure\nMADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n'
green = 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n'
for label, echo in [('absent',''), ('wrong','ffffffffffffffff'), ('right',nonce), ('uppercase',nonce.upper())]:
    text = failed + ('MADO_LANDING_WITNESS: '+echo+'\n' if echo else '')
    print('CREDIT', label, h['credit_with_witness'](b['credit'],text,nonce))
os.environ['MADO_LANDING_NONCE']='ffffffffffffffff'
h['install_rule'](b,nonce)
g=b['measure'].__globals__
print('ENV ambient='+os.environ['MADO_LANDING_NONCE']+' child='+g['child_env'](str(S))['MADO_LANDING_NONCE']+' git_has_nonce='+str('MADO_LANDING_NONCE' in h['git_env'](str(S))))
for label,out in [('absent',green),('right',green+'MADO_LANDING_WITNESS: '+nonce+'\n')]:
    print('CONTRACT',label,g['contract_line'](out,'pass','pass',2,'a'*40),'exit='+str(g['outcome_exit'](out,2)))
# Compare modes without changing the frozen template: original and clause-deleted variants.
for mutated in [False,True]:
    results=[]
    for mode in ['right','liar-success']:
        script=c['LANE_TEMPLATE'].replace('@MODE@',mode)
        if mutated: script=script.replace(c['Z_CLAUSE'].decode(),'')
        p=S/(mode+('-mut' if mutated else '')+'.sh'); p.write_text(script)
        r=subprocess.run(['bash',str(p)],env={'PATH':os.environ['PATH'],'MADO_LANDING_NONCE':nonce},capture_output=True,text=True,cwd=S)
        results.append((r.returncode,r.stdout,r.stderr))
        print('MODE',mode,'mutated='+str(mutated),'rc='+str(r.returncode),'stdout='+repr(r.stdout),'stderr='+repr(r.stderr))
    print('MODES_IDENTICAL mutated='+str(mutated),results[0]==results[1])
# Force a valid digits-only challenge in an isolated process, not in the lane.
code="import argparse,runpy; m=runpy.run_path(%r); m['secrets'].token_hex=lambda n:'0123456789012345'; raise SystemExit(m['measure'](argparse.Namespace(repo=%r,rev='HEAD',scratch_root=%r)))" % (str(S/'c1-r75-landing-controls.py'),str(S/'counter/r75-c1/fixtures/uppercase-echo'),str(S/'numeric-challenge'))
r=subprocess.run(['python3','-I','-c',code],capture_output=True,text=True,cwd=S,timeout=900)
print('NUMERIC_COMMAND',repr(['python3','-I','-c',code])); print(r.stdout); print(r.stderr); print('NUMERIC_RC',r.returncode)
print('NUMERIC_NONCE_PROBABILITY',(10/16)**16)
# The R72 pin must reject even one appended byte. Intercept read-only git show response.
real_run=subprocess.run
def fake_run(argv,**kwargs):
    r=real_run(argv,**kwargs)
    if argv[3:4]==['show'] and r.returncode==0:
        r.stdout+=b'\n'
    return r
subprocess.run=fake_run
try:
    try:
        h['load_generation'](argparse.Namespace(repo=str(S/'counter/r75-c1/fixtures/right'),rev='HEAD'),str(S/'pin-probe'))
        print('PIN unexpectedly accepted changed generation')
    except h['SetupError'] as exc:
        print('PIN refused:',exc)
finally:
    subprocess.run=real_run
