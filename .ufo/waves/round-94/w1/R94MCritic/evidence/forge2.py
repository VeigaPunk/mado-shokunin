import json, os, subprocess, sys
S='/fast/scratch/hyaku/mado-r94/R94MCritic'
GATE='/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-selftest-strength.py'
TOOL=os.path.join(S,'tools','mado-xdgmime.py')

X1=('        if mime in (b"--help", b"--manual"):','        return None, 0\n        if mime in (b"--help", b"--manual"):')
X2=('        out = self.defapp_generic(mime)','        return b"a.desktop", 0')
SPEC=('        out = self.defapp_generic(mime)','        return b"c.desktop", 0')

def mk(edits, tag, extra=()):
    src=open(TOOL,encoding='utf-8').read()
    for find,rep in extra:
        assert src.count(find)==1,(tag,src.count(find))
        src=src.replace(find,rep,1)
    for find,rep in edits:
        pre=src[:src.find('def selftest(')]
        assert pre.count(find)==1,(tag,pre.count(find))
        src=src.replace(find,rep,1)
    p=os.path.join(S,'m-'+tag+'.py'); open(p,'w',encoding='utf-8').write(src); return p

def selftest_fails(p, tag):
    d=os.path.join(S,'st-'+tag); os.makedirs(d,exist_ok=True)
    env=dict(os.environ); env['TMPDIR']=d
    r=subprocess.run([sys.executable,'-I',os.path.abspath(p),'--selftest'],capture_output=True,env=env,cwd=d)
    out=r.stdout.decode('utf-8','replace').splitlines()
    return r.returncode,[l.split(': ',1)[1] for l in out if '_SELFTEST_FAIL: ' in l]

def gate(tool, kills, tag):
    ks=os.path.join(S,'ks-%s.json'%tag)
    json.dump(kills, open(ks,'w'), indent=1)
    r=subprocess.run([sys.executable,'-I',GATE,'--tool',tool,'--kills',ks,'--scratch-root',os.path.join(S,'gate-'+tag)],
                     capture_output=True)
    return r.returncode, r.stdout.decode().strip().splitlines()[-1]

f1=mk([X1],'x1'); rc1,fails1=selftest_fails(f1,'x1')
f2=mk([X2],'x2'); rc2,fails2=selftest_fails(f2,'x2')
print('X1 fails(%d):'%len(fails1), fails1)
print('X2 fails(%d):'%len(fails2), fails2)
forged={'tool':'tools/mado-xdgmime.py','tool_sha256':'','selftest_argv':['--selftest'],
        'fail_line_prefix':'MADO_XDGMIME_SELFTEST_FAIL: ','result_line_prefix':'MADO_XDGMIME_SELFTEST: ',
        'selftest_checks':12,
        'kills':[{'id':'k-x1','find':X1[0],'replace':X1[1],'must_fail':fails1},
                 {'id':'k-x2','find':X2[0],'replace':X2[1],'must_fail':fails2}]}
print('gate on unmodified tool with 2 universal kills:', gate(TOOL,forged,'base'))
neutral_line='    failed = [n for n, ok in checks if not ok]'
labels=sorted(set(fails1)|set(fails2))
assert len(labels)==12 and len(set(labels))==12, labels
count=0; details=[]
for L in labels:
    newline='    failed = [n for n, ok in checks if not ok and n != %s]'%json.dumps(L)
    p=mk([], 'n-'+str(count), extra=[(neutral_line,newline)])
    rc,line=gate(p,forged,'n%d'%count)
    ok = (rc==1 and 'WEAK' in line)
    count += ok
    details.append((L,rc,ok))
print('neutralised_flagged with 2 universal kills:', count, '/ 12')
# loosening: m03 expectation accepts a second wrong app
LOOSEN=('q("text/plain") == ("a.desktop", 0)','q("text/plain") in (("a.desktop", 0), ("c.desktop", 0))')
p=mk([], 'loose', extra=[LOOSEN])
rc,line=gate(p,forged,'loose')
print('loosened m03 under universal kill-set:', rc, line)
# same loosening under a kill naming m03 only
specific={'tool':'tools/mado-xdgmime.py','tool_sha256':'','selftest_argv':['--selftest'],
 'fail_line_prefix':'MADO_XDGMIME_SELFTEST_FAIL: ','result_line_prefix':'MADO_XDGMIME_SELFTEST: ',
 'selftest_checks':12,
 'kills':[{'id':'k-spec','find':SPEC[0],'replace':SPEC[1],'must_fail':['m03 list: second id installed']}]}
print('same loosened tool under a m03-specific kill:', gate(p,specific,'spec'))
json.dump({'x1':fails1,'x2':fails2}, open(os.path.join(S,'forge2.json'),'w'), indent=1)
