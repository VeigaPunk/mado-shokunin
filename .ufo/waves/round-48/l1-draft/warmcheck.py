#!/usr/bin/env python3
"""L1 pre-freeze check: the l1-draft tool vs the pinned resolver on random warm-cache cases (host env -i, no bwrap).

Usage: warmcheck.py WORK N SEED   (WORK outside the lane; xdg-terminal-exec only with --print-*, XDG_CACHE_HOME in WORK)
Each case: build a tree (fixed mtimes), prime the pin with a cold --print-cmd run (sh -c '...; wait' so the background
save finishes), optionally mutate, then run the pin and the tool with the same args on the same tree and cache.
"""
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIN = "/usr/bin/xdg-terminal-exec"  # sha256 89f2be9a... = round-47 fetch pin
TOOL = os.environ.get("MADO_TOOL") or os.path.join(HERE, "mado-terminal.py")
T0 = 1761400000


def term(name, extra=""):
    return "[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n%s" % (name, name, extra)


def write(root, rel, text, t=T0):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        fh.write(text)
    os.utime(p, (t, t))


def stub(root, name):
    write(root, "bin/" + name, "#!/bin/sh\nexit 1\n")
    os.chmod(os.path.join(root, "bin", name), 0o755)


def pin_dirs(root, t=T0):
    for d, subs, _f in os.walk(root):
        for s in subs:
            os.utime(os.path.join(d, s), (t, t))


def env(root, desk="Hyprland", **kw):
    e = {"HOME": root + "/home", "PATH": root + "/bin:/usr/bin", "XDG_CONFIG_HOME": root + "/home/.config",
         "XDG_CONFIG_DIRS": root + "/etc/xdg", "XDG_DATA_HOME": root + "/home/.local/share",
         "XDG_DATA_DIRS": root + "/usr/share", "XDG_CACHE_HOME": root + "/cache", "LC_ALL": "C"}
    if desk is not None:
        e["XDG_CURRENT_DESKTOP"] = desk
    e.update(kw)
    return {k: v for k, v in e.items() if v is not None}


def run_pin(e, args, root):
    cmd = "'%s' \"$@\"; rc=$?; wait; exit $rc" % os.path.abspath(PIN)
    r = subprocess.run(["/bin/sh", "-c", cmd, "sh"] + args, env=e, cwd=root, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=20)
    return r.stdout, r.returncode


def run_tool(e, args, root):
    r = subprocess.run([sys.executable, "-I", TOOL, "print"] + args, env=e, cwd=root, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=60)
    return r.stdout, r.returncode


A = "usr/share/applications/"
H = "home/.local/share/applications/"
L = "home/.config/xdg-terminals.list"
ARGS = [["--print-id"], ["--print-path"], ["--print-cmd"], ["--print-id", "--print-path", "--print-cmd"],
        ["--print-cmd", "--dir=/srv", "--title=x"], ["--print-cmd", "--", "htop"], ["--print-content"],
        ["--print-cmd", "--hold"]]


def case(root, rng):
    os.makedirs(root + "/home", exist_ok=True)
    os.makedirs(root + "/cache", exist_ok=True)
    terms = ["foot", "kitty", "alacritty"]
    for t in terms:
        extra = rng.choice(["", "TerminalArgDir=--working-directory=\n", "X-TerminalArgTitle=--title\n",
                            "TerminalArgHold=--hold\n", "TryExec=%s\n" % t])
        write(root, rng.choice([A, H]) + t + ".desktop", term(t, extra))
        stub(root, t)
    if rng.random() < 0.6:
        write(root, L, "".join(rng.sample([t + ".desktop\n" for t in terms], 2)))
    pin_dirs(root)
    e = env(root)
    prime = ["--print-cmd"]
    run_pin(e, prime, root)
    kind = rng.choice(["none", "same-size-edit", "rm-tryexec-stub", "new-file", "touch", "desk", "rm-exec0", "args",
                       "truncate-cache", "disable"])
    if kind == "same-size-edit":
        # replace the selected entry's Exec with another stub of the same length, keep the mtime
        out = run_pin(dict(e, XTE_CACHE_ENABLED="false"), ["--print-path"], root)[0].decode().strip()
        if out and os.path.isfile(out):
            txt = open(out).read()
            for t in terms:
                txt = txt.replace("Exec=foot\n", "Exec=fooT\n")
            stub(root, "fooT")
            st = os.stat(out)
            with open(out, "w") as fh:
                fh.write(txt)
            os.utime(out, (st.st_mtime, st.st_mtime))
            pin_dirs(root)
            os.utime(root + "/bin", (T0, T0))
    elif kind == "rm-tryexec-stub":
        for t in terms:
            p = root + "/bin/" + t
            if rng.random() < 0.5 and os.path.exists(p):
                os.unlink(p)
    elif kind == "new-file":
        write(root, A + "zz.desktop", "[Desktop Entry]\n")
        pin_dirs(root)
    elif kind == "touch":
        p = root + "/" + rng.choice([A, H])
        if os.path.isdir(p):
            os.utime(p, (T0 + 120, T0 + 120))
    elif kind == "desk":
        e["XDG_CURRENT_DESKTOP"] = "GNOME"
    elif kind == "rm-exec0":
        for t in terms:
            if os.path.exists(root + "/bin/" + t):
                os.unlink(root + "/bin/" + t)
                break
    elif kind == "truncate-cache":
        p = root + "/cache/xdg-terminal-exec"
        if os.path.exists(p):
            data = open(p, "rb").read()
            open(p, "wb").write(data[:rng.randint(0, len(data))])
    elif kind == "disable":
        e["XTE_CACHE_ENABLED"] = rng.choice(["false", "0", "maybe"])
    args = rng.choice(ARGS)
    cache_before = open(root + "/cache/xdg-terminal-exec", "rb").read() if os.path.exists(root + "/cache/xdg-terminal-exec") else None
    tool = run_tool(e, args, root)
    pin = run_pin(e, args, root)
    cold = run_pin(dict(e, XDG_CACHE_HOME=root + "/cold"), args, root)
    return kind, args, pin, tool, cold, cache_before


def main():
    work, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    bad = differ = 0
    kinds = {}
    for i in range(n):
        rng = random.Random(seed * 100000 + i)
        root = os.path.join(work, "w%d" % i)
        shutil.rmtree(root, ignore_errors=True)
        kind, args, pin, tool, cold, _cb = case(root, rng)
        kinds[kind] = kinds.get(kind, 0) + 1
        if pin != cold:
            differ += 1
        if pin != tool:
            bad += 1
            if bad <= 5:
                print("MISMATCH %d kind=%s args=%s pin=%r tool=%r cold=%r" % (i, kind, args, pin, tool, cold))
        shutil.rmtree(root, ignore_errors=True)
    print("cases=%d mismatches=%d warm_differs_from_cold=%d kinds=%s seed=%d" % (n, bad, differ, kinds, seed))


main()
