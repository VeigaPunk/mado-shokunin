#!/usr/bin/env python3
"""Read-only r72 claim probes; no module imports, fixture builds, or git mutation."""
import ast
import hashlib
import json
import re
import subprocess
import sys

REPO = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = '9bcb4fd5b598844f168230dc05e441721d95b272'
BASE = '976684a27e99c2508037a60eec415f550f53d70e'
C1 = 'quality/counters/c1-r72-summary-credit.py'
C2 = 'quality/counters/c2-r72-outcome.py'
HARNESS = 'quality/counters/c1-r72-landing-controls.py'
HELD = 'quality/counters/c1-r71-landing-controls.py'
CONTROL1 = '.ufo/waves/round-72/controls/c1-modes-r72.json'
CONTROL2 = '.ufo/waves/round-72/controls/c2-controls-r72.json'

def blob(path, rev=REV):
    return subprocess.check_output(['git', '-C', REPO, 'show', rev + ':' + path])

def tree(path, rev=REV):
    return ast.parse(blob(path, rev), filename=path)

def functions(path, names, rev=REV):
    selected = [n for n in tree(path, rev).body
                if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in selected} == set(names)
    ns = {'re': re}
    exec(compile(ast.Module(body=selected, type_ignores=[]), path, 'exec'), ns)
    return ns

def assigned(path, name):
    for n in tree(path).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise ValueError(name)

labels1 = json.loads(blob(CONTROL1))['expect']
labels2 = json.loads(blob(CONTROL2))['cases']
score1 = functions(C1, ['score'])['score']
score2 = functions(C2, ['score'])['score']
candidate = functions(HARNESS, ['last_summary', 'count_fails', 'credit', 'summary_green', 'outcome_verdict'])
held = functions(HELD, ['outcome_verdict'], BASE)
section = sys.argv[1]
print('SECTION', section, 'rev=' + REV, 'base=' + BASE)
if section == 'q1':
    for answer in ('fail', 'pass', None):
        hits = sum(score1(expected, answer) for expected in labels1.values())
        print('C1 constant=%r correct=%d/8 target=%s' % (answer, hits, hits == 8))
    for answer in ('TARGET_MISSED', 'TARGET_MET', None):
        hits = sum(score2(c['expected'], answer) for c in labels2)
        print('C2 constant=%r correct=%d/8 target=%s' % (answer, hits, hits == 8))
elif section == 'q2':
    print('C1 missing verdict accepted:', any(score1(label, None) for label in labels1.values()))
    print('C2 missing verdict accepted:', any(score2(c['expected'], None) for c in labels2))
    print('C1 copied EXPECT matches frozen JSON:', assigned(C1, 'EXPECT') == labels1)
    print('C2 candidate own function correct=%d/8' % sum(score2(c['expected'], candidate['outcome_verdict'](c['gate_out'], c['killed'])) for c in labels2))
    print('C2 held own function correct=%d/8' % sum(score2(c['expected'], held['outcome_verdict'](c['gate_rc'], c['killed'])) for c in labels2))
    def wrong_successor(out, killed):
        m = re.search(r'MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed', out)
        return 'TARGET_MET' if m and m.group(1) == m.group(2) and killed == 2 else 'TARGET_MISSED'
    print('C2 wrong successor (first match; no n>0) correct=%d/8' % sum(score2(c['expected'], wrong_successor(c['gate_out'], c['killed'])) for c in labels2))
    zero = 'MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed'
    print('C2 0/0 frozen=TARGET_MISSED wrong_successor=' + wrong_successor(zero, 2))
    green_then_garbled = 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\nMADO_LANDING_COUNTERS_SELFTEST: garbled'
    fail_then_garbled = 'SELFTEST FAIL 1: x\nMADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\nMADO_LANDING_COUNTERS_SELFTEST: garbled'
    print('C1 valid failing + garbled trailer: last-PARSED expectation=True actual=' + str(candidate['credit'](fail_then_garbled)))
    print('C2 valid green + garbled trailer: last-PARSED expectation=TARGET_MET actual=' + candidate['outcome_verdict'](green_then_garbled, 2))
    for path in (C1, C2):
        for n in tree(path).body:
            if isinstance(n, ast.FunctionDef) and n.name == 'measure':
                calls = sorted({ast.unparse(c.func) for c in ast.walk(n) if isinstance(c, ast.Call)})
                print(path, 'measure calls:', ', '.join(calls))
elif section == 'q3':
    for path, rev in ((HARNESS, REV), (HELD, BASE), (C1, REV), (C2, REV), (CONTROL1, REV), (CONTROL2, REV)):
        data = blob(path, rev)
        print('COMMITTED', rev, path, 'sha256=' + hashlib.sha256(data).hexdigest())
    for path in ('.ufo/waves/round-72/measurement-c1-r72.txt', '.ufo/waves/round-72/measurement-c2-r72.txt'):
        with open(REPO + '/' + path, encoding='utf-8') as f:
            text = f.read()
        for line in text.splitlines():
            if line.startswith(('MADO_R72_REVS', 'MADO_R72_SUMMARY_CREDIT:', 'MADO_R72_OUTCOME:', 'C1_RC=', 'C2_RC=')):
                print(path, line)
    for path in ('.ufo/waves/round-72/control-baseline-c1-r72.txt', '.ufo/waves/round-72/control-baseline-c2-r72.txt'):
        with open(REPO + '/' + path, encoding='utf-8') as f:
            lines = f.read().splitlines()
        scored = [line for line in lines if line.startswith(('PROTO_R72_C1 ', 'PROTO_R72_C2 '))]
        correct = sum('correct_for_held=yes' in line or 'held_correct=yes' in line for line in scored)
        print(path, 'held_correct=%d/%d' % (correct, len(scored)))
elif section == 'q4':
    for path in (C1, C2):
        for n in tree(path).body:
            if isinstance(n, ast.FunctionDef) and n.name in ('measure', 'run_harness', 'load_module'):
                calls = sorted({ast.unparse(c.func) for c in ast.walk(n) if isinstance(c, ast.Call)})
                print(path, n.name, 'calls:', ', '.join(calls))
    print('C1 invokes whole subprocess harness; control labels embedded in EXPECT; neither JSON control set is read by measure.')
    print('C2 imports whole harness modules and calls candidate/held outcome_verdict; only C2 controls JSON read by measure.')
else:
    raise SystemExit('unknown section')
