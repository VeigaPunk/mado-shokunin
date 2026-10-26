import os, subprocess, sys, shutil, time, json
S='/fast/scratch/hyaku/mado-r47/ScoutScriptMap'
F='/usr/bin/xdg-terminal-exec'
def case(name, files, args, env=None, stubs=('foo','bar'), timeout=5, dbg=False, wait=0.0):
    root=f'{S}/c_{name}'; shutil.rmtree(root, ignore_errors=True)
    for d in ('home/.config','home/.local/share/applications','bin','cache'): os.makedirs(f'{root}/{d}')
    for s in stubs:
        p=f'{root}/bin/{s}'; open(p,'w').write('#!/bin/sh\nexit 0\n'); os.chmod(p,0o755)
    for k,v in files.items():
        p=f'{root}/{k}'; os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'w').write(v)
    e={'HOME':f'{root}/home','PATH':f'{root}/bin:/usr/bin','XDG_CACHE_HOME':f'{root}/cache',
       'XDG_CONFIG_HOME':f'{root}/home/.config','XDG_CONFIG_DIRS':f'{root}/etc','XDG_DATA_HOME':f'{root}/home/.local/share',
       'XDG_DATA_DIRS':f'{root}/usr/share','XDG_CURRENT_DESKTOP':'Hypr'}
    if env:
        for k,v in env.items():
            if v is None: e.pop(k,None)
            else: e[k]=v.replace('$ROOT',root)
    if dbg: e['XTE_DEBUG']='1'
    try:
        r=subprocess.run([F]+args,env=e,capture_output=True,text=True,timeout=timeout)
        out=(r.returncode,r.stdout.replace(root,'$ROOT'),r.stderr.replace(root,'$ROOT'))
    except subprocess.TimeoutExpired: out=('TIMEOUT','','')
    time.sleep(wait)
    cache=os.listdir(f'{root}/cache')
    return out,cache,root
A='home/.local/share/applications/'
def desk(exec_,extra='',cat='TerminalEmulator;',end='\n'):
    return f'[Desktop Entry]\nType=Application\nName=T\nCategories={cat}\nExec={exec_}\n{extra}'.rstrip('\n')+end if False else f'[Desktop Entry]\nType=Application\nName=T\nCategories={cat}\n{extra}Exec={exec_}{end}'
P=['--print-id','--print-path','--print-cmd']
def show(n,*a,**k):
    o,c,r=case(n,*a,**k); print(f'--- {n}: rc={o[0]} cache={c}\n stdout={o[1]!r}\n stderr={o[2][:300]!r}')
    return r
