#!/usr/bin/env python3
"""PRED-C1-r47 - tools/mado-terminal.py answers which terminal xdg-terminal-exec picks (C1, operability, capability).

Registration: .ufo/waves/round-47/registration.md. The judge is the resolver itself: the upstream script
xdg-terminal-exec v0.14.3 (https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec),
pinned as .ufo/waves/round-47/fetch/xdg-terminal-exec of this counter's lane (PIN_SHA256 below; the host's
/usr/bin/xdg-terminal-exec has the same bytes). No reference implementation of ours judges anything.

Scores one committed revision REV of --repo (revision-addressed git reads with ambient GIT_* removed; nothing in the
repository is written; scratch only under --work, which must lie outside the repository, this counter's lane and that
lane's parent directory). TOOL = tools/mado-terminal.py. TARGET_MET iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest`, run in the sandbox (TMPDIR=/tmp, a fresh tmpfs), exits 0 within 120 s and its
     last stdout line is exactly `MADO_TERMINAL_SELFTEST: N/N passed` (ASCII digits) with N >= 30.
  f  every fixture of FIXTURES (quality/counters/c1-r47-fixtures.json beside this file, pinned by FIXTURES_SHA256;
     another byte, or fewer than 100 fixtures, is a setup error) passes in two variants: A (case root
     <work>/fx-XXXX/r, LANG=C.UTF-8) and B (case root <work>/job-<hex>/deep/<hex>/r, LANG=en_US.UTF-8). Per variant
     the case is materialized TWICE, one tree for the oracle and one for the tool (identical bytes, written in the
     same order, at different roots), so nothing the oracle run leaves (its cache file) is visible to the tool.
     The oracle (the pin, `/oracle/xdg-terminal-exec ARGS`) and the tool (`python3 -I /oracle/tool.py print ARGS`)
     run in the sandbox with the case env; a variant passes when the tool's exit status equals the oracle's and its
     stdout, with its own root replaced by $ROOT, equals the oracle's stdout with the oracle's root replaced by
     $ROOT. stderr is not compared. The oracle's variant-A result must also equal the fixture's recorded `expect`;
     a fixture whose oracle result drifted from its record is a setup error (the record no longer describes this
     host's resolver, so the fixture set must be rebuilt before anything is scored).
  g  GEN = 150 cases drawn from NONCE by gen_case() below (list files at every precedence level incl. desktop-
     prefixed ones, list-line noise, actions, exclusions, directives, desktop entries with every key the resolver
     reads, broken quoting and field codes, missing final newlines, groups, subdirectory ids, duplicate ids, stub
     binaries present or not, 7 desktop strings incl. unset, 15 argument vectors), each judged like a fixture
     (variant A only) by the oracle run at count time. NONCE is --nonce (default: drawn from os.urandom and
     printed), so these cases cannot be precomputed.
  x  explain: for every fixture (variant A, fresh trees), the oracle prints `--print-id --print-path --print-cmd`
     and the tool runs `explain` (no --observed): its last `MADO_TERM:` line must carry selected= and path= equal to
     the oracle's first and second stdout lines and verdict=OK with exit 0 - or selected=- path=- verdict=NO_TERMINAL
     with exit 3 when the oracle exits 1. Then, for an oracle exit 0, the oracle's capture (root rewritten to the
     tool tree) is written under <root>/.rw/obs only after that run: `explain --observed <capture>` must print
     verdict=AGREE and exit 0, and with the first `.desktop` of the capture changed to `.desktoq` verdict=DIFFER and
     exit 1.
  i  isolation (allowlist): every run is `bwrap --unshare-all --die-with-parent --new-session --clearenv` with a
     fresh root holding only: /usr/lib (read-only), /bin/sh and /bin/bash = the host bash, /oracle/bin = copies of
     the resolver's seven external commands (tr find awk ls md5sum mkdir rm), /dev, /proc, a tmpfs /tmp, the case
     root (read-only) with its <root>/.rw (writable: XDG_CACHE_HOME) - plus, for an oracle run, the pin at
     /oracle/xdg-terminal-exec and, for a tool run, /usr/bin/python3 and the tool at /oracle/tool.py. No /usr/bin,
     /usr/share, /etc, /home, /fast, /run or /var of the host is visible. PATH=<root>/bin:/oracle/bin,
     HOME=<root>/home. bwrap or strace missing is a setup error.
  r  read-only: every tool run (selftest, fixtures, generated) is executed under
     `strace -f -qq -e trace=execve,execveat,socket,socketpair,connect -o <file outside the sandbox> bwrap ...`;
     after the line recording the execve of the sandboxed python3, any further traced event (a process started,
     a socket made or connected - by the tool or anything it forks) is a trip. readonly=ok iff trips=0 over all runs.
Final line: `PRED-C1-r47: fixtures=K/F explained=X/F generated=G/150 selftest=<ok|fail> readonly=<ok|fail> tool=<present|absent>
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> nonce=<n>`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup failure.
Clause lines `PRED-C1-r47 clause=<x> ...` precede it.
Residuals (declared): a tool that carries a model of the resolver (an emulator, or an interpreter for the embedded
script written in Python) is an implementation of it; the oracle is this host's bash, find, awk and tr at count time,
so a difference between hosts is a difference of the judge, recorded by the drift check; the cache path of the
resolver (a warm cache) and -h/--help are outside the contract; clause s is a printed line.
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

PRED = "PRED-C1-r47"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mado-terminal.py"
SELFTEST_MIN = 30
GEN = 150
MIN_FIXTURES = 100
FIXTURES_PATH = os.path.join(HERE, "c1-r47-fixtures.json")
FIXTURES_SHA256 = "4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86"
PIN_PATH = os.path.join(HERE, "..", "..", ".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


def pinned(path, sha):
    try:
        blob = open(path, "rb").read()
    except OSError:
        raise Setup("missing %s" % os.path.basename(path))
    if hashlib.sha256(blob).hexdigest() != sha:
        raise Setup("sha256 mismatch %s" % os.path.basename(path))
    return blob


def load_fixtures():
    fx = json.loads(pinned(FIXTURES_PATH, FIXTURES_SHA256).decode())
    if len(fx) < MIN_FIXTURES:
        raise Setup("fewer than %d fixtures" % MIN_FIXTURES)
    return fx


# ------------------------------------------------------------------------------------------------ sandbox
class Box:
    """Shared assets of one count: the externals, the pin, the tool, python3."""

    def __init__(self, work, tool_path=None):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        self.strace = shutil.which("strace")
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
            fh.write(pinned(PIN_PATH, PIN_SHA256))
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")
        self.python = os.path.realpath(sys.executable)
        self.tool = tool_path
        self.trips = []

    def argv(self, root, env, tool, args, tmpdir=False):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        if root:
            a += ["--ro-bind", root, root, "--bind", rw, rw]
        if tool:
            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool, "/oracle/tool.py"]
        else:
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        a += ["--chdir", root or "/tmp"]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if tool:
            a += ["/usr/bin/python3", "-I", "/oracle/tool.py"] + args
        else:
            a += ["/oracle/xdg-terminal-exec"] + args
        return a

    def run(self, root, env, tool, args, timeout=30):
        argv = self.argv(root, env, tool, args)
        trace = None
        if tool:
            fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
            os.close(fd)
            argv = [self.strace, "-f", "-qq", "-e", TRACE_SET, "-e", "signal=none", "-o", trace] + argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"))
        except subprocess.TimeoutExpired:
            res = (124, "")
        if trace:
            self.check_trace(trace)
        return res

    def check_trace(self, path):
        try:
            lines = open(path, encoding="latin-1").read().splitlines()
        except OSError:
            self.trips.append("trace-missing")
            return
        seen = False
        py_pid = None
        for ln in lines:
            pid, _, rest = ln.partition(" ")
            rest = rest.strip()
            if not seen:
                if 'execve("/usr/bin/python3"' in rest:
                    py_pid = pid
                    seen = rest.endswith("= 0")
                elif pid == py_pid and rest.startswith("<... execve resumed>"):
                    seen = rest.endswith("= 0")
                continue
            self.trips.append(rest[:60])
        if not seen:
            self.trips.append("python-execve-not-seen")
        os.unlink(path)


def materialize(root, case):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    for rel, text in case["files"].items():
        if ".." in rel.split("/") or rel.startswith("/"):
            raise Setup("unsafe path in case %s" % case.get("id"))
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in case["exec"]:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def case_env(case, root, lang):
    env = {k: v.replace("$ROOT", root) for k, v in case["env"].items()}
    env["HOME"] = os.path.join(root, "home")
    env["PATH"] = os.path.join(root, "bin") + ":/oracle/bin"
    env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    env["LANG"] = lang
    return env


def run_case(box, case, variant, rng):
    """Returns (ok, oracle_result_normalized, why)."""
    if variant == "A":
        base = tempfile.mkdtemp(dir=box.work, prefix="fx-")
        lang = "C.UTF-8"
    else:
        base = tempfile.mkdtemp(dir=box.work, prefix="job-%08x-" % rng.getrandbits(32))
        base = os.path.join(base, "deep", "%06x" % rng.getrandbits(24))
        lang = "en_US.UTF-8"
    ro, rt = os.path.join(base, "o", "r"), os.path.join(base, "t", "r")
    for r in (ro, rt):
        materialize(r, case)
    args_o = [a.replace("$ROOT", ro) for a in case["args"]]
    args_t = [a.replace("$ROOT", rt) for a in case["args"]]
    o_rc, o_out = box.run(ro, case_env(case, ro, lang), False, args_o)
    t_rc, t_out = box.run(rt, case_env(case, rt, lang), True, ["print"] + args_t)
    o_norm = (o_rc, o_out.replace(ro, "$ROOT"))
    t_norm = (t_rc, t_out.replace(rt, "$ROOT"))
    shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    ok = o_norm == t_norm
    why = "" if ok else "oracle=%r tool=%r" % ((o_norm[0], o_norm[1][:160]), (t_norm[0], t_norm[1][:160]))
    return ok, o_norm, why


def explain_case(box, case, rng):
    """Clause x: `explain` names what the oracle prints, and `explain --observed` agrees/differs both ways."""
    base = tempfile.mkdtemp(dir=box.work, prefix="fx-")
    ro, rt = os.path.join(base, "o", "r"), os.path.join(base, "t", "r")
    for r in (ro, rt):
        materialize(r, case)
    three = ["--print-id", "--print-path", "--print-cmd"]
    o_rc, o_out = box.run(ro, case_env(case, ro, "C.UTF-8"), False, three)
    o_out = o_out.replace(ro, "$ROOT")
    t_rc, t_out = box.run(rt, case_env(case, rt, "C.UTF-8"), True, ["explain"])
    lines = [l for l in t_out.replace(rt, "$ROOT").split("\n") if l.startswith("MADO_TERM: ")]
    why = ""
    if not lines:
        why = "no MADO_TERM line"
    else:
        f = dict(kv.split("=", 1) for kv in lines[-1][len("MADO_TERM: "):].split() if "=" in kv)
        if o_rc == 0:
            parts = o_out.split("\n")
            want = (parts[0], parts[1] if len(parts) > 1 else "", "OK", 0)
        else:
            want = ("-", "-", "NO_TERMINAL", 3)
        got = (f.get("selected"), f.get("path"), f.get("verdict"), t_rc)
        if got != want:
            why = "explain got=%r want=%r" % (got, want)
    if not why and o_rc == 0:
        obs_dir = os.path.join(rt, ".rw", "obs")
        os.makedirs(obs_dir)
        good, bad = os.path.join(obs_dir, "good"), os.path.join(obs_dir, "bad")
        with open(good, "wb") as fh:
            fh.write(o_out.replace("$ROOT", rt).encode("utf-8", "surrogateescape"))
        with open(bad, "wb") as fh:
            fh.write(o_out.replace("$ROOT", rt).replace(".desktop", ".desktoq", 1).encode("utf-8", "surrogateescape"))
        for path, want_v, want_rc in ((good, "AGREE", 0), (bad, "DIFFER", 1)):
            rc, out = box.run(rt, case_env(case, rt, "C.UTF-8"), True, ["explain", "--observed", path])
            ls = [l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
            v = ls[-1].rsplit("verdict=", 1)[-1].strip() if ls else ""
            if (v, rc) != (want_v, want_rc):
                why = "observed %s: got %s/%d" % (want_v, v, rc)
                break
    shutil.rmtree(base, ignore_errors=True)
    return why == "", why


# ------------------------------------------------------------------------------------------------ generator
NAMES = ["foot", "kitty", "alacritty", "ghostty", "xterm", "wezterm", "konsole"]
DIRS = ["usr/share/applications/", "home/.local/share/applications/", "opt/share/applications/"]
KEYS = ["Type=Application", "Categories=TerminalEmulator;", "Categories=System;TerminalEmulator", "Categories=System;",
        "Categories=", "CategoriesX=TerminalEmulator;", "Hidden=true", "Hidden=false", "Hidden= true", "NoDisplay=true",
        "TryExec={n}", "TryExec=missing", "TryExec=printf", "TryExec=$ROOT/bin/{n}", "TryExec=read_cache",
        "TryExec={id}", "OnlyShowIn=GNOME;", "OnlyShowIn=Hyprland;", "NotShowIn=Hyprland;", "NotShowIn=KDE;",
        "X-TerminalArgExec=-x", "TerminalArgExec=", "X-ExecArg=--", "ExecArg=-e", "X-TerminalArgExec=-\\se",
        "X-TerminalArgDir=--working-directory=", "TerminalArgDir=-D", "X-TerminalArgTitle=--title",
        "TerminalArgTitle=-T=", "X-TerminalArgAppId=--class=", "X-TerminalArgHold=--hold", "Actions=new;srv;",
        "Actions=other;", "Exec={n}", "Exec={n} --a %U", "Exec=\"{n}\" \"b c\" 100%%", "Exec={n} %f %u",
        "Exec={n} $HOME", "Exec={n} 'q'", "Exec={n}\\s-x", "Exec=  {n}   -a  ", "Exec={n} %k", "Exec=", "Exec=%U",
        "Exec={n} \"a\\\\\"b\"", "Exec=env {n}", "Exec={n} \"\" x", "Exec={n} %", "Exec={n} a%%b %c", "Exec={n} \"$x\"",
        "Exec={n} \"a b", "Exec={n} %i %d", "# comment", "", "  Exec = {n}", "Exec ={n}", "Name=X", "Name[de]=Y",
        "Exec[de]={n}x", "Categories[de]=Foo;"]
GROUPS = ["[Desktop Action new]", "[Desktop Action srv]", "[Other]", "[Desktop Entry] x", "[Desktop Action ]"]
LISTL = ["{id}", "{id}:new", "{id}:srv", "{id}:", "-{id}", "+{id}", "{id}:bad:", "{n}", "# c", "", "  {id}  ",
         "/execarg_strict", "/execarg_compat", "/execarg_default:{id}:-z", "/execarg_default:{id}:a:b:", "/enable_cache",
         "/disable_cache", "{id}\r", "x/{id}", "{id}:a_b", "\t{id}"]
LISTS = ["home/.config/xdg-terminals.list", "home/.config/hyprland-xdg-terminals.list", "etc/xdg/xdg-terminals.list",
         "etc/xdg/gnome-xdg-terminals.list", "usr/share/xdg-terminal-exec/xdg-terminals.list",
         "usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list", "home/.config/gnome-xdg-terminals.list"]
DESKS = ["Hyprland", "hyprland", "GNOME:Hyprland", "Hyprland:GNOME", "", None, "KDE"]
ARGVS = [["--print-id"], ["--print-path"], ["--print-id", "--print-path", "--print-cmd"],
         ["--print-cmd", "--", "htop", "-d 5"], ["--print-cmd", "--dir=/srv", "--title=t x", "--app-id=a", "--hold", "top"],
         ["--test", "-e", "ls"], ["--print-cmd=\\t", "x"], ["--print-id", "--print-delimiter=|", "--print-cmd"],
         ["--print-content"], ["--print-path", "--print-content", "--print-cmd"], ["--print-cmd", "-x", "y"],
         ["--print-cmd", "--unknown", "z"], ["--print-id", "--print-delimiter=\\c", "--print-path"],
         ["--print-cmd=\\101", "--", "a", "b"], ["--print-id", "--print-path", "--print-delimiter=\\n\\n"]]


def gen_entry(rng, n, eid):
    lines = []
    if rng.random() < 0.15:
        lines.append(rng.choice(["# lead", "Exec=" + n]))
    lines.append("[Desktop Entry]" if rng.random() < 0.95 else "[Desktop Entry]x")
    if rng.random() < 0.85:
        lines.append("Categories=TerminalEmulator;")
    if rng.random() < 0.8:
        lines.append("Exec=" + n)
    for _ in range(rng.randint(0, 4)):
        lines.append(rng.choice(KEYS).replace("{n}", n).replace("{id}", eid))
        if rng.random() < 0.1:
            lines.append(rng.choice(GROUPS))
    if rng.random() < 0.4:
        lines.append(rng.choice(GROUPS))
        lines.append("Exec=" + n + "client")
    text = "\n".join(lines)
    if rng.random() < 0.9:
        text += "\n"
    return text


def gen_case(rng, k):
    files, execs, ids = {}, [], []
    for _ in range(rng.randint(0, 5)):
        n = rng.choice(NAMES)
        sub = rng.choice(["", "", "", "vendor/"])
        eid = sub.replace("/", "-") + n + ".desktop"
        files[rng.choice(DIRS) + sub + n + ".desktop"] = gen_entry(rng, n, eid)
        ids.append(eid)
    for n in NAMES:
        if rng.random() < 0.5:
            execs.append("bin/" + n)
        if rng.random() < 0.2:
            execs.append("bin/" + n + "client")
    for lp in LISTS:
        if ids and rng.random() < 0.3:
            ls = [rng.choice(LISTL).replace("{id}", rng.choice(ids)).replace("{n}", rng.choice(NAMES))
                  for _ in range(rng.randint(1, 4))]
            files[lp] = "\n".join(ls) + ("\n" if rng.random() < 0.9 else "")
    desk = rng.choice(DESKS)
    env = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
           "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share"}
    if rng.random() < 0.1:
        env["XDG_DATA_DIRS"] = "$ROOT/usr/share/:$ROOT/opt/share"
    if rng.random() < 0.08:
        del env["XDG_CONFIG_HOME"]
    if rng.random() < 0.08:
        env["XDG_DATA_HOME"] = ""
    if desk is not None:
        env["XDG_CURRENT_DESKTOP"] = desk
    return {"id": "g%03d" % k, "class": "generated", "env": env, "files": files, "exec": execs,
            "args": list(rng.choice(ARGVS))}


# ------------------------------------------------------------------------------------------------ score
def lane_root():
    return os.path.realpath(os.path.join(HERE, "..", ".."))


def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def selftest_clause(box):
    sd = tempfile.mkdtemp(dir=box.work, prefix="st-")
    os.makedirs(os.path.join(sd, ".rw"))
    rc, out = box.run(sd, {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}, True,
                      ["--selftest"], timeout=120)
    last = out.strip().split("\n")[-1] if out.strip() else ""
    parts = last.split()
    ok = False
    if rc == 0 and len(parts) == 3 and parts[0] == "MADO_TERMINAL_SELFTEST:" and parts[2] == "passed":
        n = parts[1].split("/")
        ok = (len(n) == 2 and n[0] == n[1] and n[0].isascii() and n[0].isdigit() and int(n[0]) >= SELFTEST_MIN)
    print("%s clause=s rc=%d last=%r" % (PRED, rc, last[:120]))
    return "ok" if ok else "fail"


def score(repo, rev, work, nonce):
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev")
    full = full.decode().strip()
    fixtures = load_fixtures()
    if not shutil.which("strace"):
        raise Setup("strace missing")
    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    f_ok, g_ok, x_ok, selftest, readonly = 0, 0, 0, "fail", "fail"
    if present:
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "tool.py")
        with open(tool, "wb") as fh:
            fh.write(git(repo, "show", "%s:%s" % (full, TOOL)))
        box = Box(work, tool)
        selftest = selftest_clause(box)
        rng = random.Random(nonce)
        drift = []
        for fx in fixtures:
            ok_a, o_a, why_a = run_case(box, fx, "A", rng)
            ok_b, _o_b, why_b = run_case(box, fx, "B", rng)
            if [o_a[0], o_a[1]] != [fx["expect"]["rc"], fx["expect"]["stdout"]]:
                drift.append(fx["id"])
            ok = ok_a and ok_b
            f_ok += ok
            print("%s clause=f fixture=%s %s%s" % (PRED, fx["id"], "pass" if ok else "FAIL",
                                                  "" if ok else " " + "; ".join(w for w in (why_a, why_b) if w)))
        x_ok = 0
        for fx in fixtures:
            ok, why = explain_case(box, fx, rng)
            x_ok += ok
            if not ok:
                print("%s clause=x fixture=%s FAIL %s" % (PRED, fx["id"], why[:300]))
        print("%s clause=x explained=%d/%d" % (PRED, x_ok, len(fixtures)))
        if drift:
            raise Setup("oracle drifted from %d recorded fixture(s): %s" % (len(drift), ",".join(drift[:5])))
        grng = random.Random(nonce ^ 0x47C1)
        first_fail = None
        for k in range(GEN):
            case = gen_case(grng, k)
            ok, _o, why = run_case(box, case, "A", grng)
            g_ok += ok
            if not ok and first_fail is None:
                first_fail = (k, why)
        print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN, "" if first_fail is None else
                                                 " first_fail=%r" % (first_fail,)))
        readonly = "fail" if box.trips else "ok"
        print("%s clause=r trips=%d %s" % (PRED, len(box.trips), ";".join(sorted(set(box.trips)))[:200]))
    met = (present and selftest == "ok" and readonly == "ok" and f_ok == len(fixtures) and g_ok == GEN
           and x_ok == len(fixtures))
    print("%s: fixtures=%d/%d explained=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s verdict=%s rev=%s nonce=%d" % (
        PRED, f_ok, len(fixtures), x_ok, len(fixtures), g_ok, GEN, selftest, readonly, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", full, nonce))
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=None)
    a = ap.parse_args()
    nonce = a.nonce if a.nonce is not None else int.from_bytes(os.urandom(4), "big")
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        for h in sorted({os.path.realpath(a.repo), lane_root(), os.path.dirname(lane_root())}):
            if under(a.work, h):
                raise Setup("work dir inside a hidden path %s" % h)
        if under(a.work, "/run") or under(a.work, "/proc"):
            raise Setup("work dir under /run or /proc")
        work = tempfile.mkdtemp(dir=a.work, prefix="c1r47-")
        try:
            return score(a.repo, a.rev, work, nonce)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
