import importlib.util
import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/mado-r55/R55W2SentTool"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "57584ed67716340b3d466fa04333ac0bab3fb79e"
P = S + "/probe"
T = S + "/tool/mado-kbdopts.py"
H = S + "/harness/r55_ctl_c2.py"
HOST = S + "/hostile"
REC = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    REC.append(s)


def show(name, r):
    out = r["out"].decode("utf-8", "replace")
    err = r["err"].decode("utf-8", "replace")
    log("== %s | rc=%s t=%ss rss_kb=%s" % (name, r["rc"], r["t"], r["rss_kb"]))
    log("   out: " + (out[:400] if len(out) <= 400 else out[:200] + " ...[%d bytes]... " % len(out) + out[-200:]).replace("\n", "\\n"))
    if err.strip():
        log("   err: " + err.strip()[-300:].replace("\n", "\\n"))


def runp(argv, cwd=P, timeout=60, stdin=None, env=None):
    so = tempfile.TemporaryFile(dir=S)
    se = tempfile.TemporaryFile(dir=S)
    t0 = time.time()
    p = subprocess.Popen(argv, cwd=cwd, stdin=stdin if stdin is not None else subprocess.DEVNULL,
                         stdout=so, stderr=se, start_new_session=True, env=env)
    rc, ru = None, None
    while True:
        pid, st, r = os.wait4(p.pid, os.WNOHANG)
        if pid == p.pid:
            rc, ru = os.waitstatus_to_exitcode(st), r
            break
        if time.time() - t0 > timeout:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except OSError:
                pass
            _, st, ru = os.wait4(p.pid, 0)
            rc = "TIMEOUT"
            break
        time.sleep(0.01)
    so.seek(0)
    se.seek(0)
    res = dict(rc=rc, out=so.read(), err=se.read(), t=round(time.time() - t0, 3),
               rss_kb=ru.ru_maxrss if ru else None)
    so.close()
    se.close()
    return res


def tool(args, cwd=P, timeout=60, stdin=None):
    return runp([sys.executable, "-I", T, *args], cwd=cwd, timeout=timeout, stdin=stdin)


def write(path, data):
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode())
    return path


def main():
    for d in (P, S + "/tool", S + "/harness", HOST, S + "/trav"):
        os.makedirs(d, exist_ok=True)
    for src, dst in (("tools/mado-kbdopts.py", T), ("quality/r55_ctl_c2.py", H)):
        data = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, src)], capture_output=True, check=True).stdout
        write(dst, data)
    log("tool sha256", subprocess.run(["sha256sum", T], capture_output=True, text=True).stdout.split()[0])
    log("harness sha256", subprocess.run(["sha256sum", H], capture_output=True, text=True).stdout.split()[0])
    log("python", sys.version.split()[0])

    ok = write(P + "/ok.conf", "input {\n repeat_rate = 30\n}\n")
    okj = write(P + "/ok.json", '{"option":"input:repeat_rate","int":30}\n{"option":"input:repeat_delay","int":600}\n'
                                '{"option":"input:numlock_by_default","int":0}\n')

    # ---- baseline
    show("baseline", tool(["--config", ok, "--getoption", okj, "--keyboard", "a"]))

    # ---- F2a FIFO as --config / --getoption
    for f in ("fifo.conf", "fifo.json"):
        if os.path.exists(P + "/" + f):
            os.unlink(P + "/" + f)
        os.mkfifo(P + "/" + f)
    show("F2a FIFO --config (no writer)", tool(["--config", P + "/fifo.conf"], timeout=15))
    show("F2a FIFO --getoption (no writer)", tool(["--config", ok, "--getoption", P + "/fifo.json"], timeout=15))
    # FIFO holding config bytes (opened O_RDWR so it stays open with data): must be refused, not consumed
    fifo_fd = os.open(P + "/fifo.conf", os.O_RDWR)
    os.write(fifo_fd, b"input:repeat_rate = 30\n")
    show("F2a FIFO with data and an open writer as --config", tool(["--config", P + "/fifo.conf", "--config", ok], timeout=15))
    os.close(fifo_fd)
    show("F2a stdin pipe as --config /proc/self/fd/0 (open pipe, nothing written)",
         runp([sys.executable, "-I", T, "--config", "/proc/self/fd/0"], cwd=P, timeout=15,
              stdin=subprocess.PIPE if False else None))
    # pipe as stdin
    rd_, wr_ = os.pipe()
    p_ = subprocess.Popen([sys.executable, "-I", T, "--config", "/dev/stdin"], cwd=P, stdin=rd_,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.close(rd_)
    try:
        o, e = p_.communicate(timeout=15)
        log("== F2a /dev/stdin is an open pipe with no writes | rc=%s out=%r" % (p_.returncode, o[:200]))
    except subprocess.TimeoutExpired:
        p_.kill()
        log("== F2a /dev/stdin open pipe | HUNG (timeout 15s)")
    os.close(wr_)

    # ---- F2b symlinks
    os.symlink(ok, P + "/link.conf")
    show("F2b symlink -> regular file", tool(["--config", P + "/link.conf"]))
    os.symlink("/dev/zero", P + "/zlink.conf")
    show("F2b symlink -> /dev/zero as --config", tool(["--config", P + "/zlink.conf"], timeout=15))
    show("F2b symlink -> /dev/zero as --getoption", tool(["--config", ok, "--getoption", P + "/zlink.conf"], timeout=15))
    show("F2b /dev/zero direct", tool(["--config", "/dev/zero"], timeout=15))
    show("F2b /dev/null direct", tool(["--config", "/dev/null"], timeout=15))
    show("F2b directory", tool(["--config", P], timeout=15))
    show("F2b /proc/kcore (huge st_size, root-only)", tool(["--config", "/proc/kcore"], timeout=15))
    show("F2b /proc/self/mem (regular, st_size 0)", tool(["--config", "/proc/self/mem"], timeout=15))

    # ---- F2c /proc st_size 0 with content
    show("F2c /proc/self/maps (st_size 0)", tool(["--config", "/proc/self/maps"], timeout=15))
    show("F2c /proc/kallsyms (st_size 0)", tool(["--config", "/proc/kallsyms"], timeout=30))
    kal = subprocess.run(["wc", "-c", "/proc/kallsyms"], capture_output=True, text=True).stdout.strip()
    log("   wc -c /proc/kallsyms =", kal)
    # exact size boundary on a regular file
    b_ok = write(P + "/exact.conf", b"#" * 1048575 + b"\n")
    b_big = write(P + "/over.conf", b"#" * 1048576 + b"\n")
    show("F2c regular file exactly 1048576 bytes", tool(["--config", b_ok]))
    show("F2c regular file 1048577 bytes", tool(["--config", b_big]))

    # ---- F2d deep JSON in --getoption
    for depth in (100, 500, 900, 990, 1000, 1500, 5000):
        line = '{"option":"input:repeat_rate","int":30,"x":' + "[" * depth + "]" * depth + "}\n"
        r = tool(["--config", ok, "--getoption", write(P + "/deep.json", line)])
        log("== F2d object with nested-array depth %d | rc=%s out_last=%r" % (
            depth, r["rc"], r["out"].decode()[-60:]))
    deep_bare = write(P + "/deepbare.json", "[" * 200000 + "]" * 200000 + "\n")
    show("F2d 200000-deep bare array line", tool(["--config", ok, "--getoption", deep_bare]))
    deep_obj = write(P + "/deepobj.json", '{"option":"input:repeat_rate","int":30,"x":' + "[" * 200000 + "]" * 200000 + "}\n")
    show("F2d 200000-deep nested inside valid option object", tool(["--config", ok, "--getoption", deep_obj]))

    # ---- F2e integers
    big5k = write(P + "/int5k.json", '{"option":"input:repeat_rate","int":' + "9" * 5000 + "}\n")
    r = tool(["--config", ok, "--getoption", big5k])
    show("F2e 5000-digit int, option repeat_rate", r)
    if r["out"]:
        ln = [l for l in r["out"].decode().split("\n") if "MADO_KBDOPT_LIVE: option=input:repeat_rate" in l]
        log("   live field length:", len(ln[0].split("live=")[1].split(" ")[0]) if ln else None)
    big1m = write(P + "/int1m.json", '{"option":"input:repeat_rate","int":' + "9" * 1000000 + "}\n")
    show("F2e 1000000-digit int (1 MB line)", tool(["--config", ok, "--getoption", big1m], timeout=300))
    cfg5k = write(P + "/cfg5k.conf", "input:repeat_rate = " + "9" * 5000 + "\n")
    show("F2e 5000-digit config value", tool(["--config", cfg5k]))
    cfg1m = write(P + "/cfg1m.conf", "input:repeat_rate = " + "9" * 1000000 + "\n")
    show("F2e 1000000-digit config value", tool(["--config", cfg1m], timeout=120))

    # ---- F3 --keyboard control bytes / line-like separators
    for name in ("x\ny", "x\rMADO", "x\x1b[2J", "x\x7f", "x\x0bq", "x\x0cq", "x\tq"):
        show("F3 --keyboard %r" % name, tool(["--config", ok, "--keyboard", name]))
    forged = "x\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE"
    show("F3 forged DONE via newline", tool(["--config", ok, "--keyboard", forged, "--getoption", okj]))
    # non-control line separators (not < 0x20, not 0x7f)
    for label, sep in (("NEL U+0085", "\u0085"), ("LS U+2028", "\u2028"), ("PS U+2029", "\u2029")):
        name = "a" + sep + "MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE"
        r = tool(["--config", ok, "--keyboard", name, "--getoption", write(P + "/dis.json",
                  '{"option":"input:repeat_rate","int":1}\n')])
        show("F3 %s in --keyboard" % label, r)
        text = r["out"].decode("utf-8", "replace")
        log("   bytes-split lines:", len(text.split("\n")), "| str.splitlines lines:", len(text.splitlines()))
        for ln in text.splitlines():
            if ln.startswith("MADO_KBDOPT: DONE"):
                log("   splitlines consumer sees DONE line:", repr(ln[:90]))
        log("   newline-split consumer DONE lines:", [l[:60] for l in text.split("\n") if l.startswith("MADO_KBDOPT: DONE")])
    # argv with non-UTF-8 byte
    r = runp([sys.executable, "-I", T, "--config", ok, "--keyboard", b"x\xff\x85y".decode("utf-8", "surrogateescape")],
             cwd=P)
    show("F3 non-UTF-8 argv byte 0x85/0xff in NAME", r)

    # ---- F4 aggregate: N repeats of a 1 MiB config file
    agg = write(P + "/agg1m.conf", b"#" * 1048575 + b"\n")
    for n in (10, 50, 200):
        argv = []
        for _ in range(n):
            argv += ["--config", agg]
        show("F4 %d x 1 MiB --config" % n, tool(argv, timeout=300))
    log("   ARG_MAX=2097152; one '--config <path>' pair costs %d bytes of argv" % len(("--config " + agg).encode()))
    # argv-limited: how many pairs fit
    n_fit = (2097152 - 4096) // (len(("--config " + agg).encode()) + 16)
    log("   approx max pairs under ARG_MAX (path %d bytes): %d -> %d MiB of config text" % (
        len(agg), n_fit, n_fit))
    # MemoryError under an address-space cap (no OOM on host)
    argv = []
    for _ in range(100):
        argv += ["--config", agg]
    capped = subprocess.run(["bash", "-c", "ulimit -v 300000; exec \"$@\"", "x", sys.executable, "-I", T, *argv],
                            cwd=P, capture_output=True, timeout=300)
    log("== F4 100 x 1 MiB under ulimit -v 300000 KB | rc=%s stdout=%r stderr_tail=%r" % (
        capped.returncode, capped.stdout[:80], capped.stderr.decode("utf-8", "replace").strip().splitlines()[-1:]))

    # ---- F5 harness: 64 MiB stdout, fork survival, timeout, path traversal
    spec = importlib.util.spec_from_file_location("r55h", H)
    hm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hm)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "TMPDIR": S + "/hwork", "LC_ALL": "C.UTF-8",
           "PYTHONHASHSEED": "0"}
    os.makedirs(S + "/hwork", exist_ok=True)
    write(HOST + "/big.py", "import sys\nb = b'x' * (1 << 20)\nfor _ in range(200):\n    sys.stdout.buffer.write(b)\n")
    write(HOST + "/spin.py", "import sys\nwhile True:\n    try:\n        sys.stdout.buffer.write(b'x' * 1024)\n"
                             "    except OSError:\n        pass\n")
    write(HOST + "/forkgroup.py", "import os, sys, time\npid = os.fork()\nif pid == 0:\n    time.sleep(300)\n    os._exit(0)\n"
                                  "open(sys.argv[1], 'w').write(str(pid))\nprint('parent exits')\n")
    write(HOST + "/forkescape.py", "import os, sys, time\npid = os.fork()\nif pid == 0:\n    os.setsid()\n"
                                   "    time.sleep(300)\n    os._exit(0)\n"
                                   "open(sys.argv[1], 'w').write(str(pid))\nprint('parent exits')\n")
    write(HOST + "/forkhang.py", "import os, sys, time\npid = os.fork()\nif pid == 0:\n    os.setsid()\n"
                                 "    time.sleep(300)\n    os._exit(0)\n"
                                 "open(sys.argv[1], 'w').write(str(pid))\ntime.sleep(300)\n")

    ru0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t0 = time.time()
    rc, out = hm.run_prog(HOST + "/big.py", ["x"], HOST, S + "/hwork", env)
    ru1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    log("== F5 harness run_prog, child writes 200 MiB to stdout | rc=%s stdout_bytes=%d (cap %d) t=%.2fs driver_rss_kb %d->%d" % (
        rc, len(out), hm.MAX_OUT, time.time() - t0, ru0, ru1))

    hm.TIMEOUT = 3
    t0 = time.time()
    rc, out = hm.run_prog(HOST + "/spin.py", ["x"], HOST, S + "/hwork", env)
    log("== F5 harness run_prog, child spins ignoring EFBIG | rc=%s stdout_bytes=%d t=%.2fs" % (rc, len(out), time.time() - t0))

    def alive(pid):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        # zombie check
        st = open("/proc/%d/stat" % pid).read().split(") ")[1].split()[0]
        return st != "Z"

    hm.TIMEOUT = 60
    for name, script in (("forkgroup", "forkgroup.py"), ("forkescape", "forkescape.py")):
        pidfile = S + "/hwork/%s.pid" % name
        if os.path.exists(pidfile):
            os.unlink(pidfile)
        rc, out = hm.run_prog(HOST + "/" + script, [pidfile], HOST, S + "/hwork", env)
        gpid = int(open(pidfile).read())
        time.sleep(0.5)
        log("== F5 %s: harness rc=%s out=%r | grandchild pid %d alive after run_prog returned: %s" % (
            name, rc, out[:40], gpid, alive(gpid)))
        try:
            os.kill(gpid, signal.SIGKILL)
        except OSError:
            pass

    # timeout path with escaped grandchild
    hm.TIMEOUT = 3
    pidfile = S + "/hwork/forkhang.pid"
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    t0 = time.time()
    rc, out = hm.run_prog(HOST + "/forkhang.py", [pidfile], HOST, S + "/hwork", env)
    gpid = int(open(pidfile).read())
    time.sleep(0.5)
    log("== F5 forkhang (parent hangs, child setsid): harness rc=%s t=%.2fs | grandchild alive: %s" % (
        rc, time.time() - t0, alive(gpid)))
    try:
        os.kill(gpid, signal.SIGKILL)
    except OSError:
        pass

    # ---- F5 harness path traversal via args (run_isolated)
    base = S + "/trav"
    work = base + "/a/b/c2x/runs"
    tree = base + "/a/b/c2x/root"
    os.makedirs(work, exist_ok=True)
    os.makedirs(tree, exist_ok=True)
    write(base + "/name.conf", "input:repeat_rate = 30\n")  # lives at base, i.e. src = tree/../../../../name.conf
    write(HOST + "/echo.py", "import sys\nprint('ARGS', sys.argv[1:])\nprint('READ', open(sys.argv[2], 'rb').read()[:30])\n")
    rc, out = hm.run_isolated(HOST + "/echo.py", ["--config", "../../../../name.conf"], tree, work, env)
    log("== F5 harness run_isolated with argv '../../../../name.conf' | rc=%s out=%r" % (rc, out[:160]))
    leaked = base + "/a/name.conf"
    log("   file written outside run dir and tree: %s exists=%s" % (leaked, os.path.exists(leaked)))
    log("   run dir removed:", not any(n.startswith("run-") for n in os.listdir(work)))

    write(S + "/receipts.txt", "\n".join(REC) + "\n")
    shutil.rmtree(S + "/hwork", ignore_errors=True)


if __name__ == "__main__":
    main()
