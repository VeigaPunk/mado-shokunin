import subprocess, sys, os, json
D="/fast/scratch/hyaku/mado-r56/R56W2RevAuditE/mut"
W="/fast/scratch/hyaku/mado-r56/R56W2RevAuditE/work"
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"
ENTRY="corpus/knowledge/hyprland-config-autoreload-r56.md"
os.makedirs(W, exist_ok=True)
def git(*a):
    return subprocess.run(["git","-C",D]+list(a),capture_output=True,text=True).stdout.strip()
def setline(text, old, new):
    assert text.count(old)==1, (old, text.count(old))
    return text.replace(old,new)
def mutate(fn):
    p=subprocess.run(["git","-C",D,"show","HEAD:"+ENTRY],capture_output=True,text=True).stdout
    new=fn(p)
    open(os.path.join(D,ENTRY),"w").write(new)
    git("add","-A")
    git("-c","user.name=ctl","-c","user.email=ctl@ctl","commit","-qm","mut")
    return git("rev-parse","HEAD")
def run(rev, tag):
    w=os.path.join(W,tag); os.makedirs(w,exist_ok=True)
    p=subprocess.run(["python3","-I",os.path.join(D,"quality/counters/c1-r56-autoreload-entry.py"),
                      "--repo",D,"--rev",rev,"--work",w],capture_output=True,text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()[:200]

base=git("rev-parse","HEAD")
print("BASELINE", base)
print(run(base,"base"))

MUTS={
 "M1_K25_wrong_envvar": lambda p: setline(p,
   "The static ENVHOME pointer takes its value from getenv of the HOME variable on this line.",
   "The static ENVHOME pointer takes its value from getenv of the PATH variable on this line."),
 "M2_K26_first_not_last": lambda p: setline(p,
   "currentDir is the currentPath text cut with substr at its last slash found by find_last_of on this line.",
   "currentDir is the currentPath text cut with substr at its FIRST slash found by find_last_of on this line."),
 "M3_K27_wrong_text": lambda p: setline(p,
   "The keyword dispatch guard tests whether COMMAND contains the misc:disable_autoreload text before it runs its body.",
   "The keyword dispatch guard tests whether COMMAND contains the monitor keyword text before it runs its body."),
 "M4_K28_wrong_object": lambda p: setline(p,
   "The reload request handler calls reload on the object returned by Config::mgr() on this line.",
   "The reload request handler calls reload on the object returned by Config::watcher() on this line."),
 "M5_K29_read_not_write": lambda p: setline(p,
   "The description text says a file opened for writing and then closed produces this event, the write-close case.",
   "The description text says a file opened for reading and then closed produces this event, the read-close case."),
 "M6_K30_regular_not_symlink": lambda p: setline(p,
   "The description says the pathname is not dereferenced when it is a symbolic link.",
   "The description says the pathname is not dereferenced when it is a regular file."),
 "M7_E01_quote_wrong_line": lambda p: setline(p,
   "| E01 | The replace call on this line swaps only the leading tilde for the HOME string, so a ~user prefix is not looked up and the user name stays glued to HOME. | S388 | Hyprland-MiscFunctions.cpp:66 | `value.replace(0, 1, std::string(ENVHOME));` |",
   "| E01 | The replace call on this line swaps only the leading tilde for the HOME string, so a ~user prefix is not looked up and the user name stays glued to HOME. | S388 | Hyprland-MiscFunctions.cpp:99 | `value.replace(0, 1, std::string(ENVHOME));` |"),
 "M8_E01_prop_false": lambda p: setline(p,
   "The replace call on this line swaps only the leading tilde for the HOME string, so a ~user prefix is not looked up and the user name stays glued to HOME.",
   "The replace call on this line swaps the whole leading path prefix for the USER name looked up in the password database, so a ~user prefix is expanded to that user home directory."),
}
for tag,fn in MUTS.items():
    rev=mutate(fn)
    rc,out,err=run(rev,tag)
    print(f"{tag} rc={rc} :: {out} {err}")
    git("reset","--hard",base)
