#!/usr/bin/env python3
"""fuzz-lsmodel.py - differential fuzz: the `ls -LRl` model shipped in controls/reference.py vs /usr/bin/ls.

The model is not copied: it is extracted from controls/reference.py at run time (between the warm-cache banner and
`class Resolver:`) into <work> and imported, so the bytes under test are the bytes the controls carry. The reference
binary is `/usr/bin/ls` (what the resolver's `ls` is: the counter copies `shutil.which("ls", path="/usr/bin")`),
run inside the C1 sandbox shape (bwrap, no /etc → numeric ids, no TZ → UTC).

Each seed builds a random tree under --work (dirs, files of 0/1/12345/1234567 bytes, symlinks to files, to dirs and
dangling, non-ASCII and newline names, an unreadable dir, pinned and live mtimes), picks an operand list (the dirs,
missing paths, a config file, duplicates, trailing slashes) and compares the model's stdout with the real one.

usage: fuzz-lsmodel.py [--work DIR] [--seeds N] [--controls DIR]
"""
import argparse
import importlib.util
import os
import random
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = [b"foot", b"kitty", b"Xterm", b"_priv", b"a b", b"a-b", b"a.b", b"z1", b"z10", b"0", b"~t", b"caf\xc3\xa9"]


def load_model(controls, work):
    src = open(os.path.join(controls, "reference.py"), encoding="latin-1").read()
    i = src.index("# --------------------------------------------------------------------------------------------- warm cache") \
        if "# --------------------------------------------------------------------------------------------- warm cache" in src \
        else src.index("# ------------------------------------------------------------------------------------------------ warm cache")
    j = src.index("class Resolver:")
    mod = os.path.join(work, "_lsmodel.py")
    with open(mod, "w") as fh:
        fh.write("import os\nimport stat\nimport time\n\n\nclass OutOfContract(Exception):\n    pass\n\n\n")
        fh.write(src[i:j])
    spec = importlib.util.spec_from_file_location("_lsmodel", mod)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def real_ls(root, operands):
    argv = ["bwrap", "--unshare-all", "--die-with-parent", "--clearenv",
            "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
            "--ro-bind", "/usr/bin/ls", "/bin/ls", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
            "--ro-bind", root, root, "--chdir", "/tmp", "--setenv", "LC_ALL", "C", "--setenv", "LANG", "C",
            "/bin/ls", "-LRl"] + operands
    p = subprocess.run(argv, capture_output=True)
    return p.returncode, p.stdout.decode("latin-1")


def build(rng, root):
    os.makedirs(root)
    now = int(time.time())
    epochs = [now - 10, now - 4000, now - 86400 * 200, 1600000000]
    dirs = [root]

    def fill(d, depth):
        for _ in range(rng.randint(0, 6)):
            n = rng.choice(NAMES)
            p = os.path.join(d.encode(), n)
            if os.path.lexists(p):
                continue
            r = rng.random()
            if r < 0.15 and depth < 3:
                os.makedirs(p)
                dirs.append(p.decode())
                fill(p.decode(), depth + 1)
            elif r < 0.30:
                target = rng.choice([b"foot", b"../x", b"nowhere", b"a" * 80 + b"/nothing"])
                if rng.random() < 0.5:
                    q = os.path.join(d.encode(), rng.choice(NAMES))
                    if os.path.lexists(q):
                        continue
                    open(q, "wb").write(b"x" * rng.randint(0, 3000))
                    target = os.path.basename(q)
                try:
                    os.symlink(target, p)
                except OSError:
                    pass
            elif r < 0.38:
                open(p, "wb").write(b"x" * rng.choice([0, 1, 12345, 1234567]))
            else:
                open(p, "wb").write(b"y")
            if rng.random() < 0.2:
                t = rng.choice(epochs) + rng.randint(0, 500)
                os.utime(p, (t, t), follow_symlinks=False)

    fill(root, 0)
    return dirs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    ap.add_argument("--seeds", type=int, default=150)
    ap.add_argument("--controls", default=os.path.join(HERE, "controls"))
    a = ap.parse_args()
    if not a.work:
        raise SystemExit("--work or TMPDIR required")
    work = os.path.realpath(os.path.abspath(a.work))
    os.makedirs(work, exist_ok=True)
    model = load_model(a.controls, work)
    print("model: extracted from %s; reference binary: /usr/bin/ls = %s"
          % (os.path.join(a.controls, "reference.py"),
             subprocess.run(["/usr/bin/ls", "--version"], capture_output=True).stdout.decode().split("\n")[0]))
    bad = 0
    for k in range(a.seeds):
        rng = random.Random(k)
        base = os.path.join(work, "fz", "%03d" % k)
        shutil.rmtree(base, ignore_errors=True)
        root = os.path.join(base, "r")
        dirs = build(rng, root)
        ops = list(dirs)
        ops += [os.path.join(root, "missing-%d" % i) for i in range(rng.randint(0, 2))]
        if rng.random() < 0.4:
            ops.append(root)
        if rng.random() < 0.3:
            ops.append(root + "/")
        ops.append(os.path.join(root, "cfg.list"))
        with open(ops[-1], "w") as fh:
            fh.write("x\n")
        links = []
        for dirpath, dirnames, filenames in os.walk(root):
            for n in dirnames + filenames:
                q = os.path.join(dirpath, n)
                if os.path.islink(q):
                    links.append(q)
        if links and rng.random() < 0.5:
            ops.append(rng.choice(links))       # a dangling or valid symlink operand (-L: dropped or dereferenced)
        if rng.random() < 0.2:
            os.chmod(dirs[-1], 0o000)
        rc, real = real_ls(root, ops)
        mine = model._ls_lRl(ops)
        if os.path.exists(dirs[-1]):
            os.chmod(dirs[-1], 0o755)
        if real != mine:
            bad += 1
            print("== MISMATCH seed %d rc=%d" % (k, rc))
            rl, ml = real.split("\n"), mine.split("\n")
            for i in range(max(len(rl), len(ml))):
                x = rl[i] if i < len(rl) else "<none>"
                y = ml[i] if i < len(ml) else "<none>"
                if x != y:
                    print("  line %d\n   real %r\n   mine %r" % (i, x, y))
                    break
        else:
            shutil.rmtree(base, ignore_errors=True)
    print("fuzz: %d/%d matched" % (a.seeds - bad, a.seeds))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
