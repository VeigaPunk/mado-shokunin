import copy, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, tempfile
ROOT=pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
OUT=ROOT/'.ufo/waves/round-67/w1/R67RevRegister'
S=pathlib.Path('/fast/scratch/hyaku/mado-r67/R67RevRegister')
REV='061dc329b598b2723a224b6c7b305b436946ec91'
BASE='0b28ffb4baac9586566d246c3f0986b2bb650a33'
C=ROOT/'.ufo/waves/round-67/controls/c1-controls.json'
DRAFT=pathlib.Path(sys.argv[1]).resolve()
sys.dont_write_bytecode=True
os.makedirs(S,exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0',LC_ALL='C',TMPDIR=str(S))
records=[]
def run(cmd):
    p=subprocess.run(list(map(str,cmd)),cwd=S,env=env,capture_output=True,text=True)
    records.append({'command':list(map(str,cmd)),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p
try:
    doc=json.loads(C.read_text()); g=doc['cases'][0]; live=doc['live_path']; fp=doc['file_path']
    spec=importlib.util.spec_from_file_location('candidate',DRAFT); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    frozen=[]
    for c in doc['cases']:
        reasons,summary,_=m.assess(c['province'],c['objects'].get)
        identity=json.dumps({'province':c['province'],'objects':c['objects']},sort_keys=True).encode()
        frozen.append(dict(name=c['name'],accepted=not reasons,expect=c['expect'],reasons=reasons,summary=summary,sha256=hashlib.sha256(identity).hexdigest()))
    cases=[]
    def add(name,text,objects=None): cases.append(dict(name=name,province=text,objects=copy.deepcopy(g['objects'] if objects is None else objects)))
    text=g['province']; filetext=text.replace(live,fp); lines=text.splitlines(True); row=lines[3]
    add('heading-only',filetext.replace('this host)', 'this host '+live+')',1))
    obj=copy.deepcopy(g['objects']);obj[live]='MADO_VERIFY: CLEAN (file plane)\n'
    add('twice-cited-missing-line',filetext.replace('`'+fp+'`','`'+live+'`',2),obj)
    add('probe-cell-only',filetext.replace('| probe | `'+fp+'` |','| `'+live+'` | `'+fp+'` |',1))
    add('receipt-trailing-punctuation',text.replace('`'+live+'`','`'+live+'`.,',1))
    add('nine-rows',text.replace('<!-- r65 register end -->','| extra plane | state | probe | `'+live+'` |\n<!-- r65 register end -->'))
    add('seven-rows',text.replace(row,''))
    missing='.ufo/waves/round-65/receipts/not-committed.txt'
    add('live-plus-unresolved-same-row',text.replace('`'+live+'`','`'+live+'` `'+missing+'`',1))
    add('duplicate-capitalization',text.replace('| waybar |','| HYPR PLANE |',1))
    add('sentinel-above-table',text.replace('<!-- r65 register end -->\n','').replace(lines[0],lines[0]+'<!-- r65 register end -->\n',1))
    add('forged-state-known-nonclaim',text.replace('unmeasured state','invented state'))
    results=[]
    for c in cases:
        reasons,summary,_=m.assess(c['province'],c['objects'].get)
        results.append(dict(name=c['name'],accepted=not reasons,reasons=reasons,summary=summary))
    (OUT/'forgeries.json').write_text(json.dumps(cases,indent=2)+'\n')
    for args in [['--selftest'],['--repo',ROOT,'--rev',REV,'--controls',C,'--scratch-root',S/'counter']]:
        run(['python3','-I',DRAFT,*args])
    run(['python3','-I',ROOT/'.ufo/waves/round-67/controls/score-baseline-c1.py','--repo',ROOT,'--base',BASE,'--controls',C,'--scratch-root',S/'baseline'])
    committed=run(['git','-C',ROOT,'show',REV+':'+live]).stdout.encode()
    wanted=doc['live_line'].encode()
    matching=[(i+1,x) for i,x in enumerate(committed.splitlines()) if x==wanted]
    linecheck={'object_sha256':hashlib.sha256(committed).hexdigest(),'literal_sha256':hashlib.sha256(wanted).hexdigest(),'literal_newline_sha256':hashlib.sha256(wanted+b'\n').hexdigest(),'matching_lines':[i for i,x in matching],'matching_line_sha256':[hashlib.sha256(x).hexdigest() for i,x in matching],'candidate_literal_equal':m.LIVE_LINE==doc['live_line']}
    fixture=pathlib.Path(tempfile.mkdtemp(prefix='fixture.',dir=S))
    assert run(['git','-C',fixture,'init','-q']).returncode==0
    assert run(['git','-C',fixture,'rev-parse','--show-toplevel']).stdout.strip()==str(fixture)
    assert run(['git','-C',fixture,'fetch','--quiet',ROOT,REV]).returncode==0
    fixtureargs=['python3','-I',DRAFT,'--repo',fixture,'--rev',REV,'--controls',C,'--scratch-root',S/'fixture-counter']
    clean=run(fixtureargs)
    (fixture/'PROVINCE.md').write_text('POISONED WORKTREE NO REGISTER\n')
    p=fixture/live;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('POISONED WORKTREE NO LIVE LINE\n')
    dirty=run(fixtureargs)
    worktree={'clean_rc':clean.returncode,'dirty_rc':dirty.returncode,'same_stdout':clean.stdout==dirty.stdout,'same_stderr':clean.stderr==dirty.stderr}
    result=dict(draft=str(DRAFT),draft_sha256=hashlib.sha256(DRAFT.read_bytes()).hexdigest(),frozen=frozen,pairwise_distinct=len({x['sha256'] for x in frozen})==6,forgeries=results,linecheck=linecheck,worktree=worktree,commands=records)
finally:
    shutil.rmtree(S)
    removed=not S.exists()
if 'result' in globals():
    result['scratch_removed']=removed
    (OUT/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
    for r in records:
        if r['command'][0]=='python3':print('COMMAND',r['command'],'RC',r['rc'],r['stdout'],r['stderr'])
