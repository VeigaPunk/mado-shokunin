exec(open('/fast/scratch/hyaku/mado-r47/ScoutScriptMap/probe.py').read())
import subprocess
show('test',{A+'t.desktop':desk('foo')},['--test','--print-cmd','--','x'])
show('testonly',{A+'t.desktop':desk('foo')},['--test','--dir=/q','--','x'])
show('hafter',{A+'t.desktop':desk('foo')},['--print-id','x','-h'])
show('hafterdd',{A+'t.desktop':desk('foo')},['--print-id','--','-h'])
show('eflag',{A+'t.desktop':desk('foo')},['--print-cmd','-e','x','--print-id'])
show('unk',{A+'t.desktop':desk('foo')},['--bogus','-','--print-id','--print-cmd','x'])
show('noargs_cmd',{A+'t.desktop':desk('foo')},['--print-cmd'])
show('multinl',{A+'t.desktop':desk('foo')},['--print-id','--title=a\nb','--print-cmd','x'])
show('dup',{A+'t.desktop':desk('foo')},['--print-id','--print-id','--print-path','--print-delimiter=;'])
show('delim_only_path',{A+'t.desktop':desk('foo')},['--print-path','--print-delimiter=\\n\\n'])
# readdir order vs find order
o,c,r=case('ord',{f'{A}{n}.desktop':desk('foo') for n in ['a','m','b','q','c']},['--print-id'])
d=f'{r}/home/.local/share/applications'
print('listdir',os.listdir(d)); print('scandir',[e.name for e in os.scandir(d)])
print('find',subprocess.run(['find','-L',d,'-type','f'],capture_output=True,text=True).stdout.split())
print(subprocess.run(['stat','-f','-c','%T',d],capture_output=True,text=True).stdout, subprocess.run(['stat','-f','-c','%T','/home/vgpnk/.local/share/applications'],capture_output=True,text=True).stdout)
print(o)
