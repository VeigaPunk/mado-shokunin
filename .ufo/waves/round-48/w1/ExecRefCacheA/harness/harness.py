#!/usr/bin/env python3
"""Differential harness (seat ExecRefCacheA, round 48 w1): the warm-cache model vs the pinned resolver.

Nothing here is evidence by itself; receipts land in the seat dir.
Subcommands: lsdiff N   - compare ls_lrl() with /usr/bin/ls -LRl inside the sandbox
             warm      - prime both twin trees with the pin, mutate, compare pin (warm) with the tool
"""
import importlib.util
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import time

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = LANE + "/.ufo/waves/round-47/fetch/xdg-terminal-exec"
PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
TOOL = LANE + "/.ufo/waves/round-48/w1/ExecRefCacheA/mado-terminal.py"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
BASH = os.path.realpath("/usr/bin/bash")
PYTHON = os.path.realpath(sys.executable)
USEP = "\x1f"
TERM = "\x1eEND_OF_EXEC_USEP"

PRIME = ('/oracle/xdg-terminal-exec "$@" > /dev/null; f="$XDG_CACHE_HOME/xdg-terminal-exec"; '
         'for i in {1..300000}; do [ -s "$f" ] && break; done')

LS_PROBE = ("import importlib.util,os,sys\n"
            "spec=importlib.util.spec_from_file_location('mado','/oracle/tool.py')\n"
            "m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
            "sys.stdout.buffer.write(m.ls_lrl(sys.argv[1:], dict(os.environ), os.getcwd()))\n")


def sha(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


class Box:
    def __init__(self, work):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            raise SystemExit("bwrap missing")
        assert sha(PIN) == PIN_SHA, "pin drift"
        self.bin = os.path.join(work, "bin")
        os.makedirs(self.bin, exist_ok=True)
        self.pin = os.path.join(work, "pin/xdg-terminal-exec")
        os.makedirs(os.path.dirname(self.pin), exist_ok=True)
        with open(PIN, "rb") as fh:
            blob = fh.read()
        with open(self.pin, "wb") as fh:
            fh.write(blob)
        os.chmod(self.pin, 0o755)
        for n in EXTERNALS:
            src = shutil.which(n, path="/usr/bin")
            shutil.copy(os.path.realpath(src), os.path.join(self.bin, n))

    def argv(self, root, env, run, args, extra=()):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", BASH, "/bin/sh", "--ro-bind", BASH, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", rw, rw]
        if run in ("pin", "warm"):
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        elif run in ("tool", "model", "hash"):
            a += ["--ro-bind", PYTHON, "/usr/bin/python3", "--ro-bind", TOOL, "/oracle/tool.py"]
        a += ["--chdir", root]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if run == "pin":
            a += ["/bin/bash", "-c", PRIME, "prime"] + list(args)
        elif run == "warm":
            a += ["/oracle/xdg-terminal-exec"] + list(args)
        elif run == "tool":
            a += ["/usr/bin/python3", "-I", "/oracle/tool.py"] + list(args)
        elif run == "ls":
            a += ["/oracle/bin/ls", "-LRl"] + list(args)
        elif run == "model":
            a += ["/usr/bin/python3", "-I", "-c", LS_PROBE] + list(args)
        elif run == "hash":
            a += ["/usr/bin/python3", "-I", "-c", HASH_PROBE] + list(args)
        return a

    def run(self, root, env, kind, args, timeout=60):
        argv = self.argv(root, env, kind, args)
        p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
        return p.returncode, p.stdout.decode("latin-1"), p.stderr.decode("latin-1")


def materialize(root, files, execs, modes=(), mtime=None):
    for rel, text in files.items():
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in execs:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel, mode in modes:
        os.chmod(os.path.join(root, rel), mode)
    if mtime is not None:
        pin_mtime(root, mtime)


def pin_mtime(root, mtime):
    """Set the same epoch on every file and directory, deepest first."""
    paths = []
    for base, dirs, files in os.walk(root):
        for n in files:
            paths.append(os.path.join(base, n))
        paths.append(base)
    for p in paths:
        try:
            os.utime(p, ns=(int(mtime * 1e9), int(mtime * 1e9)), follow_symlinks=False)
        except OSError:
            pass


def case_env(files, root, extra=None):
    """The round-47 counter's case_env: HOME, PATH, XDG_CACHE_HOME, LANG, then the case's own env."""
    env = {"HOME": os.path.join(root, "home"), "PATH": os.path.join(root, "bin") + ":/oracle/bin",
           "XDG_CACHE_HOME": os.path.join(root, ".rw/cache"), "LANG": "C.UTF-8"}
    for k, v in (extra or {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v.replace("$ROOT", root)
    return env


def prime(box, root, env):
    for _ in range(3):
        rc, out, err = box.run(root, env, "pin", ["--print-cmd"])
        path = os.path.join(root, ".rw/cache/xdg-terminal-exec")
        try:
            with open(path, "rb") as fh:
                data = fh.read().decode("latin-1")
        except OSError:
            continue
        if data.endswith(TERM + "\n") and data.count("\n") >= 11:
            return data
    raise SystemExit("prime failed at %s: rc=%s err=%s" % (root, rc, err[:200]))


# ----------------------------------------------------------------------------------------------- ls differential
NOFIFO = os.environ.get("LS_NOFIFO") == "1"
HASH_PROBE = ("import importlib.util,os,sys\n"
              "spec=importlib.util.spec_from_file_location('mado','/oracle/tool.py')\n"
              "m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
              "sys.stdout.write(m.gen_hash(dict(os.environ), sys.argv[1:], os.getcwd()) or '-')\n")
NAMES = ["a", "b", "Z", ".hidden", "sp ace", "quo'te", 'dq"x', "back\\slash", "tab\there", "dollar$var",
         "semi;c", "star*", "paren(x)", "e-acute-é", "nl\nline", "long" + "x" * 40, "1", "10", "2", "0"]


def _chmod_tree(p):
    try:
        os.chmod(p, 0o755)
    except OSError:
        pass
    try:
        entries = list(os.scandir(p))
    except OSError:
        return
    for e in entries:
        try:
            if e.is_dir(follow_symlinks=False):
                _chmod_tree(e.path)
        except OSError:
            pass


def rmtree_force(path):
    """rmtree that first makes every directory searchable, parents before children."""
    if not os.path.lexists(path):
        return
    _chmod_tree(path)
    shutil.rmtree(path, ignore_errors=False) if False else None
    for _ in range(4):
        try:
            shutil.rmtree(path)
            return
        except OSError:
            _chmod_tree(path)


def rand_tree(rng, root, depth=0):
    n = rng.randint(1, 7)
    for _ in range(n):
        name = rng.choice(NAMES)
        if os.path.lexists(os.path.join(root, name)):
            name = name + "-%d" % rng.randrange(1000)
        if rng.random() < 0.3 and depth < 3:
            sub = os.path.join(root, name)
            os.makedirs(sub, exist_ok=True)
            rand_tree(rng, sub, depth + 1)
            if rng.random() < 0.25:
                os.chmod(sub, rng.choice([0o444, 0o000, 0o500]))
        elif rng.random() < 0.25:
            target = rng.choice(["../a", "/nope", "missing", ".", "..", "../b"])
            try:
                os.symlink(target, os.path.join(root, name))
            except OSError:
                pass
        elif rng.random() < 0.1 and not NOFIFO:
            try:
                os.mkfifo(os.path.join(root, name))
            except OSError:
                pass
        else:
            p = os.path.join(root, name)
            size = rng.choice([0, 1, 5, 100, 4096, 123456])
            with open(p, "wb") as fh:
                fh.write(b"x" * size)
            if rng.random() < 0.2:
                os.chmod(p, rng.choice([0o000, 0o444, 0o600, 0o755, 0o4755, 0o1777 & 0o777]))


def residual_dtype(out1, out2):
    """A declared residual: fifo/socket/device letter of an entry the process cannot lstat (unsearchable dir)."""
    a, b = out1.splitlines(), out2.splitlines()
    if len(a) != len(b):
        return False
    seen = False
    for x, y in zip(a, b):
        if x == y:
            continue
        if len(x) == len(y) and x[0] in "psbc" and y[0] == "?" and x[1:] == y[1:]:
            seen = True
            continue
        return False
    return seen


def lsdiff(box, count, seed=48):
    rng = random.Random(seed)
    bad = residual = 0
    for i in range(count):
        base = os.path.join(box.work, "ls-%03d" % i)
        rmtree_force(base)
        root = os.path.join(base, "r")
        os.makedirs(root + "/.rw")
        rand_tree(rng, root)
        # a couple of operand shapes: the root, subdirs, a dangling link, a trailing slash
        ops = [root]
        subs = [os.path.join(dp, d) for dp, dns, _ in os.walk(root) for d in dns][:2]
        ops += subs
        ops.append(root + "/")
        ops.append(os.path.join(root, "missing-operand"))
        now = time.time()
        pin_mtime(root, now - rng.choice([0, 3600, 86400 * 400, 86400 * 3]))
        env = {"PATH": "/oracle/bin", "LC_ALL": "C", "LANG": "C"}
        if i % 3 == 1:
            env["TZ"] = "UTC"
        elif i % 3 == 2:
            env["TZ"] = "Asia/Tokyo"
        rc1, out1, err1 = box.run(root, env, "ls", ops)
        rc2, out2, err2 = box.run(root, env, "model", ops)
        if "bwrap:" in err1 or "bwrap:" in err2 or "Traceback" in err2:
            raise SystemExit("setup failure case %d: %r %r" % (i, err1[:200], err2[:400]))
        if out1 != out2 and residual_dtype(out1, out2):
            residual += 1
            for x, y in zip(out1.splitlines(), out2.splitlines()):
                if x != y:
                    print("  residual: ls=%r model=%r" % (x[:70], y[:70]))
            shutil.rmtree(base, ignore_errors=True)
            continue
        if out1 != out2:
            bad += 1
            print("LS MISMATCH case %d ops=%r" % (i, [o.replace(root, "$ROOT") for o in ops]))
            import difflib
            for line in list(difflib.unified_diff(out1.splitlines(True), out2.splitlines(True),
                                                  "ls", "model"))[:40]:
                print(line.rstrip("\n").replace(root, "$ROOT"))
            if bad >= 3:
                print("stopping after 3 mismatches")
                return bad
        rmtree_force(base)
    print("LSDIFF: %d/%d agree, %d known residuals (d_type of a fifo/socket/device in an unsearchable dir)"
          % (count - bad - residual, count, residual))
    return bad


def hashdiff(box, count=12, seed=7):
    """gen_hash vs `printf '4\n%s\n' "$XDG_CURRENT_DESKTOP"; ls -LRl ... | md5sum` inside the sandbox."""
    rng = random.Random(seed)
    bad = 0
    DESKS = ["Hyprland", "", "GNOME", "Hyprland:X-Cinnamon", "with space", "a:b:c"]
    for i in range(count):
        base = os.path.join(box.work, "h-%03d" % i)
        rmtree_force(base)
        root = os.path.join(base, "r")
        os.makedirs(root + "/.rw")
        rand_tree(rng, root)
        harness = None
        pin_mtime(root, 1600000000 + i * 60)
        desk = DESKS[i % len(DESKS)]
        ops = [root, root + "/"]
        subs = [os.path.join(dp, d) for dp, dns, _ in os.walk(root) for d in dns][:3]
        ops += subs
        env = {"PATH": "/oracle/bin", "LC_ALL": "C", "LANG": "C", "XDG_CURRENT_DESKTOP": desk}
        shell = ("{ printf '4\\n%s\\n' \"$XDG_CURRENT_DESKTOP\"; "
                 "LC_ALL=C LANG=C /oracle/bin/ls -LRl \"$@\" 2>/dev/null; } | /oracle/bin/md5sum")
        argv = [box.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
                "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
                "--ro-bind", BASH, "/bin/sh", "--ro-bind", BASH, "/bin/bash", "--ro-bind", box.bin, "/oracle/bin",
                "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--ro-bind", root, root,
                "--bind", root + "/.rw", root + "/.rw", "--chdir", root]
        for k in sorted(env):
            argv += ["--setenv", k, env[k]]
        argv += ["/bin/bash", "-c", shell, "hash"] + ops
        p = subprocess.run(argv, capture_output=True, env={"PATH": "/usr/bin"})
        want = p.stdout.decode().strip().splitlines()[-1].split()[0] if p.stdout.strip() else ""
        rc, out, err = box.run(root, env, "hash", ops)
        got = out.strip()
        if got != want:
            bad += 1
            print("HASH MISMATCH %d desk=%r want=%r got=%r err=%r" % (i, desk, want, got, err[:200]))
        rmtree_force(base)
    print("HASHDIFF: %d/%d agree" % (count - bad, count))
    return bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "lsdiff"
    box = Box(S)
    if cmd == "lsdiff":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        sys.exit(1 if lsdiff(box, n) else 0)
    if cmd == "hashdiff":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        sys.exit(1 if hashdiff(box, n) else 0)
