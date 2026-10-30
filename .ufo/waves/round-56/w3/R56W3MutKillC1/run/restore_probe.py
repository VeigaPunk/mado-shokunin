import importlib.util,json,os,hashlib,shutil
R='/fast/scratch/hyaku/mado-r56/R56W3MutKillC1'
s=importlib.util.spec_from_file_location('driver',R+'/kill_c1.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
prior=json.load(open(R+'/kill-results.json')); rows=[]
for fx in m.FIXTURES:
 d,rev,good=m.build_fixture('restore-'+fx['ns']+'-'+fx['fixture'],fx['edit'])
 try:
  for mid in fx['mutants']:
   path=R+'/mutants/'+fx['ns']+'-'+fx['fixture']+'-'+mid+'.py'
   before=hashlib.sha256(open(path,'rb').read()).hexdigest()
   src=m.PRISTINE_SRC.encode();open(path,'wb').write(src)
   after=hashlib.sha256(open(path,'rb').read()).hexdigest()
   w=R+'/work/restored-'+fx['ns']+'-'+fx['fixture']+'-'+mid
   got=m.run_counter(path,d,rev,w)
   old=next(x for x in prior['results'] if x['ns']==fx['ns'] and x['fixture']==fx['fixture'])['pristine']
   norm=lambda x:x.split(' rows=',1)[-1]
   ok=got['rc']==old['rc'] and norm(got['out'])==norm(old['out'])
   rows.append(dict(fixture=fx['ns']+'-'+fx['fixture'],mutant=mid,mutated_sha256=before,restored_sha256=after,restored_matches_pristine_bytes=after==hashlib.sha256(src).hexdigest(),same_behavior=ok,restored_output=got))
 finally:shutil.rmtree(d)
p=R+'/mutants/B-F69-M69.py';before=hashlib.sha256(open(p,'rb').read()).hexdigest();open(p,'wb').write(m.PRISTINE_SRC.encode());tree=m.git(m.BASE,'rev-parse',m.BASE_REV+'^{tree}');got=m.run_counter(p,m.BASE,tree,R+'/work/restored-cli');rows.append(dict(fixture='B-F69',mutant='M69',mutated_sha256=before,restored_sha256=hashlib.sha256(open(p,'rb').read()).hexdigest(),same_behavior=got['rc']==2,restored_output=got))
json.dump(rows,open(R+'/receipts/restoration.json','w'),indent=1)
print('RESTORED',len(rows),'behavior_matches',sum(x['same_behavior'] for x in rows),'pristine_sha256',hashlib.sha256(m.PRISTINE_SRC.encode()).hexdigest())
