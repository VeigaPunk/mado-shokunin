import json, os, sys, tempfile, subprocess, shutil, importlib.util
ORACLE = '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/controls/xdgmime-oracle-r92.py'
CASES = '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/controls/xdgmime-cases-r92-gr-unlabelled.json'
CAND = '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/build/mado-xdgmime.c1.py'
spec = importlib.util.spec_from_file_location('oracle', ORACLE)
oracle = importlib.util.module_from_spec(spec); spec.loader.exec_module(oracle)
doc = json.load(open(CASES))
S = '/fast/scratch/hyaku/mado-r92/R92MExecGrep'
os.makedirs(S, exist_ok=True)
disagree = []
for c in doc['cases']:
    root = tempfile.mkdtemp(prefix='c', dir=S)
    try:
        oracle.materialise(c, root)
        env = oracle.env_of(c, root)
        r = subprocess.run([sys.executable, CAND, '--json'] + sum([['--env', f'{k}={v}'] for k, v in env.items()], []) + c['types'],
                           cwd=root, capture_output=True, timeout=60)
        got = {}
        if r.returncode == 0:
            res = json.loads(r.stdout)['results']
            got = {x['type']: {'default': x['default'], 'rc': x['rc']} for x in res}
        else:
            got = {'__rc': r.returncode, '__stderr': r.stderr.decode('utf-8','replace')[:200]}
        if got != c['expect']:
            disagree.append((c['id'], c['types'], c['expect'], got))
    finally:
        oracle.restore_modes(root); shutil.rmtree(root, ignore_errors=True)
print(f"disagreements: {len(disagree)} / {len(doc['cases'])}")
for id_, t, exp, got in disagree:
    print(f"{id_} types={t}\n  oracle={exp}\n  cand={got}\n")
json.dump([{"id":i,"types":t,"expect":e,"candidate":g} for i,t,e,g in disagree], open(f'{S}/disagreements.json','w'), indent=1)
