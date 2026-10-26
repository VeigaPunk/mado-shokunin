#!/usr/bin/env python3
"""Read-only probe: run a listing tool inside the counter's own bwrap sandbox.

Uses the counter's sandbox_cmd/run_sandboxed/prepare so the mount set, cwd, env
and RLIMIT are exactly the judge's.  Answers, for the w2 cheat seat:

  * is the live stub (mode 0111) readable by the tool, and with which errno?
  * is /tmp (tmpfs) empty, i.e. are sibling fixtures reachable?
  * is the fixture's parent (<tmp>/<opaque>) or the counter's own tree reachable?
  * is the mark directory writable by the tool?
  * does /proc/self/limits expose RLIMIT_NPROC = 1 in file mode?
"""
import importlib.util
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r41-globals-v2.py")
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
spec = importlib.util.spec_from_file_location("c1v2", COUNTER)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
M.NONCE[0] = "c0ffee00deadbeef"

PROBE = r'''import os
import sys

out = []


def show(tag, fn):
    try:
        out.append("%s=%r" % (tag, fn()))
    except OSError as exc:
        out.append("%s=ERRNO%d" % (tag, exc.errno))


def listing(path):
    return sorted(os.listdir(path))[:12]


out.append("cwd=%s" % os.getcwd())
show("cwd_ls", lambda: listing("."))
show("fixture_dir_ls", lambda: listing(".."))
show("tmp_ls", lambda: listing("/tmp"))
show("root_ls", lambda: listing("/"))
show("mark_ls", lambda: listing(os.path.join("..", "mk")))
show("tool_dir_ls", lambda: listing(os.path.dirname(os.path.abspath(sys.argv[0]))))
show("grandparent_ls", lambda: listing(os.path.dirname(os.path.dirname(
    os.path.abspath(os.getcwd())))))
show("home_ls", lambda: listing(os.environ.get("HOME", "/nonexistent")))


def read_stub():
    name = os.path.join(".", "bin", "journalctl")
    fh = open(name, "rb")
    blob = fh.read(16)
    fh.close()
    return blob


show("stub_read", read_stub)
show("stub_mode", lambda: oct(os.stat(os.path.join(".", "bin", "journalctl")).st_mode))


def limits():
    fh = open("/pro" + "c/self/limits")
    text = fh.read()
    fh.close()
    for row in text.split("\n"):
        if row.startswith("Max processes"):
            return row.split()
    return None


show("nproc_limit", limits)


def forge():
    fh = open(os.path.join("..", "mk", "probe-written"), "wb")
    fh.write(b"x")
    fh.close()
    return "wrote"


show("mark_write", forge)
show("environ", lambda: sorted(os.environ))
out.append("pid=%d" % os.getpid())
for line in out:
    print(line)
'''


def run(tag, live, nproc):
    tmp = tempfile.mkdtemp(prefix="probe-" + tag + "-")
    os.chmod(tmp, 0o755)
    try:
        j = M.sample_journal(REV, M.NONCE[0], tag, 2) if live else b"x\n"
        d, fx, mark, jp, stub = M.prepare(tmp, tag, j, live=live)
        td = os.path.join(tmp, M.opaque("probe-" + tag), "tool")
        os.makedirs(td)
        os.chmod(os.path.dirname(td), 0o755)
        os.chmod(td, 0o755)
        tool = os.path.join(td, "probe.py")
        with open(tool, "w") as fh:
            fh.write(PROBE)
        argv = ["--live"] if live else ["--journal-file", jp]
        path = os.path.join(fx, "bin") + ":/usr/bin"
        rc, out, err = M.run_sandboxed(tool, d, argv, path,
                                       ro=[os.path.dirname(tool)], rw=[mark],
                                       cwd=fx,
                                       extra_env={"XDG_RUNTIME_DIR": "/run/user/1000"},
                                       timeout=120, nproc=nproc)
        print("=== fixture=%s live=%s nproc=%s rc=%s" % (tag, live, nproc, rc))
        print(out.decode("utf-8", "replace").rstrip())
        if err:
            print("stderr=%r" % err[:200])
        print("mark_after=%r" % sorted(os.listdir(mark)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    run("live0", True, False)
    run("gen0", False, True)
    run("gen0free", False, False)
