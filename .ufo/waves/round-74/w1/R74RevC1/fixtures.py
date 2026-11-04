#!/usr/bin/env python3
"""Assigned C1 adversarial review; writes receipts only beneath --output-dir."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--scratch-root', required=True)
p.add_argument('--output-dir', required=True)
a = p.parse_args()
scratch = Path(a.scratch_root).resolve(strict=True)
outdir = Path(a.output_dir).resolve(strict=True)
rulepath = Path('/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r74-witness-rule.py')
rule = runpy.run_path(str(rulepath))
nonce = 'a1b2c3d4e5f60718'
stale = '0123456789abcdef'
summary = 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n'
detail = 'SELFTEST FAIL 1: genuine arithmetic detail want=1 got=0\n'
witness = 'MADO_LANDING_WITNESS: ' + nonce + '\n'

def frozen(out, challenge):
    # Literal frozen sentence: last parsed summary, matching detail count,
    # last 16-hex witness equals the supplied challenge; no child identity input.
    summaries = re.findall(r'^MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed$', out, re.M)
    witnesses = re.findall(r'^MADO_LANDING_WITNESS: ([0-9a-fA-F]{16})$', out, re.M)
    if not summaries or not witnesses:
        return False
    passed, total = map(int, summaries[-1])
    fails = len(re.findall(r'^SELFTEST FAIL [0-9]+: ', out, re.M))
    return total > 0 and passed < total and fails == total - passed and witnesses[-1] == challenge

cases = [
    ('witness-after-summary', detail + summary + witness, '', nonce),
    ('stderr-only-witness', detail + summary, witness, nonce),
    ('two-summaries-green-then-failing', witness + 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n' + detail + summary, '', nonce),
    ('witness-trailing-spaces', witness.rstrip('\n') + '   \n' + detail + summary, '', nonce),
    ('witness-crlf', witness.replace('\n', '\r\n') + detail + summary, '', nonce),
    ('uppercase-witness-lowercase-challenge', witness.upper().replace('MADO_LANDING_WITNESS', 'MADO_LANDING_WITNESS') + detail + summary, '', nonce),
    ('uppercase-witness-matching-challenge', 'MADO_LANDING_WITNESS: ' + nonce.upper() + '\n' + detail + summary, '', nonce.upper()),
    ('seventeen-hex-witness', witness.rstrip('\n') + '0\n' + detail + summary, '', nonce),
    ('passed-greater-than-total', witness + 'MADO_LANDING_COUNTERS_SELFTEST: 3/2 assertions passed\n', '', nonce),
    ('captured-genuine-detail-stale-witness', 'MADO_LANDING_WITNESS: ' + stale + '\n' + detail + summary, '', nonce),
    ('valid-then-uppercase-wrong-witness', witness + 'MADO_LANDING_WITNESS: DEADBEEFDEADBEEF\n' + detail + summary, '', nonce),
    ('valid-then-seventeen-hex-witness', witness + 'MADO_LANDING_WITNESS: 0123456789abcdef0\n' + detail + summary, '', nonce),
    ('last-valid-witness-wrong', witness + 'MADO_LANDING_WITNESS: ' + stale + '\n' + detail + summary, '', nonce),
]
# Separate actual children emit identical captured bytes under the same challenge.
for child in ('A', 'B'):
    r = subprocess.run(['bash', '-c', 'printf "%s" "$1"', 'review-child-' + child, witness + detail + summary], cwd=scratch, capture_output=True, text=True, check=True)
    cases.append(('same-nonce-child-' + child, r.stdout, r.stderr, nonce))
results = []
for name, stdout, stderr, challenge in cases:
    text = stdout + stderr  # canonical counter concatenation at line 293
    actual = rule['credit'](text, challenge)
    # Frozen sentence does not specify outer whitespace; report literal and
    # existing strip/splitlines normalization separately rather than hide it.
    normalized = '\n'.join(line.strip() for line in text.splitlines()) + '\n'
    expected = frozen(normalized, challenge)
    results.append(dict(name=name, stdout=stdout, stderr=stderr, nonce=challenge,
                        actual='accept' if actual else 'reject',
                        frozen='accept' if expected else 'reject', agrees=actual == expected))
receipt = dict(rule_sha256=hashlib.sha256(rulepath.read_bytes()).hexdigest(),
               fixtures=len(results), agreements=sum(r['agrees'] for r in results), results=results)
(outdir / 'fixtures-results.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('rule_sha256=' + receipt['rule_sha256'])
for r in results:
    print('{name}: rule={actual} frozen={frozen} agrees={agrees}'.format(**r))
print('fixtures=%d agreements=%d disagreements=%d' % (len(results), receipt['agreements'], len(results) - receipt['agreements']))
