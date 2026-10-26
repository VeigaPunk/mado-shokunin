import importlib.util, os, subprocess, sys, shutil, random
spec = importlib.util.spec_from_file_location("mt", sys.argv[1]); mt = importlib.util.module_from_spec(spec); spec.loader.exec_module(mt)
N = int(sys.argv[2]); seed = int(sys.argv[3])
SCR = "/fast/scratch/hyaku/mado-r47/l1/fuzzw"; shutil.rmtree(SCR, ignore_errors=True); os.makedirs(SCR)
tb = SCR + "/toolbin"; os.makedirs(tb)
for c in ["tr", "find", "awk", "ls", "md5sum", "mkdir", "rm", "sh", "bash", "cat"]:
    os.symlink(shutil.which(c), tb + "/" + c)
R = random.Random(seed)
NAMES = ["foot", "kitty", "alacritty", "ghostty", "xterm", "wezterm"]
DIRS = ["usr/share/applications/", "home/.local/share/applications/", "opt/share/applications/"]
KEYS = ["Type=Application", "Categories=TerminalEmulator;", "Categories=System;TerminalEmulator", "Categories=System;",
        "Categories=", "CategoriesX=TerminalEmulator;", "Hidden=true", "Hidden=false", "Hidden= true", "NoDisplay=true",
        "TryExec={n}", "TryExec=missing", "TryExec=printf", "TryExec=/bin/sh", "OnlyShowIn=GNOME;", "OnlyShowIn=Hyprland;",
        "NotShowIn=Hyprland;", "NotShowIn=KDE;", "X-TerminalArgExec=-x", "TerminalArgExec=", "X-ExecArg=--", "ExecArg=-e",
        "X-TerminalArgDir=--working-directory=", "TerminalArgDir=-D", "X-TerminalArgTitle=--title", "TerminalArgTitle=-T=",
        "X-TerminalArgAppId=--class=", "X-TerminalArgHold=--hold", "Actions=new;srv;", "Actions=other;",
        "Exec={n}", "Exec={n} --a %U", "Exec=\"{n}\" \"b c\" 100%%", "Exec={n} %f %u", "Exec={n} $HOME", "Exec={n} 'q'",
        "Exec={n}\\s-x", "Exec=  {n}   -a  ", "Exec={n} %k", "Exec=", "Exec=%U", "Exec={n} \"a\\\\\"b\"", "Exec=env {n}",
        "Exec={n} \"\" x", "Exec={n} %", "Exec={n} a%%b %c", "# comment", "", "  Exec = {n}", "Exec ={n}", "Name=X"]
GROUPS = ["[Desktop Action new]", "[Desktop Action srv]", "[Other]", "[Desktop Entry] x", "[Desktop Action ]"]
LISTL = ["{id}", "{id}:new", "{id}:srv", "{id}:", "-{id}", "+{id}", "{id}:bad:", "{n}", "# c", "", "  {id}  ", "/execarg_strict",
         "/execarg_compat", "/execarg_default:{id}:-z", "/execarg_default:{id}:a:b:", "/enable_cache", "{id}\r", "x/{id}", "{id}:a_b"]


def entry(n):
    lines = []
    if R.random() < 0.15:
        lines.append(R.choice(["# lead", "Exec=" + n]))
    lines.append("[Desktop Entry]" if R.random() < 0.95 else "[Desktop Entry]x")
    if R.random() < 0.85:
        lines.append("Categories=TerminalEmulator;")
    if R.random() < 0.8:
        lines.append("Exec=" + n)
    for _ in range(R.randint(0, 4)):
        k = R.choice(KEYS).replace("{n}", n)
        lines.append(k)
        if R.random() < 0.1:
            lines.append(R.choice(GROUPS))
    if R.random() < 0.4:
        lines.append(R.choice(GROUPS))
        lines.append("Exec=" + n + "client")
    text = "\n".join(lines)
    if R.random() < 0.9:
        text += "\n"
    return text


def gen(i):
    files, execs = {}, []
    ids = []
    for _ in range(R.randint(0, 5)):
        n = R.choice(NAMES)
        d = R.choice(DIRS)
        sub = R.choice(["", "", "", "vendor/"])
        rel = d + sub + n + ".desktop"
        files[rel] = entry(n)
        ids.append((sub.replace("/", "-")) + n + ".desktop")
    for n in NAMES:
        if R.random() < 0.5:
            execs.append("bin/" + n)
        if R.random() < 0.2:
            execs.append("bin/" + n + "client")
    lists = ["home/.config/xdg-terminals.list", "home/.config/hyprland-xdg-terminals.list", "etc/xdg/xdg-terminals.list",
             "usr/share/xdg-terminal-exec/xdg-terminals.list", "home/.config/gnome-xdg-terminals.list"]
    for lp in lists:
        if R.random() < 0.35 and ids:
            ls = [R.choice(LISTL).replace("{id}", R.choice(ids)).replace("{n}", R.choice(NAMES)) for _ in range(R.randint(1, 4))]
            files[lp] = "\n".join(ls) + ("\n" if R.random() < 0.9 else "")
    desk = R.choice(["Hyprland", "hyprland", "GNOME:Hyprland", "Hyprland:GNOME", "", None, "KDE"])
    args = R.choice([["--print-id"], ["--print-path"], ["--print-id", "--print-path", "--print-cmd"], ["--print-cmd", "--", "htop", "-d 5"],
                     ["--print-cmd", "--dir=/srv", "--title=t x", "--app-id=a", "--hold", "top"], ["--test", "-e", "ls"],
                     ["--print-cmd=\\t", "x"], ["--print-id", "--print-delimiter=|", "--print-cmd"], ["--print-content"],
                     ["--print-path", "--print-content", "--print-cmd"], ["--print-cmd", "-x", "y"], ["--print-cmd", "--unknown", "z"]])
    env = {}
    return files, execs, desk, args


def materialize(root, files, execs):
    for rel, text in files.items():
        p = os.path.join(root, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="latin-1").write(text)
    for rel in execs:
        p = os.path.join(root, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write("#!/bin/sh\nexit 1\n"); os.chmod(p, 0o755)


bad = 0
stats={}
outs=set()
for i in range(N):
    files, execs, desk, args = gen(i)
    root = SCR + "/c%04d" % i
    os.makedirs(root + "/home"); os.makedirs(root + "/cache")
    materialize(root, files, execs)
    env = mt._env(root, desk)
    env["PATH"] = env["PATH"] + ":" + tb
    try:
        mine = mt.run_print(env, args, cwd=root)[:2]
    except mt.OutOfContract as ex:
        mine = ("OOC " + str(ex), 2)
    p = subprocess.run(["/bin/sh", "/usr/bin/xdg-terminal-exec"] + args, env=env, cwd=root, capture_output=True, timeout=20)
    theirs = (p.stdout.decode("latin-1"), p.returncode)
    stats[theirs[1]]=stats.get(theirs[1],0)+1
    outs.add(theirs[0][:40])
    if mine != theirs:
        bad += 1
        if bad <= 6:
            print("DIFF case", i, args, desk, "\n mine=", mine, "\n theirs=", theirs)
            for k, v in files.items():
                print("   ", k, repr(v))
    else:
        shutil.rmtree(root)
print("cases", N, "diff", bad)

print(stats, len(outs)); print(list(outs)[:15])
