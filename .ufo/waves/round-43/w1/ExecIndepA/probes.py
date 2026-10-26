import importlib.util, os, subprocess, sys, json

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
TOOL = LANE + '/.ufo/waves/round-43/w1/ExecIndepA/mado-geometry.py'
spec = importlib.util.spec_from_file_location('c1', LANE + '/quality/counters/c1-r42-geometry.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
WORK = '/fast/scratch/hyaku/mado-r43/ExecIndepA/probes'
os.makedirs(WORK, exist_ok=True)

def mine(args, stdin=b''):
    p = subprocess.run([sys.executable, '-I', TOOL] + args, input=stdin,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return p.stdout.decode('utf-8', 'replace'), p.returncode

def case(name, clients, texts, cwd=None):
    cpath = os.path.join(WORK, name + '.json')
    with open(cpath, 'wb') as h:
        h.write(clients.encode('utf-8'))
    paths = []
    for i, t in enumerate(texts):
        p = os.path.join(WORK, '%s_r%d.conf' % (name, i))
        with open(p, 'wb') as h:
            h.write(t.encode('utf-8'))
        paths.append(p)
    args = ['--clients', cpath]
    for p in paths:
        args.extend(['--rules', p])
    want_stdout, want_rc = m.model_out(clients.encode('utf-8'), texts)
    got_stdout, got_rc = mine(args)
    same = (want_stdout == got_stdout and want_rc == got_rc)
    print('== %s  agree=%s  model_rc=%d mine_rc=%d' % (name, same, want_rc, got_rc))
    if not same:
        wl = want_stdout.split('\n')
        gl = got_stdout.split('\n')
        for i in range(max(len(wl), len(gl))):
            a = wl[i] if i < len(wl) else '<missing>'
            b = gl[i] if i < len(gl) else '<missing>'
            if a != b:
                print('   model:', repr(a))
                print('   mine :', repr(b))
    else:
        print('   model_out first line:', repr(want_stdout.split('\n')[0]))
    return same

C = json.dumps([{"class": "x", "mapped": True, "floating": False, "size": [1, 2]}])
Cf = json.dumps([{"class": "x", "mapped": True, "floating": True, "size": [1, 2]}])

results = {}
results['float-one-token-total'] = case(
    'float1', Cf, ['windowrule = float on, match:class x\n'])
results['float-rule-vs-client-floating'] = case(
    'float2', C, ['windowrule = size 1 2, match:class x\nwindowrule = float on, match:class x\n'])
results['float-tab-separated'] = case(
    'float3', Cf, ['windowrule =\tfloat\toff, match:class\tx\n'])
results['size-leading-zeros'] = case(
    'zero', Cf, ['windowrule = size 0001 002, match:class x\n'])
results['size-tab-separated'] = case(
    'tab', Cf, ['windowrule =\tsize\t1\t2,\tmatch:class\tx\n'])
esc150 = 'match:class ' + ('a\\.' * 75)   # 150 units, 300 source characters
results['regex-150-escapes'] = case(
    'esc150', Cf, ['windowrule = size 1 2, ' + esc150 + '\n'])
esc101 = 'match:class ' + ('a\\.' * 101)  # 202 source characters, 202 units
results['regex-202-units'] = case(
    'esc202', Cf, ['windowrule = size 1 2, ' + esc101 + '\n'])
results['regex-200-plain'] = case(
    'rx200', Cf, ['windowrule = size 1 2, match:class ' + 'a' * 200 + '\n'])
results['regex-201-plain'] = case(
    'rx201', Cf, ['windowrule = size 1 2, match:class ' + 'a' * 201 + '\n'])
results['mapped-zero'] = case(
    'map0', json.dumps([{"class": "x", "mapped": 0, "floating": True, "size": [1, 2]}]),
    ['windowrule = size 1 2, match:class x\n'])
results['mapped-null'] = case(
    'mapnull', json.dumps([{"class": "x", "mapped": None, "floating": True, "size": [1, 2]}]),
    ['windowrule = size 1 2, match:class x\n'])
results['mapped-string-false'] = case(
    'mapstr', json.dumps([{"class": "x", "mapped": "false", "floating": True, "size": [1, 2]}]),
    ['windowrule = size 1 2, match:class x\n'])
results['size-float-1500'] = case(
    'floatsz', json.dumps([{"class": "x", "mapped": True, "floating": True, "size": [1.5, 2]}]),
    ['windowrule = size 1 2, match:class x\n'])
results['size-bool'] = case(
    'boolsz', json.dumps([{"class": "x", "mapped": True, "floating": True, "size": [True, 2]}]),
    ['windowrule = size 1 2, match:class x\n'])
results['float-rule-off-only'] = case(
    'floatoff', Cf, ['windowrule = float off, match:class x\n'])
results['windowrule-no-space'] = case(
    'nospace', Cf, ['windowrule=size 1 2, match:class x\n'])
results['escape-backslash-backslash'] = case(
    'bslash', json.dumps([{"class": "a", "mapped": True, "floating": True, "size": [1, 2]}]),
    ['windowrule = size 1 2, match:class a\\\\\n'])
results['class-control-char'] = case(
    'ctl', json.dumps([{"class": "a\nb", "mapped": True, "floating": True, "size": [1, 2]}]),
    ['windowrule = size 1 2, match:class a\\sb\n'])
print('AGREED %d/%d' % (sum(1 for v in results.values() if v), len(results)))

# rules path named '-' (relative), child cwd
dashdir = os.path.join(WORK, 'dashdir')
os.makedirs(dashdir, exist_ok=True)
with open(os.path.join(dashdir, '-'), 'wb') as h:
    h.write(b'windowrule = size 1 2, match:class x\n')
with open(os.path.join(dashdir, 'c.json'), 'wb') as h:
    h.write(Cf.encode('utf-8'))
want_stdout, want_rc = m.model_out(Cf.encode('utf-8'), ['windowrule = size 1 2, match:class x\n'])
p = subprocess.run([sys.executable, '-I', TOOL, '--clients', 'c.json', '--rules', '-'],
                   cwd=dashdir, input=b'', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print('== dash-rules-path agree=%s model_rc=%d mine_rc=%d'
      % (want_stdout == p.stdout.decode('utf-8', 'replace') and want_rc == p.returncode,
         want_rc, p.returncode))
print('   mine:', repr(p.stdout.decode('utf-8', 'replace')[:160]))
