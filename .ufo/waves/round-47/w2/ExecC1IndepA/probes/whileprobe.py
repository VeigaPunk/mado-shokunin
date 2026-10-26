"""The documented 'read that ends while the last executed step failed' rule (docstring step 5)."""
import os, shutil, subprocess
ORACLE = os.environ.get("ORACLE", "/tmp/mado-r47-probe/oracle")
EXT = os.environ.get("EXT", "/tmp/mado-r47-probe/ext")
BASE = "[Desktop Entry]\nCategories=System;TerminalEmulator;\nExec=foot\nActions=new;\n[Desktop Action new]\nExec=foot --new\n"
def run(extra):
    root = os.environ.get("WP", "/tmp/mado-r47-probe/wp")
    shutil.rmtree(root, ignore_errors=True)
    app = root + "/home/.local/share/applications"
    os.makedirs(app); os.makedirs(root + "/home/.config"); os.makedirs(root + "/bin")
    open(root + "/bin/foot", "w").write("#!/bin/sh\nexit 1\n"); os.chmod(root + "/bin/foot", 0o755)
    open(app + "/foot.desktop", "w").write(BASE + extra)
    open(root + "/home/.config/xdg-terminals.list", "w").write("foot.desktop:new\n")
    env = {"HOME": root + "/home", "PATH": root + "/bin:" + EXT,
           "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc",
           "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/opt",
           "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_CACHE_HOME": root + "/.rw"}
    p = subprocess.run([ORACLE, "--print-id", "--print-cmd"], env=env, cwd=root, capture_output=True)
    return p.returncode, p.stdout.decode().strip().replace("\n", "|")
print("last line [Other]      ->", run("[Other]\n"))
print("last line [Desktop Entry]->", run("[Desktop Entry]\n"))
shutil.rmtree(os.environ.get("WP", "/tmp/mado-r47-probe/wp"), ignore_errors=True)
