#!/usr/bin/env python3
"""probe.py -- read-only probe of the C1 tripwire design for mado-terminal.py.

Round 47 / wave w1 / seat ExecStraceTrip.  Answers, by measurement on this host:

  L1  does `strace -f -qq -e trace=%process,%network -o LOG` work inside
      `bwrap --unshare-all` (ptrace across a user namespace, yama=1, no seccomp)?
  L2  does the syscall layer count exactly one execve for a pure-Python tool, and
      does it catch os.execv / subprocess / os.system / os.posix_spawn /
      ctypes execve / ctypes execveat / socket(AF_UNIX) / socket(AF_INET)?
  L3  does `sys.addaudithook` (runpy wrapper, python3 -I) catch the same set, and
      does ctypes bypass it?
  L4  can the tool neutralise the audit layer, and does an execve-only filter
      miss real process starts?

Nothing here mutates the host: no package manager, no service, no GUI, no network.
Every scratch file lands under --work (default $TMPDIR/mado-strace-probe).

Usage:
    probe.py [--work DIR] [--keep] [--json]

Exit status: 0 when every expectation held, 1 otherwise, 2 on usage error.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

# --------------------------------------------------------------------------
# fixtures written into the work dir (never into the repo)
# --------------------------------------------------------------------------

BATTERY = r'''
import sys

CASES = {}

CASES["pure"] = 'print("ok")'

CASES["execv"] = """
import os
os.execv("/bin/true", ["true"])
"""

CASES["execv_missing"] = """
import os
os.execv("/nonexistent-mado-probe", ["nope"])
"""

CASES["execve"] = """
import os
os.execve("/bin/true", ["true"], {})
"""

CASES["subprocess"] = """
import subprocess
subprocess.run(["/bin/true"], check=False)
"""

CASES["subprocess_shell"] = """
import subprocess
subprocess.run("true", shell=True, check=False)
"""

CASES["os_system"] = """
import os
os.system("true")
"""

CASES["posix_spawn"] = """
import os
os.posix_spawn("/bin/true", ["true"], {})
"""

CASES["os_spawnv"] = """
import os
os.spawnv(os.P_WAIT, "/bin/true", ["true"])
"""

CASES["fork_only"] = """
import os
pid = os.fork()
if pid == 0:
    os._exit(0)
os.waitpid(pid, 0)
"""

CASES["thread"] = """
import threading
t = threading.Thread(target=lambda: None)
t.start(); t.join()
"""

CASES["ctypes_execve"] = """
import ctypes
libc = ctypes.CDLL(None, use_errno=True)
argv = (ctypes.c_char_p * 2)(b"true", None)
libc.execve(b"/bin/true", argv, None)
"""

CASES["ctypes_execveat"] = """
import ctypes
libc = ctypes.CDLL(None, use_errno=True)
argv = (ctypes.c_char_p * 2)(b"true", None)
libc.syscall(322, ctypes.c_int(-100), ctypes.c_char_p(b"/bin/true"),
             argv, None, ctypes.c_int(0))   # x86_64 execveat
"""

CASES["socket_unix"] = """
import socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
"""

CASES["socket_inet"] = """
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""

CASES["socket_connect_unix"] = """
import socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    s.connect("/nonexistent-mado-sock")
except OSError:
    pass
"""

CASES["socket_ctypes"] = """
import ctypes
libc = ctypes.CDLL(None, use_errno=True)
fd = libc.socket(2, 1, 0)          # AF_INET, SOCK_STREAM
"""

CASES["netlink_getaddrinfo"] = """
import socket
try:
    socket.getaddrinfo("localhost", 0)
except OSError:
    pass
"""

CASES["exitcode"] = "import sys; sys.exit(int(sys.argv[2]))"

if __name__ == "__main__":
    exec(compile(CASES[sys.argv[1]], "<%s>" % sys.argv[1], "exec"),
         {"__name__": "__main__", "sys": sys})
'''

AUDITWRAP = r'''
"""Layer-2 wrapper: install sys.addaudithook, then run the target under runpy."""
import runpy
import sys

EVENTS = []


def hook(event, args):
    if (event.startswith(("os.exec", "os.system", "os.spawn", "os.fork", "os.posix_spawn",
                          "subprocess.", "socket.", "ctypes.", "_posixsubprocess."))
            or event in ("os.system", "os.kill")):
        try:
            shown = tuple(repr(a)[:60] for a in args)
        except Exception:
            shown = ("<unrepr>",)
        EVENTS.append(event)
        sys.stderr.write("AUDIT %s %s\n" % (event, shown))


sys.addaudithook(hook)
target = sys.argv[1]
sys.argv = sys.argv[1:]
try:
    runpy.run_path(target, run_name="__main__")
finally:
    sys.stderr.write("AUDIT_SUMMARY %d\n" % len(EVENTS))
'''

EVASION = r'''
"""Can a tool neutralise or sidestep sys.addaudithook?"""
import sys

CASE = sys.argv[1]

if CASE == "plain_ctypes":
    import ctypes  # noqa: F401

elif CASE == "_ctypes_direct":
    import _ctypes
    h = _ctypes.dlopen(None, 0)
    addr = _ctypes.dlsym(h, "getpid")
    sys.stderr.write("dlsym_addr=%r\n" % (bool(addr),))

elif CASE == "cfptr_sub":
    import _ctypes
    h = _ctypes.dlopen(None, 0)
    addr = _ctypes.dlsym(h, "getpid")
    cls = type("F", (_ctypes.CFuncPtr,),
               {"_flags_": 0, "_restype_": None, "_argtypes_": ()})
    sys.stderr.write("cfptr_result=%r\n" % (cls(addr)(),))

elif CASE == "clearaudit":
    import ctypes
    lib = ctypes.CDLL(None)
    sym = getattr(lib, "PySys_ClearAuditHooks", None)
    sys.stderr.write("PySys_ClearAuditHooks=%r\n" % (sym,))
    if sym is not None:
        sym()
        sys.stderr.write("called\n")
    import os
    os.execv("/bin/true", ["true"])

elif CASE == "monkeypatch":
    sys.audit = lambda *a, **k: None
    import os
    os.execv("/bin/true", ["true"])

elif CASE == "fork_exec_direct":
    import os
    import _posixsubprocess
    r, w = os.pipe()
    try:
        pid = _posixsubprocess.fork_exec(
            [b"/bin/true"], [b"/bin/true"], True, (), None, None,
            -1, -1, -1, -1, -1, -1, r, w, True, False, 0, None, None, None, -1, None)
        sys.stderr.write("spawned pid=%d\n" % pid)
        os.waitpid(pid, 0)
    except Exception as exc:                       # noqa: BLE001
        sys.stderr.write("EXC %r\n" % (exc,))
    finally:
        os.close(r)
        os.close(w)
'''

NOP = 'print("hello")\n'

# --------------------------------------------------------------------------
# strace log parsing
# --------------------------------------------------------------------------

LINE_RE = re.compile(
    r"^\d+\s+(?P<call>execve|execveat|clone|clone3|fork|vfork|"
    r"socket|socketpair|connect|bind|sendmsg|recvmsg|sendto)\((?P<args>.*)$")

EXEC_FAMILY = {"execve", "execveat"}
SOCK_FAMILY = {"socket", "socketpair"}
NET_FAMILY = {"connect", "bind", "sendmsg", "recvmsg", "sendto"}
PROC_FAMILY = {"clone", "clone3", "fork", "vfork"}


def classify(log_text):
    """Return the syscall counters the tripwire rules read."""
    counts = {"exec": 0, "socket": 0, "net": 0, "process": 0, "thread": 0}
    for line in log_text.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        call, args = m.group("call"), m.group("args")
        if call in EXEC_FAMILY:
            counts["exec"] += 1
        elif call in SOCK_FAMILY:
            counts["socket"] += 1
        elif call in NET_FAMILY:
            counts["net"] += 1
        elif call in PROC_FAMILY:
            # a thread is clone(CLONE_THREAD); anything else is a new process
            if "CLONE_THREAD" in args:
                counts["thread"] += 1
            else:
                counts["process"] += 1
    return counts


def tripwire_fires(counts):
    """The rule under test: one interpreter execve, no socket, no new process."""
    return (counts["exec"] != 1
            or counts["socket"] != 0
            or counts["net"] != 0
            or counts["process"] != 0)


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------


class Probe:
    def __init__(self, work, keep=False):
        self.work = os.path.abspath(work)
        self.keep = keep
        self.rows = []
        self.logdir = os.path.join(self.work, "traces")
        self.stubdir = os.path.join(self.work, "stubs")
        for d in (self.work, self.logdir, self.stubdir):
            os.makedirs(d, exist_ok=True)
        os.chmod(self.stubdir, 0o755)
        self.files = {}
        for name, text in (("battery.py", BATTERY), ("auditwrap.py", AUDITWRAP),
                           ("evasion.py", EVASION), ("nop.py", NOP)):
            path = os.path.join(self.work, name)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            self.files[name] = path

    # -- helpers -----------------------------------------------------------

    def record(self, layer, name, ok, detail):
        self.rows.append({"layer": layer, "case": name,
                          "ok": bool(ok), "detail": detail})

    def read(self, path):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                return fh.read()
        except OSError:
            return ""

    def bwrap(self, extra=None, argv=None):
        """Minimal read-only root.  --unshare-all includes the network and pid ns."""
        cmd = [
            "bwrap", "--unshare-all", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/bin", "/bin",
            "--ro-bind", "/sbin", "/sbin",
            "--ro-bind", "/lib", "/lib",
            "--ro-bind", "/lib64", "/lib64",
            "--ro-bind-try", "/etc", "/etc",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--ro-bind", self.work, self.work,
        ]
        # strace must write its log; the log dir is the ONLY writable host path
        cmd += ["--bind", self.logdir, self.logdir]
        if extra:
            cmd += extra
        return cmd + (argv or [])

    def run(self, cmd, **kw):
        return subprocess.run(cmd, capture_output=True, text=True, **kw)

    def strace_case(self, case, script="battery.py", extra_args=(), in_bwrap=True,
                    trace=None):
        log = os.path.join(self.logdir, "%s.%s.st" % (script.split(".")[0], case))
        trace = trace or "%process,%network"
        inner = ["strace", "-f", "-qq", "-e", "trace=" + trace, "-o", log,
                 "python3", "-I", self.files[script], case, *extra_args]
        argv = self.bwrap(argv=inner) if in_bwrap else inner
        proc = self.run(argv)
        return classify(self.read(log)), proc, log

    # -- layers ------------------------------------------------------------

    def layer_strace_bwrap(self):
        """L1: does the syscall layer even work inside the sandbox?"""
        counts, proc, log = self.strace_case("pure", script="nop.py",
                                             in_bwrap=True)
        self.record("L1-bwrap", "strace-under-bwrap", proc.returncode == 0
                    and counts["exec"] == 1,
                    "rc=%d exec=%d socket=%d net=%d process=%d log=%s"
                    % (proc.returncode, counts["exec"], counts["socket"],
                       counts["net"], counts["process"], os.path.basename(log)))

        # no --unshare-all: only user+pid+net namespaces
        log = os.path.join(self.logdir, "partial.st")
        argv = ["bwrap", "--unshare-user", "--unshare-pid", "--unshare-net",
                "--die-with-parent",
                "--ro-bind", "/usr", "/usr", "--ro-bind", "/bin", "/bin",
                "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
                "--ro-bind-try", "/etc", "/etc",
                "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                "--ro-bind", self.work, self.work,
                "--bind", self.logdir, self.logdir,
                "strace", "-f", "-qq", "-e", "trace=%process,%network",
                "-o", log, "python3", "-I", self.files["nop.py"]]
        proc = self.run(argv)
        counts = classify(self.read(log))
        self.record("L1-bwrap", "strace-partial-unshare", proc.returncode == 0
                    and counts["exec"] == 1,
                    "rc=%d exec=%d" % (proc.returncode, counts["exec"]))

        # log via /dev/stderr instead of a writable bind
        log = os.path.join(self.logdir, "stderr.st")
        argv = ["bwrap", "--unshare-all", "--die-with-parent",
                "--ro-bind", "/usr", "/usr", "--ro-bind", "/bin", "/bin",
                "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
                "--ro-bind-try", "/etc", "/etc",
                "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                "--ro-bind", self.work, self.work,
                "strace", "-f", "-qq", "-e", "trace=%process,%network",
                "-o", "/dev/stderr", "python3", "-I", self.files["nop.py"]]
        proc = self.run(argv)
        counts = classify(proc.stderr)
        self.record("L1-bwrap", "strace-log-to-stderr", proc.returncode == 0
                    and counts["exec"] == 1,
                    "rc=%d exec=%d (no writable bind needed)" % (proc.returncode,
                                                                 counts["exec"]))

        # capability/seccomp report from inside the sandbox
        argv = self.bwrap(argv=["/bin/sh", "-c",
                                "grep -E '^(CapEff|NoNewPrivs|Seccomp):' /proc/self/status; "
                                "cat /proc/sys/kernel/yama/ptrace_scope"])
        proc = self.run(argv)
        body = " ".join(proc.stdout.split())
        self.record("L1-bwrap", "sandbox-caps",
                    "CapEff:\t0000000000000000" in proc.stdout
                    or "CapEff:\t0000000000000000".replace("\t", " ") in body,
                    body[:160])

    def layer_syscall_matrix(self):
        """L2: does the syscall layer catch every escape hatch, and only those?"""
        expect_clean = {"pure", "thread"}
        for case in ("pure", "execv", "execv_missing", "execve", "subprocess",
                     "subprocess_shell", "os_system", "posix_spawn", "os_spawnv",
                     "fork_only", "thread", "ctypes_execve", "ctypes_execveat",
                     "socket_unix", "socket_inet", "socket_connect_unix",
                     "socket_ctypes", "netlink_getaddrinfo"):
            counts, proc, log = self.strace_case(case)
            fired = tripwire_fires(counts)
            ok = (not fired) if case in expect_clean else fired
            self.record("L2-syscall", case, ok,
                        "rc=%d exec=%d socket=%d net=%d process=%d thread=%d => %s"
                        % (proc.returncode, counts["exec"], counts["socket"],
                           counts["net"], counts["process"], counts["thread"],
                           "FIRES" if fired else "clean"))

    def layer_filter_gaps(self):
        """L2b: an execve-only filter misses real process starts."""
        for case in ("ctypes_execveat", "fork_only"):
            counts, proc, log = self.strace_case(case, trace="execve")
            self.record("L2b-gaps", "execve-only/" + case,
                        not tripwire_fires(counts),
                        "execve-only filter: exec=%d process=%d => %s"
                        % (counts["exec"], counts["process"],
                           "MISSED" if not tripwire_fires(counts) else "caught"))

    def layer_audit(self):
        """L3: sys.addaudithook coverage, and the ctypes hole."""
        expect_events = {
            "pure": set(),
            "subprocess": {"subprocess.Popen"},
            "os_system": {"os.system"},
            "posix_spawn": {"os.posix_spawn"},
            "fork_only": {"os.fork"},
            "socket_inet": {"socket.__new__"},
            "socket_ctypes": set(),          # ctypes bypasses
            "ctypes_execve": set(),          # ctypes bypasses
        }
        for case, want in expect_events.items():
            argv = self.bwrap(argv=["python3", "-I", self.files["auditwrap.py"],
                                    self.files["battery.py"], case])
            proc = self.run(argv)
            seen = {ln.split()[1] for ln in proc.stderr.splitlines()
                    if ln.startswith("AUDIT ")}
            missing = want - seen
            self.record("L3-audit", case, not missing,
                        "seen=%s want=subset-of-seen%s"
                        % (",".join(sorted(seen)) or "-",
                           "" if not missing else " MISSING=" + ",".join(sorted(missing))))
        # CPython 3.14 raises ctypes.call_function from the C extension for every
        # foreign call, so the FFI route is visible even though the syscall itself
        # is not a Python-level operation.
        for case in ("ctypes_execve", "socket_ctypes"):
            argv = self.bwrap(argv=["python3", "-I", self.files["auditwrap.py"],
                                    self.files["battery.py"], case])
            proc = self.run(argv)
            seen = {ln.split()[1] for ln in proc.stderr.splitlines()
                    if ln.startswith("AUDIT ")}
            self.record("L3-audit", "ffi/" + case,
                        "ctypes.call_function" in seen,
                        "seen=%s (ctypes.call_function fires from _ctypes; "
                        "a ctypes.* deny-list is a hard wall)"
                        % (",".join(sorted(seen)) or "-"))

    def layer_evasion(self):
        """L4: can the tool disable or sidestep the audit layer?"""
        cases = {
            # name: (must-see event, must-be-absent)
            "plain_ctypes": ("ctypes.dlopen", "os.exec"),
            "_ctypes_direct": ("ctypes.dlopen", "os.exec"),
            "cfptr_sub": ("ctypes.call_function", "os.exec"),
            "clearaudit": ("os.exec", None),
            "monkeypatch": ("os.exec", None),
            "fork_exec_direct": ("_posixsubprocess.fork_exec", None),
        }
        for case, (must, absent) in cases.items():
            argv = self.bwrap(argv=["python3", "-I", self.files["auditwrap.py"],
                                    self.files["evasion.py"], case])
            proc = self.run(argv)
            seen = {ln.split()[1] for ln in proc.stderr.splitlines()
                    if ln.startswith("AUDIT ")}
            ok = must in seen and (absent is None or absent not in seen)
            detail = "seen=%s" % (",".join(sorted(seen)) or "-")
            if case == "clearaudit":
                unreachable = "PySys_ClearAuditHooks=None" in proc.stderr
                ok = ok and unreachable
                detail += " symbol_reachable=%s" % (not unreachable)
            self.record("L4-evasion", case, ok, detail)

    def layer_stubs(self):
        """L5: fake binaries for the third layer -- where binding works and where not."""
        stub_x = os.path.join(self.stubdir, "xdg-terminal-exec")
        with open(stub_x, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\necho STUB-XDG >&2\nexit 42\n")
        stub_b = os.path.join(self.stubdir, "bash")
        with open(stub_b, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\necho STUB-BASH >&2\nexit 43\n")
        for p in (stub_x, stub_b):
            os.chmod(p, 0o755)

        argv = self.bwrap(extra=["--ro-bind", stub_x, "/usr/bin/xdg-terminal-exec"],
                          argv=["/usr/bin/xdg-terminal-exec", "--print-id"])
        proc = self.run(argv)
        self.record("L5-stubs", "stub-over-/usr/bin/xdg-terminal-exec",
                    proc.returncode == 42 and "STUB-XDG" in proc.stderr,
                    "rc=%d err=%r" % (proc.returncode, proc.stderr.strip()[:40]))

        argv = self.bwrap(extra=["--ro-bind", stub_b, "/usr/bin/bash"],
                          argv=["/bin/sh", "-c", "echo reached"])
        proc = self.run(argv)
        self.record("L5-stubs", "stub-/usr/bin/bash-does-not-cover-/bin/sh",
                    proc.returncode == 0 and "reached" in proc.stdout,
                    "rc=%d out=%r (/bin and /usr/bin are separate mounts)"
                    % (proc.returncode, proc.stdout.strip()[:20]))

        argv = self.bwrap(extra=["--ro-bind", stub_b, "/bin/bash",
                                 "--ro-bind", stub_b, "/usr/bin/bash"],
                          argv=["/bin/sh", "-c", "echo reached"])
        proc = self.run(argv)
        eloop = "Too many levels of symbolic links" in (proc.stderr or "")
        self.record("L5-stubs", "shell-stub-shebang-recurses",
                    proc.returncode != 0 and eloop,
                    "rc=%d err=%r (a #!/bin/sh stub stubbed over the shells "
                    "resolves to itself)" % (proc.returncode,
                                             (proc.stderr or "").strip()[:60]))

        # the card spells the layer as "fake binaries bound over ... the shells";
        # /usr/bin/sh is a symlink, and bwrap refuses to mount onto a symlink.
        argv = self.bwrap(extra=["--ro-bind", stub_b, "/usr/bin/sh"],
                          argv=["/bin/true"])
        proc = self.run(argv)
        self.record("L5-stubs", "bind-onto-symlink-refused",
                    "Can't mount on symlink destination" in (proc.stderr or ""),
                    "rc=%d err=%r" % (proc.returncode,
                                      (proc.stderr or "").strip()[:70]))

    def layer_exitcodes(self):
        """L6: strace must not perturb the exit status the counter compares."""
        bad = []
        for want in (0, 1, 2, 3, 4, 126):
            counts, proc, log = self.strace_case("exitcode",
                                                 extra_args=(str(want),))
            if proc.returncode != want:
                bad.append("%d->%d" % (want, proc.returncode))
        self.record("L6-exit", "exit-status-passthrough", not bad,
                    "mismatches=%s" % (",".join(bad) or "none"))

    def layer_wrapper(self):
        """L8: the audit wrapper must stay transparent to stdout bytes and exit status."""
        tool = os.path.join(self.work, "transparency.py")
        with open(tool, "w", encoding="utf-8") as fh:
            fh.write('import sys\nprint("h\\u00e9llo")\nprint("diag", file=sys.stderr)\n'
                     'sys.exit(int(sys.argv[1]))\n')
        bad = []
        for want in (0, 1, 2, 3):
            plain = self.run(["python3", "-I", tool, str(want)])
            wrapped = self.run(["python3", "-I", self.files["auditwrap.py"],
                                tool, str(want)])
            if plain.stdout != wrapped.stdout or wrapped.returncode != want:
                bad.append("%d:%r/%d" % (want, wrapped.stdout, wrapped.returncode))
        self.record("L8-wrapper", "stdout+rc-transparent", not bad,
                    "mismatches=%s" % (",".join(bad) or "none"))

    def layer_timing(self):
        """L7: cost of the tripwire (30 runs of the pure tool)."""
        n = 30
        start = time.monotonic()
        for _ in range(n):
            self.strace_case("pure")
        elapsed = time.monotonic() - start
        avg_ms = elapsed * 1000.0 / n
        self.record("L7-cost", "per-run", avg_ms < 500.0,
                    "n=%d total=%.0fms avg=%.0fms" % (n, elapsed * 1000, avg_ms))
        return avg_ms

    # -- driver ------------------------------------------------------------

    def run_all(self):
        self.layer_strace_bwrap()
        self.layer_syscall_matrix()
        self.layer_filter_gaps()
        self.layer_audit()
        self.layer_evasion()
        self.layer_stubs()
        self.layer_exitcodes()
        self.layer_wrapper()
        avg_ms = self.layer_timing()
        return avg_ms

    def report(self, avg_ms):
        width = max(len(r["case"]) for r in self.rows) + 1
        layer = None
        for row in self.rows:
            if row["layer"] != layer:
                layer = row["layer"]
                print("\n[%s]" % layer)
            print("  %-*s %s  %s" % (width, row["case"],
                                     "PASS" if row["ok"] else "FAIL", row["detail"]))
        passed = sum(1 for r in self.rows if r["ok"])
        total = len(self.rows)
        print("\ntripwire cost: %.0f ms/run (bwrap + strace + python3 -I)" % avg_ms)
        print("MADO_STRACE_PROBE: %d/%d expectations" % (passed, total))
        return passed == total


RECOMMENDED = """
RECOMMENDED C1 TRIPWIRE (all three layers, cheapest first)
--------------------------------------------
1. syscall layer (the boundary)
   bwrap --unshare-all --die-with-parent --new-session \\
         --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /sbin /sbin \\
         --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind-try /etc /etc \\
         --proc /proc --dev /dev --tmpfs /tmp \\
         --ro-bind $CASE $CASE --bind $LOGDIR $LOGDIR \\
         strace -f -qq -e trace=%process,%network -o $LOGDIR/trace \\
           python3 -I $TOOL print ...
   PASS iff, after filtering lines by syscall name:
     execve+execveat == 1        (the single python3 execve; >=2 means the tool
                                  started something, even a failed execve counts)
     socket+socketpair == 0
     connect/bind/sendmsg/recvmsg == 0
     clone/clone3/fork/vfork == 0 after discarding lines whose flags contain
                                  CLONE_THREAD (threads are not processes)
   Use the syscall CLASSES (%process,%network), never a hand-written name list:
   -e trace=execve alone misses execveat (ctypes) and misses a bare os.fork.
   strace writes only $LOGDIR, so bind exactly one writable path; alternatively
   -o /dev/stderr needs no writable bind at all.
   Exit status survives strace unchanged (0..126 and 128+signal).

2. audit layer (defence in depth, one line of signal)
   python3 -I auditwrap.py $TOOL ...  where auditwrap installs sys.addaudithook and
   then runpy.run_path(tool, run_name="__main__").  FAIL on any event whose name
   starts with os.exec / os.system / os.spawn / os.fork / os.posix_spawn /
   subprocess. / socket. / ctypes. / _posixsubprocess.
   This layer catches _posixsubprocess.fork_exec (direct call) and all ctypes
   gateways; the tool cannot remove hooks (no API) and PySys_ClearAuditHooks is
   not reachable through ctypes on this host.

3. stub binaries (belt only, optional)
   Bind a NON-SHELL stub (compiled, or #!/bin/false) over /usr/bin/xdg-terminal-exec:
   it takes effect and the tool sees exit 42.
   Do NOT rely on stubbing the shells: /bin is a separate mount from /usr/bin, so
   a bind at /usr/bin/bash leaves /bin/sh intact, and binding a #!/bin/sh stub over
   both /bin/bash and /usr/bin/bash makes /bin/sh resolve to the stub itself
   (ELOOP). The syscall layer already catches every execve; skip the shell stubs.
"""


def main(argv):
    ap = argparse.ArgumentParser(
        prog="probe.py", add_help=True,
        description="Probe the read-only C1 tripwire design (strace + bwrap + audit hook).")
    ap.add_argument("--work", default=None,
                    help="scratch dir (default $TMPDIR/mado-strace-probe)")
    ap.add_argument("--keep", action="store_true",
                    help="keep the work dir instead of removing it on exit")
    ap.add_argument("--json", action="store_true", help="emit the result table as JSON")
    args = ap.parse_args(argv)

    work = args.work or os.path.join(tempfile.gettempdir(), "mado-strace-probe")
    for tool in ("bwrap", "strace", "python3"):
        if shutil.which(tool) is None:
            sys.stderr.write("probe.py: required tool not found: %s\n" % tool)
            return 2

    probe = Probe(work, keep=args.keep)
    avg_ms = probe.run_all()
    ok = probe.report(avg_ms)

    if args.json:
        print(json.dumps({"rows": probe.rows, "avg_ms": round(avg_ms, 1),
                          "work": probe.work}, indent=2))
    else:
        print(RECOMMENDED)
    print("work dir: %s" % probe.work)

    if not args.keep:
        shutil.rmtree(probe.work, ignore_errors=True)
        print("work dir removed (pass --keep to retain)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
