import importlib.util,sys,json,subprocess
sys.argv=['x']
spec=importlib.util.spec_from_file_location("c2","quality/counters/c2-r89-survivor-kills.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
F,K=m.F,m.K
tool=open(sys.stdin.readline().strip() if False else 'tools/mado-mako.py').read()
fb=[c for c in F.load_cases(open('.ufo/waves/round-88/controls/mako-cases-r88.json','rb').read()) if c['id'] not in m.EXCLUDED_B]
kb=K.load_cases(open('.ufo/waves/round-88/controls/containment-cases-r88.json','rb').read())
fs=F.load_cases(open('.ufo/waves/round-89/controls/survivor-cases-c1side-r89.json','rb').read())
ks=K.load_cases(open('.ufo/waves/round-89/controls/survivor-cases-c2side-r89.json','rb').read())
surv=F.load_mutants(open('.ufo/waves/round-89/controls/survivor-mutants-r89.json','rb').read())
mode=__import__('os').environ.get('MODE','draft')
if mode=='control':
    r=m.evaluate(tool,fb,kb,[],[],surv,'/fast/scratch/hyaku/mado-r89/L1')
else:
    r=m.evaluate(tool,fb,kb,fs,ks,surv,'/fast/scratch/hyaku/mado-r89/L1')
print([l for l in r['lines'] if 'FAIL' in l])
for row in r['rows']: print(row['id'],row['status'],row['killed_by_b'],row['differs_on'],row['crashed_on'][:3])
print({k:v for k,v in r.items() if k not in('rows','lines')})
