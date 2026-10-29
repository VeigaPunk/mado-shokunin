import json, os, subprocess, sys
EXP = '/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/export/.ufo/waves/round-56/fixtures/c2'
INTERP = '/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/interp.py'
WORK = '/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/work'
ok = 0
for n in range(1, 10):
    fx = f'{EXP}/F{n:02d}'
    args = [a.replace('{FX}', fx) for a in json.load(open(f'{fx}/args.json'))]
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': WORK}
    p = subprocess.run(['python3', '-I', INTERP] + args, cwd=WORK, env=env, capture_output=True)
    exp_out = open(f'{fx}/expected.out', 'rb').read()
    exp_rc = int(open(f'{fx}/expected.rc').read().strip())
    same = (p.stdout == exp_out and p.returncode == exp_rc)
    ok += same
    print(f'F{n:02d} stdout_match={p.stdout == exp_out} rc_match={p.returncode == exp_rc} interp_rc={p.returncode} exp_rc={exp_rc} stderr={p.stderr.decode()!r}')
    open(f'{WORK}/F{n:02d}.interp.out', 'wb').write(p.stdout)
    if not same:
        import difflib
        sys.stdout.write(''.join(difflib.unified_diff(exp_out.decode().splitlines(True), p.stdout.decode().splitlines(True), 'expected.out', 'interp.out')))
print('MATCHED', ok, '/ 9')
