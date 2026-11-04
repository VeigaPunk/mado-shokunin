import concurrent.futures as cf
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path('/fast/scratch/hyaku/mado-r76/R76Mutant')
OUT = Path('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-76/w1/R76Mutant')
REPO = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = 'cb713254ee9926e036e594312fdc61b57825526b'
def extract(path):
    return subprocess.run(['git', '-C', REPO, 'show', REV + ':' + path], capture_output=True, check=True).stdout

def digest(data):
    return hashlib.sha256(data).hexdigest()

c1 = runpy.run_path(str(ROOT / 'c1-r76-outcome-field.py'))
cases1_raw = extract('.ufo/waves/round-76/controls/c1-outcome-cases-r76.json')
cases2_raw = extract('.ufo/waves/round-76/controls/c2-cases-r76.json')
assert digest(cases1_raw) == c1['CONTROLS_SHA']
cases1 = json.loads(cases1_raw)['cases']
cases2 = json.loads(cases2_raw)['cases']
assert digest(cases2_raw) == runpy.run_path(str(ROOT / 'c2-r76-shapes.py'))['FROZEN_CONTROLS_SHA']
work = Path(tempfile.mkdtemp(prefix='probe-', dir=ROOT))
home = work / 'home'
home.mkdir()
env = c1['git_env'](str(home))
lane_files = {p: extract(p) for p in (c1['USEDBY'], c1['LEDGER'], c1['CITECHECK'], c1['R72'])}
fixtures = {c['name']: c1['make_fixture'](str(work), c, lane_files, env) for c in cases1}

def score1(path, label):
    rows = []
    for case in cases1:
        r = c1['harness_run'](str(path), fixtures[case['name']], str(work / label / case['name']), env)
        text = c1['dec'](r.stdout)
        got = c1['parse_row'](text)
        expected = (case['expect_mz'], case['expect_verdict'])
        rows.append({'name': case['name'], 'expected': expected, 'got': got,
                     'rc': r.returncode, 'correct': got == expected,
                     'stdout': text, 'stderr': c1['dec'](r.stderr)})
    return {'score': sum(r['correct'] for r in rows), 'total': len(rows),
            'separators': [r['name'] for r in rows if not r['correct']], 'rows': rows}

def score2(path, label):
    mod = runpy.run_path(str(path))
    rows = []
    for case in cases2:
        got = mod['classify'](case['src'])
        expected = (case['expect_reader'], case['expect_guard'])
        rows.append({'name': case['name'], 'expected': expected, 'got': got, 'correct': got == expected})
    return {'score': sum(r['correct'] for r in rows), 'total': len(rows),
            'separators': [r['name'] for r in rows if not r['correct']], 'rows': rows}

specs = [('constant', 'c1-r76-landing-controls.py', score1),
         ('grammar16', 'c1-r76-landing-controls.py', score1),
         ('forward', 'c1-r76-landing-controls.py', score1),
         ('d3-anyarg', 'c2-r76-shapes.py', score2),
         ('d4-twobind', 'c2-r76-shapes.py', score2)]
results = {}
# Each probe runs the identical detector before mutation, during mutation and after exact restore.
# Mutant bytes were prepared surgically; keep a private preserved payload while restoring each target.
def probe(spec):
    name, source, detector = spec
    path = ROOT / (name + '.py')
    mutant = path.read_bytes()
    pristine = (ROOT / source).read_bytes()
    data = {'before_sha256': digest(pristine), 'mutated_sha256': digest(mutant)}
    path.write_bytes(pristine)
    try:
        data['baseline'] = detector(path, name + '-baseline')
        path.write_bytes(mutant)
        data['mutated'] = detector(path, name + '-mutated')
    finally:
        path.write_bytes(pristine)
        data['after_sha256'] = digest(path.read_bytes())
    data['restored'] = detector(path, name + '-restored')
    baseline_ok = data['baseline']['score'] == data['baseline']['total']
    restored_ok = data['restored']['score'] == data['restored']['total']
    data['verdict'] = ('inconclusive' if not (baseline_ok and restored_ok) else
                       'killed' if data['mutated']['score'] < data['mutated']['total'] else 'survived')
    return name, data

with cf.ThreadPoolExecutor(max_workers=5) as pool:
    for name, data in pool.map(probe, specs):
        results[name] = data
        print(name, data['verdict'], data['mutated']['score'], '/', data['mutated']['total'], data['mutated']['separators'], flush=True)
(OUT / 'results.json').write_text(json.dumps({'revision': REV, 'axes': ['frozen-set discrimination', 'exact restoration', 'lane isolation'], 'results': results}, indent=2) + '\n')
