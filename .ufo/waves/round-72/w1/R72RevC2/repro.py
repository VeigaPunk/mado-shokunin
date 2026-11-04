#!/usr/bin/env python3
"""Read-only committed-code review; all measurement writes confined to --scratch-root."""
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import types

p = argparse.ArgumentParser()
p.add_argument('--scratch-root', required=True)
a = p.parse_args()
repo = '/home/vgpnk/Projects/shokunin/mado-shokunin'
rev = '9bcb4fd5b598844f168230dc05e441721d95b272'
base = '976684a27e99c2508037a60eec415f550f53d70e'
os.makedirs(a.scratch_root, exist_ok=True)

def load(ref, path):
    source = subprocess.check_output(['git', '-C', repo, 'show', ref + ':' + path])
    m = types.ModuleType('review_' + path.replace('/', '_'))
    m.__file__ = os.path.join(a.scratch_root, os.path.basename(path))
    exec(compile(source, m.__file__, 'exec'), m.__dict__)
    return m

h = load(rev, 'quality/counters/c1-r72-landing-controls.py')
b = load(base, 'quality/counters/c1-r71-landing-controls.py')
c = load(rev, 'quality/counters/c2-r72-outcome.py')
green = 'MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed'
red = 'MADO_LANDING_COUNTERS_SELFTEST: 11/12 assertions passed'
cases = [
    ('green-then-real-setup-exit2', [(green, 'out'), ('fatal: setup dependency unavailable', 'err')], 2),
    ('same-stream-green-then-fail', [(green, 'out'), (red, 'out')], 0),
    ('same-stream-fail-then-green', [(red, 'out'), (green, 'out')], 0),
    ('stderr-only-green', [(green, 'err')], 0),
    ('stderr-fail-then-stdout-green', [(red, 'err'), (green, 'out')], 0),
    ('stderr-green-then-stdout-fail', [(green, 'err'), (red, 'out')], 0),
    ('green-then-garbled-fraction', [(green, 'out'), ('MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed INVALID', 'out')], 0),
    ('green-then-garbled-no-fraction', [(green, 'out'), ('MADO_LANDING_COUNTERS_SELFTEST: invalid', 'out')], 0),
]
results = []
for name, events, gate_rc in cases:
    # Statements flush immediately, establishing program order across both streams.
    source = 'import sys\n' + '\n'.join('print(%r, file=sys.%s, flush=True)' % (text, 'stdout' if stream == 'out' else 'stderr') for text, stream in events) + '\nsys.exit(%d)\n' % gate_rc
    child = subprocess.run([sys.executable, '-I', '-c', source], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=a.scratch_root)
    merged = child.stdout.decode() + child.stderr.decode()
    scripted = h._scripted_run({'mz_rc': 1, 'child_rc': 0, 'child_marker': h.MET_MARKER}, 'a' * 40)
    def fake(argv, env, cwd=None, input_bytes=None, timeout=900):
        if argv[0] == 'bash' and '--selftest' in argv and '/mz/' not in ' '.join(argv):
            return child
        return scripted(argv, env, cwd=cwd, input_bytes=input_bytes, timeout=timeout)
    h.run = fake
    work = os.path.join(a.scratch_root, name)
    os.makedirs(work, exist_ok=True)
    args = types.SimpleNamespace(repo=a.scratch_root, rev='HEAD', scratch_root=work)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        rc = h.measure(args)
    result = {'case': name, 'events_in_program_order': events, 'gate_rc': child.returncode,
              'summary_fraction': h.summary_fraction(merged), 'summary_green': h.summary_green(merged),
              'verdict': h.outcome_verdict(merged, 2), 'base_verdict': b.outcome_verdict(child.returncode, 2),
              'counter_oracle': c.expected_from_summary(merged, 2), 'harness_rc': rc,
              'receipt': [s for s in capture.getvalue().splitlines() if s.startswith(('MADO_R72_SELFTEST ', 'MADO_R72_LANDING_CONTROLS:'))]}
    results.append(result)
print(json.dumps({'instrument_revision': rev, 'base_revision': base, 'results': results}, indent=2))
