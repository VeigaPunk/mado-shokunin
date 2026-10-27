#!/usr/bin/env python3
"""Differential harness: warmcache.ls_lRL() vs the host's GNU ls, inside a bwrap sandbox with no /etc.

Run as:  /usr/bin/python3 /mod/harness_ls.py <workdir> <seed> <trees> [--keep]

Every tree is built under <workdir>/t<NN>/ and listed with one or more random operand sets.
The oracle is `/usr/bin/ls -LRl <operands>` (a copy of the host binary at /lsbin/ls) run with
LANG=C LC_ALL=C and a piped stdout, exactly as the resolver runs it (x:205). stderr is dropped on
both sides. A mismatch prints the first differing offset plus the two outputs and exits 1.
Writes nothing outside <workdir>; prints a one-line summary per tree.
"""
import os
import random
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warmcache  # noqa: E402

LS = "/lsbin/ls"
NOW = time.time()

NAME_POOL = ["foot", "kitty", "alacritty", "xterm", "a", "B", "z1", "0", "_x", "with space",
             "dot.name", "dot..dot", "üni", "日本", "tab\tchar", "quo\"te", "ap'os", "back\\slash",
             "star*", "semi;", "-dash", "x=y", "par(en)", "nl\nname", "ctl\x01", "del\x7f", "~tilde",
             "a" * 60, "Zz", ".hidden", ".hiddendir"]


def rnd_name(rng):
    n = rng.choice(NAME_POOL)
    if rng.random() < 0.35:
        n = n + rng.choice(["", "1", "_2", ".bak", "-x"])
    return n


def rnd_mtime(rng):
    kind = rng.randrange(12)
    if kind == 0:
        return NOW + rng.randrange(60, 100000)              # future -> year
    if kind == 1:
        return NOW - rng.randrange(15778476 + 7200, 40000000)  # older than six months -> year
    if kind == 2:
        return NOW - rng.randrange(7200, 15778476 - 7200)   # inside the window -> HH:MM
    if kind == 3:
        return 0
    if kind == 4:
        return 946684800
    if kind == 5:
        return -rng.randrange(1, 100000000)
    if kind == 6:
        return NOW - 15778476 - rng.randrange(7200, 90000000)
    if kind == 7:
        return NOW - 15778476 + rng.randrange(7200, 90000000)
    if kind == 8:
        return NOW - rng.randrange(1, 600)                  # within the last minutes
    return rng.randrange(-2000000000, int(NOW) + 3000000)


def pinned_now_collision(ts):
    """Keep a pinned mtime away from ls's two decision boundaries (they move with the wall clock)."""
    for edge in (NOW, NOW - warmcache.HALF_YEAR):
        if abs(ts - edge) < 120:
            ts = edge - 3600 if ts <= edge else edge + 3600
    return ts


def mkfile(path, size, rng):
    with open(path, "wb") as fh:
        fh.write(bytes(rng.randrange(256) for _ in range(size)) if size < 200
                 else b"\xab" * size)


def build(root, rng, depth=0):
    """Random tree; returns (files, dirs) of relative paths."""
    files, dirs = [], []
    n = rng.randrange(1, 6)
    for _ in range(n):
        nm = rnd_name(rng)
        p = os.path.join(root, nm)
        if os.path.lexists(p):
            continue
        kind = rng.randrange(10)
        if kind < 6:
            mkfile(p, rng.choice([0, 0, 1, 2, 100, 4096, 4097, 5000, 65536]), rng)
        elif kind < 8:
            os.mkdir(p)
            dirs.append(p)
        else:
            target = rng.choice(["nowhere", "/nonexistent/x", "sibling", ".", "..", "loop_a", "loop_b"])
            try:
                os.symlink(target, p)
            except OSError:
                pass
        if os.path.lexists(p):
            files.append(p)
        if os.path.isdir(p) and not os.path.islink(p) and depth < 2 and rng.random() < 0.9:
            sub_f, sub_d = build(p, rng, depth + 1)
            files += sub_f
            dirs += sub_d
    # a couple of deliberate shapes
    if rng.random() < 0.4:
        q = os.path.join(root, "loop_a")
        if not os.path.lexists(q):
            try:
                os.symlink("loop_b", q)
                os.symlink("loop_a", os.path.join(root, "loop_b"))
            except OSError:
                pass
    if rng.random() < 0.3:
        q = os.path.join(root, "dirlink")
        if not os.path.lexists(q) and dirs:
            try:
                os.symlink(os.path.basename(rng.choice([d for d in dirs])) or ".", q)
            except OSError:
                pass
    return files, dirs


def set_modes(root, rng):
    for dirpath, dirnames, filenames in os.walk(root):
        for nm in filenames + dirnames:
            p = os.path.join(dirpath, nm)
            if os.path.islink(p):
                continue
            mode = rng.choice([0o644, 0o600, 0o640, 0o664, 0o755, 0o700, 0o750, 0o444])
            if os.path.isdir(p) and rng.random() < 0.4:
                mode = rng.choice([0o1777, 0o2755, 0o700, 0o755, 0o750])
            if os.path.isfile(p) and rng.random() < 0.15:
                mode |= 0o4000
            try:
                os.chmod(p, mode)
            except OSError:
                pass


def pin_mtimes(root, rng):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for nm in filenames + dirnames + ["."]:
            p = os.path.join(dirpath, nm)
            ts = pinned_now_collision(rnd_mtime(rng))
            try:
                os.utime(p, (ts, ts), follow_symlinks=False)
            except OSError:
                pass


def pick_operands(root, files, dirs, rng):
    ops = []
    pool = list(files) + list(dirs)
    rng.shuffle(pool)
    for p in pool[:rng.randrange(0, 5)]:
        ops.append(p)
    if dirs and rng.random() < 0.5:
        ops.append(rng.choice(dirs) + "/")
    if rng.random() < 0.3:
        ops.append(os.path.join(root, "missing-%d" % rng.randrange(100)))
    if rng.random() < 0.2:
        ops.append(".")
    if rng.random() < 0.2 and ops:
        ops.append(ops[0])
    if rng.random() < 0.15:
        ops.insert(0, "")
    rng.shuffle(ops)
    return ops


def oracle(ops, cwd):
    env = {"PATH": "/lsbin", "LANG": "C", "LC_ALL": "C", "HOME": "/nonexistent"}
    p = subprocess.run([LS, "-LRl"] + ops, cwd=cwd, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)
    return p.stdout


def _rmtree(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for nm in dirnames:
            try:
                os.chmod(os.path.join(dirpath, nm), 0o755)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def first_diff(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    return n if len(a) != len(b) else -1


def show(data, off):
    lo = max(0, data.rfind(b"\n", 0, off) - 200)
    return data[lo:off + 200]


def main(argv):
    work = argv[1]
    seed = int(argv[2])
    trees = int(argv[3])
    rng = random.Random(seed)
    bad = 0
    cases = 0
    for t in range(trees):
        root = os.path.join(work, "t%03d" % t)
        if os.path.lexists(root):
            _rmtree(root)
        os.makedirs(root, exist_ok=True)
        files, dirs = build(root, rng)
        set_modes(root, rng)
        pin_mtimes(root, rng)
        for k in range(4):
            ops = pick_operands(root, files, dirs, rng)
            ops_abs = [o if not o or o.startswith(("/", ".")) else os.path.join(root, o) for o in ops]
            # run from / so the printed names are the absolute ones both sides see
            want = oracle(ops_abs, os.getcwd())
            # the module sees the same strings; now must be the moment ls ran, close enough
            got = warmcache.ls_lRL(ops_abs, now=time.time())
            cases += 1
            off = first_diff(want, got)
            if off >= 0:
                bad += 1
                print("MISMATCH tree=%d case=%d seed=%d off=%d" % (t, k, seed, off))
                print(" operands: %r" % (ops_abs,))
                print(" want: %r" % show(want, min(off, len(want))))
                print(" got : %r" % show(got, min(off, len(got))))
                if bad >= 6:
                    print("stopping after 6 mismatches")
                    return 1
        print("ok tree=%d files=%d dirs=%d" % (t, len(files), len(dirs)))
    print("LS-DIFF: seed=%d trees=%d cases=%d mismatches=%d" % (seed, trees, cases, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
