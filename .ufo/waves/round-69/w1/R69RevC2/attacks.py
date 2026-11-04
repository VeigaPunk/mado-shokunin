#!/usr/bin/env python3
import ast, hashlib, json, pathlib, shutil, subprocess, sys
R=pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
S=pathlib.Path('/fast/scratch/hyaku/mado-r69/R69RevC2')
BASE='04093b83f73a841117d3b31dbb2a6063f4f2a454'
P=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else R/'.ufo/waves/round-69/proto/c2-classify.proto.py'
HEAD='import os, subprocess\nKEY = "GIT_NO_REPLACE_OBJECTS"\n'
CALL='subprocess.run(["git", "show", "HEAD:a"], env=env)\n'
cases={
'filtered-conditional': HEAD+'env = {k: v for k, v in os.environ.items() if k != "GIT_"}\nif enabled:\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'+CALL,
'attribute-env': HEAD+'self.env = {}\nself.env["GIT_NO_REPLACE_OBJECTS"] = "1"\nsubprocess.run(["git", "show", "HEAD:a"], env=self.env)\n',
'alias-env': HEAD+'env = {"GIT_NO_REPLACE_OBJECTS": "1"}\ne = env\nsubprocess.run(["git", "show", "HEAD:a"], env=e)\n',
'late-guard': HEAD+'env = {}\n'+CALL+'env["GIT_NO_REPLACE_OBJECTS"] = "1"\n',
'except-other-env': HEAD+'env = {}\ntry:\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\nexcept Exception:\n    env = {"PATH": "/usr/bin"}\n'+CALL,
'closure-env': HEAD+'def outer():\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n    def inner():\n        '+CALL+'    return inner()\n',
'splat-env': HEAD+'env = {**{"GIT_NO_REPLACE_OBJECTS": "1"}}\n'+CALL,
'cross-module': 'from producer import git_env\nimport subprocess\nenv = git_env()\n'+CALL,
'dead-inline': HEAD+'if False:\n    subprocess.run(["git", "show", "HEAD:a"], env={"GIT_NO_REPLACE_OBJECTS": "1"})\n',
'producer-overwrite': HEAD+'def git_env():\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n    env = {}\n    return env\nenv = git_env()\n'+CALL,
'producer-late': HEAD+'def git_env():\n    env = {}\n    return env\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\nenv = git_env()\n'+CALL,
'sibling-scope': HEAD+'def never():\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\ndef run():\n    '+CALL,
'nested-key-value': HEAD+'env = {"LABEL": {"GIT_NO_REPLACE_OBJECTS": "1"}}\n'+CALL,
'onehop-wrong-parameter': HEAD+'def launch(env, other_env):\n    subprocess.run(["git", "show", "HEAD:a"], env=other_env)\nenv = {"GIT_NO_REPLACE_OBJECTS": "1"}\nlaunch(env, {})\n',
'dead-else-valid': HEAD+'if False:\n    pass\nelse:\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'+CALL,
'producer-direct': HEAD+'def git_env():\n    return {"GIT_NO_REPLACE_OBJECTS": "1"}\nenv = git_env()\n'+CALL,
}
def git(*a):
    return subprocess.check_output(['git','-C',str(R),*a],text=True)
def load(src):
    ns={'__name__':'review_import'}; exec(compile(src,str(P),'exec'),ns); return ns
S.mkdir(parents=True,exist_ok=True)
try:
    source=P.read_text(); ns=load(source)
    print('COUNTER',str(P),'sha256='+hashlib.sha256(source.encode()).hexdigest())
    cpath=R/'.ufo/waves/round-69/controls/c2-controls-r69.json'
    data=cpath.read_bytes(); print('CONTROLS_SHA256',hashlib.sha256(data).hexdigest())
    controls=json.loads(data)['cases']
    oldsrc=git('show',BASE+':quality/counters/c2-r68-reader-guard.py')
    old=load(oldsrc)
    print('OLD_FUNCTIONS',sorted(k for k,v in old.items() if callable(v) and not k.startswith('__')))
    for name,src in cases.items():
        print('ATTACK',name,'verdict='+str(ns['classify'](src)))
        print('SOURCE_BEGIN\n'+src+'SOURCE_END')
    print('SECOND_MODULE producer.py\ndef git_env():\n    return {"GIT_NO_REPLACE_OBJECTS": "1"}')
    for c in controls:
        print('CONTROL',c['name'],'prototype='+str(ns['classify'](c['src'])),'r68='+str(old['classify'](c['src'])))
    paths=[p for p in git('ls-tree','-r','--name-only',BASE,'--','quality').splitlines() if __import__('re').match(r'^quality/check-[^/]+\.py$',p)]
    readers=guards=0
    for p in paths:
        src=git('show',BASE+':'+p); r,g=ns['classify'](src); readers+=r; guards+=g
        nohop=load(source); nohop['callee_passes_env_to_git']=lambda fn:False
        noprod=load(source); noprod['guard_producers']=lambda tree:set()
        print('FILE',p,'verdict='+str((r,g)),'without_onehop='+str(nohop['classify'](src)),'without_producer='+str(noprod['classify'](src)))
    print('TOTAL population=%s readers=%s guarded=%s unguarded=%s'%(len(paths),readers,guards,readers-guards))
finally:
    shutil.rmtree(S,ignore_errors=True)
    print('SCRATCH_REMOVED',not S.exists())
