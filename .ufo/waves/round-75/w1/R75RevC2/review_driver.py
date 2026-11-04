import ast, difflib, importlib.util, json, pathlib, subprocess, types
ROOT = pathlib.Path('/fast/scratch/hyaku/mado-r75/R75RevC2')
REPO = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = 'def73656c94f0e88bd671cfb4a65124338261722'
BASE = 'b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6'
def git(*args):
    return subprocess.check_output(['git', '-C', REPO, *args], text=True)
spec = importlib.util.spec_from_file_location('frozen', ROOT / 'c2-r75-shapes.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
b = types.ModuleType('held')
held = git('show', BASE + ':quality/counters/c2-r74-shapes.py')
exec(compile(held, '<held-r74>', 'exec'), b.__dict__)
new = (ROOT / 'c2-r75-shapes.py').read_text()
(ROOT / 'counter-diff.txt').write_text(''.join(difflib.unified_diff(held.splitlines(True), new.splitlines(True), fromfile='held-r74', tofile='frozen-r75')))
cases = json.loads((ROOT / 'c2-cases-r75.json').read_text())['cases']
print('AXES: guard precision; guard recall; frozen-label validity; census reproducibility; no mutation')
for name in ['copy-dict-kw-bound','copy-splat-bound','copy-dict-value-position','del-env-literal-cancel']:
    c = next(c for c in cases if c['name'] == name)
    print('REDERIVE', name, 'held=', b.classify(c['src']), 'successor=', m.classify(c['src']), 'label=', (c['expect_reader'],c['expect_guard']))
print('POPULATION independently enumerated via ls-tree, direct-child filename predicate')
paths = sorted(p for p in git('ls-tree','-r','--name-only',REV,'--','quality').splitlines() if pathlib.PurePosixPath(p).parent.as_posix() == 'quality' and pathlib.PurePosixPath(p).name.startswith('check-') and p.endswith('.py'))
rows=[]
for p in paths:
    src=git('show',REV + ':' + p)
    r,g=m.classify(src)
    rows.append((p,r,g))
    print('POP',p,'reader=',r,'guard=',g)
print('TOTAL',len(paths),sum(r for _,r,g in rows),sum(g for _,r,g in rows),sum(r and not g for _,r,g in rows))
print('ENUMERATION_MISMATCH',set(paths)^set(m.population_at(REPO,REV)))
call='    subprocess.run(["git", "show", "HEAD:a"], env=child)\n'
probes={
'positional-child': 'def run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "show", "HEAD:a"], child)\n',
'positional-helper-ignores-child': 'def wrapper(argv, metadata):\n    return subprocess.run(argv)\ndef run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    wrapper(["git", "show", "HEAD:a"], child)\n',
'dead-delete': 'def run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    if False:\n        del child["GIT_NO_REPLACE_OBJECTS"]\n'+call,
'other-scope-delete': 'def run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    def unrelated():\n        child = dict(GIT_NO_REPLACE_OBJECTS="1")\n        del child["GIT_NO_REPLACE_OBJECTS"]\n'+call,
'delete-then-restore': 'def run():\n    env = dict(GIT_NO_REPLACE_OBJECTS="1")\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "show", "HEAD:a"], env=env)\n',
'copy-alias-delete': 'def run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    env = child\n    del env["GIT_NO_REPLACE_OBJECTS"]\n'+call,
'environ-other-scope-delete': 'def run():\n    env = os.environ\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    def unrelated():\n        env = {"GIT_NO_REPLACE_OBJECTS":"1"}\n        del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "show", "HEAD:a"], env=dict(env))\n',
'environ-rebound-store': 'def run():\n    env = os.environ\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    env = {}\n    subprocess.run(["git", "show", "HEAD:a"], env=dict(env))\n',
}
class FakeSubprocess:
    def __init__(self): self.calls=[]
    def run(self,*args,**kwargs):
        self.calls.append({'args':repr(args),'guard':kwargs.get('env',{}).get(m.KEY), 'has_env': 'env' in kwargs})
        return None
for name,src in probes.items():
    fake=FakeSubprocess()
    ns={'subprocess':fake,'os':types.SimpleNamespace(environ={})}
    try:
        exec(src, ns)
        ns['run']()
        observed=fake.calls
    except Exception as e: observed=type(e).__name__+': '+str(e)
    print('PROBE',name,'held=',b.classify(src),'successor=',m.classify(src),'runtime=',observed)
    print(src)
case=next(c for c in cases if c['name']=='del-before-store')
fake=FakeSubprocess(); ns={'subprocess':fake}
try:
    exec(case['src'],ns)
    ns['run']('/unused')
    observed=fake.calls
except Exception as e: observed=type(e).__name__+': '+str(e)
print('FROZEN_DEL_BEFORE_STORE_RUNTIME',observed,'launches=',len(fake.calls))
