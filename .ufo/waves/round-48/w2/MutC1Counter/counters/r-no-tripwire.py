#!/usr/bin/env python3
"""PRED-C1-r48 - tools/mado-terminal.py predicts which terminal xdg-terminal-exec picks, INCLUDING the warm cache.

Registration: .ufo/waves/round-48/registration.md. The judge is the resolver itself: the upstream script
xdg-terminal-exec v0.14.3 (https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec),
pinned as .ufo/waves/round-47/fetch/xdg-terminal-exec of this counter's lane (PIN_SHA256 below; the host's
/usr/bin/xdg-terminal-exec has the same bytes). No reference implementation of ours judges anything.

Scores one committed revision REV of --repo (revision-addressed git reads with ambient GIT_* removed; nothing in the
repository is written; scratch only under --work, which must lie outside the repository, this counter's lane and that
lane's parent directory). TOOL = tools/mado-terminal.py. TARGET_MET iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest`, run in the sandbox (TMPDIR=/tmp, a fresh tmpfs), exits 0 within 120 s and its
     last stdout line is exactly `MADO_TERMINAL_SELFTEST: N/N passed` (ASCII digits) with N >= 60.
  f  COLD: every fixture of the round-47 file (c1-r47-fixtures.json beside this counter, else in the lane's
     quality/counters; pinned by SHA256_COLD; another byte, or fewer than 100 fixtures, is a setup error) passes in
     two variants: A (case root <work>/fx-XXXX/r, LANG=C.UTF-8) and B (case root <work>/job-<hex>/deep/<hex>/r,
     LANG=en_US.UTF-8). Per variant the case is materialized once per tree (a fixture that declares no cache key has
     one tree for the oracle and one for the tool, identical bytes, written in the same order, at different roots).
     The oracle (the pin, `/oracle/xdg-terminal-exec ARGS`) and the tool (`python3 -I /oracle/tool.py print ARGS`)
     run in the sandbox with the case env; a variant passes when the tool's exit status equals the oracle's and its
     stdout, with its own root replaced by $ROOT, equals the oracle's stdout with the oracle's root replaced by
     $ROOT. stderr is not compared. The oracle's variant-A result must also equal the fixture's recorded `expect`;
     a fixture whose oracle result drifted from its record is a setup error. The round-47 fixture file is used
     unchanged, so this clause is the round-47 cold clause verbatim (harm watch): same 190 cases, same records.
  w  WARM: every fixture of the round-48 file (c1-r48-fixtures.json beside this counter, else in the lane's
     quality/counters; pinned by SHA256_WARM; fewer than 20 is a setup error) passes in the same two variants, with
     the fixture schema v2 preparation applied to EACH tree independently, in this order:
       1. materialize `files` (paths relative to the tree, `$ROOT` substituted; a trailing `/` is a directory; in the
          order `meta.files_order` names first, then the rest in file order, so readdir order is reproducible on the
          same filesystem) and then `exec` stubs (`#!/bin/sh\\nexit 1\\n`, mode 755, never overwriting a file);
       2. if `mtime` (epoch seconds) is given: pin it on every file, then on every directory deepest-first
          (`.rw` excluded), so `ls -lRl` dates are deterministic;
       3. the cache, exactly one of:
          `cache` - write the literal text (`$ROOT` substituted) as the cache file, no priming; or
          `prime` - run THE PIN on that same tree with `prime.args` (default `--print-cmd`; every prime argv must
            carry a print option, so no terminal can be launched) and WAIT for the resolver's background cache
            save: the counter runs it as `/bin/bash -c <waiter> w <cache path> /oracle/xdg-terminal-exec ARGS`,
            the waiter reaps the save (the resolver forks it, so a plain sandbox run leaves no cache at all) and
            returns only when the cache ends with the resolver's `\\x1eEND_OF_EXEC_USEP` terminator, or after a
            bounded spin; nothing is copied between the oracle tree and the tool tree;
       4. if `after` is given: apply its mutations to that tree (`files` {path: text|null} - null deletes a file or a
          whole directory, a trailing `/` creates a directory; `exec_add`; `exec_remove`; `modes` {path: mode};
          `cache_lines` {1-based line: text} / `cache_sub` [[find, replace]] / `cache_append` [line] edit the primed
          cache file, `$ROOT` substituted, never on the cold twin; `env`/`unset` overlay the SCORED env only), then
          re-pin `after.mtime` (default: `mtime`);
       5. the scored run uses the case env overlaid with `after.env` minus `after.unset`, one variant lang.
     The oracle runs with `XTE_DEBUG=1` (its debug() writes stderr only, so stdout and exit status are the judge's);
     the cache state is derived from that stderr: `cache is actual` -> hit, `cache is out-of-date` -> stale,
     `invalid cache data` / `reached cache line limit` / `failed to get fresh hash` -> invalid, `no cache data` ->
     absent, none of these but the `paths:` line (the resolver reached the cache gate) -> disabled, none of these
     and no `paths:` line (the resolver died before the gate, e.g. HOME unset) -> `-` (unreached). The tool tree's cache is
     therefore the resolver's own cache FOR THAT TREE (each tree hashes its own paths, so the two caches differ by
     root: nothing is transplanted). A fixture passes when, in both variants, the tool's exit status and normalized
     stdout equal the oracle's AND, in variant A, (i) the derived state equals the fixture's recorded `state`,
     (ii) the class premise holds, measured at count time on a third tree prepared identically but with no cache
     (the "cold twin"): WARM-DIFFERS -> the cold twin answers differently from the warm run, WARM-SAME -> it answers
     identically, every other class -> no premise. A premise that no longer holds (or a recorded `cold` that no
     longer matches) is a setup error: the fixture no longer demonstrates what it claims on this host.
  x  explain: for every fixture of both files (variant A), a prepared pair per fixture:
       - selected= and path= equal the oracle's `--print-id` and `--print-path` items;
       - cmd= equals the oracle's FIRST `--print-cmd` word, taken from a second oracle run on a second prepared tree
         with `--print-cmd=\\036` so a word may itself contain a newline;
       - cache= equals the state derived from the first run's debug stderr (as in clause w);
       - verdict=OK with exit 0 when the oracle exits 0, selected=- path=- cmd=- verdict=NO_TERMINAL with exit 3
         when the oracle exits 1;
       then, for an oracle exit 0, three captures written under a fresh directory created INSIDE the tool tree's
       `.rw` (tempfile.mkdtemp, then O_EXCL|O_NOFOLLOW files; any OSError there is a clause-x failure for that
       fixture, never an abort): the oracle's own default-delimiter capture -> verdict=AGREE exit 0; that capture
       with its first `.desktop` renamed `.desktoq` -> DIFFER exit 1; that capture cut to its first two items (id
       and path only - the round-47 w2/CritC1Explain hole, a tool that drops or ignores the command line) ->
       DIFFER exit 1.
  g  GEN = 150 cold cases drawn from NONCE by gen_case() (the round-47 generator, unchanged) plus GEN_W = 80 warm
     cases drawn by gen_warm_case() (kind hit/stale/invalid/disabled, each judged like a fixture at count time,
     variant A only; the kind's premise is the derived state - a mismatch is a setup error, because each kind is
     built so that its state cannot depend on the clock). NONCE is --nonce (default: drawn from os.urandom and
     printed), so these cases cannot be precomputed.
  i  isolation (allowlist, stated as the mount set - path absence is bwrap's business, not the clause's): every run
     is `bwrap --unshare-all --die-with-parent --new-session --clearenv` with a fresh root whose mounts are exactly:
     `/` (bwrap tmpfs); `/usr/lib` (the host tree, read-only) and `/lib`, `/lib64` as symlinks to `usr/lib`;
     `/bin/sh` and `/bin/bash` = copies-pointing binds of the host bash; `/oracle/bin` = read-only copies of the
     resolver's seven external commands (tr find awk ls md5sum mkdir rm); `/dev` (bwrap tmpfs carrying host
     devtmpfs device nodes, plus a fresh devpts at /dev/pts); `/proc` (fresh pid namespace); `/tmp` (tmpfs); the
     case root (read-only); the case root's `.rw` (read-write for an oracle run - the resolver saves its cache
     there - and READ-ONLY for a tool run: the tool writes nothing, so a tool that performs the resolver's save
     fails here); when a fixture asks for the default cache location (`default_cache`), `.rw/cache` is additionally
     mounted at `<root>/home/.cache` (same mode as `.rw`); plus, for an oracle run, the pin at
     `/oracle/xdg-terminal-exec`, and for a tool run, `/usr/bin/python3` and the tool at `/oracle/tool.py`.
     No host path outside that set is BOUND. What a path test sees beyond it are bwrap's own empty stub
     directories for the mountpoints (the `/fast/...` chain of --work, `/usr/bin` as the python bind's mountpoint)
     plus, declared residuals, the host `/usr/lib` bytes (all of them, including site-packages and os-release), the
     inherited host UTS name (bwrap sets no --hostname), the `PWD` bwrap injects on --chdir, and `/proc/1/cmdline`
     showing the complete bwrap argv (hence the host --work path as a string). PATH=<root>/bin:/oracle/bin,
     HOME=<root>/home. bwrap or strace missing is a setup error.
  r  read-only: every TOOL run (selftest, fixtures, generated, explain, explain --observed) is executed under
     `strace -f -qq -e trace=execve,execveat,socket,socketpair,connect -o <file outside the sandbox> bwrap ...`;
     after the line recording the execve of the sandboxed python3, any further traced event (a process started, a
     socket made or connected - by the tool or anything it forks) is a trip. readonly=ok iff trips=0 over all runs.
Final line: `PRED-C1-r48: cold=K/F warm=W/V explained=X/T generated=G/N selftest=<ok|fail> readonly=<ok|fail>
tool=<present|absent> verdict=TARGET_MET|TARGET_MISSED`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup failure.
Clause lines `PRED-C1-r48 clause=<x> ...` precede it (rev= and nonce= ride on clause=meta).
Residuals (declared): a tool that carries a model of the resolver (an emulator, or an interpreter for the embedded
script written in Python) is an implementation of it; the oracle is this host's bash, find, awk, ls, md5sum and tr
at count time, so a difference between hosts is a difference of the judge, recorded by the drift check; the warm
clause's determinism rests on the pinned mtimes (chosen far enough in the past that `ls` prints the year form, so
the listing cannot drift across a minute or a six-month boundary) and on the counter's own waiter for the
resolver's background save (the resolver's timing is not the clause's, only its result is); -h/--help and
\\u/\\U delimiter escapes beyond ASCII stay outside the contract (round-47 docstring, unchanged); a cache file the
resolver would have to write outside the sandbox's writable `.rw` (an unreadable cache, a cache path under a
read-only tree) is not modelled.
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

PRED = "PRED-C1-r48"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mado-terminal.py"
SELFTEST_MIN = 60
GEN = 150
GEN_W = 80
MIN_FIXTURES_COLD = 100
MIN_FIXTURES_WARM = 20
NAME_COLD = "c1-r47-fixtures.json"
NAME_WARM = "c1-r48-fixtures.json"
SHA256_COLD = "4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86"
SHA256_WARM = "4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa"
PIN_REL = os.path.join(".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"
CACHE_TERMINATOR = "\x1eEND_OF_EXEC_USEP"
STATES = ("absent", "hit", "stale", "invalid", "disabled", "-")
# Old enough that `ls -l` prints "Mon dd  YYYY" instead of "Mon dd HH:MM": the listing cannot drift with the clock.
PINNED_MTIME = 1600000000
WAITER = r'''set +e
xte__cache=$1; shift
"$@"
xte__rc=$?
xte__n=0
while [ "$xte__n" -lt 1200 ]; do
	xte__ok=
	if [ -f "$xte__cache" ]; then
		while IFS= read -r xte__l || [ -n "$xte__l" ]; do
			case "$xte__l" in *$'\036'END_OF_EXEC_USEP) xte__ok=1 ;; esac
		done < "$xte__cache" 2>/dev/null
	fi
	if [ -n "$xte__ok" ]; then break; fi
	xte__n=$((xte__n + 1)); xte__z=0
	while [ "$xte__z" -lt 400 ]; do xte__z=$((xte__z + 1)); done
done
exit "$xte__rc"
'''


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


def lane_root():
    """The directory holding tools/mado-terminal.py, found above this counter's directory."""
    p = os.path.realpath(HERE)
    while p != "/":
        if os.path.isfile(os.path.join(p, "tools", "mado-terminal.py")):
            return p
        p = os.path.dirname(p)
    raise Setup("lane root (tools/mado-terminal.py) not found above %s" % HERE)


def beside(name):
    """A counter-side data file: beside this counter when the L1 has installed it, else where the lane keeps it."""
    p = os.path.join(HERE, name)
    if os.path.isfile(p):
        return p
    return os.path.join(lane_root(), "quality", "counters", name)


def pinned(path, sha):
    try:
        blob = open(path, "rb").read()
    except OSError:
        raise Setup("missing %s" % os.path.basename(path))
    if hashlib.sha256(blob).hexdigest() != sha:
        raise Setup("sha256 mismatch %s" % os.path.basename(path))
    return blob


def check_case(case, name):
    if not isinstance(case, dict):
        raise Setup("%s: case is not an object" % name)
    for k in ("id", "class", "env", "files", "exec", "args"):
        if k not in case:
            raise Setup("%s: case without %r" % (name, k))
    if not isinstance(case["expect"], dict) or set(case["expect"]) != {"rc", "stdout"}:
        raise Setup("%s: case %s: expect must be {rc, stdout}" % (name, case["id"]))
    if "mtime" in case and not isinstance(case["mtime"], int):
        raise Setup("%s: case %s: mtime must be an integer" % (name, case["id"]))
    if "cache" in case and case.get("prime"):
        raise Setup("%s: case %s: cache and prime are exclusive" % (name, case["id"]))
    if "state" in case and case["state"] not in STATES:
        raise Setup("%s: case %s: unknown state %r" % (name, case["id"], case["state"]))
    if "prime" in case:
        pargs = (case["prime"] or {}).get("args") or ["--print-cmd"]
        if not any(a == "--test" or a.startswith("--print-") for a in pargs):
            raise Setup("%s: case %s: prime args would launch a terminal" % (name, case["id"]))
    if not any(a == "--test" or a.startswith("--print-") for a in case["args"]):
        raise Setup("%s: case %s: args would launch a terminal" % (name, case["id"]))
    if case.get("default_cache"):
        if "XDG_CACHE_HOME" in (case.get("env") or {}) or "HOME" in (case.get("unset") or []):
            raise Setup("%s: case %s: default_cache needs HOME and no XDG_CACHE_HOME" % (name, case["id"]))
    else:
        home = (case.get("env") or {}).get("XDG_CACHE_HOME")
        if home is not None and not str(home).startswith("$ROOT/.rw"):
            raise Setup("%s: case %s: XDG_CACHE_HOME must be under $ROOT/.rw" % (name, case["id"]))
    after = case.get("after") or {}
    if set(after) - {"files", "exec_add", "exec_remove", "env", "unset", "mtime", "modes", "cache_lines", "cache_sub",
                     "cache_append"}:
        raise Setup("%s: case %s: unknown after key" % (name, case["id"]))
    if "mtime" in after and not isinstance(after["mtime"], int):
        raise Setup("%s: case %s: after.mtime must be an integer" % (name, case["id"]))
    return case


def load_fixtures(path, sha, minimum):
    fx = json.loads(pinned(path, sha).decode())
    if not isinstance(fx, list) or len(fx) < minimum:
        raise Setup("%s: fewer than %d fixtures" % (os.path.basename(path), minimum))
    for case in fx:
        check_case(case, os.path.basename(path))
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
            fh.write(pinned(os.path.join(lane_root(), PIN_REL), PIN_SHA256))
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")
        self.python = os.path.realpath(sys.executable)
        self.tool = tool_path
        self.trips = []

    def prefix(self, root, tool, default_cache):
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        mode = "--ro-bind" if tool else "--bind"
        if root:
            a += ["--ro-bind", root, root, mode, os.path.join(root, ".rw"), os.path.join(root, ".rw")]
            if default_cache:
                a += [mode, os.path.join(root, ".rw", "cache"), os.path.join(root, "home", ".cache")]
        if tool:
            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool, "/oracle/tool.py"]
        else:
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        a += ["--chdir", root or "/tmp"]
        return a

    def argv(self, root, env, tool, args, default_cache=False):
        a = self.prefix(root, tool, default_cache)
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if tool:
            a += ["/usr/bin/python3", "-I", "/oracle/tool.py"] + args
        else:
            a += ["/oracle/xdg-terminal-exec"] + args
        return a

    def run(self, root, env, tool, args, timeout=60, default_cache=False):
        """Returns (rc, stdout, stderr). Tool runs are traced (clause r)."""
        argv = self.argv(root, env, tool, args, default_cache)
        trace = None
        if tool:
            fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
            os.close(fd)
            argv = [self.strace, "-f", "-qq", "-e", TRACE_SET, "-e", "signal=none", "-o", trace] + argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                   p.stderr.decode("utf-8", "surrogateescape"))
        except subprocess.TimeoutExpired:
            res = (124, "", "")
        if trace:
            self.check_trace(trace)
        return res

    def prime(self, root, env, args, cache_path, default_cache=False, timeout=120):
        """Run the pin once and wait for its background cache save (see the clause-w docstring)."""
        a = self.prefix(root, False, default_cache)
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        a += ["/bin/bash", "-c", WAITER, "w", cache_path, "/oracle/xdg-terminal-exec"] + list(args)
        try:
            p = subprocess.run(a, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            return p.returncode, p.stdout.decode("utf-8", "surrogateescape")
        except subprocess.TimeoutExpired:
            return 124, ""

    def check_trace(self, path):
        try:
            lines = open(path, encoding="latin-1").read().splitlines()
        except OSError:
            self.trips.append("trace-missing")
            return
        seen = False
        py_pid = None
        trip = re.compile(r"^(execve|execveat|socket|socketpair|connect)\(")
        for ln in lines:
            pid, _, rest = ln.partition(" ")
            rest = rest.strip()
            # strace attach noise ("???", "<detached ...>") and resume/exit
            # tails ("<... socket resumed>", "+++ exited") are not new
            # invocations; a trip is a traced syscall name at column 0
            # followed by '('. Round-48 flake: two ??? lines once scored as
            # trips under bwrap's own threads.
            if rest.startswith("<..."):
                continue
            if not seen:
                if 'execve("/usr/bin/python3"' in rest:
                    py_pid = pid
                    seen = rest.endswith("= 0")
                elif pid == py_pid and rest.startswith("<... execve resumed>"):
                    seen = rest.endswith("= 0")
                continue
            if trip.match(rest):
                self.trips.append(rest[:60])
        if not seen:
            self.trips.append("python-execve-not-seen")
        os.unlink(path)


# ------------------------------------------------------------------------------------------------ case plumbing
def safe_rel(root, rel):
    if not isinstance(rel, str) or rel.startswith("/") or ".." in rel.split("/"):
        raise Setup("unsafe path %r" % (rel,))
    return os.path.join(root, rel)


def encode(text, root):
    return text.replace("$ROOT", root).encode("utf-8", "surrogateescape")


def write_files(root, files, mode="wb", order=None):
    names = list(order or []) + [r for r in files if r not in (order or [])]
    for rel in names:
        text = files[rel]
        if rel.endswith("/"):
            os.makedirs(safe_rel(root, rel), exist_ok=True)
            continue
        p = safe_rel(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, mode) as fh:
            fh.write(encode(text, root))


def add_execs(root, execs):
    for rel in execs:
        p = safe_rel(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def materialize(root, case):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    if case.get("default_cache"):
        # bwrap needs a real mountpoint for the .rw/cache alias; `home` is not hashed, so this dir is invisible.
        os.makedirs(os.path.join(root, "home", ".cache"))
    write_files(root, case["files"], order=(case.get("meta") or {}).get("files_order"))
    add_execs(root, case["exec"])


def apply_mtime(root, t):
    """Pin mtime on every file, then every directory deepest-first (`.rw` excluded: it is not hashed)."""
    files, dirs = [], []
    for d, ds, fs in os.walk(root):
        if os.path.relpath(d, root).split(os.sep)[0] == ".rw":
            ds[:] = []
            continue
        for f in fs:
            files.append(os.path.join(d, f))
        for x in ds:
            p = os.path.join(d, x)
            if os.path.relpath(p, root).split(os.sep)[0] != ".rw":
                dirs.append(p)
    for p in files:
        os.utime(p, (t, t))
    for p in sorted(dirs, key=lambda x: x.count(os.sep), reverse=True):
        os.utime(p, (t, t))


def cache_host(root):
    return os.path.join(root, ".rw", "cache", "xdg-terminal-exec")


def cache_inside(root, case):
    """The cache path as the resolver computes it inside the sandbox."""
    if case.get("default_cache"):
        return os.path.join(root, "home", ".cache", "xdg-terminal-exec")
    return cache_host(root)


def case_env(case, root, lang, phase):
    e = dict(case["env"])
    unset = set(case.get("unset") or [])
    if phase == "scored":
        a = case.get("after") or {}
        for k, v in (a.get("env") or {}).items():
            e[k] = v
        unset |= set(a.get("unset") or [])
    out = {k: v.replace("$ROOT", root) for k, v in e.items() if v is not None}
    for k in unset:
        out.pop(k, None)
    if "HOME" not in unset:
        out["HOME"] = os.path.join(root, "home")
    if "PATH" not in unset:
        out["PATH"] = os.path.join(root, "bin") + ":/oracle/bin"
    if "LANG" not in unset:
        out["LANG"] = lang
    if "XDG_CACHE_HOME" not in unset:
        if case.get("default_cache"):
            out.pop("XDG_CACHE_HOME", None)
        else:
            out["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    return out


def apply_after(root, after, with_cache=True):
    for rel, text in (after.get("files") or {}).items():
        p = safe_rel(root, rel)
        if text is None:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p)
            elif os.path.lexists(p):
                os.unlink(p)
        elif rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(encode(text, root))
    add_execs(root, after.get("exec_add") or [])
    for rel in after.get("exec_remove") or []:
        p = safe_rel(root, rel)
        if os.path.lexists(p):
            os.unlink(p)
    for rel, mode in (after.get("modes") or {}).items():
        os.chmod(safe_rel(root, rel), int(mode))
    if with_cache and (after.get("cache_lines") or after.get("cache_sub") or after.get("cache_append") is not None):
        cp = cache_host(root)
        try:
            text = open(cp, "rb").read().decode("utf-8", "surrogateescape")
        except OSError:
            raise Setup("cache edit on a tree without a cache")
        if after.get("cache_lines"):
            lines = text.split("\n")
            for ln, val in sorted(after["cache_lines"].items(), key=lambda kv: int(kv[0])):
                i = int(ln) - 1
                if i >= len(lines):
                    raise Setup("cache_lines %s beyond the cache" % ln)
                lines[i] = val.replace("$ROOT", root)
            text = "\n".join(lines)
        for old, new in after.get("cache_sub") or []:
            old, new = old.replace("$ROOT", root), new.replace("$ROOT", root)
            if old not in text:
                raise Setup("cache_sub target absent")
            text = text.replace(old, new)
        for ln in after.get("cache_append") or []:
            text = text + ln.replace("$ROOT", root) + "\n"
        with open(cp, "wb") as fh:
            fh.write(text.encode("utf-8", "surrogateescape"))


def prepare(box, root, case, lang, cold=False):
    """Schema v2 preparation of ONE tree (see clause w). `cold` skips the cache step (the cold twin)."""
    materialize(root, case)
    t = case.get("mtime")
    if t is not None:
        apply_mtime(root, t)
    if not cold:
        if "cache" in case:
            p = cache_host(root)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(encode(case["cache"], root))
        elif "prime" in case:
            pargs = [a.replace("$ROOT", root) for a in ((case["prime"] or {}).get("args") or ["--print-cmd"])]
            box.prime(root, case_env(case, root, lang, "prime"), pargs, cache_inside(root, case),
                      case.get("default_cache", False))
    after = case.get("after") or {}
    apply_after(root, after, with_cache=not cold)
    t2 = after.get("mtime", t)
    if t2 is not None:
        apply_mtime(root, t2)


def cache_state(err):
    """Derive the resolver's cache verdict from its XTE_DEBUG stderr (clause w)."""
    if "cache is actual" in err:
        return "hit"
    if "cache is out-of-date" in err:
        return "stale"
    if "invalid cache data" in err or "reached cache line limit" in err or "failed to get fresh hash" in err:
        return "invalid"
    if "no cache data" in err:
        return "absent"
    if "paths:" in err:
        return "disabled"
    return "-"


def warm_kind(case):
    """'hit'/'stale'/'invalid'/'disabled' for a generated warm case, else None."""
    cls = case.get("class", "")
    if cls.startswith("generated-warm-"):
        return cls.rsplit("-", 1)[-1]
    return None


def norm(rc, out, root):
    return rc, out.replace(root, "$ROOT")


def variant_roots(box, variant, rng):
    if variant == "A":
        base = tempfile.mkdtemp(dir=box.work, prefix="fx-")
        lang = "C.UTF-8"
    else:
        base = tempfile.mkdtemp(dir=box.work, prefix="job-%08x-" % rng.getrandbits(32))
        base = os.path.join(base, "deep", "%06x" % rng.getrandbits(24))
        lang = "en_US.UTF-8"
    return base, lang


def oracle_side(box, case, root, lang):
    """One scored oracle run: (rc, $ROOT-normalized stdout) plus the cache state its debug stderr names.

    Shared by the score and by the fixture builder, so a recorded `expect` is exactly what clause w measures.
    """
    env = case_env(case, root, lang, "scored")
    env["XTE_DEBUG"] = "1"
    rc, out, err = box.run(root, env, False, [a.replace("$ROOT", root) for a in case["args"]],
                           default_cache=case.get("default_cache", False))
    return norm(rc, out, root), cache_state(err)


def run_case(box, case, variant, rng):
    """Returns (ok, warm_norm, why, state, cold_norm)."""
    base, lang = variant_roots(box, variant, rng)
    ro, rt = os.path.join(base, "o", "r"), os.path.join(base, "t", "r")
    dc = case.get("default_cache", False)
    for r in (ro, rt):
        prepare(box, r, case, lang)
    o_norm, state = oracle_side(box, case, ro, lang)
    et = case_env(case, rt, lang, "scored")
    t_rc, t_out, _t_err = box.run(rt, et, True, ["print"] + [a.replace("$ROOT", rt) for a in case["args"]],
                                  default_cache=dc)
    cold = None
    if case.get("prime") or "cache" in case:
        rcold = os.path.join(base, "c", "r")
        prepare(box, rcold, case, lang, cold=True)
        cold, _c_st = oracle_side(box, case, rcold, lang)
    t_norm = norm(t_rc, t_out, rt)
    shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    ok = o_norm == t_norm
    why = "" if ok else "oracle=%r tool=%r" % ((o_norm[0], o_norm[1][:160]), (t_norm[0], t_norm[1][:160]))
    return ok, o_norm, why, state, cold


def check_premise(case, state, cold):
    """Clause w: the fixture still demonstrates what it claims (Setup otherwise)."""
    cls = case["class"]
    if "state" in case and state != case["state"]:
        raise Setup("case %s: cache state is %r, recorded %r" % (case["id"], state, case["state"]))
    if "cold" in case:
        if cold is None:
            raise Setup("case %s: records a cold twin it cannot measure" % case["id"])
        if [cold[0], cold[1]] != [case["cold"]["rc"], case["cold"]["stdout"]]:
            raise Setup("case %s: cold twin drifted" % case["id"])
    if cls == "WARM-DIFFERS":
        if cold is None:
            raise Setup("case %s: WARM-DIFFERS without a cold twin" % case["id"])
        if [cold[0], cold[1]] == [case["expect"]["rc"], case["expect"]["stdout"]]:
            raise Setup("case %s: warm answer no longer differs from the cold one" % case["id"])
    if cls == "WARM-SAME" and cold is not None:
        if [cold[0], cold[1]] != [case["expect"]["rc"], case["expect"]["stdout"]]:
            raise Setup("case %s: warm answer differs from the cold one" % case["id"])
    kind = warm_kind(case)
    if kind is not None and state != kind:
        raise Setup("case %s: kind %r but the oracle derived %r" % (case["id"], kind, state))


def explain_case(box, case, rng):
    """Clause x: selected/path/cmd/cache named as the oracle sees them, and --observed both ways."""
    why = ""
    base, lang = variant_roots(box, "A", rng)
    dc = case.get("default_cache", False)
    ro, ro2, rt = os.path.join(base, "o", "r"), os.path.join(base, "p", "r"), os.path.join(base, "t", "r")
    try:
        for r in (ro, ro2, rt):
            prepare(box, r, case, lang)
        three = ["--print-id", "--print-path", "--print-cmd"]
        eo = case_env(case, ro, lang, "scored")
        eo["XTE_DEBUG"] = "1"
        o_rc, o_out, o_err = box.run(ro, eo, False, three, default_cache=dc)
        state = cache_state(o_err)
        o_norm = o_out.replace(ro, "$ROOT")
        eo2 = case_env(case, ro2, lang, "scored")
        rc2, out2, _ = box.run(ro2, eo2, False, ["--print-id", "--print-path", "--print-cmd=\\036",
                                                 "--print-delimiter=\\036"], default_cache=dc)
        cmd_word = None
        if o_rc == 0:
            if rc2 != 0:
                why = "oracle exited %d on the cmd probe" % rc2
            else:
                items = out2.split("\x1e")
                if len(items) < 3:
                    why = "oracle cmd probe printed %d item(s)" % len(items)
                else:
                    cmd_word = items[2].replace(ro2, "$ROOT")
        et = case_env(case, rt, lang, "scored")
        t_rc, t_out, _ = box.run(rt, et, True, ["explain"], default_cache=dc)
        lines = [l for l in t_out.replace(rt, "$ROOT").split("\n") if l.startswith("MADO_TERM: ")]
        if not why:
            if not lines:
                why = "no MADO_TERM line"
            else:
                f = term_line(lines[-1])
                if f is None:
                    why = "unparseable MADO_TERM line: %r" % lines[-1][:120]
                else:
                    if o_rc == 0:
                        parts = o_norm.split("\n")
                        want = (parts[0], parts[1] if len(parts) > 1 else "", cmd_word, state, "OK", 0)
                    else:
                        want = ("-", "-", "-", state, "NO_TERMINAL", 3)
                    got = (f.get("selected"), f.get("path"), f.get("cmd"), f.get("cache"), f.get("verdict"), t_rc)
                    if got != want:
                        why = "explain got=%r want=%r" % (got, want)
        if not why and o_rc == 0:
            why = observed_case(box, case, rt, et, o_norm, lang)
    except OSError as e:
        why = "tree error: %s" % str(e)[:120]
    shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return why == "", why


TERM_RE = re.compile(r"MADO_TERM: selected=(.*?) path=(.*?) cmd=(.*?) cache=(\S+) verdict=(\S+)$")


def term_line(line):
    """Parse the fixed `MADO_TERM: selected= path= cmd= cache= verdict=` line, values allowed to hold spaces.

    The fields are located by their literal markers in their contract order, so an id, a path or a command word
    carrying a space survives (the round-47 counter split on whitespace and truncated `cmd=my term` to `my`).
    A value containing a marker of a later field is outside what this parser can read; declared, not scored.
    """
    m = TERM_RE.match(line)
    if not m:
        return None
    return {"selected": m.group(1), "path": m.group(2), "cmd": m.group(3), "cache": m.group(4), "verdict": m.group(5)}


def observed_case(box, case, rt, et, o_norm, lang):
    """The three captures of clause x, written into the tool tree's .rw without ever following a name the tool made."""
    dc = case.get("default_cache", False)
    rw = os.path.join(rt, ".rw")
    try:
        d = tempfile.mkdtemp(dir=rw, prefix="obs-")
    except OSError as e:
        return "observed dir: %s" % str(e)[:120]
    parts = o_norm.split("\n", 2)
    two = (parts[0] + "\n" + (parts[1] if len(parts) > 1 else "") + "\n")
    caps = ((0, o_norm, "AGREE", 0),
            (1, o_norm.replace(".desktop", ".desktoq", 1), "DIFFER", 1),
            (2, two, "DIFFER", 1))
    for idx, text, want_v, want_rc in caps:
        p = os.path.join(d, "cap%d" % idx)
        try:
            fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "wb") as fh:
                fh.write(text.replace("$ROOT", rt).encode("utf-8", "surrogateescape"))
        except OSError as e:
            return "capture %d: %s" % (idx, str(e)[:120])
        rc, out, _ = box.run(rt, et, True, ["explain", "--observed", p], default_cache=dc)
        ls = [l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
        v = ls[-1].rsplit("verdict=", 1)[-1].strip() if ls else ""
        if (v, rc) != (want_v, want_rc):
            return "observed %s: got %s/%d" % (want_v, v, rc)
    return ""


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
WARM_ARGVS = [["--print-cmd"], ["--print-id"], ["--print-id", "--print-path", "--print-cmd"],
              ["--print-cmd", "--dir=/srv"], ["--print-cmd", "--title=t x", "--hold"], ["--test"]]
CONFIGS = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
           "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share"}


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
    env = dict(CONFIGS)
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


def gen_warm_text(rng, n):
    """A valid terminal entry that the resolver will select (so the prime can save a cache)."""
    lines = ["[Desktop Entry]", "Type=Application", "Categories=TerminalEmulator;", "Exec=" + n, "Name=" + n]
    if rng.random() < 0.5:
        lines.append("TryExec=" + n)
    if rng.random() < 0.3:
        lines.append("X-TerminalArgDir=--working-directory=")
    if rng.random() < 0.3:
        lines.append("X-TerminalArgTitle=--title")
    if rng.random() < 0.25:
        lines.append("X-TerminalArgHold=--hold")
    for _ in range(rng.randint(0, 2)):
        lines.append(rng.choice(["GenericName=X", "Comment=Y", "Terminal=false", "Name[de]=Z"]))
    return "\n".join(lines) + "\n"


def same_size_edit(text, n):
    """Change the Exec command word without changing the file's length (the hash must not move)."""
    other = n[:-1] + ("q" if n[-1] != "q" else "z")
    if other == n:
        other = "q" + n[1:]
    out = text.replace("Exec=" + n, "Exec=" + other, 1)
    assert len(out) == len(text) and out != text
    return out


def corrupt_cache(rng):
    head = ["0" * 32, "foot", "/x/foot.desktop", "foot.desktop", ""]
    return rng.choice([
        "",
        "abc\n",
        "\n".join(["0" * 32, "foot", "x", "x", "x", "x", "x", "x", "x", "x", "x"]),           # no terminator
        "\n".join(head + ["\x1eEND_OF_EXEC_USEP"]) + "\n",                                      # terminator too early
        "\n".join(["0" * 32, "foot"] + ["x"] * 60) + "\n",                                       # line limit
        "\n".join(["0" * 32] + ["x"] * 48) + "\n",                                               # 49 lines, no terminator
        "x" * 400 + "\n",                                                                        # one long line
    ])


def gen_warm_case(rng, k):
    kind = ("hit", "stale", "invalid", "disabled")[k % 4]
    n = rng.choice(NAMES)
    eid = n + ".desktop"
    sub = rng.choice(["", "", "vendor/"])
    path = "usr/share/applications/" + sub + (sub.replace("/", "-") + n + ".desktop")
    text = gen_warm_text(rng, n)
    files = {path: text, "home/.config/hyprland-xdg-terminals.list": sub.replace("/", "-") + eid + "\n"}
    if rng.random() < 0.5:
        files["home/.config/xdg-terminals.list"] = sub.replace("/", "-") + eid + "\n"
    if rng.random() < 0.3:
        files["etc/xdg/xdg-terminals.list"] = sub.replace("/", "-") + eid + "\n"
    env = dict(CONFIGS)
    env["XDG_CURRENT_DESKTOP"] = rng.choice(["Hyprland", "Hyprland:GNOME", "hyprland"])
    mt = PINNED_MTIME + rng.choice([0, 60, 7200])
    case = {"id": "w%03d" % k, "class": "generated-warm-" + kind, "env": env, "files": files,
            "exec": ["bin/" + n], "args": list(rng.choice(WARM_ARGVS)), "mtime": mt}
    if kind == "hit":
        case["prime"] = {"args": ["--print-cmd"]}
        case["after"] = {"files": {path: same_size_edit(text, n)}, "mtime": mt}
    elif kind == "stale":
        case["prime"] = {"args": ["--print-cmd"]}
        if rng.random() < 0.5:
            case["after"] = {"files": {path: text + "GenericName=Q\n"}, "mtime": mt}
        else:
            case["after"] = {"mtime": mt + 86400}
    elif kind == "invalid":
        case["cache"] = corrupt_cache(rng)
    else:
        case["cache"] = rng.choice(["", "\n".join(["0" * 32, "foot"] + ["x"] * 12) + "\n"])
        case["env"]["XTE_CACHE_ENABLED"] = rng.choice(["false", "0", "no", "garbage"])
    return case


# ------------------------------------------------------------------------------------------------ score
def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def selftest_clause(box):
    sd = tempfile.mkdtemp(dir=box.work, prefix="st-")
    os.makedirs(os.path.join(sd, ".rw"))
    rc, out, _err = box.run(sd, {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}, True,
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
    cold_fx = load_fixtures(beside(NAME_COLD), SHA256_COLD, MIN_FIXTURES_COLD)
    warm_fx = load_fixtures(beside(NAME_WARM), SHA256_WARM, MIN_FIXTURES_WARM)
    if not shutil.which("strace"):
        raise Setup("strace missing")
    lane = lane_root()
    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    print("%s clause=meta rev=%s nonce=%d lane=%s" % (PRED, full, nonce, lane))
    f_ok = w_ok = x_ok = g_ok = 0
    selftest, readonly = "fail", "fail"
    if present:
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "tool.py")
        with open(tool, "wb") as fh:
            fh.write(git(repo, "show", "%s:%s" % (full, TOOL)))
        box = Box(work, tool)
        selftest = selftest_clause(box)
        rng = random.Random(nonce)
        drift = []
        for fx in cold_fx:
            ok_a, o_a, why_a, st_a, _c_a = run_case(box, fx, "A", rng)
            ok_b, _o_b, why_b, _st_b, _c_b = run_case(box, fx, "B", rng)
            if [o_a[0], o_a[1]] != [fx["expect"]["rc"], fx["expect"]["stdout"]]:
                drift.append(fx["id"])
            ok = ok_a and ok_b
            f_ok += ok
            print("%s clause=f fixture=%s %s%s" % (PRED, fx["id"], "pass" if ok else "FAIL",
                                                  "" if ok else " " + "; ".join(w for w in (why_a, why_b) if w)))
        print("%s clause=f cold=%d/%d" % (PRED, f_ok, len(cold_fx)))
        for fx in warm_fx:
            ok_a, o_a, why_a, st_a, cold_a = run_case(box, fx, "A", rng)
            ok_b, _o_b, why_b, _st_b, _c_b = run_case(box, fx, "B", rng)
            if [o_a[0], o_a[1]] != [fx["expect"]["rc"], fx["expect"]["stdout"]]:
                drift.append(fx["id"])
            check_premise(fx, st_a, cold_a)
            ok = ok_a and ok_b
            w_ok += ok
            print("%s clause=w fixture=%s class=%s state=%s %s%s" % (
                PRED, fx["id"], fx["class"], st_a, "pass" if ok else "FAIL",
                "" if ok else " " + "; ".join(w for w in (why_a, why_b) if w)))
        print("%s clause=w warm=%d/%d" % (PRED, w_ok, len(warm_fx)))
        if drift:
            raise Setup("oracle drifted from %d recorded fixture(s): %s" % (len(drift), ",".join(drift[:5])))
        for fx in cold_fx + warm_fx:
            ok, why = explain_case(box, fx, rng)
            x_ok += ok
            if not ok:
                print("%s clause=x fixture=%s FAIL %s" % (PRED, fx["id"], why[:300]))
        print("%s clause=x explained=%d/%d" % (PRED, x_ok, len(cold_fx) + len(warm_fx)))
        grng = random.Random(nonce ^ 0x47C1)
        first_fail = None
        for k in range(GEN):
            case = gen_case(grng, k)
            ok, _o, why, _st, _c = run_case(box, case, "A", grng)
            g_ok += ok
            if not ok and first_fail is None:
                first_fail = (case["id"], why)
        for k in range(GEN_W):
            case = gen_warm_case(grng, k)
            ok, _o, why, st, cold = run_case(box, case, "A", grng)
            check_premise(case, st, cold)
            g_ok += ok
            if not ok and first_fail is None:
                first_fail = (case["id"], why)
        print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN + GEN_W, "" if first_fail is None else
                                                 " first_fail=%r" % (first_fail,)))
        readonly = "ok"
        print("%s clause=r trips=%d %s" % (PRED, len(box.trips), ";".join(sorted(set(box.trips)))[:200]))
    total_fx = len(cold_fx) + len(warm_fx)
    met = (present and selftest == "ok" and readonly == "ok" and f_ok == len(cold_fx) and w_ok == len(warm_fx)
           and g_ok == GEN + GEN_W and x_ok == total_fx)
    print("%s: cold=%d/%d warm=%d/%d explained=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s verdict=%s" % (
        PRED, f_ok, len(cold_fx), w_ok, len(warm_fx), x_ok, total_fx, g_ok, GEN + GEN_W, selftest, readonly,
        "present" if present else "absent", "TARGET_MET" if met else "TARGET_MISSED"))
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
        work = tempfile.mkdtemp(dir=a.work, prefix="c1r48-")
        try:
            return score(a.repo, a.rev, work, nonce)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
