# Spec-vs-script probes: runs /usr/bin/xdg-terminal-exec (sha256 89f2be9a...) with print modes only, cache in scratch.
import os,subprocess,sys,json,shutil,tempfile
SCR=sys.argv[1]
SCRIPT='/usr/bin/xdg-terminal-exec'
def desk(cats='Categories=TerminalEmulator',exe='fooexe',extra=''):
    return f"[Desktop Entry]\n{extra}Name=T\nExec={exe}\n{cats}\n"
def case(cid,files,args=('--print-id',),env=None,rel=False,note=''):
    root=tempfile.mkdtemp(dir=SCR,prefix=cid+'-')
    os.makedirs(root+'/bin');os.makedirs(root+'/home/.config');os.makedirs(root+'/cache')
    for ex in ('fooexe','barexe'):
        open(root+f'/bin/{ex}','w').write('#!/bin/sh\nexit 0\n');os.chmod(root+f'/bin/{ex}',0o755)
    for p,t in files.items():
        os.makedirs(os.path.dirname(root+'/'+p),exist_ok=True);open(root+'/'+p,'w').write(t)
    e={'XDG_CURRENT_DESKTOP':'Hyprland','XDG_CONFIG_HOME':root+'/home/.config','XDG_CONFIG_DIRS':root+'/etc/xdg',
       'XDG_DATA_HOME':root+'/home/.local/share','XDG_DATA_DIRS':root+'/usr/share','HOME':root+'/home',
       'PATH':root+'/bin:/usr/bin','XDG_CACHE_HOME':root+'/cache','LC_ALL':'C'}
    if env: 
        for k,v in env.items():
            if v is None: e.pop(k,None)
            else: e[k]=v.replace('$ROOT',root)
    r=subprocess.run([SCRIPT,*args],env=e,cwd=root,capture_output=True,text=True)
    out=(r.stdout+('|ERR:'+r.stderr if r.stderr else '')).replace(root,'$ROOT')
    return (cid,note,r.returncode,out.replace('\n','\\n'))
LST='home/.config/xdg-terminals.list'
A='usr/share/applications/foo.desktop'
rows=[]
rows.append(case('P01-baseline-no-type',{LST:'foo.desktop\n',A:desk()},note='entry without Type= key selected?'))
rows.append(case('P02-type-link',{LST:'foo.desktop\n',A:desk(extra='Type=Link\n')},note='Type=Link (spec: unknown type ignored)'))
rows.append(case('P03-type-bogus',{LST:'foo.desktop\n',A:desk(extra='Type=Bogus\n')},note='Type=Bogus'))
rows.append(case('P04-nodisplay-listed',{LST:'foo.desktop\n',A:desk(extra='NoDisplay=true\n')},note='NoDisplay=true, explicit list'))
rows.append(case('P05-nodisplay-fallback',{A:desk(extra='NoDisplay=true\n')},note='NoDisplay=true, fallback scan'))
rows.append(case('P06-hidden-TRUE',{LST:'foo.desktop\n',A:desk(extra='Hidden=TRUE\n')},note='Hidden=TRUE (spec boolean is lowercase only)'))
rows.append(case('P07-hidden-1',{LST:'foo.desktop\n',A:desk(extra='Hidden=1\n')},note='Hidden=1'))
rows.append(case('P08-hidden-true',{LST:'foo.desktop\n',A:desk(extra='Hidden=true\n')},note='Hidden=true control'))
rows.append(case('P09-subdir-id',{A.replace('foo','sub/foo'):desk()},note='fallback: applications/sub/foo.desktop ID'))
rows.append(case('P10-space-around-eq',{LST:'foo.desktop\n',A:'[Desktop Entry]\nName = T\nExec = fooexe\nCategories = TerminalEmulator\n'},note='spaces around = '))
rows.append(case('P11-relative-data-home',{ 'rel/applications/foo.desktop':desk()},env={'XDG_DATA_HOME':'rel','XDG_DATA_DIRS':'$ROOT/nodir'},note='relative XDG_DATA_HOME (basedir: ignore)'))
rows.append(case('P12-digit-first-id',{'usr/share/applications/1foo.desktop':desk()},note='ID starting with a digit'))
rows.append(case('P13-space-in-name',{'usr/share/applications/a b.desktop':desk()},note='space in file name'))
rows.append(case('P14-dot-leading',{'usr/share/applications/.foo.desktop':desk()},note='leading dot file'))
rows.append(case('P15-onlyshowin-miss-fallback',{A:desk(extra='OnlyShowIn=GNOME;\n')},note='OnlyShowIn=GNOME fallback'))
rows.append(case('P16-onlyshowin-miss-listed',{LST:'foo.desktop\n',A:desk(extra='OnlyShowIn=GNOME;\n')},note='OnlyShowIn=GNOME explicit list'))
rows.append(case('P17-cat-lowercase',{LST:'foo.desktop\n',A:desk(cats='Categories=terminalemulator;')},note='lowercase category'))
rows.append(case('P18-cat-list',{LST:'foo.desktop\n',A:desk(cats='Categories=System;TerminalEmulator;')},note='category in list'))
rows.append(case('P19-gap-before-group',{LST:'foo.desktop\n',A:'Name=T\nExec=fooexe\nCategories=TerminalEmulator\n[Desktop Entry]\n'},note='keys before [Desktop Entry]'))
rows.append(case('P20-data-home-outranks',{LST:'foo.desktop\n',A:desk(exe='barexe'),'home/.local/share/applications/foo.desktop':desk()},args=('--print-id','--print-path','--print-cmd'),note='data home beats data dirs'))
rows.append(case('P21-trailing-slash-dirs',{LST:'foo.desktop\n','usr/share/applications/foo.desktop':desk()},env={'XDG_DATA_DIRS':'$ROOT/usr/share//:$ROOT/zz/'},args=('--print-path',),note='doubled slash in data dir'))
with open('probes.tsv','w') as f:
    f.write('id\tnote\trc\tstdout(root->$ROOT; \\n escaped)\n')
    for r in rows: f.write('\t'.join(map(str,r))+'\n')
for r in rows: print(r)
