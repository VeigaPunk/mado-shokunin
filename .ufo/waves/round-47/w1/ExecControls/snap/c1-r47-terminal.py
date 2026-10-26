#!/usr/bin/env python3
"""PRED-C1-r47 - tools/mado-terminal.py reproduces the terminal selection of xdg-terminal-exec v0.14.3 (C1, operability,
capability acquisition).

The JUDGE IS THE REAL SCRIPT, not a reference implementation of ours. The script bytes are pinned by SCRIPT_SHA256 and
resolved from a fixed candidate list (a copy beside this counter first, then the lane's ScoutScriptMap pin, then the
host binary); any byte difference is a setup error, so a revocation of the pin is visible and no unpinned text is ever
executed. Every `expect` of a fixture is re-checked against the script at count time, and the generated clause (`g`)
takes its expected output from the script only.

Scores one committed revision REV (revision-addressed git reads with ambient GIT_* removed; nothing in the lane is
written; scratch only under --work, which must lie outside the repository, the counter's lane and that lane's parent
directory). TOOL = tools/mado-terminal.py. TARGET_MET iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest`, run in the sandbox below, exits 0 within 60 s and its last non-empty stdout line is
     exactly `MADO_TERMINAL_SELFTEST: N/N passed` with N >= 30 and N read from ASCII digits only.
  f  every fixture of FIXTURES passes in four runs: (seed 47 case-root path, the fixture's env), (seed NONCE case-root
     path, the fixture's env), (seed NONCE case-root path, the fixture's env plus an env variant) and (a forged-cache
     run, below), where each fixture is run against both the tool (`print <args>`) and the real script (`<args>`) in
     that order, each in its own freshly materialized case root, and every case root starts with an EMPTY resolver cache
     (a fixture may not ship one; the cache is out of the contract). Runs A-C pass iff (1) the tool's stdout and exit
     status equal the script's on the same case (both normalized by replacing that run's case root with `$ROOT`) AND
     (2) the script's normalized stdout and exit status equal the fixture's recorded `expect`. Run D passes iff the tool
     still prints the script's cold answer for that root after the script's own cache file has been forged (entry path,
     id, action and exec arg replaced; hash and command lines kept, so the script would treat it as actual): the tool
     must model a cold cache instead of reading one. In every run the tool's stderr is unconstrained (the script writes
     diagnostics to stderr; the contract is stdout and exit status), and a timeout of the SCRIPT is a setup error while
     a timeout of the tool is a failure. FIXTURES is --fixtures or `c1-r47-fixtures.json` beside this counter; fewer
     than MIN_FIXTURES entries, duplicate ids, an unknown shape, a path that escapes the case root, a cache file, an
     env entry that pins HOME/PATH/XDG_CACHE_HOME or points into the operator's home, or an argument list that reaches
     the option scanner's break before consuming a print mode, is a setup error (the last because xdg-terminal-exec
     without a print mode EXECUTES a terminal).
  i  isolation (allowlist): every run - selftest, fixture, generated, read-only - is executed by bubblewrap with a root
     built from `/usr` and `/etc` only (read-only; `/bin`, `/sbin`, `/lib`, `/lib64` as the host's symlinks into /usr),
     `--dev /dev --proc /proc --tmpfs /tmp --unshare-pid --unshare-net --die-with-parent`, plus read-only binds of the
     tool directory, the pinned-script directory, the tool-bin directory, the tripwire directory and a writable bind of
     the case directory only. No other /home, /fast, /run, /var, /srv, /opt or /mnt path of the host is visible
     (the case directory itself lives under --work, the only /fast path bound); bwrap or strace missing is a setup
     error.
  g  generated cases: GEN = 150 cases drawn from NONCE by gen_case() below (config list files with desktop-prefixed and
     plain names across XDG_CONFIG_HOME/XDG_CONFIG_DIRS and the data-dir xdg-terminal-exec/ stores, the /enable_cache
     /disable_cache /execarg_compat /execarg_strict /execarg_default directives, `+`/`-` fallback markers, entry IDs
     with actions; desktop entries across data dirs with duplicate overrides, Hidden, TryExec, Type, Categories,
     OnlyShowIn/NotShowIn, Actions and X-TerminalArg* keys, quoting and % fields, missing executables, invalid IDs;
     print modes --print-id/--print-path/--print-cmd[=seq]/--print-delimiter=seq mixed and repeated, with --dir/
     --title/--app-id/--hold and trailing command words). Each case runs the real script in the sandbox to obtain its
     expected stdout and exit status and requires the tool to equal both (normalized by case root).
  r  read-only: the tool starts no process and opens no socket. (1) Tripwire: PATH is `$ROOT/bin:<toolbin>` where
     toolbin holds symlinks to /usr/bin and executable stubs named `xdg-terminal-exec`, `sh`, `bash`, `dash`,
     `busybox` and every `python*` other than the interpreter, each of which connects to a unix socket the counter
     listens on (in a directory bound read-only, so the tool cannot remove it); the same files are also bound read-only
     over /usr/bin/<name> during tool runs, so an absolute path runs them too. All tool runs of clauses s, f, g and r
     execute with that tripwire; the counter accepts in a thread outside the sandbox, so a tool can add connections but
     cannot take one back. The tripwire is proven live at count time (one deliberate run of the fake
     `xdg-terminal-exec` must be accepted) and its hits are cleared before the tool runs; after all runs no connection
     was accepted. (2) strace: on a synthetic resolving case the tool is run under
     `strace -f -qq -e trace=execve,socket,connect` and the trace must show exactly one successful execve (the
     interpreter, same basename as the counter's sys.executable) and no `socket(`/`connect(` line; the strace parser is
     proven live at count time on a two-execve control.
Final line: `PRED-C1-r47: fixtures=K/F generated=G/150 selftest=<ok|fail> readonly=<ok|fail> tool=<present|absent>
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> seeds=47,<nonce>`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup
failure. Clause lines `PRED-C1-r47 clause=<x> ...` precede it. A selftest count is read only from ASCII digits.
Residuals (declared): a tool that ignores the cache and a tool that reads an absent one are indistinguishable in runs
A-C, so run D carries the cache claim and it cannot forge when the script wrote no cache (no terminal found); because
`save_cache` is backgrounded (`xdg-terminal-exec:1457`), a forged cache can be overwritten by the tail of that write,
which can only turn a cache-reading tool's failure into a pass for that fixture; `find -L` is unsorted
(`xdg-terminal-exec:795`), so a fixture that leaves two co-equal terminal entries in one applications directory
under a filesystem-dependent directory order is materialized in JSON key order in both roots, which is the one order
this counter pins (a fixture file whose order matters is a fixture defect); the fixtures and the generated cases are
cases of the contract, not a proof of equivalence over all inputs; the generated cases are drawn from one generator, so a shared blind spot of generator and tool is
invisible; clause r proves "no process and no socket on the probed case", not on every input (a tool could branch on
its arguments and spawn only where nothing is traced); the tripwire covers the named binaries and PATH/absolute
lookups of them, not every possible exec path (e.g. a static binary the tool carries, which the strace clause would
still catch on the probed case); clause s is a printed line, not capability evidence; whether the resolver matches the
host's launch path beyond the pinned script is the non-author reading.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

PRED = "PRED-C1-r47"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mado-terminal.py"
SELFTEST_MARK = "MADO_TERMINAL_SELFTEST:"
SELFTEST_MIN = 30
SEED = 47
GEN = 150
MIN_FIXTURES = 100
SCRIPT_NAME = "xdg-terminal-exec"
SCRIPT_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
PRINT_MODES = ("--print-id", "--print-path", "--print-content", "--print-cmd")
FAKE_STEMS = ("xdg-terminal-exec", "sh", "bash", "dash", "busybox")
FAKEBIN = []
FAKE_NAMES = []
FAKE_TARGETS = {}
TRIPDIR = None
TRIP_MOUNT = "/trip"
TRIP_SOCK = TRIP_MOUNT + "/s.sock"


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


def pinned(path, sha, what):
    try:
        blob = open(path, "rb").read()
    except OSError:
        raise Setup("missing %s" % what)
    if hashlib.sha256(blob).hexdigest() != sha:
        raise Setup("sha256 mismatch %s" % what)
    return blob


def lane_root():
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, ".ufo")) and os.path.isdir(os.path.join(d, "quality")):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    return os.path.realpath(os.path.join(HERE, "..", ".."))


def script_candidates():
    lane = lane_root()
    return [
        os.path.join(HERE, SCRIPT_NAME),
        os.path.join(HERE, SCRIPT_NAME + "-v0.14.3"),
        os.path.join(lane, "quality", "counters", SCRIPT_NAME),
        os.path.join(lane, "quality", "counters", SCRIPT_NAME + "-v0.14.3"),
        os.path.join(lane, ".ufo", "waves", "round-47", "w1", "ScoutScriptMap", "upstream-" + SCRIPT_NAME),
        "/usr/bin/" + SCRIPT_NAME,
    ]


def load_script():
    """First existing candidate decides: a present-but-different copy is a revocation of the pin, not something to
    paper over by falling through to the next path."""
    tried = []
    for c in script_candidates():
        if not os.path.isfile(c):
            tried.append("%s:absent" % c)
            continue
        blob = open(c, "rb").read()
        if hashlib.sha256(blob).hexdigest() != SCRIPT_SHA256:
            raise Setup("sha256 mismatch of the pinned script at %s" % c)
        return c, blob
    raise Setup("pinned script not found (%s)" % ", ".join(tried))


HOME_DIR = os.path.realpath(os.path.expanduser("~"))


def no_home_path(value):
    return value == HOME_DIR or value.startswith(HOME_DIR + "/")


def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def hidden_paths(repo):
    lr = lane_root()
    return sorted({os.path.realpath(repo), lr, os.path.dirname(lr)})


def root_links():
    out = []
    for n in ("bin", "sbin", "lib", "lib64"):
        p = "/" + n
        if os.path.islink(p):
            out += ["--symlink", os.readlink(p), p]
    return out


# ---------------------------------------------------------------- fixtures

def rel_ok(rel):
    if not isinstance(rel, str) or not rel or rel.startswith("/"):
        return False
    parts = rel.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def print_mode(a):
    return a in PRINT_MODES or a.startswith("--print-cmd=")


def shell_safe(args):
    """Refuse to run an argument list that reaches the option scanner's break (end of options, `-e`, or the first
    non-option word) before consuming a print mode: xdg-terminal-exec EXECUTES a terminal then, and this counter never
    launches a terminal. The break may also be caused by a token equal to the entry's own TerminalArgExec value, which
    is only known once the case exists; such a case still executes only inside the sandbox, where the case's own
    `bin/` stubs are the only reachable programs and no display, /run or /home path exists."""
    ok = False
    for a in args:
        if not isinstance(a, str):
            return False
        if print_mode(a):
            ok = True
            continue
        if a == "--" or a == "-e" or not a.startswith("-"):
            return ok
    return ok


def load_fixtures(path):
    try:
        raw = open(path, "rb").read()
    except OSError:
        raise Setup("missing fixtures %s" % os.path.basename(path))
    try:
        fx = json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise Setup("fixtures not JSON: %s" % e)
    if not isinstance(fx, list):
        raise Setup("fixtures not a JSON list")
    if len(fx) < MIN_FIXTURES:
        raise Setup("fewer than %d fixtures (%d)" % (MIN_FIXTURES, len(fx)))
    seen = set()
    for k, c in enumerate(fx):
        if not isinstance(c, dict):
            raise Setup("fixture %d not an object" % k)
        cid = c.get("id")
        if not isinstance(cid, str) or not cid:
            raise Setup("fixture %d has no id" % k)
        if cid in seen:
            raise Setup("duplicate fixture id %r" % cid)
        seen.add(cid)
        if not isinstance(c.get("env") or {}, dict):
            raise Setup("fixture %s env not an object" % cid)
        for key, val in (c.get("env") or {}).items():
            if not isinstance(key, str) or not isinstance(val, str):
                raise Setup("fixture %s env entry not a string pair" % cid)
            if key in ("HOME", "PATH", "XDG_CACHE_HOME"):
                raise Setup("fixture %s sets the counter-pinned variable %s" % (cid, key))
            if isinstance(val, str) and no_home_path(val):
                raise Setup("fixture %s env %s points into the operator's home: %r" % (cid, key, val))
        files = c.get("files") or {}
        if not isinstance(files, dict):
            raise Setup("fixture %s files not an object" % cid)
        for rel in files:
            if not rel_ok(rel):
                raise Setup("fixture %s file path escapes the case root: %r" % (cid, rel))
            if not isinstance(files[rel], str):
                raise Setup("fixture %s file %r not text" % (cid, rel))
            if rel.split("/")[0] == ".cache" or rel == ".cache":
                raise Setup("fixture %s ships a resolver cache file (the cache is out of the contract)" % cid)
        execs = c.get("exec") or []
        if not isinstance(execs, list) or any(not rel_ok(r) for r in execs):
            raise Setup("fixture %s exec not a list of root-relative paths" % cid)
        args = c.get("args")
        if not isinstance(args, list):
            raise Setup("fixture %s args not a list" % cid)
        if not shell_safe(args):
            raise Setup("fixture %s has no print mode (refusing to launch a terminal)" % cid)
        exp = c.get("expect") or {}
        if not isinstance(exp.get("stdout"), str) or not isinstance(exp.get("rc"), int):
            raise Setup("fixture %s expect is not {rc:int, stdout:str}" % cid)
    return fx, hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------- sandbox

def fake_names():
    interp = {os.path.basename(sys.executable), os.path.basename(os.path.realpath(sys.executable))}
    real_interp = os.path.realpath(sys.executable)
    names = list(FAKE_STEMS)
    try:
        entries = sorted(os.listdir("/usr/bin"))
    except OSError:
        entries = []
    for n in entries:
        if not n.startswith("python") or n in interp:
            continue
        if os.path.realpath(os.path.join("/usr/bin", n)) == real_interp:
            continue
        names.append(n)
    return names


def fake_targets():
    """Absolute host paths to cover with fakes. /usr/bin/sh is a symlink to bash and bubblewrap cannot mount on a
    symlink destination, so a name is covered at its realpath; the interpreter's realpath is never covered (the tool
    itself is python)."""
    out = {}
    real_interp = os.path.realpath(sys.executable)
    for n in FAKE_NAMES:
        p = os.path.join("/usr/bin", n)
        if not os.path.lexists(p):
            continue
        real = os.path.realpath(p)
        if real == real_interp or not real.startswith("/usr/bin/"):
            continue
        out.setdefault(real, n)
    return out


def make_fakebin(d, sock_path):
    os.makedirs(d)
    global FAKE_NAMES, FAKE_TARGETS
    FAKE_NAMES = fake_names()
    fakes = set(FAKE_NAMES)
    for n in sorted(os.listdir("/usr/bin")):
        if n in fakes:
            continue
        try:
            os.symlink(os.path.join("/usr/bin", n), os.path.join(d, n))
        except OSError:
            pass
    for n in FAKE_NAMES:
        p = os.path.join(d, n)
        with open(p, "w") as f:
            f.write("#!%s -I\nimport socket\ns = socket.socket(socket.AF_UNIX)\ns.connect(%r)\n"
                    "s.sendall(%r)\ns.close()\n" % (sys.executable, sock_path, n.encode()))
        os.chmod(p, 0o755)
    FAKEBIN[:] = [d]
    FAKE_TARGETS = fake_targets()
    return d


class Trip:
    """Unix-socket tripwire: every accepted connection is one watched-binary run."""

    def __init__(self, d):
        import socket
        import threading
        self.path = os.path.join(d, "s.sock")
        if len(self.path.encode()) > 100:
            raise Setup("socket path too long (%d bytes); use a shorter --work" % len(self.path.encode()))
        self.srv = socket.socket(socket.AF_UNIX)
        self.srv.bind(self.path)
        self.srv.listen(128)
        self.srv.settimeout(0.2)
        self.hits = []
        self.lock = threading.Lock()
        self.stop = False
        self.t = threading.Thread(target=self.loop, daemon=True)
        self.t.start()

    def loop(self):
        while not self.stop:
            try:
                c, _ = self.srv.accept()
            except OSError:
                continue
            try:
                c.settimeout(2)
                got = c.recv(64) or b"?"
            except OSError:
                got = b"?"
            c.close()
            with self.lock:
                self.hits.append(got)

    def clear(self):
        with self.lock:
            self.hits = []

    def await_hits(self, n, timeout=3.0):
        import time
        end = time.time() + timeout
        while time.time() < end:
            if len(self.snapshot()) >= n:
                break
            time.sleep(0.02)
        return self.snapshot()

    def snapshot(self):
        with self.lock:
            return list(self.hits)

    def close(self):
        import time
        time.sleep(0.3)
        self.stop = True
        self.t.join()
        self.srv.close()
        return self.snapshot()


def sandbox(argv, cwd, ro_dirs, fake=False):
    """Allowlist root: /usr and /etc read-only, the given dirs read-only, the case dir writable; during tool runs the
    fake binaries also cover /usr/bin/<name>."""
    cmd = ["bwrap", "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"] + root_links() + [
        "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-pid", "--unshare-net",
        "--die-with-parent"]
    if TRIPDIR is not None:
        cmd += ["--ro-bind", TRIPDIR, TRIP_MOUNT]
    for d in ro_dirs:
        cmd += ["--ro-bind", d, d]
    if fake:
        for real, n in sorted(FAKE_TARGETS.items()):
            cmd += ["--ro-bind", os.path.join(FAKEBIN[0], n), real]
    cmd += ["--bind", cwd, cwd, "--chdir", cwd, "--"]
    return cmd + argv


def materialize(root, files, execs):
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, "bin"), exist_ok=True)
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            f.write(text)
    for rel in execs:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(p, 0o755)


def case_env(fx_env, root, toolbin, variant):
    """HOME and PATH are fixed by the fixture schema; XDG_CACHE_HOME is forced into the case root so the resolver's
    cache is always cold and never the host's (the tool models a cold cache)."""
    env = {"PATH": os.path.join(root, "bin") + os.pathsep + toolbin,
           "HOME": os.path.join(root, "home"),
           "XDG_CACHE_HOME": os.path.join(root, ".cache"),
           "LANG": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1"}
    for key, val in (fx_env or {}).items():
        env[key] = val.replace("$ROOT", root)
    if variant:
        for extra, val in (("TMPDIR", root + "/tmp"), ("XDG_RUNTIME_DIR", root + "/run"),
                           ("TERM", "dumb"), ("PYTHONHASHSEED", "0"), ("LANG", "en_US.UTF-8")):
            env[extra] = val
        for sub in ("tmp", "run"):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
    return env


def check_sandbox(p):
    if p is not None and p.stderr.startswith(b"bwrap:"):
        raise Setup("sandbox failed: %r" % p.stderr[:200])
    return p


def run_oracle(script, args, cwd, env, ro_dirs, timeout=40):
    try:
        return check_sandbox(subprocess.run(sandbox([script] + args, cwd, ro_dirs), input=b"",
                                            capture_output=True, env=env, timeout=timeout))
    except subprocess.TimeoutExpired:
        return None


def run_oracle_cached(script, args, cwd, env, ro_dirs, timeout=40):
    """Run the pinned script once so that its backgrounded `save_cache` can finish: the wrapper relays stdout and the
    exit status unchanged, so this is still the script's answer."""
    wrap = "%s \"$@\"; rc=$?; sleep 0.15; exit $rc" % shlex_quote(script)
    try:
        return check_sandbox(subprocess.run(sandbox(["/bin/sh", "-c", wrap, "sh"] + args, cwd, ro_dirs),
                                            input=b"", capture_output=True, env=env, timeout=timeout))
    except subprocess.TimeoutExpired:
        return None


def shlex_quote(text):
    return "'" + text.replace("'", "'\\''") + "'"


def run_tool(tool, args, cwd, env, ro_dirs, timeout=30, trace=None):
    argv = [sys.executable, "-I", tool, "print"] + args
    if trace is not None:
        argv = ["/usr/bin/strace", "-f", "-qq", "-e", "trace=execve,socket,connect", "-o", trace] + argv
    try:
        return check_sandbox(subprocess.run(sandbox(argv, cwd, ro_dirs, fake=True), input=b"",
                                            capture_output=True, env=env, timeout=timeout))
    except subprocess.TimeoutExpired:
        return None


def dec(raw):
    return raw.decode("utf-8", "replace")


def norm(text, root):
    return text.replace(root, "$ROOT")


def trace_counts(path):
    execs, socks = [], []
    try:
        text = open(path, "r", errors="replace").read()
    except OSError:
        return None, None
    for line in text.splitlines():
        body = line.split(None, 1)[1] if len(line.split(None, 1)) == 2 else ""
        if body.startswith("execve("):
            m = re.match(r'execve\("((?:[^"\\]|\\.)*)"', body)
            if m and re.search(r"= 0$", body.strip()):
                execs.append(m.group(1))
        elif body.startswith("socket(") or body.startswith("connect("):
            socks.append(body[:80])
    return execs, socks


# ---------------------------------------------------------------- generated cases

DESKTOPS = ["Hyprland", "Hyprland", "Hyprland:GNOME", "hyprland", "sway", "", "Hyprland:", "SWAY:Hyprland"]
EXEC_NAMES = ["alacritty", "kitty", "foot", "myterm", "xterm"]
ENTRY_NAMES = ["Alacritty.desktop", "kitty.desktop", "xterm.desktop", "foot.desktop", "myterm.desktop",
               "org.gnome.Terminal.desktop", "2048-qt.desktop", "a_b-c.desktop", "UPPER.desktop",
               "nested/deep.desktop", "bad name.desktop", ".hidden.desktop"]
DELIMS = ["\\n", "|", ";", "", "\\t", "::", "\\n\\n"]
ACTIONS = ["new", "New", "window", ""]
ARG_PREFIX = ["", "", "--dir=$ROOT/home", "--title=Term", "--app-id=Alacritty", "--hold"]


def entry_text(rng, exe, want_term, action_hint):
    lines = ["[Desktop Entry]"]
    lines.append("Type=" + rng.choice(["Application", "Application", "Application", "Link", ""]))
    lines.append("Name=" + rng.choice(["Alacritty", "Kitty", "Foot", "MyTerm", "Terminal"]))
    kind = rng.random()
    if kind < 0.08:
        lines.append("Exec=" + rng.choice([exe, "/nonexistent/%s" % exe, "missingbin"]))
    elif kind < 0.16:
        lines.append('Exec="%s" --flag' % exe)
    elif kind < 0.24:
        lines.append("Exec=%s %%F" % exe)
    elif kind < 0.30:
        lines.append("Exec=%s %%u %%f" % exe)
    elif kind < 0.36:
        lines.append("Exec=%s \\\\s--opt" % exe)
    else:
        lines.append("Exec=" + rng.choice(["%s", "%s --class Alacritty", "%s --single-instance",
                                           "%s -e", "%s --working-directory=%%k"]) % exe)
    if rng.random() < 0.8:
        cats = "TerminalEmulator;" if want_term else rng.choice(
            ["Utility;", "TerminalEmulator;Utility;", "System;TerminalEmulator;", "Utility;", ""])
        lines.append("Categories=" + cats)
    if rng.random() < 0.12:
        lines.append("Hidden=" + rng.choice(["true", "false", "True"]))
    if rng.random() < 0.18:
        lines.append("TryExec=" + rng.choice([exe, "missingbin", ""]))
    if rng.random() < 0.15:
        lines.append("OnlyShowIn=" + rng.choice(["Hyprland;", "GNOME;", "sway;Hyprland;", ""]))
    if rng.random() < 0.15:
        lines.append("NotShowIn=" + rng.choice(["Hyprland;", "GNOME;", "sway;", ""]))
    for key, vals in (("TerminalArgExec", ["-e", "--", "exec", "\\s-e"]),
                      ("X-TerminalArgAppId", ["--class=", "--app-id"]),
                      ("TerminalArgDir", ["--working-directory=", "--dir"]),
                      ("TerminalArgTitle", ["--title", "--title="]),
                      ("TerminalArgHold", ["--hold"])):
        if rng.random() < 0.12:
            lines.append("%s=%s" % (key, rng.choice(vals)))
    if action_hint and rng.random() < 0.7:
        lines.append("Actions=new;")
        lines.append("")
        lines.append("[Desktop Action new]")
        lines.append("Name=New Window")
        lines.append("Exec=%s --new" % exe)
    if rng.random() < 0.1:
        lines.append("X-Custom=" + rng.choice(["a=b", " spaced ", "%%U"]))
    if rng.random() < 0.06:
        lines.append("[Desktop Action other]")
        lines.append("Exec=%s --other" % exe)
    return "\n".join(lines) + "\n"


def list_text(rng, ids):
    out = []
    for _ in range(rng.randint(0, 2)):
        out.append(rng.choice(["/enable_cache", "/disable_cache", "/execarg_compat", "/execarg_strict"]))
    for _ in range(rng.randint(1, 4)):
        pick = rng.random()
        if pick < 0.1:
            out.append("# comment " + rng.choice(["Alacritty.desktop", "x"]))
        elif pick < 0.16:
            out.append("")
        elif pick < 0.22:
            out.append(rng.choice(["Alacritty", "bad name.desktop", ".desktop", "a/b.desktop", "x y"]))
        else:
            eid = rng.choice(ids)
            lead = rng.choice(["", "", "", "+", "-"])
            act = rng.choice(ACTIONS)
            out.append("%s%s%s" % (lead, eid, (":" + act) if act else ""))
    return "\n".join(out) + ("\n" if rng.random() < 0.9 else "")


def gen_case(rng):
    env = {"XDG_CURRENT_DESKTOP": rng.choice(DESKTOPS)}
    cfg_home = "$ROOT/home/.config"
    if rng.random() < 0.85:
        env["XDG_CONFIG_HOME"] = cfg_home
    n_cfg = rng.choice([0, 1, 1, 2])
    cfg_dirs = ["$ROOT/etc-xdg%d" % i for i in range(n_cfg)]
    if n_cfg and rng.random() < 0.85:
        env["XDG_CONFIG_DIRS"] = ":".join(cfg_dirs)
    data_home = "$ROOT/home/.local/share"
    if rng.random() < 0.85:
        env["XDG_DATA_HOME"] = data_home
    n_data = rng.choice([1, 2, 2, 3])
    data_dirs = ["$ROOT/share%d" % i for i in range(n_data)]
    if rng.random() < 0.92:
        env["XDG_DATA_DIRS"] = ":".join(data_dirs)
    else:
        env["XDG_DATA_DIRS"] = "$ROOT/share0"

    files = {}
    execs = []
    stubs = [n for n in EXEC_NAMES if rng.random() < 0.7] or [EXEC_NAMES[0]]
    for n in stubs:
        execs.append("bin/" + n)
    apps_dirs = [data_home + "/applications", data_dirs[0] + "/applications"]
    if rng.random() < 0.3:
        apps_dirs.append("$ROOT/home/.local/share/applications")
    if n_data > 1:
        apps_dirs.append(data_dirs[1] + "/applications")
    names = []
    for _ in range(rng.randint(1, 3)):
        n = rng.choice(ENTRY_NAMES)
        if n not in names:
            names.append(n)
    action_hint = rng.random() < 0.4
    ids = [n[:-len(".desktop")].replace("/", "-") for n in names if n.endswith(".desktop")]
    for nm in names:
        content = entry_text(rng, rng.choice(stubs + ["missingbin"]), rng.random() < 0.75, action_hint)
        primary = apps_dirs[0].replace("$ROOT", "").lstrip("/")
        files[primary + "/" + nm] = content
        if rng.random() < 0.4:
            dup = apps_dirs[-1].replace("$ROOT", "").lstrip("/")
            files[dup + "/" + nm] = content.replace("--class Alacritty", "--class Override")
    # config list files
    desktop = env["XDG_CURRENT_DESKTOP"].split(":")[0].lower()
    where = []
    if rng.random() < 0.7:
        where.append(cfg_home.replace("$ROOT", "").lstrip("/") + "/" + (desktop + "-" if desktop else "") +
                     "xdg-terminals.list")
    if rng.random() < 0.5:
        base = cfg_home if "XDG_CONFIG_HOME" in env else "$ROOT/home/.config"
        where.append(base.replace("$ROOT", "").lstrip("/") + "/xdg-terminals.list")
    for cd in cfg_dirs:
        if rng.random() < 0.35:
            where.append(cd.replace("$ROOT", "").lstrip("/") + "/xdg-terminals.list")
    for dd in data_dirs:
        if rng.random() < 0.3:
            where.append(dd.replace("$ROOT", "").lstrip("/") + "/xdg-terminal-exec/xdg-terminals.list")
    for w in where:
        if w in files:
            continue
        files[w] = list_text(rng, ids or ["Alacritty"])
    # a self-consistent fallback: at least one listed ID exists somewhere
    if ids and rng.random() < 0.6:
        key = where[0] if where else (cfg_home.replace("$ROOT", "").lstrip("/") + "/xdg-terminals.list")
        files[key] = (files.get(key, "") + ids[0] + "\n").lstrip("\n")

    args = []
    mode = rng.random()
    if mode < 0.4:
        args += rng.sample(["--print-id", "--print-path", "--print-cmd"], rng.randint(1, 3))
    elif mode < 0.55:
        args += ["--print-id", "--print-path", "--print-cmd=" + rng.choice(DELIMS)]
    elif mode < 0.7:
        args += [rng.choice(["--print-id", "--print-path"]), "--print-delimiter=" + rng.choice(DELIMS)]
    else:
        args += ["--print-cmd=" + rng.choice(DELIMS), "--print-id"]
    extras = [p for p in ARG_PREFIX if p and rng.random() < 0.3]
    if rng.random() < 0.12:
        extras.append(rng.choice(["-x", "--bogus", "--unknown"]))
    args += extras
    if rng.random() < 0.45:
        args.append("--")
        args += rng.choice([["ls", "-l"], ["sh", "-c", "echo hi"], ["myterm"], []] )
    rng.shuffle(args)
    if not shell_safe(args):
        args = ["--print-id"] + args
    return {"class": "gen", "env": env, "files": files, "exec": execs, "args": args}


# ---------------------------------------------------------------- runs

def load_case(root, files, execs):
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    materialize(root, files, execs)
    # the resolver's cache is out of the contract: every case starts cold, both for the script and for the tool
    shutil.rmtree(os.path.join(root, ".cache"), ignore_errors=True)
    os.makedirs(os.path.join(root, ".cache"), exist_ok=True)


def one_run(tool, script, case, variant, work, toolbin, ro_dirs, prefix, label=""):
    """One fixture case, one seed: oracle in its own root, then the tool in a second root, then compare. A timeout of
    the SCRIPT is a setup error (a case that blocks the judge would otherwise be scored as a verdict); a timeout of the
    tool is a failure of the tool."""
    root_o = tempfile.mkdtemp(dir=work, prefix=prefix + "or-")
    root_t = tempfile.mkdtemp(dir=work, prefix=prefix + "tl-")
    load_case(root_o, case["files"], case.get("exec") or [])
    load_case(root_t, case["files"], case.get("exec") or [])
    env_o = case_env(case.get("env"), root_o, toolbin, variant)
    env_t = case_env(case.get("env"), root_t, toolbin, variant)
    p_o = run_oracle(script, case["args"], root_o, env_o, ro_dirs)
    p_t = run_tool(tool, case["args"], root_t, env_t, ro_dirs)
    shutil.rmtree(root_o, ignore_errors=True)
    shutil.rmtree(root_t, ignore_errors=True)
    if p_o is None:
        raise Setup("the pinned script timed out on case %r (case-%s root %s)" % (label, prefix, root_o))
    if p_t is None:
        return {"rc": p_o.returncode, "stdout": norm(dec(p_o.stdout), root_o)}, None, "tool-timeout"
    oracle = {"rc": p_o.returncode, "stdout": norm(dec(p_o.stdout), root_o)}
    tool_out = {"rc": p_t.returncode, "stdout": norm(dec(p_t.stdout), root_t)}
    return oracle, tool_out, ""


def cached_run(tool, script, case, work, toolbin, ro_dirs, label, state):
    """Clause f, run D: the tool must IGNORE the resolver's cache. The case is materialized, the script is run once so
    it writes its own cache, the cache is forged (entry path, id, action and exec array replaced, hash and command lines
    kept, so the script would consider it actual), and the tool must still print the cold answer of the script in that
    same root. `save_cache` is backgrounded, so the cache file is waited for; if it never appears the run cannot forge
    and only the cold comparison is scored (a cache-reading tool is then indistinguishable - declared residual)."""
    root = tempfile.mkdtemp(dir=work, prefix="job-cache-")
    load_case(root, case["files"], case.get("exec") or [])
    env = case_env(case.get("env"), root, toolbin, False)
    p_o = run_oracle_cached(script, case["args"], root, env, ro_dirs)
    if p_o is None:
        raise Setup("the pinned script timed out on case %r (cache run)" % label)
    cold = {"rc": p_o.returncode, "stdout": norm(dec(p_o.stdout), root)}
    cache = os.path.join(root, ".cache", SCRIPT_NAME)
    # the script writes its cache only on the --print-cmd path (it exits before save_cache for id/path-only modes), and
    # the write is backgrounded: wait briefly, but only when a cache can exist at all
    import time
    if any(a == "--print-cmd" or a.startswith("--print-cmd=") for a in case["args"]):
        end = time.time() + 0.6
        while time.time() < end and not os.path.exists(cache):
            time.sleep(0.01)
    forged = False
    try:
        with open(cache, "r", errors="replace", newline="") as f:
            lines = f.read().split("\n")
    except OSError:
        lines = []
    if len(lines) >= 4:
        lines[2] = root + "/forged-path.desktop"
        lines[3] = "Forged.desktop"
        if len(lines) >= 5:
            lines[4] = ""
        if len(lines) >= 11:
            # the exec array is USEP-delimited and the cache ends it with RSEP + END_OF_EXEC_USEP
            lines[10] = "forged-term\x1eEND_OF_EXEC_USEP"
        try:
            with open(cache, "w", newline="") as f:
                f.write("\n".join(lines))
            forged = True
        except OSError:
            forged = False
    if forged and state.get("liveness") is None:
        p_w = run_oracle(script, case["args"], root, env, ro_dirs)
        state["liveness"] = (p_w is not None and p_w.returncode == cold["rc"]
                             and dec(p_w.stdout) != cold["stdout"])
        state["warm"] = None if p_w is None else dec(p_w.stdout)[:120]
    p_t = run_tool(tool, case["args"], root, env, ro_dirs)
    shutil.rmtree(root, ignore_errors=True)
    if p_t is None:
        return False, "cache:tool-timeout", forged
    tool_out = norm(dec(p_t.stdout), root)
    if tool_out != cold["stdout"] or p_t.returncode != cold["rc"]:
        return False, "cache:tool-vs-cold rc=%d/%d out=%r/%r" % (
            p_t.returncode, cold["rc"], tool_out[-160:], cold["stdout"][-160:]), forged
    return True, "", forged


def fixture_ok(tool_out, oracle, expect):
    """The recorded expect is checked against the script first, so a drifted fixture is reported as fixture drift and
    not as a tool defect; only then is the tool compared with the script."""
    if tool_out is None:
        return False, "tool-timeout"
    if oracle["stdout"] != expect["stdout"] or oracle["rc"] != expect["rc"]:
        return False, "oracle-vs-expect rc=%d/%d out=%r/%r" % (
            oracle["rc"], expect["rc"], oracle["stdout"][-160:], expect["stdout"][-160:])
    if tool_out["stdout"] != oracle["stdout"] or tool_out["rc"] != oracle["rc"]:
        return False, "tool-vs-script rc=%d/%d out=%r/%r" % (
            tool_out["rc"], oracle["rc"], tool_out["stdout"][-160:], oracle["stdout"][-160:])
    return True, ""


def score(repo, rev, work, nonce, fixtures_path):
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev %r" % rev)
    full = full.decode().strip()
    script_src, blob = load_script()
    fixtures, fixtures_sha = load_fixtures(fixtures_path)

    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    print("%s clause=i script=%s sha256=%s fixtures=%d fixtures_sha256=%s" % (
        PRED, script_src, SCRIPT_SHA256, len(fixtures), fixtures_sha))
    if not present:
        print("%s: fixtures=0/%d generated=0/%d selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED "
              "rev=%s seeds=%d,%d" % (PRED, len(fixtures), GEN, full, SEED, nonce))
        return 1

    blob_tool = git(repo, "show", "%s:%s" % (full, TOOL))
    if blob_tool is None:
        raise Setup("cannot read %s at %s" % (TOOL, full))

    sdir = os.path.join(work, "script")
    os.makedirs(sdir)
    script = os.path.join(sdir, SCRIPT_NAME)
    with open(script, "wb") as f:
        f.write(blob)
    os.chmod(script, 0o755)
    tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
    tool = os.path.join(tdir, "mado-terminal.py")
    with open(tool, "wb") as f:
        f.write(blob_tool)

    global TRIPDIR
    TRIPDIR = os.path.join(work, "t")
    os.makedirs(TRIPDIR)
    trip = Trip(TRIPDIR)
    fakebin = make_fakebin(os.path.join(work, "bin"), TRIP_SOCK)
    ro_dirs = [tdir, sdir, fakebin]

    # tripwire and strace liveness (proven able to fail) before any tool run
    probe = tempfile.mkdtemp(dir=work, prefix="live-")
    env_probe = case_env({}, probe, fakebin, False)
    p = check_sandbox(run_oracle(fakebin + "/xdg-terminal-exec", [], probe, env_probe, ro_dirs))
    live = trip.await_hits(1, timeout=3.0)
    if p is None or len(live) != 1 or live[0] != b"xdg-terminal-exec":
        raise Setup("tripwire dead (%r)" % (live,))
    tr = os.path.join(probe, "ctl.trace")
    subprocess.run(sandbox(["/usr/bin/strace", "-f", "-qq", "-e", "trace=execve,socket,connect", "-o", tr,
                            "/bin/sh", "-c", "/bin/true"], probe, ro_dirs),
                   input=b"", capture_output=True, env=env_probe, timeout=30)
    ctl_execs, ctl_socks = trace_counts(tr)
    if ctl_execs is None or len(ctl_execs) < 2:
        raise Setup("strace parser dead (%r)" % (ctl_execs,))
    trip.clear()
    print("%s clause=r tripwire=live control=%r strace=live control_execve=%d" % (
        PRED, b"".join(live).decode("ascii", "replace"), len(ctl_execs)))

    selftest = "fail"
    sd = tempfile.mkdtemp(dir=work, prefix="st-")
    os.makedirs(os.path.join(sd, "home"))
    os.makedirs(os.path.join(sd, "tmp"))
    env_s = {"PATH": fakebin, "HOME": os.path.join(sd, "home"), "TMPDIR": os.path.join(sd, "tmp"),
             "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        p = check_sandbox(subprocess.run(sandbox([sys.executable, "-I", tool, "--selftest"], sd, ro_dirs,
                                                  fake=True), input=b"", capture_output=True, env=env_s,
                                         timeout=60))
        lines = [ln for ln in dec(p.stdout).splitlines() if ln.strip()]
        last = lines[-1] if lines else ""
        parts = last.split()
        okst = False
        if p.returncode == 0 and len(parts) == 3 and parts[0] == SELFTEST_MARK and parts[2] == "passed":
            n = parts[1].split("/")
            okst = (len(n) == 2 and n[0] == n[1] and n[0].isascii() and n[0].isdigit()
                    and int(n[0]) >= SELFTEST_MIN)
        selftest = "ok" if okst else "fail"
        print("%s clause=s rc=%d last=%r" % (PRED, p.returncode, last[:140]))
    except subprocess.TimeoutExpired:
        print("%s clause=s timeout" % PRED)

    fixtures_ok = 0
    cache_forged = 0
    cache_state = {}
    fx_rng = random.Random(SEED)
    runs = [("seedA", "fx-%08x-" % fx_rng.getrandbits(32), False),
            ("seedB", "job-%08x-" % random.Random(nonce).getrandbits(32), False),
            ("envC", "job-%08x-" % random.Random(nonce ^ 0xA5A5A5A5).getrandbits(32), True)]
    for fx in fixtures:
        ok = True
        whys = []
        for label, prefix, variant in runs:
            oracle, tool_out, why = one_run(tool, script, fx, variant, work, fakebin, ro_dirs, prefix, fx["id"])
            if oracle is None:
                ok = False
                whys.append("%s:%s" % (label, why))
                continue
            good, why = fixture_ok(tool_out, oracle, fx["expect"])
            if not good:
                ok = False
                whys.append("%s:%s" % (label, why))
        good, why, forged = cached_run(tool, script, fx, work, fakebin, ro_dirs, fx["id"], cache_state)
        cache_forged += forged
        if not good:
            ok = False
            whys.append("cacheD:" + why)
        fixtures_ok += ok
        print("%s clause=f fixture=%s %s%s" % (PRED, fx["id"], "pass" if ok else "FAIL",
                                               "" if ok else " " + "; ".join(whys)[:400]))
    print("%s clause=f forged_cache_runs=%d/%d forge_live=%s warm=%r" % (
        PRED, cache_forged, len(fixtures),
        {True: "ok", False: "dead"}.get(cache_state.get("liveness"), "unproven"), cache_state.get("warm")))

    g_ok, first_fail = 0, None
    grng = random.Random(nonce ^ 0x5DEECE66D)
    for k in range(GEN):
        case = gen_case(grng)
        oracle, tool_out, why = one_run(tool, script, case, False, work, fakebin, ro_dirs, "g%03d-" % k,
                                        "g%d" % k)
        good = (oracle is not None and tool_out is not None and tool_out["stdout"] == oracle["stdout"]
                and tool_out["rc"] == oracle["rc"])
        g_ok += good
        if not good and first_fail is None:
            first_fail = (k, case["args"], oracle, tool_out, why)
    print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN, "" if first_fail is None else
                                             " first_fail=%r" % ((first_fail[0], first_fail[1],
                                                                  first_fail[2], first_fail[3],
                                                                  first_fail[4]),)))

    # clause r: strace a resolving case
    rcase = tempfile.mkdtemp(dir=work, prefix="rcase-")
    rc_files = {
        "home/.config/hyprland-xdg-terminals.list": "Alacritty.desktop\n",
        "home/.local/share/applications/Alacritty.desktop":
            "[Desktop Entry]\nType=Application\nName=Alacritty\nExec=alacritty --class Alacritty\n"
            "Categories=TerminalEmulator;\nTerminalArgExec=--\nTerminalArgDir=--working-directory=\n"
            "TerminalArgTitle=--title\nTerminalArgAppId=--class\nTerminalArgHold=--hold\n",
    }
    rc_exec = ["bin/alacritty"]
    rc_args = ["--print-id", "--print-path", "--print-cmd", "--dir=/", "--title=T", "--app-id=A", "--hold"]
    load_case(rcase, rc_files, rc_exec)
    rc_env = case_env({"XDG_CURRENT_DESKTOP": "Hyprland",
                       "XDG_CONFIG_HOME": "$ROOT/home/.config",
                       "XDG_CONFIG_DIRS": "$ROOT/etc-xdg",
                       "XDG_DATA_HOME": "$ROOT/home/.local/share",
                       "XDG_DATA_DIRS": "$ROOT/usr-share"}, rcase, fakebin, False)
    # the resolver must not open anything under the operator's home: the ambient XDG_* of the agent shell would
    # otherwise be a leak that HOME=<case root> cannot redirect
    tr_open = os.path.join(rcase, "opens.log")
    check_sandbox(subprocess.run(
        sandbox(["/usr/bin/strace", "-f", "-qq", "-e", "trace=openat,open,openat2", "-o", tr_open, script] + rc_args,
                rcase, ro_dirs), input=b"", capture_output=True, env=rc_env, timeout=40))
    try:
        opens = open(tr_open, errors="replace").read().splitlines()
    except OSError:
        opens = []
    home_hits = [ln for ln in opens if ('"' + HOME_DIR + "/") in ln or ('"' + HOME_DIR + '"') in ln]
    if home_hits:
        raise Setup("the pinned script opened a path under the operator's home: %r" % home_hits[0][:160])
    print("%s clause=i resolver_opens_home=%d" % (PRED, len(home_hits)))
    trc = os.path.join(rcase, "trace.log")
    p = run_tool(tool, rc_args, rcase, rc_env, ro_dirs, trace=trc)
    execs, socks = trace_counts(trc)
    trips = trip.close()
    strace_ok = False
    if execs is not None and p is not None:
        interp_ok = (len(execs) == 1 and os.path.basename(execs[0]) in
                     {os.path.basename(sys.executable), os.path.basename(os.path.realpath(sys.executable))})
        strace_ok = interp_ok and not socks
    print("%s clause=r execve=%r socket=%r trips=%d" % (
        PRED, execs, socks, len(trips)))
    if trips:
        print("%s clause=r tripped=%r" % (PRED, b",".join(sorted(set(trips)))[:120].decode("ascii", "replace")))
    readonly = "ok" if (strace_ok and not trips) else "fail"

    met = (selftest == "ok" and readonly == "ok" and fixtures_ok == len(fixtures) and g_ok == GEN)
    print("%s: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=present verdict=%s rev=%s seeds=%d,%d"
          % (PRED, fixtures_ok, len(fixtures), g_ok, GEN, selftest, readonly,
             "TARGET_MET" if met else "TARGET_MISSED", full, SEED, nonce))
    return 0 if met else 1


def smoke(work):
    d = tempfile.mkdtemp(dir=work, prefix="smoke-")
    p = subprocess.run(sandbox(["/bin/true"], d, []), input=b"", capture_output=True)
    if p.returncode != 0:
        raise Setup("bwrap unusable (%r)" % (p.stderr[:200],))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=None)
    ap.add_argument("--fixtures", default=None)
    a = ap.parse_args()
    nonce = a.nonce if a.nonce is not None else int.from_bytes(os.urandom(4), "big")
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        if under(a.work, "/run") or under(a.work, "/proc") or under(a.work, "/dev"):
            raise Setup("work dir under /run, /proc or /dev")
        if under(a.work, "/home"):
            raise Setup("work dir under /home (never the operator's home)")
        for h in hidden_paths(a.repo):
            if under(a.work, h):
                raise Setup("work dir inside a hidden path %s" % h)
        for tool in ("bwrap", "strace"):
            if shutil.which(tool) is None:
                raise Setup("%s missing" % tool)
        smoke(a.work)
        fixtures_path = a.fixtures or os.path.join(HERE, "c1-r47-fixtures.json")
        if not os.path.isabs(fixtures_path):
            fixtures_path = os.path.abspath(fixtures_path)
        work = tempfile.mkdtemp(dir=a.work, prefix="c1-")
        try:
            return score(a.repo, a.rev, work, nonce, fixtures_path)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
