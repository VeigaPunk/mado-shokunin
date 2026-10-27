import importlib.util, json, os, random, shutil, sys, tempfile, hashlib
sys.dont_write_bytecode = True
L="/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE=os.path.join(L,".ufo/waves/round-48/l1-draft")
spec=importlib.util.spec_from_file_location("c48", os.path.join(HERE,"c1-r48-terminal-cache.py"))
c48=importlib.util.module_from_spec(spec); spec.loader.exec_module(c48)
WORK=tempfile.mkdtemp(dir="/fast/scratch/hyaku/mado-r48/CritDataCompleteness", prefix="probe-")
box=c48.Box(WORK)
MT=c48.PINNED_MTIME
LIST="home/.config/hyprland-xdg-terminals.list"
APP="home/.local/share/applications/"
def env(desk="Hyprland", extra=None):
    e={"XDG_CONFIG_HOME":"$ROOT/home/.config","XDG_CONFIG_DIRS":"$ROOT/etc/xdg",
       "XDG_DATA_HOME":"$ROOT/home/.local/share","XDG_DATA_DIRS":"$ROOT/usr/share","XDG_CURRENT_DESKTOP":desk}
    if extra: e.update(extra)
    return e
def entry(cmd,extra=""):
    return "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=%s\n%s"%(cmd,extra)
FILES={LIST:"foot.desktop\n", APP+"foot.desktop":entry("foot --a","Actions=srv;\n[Desktop Action srv]\nExec=footclient\n")}

def measure(case, seed=0):
    rng=random.Random(seed)
    base,lang=c48.variant_roots(box,"A",rng)
    ro=os.path.join(base,"o","r")
    c48.prepare(box,ro,case,lang)
    warm,state=c48.oracle_side(box,case,ro,lang)
    shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return warm,state

R={}
# P1: default_cache with a real prime -> is it a HIT?
p1={"id":"P1-defaultcache-hit","class":"WARM-SAME","env":env(),"files":dict(FILES),"exec":["bin/foot","bin/footclient"],
    "args":["--print-cmd"],"mtime":MT,"default_cache":True,"prime":{"args":["--print-cmd"]},
    "expect":{"rc":-1,"stdout":""}}
try:
    (rc,out),st=measure(p1); R["P1-defaultcache-hit"]={"rc":rc,"stdout":out,"state":st}
except Exception as e: R["P1-defaultcache-hit"]={"error":str(e)}

# P2: default_cache DIFFERS (prime then edit entry same-size so cold differs)
p2={"id":"P2-defaultcache-differs","class":"WARM-DIFFERS","env":env(),"files":dict(FILES),"exec":["bin/foot","bin/footclient"],
    "args":["--print-cmd"],"mtime":MT,"default_cache":True,"prime":{"args":["--print-cmd"]},
    "after":{"files":{APP+"foot.desktop":entry("feot --a","Actions=srv;\n[Desktop Action srv]\nExec=footclient\n")},"mtime":MT},
    "expect":{"rc":-1,"stdout":""}}
try:
    (rc,out),st=measure(p2); R["P2-defaultcache-differs"]={"rc":rc,"stdout":out,"state":st}
except Exception as e: R["P2-defaultcache-differs"]={"error":str(e)}

# P3: cache file is a DIRECTORY (XDG_CACHE_HOME/xdg-terminal-exec as dir)
p3={"id":"P3-cache-is-dir","class":"WARM-ABSENT","env":env(),"files":dict(FILES),"exec":["bin/foot"],
    "args":["--print-cmd"],"mtime":MT,"cache":None,"expect":{"rc":-1,"stdout":""}}
# build manually: materialize, then replace cache file with a directory
def measure_p3():
    rng=random.Random(0); base,lang=c48.variant_roots(box,"A",rng); ro=os.path.join(base,"o","r")
    c48.materialize(ro,p3); c48.apply_mtime(ro,MT)
    cp=c48.cache_host(ro)
    if os.path.isfile(cp): os.unlink(cp)
    elif os.path.isdir(cp): shutil.rmtree(cp)
    os.makedirs(cp)  # cache path is now a directory
    warm,state=c48.oracle_side(box,p3,ro,lang)
    shutil.rmtree(base, ignore_errors=True); return warm,state
try:
    (rc,out),st=measure_p3(); R["P3-cache-is-dir"]={"rc":rc,"stdout":out,"state":st}
except Exception as e: R["P3-cache-is-dir"]={"error":str(e)}

# P4: XTE_CACHE_ENABLED="" (empty string) -> disabled?
p4={"id":"P4-cache-enabled-empty","class":"WARM-INVALID","env":env(),"files":dict(FILES),"exec":["bin/foot"],
    "args":["--print-cmd"],"mtime":MT,"cache":"0"*32+"\nfoot\n/x\nfoot.desktop\n\n\n\n\n\n\nfoot\x1eEND_OF_EXEC_USEP\n",
    "after":{"env":{"XTE_CACHE_ENABLED":""}},"expect":{"rc":-1,"stdout":""}}
try:
    (rc,out),st=measure(p4); R["P4-cache-enabled-empty"]={"rc":rc,"stdout":out,"state":st}
except Exception as e: R["P4-cache-enabled-empty"]={"error":str(e)}

# P5: env XTE_CACHE_ENABLED=yes (truthy, non-true/1 form) with primed cache -> hit?
p5={"id":"P5-cache-enabled-yes","class":"WARM-SAME","env":env(),"files":dict(FILES),"exec":["bin/foot"],
    "args":["--print-cmd"],"mtime":MT,"prime":{"args":["--print-cmd"]},"after":{"env":{"XTE_CACHE_ENABLED":"yes"}},
    "expect":{"rc":-1,"stdout":""}}
try:
    (rc,out),st=measure(p5); R["P5-cache-enabled-yes"]={"rc":rc,"stdout":out,"state":st}
except Exception as e: R["P5-cache-enabled-yes"]={"error":str(e)}

shutil.rmtree(WORK, ignore_errors=True)
print(json.dumps(R, indent=1))
