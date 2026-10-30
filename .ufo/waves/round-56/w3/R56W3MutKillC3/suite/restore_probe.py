#!/usr/bin/env python3
"""Run each proposed detector on pristine, mutated, and byte-restored copies. Preserve actual outputs and hashes."""
import sys, os, json, tempfile, shutil, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import kill_harness as KH
import harness_killers as HK
import kill_counter as KC
import counter_killers as CK
S=HERE.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for mid in HK.KILLERS:
    original=Path(KH.HARNESS_SRC).read_bytes()
    d=Path(tempfile.mkdtemp(prefix='restore-h.',dir=S/'work'))
    p=d/'r56_ctl_c3.py'
    results=[]
    try:
        for phase,data in [('pristine',original),('mutated',KH.mutant_source(mid)),('restored',original)]:
            p.write_bytes(data)
            shutil.rmtree(d/'__pycache__',ignore_errors=True)
            result=KH.apply_killer(mid,str(p),str(p))
            results.append(dict(phase=phase,sha256=sha(p.read_bytes()),passes=bool(result[0]),detail=result[1]))
        rows.append(dict(id=mid,target='harness',runs=results,verdict='KILLED' if results[0]['passes'] and not results[1]['passes'] and results[2]['passes'] else 'INCONCLUSIVE',restored_exact=p.read_bytes()==original))
    finally:
        p.write_bytes(original)
        shutil.rmtree(d)
for mid,spec in CK.FIXTURES.items():
    original=Path(KC.COUNTER_SRC).read_bytes()
    d=Path(tempfile.mkdtemp(prefix='restore-c.',dir=S/'work'))
    p=d/'counter.py'
    repo=None
    results=[]
    try:
        repo,rev,ctx=KC.build_fixture(mid)
        pred=spec['predicate'] or KC.population_predicate(mid)
        for phase,data in [('pristine',original),('mutated',KC.mutant_source(mid)),('restored',original)]:
            p.write_bytes(data)
            rc,out,err=KC.run_counter(str(p),repo,rev,str(d))
            ok,detail=pred(out,rc)
            results.append(dict(phase=phase,sha256=sha(p.read_bytes()),passes=bool(ok),rc=rc,stdout=out,stderr=err,detail=detail))
        rows.append(dict(id=mid,target='counter',fixture_context=ctx,runs=results,verdict='KILLED' if results[0]['passes'] and not results[1]['passes'] and results[2]['passes'] else 'INCONCLUSIVE',restored_exact=p.read_bytes()==original))
    finally:
        p.write_bytes(original)
        shutil.rmtree(d)
        if repo: shutil.rmtree(repo)
(S/'restoration.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:
    print(r['id'],r['verdict'],'pristine/mutant/restored='+str([x['passes'] for x in r['runs']]),'exact='+str(r['restored_exact']))
print('TOTAL',len(rows),'KILLED',sum(r['verdict']=='KILLED' for r in rows),'exact_restorations',sum(r['restored_exact'] for r in rows))
