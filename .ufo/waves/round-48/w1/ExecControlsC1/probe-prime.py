#!/usr/bin/env python3
"""probe-prime.py - F1: the resolver's cache exists only if the sandbox's PID namespace is held open.

`save_cache "$1" &` (pin :1455-1457) is forked; bwrap is PID 1 of the namespace and kills the namespace when its
child exits, so a plain `--print-cmd` run leaves no cache. This probe runs the pinned resolver twice on identical
trees with the same argv, once plain and once wrapped in a shell that spins until the cache file appears, and prints
what each leaves behind. Read-only outside --work; launches no terminal (print options only).

usage: probe-prime.py [--work DIR]
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.realpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PIN = os.path.join(LANE, ".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec")
SPIN = 'i=0; while [ ! -f "$XDG_CACHE_HOME/xdg-terminal-exec" ] && [ "$SECONDS" -lt 5 ]; do :; done'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    a = ap.parse_args()
    if not a.work:
        raise SystemExit("--work or TMPDIR required")
    w = os.path.realpath(os.path.join(os.path.abspath(a.work), "prime-probe"))
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    bin7 = os.path.join(w, "bin7")
    os.makedirs(bin7)
    for n in ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm"):
        shutil.copy(os.path.realpath("/usr/bin/" + n), os.path.join(bin7, n))
    pin = os.path.join(w, "xdg-terminal-exec")
    shutil.copyfile(PIN, pin)
    os.chmod(pin, 0o755)

    def tree(name):
        root = os.path.join(w, name, "r")
        for d in ("home/.config", ".rw/cache", "usr/share/applications", "bin"):
            os.makedirs(os.path.join(root, d))
        with open(os.path.join(root, "usr/share/applications/foot.desktop"), "w") as fh:
            fh.write("[Desktop Entry]\nType=Application\nName=foot\nExec=foot\n"
                     "Categories=System;TerminalEmulator;\n")
        with open(os.path.join(root, "home/.config/xdg-terminals.list"), "w") as fh:
            fh.write("foot.desktop\n")
        with open(os.path.join(root, "bin/foot"), "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(root, "bin/foot"), 0o755)
        for p in (root, os.path.join(root, "usr/share/applications/foot.desktop")):
            os.utime(p, (1600000000, 1600000000))
        return root

    def run(root, wrap):
        env = {"HOME": root + "/home", "PATH": root + "/bin:/oracle/bin",
               "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc/xdg",
               "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/usr/share",
               "XDG_CACHE_HOME": root + "/.rw/cache", "XDG_CURRENT_DESKTOP": "Hyprland", "LANG": "C.UTF-8"}
        argv = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
                "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib",
                "--symlink", "usr/lib", "/lib64", "--ro-bind", "/usr/bin/bash", "/bin/sh",
                "--ro-bind", "/usr/bin/bash", "/bin/bash", "--ro-bind", bin7, "/oracle/bin",
                "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
                "--ro-bind", root, root, "--bind", root + "/.rw", root + "/.rw", "--chdir", root,
                "--ro-bind", pin, "/oracle/xdg-terminal-exec"]
        for k in sorted(env):
            argv += ["--setenv", k, env[k]]
        if wrap:
            argv += ["/bin/bash", "-c", "/oracle/xdg-terminal-exec --print-cmd; " + SPIN]
        else:
            argv += ["/oracle/xdg-terminal-exec", "--print-cmd"]
        p = subprocess.run(argv, capture_output=True)
        time.sleep(0.5)
        cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        return p.returncode, p.stdout.decode(), os.path.exists(cache)

    for label, wrap in (("plain run", False), ("wrapped in a waiter", True)):
        root = tree(label.replace(" ", "-"))
        rc, out, has = run(root, wrap)
        print("%-22s rc=%d stdout=%r cache written=%s" % (label, rc, out, has))
        if has:
            text = open(os.path.join(root, ".rw/cache/xdg-terminal-exec")).read()
            print("%-22s cache line 1 = %s, %d lines, ends with the terminator: %s"
                  % ("", text.split("\n")[0], len(text.split("\n")) - 1,
                     text.rstrip("\n").endswith("\x1eEND_OF_EXEC_USEP")))
    shutil.rmtree(w, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
