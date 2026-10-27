#!/usr/bin/env python3
"""gen_hash agreement: prime the REAL pinned resolver, then compare line 1 of the cache it saved with
warmcache.gen_hash() over the resolver's own XTE__CONFIGS / XTE__APPLICATIONS_DIRS (read from XTE_DEBUG=1
stderr, not re-derived here).

  /usr/bin/python3 /mod/harness_hash.py <workdir> <seed> <trees>

Per tree: one cold `--print-cmd` run inside the sandbox (the background save_cache is given 0.4 s to land,
see the wrapper), then the cache file is read. Prints one line per tree and a final
`HASH-AGREE: seed=.. trees=.. agree=.. disagree=..` and writes a TSV (tree, ours, theirs) to
<workdir>/hash-<seed>.tsv.
"""
import os
import random
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warmcache  # noqa: E402

PIN = "/oracle/xdg-terminal-exec"
NOW = time.time()
W = "/xbin/wrapped-pin"  # keeps the sandbox alive for the background save_cache
NAMES = ["foot", "kitty", "xterm", "a b", "üni", "tab\tx", "n\nl", "dot.name", "-dash", "star*",
         "q\"q", "back\\sl", "long" + "n" * 40, ".hidden", "caps", "0n"]
DESKTOPS = ["Hyprland", "Hyprland:GNOME", "", "sway", "KDE:Hyprland:Hyprland", "GNOME"]
SIZES = [0, 1, 7, 100, 1024, 4096, 4097, 5000, 65536]


def rmtree(path):
    if not os.path.lexists(path):
        return
    for dirpath, dirnames, _f in os.walk(path):
        for nm in dirnames:
            try:
                os.chmod(os.path.join(dirpath, nm), 0o755)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def mtime(rng):
    k = rng.randrange(8)
    if k == 0:
        ts = NOW + rng.randrange(120, 90000)
    elif k == 1:
        ts = NOW - rng.randrange(warmcache.HALF_YEAR + 7200, 40000000)
    elif k == 2:
        ts = NOW - rng.randrange(7200, warmcache.HALF_YEAR - 7200)
    elif k == 3:
        ts = 0
    elif k == 4:
        ts = 946684800
    elif k == 5:
        ts = -rng.randrange(1, 100000000)
    elif k == 6:
        ts = NOW - rng.randrange(1, 600)
    else:
        ts = rng.randrange(-2000000000, int(NOW) + 3000000)
    for edge in (NOW, NOW - warmcache.HALF_YEAR):
        if abs(ts - edge) < 300:
            ts = int(edge) - 7200 if ts <= edge else int(edge) + 7200
    return int(ts)


def junk(appdir, rng, depth=0):
    """Random files, symlinks, nested dirs inside an application dir (the hash sees all of them)."""
    for _ in range(rng.randrange(1, 5)):
        nm = rng.choice(NAMES)
        p = os.path.join(appdir, nm)
        if os.path.lexists(p):
            continue
        kind = rng.randrange(10)
        if kind < 6:
            with open(p, "wb") as fh:
                fh.write(b"x" * rng.choice(SIZES))
        elif kind < 8:
            os.mkdir(p)
            if depth < 2:
                junk(p, rng, depth + 1)
        else:
            try:
                os.symlink(rng.choice(["nowhere", "..", ".", nm, "/nowhere/x"]), p)
            except OSError:
                pass
        if os.path.lexists(p):
            ts = mtime(rng)
            try:
                os.utime(p, (ts, ts), follow_symlinks=False)
            except OSError:
                pass


def build(root, rng):
    home = os.path.join(root, "home")
    for d in ("home/.config", "home/.local/share/applications", "cfg1", "cfg2",
              "data1/applications", "data2/applications", "data1/xdg-terminal-exec",
              "data2/xdg-terminal-exec", "bin", ".rw/cache"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    term = "foot"
    with open(os.path.join(root, "home/.local/share/applications/foot.desktop"), "w") as fh:
        fh.write("[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\n"
                 "Categories=System;TerminalEmulator;\n")
    with open(os.path.join(root, "bin", term), "w") as fh:
        fh.write("#!/bin/sh\nexit 1\n")
    os.chmod(os.path.join(root, "bin", term), 0o755)
    with open(os.path.join(root, "home/.config/xdg-terminals.list"), "w") as fh:
        fh.write("foot.desktop\n")
    # random list files in every config position, some with junk lines
    for cfg in ("home/.config", "cfg1", "cfg2", "data1/xdg-terminal-exec", "data2/xdg-terminal-exec"):
        for sfx in ("xdg-terminals.list", "hyprland-xdg-terminals.list"):
            p = os.path.join(root, cfg, sfx)
            if os.path.exists(p):
                continue
            if rng.random() < 0.5:
                with open(p, "w") as fh:
                    fh.write(rng.choice(["", "foot.desktop\n", "nope.desktop\nfoot.desktop\n",
                                         "+foot.desktop\n", "garbage line\n"]))
                ts = mtime(rng)
                os.utime(p, (ts, ts))
    for appdir in ("home/.local/share/applications", "data1/applications", "data2/applications"):
        junk(os.path.join(root, appdir), rng)
    # a couple of empty directories and a dangling symlink in the app dirs
    os.makedirs(os.path.join(root, "data2/applications/emptydir"), exist_ok=True)
    try:
        os.symlink("nowhere-at-all", os.path.join(root, "data1/applications/gone"))
    except OSError:
        pass
    ts = mtime(rng)
    for d in ("data1/applications", "data2/applications", "home/.local/share/applications"):
        try:
            os.utime(os.path.join(root, d), (ts, ts))
        except OSError:
            pass


def run_primed(root, desk):
    env = {
        "HOME": os.path.join(root, "home"),
        "XDG_CONFIG_HOME": os.path.join(root, "home/.config"),
        "XDG_CONFIG_DIRS": os.path.join(root, "cfg1") + ":" + os.path.join(root, "cfg2"),
        "XDG_DATA_HOME": os.path.join(root, "home/.local/share"),
        "XDG_DATA_DIRS": os.path.join(root, "data1") + ":" + os.path.join(root, "data2"),
        "XDG_CACHE_HOME": os.path.join(root, ".rw/cache"),
        "XDG_CURRENT_DESKTOP": desk,
        "PATH": os.path.join(root, "bin") + ":/oracle/bin",
        "LANG": "C.UTF-8",
        "XTE_DEBUG": "1",
    }
    argv = [W, "--print-cmd"]
    p = subprocess.run(argv, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    err = p.stderr.decode("utf-8", "surrogateescape")
    conf = re.search(r"^D:   XTE__CONFIGS=(.*)$", err, re.M)
    apps = re.search(r"^D:   XTE__APPLICATIONS_DIRS=(.*)$", err, re.M)
    dhash = re.search(r"^D: got fresh hash '([0-9a-f]{32})'$", err, re.M)
    cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
    saved = None
    for _ in range(40):
        try:
            with open(cache, "rb") as fh:
                data = fh.read()
            if data.endswith(b"\n"):
                saved = data.split(b"\n")[0].decode()
                break
        except OSError:
            pass
        time.sleep(0.02)
    return p.returncode, p.stdout, conf.group(1) if conf else None, apps.group(1) if apps else None, \
        saved, (dhash.group(1) if dhash else None), err


def main(argv):
    work = argv[1]
    seed = int(argv[2])
    trees = int(argv[3])
    rng = random.Random(seed)
    agree = disagree = 0
    rows = []
    for t in range(trees):
        root = os.path.join(work, "h%03d" % t)
        rmtree(root)
        os.makedirs(root)
        build(root, rng)
        desk = rng.choice(DESKTOPS)
        rc, out, conf, apps, saved, dhash, err = run_primed(root, desk)
        if conf is None or apps is None:
            print("SETUP tree=%d rc=%d no debug paths\n%s" % (t, rc, err[-600:]))
            return 2
        mine = warmcache.gen_hash(desk, conf, apps, now=time.time())
        theirs = saved
        ok = (mine == theirs) and (dhash is None or mine == dhash)
        agree += 1 if ok else 0
        disagree += 0 if ok else 1
        rows.append((t, mine, theirs, dhash or "-", desk))
        print("%s tree=%d seed=%d ours=%s cache=%s debug=%s" %
              ("agree" if ok else "DISAGREE", t, seed, mine, theirs, dhash))
        if not ok:
            print("  desktop=%r\n  configs=%s\n  apps=%s" % (desk, conf, apps))
            print("  stdout=%r rc=%d" % (out[:200], rc))
    with open(os.path.join(work, "hash-%d.tsv" % seed), "w") as fh:
        for r in rows:
            fh.write("%d\t%s\t%s\t%s\t%s\n" % r)
    print("HASH-AGREE: seed=%d trees=%d agree=%d disagree=%d" % (seed, trees, agree, disagree))
    return 0 if disagree == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
