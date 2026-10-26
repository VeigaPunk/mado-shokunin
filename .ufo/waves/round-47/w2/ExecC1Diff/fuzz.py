#!/usr/bin/env python3
"""ExecC1Diff - differential fuzz of the C1 reference (L1 draft) against the pinned resolver.

Judge: the real xdg-terminal-exec v0.14.3 pin, run in the same bwrap allowlist sandbox the C1 counter uses.
Candidate: .ufo/waves/round-47/l1-draft/mado-terminal.py, run as `python3 -I tool.py print ARGS`.

Areas (grammar the frozen ctl/l1-fuzz.py does not reach): symlinks, unreadable files, NUL bytes, CR, very long
lines, repeated [Desktop Entry] groups, every Exec escape, empty/trailing-slash XDG components, XTE_* env,
--print-content / --test / unknown options, printf %b delimiters.

Every case is materialized twice (oracle tree, tool tree) so nothing the oracle leaves (its cache file) is visible
to the tool. stdout is compared as BYTES with the case root replaced by $ROOT; stderr is not compared.

Usage: fuzz.py --work DIR [--cases N] [--seed S] [--area NAME] [--jobs J] [--max-fail K] [--receipt FILE]
"""
import argparse
import copy
import hashlib
import json
import os
import random
import shutil
import stat as statmod
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.realpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PIN_PATH = os.path.join(LANE, ".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec")
REF_PATH = os.path.join(LANE, ".ufo", "waves", "round-47", "l1-draft", "mado-terminal.py")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")

TERM = ("[Desktop Entry]\nType=Application\nName={n}\nExec={n}\nCategories=System;TerminalEmulator;\n")
A = "usr/share/applications/"
B = "opt/share/applications/"
H = "home/.local/share/applications/"
L = "home/.config/xdg-terminals.list"
STD_ENV = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
           "XDG_DATA_HOME": "$ROOT/home/.local/share",
           "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share", "XDG_CURRENT_DESKTOP": "Hyprland"}


class Setup(Exception):
    pass


def pinned():
    blob = open(PIN_PATH, "rb").read()
    if hashlib.sha256(blob).hexdigest() != PIN_SHA256:
        raise Setup("pin sha256 mismatch")
    return blob


class Box:
    def __init__(self, work):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            raise Setup("bwrap missing")
        self.bin = tempfile.mkdtemp(dir=work, prefix="bin-")
        for n in EXTERNALS:
            src = shutil.which(n, path="/usr/bin")
            if not src:
                raise Setup("external %s missing" % n)
            shutil.copy(os.path.realpath(src), os.path.join(self.bin, n))
        pdir = tempfile.mkdtemp(dir=work, prefix="pin-")
        self.pin = os.path.join(pdir, "xdg-terminal-exec")
        with open(self.pin, "wb") as fh:
            fh.write(pinned())
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")
        self.python = os.path.realpath(sys.executable)
        self.tool = os.path.join(pdir, "tool.py")
        shutil.copy(REF_PATH, self.tool)
        self.runs = 0

    def argv(self, root, env, tool, args):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", rw, rw]
        if tool:
            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool, "/oracle/tool.py"]
        else:
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        a += ["--chdir", root]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if tool:
            a += ["/usr/bin/python3", "-I", "/oracle/tool.py", "print"] + args
        else:
            a += ["/oracle/xdg-terminal-exec"] + args
        return a

    def run(self, root, env, tool, args, timeout):
        self.runs += 1
        try:
            p = subprocess.run(self.argv(root, env, tool, args), capture_output=True, timeout=timeout,
                               env={"PATH": "/usr/bin"})
            return p.returncode, p.stdout
        except subprocess.TimeoutExpired:
            return 124, b""


def case_env(case, root):
    env = {}
    for k, v in case.get("env", {}).items():
        env[k] = v.replace("$ROOT", root)
    if "HOME" not in env and not case.get("no_home"):
        env["HOME"] = root + "/home"
    env["PATH"] = case.get("path", "$ROOT/bin:/oracle/bin").replace("$ROOT", root)
    env["XDG_CACHE_HOME"] = case.get("cache", "$ROOT/.rw/cache").replace("$ROOT", root)
    env["LANG"] = case.get("lang", "C.UTF-8")
    return env


def _chmod_walk(root):
    for dp, dns, fns in os.walk(root):
        for n in dns + fns:
            p = os.path.join(dp, n)
            try:
                if not os.path.islink(p):
                    os.chmod(p, 0o755)
            except OSError:
                pass


def materialize(root, case):
    for key in ("files", "dirs", "links", "modes"):
        rels = case.get(key, {})
        for rel in (rels if isinstance(rels, list) else rels):
            if rel.startswith("/") or ".." in rel.split("/"):
                raise Setup("unsafe %s path %r" % (key, rel))
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    for rel, data in case.get("files", {}).items():
        if ".." in rel.split("/") or rel.startswith("/"):
            raise Setup("unsafe path %s" % rel)
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(data, str):
            data = data.replace("$ROOT", root).encode("latin-1")
        with open(p, "wb") as fh:
            fh.write(data)
    for rel in case.get("dirs", []):
        try:
            os.makedirs(os.path.join(root, rel), exist_ok=True)
        except OSError:
            pass
    for rel, target in case.get("links", {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.lexists(p):
            try:
                os.unlink(p)
            except OSError:
                continue
        os.symlink(target.replace("$ROOT", root), p)
    for rel in case.get("exec", []):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.lexists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel, mode in case.get("modes", {}).items():
        try:
            os.chmod(os.path.join(root, os.path.normpath(rel)), mode)
        except OSError:
            pass


def judge(box, case, timeout=20):
    """Returns (ok, o_norm, t_norm)."""
    base = tempfile.mkdtemp(dir=box.work, prefix="c-")
    ro, rt = os.path.join(base, "o"), os.path.join(base, "t")
    try:
        for r in (ro, rt):
            materialize(r, case)
        args = [a.replace("$ROOT", ro) for a in case.get("args", [])]
        o_rc, o_out = box.run(ro, case_env(case, ro), False, args, timeout)
        targs = [a.replace("$ROOT", rt) for a in case.get("args", [])]
        t_rc, t_out = box.run(rt, case_env(case, rt), True, targs, timeout)
        o_norm = (o_rc, o_out.replace(ro.encode(), b"$ROOT"))
        t_norm = (t_rc, t_out.replace(rt.encode(), b"$ROOT"))
        return o_norm == t_norm, o_norm, t_norm
    finally:
        _chmod_walk(base)
        shutil.rmtree(base, ignore_errors=True)


# -------------------------------------------------------------------------------------------- case builders
def base(**kw):
    c = {"env": dict(STD_ENV), "files": {A + "foot.desktop": TERM.format(n="foot")}, "exec": ["bin/foot"],
         "args": ["--print-id"]}
    c.update(kw)
    return c


def cat(cid, area, c, declared=False, note=""):
    c["id"] = cid
    c["area"] = area
    if declared:
        c["declared"] = note or (declared if isinstance(declared, str) else "declared")
    return c


PRINTABLE = [chr(i) for i in range(32, 127)]


def area_symlink():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("sym%03d" % k[0], "symlink", c, note=note))

    # file symlink, same dir, target present
    add(base(files={A + "foot.desktop": TERM.format(n="foot"), A + "kitty.desktop": TERM.format(n="kitty")},
             links={A + "foot.desktop": "$ROOT/" + A + "kitty.desktop"}, exec=["bin/kitty"],
             args=["--print-path"]))
    # dangling symlink
    add(base(links={A + "foot.desktop": "$ROOT/nowhere.desktop"}, args=["--print-path"]))
    # symlink to a directory, named *.desktop, highest preference dir shadows a real file
    add(base(dirs=[H + "foot.desktop"], args=["--print-path"]))
    add(base(dirs=[B + "foot.desktop"], args=["--print-path"]))
    add(base(links={H + "foot.desktop": "$ROOT/" + A + "foot.desktop"}, args=["--print-path"]))
    add(base(links={H + "foot.desktop": "$ROOT/" + A}, args=["--print-path"]))
    # directory named *.desktop inside the FIRST (lowest preference) applications dir
    add(base(dirs=[A + "zzz.desktop"], args=["--print-id"]))
    # symlinked subdirectory holding an entry
    add(base(files={A + "vendor/foot.desktop": TERM.format(n="foot")},
             links={A + "lnk": "$ROOT/" + A + "vendor"}, exec=["bin/foot"], args=["--print-path"]))
    # symlink loop
    add(base(dirs=[A + "loop"], links={A + "loop/self": "$ROOT/" + A + "loop"}, args=["--print-id"]))
    add(base(dirs=[A + "loop"], links={A + "loop/self": "$ROOT/" + A}, args=["--print-id"]))
    # symlink chain
    add(base(files={A + "a1.desktop": TERM.format(n="foot"), A + "a2.desktop": TERM.format(n="foot")},
             links={A + "foot.desktop": "$ROOT/" + A + "a1.desktop", A + "a1.desktop": "$ROOT/" + A + "a2.desktop"},
             exec=["bin/foot"], args=["--print-path"]))
    # symlink to an unreadable file
    add(base(files={A + "real.desktop": TERM.format(n="foot")},
             links={A + "foot.desktop": "$ROOT/" + A + "real.desktop"},
             modes={A + "real.desktop": 0o000}, exec=["bin/foot"], args=["--print-path"]))
    # applications dir itself a symlink
    add({"env": dict(STD_ENV, XDG_DATA_HOME="$ROOT/home/.local/share"),
         "files": {"home/.local/share/realapps/foot.desktop": TERM.format(n="foot")},
         "links": {H: "$ROOT/home/.local/share/realapps"}, "exec": ["bin/foot"], "args": ["--print-path"]})
    # symlink to /dev/null named *.desktop in a high-preference dir
    add(base(links={H + "foot.desktop": "/dev/null"}, args=["--print-path"]))
    # symlink to a file in another data dir (cross-dir id)
    add(base(files={A + "real.desktop": TERM.format(n="foot")},
             links={H + "foot.desktop": "$ROOT/" + A + "real.desktop"}, exec=["bin/foot"], args=["--print-path"]))
    # symlink target with an invalid id character in its name, link name valid
    add(base(files={A + "re al.desktop": TERM.format(n="foot")},
             links={A + "foot.desktop": "$ROOT/" + A + "re al.desktop"}, exec=["bin/foot"], args=["--print-path"]))
    # random symlink fuzz
    rng = random.Random(4701)
    names = ["foot", "kitty", "xterm", "a1", "zz"]
    for i in range(500):
        files, links, dirs, execs = {}, {}, [], []
        n = rng.choice(names)
        files[A + n + ".desktop"] = TERM.format(n=n)
        execs.append("bin/" + n)
        kind = rng.randrange(8)
        d = rng.choice([A, B, H])
        tgt = rng.choice([n, "other", "sub", "..", "/dev/null", "$ROOT/" + A + n + ".desktop"])
        if kind == 0:
            links[d + "lnk.desktop"] = tgt
        elif kind == 1:
            dirs.append(d + "lnk.desktop")
        elif kind == 2:
            links[d + "lnk.desktop"] = "$ROOT/" + d + ".."
        elif kind == 3:
            files[d + "sub/inner.desktop"] = TERM.format(n=n)
            links[d + "lnk"] = "$ROOT/" + d + "sub"
        elif kind == 4:
            links[d + "self"] = "$ROOT/" + d
        elif kind == 5:
            links[d + n + ".desktop"] = "$ROOT/" + A + n + ".desktop"
        elif kind == 6:
            links[d + n + ".desktop"] = "$ROOT/" + A
        else:
            files[d + "x.desktop"] = TERM.format(n=n)
            links[d + "y.desktop"] = "$ROOT/" + d + "x.desktop"
        args = rng.choice([["--print-id"], ["--print-path"], ["--print-cmd"], ["--print-id", "--print-path"]])
        add(base(files=files, links=links, dirs=dirs, exec=execs, args=args))
    return out


def area_unreadable():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("unr%03d" % k[0], "unreadable", c, note=note))

    add(base(modes={L: 0o000}))
    add(base(files={L: "foot.desktop\n", A + "kitty.desktop": TERM.format(n="kitty")},
             modes={L: 0o000}, exec=["bin/foot", "bin/kitty"], args=["--print-id"]))
    add(base(modes={A + "foot.desktop": 0o000}, exec=["bin/foot"]))
    add(base(files={A + "a1.desktop": TERM.format(n="foot"), A + "b2.desktop": TERM.format(n="foot")},
             modes={A + "a1.desktop": 0o000}, exec=["bin/foot"], args=["--print-id"]))
    add(base(dirs=[A + "sub"], files={A + "sub/foot.desktop": TERM.format(n="foot")},
             modes={A + "sub": 0o000}, exec=["bin/foot"], args=["--print-id"]))
    add(base(dirs=[A + "sub"], files={A + "sub/foot.desktop": TERM.format(n="foot")},
             modes={A + "sub": 0o100}, exec=["bin/foot"], args=["--print-id"]))
    add(base(modes={A: 0o000}, exec=["bin/foot"]))
    add(base(modes={A: 0o100}, exec=["bin/foot"]))
    add(base(modes={"home/.config": 0o000}, files={"home/.config/xdg-terminals.list": "foot.desktop\n"}))
    add(base(modes={"bin/foot": 0o000}, exec=["bin/foot"]))
    add(base(files={A + "foot.desktop": TERM.format(n="foot", ).replace("Exec=foot", "Exec=foot\nTryExec=foot\n")},
             modes={"bin/foot": 0o644}, exec=["bin/foot"]))
    add(base(files={A + "foot.desktop": TERM.format(n="foot").replace("Exec=foot", "Exec=foot\nTryExec=bar")},
             exec=["bin/foot", "bin/bar"], modes={"bin/bar": 0o644}))
    add(base(path="$ROOT/bin:/oracle/bin", modes={"bin/foot": 0o000}, exec=["bin/foot"]))
    add(base(path="$ROOT/bin:/oracle/bin", exec=["bin/foot"]))
    # unreadable config list after a good one
    add(base(files={"etc/xdg/xdg-terminals.list": "foot.desktop\n", L: "kitty.desktop\n"},
             modes={"etc/xdg/xdg-terminals.list": 0o000}, exec=["bin/foot", "bin/kitty"]))
    # unreadable cache dir / cache file
    add(base(cache="$ROOT/.rw/nonexistent/deep", args=["--print-cmd"]))
    add(base(files={".rw/cache/xdg-terminal-exec": ""}, modes={".rw/cache": 0o500}, args=["--print-cmd"]))
    # config dir unreadable, list inside it; list in a later dir readable
    add(base(files={"etc/xdg/sub/xdg-terminals.list": "kitty.desktop\n", L: "foot.desktop\n"},
             modes={"etc/xdg/sub": 0o000}, exec=["bin/foot", "bin/kitty"]))
    add(base(files={"etc/xdg/xdg-terminals.list": "kitty.desktop\n", L: "foot.desktop\n"},
             modes={"etc/xdg/xdg-terminals.list": 0o000}, exec=["bin/foot", "bin/kitty"]))
    # entry listed explicitly and unreadable, followed by a valid entry (keys carry over or not)
    add(base(files={A + "a1.desktop": TERM.format(n="foot"), A + "b2.desktop": TERM.format(n="foot"),
                    L: "a1.desktop\nb2.desktop\n"}, modes={A + "a1.desktop": 0o000}, exec=["bin/foot"]))
    add(base(files={A + "a1.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\n",
                    A + "b2.desktop": TERM.format(n="foot"), L: "a1.desktop\nb2.desktop\n"},
             modes={A + "a1.desktop": 0o000}, exec=["bin/foot"]))
    # TryExec at an unreadable executable
    add(base(files={A + "foot.desktop": TERM.format(n="foot").replace("Exec=foot", "Exec=foot\nTryExec=bar")},
             exec=["bin/foot", "bin/bar"], modes={"bin/bar": 0o644}))
    add(base(files={A + "foot.desktop": TERM.format(n="foot").replace("Exec=foot", "Exec=foot\nTryExec=$ROOT/bin/bar")},
             exec=["bin/foot", "bin/bar"], modes={"bin/bar": 0o000}))
    # PATH holding an unreadable directory first, then the real bin
    add(base(path="$ROOT/locked:$ROOT/bin:/oracle/bin", dirs=["locked"], exec=["bin/foot"]))
    # applications dir unreadable while another holds a valid entry
    add(base(modes={B: 0o000}, exec=["bin/foot"]))
    add(base(modes={H: 0o000}, exec=["bin/foot"]))
    # list is a symlink to an unreadable file
    add(base(files={"home/.config/real.list": "foot.desktop\n"},
             links={L: "$ROOT/home/.config/real.list"}, modes={"home/.config/real.list": 0o000}))
    # list is a symlink to a directory
    add(base(dirs=["home/.config/d"], links={L: "$ROOT/home/.config/d"}))
    return out


def area_nul():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("nul%03d" % k[0], "nul", c, note=note))

    add(base(files={L: b"foot.desktop\x00\n"}))
    add(base(files={L: b"\x00foot.desktop\n"}))
    add(base(files={L: b"foot\x00.desktop\n"}))
    add(base(files={L: b"foo\x00t.desktop\x00\n\x00"}))
    add(base(files={L: b"#\x00 comment\nfoot.desktop\n"}))
    add(base(files={L: b"/enable\x00_cache\nfoot.desktop\n"}))
    add(base(files={L: b"/execarg_default:foot.desktop:-x\x00\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\x00\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\x00\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=fo\x00ot\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n",
                    L: b"foot.desktop\n"}, args=["--print-content"]))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\n\x00\nExec=foot\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": b"\x00[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\x00\x00\n"}))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"},
             args=["--print-content"]))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nName=a\x00b\n"},
             args=["--print-content"]))
    add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"},
             args=["--print-cmd", "--print-delimiter=\\0"]))
    # NUL at every position of a list line and of an Exec value
    line = b"foot.desktop"
    for i in range(len(line) + 1):
        add(base(files={L: line[:i] + b"\x00" + line[i:] + b"\n"}))
    ex = b"foot --a %U"
    for i in range(len(ex) + 1):
        add(base(files={A + "foot.desktop": b"[Desktop Entry]\nExec=" + ex[:i] + b"\x00" + ex[i:] +
                        b"\nCategories=TerminalEmulator;\n"}, args=["--print-cmd"]))
    return out


def area_cr():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("cr%03d" % k[0], "cr", c, note=note))

    add(base(files={L: "foot.desktop\r\n"}))
    add(base(files={L: "\rfoot.desktop\n"}))
    add(base(files={L: "foot.desktop\n\r\n"}))
    add(base(files={L: "/enable_cache\r\nfoot.desktop\n"}))
    add(base(files={L: "/execarg_compat\r\nfoot.desktop\n"}))
    add(base(files={L: "-foot.desktop\r\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\r\nExec=foot\r\nCategories=TerminalEmulator;\r\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\r\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foo\rt\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=\"foo\rt\"\nCategories=TerminalEmulator;\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\r\nCategories=TerminalEmulator;\r\n"},
             args=["--print-content"]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nName=a\rb\n"},
             args=["--print-content"]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"},
             args=["--print-cmd", "--print-delimiter=\\r"]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"},
             args=["--print-cmd=\\r", "--", "x"]))
    add(base(files={L: "foot.desktop\r"}))
    add(base(files={L: "foot.desktop:act\r\n",
                    A + "foot.desktop": TERM.format(n="foot") + "Actions=act;\n[Desktop Action act]\nExec=foot\n"},
             args=["--print-id"]))
    # CR at every position of a list line and of an Exec value
    for i in range(len("foot.desktop") + 1):
        add(base(files={L: "foot.desktop"[:i] + "\r" + "foot.desktop"[i:] + "\n"}))
    for i in range(len("foot --a") + 1):
        v = "foot --a"[:i] + "\r" + "foot --a"[i:]
        add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=" + v +
                        "\nCategories=TerminalEmulator;\n"}, args=["--print-cmd"]))
    return out


def area_longline():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("lng%03d" % k[0], "longline", c, note=note))

    for n in (4096, 65536):
        add(base(files={A + "foot.desktop": "[Desktop Entry]\n#" + "c" * n + "\nExec=foot\n"
                        "Categories=TerminalEmulator;\n"}))
        add(base(files={L: "foot.desktop\n" + "#" + "c" * n + "\n"}))
        add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nName=" +
                        "n" * n + "\n"}, args=["--print-content"]))
        add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot \"" + "a" * n + "\"\n"
                        "Categories=TerminalEmulator;\n"}, args=["--print-cmd"]))
        add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n" +
                        "X" * n + "\n"}))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=" + "f" * 65536 + "\n"
                    "Categories=TerminalEmulator;\n"}, exec=["bin/" + "f" * 200]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot " + " %U" * 2000 + "\n"
                    "Categories=TerminalEmulator;\n"}, args=["--print-cmd"]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot " + " " * 1024 + "%U\n"
                    "Categories=TerminalEmulator;\n"}, args=["--print-cmd"]))
    add(base(files={A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"},
             args=["--print-cmd", "--print-delimiter=" + "d" * 65536, "--print-id"]))
    return out


def area_groups():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("grp%03d" % k[0], "groups", c, note=note))

    e = A + "foot.desktop"
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Entry]\nExec=foot\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\n[Desktop Entry]\nCategories=TerminalEmulator;\n"}))
    add(base(files={e: "[Desktop Entry]\nCategories=TerminalEmulator;\n[Desktop Entry]\nExec=foot\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Entry]\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Entry]x\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Entry] junk\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[desktop entry]\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Action ]\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Action ]\nExec=foot\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Action act]\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nActions=act;\n"
                    "[Desktop Action act]\nExec=foot\n[Desktop Action act]\nExec=foot\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nActions=act;\n"
                    "[Desktop Action act]\nExec=foot\n[Other]\n[Desktop Entry]\nExec=foot\n"}))
    add(base(files={e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n"
                    "Categories=TerminalEmulator;\n[Desktop Entry]\n"}))
    add(base(files={e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n"
                    "Categories=TerminalEmulator;\n[Desktop Entry]\n"}, args=["--print-id"]))
    add(base(files={e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n"
                    "Categories=TerminalEmulator;\n"}, files2=None, args=["--print-id"]))
    add(base(files={e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n"
                    "Categories=TerminalEmulator;\n[Other]\n"}, args=["--print-id"]))
    add(base(files={L: "foot.desktop:act\n",
                    e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\nActions=act;\n"
                       "[Desktop Action act]\nExec=foot\n[Desktop Entry]\nExec=foot\n"},
             args=["--print-id", "--print-cmd"]))
    add(base(files={L: "foot.desktop:act\n",
                    e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n"
                       "Categories=TerminalEmulator;\n[Desktop Action act]\nExec=other\n"},
             exec=["bin/foot", "bin/other"], args=["--print-cmd"]))
    # repeated headers with an action, key after the second header
    add(base(files={L: "foot.desktop:act\n",
                    e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n[Desktop Entry]\n"
                       "Categories=TerminalEmulator;\n"}, args=["--print-id"]))
    # [Desktop Entry] as the very last line, with and without an action
    add(base(files={L: "foot.desktop:act\n", e: "[Desktop Entry]\nActions=act;\n"
                                                 "[Desktop Action act]\nExec=foot\n[Desktop Entry]\n"}))
    add(base(files={L: "foot.desktop:act\n", e: "Categories=TerminalEmulator;\n"
                                                 "[Desktop Action act]\nExec=foot\n[Desktop Entry]\n"}))
    # an empty group name and a bracket line at EOF
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[]\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[\n"}))
    add(base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Action act\n"}))
    # a second [Desktop Entry] header at every position of a 5-line body, with and without an action
    body = ["Categories=TerminalEmulator;", "Exec=foot", "Name=foot", "[Other]", "Type=Application"]
    for i in range(len(body) + 1):
        lines = body[:i] + ["[Desktop Entry]"] + body[i:]
        add(base(files={e: "[Desktop Entry]\n" + "\n".join(lines) + "\n"}, args=["--print-id"]))
        add(base(files={L: "foot.desktop:act\n",
                        e: "[Desktop Entry]\nActions=act;\n[Desktop Action act]\nExec=foot\n" +
                           "\n".join(lines) + "\n"}, args=["--print-id"]))
    return out


def area_escape():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("esc%03d" % k[0], "escape", c, note=note))

    e = A + "foot.desktop"

    def with_exec(ex):
        return base(files={e: "[Desktop Entry]\nExec=" + ex + "\nCategories=TerminalEmulator;\n"},
                    args=["--print-cmd"])

    def with_key(key, val):
        return base(files={e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n" + key + "=" + val + "\n"},
                    args=["--print-cmd", "--", "x"])

    # de_expand_str + tokenizer: every printable char after one backslash, unquoted and quoted
    for ch in PRINTABLE:
        add(with_exec("foot\\" + ch))
        add(with_exec("foot \"\\" + ch + "\""))
        add(with_exec("foot \\\\" + ch))
        add(with_exec("foot \"\\\\" + ch + "\""))
    # trailing backslash forms
    for ex in ("foot\\", "foot \"\\", "foot \\\\", "foot \"\\\\\"", "foot \"a\\\\\"", "foot a\\ b",
               "foot\\\t", "foot\\\n", "foot \\", "\\foot", "\"\\foot\""):
        add(with_exec(ex))
    # every TerminalArg* value through de_expand_str only
    for key in ("X-TerminalArgExec", "TerminalArgExec", "X-TerminalArgDir", "TerminalArgDir", "X-TerminalArgTitle",
                "TerminalArgTitle", "X-TerminalArgAppId", "TerminalArgAppId", "X-TerminalArgHold", "TerminalArgHold",
                "TryExec", "ExecArg", "X-ExecArg"):
        for ch in PRINTABLE[::3]:
            add(with_key(key, "v\\" + ch))
    # field codes, every one, alone and inside a word
    for f in "fFuUdDnNvmick":
        add(with_exec("foot %" + f))
        add(with_exec("foot a%" + f + "b"))
        add(with_exec("foot %%" + f))
        add(with_exec("foot \"%" + f + "\""))
    for ex in ("foot %", "foot %x", "foot a%", "foot %%", "foot %%%", "foot %%%%", "foot %f %f", "foot %u %U",
               "foot %f %u", "foot %i %c %d", "foot %n%N%v%m", "foot 100%% done", "foot %%f", "foot \"%\"",
               "foot %F%U", "foot %f%u", "foot a%%b", "foot %k", "foot \"a %f\"", "foot %%%f"):
        add(with_exec(ex))
    # escape + field interaction
    for ex in ("foot \\s%f", "foot \\t%U", "foot \\\\%f", "foot \"\\\\%f\"", "foot \\%%f", "foot \\n%f"):
        add(with_exec(ex))
    return out


def area_xdg():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("xdg%03d" % k[0], "xdg", c, note=note))

    def env(**kw):
        e = dict(STD_ENV)
        for kk, vv in kw.items():
            if vv is None:
                e.pop(kk, None)
            else:
                e[kk] = vv
        return e

    files = {A + "foot.desktop": TERM.format(n="foot"), "home/.local/share/applications/foot.desktop":
             TERM.format(n="foot"), "etc/xdg/xdg-terminals.list": "foot.desktop\n",
             "home/.config/xdg-terminals.list": "foot.desktop\n"}
    cases = [
        dict(XDG_CONFIG_HOME=""), dict(XDG_CONFIG_HOME=None), dict(XDG_CONFIG_DIRS=""),
        dict(XDG_CONFIG_DIRS=None), dict(XDG_DATA_HOME=""), dict(XDG_DATA_HOME=None), dict(XDG_DATA_DIRS=""),
        dict(XDG_DATA_DIRS=None),
        dict(XDG_CONFIG_HOME="$ROOT/home/.config/"), dict(XDG_CONFIG_HOME="$ROOT/home/.config//"),
        dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg/"), dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg//"),
        dict(XDG_DATA_HOME="$ROOT/home/.local/share/"), dict(XDG_DATA_HOME="$ROOT/home/.local/share//"),
        dict(XDG_DATA_DIRS="$ROOT/opt/share/:$ROOT/usr/share/"),
        dict(XDG_DATA_DIRS="$ROOT/opt/share//:$ROOT/usr/share//"),
        dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg:"), dict(XDG_CONFIG_DIRS=":$ROOT/etc/xdg"),
        dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg::$ROOT/etc/other"),
        dict(XDG_DATA_DIRS="$ROOT/opt/share::$ROOT/usr/share"),
        dict(XDG_DATA_DIRS="::$ROOT/usr/share"), dict(XDG_DATA_DIRS="$ROOT/usr/share::"),
        dict(XDG_DATA_DIRS=":"), dict(XDG_DATA_DIRS="::"), dict(XDG_CONFIG_DIRS=":"),
        dict(XDG_DATA_HOME="$ROOT/home/.local/share", XDG_DATA_DIRS="$ROOT/usr/share"),
        dict(XDG_DATA_DIRS="$ROOT/usr/share/."), dict(XDG_DATA_DIRS="$ROOT/opt/share/../share"),
        dict(XDG_CONFIG_HOME="."), dict(XDG_DATA_DIRS="."), dict(XDG_DATA_HOME="."),
        dict(XDG_CONFIG_HOME="$ROOT/home/.config", XDG_CONFIG_DIRS="$ROOT/home/.config"),
        dict(XDG_DATA_DIRS="$ROOT/opt/share:$ROOT/opt/share"),
        dict(XDG_CURRENT_DESKTOP="Hyprland:"), dict(XDG_CURRENT_DESKTOP=":Hyprland"),
        dict(XDG_CURRENT_DESKTOP="Hyprland::GNOME"), dict(XDG_CURRENT_DESKTOP=""),
        dict(XDG_CURRENT_DESKTOP="HYPRLAND"), dict(XDG_CURRENT_DESKTOP="hyprland"),
        dict(XDG_CURRENT_DESKTOP="Hyprland\n"), dict(XDG_CURRENT_DESKTOP="Hyprland\n\n"),
        dict(XDG_CURRENT_DESKTOP="\nHyprland"),
    ]
    for i, kw in enumerate(cases):
        add(base(env=env(**kw), files=files, exec=["bin/foot"], args=["--print-path"]))
        add(base(env=env(**kw), files=files, exec=["bin/foot"], args=["--print-id"]))
    # desktop-prefixed list names under empty components / trailing slashes
    files2 = dict(files)
    files2["home/.config/hyprland-xdg-terminals.list"] = "kitty.desktop\n"
    files2[A + "kitty.desktop"] = TERM.format(n="kitty")
    for kw in (dict(XDG_CONFIG_HOME="$ROOT/home/.config/"), dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg/"),
               dict(XDG_CONFIG_HOME=""), dict(XDG_CONFIG_DIRS=""), dict(XDG_CONFIG_DIRS="$ROOT/etc/xdg:")):
        add(base(env=env(**kw), files=files2, exec=["bin/foot", "bin/kitty"], args=["--print-id"]))
    # HOME itself with a trailing slash and a doubled slash
    for h in ("$ROOT/home/", "$ROOT/home//", "$ROOT//home"):
        e = dict(STD_ENV, HOME=h)
        e.pop("XDG_CONFIG_HOME")
        e.pop("XDG_DATA_HOME")
        add({"env": e, "files": {"home/.config/xdg-terminals.list": "foot.desktop\n",
                                 "home/.local/share/applications/foot.desktop": TERM.format(n="foot")},
             "exec": ["bin/foot"], "args": ["--print-path"]})
    # relative XDG components resolve against the working directory
    add({"env": dict(STD_ENV, XDG_CONFIG_HOME="."), "files": {"xdg-terminals.list": "foot.desktop\n",
         A + "foot.desktop": TERM.format(n="foot")}, "exec": ["bin/foot"], "args": ["--print-id"]})
    add({"env": dict(STD_ENV, XDG_DATA_HOME="."), "files": {"applications/foot.desktop": TERM.format(n="foot")},
         "exec": ["bin/foot"], "args": ["--print-path"]})
    add({"env": dict(STD_ENV, XDG_DATA_DIRS="."), "files": {"applications/foot.desktop": TERM.format(n="foot")},
         "exec": ["bin/foot"], "args": ["--print-path"]})
    add({"env": dict(STD_ENV, XDG_CONFIG_HOME="home/.config", XDG_DATA_HOME="home/.local/share"),
         "files": {"home/.config/xdg-terminals.list": "foot.desktop\n",
                   "home/.local/share/applications/foot.desktop": TERM.format(n="foot")},
         "exec": ["bin/foot"], "args": ["--print-path"]})
    add({"env": dict(STD_ENV, HOME="home"), "files": {"home/.config/xdg-terminals.list": "foot.desktop\n",
         "home/.local/share/applications/foot.desktop": TERM.format(n="foot")}, "exec": ["bin/foot"],
         "args": ["--print-path"]})
    # XDG dirs with a colon inside a default (HOME unset)
    add({"env": {"XDG_CONFIG_DIRS": "$ROOT/etc/xdg", "XDG_DATA_DIRS": "$ROOT/usr/share",
                 "XDG_CURRENT_DESKTOP": "Hyprland"},
         "files": files, "exec": ["bin/foot"], "args": ["--print-id"], "no_home": True}, note="HOME unset")
    return out


def area_xte():
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("xte%03d" % k[0], "xte_env", c, note=note))

    e = A + "foot.desktop"
    plain = {e: TERM.format(n="foot")}
    witharg = {e: TERM.format(n="foot") + "TerminalArgExec=--exec\n"}
    withx = {e: TERM.format(n="foot") + "X-ExecArg=--x\n"}
    noexec = {e: "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;\n"}
    vals = ["true", "True", "TRUE", "yes", "Yes", "YES", "1", "false", "False", "FALSE", "no", "No", "NO", "0",
            "", "garbage", "TRUE ", " true", "2"]
    for v in vals:
        add(base(env=dict(STD_ENV, XTE_EXECARG_COMPAT=v), files=plain, exec=["bin/foot"],
                 args=["--print-cmd", "--", "x"]))
        add(base(env=dict(STD_ENV, XTE_EXECARG_COMPAT=v), files=withx, exec=["bin/foot"],
                 args=["--print-cmd", "--", "x"]))
        add(base(env=dict(STD_ENV, XTE_EXECARG_COMPAT=v), files=noexec, exec=["bin/foot"],
                 args=["--print-cmd", "--", "x"]))
        add(base(env=dict(STD_ENV, XTE_CACHE_ENABLED=v), files=plain, exec=["bin/foot"], args=["--print-id"]))
        add(base(env=dict(STD_ENV, XTE_CACHE_ENABLED=v), files=plain, exec=["bin/foot"],
                 args=["--print-cmd", "--", "x"]))
    # directives vs env (the env sets the configured flag)
    lists = {"/execarg_compat\n": "compat", "/execarg_strict\n": "strict", "/enable_cache\n": "enable",
             "/disable_cache\n": "disable"}
    for line, tag in lists.items():
        for v in ("true", "false", ""):
            add(base(env=dict(STD_ENV, XTE_EXECARG_COMPAT=v), files=dict(withx, **{L: line}),
                     exec=["bin/foot"], args=["--print-cmd", "--", "x"]))
            add(base(env=dict(STD_ENV, XTE_CACHE_ENABLED=v), files=dict(plain, **{L: line}),
                     exec=["bin/foot"], args=["--print-cmd", "--", "x"]))
    # both directives present, env absent
    add(base(files=dict(withx, **{L: "/execarg_compat\n/execarg_strict\n"}), exec=["bin/foot"],
             args=["--print-cmd", "--", "x"]))
    add(base(files=dict(withx, **{L: "/execarg_strict\n/execarg_compat\n"}), exec=["bin/foot"],
             args=["--print-cmd", "--", "x"]))
    # /execarg_default in strict mode, and repeated defaults
    for line in ("/execarg_default:foot.desktop:-z\n", "/execarg_default:foot.desktop:-z\n"
                 "/execarg_default:foot.desktop:-y\n", "/execarg_strict\n/execarg_default:foot.desktop:-z\n"):
        add(base(files=dict(plain, **{L: line}), exec=["bin/foot"], args=["--print-cmd", "--", "x"]))
        add(base(env=dict(STD_ENV, XTE_EXECARG_COMPAT="false"), files=dict(plain, **{L: line}),
                 exec=["bin/foot"], args=["--print-cmd", "--", "x"]))
    return out


def area_print():
    out = []
    k = [0]

    def add(c, note="", declared=False):
        k[0] += 1
        out.append(cat("prn%03d" % k[0], "print", c, note=note, declared=declared))

    e = A + "foot.desktop"
    entry = ("[Desktop Entry]\nType=Application\nName=foot\nExec=foot --a %U\nCategories=System;TerminalEmulator;\n"
             "X-TerminalArgDir=--working-directory=\nX-TerminalArgTitle=--title\nX-TerminalArgAppId=--class=\n"
             "X-TerminalArgHold=--hold\nActions=act;\n[Desktop Action act]\nExec=footclient\n")
    files = {e: entry, L: "foot.desktop\n"}
    execs = ["bin/foot", "bin/footclient"]
    argvs = [
        ["--print-content"], ["--print-content", "--print-id"], ["--print-content", "--print-path"],
        ["--print-content", "--print-id", "--print-path", "--print-delimiter=|"],
        ["--print-content", "--print-cmd"], ["--print-content", "--test"],
        ["--print-content", "--test", "--", "x"], ["--print-id", "--print-content"],
        ["--test"], ["--test", "--", "ls"], ["--test", "-e", "ls"], ["--test", "--print-id"],
        ["--test", "--print-id", "--print-cmd"], ["--test", "--print-cmd", "--", "a", "b"],
        ["--test", "--print-path", "--print-delimiter=\\t"],
        ["--print-id", "--unknown"], ["--unknown", "--print-id"], ["-x", "--print-id"],
        ["--print-idd", "--print-id"], ["--print-id=x", "--print-id"], ["--app-id", "--print-id"],
        ["--dir", "--print-id"], ["--print-delimiter", "--print-id"], ["--print-cmd", "--print-cmdx"],
        ["--print-id", "--print-delimiter=|", "--print-path"],
        ["--print-id", "--print-delimiter=", "--print-path"],
        ["--print-id", "--print-delimiter=\\n\\n", "--print-path"],
        ["--print-id", "--print-delimiter=\\c", "--print-path"],
        ["--print-id", "--print-delimiter=a\\cb", "--print-path"],
        ["--print-cmd=\\t", "--", "a", "b"], ["--print-cmd=", "--", "a"],
        ["--print-cmd=\\c", "--", "a", "b"], ["--print-cmd=a\\cb", "--", "a", "b"],
        ["--print-cmd=\\101", "--", "a"], ["--print-cmd=\\x41", "--", "a"],
        ["--print-id", "--print-path", "--print-content", "--print-cmd"],
        ["--print-cmd", "--", "--print-id"], ["--print-id", "--", "--print-path"],
        ["--print-id", "-e"], ["--print-id", "--print-cmd", "-e", "x"],
        ["--app-id=a=b", "--print-cmd"], ["--title=a=b", "--print-cmd"], ["--dir=a=b", "--print-cmd"],
        ["--app-id=", "--print-cmd"], ["--hold", "--print-cmd"],
        ["--hold", "--dir=/srv", "--title=t", "--app-id=z", "--print-cmd"],
        ["--dir=/srv", "--print-cmd", "--", "x"], ["--print-cmd", "--dir=/srv", "--", "x"],
        ["--print-id", "--print-path", "--print-delimiter=%s"],
        ["--print-id", "--print-delimiter=\\0", "--print-path"],
        ["--print-id", "--print-delimiter=\\x", "--print-path"],
        ["--print-id", "--print-delimiter=\\u0041", "--print-path"],
        ["--print-id", "--print-delimiter=\\u004", "--print-path"],
        ["--print-id", "--print-delimiter=\\777", "--print-path"],
        ["--print-id", "--print-delimiter=\\08", "--print-path"],
        ["--print-id", "--print-delimiter=\\e[1m", "--print-path"],
        ["--print-id", "--print-delimiter=\\\\", "--print-path"],
        ["--print-id", "--print-delimiter=\\z", "--print-path"],
        ["--print-id", "--print-delimiter=\\%", "--print-path"],
        ["--print-id", "--print-delimiter=\\a\\b\\f\\v", "--print-path"],
    ]
    for a in argvs:
        add(base(files=files, exec=execs, args=a))
        add(base(files=files, exec=execs, args=a + ["--", "top"]) if a[-1] != "--" else
            base(files=files, exec=execs, args=a))
    # every printable escape as a delimiter, id+path and cmd modes
    for ch in PRINTABLE:
        add(base(files=files, exec=execs, args=["--print-id", "--print-delimiter=\\" + ch, "--print-path"]))
        add(base(files=files, exec=execs, args=["--print-cmd=\\" + ch, "--", "a", "b"]))
    # octal / hex / unicode delimiter families
    for seq in ("\\0", "\\00", "\\000", "\\0000", "\\1", "\\12", "\\123", "\\1234", "\\7", "\\77", "\\377",
                "\\400", "\\x", "\\x0", "\\x00", "\\x41", "\\x4", "\\x414", "\\u", "\\u0", "\\u00", "\\u0041",
                "\\u004", "\\U00000041", "\\U0000004", "\\U", "\\c", "a\\cb", "\\c\\n"):
        add(base(files=files, exec=execs, args=["--print-id", "--print-delimiter=" + seq, "--print-path"]))
    # declared: no print option and no --test -> the resolver launches a terminal (tool refuses with 2)
    add(base(files=files, exec=execs, args=["--print-idd"]), declared="no print option: resolver execs the entry")
    add(base(files=files, exec=execs, args=["--test=x"]), declared="no print option: resolver execs the entry")
    add(base(files=files, exec=execs, args=["--hold"]), declared="no print option: resolver execs the entry")
    # declared: -h/--help
    add(base(files=files, exec=execs, args=["-h"]), declared="-h/--help out of contract")
    add(base(files=files, exec=execs, args=["--help", "--print-id"]), declared="-h/--help out of contract")
    return out


def area_mixed():
    out = []
    rng = random.Random(4747)
    names = ["foot", "kitty", "alacritty", "xterm", "wezterm", "ghostty"]
    keys = ["Type=Application", "Categories=TerminalEmulator;", "Categories=System;TerminalEmulator",
            "Categories=", "Hidden=true", "Hidden=True", "TryExec={n}", "TryExec=-p", "TryExec=--",
            "OnlyShowIn=GNOME;", "NotShowIn=Hyprland;", "X-TerminalArgExec=-x", "TerminalArgExec=",
            "X-ExecArg=--", "ExecArg=-e", "X-TerminalArgDir=--working-directory=", "TerminalArgTitle=-T=",
            "X-TerminalArgAppId=--class=", "X-TerminalArgHold=--hold", "Actions=act;", "Exec={n}",
            "Exec={n} --a %U", "Exec=\"{n}\" \"b c\" 100%%", "Exec={n} %f %u", "Exec={n} $HOME",
            "Exec={n} 'q'", "Exec={n}\\s-x", "Exec=-p", "Exec=--", "Exec={n} \"a\\\\\"b\"", "Exec=env {n}",
            "Exec={n} %", "Exec={n} %i %d", "# c", "", "  Exec = {n}", "Name=X", "Exec[de]={n}x"]
    groups = ["[Desktop Entry]", "[Desktop Entry]", "[Desktop Entry]x", "[Desktop Action act]", "[Other]",
              "[Desktop Action ]", "[desktop entry]"]
    listl = ["{id}", "{id}:act", "{id}:", "-{id}", "+{id}", "{n}", "# c", "", "  {id}  ", "/execarg_strict",
             "/execarg_compat", "/execarg_default:{id}:-z", "/enable_cache", "/disable_cache", "{id}\r", "\t{id}"]
    dirs = [A, B, H]
    argvs = [["--print-id"], ["--print-path"], ["--print-cmd"], ["--print-content"],
             ["--print-id", "--print-path", "--print-cmd"], ["--test"], ["--print-cmd", "--", "htop", "-d", "5"],
             ["--print-content", "--print-cmd"], ["--print-id", "--print-delimiter=\\t", "--print-path"],
             ["--test", "--print-id"], ["--print-cmd=\\t", "x"], ["--print-content", "--print-id"]]
    for i in range(1300):
        files, execs, dirs_, links, modes = {}, [], [], {}, {}
        used = set()
        ids = []
        for _ in range(rng.randint(1, 3)):
            n = rng.choice(names)
            sub = rng.choice(["", "", "vendor/"])
            eid = sub.replace("/", "-") + n + ".desktop"
            lines = []
            if rng.random() < 0.2:
                lines.append(rng.choice(["# lead", "Exec=" + n]))
            lines.append(rng.choice(groups))
            if rng.random() < 0.85:
                lines.append("Categories=TerminalEmulator;")
            if rng.random() < 0.8:
                lines.append("Exec=" + n)
            for _ in range(rng.randint(0, 4)):
                lines.append(rng.choice(keys).replace("{n}", n))
                if rng.random() < 0.25:
                    lines.append(rng.choice(groups))
            text = "\n".join(lines)
            if rng.random() < 0.9:
                text += "\n"
            if rng.random() < 0.1:
                text = text.replace("\n", "\r\n")
            if rng.random() < 0.1:
                text = text.replace("Exec=", "Ex\x00ec=", 1)
            d = rng.choice(dirs)
            rel = d + sub + n + ".desktop"
            if rel in used:
                continue
            used.add(rel)
            if rng.random() < 0.12:
                dirs_.append(rel)
            elif rng.random() < 0.1:
                links[rel] = rng.choice(["$ROOT/" + d + "other.desktop", "$ROOT/" + d, "/dev/null",
                                         "$ROOT/nowhere"])
            else:
                files[rel] = text
            ids.append(eid)
        for n in names:
            if rng.random() < 0.5:
                execs.append("bin/" + n)
            if rng.random() < 0.2:
                execs.append("bin/" + n + "client")
        if ids and rng.random() < 0.5:
            ls = [rng.choice(listl).replace("{id}", rng.choice(ids)).replace("{n}", rng.choice(names))
                  for _ in range(rng.randint(1, 4))]
            files[L] = "\n".join(ls) + ("\n" if rng.random() < 0.9 else "")
        if rng.random() < 0.15:
            files[L] = files.get(L, "") + "\x00"
        if rng.random() < 0.12 and (files or dirs_ or links):
            modes[rng.choice(list(files) + list(dirs_) + list(links))] = 0o000
        env = dict(STD_ENV)
        if rng.random() < 0.15:
            env["XDG_DATA_DIRS"] = "$ROOT/opt/share/:$ROOT/usr/share//"
        if rng.random() < 0.1:
            env["XDG_CONFIG_DIRS"] = ""
        if rng.random() < 0.1:
            env.pop("XDG_DATA_HOME")
        if rng.random() < 0.15:
            env["XTE_EXECARG_COMPAT"] = rng.choice(vals_compat)
        if rng.random() < 0.1:
            env["XTE_CACHE_ENABLED"] = rng.choice(["false", "0", "garbage"])
        if rng.random() < 0.1:
            env["XDG_CURRENT_DESKTOP"] = rng.choice(["Hyprland", "", "GNOME:Hyprland", "hyprland", "KDE"])
        out.append(cat("mix%03d" % i, "mixed", {"env": env, "files": files, "dirs": dirs_, "links": links,
                                                "modes": modes, "exec": execs, "args": rng.choice(argvs)}))
    return out


vals_compat = ["true", "false", "", "garbage", "1", "0"]


def area_cmdv():
    """command -v with option-like names: bash's `command` builtin parses -p/-v/-V/-- as its own options."""
    out = []
    k = [0]

    def add(c, note=""):
        k[0] += 1
        out.append(cat("cmdv%03d" % k[0], "cmdv", c, note=note))

    e = A + "p.desktop"

    def entry(line):
        return {e: "[Desktop Entry]\nType=Application\nName=p\n" + line + "\nCategories=System;TerminalEmulator;\n"}

    for ex in ("-p", "-v", "-V", "--", "-pv", "-pV", "-vp", "-x", "-q", "--foo", "-", "-p ", " -p", "p"):
        add(base(files=entry("Exec=" + ex), exec=["bin/p"], args=["--print-id"]))
        add(base(files=entry("Exec=" + ex), exec=["bin/p"], args=["--print-cmd"]))
    for te in ("-p", "-v", "-V", "--", "-x", "-", "-pv", "p"):
        add(base(files=entry("Exec=p\nTryExec=" + te), exec=["bin/p"], args=["--print-id"]))
    # a path containing '/' that is an executable non-directory, and one that is a directory
    add(base(files=entry("Exec=./p"), files_extra=None, exec=["p"], args=["--print-id"]))
    add(base(files=entry("Exec=./p"), dirs=["p"], args=["--print-id"]))
    add(base(files=entry("Exec=$ROOT/bin/p"), exec=["bin/p"], args=["--print-id"]))
    add(base(files=entry("Exec=$ROOT/bin"), dirs=["bin"], args=["--print-id"]))
    # builtin / keyword / function names
    for ex in ("true", "printf", "read", "command", "if", "time", "[", ":", "test", "exec", "eval", "error",
               "check_bool", "de_tokenize_exec", "find_entry", "list_contains", "reset_keys", "cd", "alias"):
        add(base(files=entry("Exec=" + ex), args=["--print-id"]))
    return out


AREAS = {"symlink": area_symlink, "unreadable": area_unreadable, "nul": area_nul, "cr": area_cr,
         "longline": area_longline, "groups": area_groups, "escape": area_escape, "xdg": area_xdg,
         "xte_env": area_xte, "print": area_print, "cmdv": area_cmdv, "mixed": area_mixed}


# -------------------------------------------------------------------------------------------- minimization
def minimize(box, case, budget=90, timeout=20):
    """Greedy delta-debugging: drop files/lines/args/env keys/execs while the disagreement holds."""
    cur = json.loads(json.dumps(case))
    ok, _, _ = judge(box, cur, timeout)
    if ok:
        return cur, False
    tries = 0

    def valid(cand):
        """A minimized case must still be a contract case: at least one print option or --test."""
        args = cand.get("args", [])
        return any(x in ("--print-id", "--print-path", "--print-content", "--print-cmd", "--test")
                   or x.startswith("--print-cmd=") for x in args)

    def attempt(cand):
        nonlocal tries
        if tries >= budget or not valid(cand):
            return False
        tries += 1
        ok2, o2, _ = judge(box, cand, timeout)
        return (not ok2) and o2[0] not in (124, 127)

    for phase in ("args", "files", "lines", "env", "exec", "modes", "links", "dirs"):
        changed = True
        while changed and tries < budget:
            changed = False
            if phase == "args":
                for i in range(len(cur.get("args", []))):
                    cand = copy.deepcopy(cur)
                    del cand["args"][i]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "files":
                for rel in list(cur.get("files", {})):
                    cand = copy.deepcopy(cur)
                    del cand["files"][rel]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "lines":
                for rel, data in list(cur.get("files", {}).items()):
                    if isinstance(data, bytes):
                        lines = data.split(b"\n")
                    else:
                        lines = data.encode("latin-1").split(b"\n")
                    if len(lines) < 2:
                        continue
                    for i in range(len(lines)):
                        cand = copy.deepcopy(cur)
                        cand["files"][rel] = b"\n".join(lines[:i] + lines[i + 1:])
                        if attempt(cand):
                            cur = cand
                            changed = True
                            break
                    if changed:
                        break
            elif phase == "env":
                for kk in list(cur.get("env", {})):
                    cand = copy.deepcopy(cur)
                    del cand["env"][kk]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "exec":
                for i in range(len(cur.get("exec", []))):
                    cand = copy.deepcopy(cur)
                    del cand["exec"][i]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "modes":
                for kk in list(cur.get("modes", {})):
                    cand = copy.deepcopy(cur)
                    del cand["modes"][kk]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "links":
                for kk in list(cur.get("links", {})):
                    cand = copy.deepcopy(cur)
                    del cand["links"][kk]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
            elif phase == "dirs":
                for i in range(len(cur.get("dirs", []))):
                    cand = copy.deepcopy(cur)
                    del cand["dirs"][i]
                    if attempt(cand):
                        cur = cand
                        changed = True
                        break
    return cur, True


def show(case):
    return json.dumps(case, indent=1, sort_keys=True, default=lambda b: b.decode("latin-1") if isinstance(b, bytes)
                      else str(b))


# -------------------------------------------------------------------------------------------- driver
def worker(args):
    wid, cases, work, timeout = args
    box = Box(work)
    out = []
    for c in cases:
        ok, o, t = judge(box, c, timeout)
        out.append((c["id"], ok, o, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--cases", type=int, default=0)
    ap.add_argument("--seed", type=int, default=4701)
    ap.add_argument("--area", default="")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--max-fail", type=int, default=12)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--receipt", default="")
    ap.add_argument("--list-areas", action="store_true")
    ap.add_argument("--no-minimize", action="store_true")
    a = ap.parse_args()
    if a.list_areas:
        print(" ".join(sorted(AREAS)))
        return 0
    if not os.path.isdir(a.work):
        raise Setup("work dir missing: %s" % a.work)
    cases = []
    for name in (a.area.split(",") if a.area else sorted(AREAS)):
        cases.extend(AREAS[name]())
    # deterministic shuffle so --cases N samples every area
    rng = random.Random(a.seed)
    rng.shuffle(cases)
    if a.cases:
        cases = cases[:a.cases]
    work = tempfile.mkdtemp(dir=a.work, prefix="run-")
    t0 = time.time()
    jobs = max(1, a.jobs)
    chunks = [cases[i::jobs] for i in range(jobs)]
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    with ctx.Pool(jobs) as pool:
        results = []
        for r in pool.imap_unordered(worker, [(i, chunks[i], work, a.timeout) for i in range(jobs)]):
            results.extend(r)
    results.sort(key=lambda r: r[0])
    dt = time.time() - t0
    fails = [r for r in results if not r[1]]
    by_area = {}
    for cid, ok, _o, _t in results:
        area = cid.rstrip("0123456789")
        by_area.setdefault(area, [0, 0])
        by_area[area][0] += 1
        by_area[area][1] += 0 if ok else 1
    lines = []
    lines.append("cases=%d agree=%d differ=%d seconds=%.1f jobs=%d" % (len(results), len(results) - len(fails),
                                                                      len(fails), dt, jobs))
    for area in sorted(by_area):
        lines.append("  area=%-12s cases=%-4d differ=%d" % (area, by_area[area][0], by_area[area][1]))
    findings = []
    seen = {}
    cls = {}
    for cid, ok, o, t in results:
        case = next(c for c in cases if c["id"] == cid)
        if ok:
            continue
        rec = {"id": cid, "area": case["area"], "declared": case.get("declared", ""),
               "oracle": [o[0], o[1].decode("latin-1")], "tool": [t[0], t[1].decode("latin-1")]}
        if 124 in (o[0], t[0]):
            rec["class"] = "timeout"
        elif o[0] == 127:
            rec["class"] = "invalid-oracle"
        elif case.get("declared"):
            rec["class"] = "declared"
        else:
            rec["class"] = "hole"
        key = (rec["area"], o[0], t[0], o[1][:80], t[1][:80])
        rec["signature"] = "%s o%d t%d %r %r" % key
        if rec["class"] == "hole" and key not in seen and not a.no_minimize and len(seen) < a.max_fail:
            seen[key] = cid
            rec["representative"] = True
            bx = Box(work)
            m, _ = minimize(bx, case, timeout=a.timeout)
            ok2, o2, t2 = judge(bx, m, a.timeout)
            rec["minimal"] = m
            rec["minimal_oracle"] = [o2[0], o2[1].decode("latin-1")]
            rec["minimal_tool"] = [t2[0], t2[1].decode("latin-1")]
            rec["minimal_still_differs"] = not ok2
        findings.append(rec)
        cls[rec["class"]] = cls.get(rec["class"], 0) + 1
        lines.append("DIFF %s area=%s class=%s%s" % (cid, rec["area"], rec["class"],
                                                     " REPRESENTATIVE" if rec.get("representative") else ""))
        oo = rec.get("minimal_oracle", rec["oracle"])
        tt = rec.get("minimal_tool", rec["tool"])
        lines.append("  oracle rc=%d out=%r" % (oo[0], oo[1][:400]))
        lines.append("  tool   rc=%d out=%r" % (tt[0], tt[1][:400]))
    holes = [r for r in findings if r["class"] == "hole"]
    lines.insert(len(by_area) + 1, "holes=%d declared=%d timeout=%d invalid=%d distinct_hole_signatures=%d" % (
        len(holes), cls.get("declared", 0), cls.get("timeout", 0), cls.get("invalid-oracle", 0), len(seen)))
    text = "\n".join(lines)
    print(text[:20000])
    if a.receipt:
        with open(a.receipt, "w") as fh:
            fh.write(text + "\n")
        with open(a.receipt + ".json", "w") as fh:
            json.dump(findings, fh, indent=1, default=lambda b: b.decode("latin-1") if isinstance(b, bytes)
                      else str(b))
    shutil.rmtree(work, ignore_errors=True)
    return 0 if not holes else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as e:
        print("SETUP %s" % e)
        sys.exit(2)
