"""Reproduce with ORACLE/EXT pointing at a copy of the pinned resolver and a dir of
its seven externals. Same tree, same creation order, two filesystems: the resolver's fallback order follows readdir."""
import os, shutil, subprocess, sys
ORACLE = os.environ.get("ORACLE", "/tmp/mado-r47-probe/oracle")
EXT = os.environ.get("EXT", "/tmp/mado-r47-probe/ext")
ENTRY = "[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=%s\n"
def build(root):
    shutil.rmtree(root, ignore_errors=True)
    app = os.path.join(root, "home/.local/share/applications")
    os.makedirs(app)
    os.makedirs(os.path.join(root, "home/.config"))
    os.makedirs(os.path.join(root, "bin"))
    for n in ("foot", "alacritty"):
        open(os.path.join(root, "bin", n), "w").write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(root, "bin", n), 0o755)
    for n in ("foot", "alacritty"):          # same creation order in both trees
        open(os.path.join(app, n + ".desktop"), "w").write(ENTRY % n)
    open(os.path.join(root, "home/.config/xdg-terminals.list"), "w").write("+foot.desktop\n-foot.desktop\n")
    return root
def run(root):
    env = {"HOME": root + "/home", "PATH": root + "/bin:" + EXT,
           "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc",
           "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/opt",
           "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_CACHE_HOME": root + "/.rw"}
    p = subprocess.run([ORACLE, "--print-id"], env=env, cwd=root, capture_output=True)
    return p.returncode, p.stdout.decode().strip(), os.listdir(root + "/home/.local/share/applications")
for base in (os.environ.get("TMPA", "/tmp/mado-r47-probe/ord"), os.environ.get("TMPB", "/dev/shm/ord")):
    root = build(base)
    rc, out, order = run(root)
    print("%-45s readdir=%s -> --print-id rc=%d %r" % (base, order, rc, out))
    shutil.rmtree(base, ignore_errors=True)
