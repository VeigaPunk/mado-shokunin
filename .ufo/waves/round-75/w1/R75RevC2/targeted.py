import importlib.util, json, pathlib, subprocess, types
R=pathlib.Path('/fast/scratch/hyaku/mado-r75/R75RevC2')
spec=importlib.util.spec_from_file_location('frozen',R/'c2-r75-shapes.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
b=types.ModuleType('held'); exec(compile(subprocess.check_output(['git','-C','/home/vgpnk/Projects/shokunin/mado-shokunin','show','b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6:quality/counters/c2-r74-shapes.py'],text=True),'<held>','exec'),b.__dict__)
class Fake:
    def __init__(self):self.calls=[]
    def run(self,*a,**kw):self.calls.append({'has_env': 'env' in kw,'key':kw.get('env',{}).get(m.KEY)})
cases=json.loads((R/'c2-cases-r75.json').read_text())['cases']
out=[]
for name in ['copy-dict-kw-bound','copy-splat-bound','copy-dict-value-position','del-env-literal-cancel']:
    c=next(c for c in cases if c['name']==name); fake=Fake(); ns={'os':types.SimpleNamespace(environ={}), 'subprocess':fake};exec(c['src'],ns);ns['run']('/unused')
    out.append('INDEPENDENT_RUNTIME '+name+' '+repr(fake.calls))
probes={
'env-dead-delete':'def run():\n    env = dict(GIT_NO_REPLACE_OBJECTS="1")\n    if False:\n        del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "show", "HEAD:a"], env=env)\n',
'environ-unrelated-param-delete':'def run():\n    env = os.environ\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    def unrelated(env):\n        del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "show", "HEAD:a"], env=dict(env))\n',
'guarded-helper-metadata':'def wrapper(argv, metadata):\n    return subprocess.run(argv)\ndef run():\n    child = dict(GIT_NO_REPLACE_OBJECTS="1")\n    wrapper(["git", "show", "HEAD:a"], child)\n',
}
for name,src in probes.items():
    fake=Fake();ns={'os':types.SimpleNamespace(environ={}), 'subprocess':fake};exec(src,ns);ns['run']()
    out.extend(['PROBE '+name+' held='+repr(b.classify(src))+' successor='+repr(m.classify(src))+' runtime='+repr(fake.calls),src])
text='\n'.join(out)+'\n';(R/'targeted-receipt.txt').write_text(text); print(text,end='')
