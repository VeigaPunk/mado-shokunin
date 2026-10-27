#!/usr/bin/env python3
"""L1 differential fuzz: lsemu.ls_lRL vs `LC_ALL=C LANG=C ls -LRl` (host). Usage: lsfuzz.py WORK N SEED"""
import os
import random
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lsemu  # noqa: E402

NAMES = ["a", "b", "B", "_x", "a.desktop", "foo bar", "z-1", "10", "9", "x.list", "sub", "Sub", ".hid", "é", "a_b"]


def build(root, rng):
    os.makedirs(root)
    dirs = [root]
    for _ in range(rng.randint(0, 14)):
        d = rng.choice(dirs)
        n = rng.choice(NAMES) + ("" if rng.random() < 0.6 else str(rng.randint(0, 99)))
        p = os.path.join(d, n)
        if os.path.lexists(p):
            continue
        r = rng.random()
        if r < 0.25 and len(dirs) < 6:
            os.mkdir(p)
            dirs.append(p)
        elif r < 0.35:
            tgt = rng.choice(dirs + [p + "-missing"])
            os.symlink(tgt, p)
        else:
            with open(p, "w") as fh:
                fh.write("x" * rng.choice([0, 1, 5, 100, 4097, 9000]))
            os.chmod(p, rng.choice([0o644, 0o755, 0o600, 0o4755, 0o1777, 0o640]))
        t = rng.choice([1790000000, 1761500000, 1500000000, 1761490000 + rng.randint(0, 9999)])
        os.utime(p, (t, t), follow_symlinks=False) if not os.path.islink(p) else None
    for d in dirs[1:]:
        t = rng.choice([1790000000, 1761500000, 1500000000])
        os.utime(d, (t, t))
    return dirs


def main():
    work, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    bad = 0
    for i in range(n):
        rng = random.Random(seed * 100000 + i)
        root = os.path.join(work, "t%d" % i)
        dirs = build(root, rng)
        ops = [root + "/x.list", root + "/missing"] + [d + ("/" if rng.random() < 0.5 else "") for d in dirs[:3]]
        rng.shuffle(ops)
        env = {"LC_ALL": "C", "LANG": "C", "PATH": "/usr/bin", "TZ": os.environ.get("TZ", "")}
        if not env["TZ"]:
            del env["TZ"]
        real = subprocess.run(["ls", "-LRl"] + ops, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env).stdout
        mine = lsemu.ls_lRL(ops)
        if real != mine:
            bad += 1
            if bad <= 3:
                print("MISMATCH case %d" % i)
                rl, ml = real.decode(errors="replace").splitlines(), mine.decode(errors="replace").splitlines()
                for a, b in zip(rl, ml):
                    if a != b:
                        print(" real:", repr(a))
                        print(" mine:", repr(b))
                        break
                else:
                    print(" lengths", len(rl), len(ml))
        shutil.rmtree(root)
    print("cases=%d mismatches=%d seed=%d" % (n, bad, seed))


main()
