#!/usr/bin/env python3
"""Read-only independent derivation; writes extracted modules only under seat scratch."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
repo = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
scratch = Path('/fast/scratch/hyaku/mado-r72/R72ExecC2')
base_rev = '976684a27e99c2508037a60eec415f550f53d70e'
rev = '9bcb4fd5b598844f168230dc05e441721d95b272'
modules = []
for name, revision, path in (
    ('held', base_rev, 'quality/counters/c1-r71-landing-controls.py'),
    ('candidate', rev, 'quality/counters/c1-r72-landing-controls.py'),
):
    data = subprocess.check_output(['git', '-C', str(repo), 'show', revision + ':' + path])
    target = scratch / (name + '-independent.py')
    target.write_bytes(data)
    spec = importlib.util.spec_from_file_location(name, target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    modules.append(module)
    print(f'INDEPENDENT_SOURCE role={name} rev={revision} path={path} sha256={hashlib.sha256(data).hexdigest()}')
held, candidate = modules
cases = json.loads((repo / '.ufo/waves/round-72/controls/c2-controls-r72.json').read_text())['cases']
measurement = (repo / '.ufo/waves/round-72/measurement-c2-r72.txt').read_text().splitlines()
baseline = (repo / '.ufo/waves/round-72/control-baseline-c2-r72.txt').read_text().splitlines()
correct = 0
differences = []
for case in cases:
    got = held.outcome_verdict(case['gate_rc'], case['killed'])
    successor = candidate.outcome_verdict(case['gate_out'], case['killed'])
    ok = got == case['expected']
    correct += ok
    line = f"PROTO_R72_C2 case={case['id']} expect={case['expected']} held={got} held_correct={'yes' if ok else 'NO'}"
    print(line)
    if line not in baseline:
        differences.append('baseline: ' + case['id'])
    candidate_ok = successor == case['expected']
    expected = f"MADO_R72_CASE case={case['id']} expect={case['expected']} candidate={successor} base={got} correct={'yes' if candidate_ok else 'no'} base_correct={'yes' if ok else 'no'}"
    if expected not in measurement:
        differences.append('measurement: ' + case['id'])
print(f'INDEPENDENT_BASELINE: cases={len(cases)} correct={correct}')
print('RECONCILIATION: differences=' + str(len(differences)))
for difference in differences:
    print(difference)
