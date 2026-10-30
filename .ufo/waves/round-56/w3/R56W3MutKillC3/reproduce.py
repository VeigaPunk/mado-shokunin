#!/usr/bin/env python3
"""Rebuild this receipt in an explicitly supplied empty seat scratch directory.
Example: python3 -I reproduce.py --scratch /fast/scratch/hyaku/mado-r56/R56W3MutKillC3
Creates no lane changes. Scratch is removed in finally. This entrypoint itself has not been exercised;
its component detector scripts were exercised, as recorded in receipts/kill-c3.txt.
"""
import argparse, io, os, shutil, subprocess, tarfile
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--scratch',required=True)
a=p.parse_args()
s=Path(a.scratch).resolve()
allowed=Path('/fast/scratch/hyaku/mado-r56/R56W3MutKillC3')
if s!=allowed or s.exists():
    raise SystemExit('Use the absent exact seat scratch directory: '+str(allowed))
lane=Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
here=Path(__file__).resolve().parent
rev='0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
def git(d,*args):
    return subprocess.run(['git','-C',str(d),*args],capture_output=True,check=True).stdout
try:
    shutil.copytree(here,s)
    (s/'work').mkdir(exist_ok=True)
    os.environ['TMPDIR']=str(s/'work')
    mini=s/'mini';mini.mkdir()
    blob=git(lane,'archive',rev,'--','corpus','.ufo/waves/round-56/frozen-tables-v2.json','.ufo/waves/round-56/c3-name-only.tsv','quality/counters/c3-r56-used-by.py')
    with tarfile.open(fileobj=io.BytesIO(blob)) as t:
        t.extractall(mini,filter='data')
    git(mini,'init','-q')
    assert Path(git(mini,'rev-parse','--show-toplevel').decode().strip()).resolve()==mini.resolve()
    git(mini,'add','-A','-f','.')
    git(mini,'-c','user.name=ctl','-c','user.email=ctl@ctl','commit','-q','--no-gpg-sign','-m','tip snapshot')
    (mini/'.git/objects/info/alternates').write_text(str(lane/'.git/objects')+'\n')
    (s/'mini_sha.txt').write_bytes(git(mini,'rev-parse','HEAD'))
    for name in ['sweep.py','kill_harness.py','check_equivalent.py','sweep_counter.py','kill_counter.py','restore_probe.py']:
        subprocess.run(['python3','-I',str(s/'suite'/name)],cwd=s,check=True)
    for name in ['sweep.json','kill_harness.json','equivalent.json','sweep_counter.json','kill_counter.json','restoration.json']:
        print(name,(s/name).read_text())
finally:
    if s.exists(): shutil.rmtree(s)
