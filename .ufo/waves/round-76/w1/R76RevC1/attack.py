import argparse, concurrent.futures, contextlib, io, json, os, pathlib, subprocess
REPO='/home/vgpnk/Projects/shokunin/mado-shokunin'
REV='cb713254ee9926e036e594312fdc61b57825526b'
SCRATCH=pathlib.Path('/fast/scratch/hyaku/mado-r76/R76RevC1')
SEAT=pathlib.Path(__file__).parent
CONTROLS=REPO+'/.ufo/waves/round-76/controls/c1-outcome-cases-r76.json'
def frozen(path):
    return subprocess.check_output(['git','-C',REPO,'show',REV+':'+path])
def load():
    ns={'__name__':'review'}
    exec(compile(frozen('quality/counters/c1-r76-outcome-field.py'),'frozen-counter','exec'),ns)
    return ns

def absent_base():
    old='74d3b7bacab1c8eb2300b82d39eb0fcadf62db12'
    p=subprocess.run(['python3','-I',str(SEAT/'frozen-counter.py'),'--repo',REPO,'--rev',REV,'--base-rev',old,'--controls',CONTROLS,'--scratch-root',str(SCRATCH/'absent-base')],capture_output=True,text=True)
    (SEAT/'absent-base.txt').write_text('COMMAND: frozen-counter.py --repo '+REPO+' --rev '+REV+' --base-rev '+old+' --controls '+CONTROLS+' --scratch-root '+str(SCRATCH/'absent-base')+'\n'+p.stdout+'STDERR: '+p.stderr+'\nRC: '+str(p.returncode)+'\n')
    return 'absent-base',p.returncode,p.stdout.splitlines()[-1]

def local_attacks():
    ns=load(); cases=json.loads(pathlib.Path(CONTROLS).read_text())['cases']
    work=SCRATCH/'attacks'; work.mkdir(parents=True,exist_ok=True)
    home=work/'home'; home.mkdir(exist_ok=True)
    env=ns['git_env'](str(home))
    lane_files={p:frozen(p) for p in (ns['USEDBY'],ns['LEDGER'],ns['CITECHECK'],ns['R72'])}
    harness=frozen(ns['CAND'])
    candidate=work/'candidate.py'; candidate.write_bytes(harness)
    both=work/'both.py'
    both.write_bytes(harness.replace(b'"pass" if mz_killed else "fail"',b'"fail" if mz_killed else "pass"') if False else harness.replace(b'g["credit"] = lambda out: credit_with_witness(r72_credit, out, nonce)',b'g["credit"] = lambda out: False').replace(b'return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2',b'return True'))
    outputs=[]; mutant_score=base_score=0
    for case in cases:
        fixture=ns['make_fixture'](str(work),case,lane_files,env)
        r=ns['harness_run'](str(both),fixture,str(work/'both'/case['name']),env)
        out=ns['dec'](r.stdout); got=ns['parse_row'](out)
        mutant_score+=int(got==(case['expect_mz'],case['expect_verdict']))
        base_score+=int(got[0]==case['expect_mz'])
        if case['name'] in ('right','always-red','green-mutant'):
            r=ns['harness_run'](str(candidate),fixture,str(work/'labels'/case['name']),env)
            evidence=ns['dec'](r.stdout)
            outputs.append('LABEL '+case['name']+'\n'+evidence+'\nRC '+str(r.returncode))
    outputs.append('BOTH_FIELDS score=%d/16 base_score=%d/16 killed=%s base_killed=%s'%(mutant_score,base_score,mutant_score<16,base_score<16))
    row=lambda mz,v:'MADO_R76_LANDING_CONTROLS: selftest=2/2 mz=%s mr=pass killed=2/2 baseline=0/2 witness=ok verdict=%s rev=%s'%(mz,v,'a'*40)
    outputs.append('LATER_ROW '+repr(ns['parse_row'](row('fail','TARGET_MISSED')+'\n'+row('pass','TARGET_MET'))))
    # The declared unobservable outcome-echo mutant is directly compared on a failing witness.
    h={'__name__':'harness_review'}; exec(compile(harness,'frozen-harness','exec'),h)
    green=lambda _:True
    outputs.append('BROKEN_ECHO_RULE absent witness killed=1 canonical=%s broken_without_echo=%s'%(h['outcome_green'](green,'','deadbeefdeadbeef',1),bool(green('')) and 1==2))
    (SEAT/'attacks.txt').write_text('\n'.join(outputs)+'\n')
    return 'attacks',mutant_score,base_score

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(absent_base),pool.submit(local_attacks)]
    for future in futures:
        print(future.result(),flush=True)
