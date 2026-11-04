import argparse, pathlib, subprocess
REPO='/home/vgpnk/Projects/shokunin/mado-shokunin'
REV='cb713254ee9926e036e594312fdc61b57825526b'
SEAT=pathlib.Path(__file__).parent
SCRATCH='/fast/scratch/hyaku/mado-r76/R76RevC1/echo-drop'
def frozen(p):return subprocess.check_output(['git','-C',REPO,'show',REV+':'+p])
ns={'__name__':'review'}
exec(compile(frozen('quality/counters/c1-r76-outcome-field.py'),'frozen-counter','exec'),ns)
original_git=ns['git']
candidate=frozen(ns['CAND']).replace(b'return bool(r72_green(out)) and last_witness(out) == nonce',b'return bool(r72_green(out))')
# Inject ONLY candidate extraction bytes; frozen counter, cases, real fixture builders,
# subprocess pipeline, mutation recipes and scoring execute unchanged.
def git(repo,args,env):
    if args==['show',REV+':'+ns['CAND']]:
        return subprocess.CompletedProcess(args,0,candidate,b'')
    return original_git(repo,args,env)
ns['git']=git
args=argparse.Namespace(repo=REPO,rev=REV,base_rev='c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf',controls=REPO+'/.ufo/waves/round-76/controls/c1-outcome-cases-r76.json',scratch_root=SCRATCH)
print('ATTACK: green_with_witness returns r72_green only; candidate bytes injected at git extraction, not a committed revision')
rc=ns['measure'](args)
print('RC:',rc)
