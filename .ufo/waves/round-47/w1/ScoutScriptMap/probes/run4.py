exec(open('/fast/scratch/hyaku/mado-r47/ScoutScriptMap/probe.py').read())
files={f'{A}app{n:05d}-padding-padding-padding.desktop':'[Desktop Entry]\nExec=nope\n' for n in range(1500)}
files[A+'zz.desktop']=desk('foo')
for tm in (None,'/nonexistent-tmp'):
    env={'TMPDIR':tm} if tm else None
    o,c,r=case('big'+str(bool(tm)),files,['--print-id'],env=env)
    print('TMPDIR=',tm,o[0],repr(o[1]),repr(o[2][:300]))
# strace-free check for tmpfile: small
