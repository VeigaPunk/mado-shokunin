#!/usr/bin/env python3
import contextlib
import hashlib
import io
import json
import pathlib
import runpy
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
ROOT = pathlib.Path('/fast/scratch/hyaku/mado-r70/R70RevC2')
REV = '5144a6b5f43225d8021a469f4d24c19558026b9e'
BASE = 'b37a5aec4ea03f2223d8e09dd5d386d055c24179'
CONTROLS = LANE / '.ufo/waves/round-70/controls/c2-controls-r70.json'
ROOT.mkdir(parents=True, exist_ok=True)
results = {}

def execute(argv):
    p = subprocess.run([str(x) for x in argv], capture_output=True, text=True)
    return dict(command=[str(x) for x in argv], rc=p.returncode,
                stdout=p.stdout, stderr=p.stderr)

def measure(repo, rev, controls=CONTROLS):
    return execute(['python3', HERE/'instrument-pinned.py', '--repo', repo,
                    '--rev', rev, '--base-rev', BASE, '--controls', controls,
                    '--scratch-root', ROOT])

try:
    new = runpy.run_path(str(HERE/'instrument-pinned.py'))
    old = runpy.run_path(str(HERE/'held-instrument.py'))
    results['instrument_sha256'] = hashlib.sha256((HERE/'instrument-pinned.py').read_bytes()).hexdigest()
    results['attacks'] = []
    for case in json.loads((HERE/'attack-sources.json').read_text()):
        results['attacks'].append(dict(**case, observed_new=new['classify'](case['src']),
                                      observed_held=old['classify'](case['src'])))
    results['pinned_measurement'] = measure(LANE, REV)
    raw = CONTROLS.read_bytes()
    doc = json.loads(raw)
    truncated = ROOT/'truncated.json'
    truncated.write_bytes(raw[:400])
    renamed = ROOT/'renamed.json'
    renamed.write_bytes(raw.replace(b'guarded-inline',b'guarded-inline-x',1))
    sixteen = ROOT/'sixteen.json'
    sixteen.write_text(json.dumps(dict(doc, cases=doc['cases'][:-1])))
    results['controls_attacks'] = {p.name:measure(LANE,REV,p) for p in (truncated,renamed,sixteen)}
    results['verdict_attacks'] = {}
    for name, values in [('base17',(20,13,13,0,17,17)),('controls16',(20,13,13,0,16,13)),('population19',(19,13,13,0,17,13))]:
        results['verdict_attacks'][name] = dict(values=values,accepted=new['verdict_met'](*values),line=new['contract_line'](*values,REV))
    fixture = pathlib.Path(tempfile.mkdtemp(prefix='fixture.',dir=ROOT))
    p=execute(['git','clone','--quiet','--no-hardlinks','--no-checkout',LANE,fixture])
    assert p['rc']==0,p
    top=execute(['git','-C',fixture,'rev-parse','--show-toplevel'])
    assert top['rc']==0 and pathlib.Path(top['stdout'].strip())==fixture,top
    def git(*args):
        p=execute(['git','-C',fixture,*args]); assert p['rc']==0,p; return p
    git('checkout','--quiet',REV)
    git('rm','--quiet','quality/check-state-cite.py')
    git('-c','user.name=R70RevC2','-c','user.email=r70revc2@scratch.invalid','commit','--quiet','-m','scratch population 19')
    sha19=git('rev-parse','HEAD')['stdout'].strip()
    results['population19_cli']=measure(fixture,sha19)
    held=fixture/'.ufo/waves/round-69/controls/c2-controls-r69.json'
    held.write_bytes(held.read_bytes()+b'\n')
    git('add','--','.ufo/waves/round-69/controls/c2-controls-r69.json')
    git('-c','user.name=R70RevC2','-c','user.email=r70revc2@scratch.invalid','commit','--quiet','-m','scratch held digest tamper')
    broken=git('rev-parse','HEAD')['stdout'].strip()
    results['held_digest_break']=measure(fixture,broken)
finally:
    shutil.rmtree(ROOT,ignore_errors=True)
    results['scratch_removed']=not ROOT.exists()
    (HERE/'evidence.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'pinned_rc':results['pinned_measurement']['rc'],
                  'controls_rc':{k:v['rc'] for k,v in results['controls_attacks'].items()},
                  'population19_rc':results['population19_cli']['rc'],
                  'held_break_rc':results['held_digest_break']['rc'],
                  'scratch_removed':results['scratch_removed']}))
