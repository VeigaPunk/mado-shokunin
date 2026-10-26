import importlib.util, os, tempfile, sys, shutil
L="/home/vgpnk/Projects/shokunin/mado-shokunin"
spec=importlib.util.spec_from_file_location("c", L+"/quality/counters/c1-r47-terminal.py"); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
w=tempfile.mkdtemp(dir="/fast/scratch/hyaku/mado-r47/l1"); box=c.Box(w, "/fast/scratch/hyaku/mado-r47/l1/data/repo/tools/mado-terminal.py")
T="[Desktop Entry]\nExec=%s\nCategories=System;TerminalEmulator;\n"
env={"XDG_CURRENT_DESKTOP":"Hyprland","XDG_CONFIG_HOME":"$ROOT/home/.config","XDG_CONFIG_DIRS":"$ROOT/etc/xdg","XDG_DATA_HOME":"$ROOT/home/.local/share","XDG_DATA_DIRS":"$ROOT/usr/share"}
cases=[("H1-dir-shadow",{"usr/share/applications/foot.desktop":T%"foot","home/.local/share/applications/foot.desktop/":""}),
("H1-dir-nested",{"usr/share/applications/foot.desktop":T%"foot","home/.local/share/applications/kitty.desktop/":"","home/.local/share/applications/kitty.desktop/x.desktop":T%"foot"})]
for x in ["-p","--","-v","-pV","-x","-","--foo"]:
    cases.append(("H2 Exec="+x,{"usr/share/applications/p.desktop":T%x}))
    cases.append(("H2 TryExec="+x,{"usr/share/applications/p.desktop":(T%"foot")+"TryExec=%s\n"%x}))
import random
rng=random.Random(1); bad=0
for name,files in cases:
    for args in (["--print-id","--print-path","--print-cmd"],["--test","x"]):
        ok,o,why=c.run_case(box,{"id":name,"env":env,"files":files,"exec":["bin/foot"],"args":args},"A",rng)
        if not ok: bad+=1; print("DIFF",name,args,why)
print("cases",len(cases)*2,"diff",bad,"trips",len(box.trips))
shutil.rmtree(w)
