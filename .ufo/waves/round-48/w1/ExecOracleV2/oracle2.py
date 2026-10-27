#!/usr/bin/env python3
"""ORACLE2-r48 - warm-cache judging harness for tools/mado-terminal.py (C1, round 48 w1).

The judge is the resolver itself: xdg-terminal-exec v0.14.3, pinned by PIN_SHA256 (the host's
/usr/bin/xdg-terminal-exec has the same bytes). Nothing of ours judges the answer.

A fixture-v2 case is materialized, optionally primed by a cold resolver run (which writes
$XDG_CACHE_HOME/xdg-terminal-exec in the BACKGROUND, pin:1455 `save_cache "$1" &`), mutated by
`after` with every mtime re-pinned (directories included, so `ls -lR` dates are fixed), and then
scored on the warm run: the oracle prints and the tool must print the same bytes and exit status.

Why priming needs a wrapper (measured, receipt exp1.txt): the pin's background child is a fork of
the resolver's own shell. bwrap --unshare-all makes bwrap PID 1 of a new pid namespace and kills
everything when it exits, so the fork is destroyed before it writes anything - a plain
`bwrap ... /oracle/xdg-terminal-exec --print-cmd` leaves NO cache file, while the same run behind
`/bin/sh -c` with a busy-wait on the cache terminator does. `sh -c '<pin>; wait'` cannot help:
`wait` only reaps the shell's own children, and the writer is a child of the pin, not of the
wrapper. WAIT_CACHE below therefore polls (bash builtins only - the sandbox allowlist has no
sleep, cat or test binary) until the file's last line carries the 0x1e"END_OF_EXEC_USEP"
terminator, and preserves the pin's exit status.

Roots: the resolver hashes `LANG=C ls -LRl` of the config and applications operands, whose
headers are absolute paths, so two different roots produce two different hashes and a cache
primed at one root is stale at the other. Each tree is therefore primed at its own root; the two
caches differ only by the root string (checked as an invariant, `cache_before` normalized).
`--hash-probe` prints both line 1 hashes as a receipt.

Usage:
  oracle2.py --work DIR [--fixtures F] [--tool PATH] [--reps 3] [--json OUT] [--case ID ...]
  oracle2.py --work DIR --emit-expect OUT      # rewrite the fixture file with pin-produced expect
  oracle2.py --work DIR --hash-probe           # two-root hash receipt only

Exit 0 iff every selected case passes every invariant, 1 if a case fails, 2 on setup error.
"""
import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

PRED = "ORACLE2-r48"
HERE = os.path.dirname(os.path.abspath(__file__))
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"
TERMINATOR = "\x1eEND_OF_EXEC_USEP"
CACHE_STATES = (("cache is actual", "hit"), ("cache is out-of-date", "stale"),
                ("invalid cache data", "invalid"), ("reached cache line limit", "invalid"),
                ("no cache data", "absent"), ("cache is disabled", "disabled"))

# bash + [ + read + case only: no external command of the sandbox allowlist is needed, and the
# loop is bounded. Poll for the resolver's background save, then exit with the pin's own status.
WAIT_CACHE = (
    'p="${XDG_CACHE_HOME:-${HOME-}/.cache}/xdg-terminal-exec"; pin=$1; shift; "$pin" "$@"; rc=$?; '
    '[ "$rc" -eq 0 ] || exit "$rc"; '
    'n=0; while [ "$n" -lt 20000 ]; do '
    'if [ -s "$p" ]; then last=; while IFS= read -r l; do last=$l; done < "$p"; '
    'case "$last" in *END_OF_EXEC_USEP) exit "$rc" ;; esac; fi; '
    'n=$((n+1)); done; exit "$rc"')

# The naive way to keep the fork alive: `wait` reaps only the wrapper's own children, and the
# writer is a child of the pin, so it waits for nothing. Kept for the --prime-probe receipt.
WAIT_NAIVE = 'pin=$1; shift; "$pin" "$@"; rc=$?; wait; exit "$rc"'

TRUE_SET = ("true", "True", "TRUE", "yes", "Yes", "YES", "1")


class Setup(Exception):
    pass


def find_lane(start):
    d = os.path.realpath(start)
    while True:
        if os.path.isfile(os.path.join(d, "tools", "mado-terminal.py")):
            return d
        p = os.path.dirname(d)
        if p == d:
            raise Setup("lane root not found above %s" % start)
        d = p


def pinned_blob(path, sha):
    try:
        with open(path, "rb") as fh:
            blob = fh.read()
    except OSError as e:
        raise Setup("cannot read %s: %s" % (path, e))
    got = hashlib.sha256(blob).hexdigest()
    if got != sha:
        raise Setup("%s sha256 %s != %s" % (path, got, sha))
    return blob


def check_bool(v):
    """The pin's check_bool True-set (pin:54-58); anything else is false."""
    return v in TRUE_SET


# ------------------------------------------------------------------------------------------------ sandbox
class Box:
    """Clause-i sandbox of the round-47 counter: every run is a fresh bwrap root with only the
    allowlisted externals, the pin (or python3 + the tool), /dev, /proc and a tmpfs /tmp."""

    def __init__(self, work, pin_src):
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
            fh.write(pinned_blob(pin_src, PIN_SHA256))
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")
        self.python = os.path.realpath(sys.executable)
        self.tool = None
        self.trace = True
        self.trips = []
        self.last_argv = None

    def argv(self, root, env, kind, args, wait=False, wrapper=None):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib",
             "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc",
             "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", rw, rw]
        if kind == "tool":
            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool,
                  "/oracle/tool.py"]
        else:
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        a += ["--chdir", root]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        if kind == "tool":
            a += ["/usr/bin/python3", "-I", "/oracle/tool.py"] + args
        elif wrapper or wait:
            a += ["/bin/sh", "-c", wrapper or WAIT_CACHE, "prime",
                  "/oracle/xdg-terminal-exec"] + args
        else:
            a += ["/oracle/xdg-terminal-exec"] + args
        self.last_argv = a
        return a

    def run(self, root, env, kind, args, wait=False, wrapper=None, timeout=60):
        argv = self.argv(root, env, kind, args, wait=wait, wrapper=wrapper)
        trace = None
        if kind == "tool" and self.trace:
            fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
            os.close(fd)
            argv = [shutil.which("strace", path="/usr/bin"), "-f", "-qq", "-e", TRACE_SET,
                    "-e", "signal=none", "-o", trace] + argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout,
                               env={"PATH": "/usr/bin"})
            res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                   p.stderr.decode("utf-8", "surrogateescape"))
        except subprocess.TimeoutExpired:
            res = (124, "", "")
        if trace:
            self.check_trace(trace)
        return res

    def check_trace(self, path):
        try:
            with open(path, encoding="latin-1") as fh:
                lines = fh.read().splitlines()
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


# ------------------------------------------------------------------------------------------------ fixture trees
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
        make_stub(root, rel)


def make_stub(root, rel):
    if ".." in rel.split("/") or rel.startswith("/"):
        raise Setup("unsafe exec path %r" % rel)
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
    os.chmod(p, 0o755)


def pin_mtimes(root, when):
    """Set atime=mtime=when on every file and directory below root except .rw (the writable
    state area, which the resolver's listing never covers). Deepest first: writing a child bumps
    its parent's mtime. Without this the `ls -lR` dates would depend on the run clock."""
    t = float(when)
    rw = os.path.join(root, ".rw")
    for dp, dns, fns in os.walk(root, topdown=False):
        if dp == rw or dp.startswith(rw + os.sep):
            continue
        for f in fns:
            os.utime(os.path.join(dp, f), (t, t), follow_symlinks=False)
        if dp != root:
            os.utime(dp, (t, t))
    os.utime(root, (t, t))


def base_env(root, case, lang="C.UTF-8"):
    env = {"HOME": os.path.join(root, "home"),
           "PATH": os.path.join(root, "bin") + ":/oracle/bin",
           "XDG_CACHE_HOME": os.path.join(root, ".rw", "cache"),
           "LANG": lang}
    for k, v in case.get("env", {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v.replace("$ROOT", root)
    return env


def score_env(root, case, lang="C.UTF-8"):
    env = base_env(root, case, lang)
    for k, v in case.get("after", {}).get("env", {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v.replace("$ROOT", root)
    return env


def cache_file(root, env):
    d = env.get("XDG_CACHE_HOME")
    if not d:
        home = env.get("HOME")
        if not home:
            return None
        d = os.path.join(home, ".cache")
    return os.path.join(d, "xdg-terminal-exec")


def read_cache(root, env):
    p = cache_file(root, env)
    if not p or not os.path.isfile(p):
        return None
    with open(p, "rb") as fh:
        return fh.read().decode("latin-1")


def install_cache(root, case, env):
    p = cache_file(root, env)
    if not p:
        raise Setup("case %s: cache literal with no cache path" % case.get("id"))
    if not p.startswith(os.path.join(root, ".rw") + os.sep):
        raise Setup("case %s: cache path %s is outside the writable .rw" % (case.get("id"), p))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(case["cache"].replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    os.chmod(p, 0o600)


def apply_after(root, case):
    after = case.get("after") or {}
    for rel, text in (after.get("files") or {}).items():
        if ".." in rel.split("/") or (rel.startswith("/") and not rel.startswith("$ROOT/")):
            raise Setup("unsafe path in case %s after" % case.get("id"))
        rel = rel.replace("$ROOT", root)
        p = os.path.join(root, rel)
        if text is None:
            if os.path.exists(p):
                os.unlink(p)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in after.get("exec_add") or ():
        make_stub(root, rel)
    for rel in after.get("exec_remove") or ():
        p = os.path.join(root, rel)
        if os.path.exists(p):
            os.unlink(p)


def prepare(box, root, case):
    """Materialize, pin dates, prime (or install the literal cache), mutate `after`, re-pin."""
    materialize(root, case)
    if "mtime" in case:
        pin_mtimes(root, case["mtime"])
    pre = base_env(root, case)
    if "cache" in case:
        if "prime" in case:
            raise Setup("case %s: cache literal and prime are exclusive" % case.get("id"))
        install_cache(root, case, pre)
        prime_result = None
    elif "prime" in case:
        prime_args = [a.replace("$ROOT", root) for a in case["prime"]["args"]]
        prime_result = box.run(root, pre, "pin", prime_args, wait=True)
    else:
        prime_result = None
    before = read_cache(root, pre)
    apply_after(root, case)
    after = case.get("after") or {}
    if "mtime" in after:
        pin_mtimes(root, after["mtime"])
    elif "mtime" in case:
        pin_mtimes(root, case["mtime"])
    return {"cache_before": before, "cache_after": read_cache(root, score_env(root, case)),
            "prime_rc": None if prime_result is None else prime_result[0]}


# ------------------------------------------------------------------------------------------------ verdicts
def cache_verdict(stderr, env):
    """What happened at the cache read. The resolver names it on the debug channel (pin:274-296,
    300-343); the only state that leaves no line is the skipped read, which is `disabled`.
    A /disable_cache directive is parsed after the read (pin:1179 before pin:1201), so it can
    never turn a readable cache into `disabled`: it only suppresses the save."""
    dbg = [l for l in stderr.splitlines() if l.startswith("D: ")]
    for needle, name in CACHE_STATES:
        if any(needle in l for l in dbg):
            return name
    v = env.get("XTE_CACHE_ENABLED")
    if v is not None and not check_bool(v):
        return "disabled"
    return None


def parse_mado_line(out):
    lines = [l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
    if not lines:
        return None
    return dict(kv.split("=", 1) for kv in lines[-1][len("MADO_TERM: "):].split() if "=" in kv)


# ------------------------------------------------------------------------------------------------ one case
def observe(box, case, control="tool", trace=True):
    """Three trees, one run each: o the authoritative oracle run, d the same run with XTE_DEBUG=1
    (it names the cache state), t the scored tool run. One run per tree because a cold run's
    background save may or may not land before the sandbox dies: a second run in the same tree
    could see a cache written by the first one and change its verdict."""
    box.trace = trace
    box.trips = []
    base = tempfile.mkdtemp(dir=box.work, prefix="case-")
    ro, rd, rt = (os.path.join(base, x, "r") for x in ("o", "d", "t"))
    mode = case.get("mode", "print")
    try:
        prep = {root: prepare(box, root, case) for root in (ro, rd, rt)}
        eo, ed, et = score_env(ro, case), score_env(rd, case), score_env(rt, case)
        args_o = [a.replace("$ROOT", ro) for a in case["args"]]
        args_d = [a.replace("$ROOT", rd) for a in case["args"]]
        if control == "pin":
            args_t = [a.replace("$ROOT", rt) for a in case["args"]]
        elif mode == "explain":
            args_t = ["explain"]
        else:
            args_t = ["print"] + [a.replace("$ROOT", rt) for a in case["args"]]
        o_rc, o_out, o_err = box.run(ro, eo, "pin", args_o)
        ed = dict(ed)
        ed["XTE_DEBUG"] = "1"
        d_rc, d_out, d_err = box.run(rd, ed, "pin", args_d)
        verdict = cache_verdict(d_err, eo)
        if control == "pin":
            t_rc, t_out, t_err = box.run(rt, et, "pin", args_t)
        else:
            t_rc, t_out, t_err = box.run(rt, et, "tool", args_t)
        cold = None
        if case.get("class") == "warm-diff":
            rc_ = os.path.join(base, "c", "r")
            prepare(box, rc_, case)
            cf = cache_file(rc_, score_env(rc_, case))
            if cf and os.path.isfile(cf):
                os.unlink(cf)
            c_rc, c_out, _ = box.run(rc_, score_env(rc_, case), "pin",
                                     [a.replace("$ROOT", rc_) for a in case["args"]])
            cold = {"rc": c_rc, "stdout": c_out.replace(rc_, "$ROOT")}
        # A cold run forks save_cache; whether that write lands before the namespace dies is a
        # race, so the post-run bytes are only asserted where the resolver cannot save at all:
        # a warm hit never reaches pin:1455 with XTE__CACHE_USED=false.
        post_o, post_t = read_cache(ro, eo), read_cache(rt, et)
        post_ok = (verdict != "hit"
                   or (post_o == prep[ro]["cache_after"] and post_t == prep[rt]["cache_after"]))
        trips = list(box.trips)
        o_norm = (o_rc, o_out.replace(ro, "$ROOT"))
        d_norm = (d_rc, d_out.replace(rd, "$ROOT"))
        t_norm = (t_rc, t_out.replace(rt, "$ROOT"))
        obs = {
            "mode": mode,
            "verdict": verdict,
            "debug_neutral": d_norm == o_norm,
            "oracle": {"rc": o_rc, "stdout": o_norm[1]},
            "scored": {"rc": t_rc, "stdout": t_norm[1],
                       "stderr": t_err.replace(rt, "$ROOT")[:400]},
            "cache_before": cache_shape(prep[ro]["cache_before"], ro),
            "cache_after": cache_shape(prep[ro]["cache_after"], ro),
            "cache_post_ok": post_ok,
            "cache_before_d": cache_shape(prep[rd]["cache_before"], rd),
            "cache_before_t": cache_shape(prep[rt]["cache_before"], rt),
            "cache_after_t": cache_shape(prep[rt]["cache_after"], rt),
            "hash_differs": len({hash_line(prep[x]["cache_before"]) for x in (ro, rd, rt)}) > 1,
            "prime_rc": prep[ro]["prime_rc"],
            "trips": trips,
            "cold": cold,
            "same": o_norm == t_norm,
        }
        if mode == "explain" and control == "tool":
            f = parse_mado_line(t_norm[1]) or {}
            parts = o_norm[1].split("\n")
            if o_rc == 0:
                want = {"selected": parts[0], "path": parts[1] if len(parts) > 1 else "",
                        "verdict": "OK", "cache": verdict}
            else:
                want = {"selected": "-", "path": "-", "verdict": "NO_TERMINAL", "cache": verdict}
            got = {k: f.get(k) for k in want}
            obs["explain"] = {"want": want, "got": got}
            obs["same"] = got == want and t_rc == (0 if o_rc == 0 else 3)
        return obs
    finally:
        shutil.rmtree(base, ignore_errors=True)


def norm(text, root):
    if text is None:
        return None
    return text.replace(root, "$ROOT")


def cache_shape(text, root):
    """Line 1 is the hash of `ls -lR` output whose headers are absolute paths, so it is a
    function of the root; every other line is the answer. Elide line 1 to $HASH so two roots and
    two runs can be compared, and keep the hash separately to prove that it moves."""
    if text is None:
        return None
    head, sep, tail = norm(text, root).partition("\n")
    return "$HASH" + sep + tail


def hash_line(text):
    return None if text is None else text.split("\n", 1)[0]


def judge(case, obs, expect):
    """Return (ok, notes). Every note is a reason, not a score."""
    notes = []
    ok = obs["same"]
    if not obs["same"]:
        if obs.get("explain"):
            notes.append("explain want=%r got=%r" % (obs["explain"]["want"],
                                                     obs["explain"]["got"]))
        else:
            notes.append("mismatch oracle=%r scored=%r" % (
                (obs["oracle"]["rc"], obs["oracle"]["stdout"][:160]),
                (obs["scored"]["rc"], obs["scored"]["stdout"][:160])))
    if not obs["debug_neutral"]:
        notes.append("XTE_DEBUG changed the oracle result")
    if obs["verdict"] is None and case.get("want_cache") is not None:
        notes.append("cache state unresolved (no debug line, no XTE_CACHE_ENABLED)")
    if "want_cache" in case and obs["verdict"] != case["want_cache"]:
        notes.append("fixture invalid: cache=%s want=%s" % (obs["verdict"], case["want_cache"]))
    if not (obs["cache_before"] == obs["cache_before_d"] == obs["cache_before_t"]):
        notes.append("cache_before differs between roots")
    if case.get("prime") and obs["cache_before"] is not None and not obs["hash_differs"]:
        notes.append("primed caches share a hash across roots (the hash ignores the root?)")
    if obs["cache_after"] != obs["cache_after_t"]:
        notes.append("cache_after differs between roots")
    # a warm hit does not fork save_cache at all (pin:1455 is guarded by XTE__CACHE_USED), so the
    # file must be byte identical after the run; for a cold run the background save is
    # non-deterministic by nature (the sandbox usually kills it) and is only recorded
    if not obs["cache_post_ok"]:
        notes.append("a warm hit rewrote the cache")
    if obs.get("cold") is not None:
        cold = obs["cold"]
        if (cold["rc"], cold["stdout"]) == (obs["oracle"]["rc"], obs["oracle"]["stdout"]):
            notes.append("warm-diff case: the warm answer equals the cold one")
    if expect:
        if expect.get("stdout") != obs["oracle"]["stdout"] or expect.get("rc") != obs["oracle"]["rc"]:
            notes.append("oracle drifted from expect")
        if expect.get("verdict") != obs["verdict"]:
            notes.append("verdict drifted from expect (was %r)" % (expect.get("verdict"),))
        if expect.get("cache_before") != obs["cache_before"]:
            notes.append("cache_before drifted from expect")
        if expect.get("cache_after") != obs["cache_after"]:
            notes.append("cache_after drifted from expect")
    return ok and not notes, notes


def expect_of(obs):
    return {"rc": obs["oracle"]["rc"], "stdout": obs["oracle"]["stdout"],
            "verdict": obs["verdict"], "cache_before": obs["cache_before"],
            "cache_after": obs["cache_after"]}


# ------------------------------------------------------------------------------------------------ hash probe
def hash_probe(box, cases):
    """Receipt: the same content at two roots yields two different cache hashes, and the two
    caches are equal once the root is replaced by $ROOT. That is why each tree is primed."""
    rows = []
    for case in cases:
        base = tempfile.mkdtemp(dir=box.work, prefix="probe-")
        try:
            roots = [os.path.join(base, "a", "r"), os.path.join(base, "bbbbbbbb", "deep", "r")]
            cache = {}
            for root in roots:
                materialize(root, case)
                if "mtime" in case:
                    pin_mtimes(root, case["mtime"])
                env = base_env(root, case)
                args = [a.replace("$ROOT", root) for a in case["prime"]["args"]]
                box.run(root, env, "pin", args, wait=True)
                cache[root] = read_cache(root, env) or ""
            if not all(cache[r] for r in roots):
                rows.append({"id": case.get("id"), "no_cache": True, "hashes": ["", ""],
                             "hashes_differ": True, "shape_equal": True, "lines": [0, 0]})
                continue
            h = [hash_line(cache[r]) for r in roots]
            n = [cache_shape(cache[r], r) for r in roots]
            rows.append({"id": case.get("id"), "no_cache": False, "hashes": h,
                         "hashes_differ": h[0] != h[1], "shape_equal": n[0] == n[1],
                         "lines": [len(cache[r].splitlines()) for r in roots]})
        finally:
            shutil.rmtree(base, ignore_errors=True)
    return rows


# ------------------------------------------------------------------------------------------------ prime probe
def prime_probe(box, case, rounds=3):
    """Which way of running the pin leaves a finished cache: the plain run, `sh -c '<pin>; wait'`,
    or a bounded poll for the terminator. Each strategy gets a fresh tree, `rounds` times."""
    rows = []
    for name, wrapper in (("plain", ""), ("wait", WAIT_NAIVE), ("poll", WAIT_CACHE)):
        for i in range(rounds):
            base = tempfile.mkdtemp(dir=box.work, prefix="probe-")
            root = os.path.join(base, "r")
            try:
                materialize(root, case)
                if "mtime" in case:
                    pin_mtimes(root, case["mtime"])
                env = base_env(root, case)
                box.run(root, env, "pin", case["prime"]["args"],
                        wrapper=wrapper or None)
                blob = read_cache(root, env)
                rows.append({"strategy": name, "run": i + 1,
                             "present": blob is not None,
                             "terminated": bool(blob) and blob.rstrip("\n").endswith(TERMINATOR),
                             "bytes": 0 if blob is None else len(blob)})
            finally:
                shutil.rmtree(base, ignore_errors=True)
    return rows


def transplant_probe(box, case):
    """Prove the root scheme: a cache primed at root A is NOT trusted at root B, and rewriting
    the root string inside it does not help - line 1 is a hash over the absolute paths that went
    into `ls -lR`, and the only way to get an equivalent cache is to prime at B itself."""
    base = tempfile.mkdtemp(dir=box.work, prefix="trans-")
    rows = []
    try:
        a = os.path.join(base, "a", "r")
        materialize(a, case)
        if "mtime" in case:
            pin_mtimes(a, case["mtime"])
        ea = base_env(a, case)
        box.run(a, ea, "pin", case["prime"]["args"], wait=True)
        primed = read_cache(a, ea)
        for name, mutate, prime_here in (
                ("verbatim", lambda t, root: t, False),
                ("root-rewritten", lambda t, root: t.replace(a, root), False),
                ("primed-here", None, True)):
            root = os.path.join(base, name, "r")
            materialize(root, case)
            if "mtime" in case:
                pin_mtimes(root, case["mtime"])
            env = base_env(root, case)
            if prime_here:
                box.run(root, env, "pin", case["prime"]["args"], wait=True)
            elif primed:
                install_cache(root, dict(case, cache=mutate(primed, root)), env)
            dbg = dict(env)
            dbg["XTE_DEBUG"] = "1"
            rc, out, err = box.run(root, dbg, "pin", case["args"])
            rows.append({"scheme": name, "verdict": cache_verdict(err, env),
                         "rc": rc, "stdout": out.replace(root, "$ROOT")})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return rows


# ------------------------------------------------------------------------------------------------ main
def load_cases(path):
    with open(path, encoding="utf-8") as fh:
        cases = json.load(fh)
    if not isinstance(cases, list):
        raise Setup("fixtures must be a JSON list")
    return cases


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--fixtures", default=os.path.join(HERE, "fixtures-v2.json"))
    ap.add_argument("--lane", default=None)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--pin", default=None)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--case", action="append", default=[])
    ap.add_argument("--json", default=None)
    ap.add_argument("--emit-expect", default=None)
    ap.add_argument("--hash-probe", action="store_true")
    ap.add_argument("--prime-probe", action="store_true")
    ap.add_argument("--show-argv", default=None, metavar="CASE")
    ap.add_argument("--transplant-probe", action="store_true")
    ap.add_argument("--control", default="tool", choices=("tool", "pin"))
    ap.add_argument("--no-trace", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    try:
        work = os.path.realpath(args.work)
        lane = os.path.realpath(args.lane or find_lane(HERE))
        if os.path.commonpath([work, lane]) == lane:
            raise Setup("--work must lie outside the lane")
        os.makedirs(work, exist_ok=True)
        tool = os.path.realpath(args.tool or os.path.join(lane, "tools", "mado-terminal.py"))
        pin = os.path.realpath(args.pin or os.path.join(lane, ".ufo", "waves", "round-47",
                                                        "fetch", "xdg-terminal-exec"))
        prereq = [os.path.join(lane, "tools", "mado-terminal.py")]
        if args.control == "tool":
            for p in prereq:
                if not os.path.isfile(p):
                    raise Setup("missing %s" % p)
        box = Box(work, pin)
        box.tool = tool
        cases = load_cases(args.fixtures)
        if args.case:
            cases = [c for c in cases if c.get("id") in args.case]
            if not cases:
                raise Setup("no case matched --case")

        if args.transplant_probe:
            case = next(c for c in cases if "prime" in c and c.get("want_cache") == "hit")
            for r in transplant_probe(box, case):
                print("TRANSPLANT %-16s cache=%-6s rc=%d stdout=%r" % (
                    r["scheme"], r["verdict"], r["rc"], r["stdout"]))
            return 0

        if args.show_argv:
            case = next(c for c in cases if c.get("id") == args.show_argv)
            root = os.path.join(os.path.realpath(work), "argv-root", "r")
            env = base_env(root, case)
            for label, kw in (("prime", {"wrapper": WAIT_CACHE}),
                              ("scored", {})):
                a = box.argv(root, env, "tool" if label == "scored" else "pin",
                             (["print"] if label == "scored" else []) + case["args"], **kw)
                print("ARGV %s: %s" % (label, shlex.join(a)))
            return 0

        if args.prime_probe:
            case = next(c for c in cases if "prime" in c)
            rows = prime_probe(box, case, rounds=3)
            for r in rows:
                print("PRIME %-6s run=%d present=%s terminated=%s bytes=%d" % (
                    r["strategy"], r["run"], r["present"], r["terminated"], r["bytes"]))
            by = {}
            for r in rows:
                by.setdefault(r["strategy"], set()).add((r["present"], r["terminated"]))
            print("PRIME case=%s %s" % (case.get("id"),
                  " ".join("%s=%s" % (k, sorted(v)) for k, v in sorted(by.items()))))
            return 0

        if args.hash_probe:
            rows = hash_probe(box, [c for c in cases if "prime" in c])
            for r in rows:
                print("PROBE %-28s %s hashes_differ=%s shape_equal=%s lines=%s %s %s" % (
                    r["id"], "no-cache" if r["no_cache"] else "primed  ",
                    r["hashes_differ"], r["shape_equal"], r["lines"],
                    r["hashes"][0], r["hashes"][1]))
            bad = [r for r in rows if not r["hashes_differ"] or not r["shape_equal"]]
            print("PROBE rows=%d bad=%d" % (len(rows), len(bad)))
            return 1 if bad else 0

        if args.emit_expect:
            out = []
            for case in cases:
                obs = observe(box, case, control="pin" if args.control == "pin" else "tool",
                              trace=not args.no_trace)
                case = dict(case)
                case["expect"] = expect_of(obs)
                out.append(case)
                print("EXPECT %-28s rc=%d verdict=%s" % (case.get("id"), obs["oracle"]["rc"],
                                                         obs["verdict"]))
            with open(args.emit_expect, "w", encoding="utf-8") as fh:
                json.dump(out, fh, indent=1, sort_keys=True)
                fh.write("\n")
            return 0

        results, failures = [], 0
        for case in cases:
            reps = [observe(box, case, control=args.control, trace=not args.no_trace)
                    for _ in range(max(1, args.reps))]
            stable = all(r == reps[0] for r in reps[1:])
            ok, notes = judge(case, reps[0], case.get("expect"))
            if not stable:
                ok = False
                notes.append("not deterministic across %d runs" % len(reps))
            if reps[0]["trips"]:
                ok = False
                notes.append("read-only trip: %r" % (reps[0]["trips"][:2],))
            failures += 0 if ok else 1
            results.append({"id": case.get("id"), "class": case.get("class"), "ok": ok,
                            "stable": stable, "notes": notes, "obs": reps[0]})
            if not args.quiet:
                print("CASE %-28s %-4s stable=%s cache=%s oracle_rc=%d %s" % (
                    case.get("id"), "ok" if ok else "FAIL", "ok" if stable else "no",
                    reps[0]["verdict"], reps[0]["oracle"]["rc"],
                    "; ".join(notes)[:200]))
        kinds = {}
        for r in results:
            kinds.setdefault(r["class"], [0, 0])
            kinds[r["class"]][1] += 1
            kinds[r["class"]][0] += 0 if r["ok"] else 1
        print("ORACLE2-r48: cases=%d pass=%d fail=%d reps=%d control=%s classes=%s" % (
            len(results), len(results) - failures, failures, max(1, args.reps), args.control,
            ",".join("%s:%d/%d" % (k, v[1] - v[0], v[1]) for k, v in sorted(kinds.items()))))
        if args.json:
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"pred": PRED, "cases": results}, fh, indent=1, sort_keys=True)
                fh.write("\n")
        return 0 if failures == 0 else 1
    except Setup as e:
        print("ORACLE2-r48: setup error: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
