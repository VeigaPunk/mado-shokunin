#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,sys
R=pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
P=R/'quality/counters/c2-r69-guard-dominance.py'
S=pathlib.Path('/fast/scratch/hyaku/mado-r69/R69RevC2')
ns={'__name__':'review_import'}
source=P.read_bytes();exec(compile(source,str(P),'exec'),ns)
S.mkdir(parents=True,exist_ok=True)
try:
    print('COUNTER',P,'sha256='+hashlib.sha256(source).hexdigest())
    raw=(R/'.ufo/waves/round-69/controls/c2-controls-r69.json').read_bytes()
    for label in ['truncated','renamed']:
        doc=json.loads(raw)
        if label=='truncated': doc['cases']=doc['cases'][:-1]
        else: doc['cases'][0]['name']='renamed-case'
        p=S/(label+'.json');p.write_text(json.dumps(doc))
        try: ns['load_controls'](p); print(label,'ACCEPTED')
        except ns['SetupError'] as exc: print(label,'REJECTED',str(exc))
    for label,counts in [('canonical',(20,13,13,0,11,7)),('base-controls-eleven',(20,13,13,0,11,11)),('population-nineteen',(19,13,13,0,11,7)),('controls-ten',(20,13,13,0,10,7))]:
        print(label,ns['verdict_met'](*counts),ns['contract_line'](*counts,'a'*40))
    for label,src in {
        'constant-key-subscript':'KEY="GIT_NO_REPLACE_OBJECTS"\nenv={}\nenv[KEY]="1"\nsubprocess.run(["git","show"],env=env)\n',
        'constant-key-splat':'KEY="GIT_NO_REPLACE_OBJECTS"\nenv={**{KEY:"1"}}\nsubprocess.run(["git","show"],env=env)\n',
        'constant-key-attribute':'KEY="GIT_NO_REPLACE_OBJECTS"\nself.env={}\nself.env[KEY]="1"\nsubprocess.run(["git","show"],env=self.env)\n',
    }.items():
        print('ATTACK',label,'verdict='+str(ns['classify'](src)));print('SOURCE_BEGIN\n'+src+'SOURCE_END')
finally:
    shutil.rmtree(S,ignore_errors=True)
    print('SCRATCH_REMOVED',not S.exists())
