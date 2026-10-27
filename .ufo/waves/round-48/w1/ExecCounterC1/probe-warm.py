#!/usr/bin/env python3
"""Probe 2: pinned-mtime determinism, same-size edit -> hit, size change -> stale, debug markers."""
import importlib.util
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location("c47", os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py"))
c47 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c47)

WORK = "/fast/scratch/hyaku/mado-r48/ExecCounterC1/probe"
os.makedirs(WORK, exist_ok=True)
box = c47.Box(WORK)
T = 1600000000

ENTRY = "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\nTryExec=foot\n"
CASE = {
    "id": "p2",
    "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
            "XDG_CURRENT_DESKTOP": "Hyprland"},
    "files": {
        "usr/share/applications/foot.desktop": ENTRY,
        "home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
        "home/.config/xdg-terminals.list": "foot.desktop\n",
        "etc/xdg/xdg-terminals.list": "foot.desktop\n",
    },
    "exec": ["bin/foot"],
    "args": ["--print-cmd"],
}
WRAP = open(os.path.join(WORK, "wrap.sh")).read() if os.path.exists(os.path.join(WORK, "wrap.sh")) else None


def pin_mtimes(root, t):
    files, dirs = [], []
    for d, ds, fs in os.walk(root):
        if os.path.relpath(d, root).split(os.sep)[0] == ".rw":
            continue
        for f in fs:
            files.append(os.path.join(d, f))
        for x in ds:
            p = os.path.join(d, x)
            if os.path.relpath(p, root).split(os.sep)[0] != ".rw":
                dirs.append(p)
    for p in files:
        os.utime(p, (t, t))
    for p in sorted(dirs, key=len, reverse=True):
        os.utime(p, (t, t))


def run(root, args, wrapped, extra_env=None):
    env = c47.case_env(CASE, root, "C.UTF-8")
    if extra_env:
        env.update(extra_env)
    a = box.argv(root, env, False, args)
    if wrapped:
        cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
        i = len(a) - len(args) - 1
        assert a[i] == "/oracle/xdg-terminal-exec"
        a[i:i + 1] = ["/bin/bash", "-c", WRAP, "w", cache, "/oracle/xdg-terminal-exec"]
    p = subprocess.run(a, capture_output=True, timeout=90, env={"PATH": "/usr/bin"})
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")


def state(err):
    if "cache is actual" in err:
        return "hit"
    if "cache is out-of-date" in err:
        return "stale"
    if "invalid cache data" in err or "reached cache line limit" in err or "failed to get fresh hash" in err:
        return "invalid"
    if "no cache data" in err:
        return "absent"
    return "disabled" if "paths:" in err else "early-exit"


def tree(tag, mutate=None):
    root = os.path.join(WORK, "same", "r")   # SAME path every time: hash comparability
    shutil.rmtree(os.path.join(WORK, "same"), ignore_errors=True)
    c47.materialize(root, CASE)
    pin_mtimes(root, T)
    return root


def scenario(name, mutate):
    root = tree(name)
    rc, out, err = run(root, ["--print-cmd"], True)
    cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
    primed = open(cache, "rb").read() if os.path.exists(cache) else b""
    if mutate:
        mutate(root)
        pin_mtimes(root, T)
    rc2, out2, err2 = run(root, ["--print-cmd"], False, {"XTE_DEBUG": "1"})
    print("%-14s prime_rc=%d prime_out=%r primed=%d lines=%d state=%s rc=%d out=%r cache_sha=%s" % (
        name, rc, out[:20], len(primed), primed.count(b"\n"), state(err2), rc2, out2[:40],
        (primed.split(b"\n", 1)[0][:8] if primed else b"-")))


def same_size(root):
    p = os.path.join(root, "usr/share/applications/foot.desktop")
    s = open(p).read().replace("Exec=foot", "Exec=foou").replace("TryExec=foot", "TryExec=foou")
    open(p, "w").write(s)


def bigger(root):
    p = os.path.join(root, "usr/share/applications/foot.desktop")
    open(p, "a").write("Name=x\n")


def tryexec_gone(root):
    os.unlink(os.path.join(root, "bin/foot"))
    p = os.path.join(root, "usr/share/applications/foot.desktop")
    open(p, "w").write(ENTRY.replace("TryExec=foot\n", ""))


scenario("pristine", None)
scenario("samesize", same_size)
scenario("bigger", bigger)
print("---- cache bytes:")
root = tree("x")
run(root, ["--print-cmd"], True)
print(repr(open(os.path.join(root, ".rw", "cache", "xdg-terminal-exec"), "rb").read()))
