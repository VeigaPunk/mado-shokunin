#!/bin/bash
# R94MCritic evidence reproduction (read-only against the lane; writes only under $S).
# Usage: bash repro.sh   (prints every command's output; exit 0 when all sections ran)
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
TOOL=$LANE/.ufo/waves/round-94/build/mado-mimeglob.c1.py
ORACLE_SRC=$LANE/.ufo/waves/round-94/controls/mimeglob-oracle-r94.c
GATE=$LANE/quality/check-selftest-strength.py
HERE=$(cd "$(dirname "$0")" && pwd)
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r94/critic-repro
rm -rf "$S"; mkdir -p "$S"; cd "$S" || exit 1
set -x
gcc -O1 -o oracle "$ORACLE_SRC" $(pkg-config --cflags --libs gio-2.0); echo "gcc rc=$?"
sha256sum oracle "$TOOL" "$ORACLE_SRC"
set +x
PY=$(command -v python3)

echo "===== A. text mode: candidate vs oracle (12 names, one >254-byte globs2 line present)"
mkdir -p fx/dh/mime fx/h
"$PY" - <<'EOP'
line = "50:text/x-lf:*.lf:" + "x"*240 + ",cs\n"
base = ("50:text/plain:*.txt\n50:text/x-c:*.c:cs\n50:text/x-c++:*.C:cs\n"
        "50:app/x-gz:*.gz\n60:app/x-tgz:*.tar.gz\n60:app/hi:*.dup\n40:app/lo:*.dup\n"
        "50:text/x-make:Makefile\n50:app/full:x?y\n50:t/one:*.two\n50:t/other:*.two\n")
open("fx/dh/mime/globs2","w").write(base+line)
open("fx/dh/mime/globs","w").write("text/v1:*.one\n")
EOP
N=(a.txt A.TXT x.C x.tar.gz x.dup Makefile MAKEFILE xzy zz dir/ D.TXT x.one)
env -i LC_ALL=C HOME=$S/fx/h XDG_DATA_HOME=$S/fx/dh XDG_DATA_DIRS= ./oracle "${N[@]}"
"$PY" -I "$TOOL" --data-home "$S/fx/dh" --data-dirs '' --home "$S/fx/h" "${N[@]}"

echo "===== B. cache mode + mixed mode (update-mime-database on a scratch dir)"
mkdir -p fx2/mime/packages fx2/mime-globs/mime fx2/h
cat > fx2/mime/packages/p.xml <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
 <mime-type type="text/x-c1">
  <glob pattern="*.c1"/><glob pattern="*.C1" case-sensitive="true"/>
  <glob pattern="*.tar.c1"/><glob pattern="Makefile.c1"/>
 </mime-type>
 <mime-type type="text/x-c2"><glob pattern="*.c2" weight="60"/></mime-type>
</mime-info>
XML
update-mime-database "$S/fx2/mime"; echo "update-mime-database rc=$?"
printf '50:text/x-globsonly:*.gon\n' > fx2/mime-globs/mime/globs2
N2=(a.c1 A.C1 a.c2 x.tar.c1 Makefile.c1 MAKEFFILE.c1 a.gon)
env -i LC_ALL=C HOME=$S/fx2/h XDG_DATA_HOME=$S/fx2 XDG_DATA_DIRS= ./oracle "${N2[@]}"
"$PY" -I "$TOOL" --json --data-home "$S/fx2" --data-dirs '' --home "$S/fx2/h" "${N2[@]}"
echo "-- mixed: a cache dir plus a globs2-only dir (globs2-only must be ignored)"
env -i LC_ALL=C HOME=$S/fx2/h XDG_DATA_HOME=$S/fx2 XDG_DATA_DIRS=$S/fx2/mime-globs ./oracle a.c1 a.gon
"$PY" -I "$TOOL" --json --data-home "$S/fx2" --data-dirs "$S/fx2/mime-globs" --home "$S/fx2/h" a.c1 a.gon

echo "===== C. fgets class discriminator: the >254-byte line makes one glob case-sensitive only when chunked"
mkdir -p fx3/dh/mime fx3/h
"$PY" - <<'EOP'
open("fx3/dh/mime/globs2","w").write("50:text/x-lf:*.lf:" + "x"*240 + ",cs\n")
src = open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-94/build/mado-mimeglob.c1.py", encoding="utf-8").read()
find = '        nl = data.find(b"\\n", i, i + 254)'
assert src.count(find) == 1
open("fg-mut.py","w",encoding="utf-8").write(src.replace(find, '        nl = data.find(b"\\n", i)', 1))
EOP
env -i LC_ALL=C HOME=$S/fx3/h XDG_DATA_HOME=$S/fx3/dh XDG_DATA_DIRS= ./oracle A.LF a.lf
"$PY" -I "$TOOL" --data-home "$S/fx3/dh" --data-dirs '' --home "$S/fx3/h" A.LF a.lf
"$PY" -I "$S/fg-mut.py" --data-home "$S/fx3/dh" --data-dirs '' --home "$S/fx3/h" A.LF a.lf
echo "-- the two naive extension maps on the same case (folded is RIGHT, exact is WRONG: the control's strength is not pinned)"
"$PY" "$HERE/naive.py" exact "$S/fx3/dh" A.LF
"$PY" "$HERE/naive.py" folded "$S/fx3/dh" A.LF
echo "-- and on the fx fixture the two variants differ: exact vs folded against the oracle labels printed in section A"
"$PY" "$HERE/naive.py" exact "$S/fx/dh" a.txt A.TXT x.C x.tar.gz x.dup Makefile MAKEFILE xzy zz dir/ D.TXT x.one
"$PY" "$HERE/naive.py" folded "$S/fx/dh" a.txt A.TXT x.C x.tar.gz x.dup Makefile MAKEFILE xzy zz dir/ D.TXT x.one

echo "-- naive variant correctness against the oracle on the fx fixture (same 12 names as section A)"
"$PY" - "$S" "$HERE" <<'EOP'
import subprocess, sys
S, HERE = sys.argv[1], sys.argv[2]
names=['a.txt','A.TXT','x.C','x.tar.gz','x.dup','Makefile','MAKEFILE','xzy','zz','dir/','D.TXT','x.one']
env={'LC_ALL':'C','HOME':S+'/fx/h','XDG_DATA_HOME':S+'/fx/dh','XDG_DATA_DIRS':''}
oracle=subprocess.run([S+'/oracle',*names],capture_output=True,env=env).stdout.decode().splitlines()
for mode in ('exact','folded'):
    out=subprocess.run([sys.executable, HERE+'/naive.py', mode, S+'/fx/dh', *names],capture_output=True).stdout.decode().splitlines()
    ok=sum(1 for a,b in zip(oracle,out) if a=='%s\t%s'%tuple(b.split('\t')[1:3]))
    print('naive-%s: %d of %d names equal to the oracle'%(mode,ok,len(names)))
EOP

echo "===== D. oracle-exec wrapper: behaviourally identical to the oracle on every layout, including fresh random ones"
cp "$HERE/wrapper-tool.py" "$S/wrapper-tool.py"; "$PY" - "$S" <<'EOP'
import json, os, random, subprocess, sys
S=sys.argv[1]
def run(cmd, env): return subprocess.run(cmd, capture_output=True, env=env)
# text fixture
names=['a.txt','A.TXT','x.C','x.tar.gz','x.dup','Makefile','MAKEFILE','xzy','zz','dir/','D.TXT','x.one']
env={'LC_ALL':'C','HOME':S+'/fx/h','XDG_DATA_HOME':S+'/fx/dh','XDG_DATA_DIRS':''}
o=run([S+'/oracle',*names],env).stdout.decode().splitlines()
w=json.loads(run([sys.executable,'-I',S+'/wrapper-tool.py','--json','--data-home',S+'/fx/dh','--data-dirs','','--home',S+'/fx/h',*names],env).stdout)['results']
print('wrapper text fixture: mismatches %d of %d'%(sum(a!='%s\t%d'%(b['type'],b['uncertain']) for a,b in zip(o,w)), len(o)))
# cache/mixed fixture (built in section B)
names2=['a.c1','A.C1','a.c2','x.tar.c1','Makefile.c1','MAKEFFILE.c1','a.gon','zz','dir/']
e2={'LC_ALL':'C','HOME':S+'/fx2/h','XDG_DATA_HOME':S+'/fx2','XDG_DATA_DIRS':S+'/fx2/mime-globs'}
o2=run([S+'/oracle',*names2],e2).stdout.decode().splitlines()
w2=json.loads(run([sys.executable,'-I',S+'/wrapper-tool.py','--json','--data-home',S+'/fx2','--data-dirs',S+'/fx2/mime-globs','--home',S+'/fx2/h',*names2],e2).stdout)['results']
print('wrapper cache/mixed fixture: mismatches %d of %d'%(sum(a!='%s\t%d'%(b['type'],b['uncertain']) for a,b in zip(o2,w2)), len(o2)))
# 20 fresh random layouts
rnd=random.Random(1234); total=bad=0
for i in range(20):
    root=os.path.join(S,'fresh','L%02d'%i); os.makedirs(root+'/mime',exist_ok=True)
    exts=[]; lines=[]
    for j in range(6):
        ext=''.join(rnd.choice('abcdefgh') for _ in range(rnd.randint(1,4))); exts.append(ext)
        lines.append('%d:app/x-%d:*.%s%s'%(rnd.choice([10,40,50,60,80]),j,ext,':cs' if rnd.random()<0.3 else ''))
    open(root+'/mime/globs2','w').write('\n'.join(lines)+'\n')
    nm=[''.join(rnd.choice('abcXY.') for _ in range(rnd.randint(1,6)))+'.'+rnd.choice(exts) for _ in range(15)]
    e={'LC_ALL':'C','HOME':root+'/h','XDG_DATA_HOME':root,'XDG_DATA_DIRS':''}
    oo=run([S+'/oracle',*nm],e).stdout.decode().splitlines()
    ww=json.loads(run([sys.executable,'-I',S+'/wrapper-tool.py','--json','--data-home',root,'--data-dirs','','--home',root+'/h',*nm],e).stdout)['results']
    for a,b in zip(oo,ww):
        total+=1; bad += a!='%s\t%d'%(b['type'],b['uncertain'])
print('wrapper fresh random layouts: mismatches %d of %d'%(bad,total))
EOP

echo "===== E. C2: a 2-kill universal kill-set passes the gate and flags every single-check neutralisation"
cp "$LANE/tools/mado-xdgmime.py" tool.py
"$PY" - <<'EOP'
import json, os, subprocess, sys
S=os.getcwd(); GATE=os.environ['GATE']; TOOL=os.path.abspath('tool.py')
X1=('        if mime in (b"--help", b"--manual"):','        return None, 0\n        if mime in (b"--help", b"--manual"):')
X2=('        out = self.defapp_generic(mime)','        return b"a.desktop", 0')
SPEC=('        out = self.defapp_generic(mime)','        return b"c.desktop", 0')
def mk(edits, tag, extra=()):
    src=open(TOOL,encoding='utf-8').read()
    for f,r in extra:
        assert src.count(f)==1; src=src.replace(f,r,1)
    for f,r in edits:
        pre=src[:src.find('def selftest(')]; assert pre.count(f)==1; src=src.replace(f,r,1)
    p=os.path.join(S,'m-'+tag+'.py'); open(p,'w',encoding='utf-8').write(src); return p
def fails(p,tag):
    d=os.path.join(S,'st-'+tag); os.makedirs(d,exist_ok=True)
    env=dict(os.environ); env['TMPDIR']=d
    r=subprocess.run([sys.executable,'-I',p,'--selftest'],capture_output=True,env=env,cwd=d)
    return [l.split(': ',1)[1] for l in r.stdout.decode().splitlines() if '_SELFTEST_FAIL: ' in l]
def gate(tool,kills,tag):
    ks=os.path.join(S,'ks-%s.json'%tag); json.dump(kills,open(ks,'w'),indent=1)
    r=subprocess.run([sys.executable,'-I',GATE,'--tool',tool,'--kills',ks,'--scratch-root',os.path.join(S,'gate-'+tag)],capture_output=True)
    return r.returncode, r.stdout.decode().strip().splitlines()[-1]
f1=fails(mk([X1],'x1'),'x1'); f2=fails(mk([X2],'x2'),'x2')
print('X1 FAIL set (%d): %s'%(len(f1),f1)); print('X2 FAIL set (%d): %s'%(len(f2),f2))
forged={'tool':'tools/mado-xdgmime.py','tool_sha256':'','selftest_argv':['--selftest'],
        'fail_line_prefix':'MADO_XDGMIME_SELFTEST_FAIL: ','result_line_prefix':'MADO_XDGMIME_SELFTEST: ',
        'selftest_checks':12,
        'kills':[{'id':'k-x1','find':X1[0],'replace':X1[1],'must_fail':f1},
                 {'id':'k-x2','find':X2[0],'replace':X2[1],'must_fail':f2}]}
print('gate on the unmodified tool with 2 universal kills:', gate(TOOL,forged,'base'))
labels=sorted(set(f1)|set(f2)); print('union of the two FAIL sets = %d labels'%len(labels))
line='    failed = [n for n, ok in checks if not ok]'; n=0
for L in labels:
    p=mk([], 'n', extra=[(line,'    failed = [n for n, ok in checks if not ok and n != %s]'%json.dumps(L))])
    rc,out=gate(p,forged,'n'); n += (rc==1 and 'WEAK' in out)
print('neutralised_flagged with those 2 kills: %d / %d'%(n,len(labels)))
LOOSEN=('q("text/plain") == ("a.desktop", 0)','q("text/plain") in (("a.desktop", 0), ("c.desktop", 0))')
p=mk([], 'loose', extra=[LOOSEN])
print('a real LOOSENING of check m03 under the 2 universal kills:', gate(p,forged,'loose'))
specific={'tool':'tools/mado-xdgmime.py','tool_sha256':'','selftest_argv':['--selftest'],
 'fail_line_prefix':'MADO_XDGMIME_SELFTEST_FAIL: ','result_line_prefix':'MADO_XDGMIME_SELFTEST: ',
 'selftest_checks':12,'kills':[{'id':'k-spec','find':SPEC[0],'replace':SPEC[1],
 'must_fail':['m03 list: second id installed']}]}
print('the same loosened tool under a m03-specific kill:', gate(p,specific,'spec'))
EOP

echo "===== F. do-nothing instrument is blind to a neutralised check (result line unchanged)"
GATE=$GATE "$PY" - <<'EOP'
import os, subprocess, sys
src=open('tool.py',encoding='utf-8').read()
line='    failed = [n for n, ok in checks if not ok]'
open('n-ev.py','w',encoding='utf-8').write(src.replace(line, line.replace('if not ok]','if not ok and n != "m05 desktop-specific file first"]'),1))
d=os.path.join(os.getcwd(),'st-ev'); os.makedirs(d,exist_ok=True)
env=dict(os.environ); env['TMPDIR']=d
out=subprocess.run([sys.executable,'-I','n-ev.py','--selftest'],capture_output=True,env=env).stdout.decode()
print('neutralised result line:', [l for l in out.splitlines() if l.startswith('MADO_XDGMIME_SELFTEST: ')])
print('FAIL lines seen by a result-line watcher:', [l for l in out.splitlines() if 'FAIL' in l])
EOP

echo "===== G. base: the C1 tool does not exist at a3de9972"
git -C "$LANE" show a3de997289014e7dbf1d73ae206be1d6f8cdadd0:tools/mado-mimeglob.py > /dev/null; echo "git show rc=$?"
ls "$LANE"/quality/selftest-kills/
echo "all sections ran"
