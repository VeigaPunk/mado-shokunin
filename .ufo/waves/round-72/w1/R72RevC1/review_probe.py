#!/usr/bin/env python3
"""Read-only revision extraction; real bash fixtures; scripted non-MZ harness children."""
import argparse, contextlib, io, json, os, pathlib, subprocess, types

p = argparse.ArgumentParser()
p.add_argument('--scratch-root', required=True)
a = p.parse_args()
root = pathlib.Path(a.scratch_root).resolve()
assert str(root) == '/fast/scratch/hyaku/mado-r72/R72RevC1'
root.mkdir(parents=True, exist_ok=True)
repo = '/home/vgpnk/Projects/shokunin/mado-shokunin'
base_rev = '976684a27e99c2508037a60eec415f550f53d70e'
rev = '9bcb4fd5b598844f168230dc05e441721d95b272'
def load(revision, name):
    path = 'quality/counters/' + name + '.py'
    data = subprocess.check_output(['git', '-C', repo, 'show', revision + ':' + path])
    m = types.ModuleType(name)
    exec(compile(data, path, 'exec'), m.__dict__)
    return m
candidate = load(rev, 'c1-r72-landing-controls')
base = load(base_rev, 'c1-r71-landing-controls')
counter = load(rev, 'c1-r72-summary-credit')
S = 'MADO_LANDING_COUNTERS_SELFTEST: '
F = 'SELFTEST FAIL 2: zero citations refused want=1 got=0\n'
probes = {
 'nested-detail': 'nested runner output follows\n' + F + 'wrapper did not assert anything\n' + S + '1/2 assertions passed\n',
 'wrapper-echo': F + S + '1/2 assertions passed\n',
 'unrelated-detail': 'SELFTEST FAIL 88: unrelated nested test\n' + S + '1/2 assertions passed\n',
 'prefix-not-fail-line': 'SELFTEST FAILURE: wrapper logging only\n' + S + '1/2 assertions passed\n',
 'valid-then-garbled': F + S + '1/2 assertions passed\n' + S + 'runner cleanup complete\n',
 'different-spelling': 'SELFTEST failed 2: zero citations refused\n' + S + '1/2 assertions passed\n',
 'no-details': S + '1/2 assertions passed\n',
 'summary-before-detail': S + '1/2 assertions passed\n' + F,
 'two-genuine-run-blocks': F + S + '1/2 assertions passed\n' + F + S + '1/2 assertions passed\n',
}
for name, out in probes.items():
    print('PROBE ' + json.dumps(dict(name=name, credit=candidate.credit(out), fails=candidate.count_fails(out), last=candidate.last_summary(out), output=out), sort_keys=True))
# The new frozen count is independently derived by running each actual bash child.
# Drive both committed measure bodies; every non-MZ child is their own scripted stub.
# No git write command is executed (scripted argv dispatch only).
counts = {'candidate': 0, 'base': 0}
for mode in counter.MODES:
    script = counter.LANE_TEMPLATE.replace('@MODE@', mode)
    # Guarded and guard-deleted children are both real bash subprocesses.
    guarded = subprocess.run(['bash'], input=script.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=root)
    mutant = script.replace(counter.Z_CLAUSE.decode(), '', 1)
    child = subprocess.run(['bash'], input=mutant.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=root)
    out = child.stdout + child.stderr
    got = {}
    contracts = {}
    for label, harness in [('candidate', candidate), ('base', base)]:
        work = root / (label + '-' + mode)
        work.mkdir(exist_ok=True)
        case = dict(name=mode, mz_rc=child.returncode, mz_stdout=out, child_rc=0, child_marker=harness.MET_MARKER)
        rc, contract = harness._measure_case(str(work), case, 'a' * 40)
        prefix = counter.CAND_PREFIX if label == 'candidate' else counter.BASE_PREFIX
        got[label] = counter.parse_mz(contract, prefix)
        counts[label] += got[label] == counter.EXPECT[mode]
        contracts[label] = contract
    print('MODE ' + json.dumps(dict(mode=mode, expected=counter.EXPECT[mode], guarded_rc=guarded.returncode, child_rc=child.returncode, stdout=child.stdout.decode(), stderr=child.stderr.decode(), got=got, contracts=contracts), sort_keys=True))
print('DERIVED_COUNTS ' + json.dumps(counts, sort_keys=True))
assert counts == dict(candidate=8, base=6)
# A real failing bash assertion with the summary emitted before its detail.
shell = "printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; if [ 0 -eq 1 ]; then :; else printf 'SELFTEST FAIL 2: real assertion\\n'; fi; exit 1"
r = subprocess.run(['bash', '-c', shell], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print('REAL_SUMMARY_FIRST ' + json.dumps(dict(rc=r.returncode, credit=candidate.credit((r.stdout+r.stderr).decode()), stdout=r.stdout.decode())))
# Both streams are captured, but no delimiter is inserted by the actual measure body.
r = subprocess.run(['bash', '-c', "printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed'; printf 'SELFTEST FAIL 2: real assertion\\n' >&2; exit 1"], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print('REAL_NO_NEWLINE_SPLIT ' + json.dumps(dict(rc=r.returncode, credit=candidate.credit((r.stdout+r.stderr).decode()), stdout=r.stdout.decode(), stderr=r.stderr.decode())))
