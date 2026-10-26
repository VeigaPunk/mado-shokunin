import importlib.util, os, subprocess, sys, json, random

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
TOOL = LANE + '/.ufo/waves/round-43/w1/ExecIndepA/mado-geometry.py'
spec = importlib.util.spec_from_file_location('c1', LANE + '/quality/counters/c1-r42-geometry.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

WORK = '/fast/scratch/hyaku/mado-r43/ExecIndepA/cases'
os.makedirs(WORK, exist_ok=True)

def run(args, stdin_bytes):
    p = subprocess.run([sys.executable, '-I', TOOL] + args, input=stdin_bytes,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return p.stdout, p.returncode, p.stderr

bad = []
rows = []
BASE = int(sys.argv[1]); COUNT = int(sys.argv[2])
for case in range(COUNT):
    rng = m.random.Random(BASE + case)
    lines, wants = m.gen_texts(rng)
    text = '\n'.join(lines)
    clients = json.dumps(m.gen_clients(rng, wants)).encode('utf-8')
    # split the lines into 1-3 consecutive rule files
    nfiles = 1 + (case % 3)
    chunks = []
    if nfiles == 1 or not lines:
        chunks = [text]
    else:
        size = max(1, (len(lines) + nfiles - 1) // nfiles)
        parts = [lines[i:i + size] for i in range(0, len(lines), size)]
        chunks = ['\n'.join(p) for p in parts]
    expected_stdout, expected_rc = m.model_out(clients, chunks)
    paths = []
    for i, chunk in enumerate(chunks):
        path = os.path.join(WORK, 'r%d_%d.conf' % (case, i))
        with open(path, 'wb') as h:
            h.write(chunk.encode('utf-8'))
        paths.append(path)
    args = []
    use_stdin = (case % 2 == 1)
    if use_stdin:
        args = ['--clients', '-']
        stdin_bytes = clients
    else:
        cpath = os.path.join(WORK, 'c%d.json' % case)
        with open(cpath, 'wb') as h:
            h.write(clients)
        args = ['--clients', cpath]
        stdin_bytes = b''
    for p in paths:
        args.extend(['--rules', p])
    got_stdout, got_rc, err = run(args, stdin_bytes)
    ok = (got_stdout == expected_stdout.encode('utf-8') and got_rc == expected_rc and err == b'')
    rows.append((case, ok, got_rc, expected_rc))
    if not ok:
        bad.append((case, args, chunks, clients, expected_stdout, expected_rc,
                    got_stdout.decode('utf-8', 'replace'), got_rc, err))

print('cases=%d agree=%d disagree=%d base=%d' % (len(rows), sum(1 for r in rows if r[1]), len(bad), BASE))
for entry in bad[:10]:
    case, args, chunks, clients, eo, erc, go, grc, err = entry
    print('--- case', case, 'args', args)
    print('clients:', clients.decode('utf-8', 'replace')[:400])
    for ch in chunks:
        print('rules:', repr(ch)[:300])
    print('expected rc', erc)
    print('got      rc', grc, 'stderr', err[:200])
    el = eo.split('\n')
    gl = go.split('\n')
    for i in range(max(len(el), len(gl))):
        a = el[i] if i < len(el) else '<missing>'
        b = gl[i] if i < len(gl) else '<missing>'
        if a != b:
            print('line', i)
            print('  model:', repr(a))
            print('  mine :', repr(b))
print('DISAGREEMENTS', len(bad))
