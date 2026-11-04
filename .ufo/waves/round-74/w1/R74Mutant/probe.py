#!/usr/bin/env python3
"""Bounded frozen-case mutation probe; all writes are seat-local or declared scratch."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import runpy
import secrets
import shutil
import subprocess

REPO = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
OUT = REPO / '.ufo/waves/round-74/w1/R74Mutant'
SCRATCH = Path('/fast/scratch/hyaku/mado-r74/R74Mutant')
REV = 'b73db773aaf67c9b26c8cf1a4cd567dec3af11f4'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')

def frozen(path):
    return subprocess.run(['git', '-C', str(REPO), 'show', REV + ':' + path], env=ENV,
                          check=True, capture_output=True).stdout

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(data, name):
    scope = {'__name__': name, '__file__': str(OUT / (name + '.py'))}
    exec(compile(data, scope['__file__'], 'exec'), scope)
    return scope

C1 = frozen('quality/counters/c1-r74-witness-rule.py')
C2 = frozen('quality/counters/c2-r74-shapes.py')
HARNESS = frozen('quality/counters/c1-r74-replay-witness.py')
h = load(HARNESS, 'frozen_c1_counter')
c = load(C2, 'frozen_c2_counter')
controls = {}
for kind, path, loader in [
    ('C1', '.ufo/waves/round-74/controls/c1-replay-cases-r74.json', h['load_controls']),
    ('C2', '.ufo/waves/round-74/controls/c2-cases-r74.json', c['load_controls']),
]:
    data = frozen(path)
    target = OUT / (kind + '-frozen-cases.json')
    target.write_bytes(data)
    controls[kind] = loader(str(target))
SCRATCH.mkdir(parents=True, exist_ok=True)
nonce = secrets.token_hex(8)
while nonce in (h['STALE'], 'deadbeefdeadbeef'):
    nonce = secrets.token_hex(8)

def run_case(case):
    work = SCRATCH / case['name']
    work.mkdir()
    lane = h['build_lane'](case['mode'], str(work))
    p = subprocess.run(['bash', lane], cwd=work, env=h['child_env'](nonce),
                       capture_output=True, timeout=120)
    return dict(name=case['name'], expect=case['expect'], rc=p.returncode,
                stdout=h['dec'](p.stdout), stderr=h['dec'](p.stderr))

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    outputs = list(pool.map(run_case, controls['C1']))
(OUT / 'c1-child-outputs.json').write_text(json.dumps(dict(nonce=nonce, cases=outputs), indent=2) + '\n')

def score(kind, data, name):
    mod = load(data, name)
    rows = []
    if kind == 'C1':
        for case in outputs:
            got = 'pass' if mod['credit'](case['stdout'] + case['stderr'], nonce) else 'fail'
            rows.append(dict(name=case['name'], got=got, expect=case['expect'], correct=h['score'](case['expect'], got)))
    else:
        for case in controls[kind]:
            got = mod['classify'](case['src'])
            expect = (case['expect_reader'], case['expect_guard'])
            rows.append(dict(name=case['name'], got=got, expect=expect, correct=got == expect))
    return dict(correct=sum(r['correct'] for r in rows), total=len(rows),
                wrong=[r['name'] for r in rows if not r['correct']], rows=rows)

MUTATIONS = [
    ('C1-M1', C1, 'return token is not None and token == nonce', 'return token is not None'),
    ('C1-M2', C1, 'return token is not None and token == nonce', 'return token is not None and len(token) == 16'),
    ('C1-M3', C1, 'for line in out.splitlines():\n        m = WITNESS_RE.fullmatch(line.strip())', 'for line in reversed(out.splitlines()):\n        m = WITNESS_RE.fullmatch(line.strip())'),
    ('C1-M4', C1, '    if count_fails(out) != total - passed:\n        return False\n', ''),
    ('C2-M1', C2, 'if not (crossed_call or crossed_store):', 'if not crossed_call:'),
    ('C2-M2', C2, 'for r in replaced.get(canonical, ())', 'for r in ()'),
    ('C2-M3', C2, 'if attr_dotted(node.value) == "os.environ":', 'if attr_dotted(node.value) == "os.environ" or isinstance(node.value, ast.Name):'),
    ('C2-M4', C2, '                    cancels.setdefault(target.value.id, set()).add(node.lineno)', '                    pass'),
]
results = []
try:
    for name, pristine, old, new in MUTATIONS:
        kind = name[:2]
        old, new = old.encode(), new.encode()
        assert pristine.count(old) == 1, (name, pristine.count(old))
        path = OUT / (name + '.py')
        path.write_bytes(pristine)
        before_hash = sha(path.read_bytes())
        baseline = score(kind, path.read_bytes(), name + '_baseline')
        mutated = pristine.replace(old, new, 1)
        try:
            path.write_bytes(mutated)
            mutant = score(kind, path.read_bytes(), name + '_mutated')
        finally:
            path.write_bytes(pristine)
        restored = score(kind, path.read_bytes(), name + '_restored')
        after_hash = sha(path.read_bytes())
        assert path.read_bytes() == pristine
        # Preserve each single-substitution mutant alongside its restored probe copy.
        (OUT / (name + '-mutant.py')).write_bytes(mutated)
        verdict = ('inconclusive' if baseline['correct'] != baseline['total'] or restored['correct'] != restored['total']
                   else 'killed' if mutant['correct'] < mutant['total'] else 'survived')
        result = dict(name=name, substitution_count=1, old=old.decode(), new=new.decode(),
                      before_sha256=before_hash, mutant_sha256=sha(mutated), after_sha256=after_hash,
                      baseline=baseline, mutant=mutant, restored=restored, verdict=verdict)
        results.append(result)
        print(f"{name} baseline={baseline['correct']}/{baseline['total']} mutant={mutant['correct']}/{mutant['total']} wrong={len(mutant['wrong'])} restored={restored['correct']}/{restored['total']} verdict={verdict} cases={','.join(mutant['wrong']) or '-'}", flush=True)
finally:
    shutil.rmtree(SCRATCH)
(OUT / 'mutation-results.json').write_text(json.dumps(dict(revision=REV, axes=['calibration/C1 discrimination', 'operability/C2 discrimination', 'no-harm/exact restoration'], results=results, scratch_removed=not SCRATCH.exists()), indent=2) + '\n')
