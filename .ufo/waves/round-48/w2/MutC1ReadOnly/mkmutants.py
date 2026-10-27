#!/usr/bin/env python3
"""w2/MutC1ReadOnly - build the no-process/no-write boundary mutants from the frozen reference tool.

Every mutant is the reference tool with ONE hook inserted immediately before `if __name__ == "__main__":`.
The hook runs on every invocation, does its violation, writes a single `R48PROBE ...` line to stderr (which the
frozen counter never compares: run_case/explain_case keep stdout and rc only) and never touches stdout or the
exit status. So a mutant is functionally the reference tool unless the hook raises, and the hook cannot.

Usage: mkmutants.py --ref <mado-terminal.py> --out <dir> [--diff <file>]
"""
import argparse
import difflib
import os
import sys

MARK = 'if __name__ == "__main__":'

HEAD = '''def _r48_probe():
    import hashlib as _hl
    import socket as _sk
    import subprocess as _sp
    import tempfile as _tf
    _r = []
'''

WRITE = HEAD + '''    _tgt = []
    _cache = os.environ.get("XDG_CACHE_HOME")
    if _cache:
        _tgt.append(("cache", os.path.join(_cache, "xdg-terminal-exec")))
    if os.environ.get("HOME"):
        _tgt.append(("homecache", os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")))
    _tgt.append(("tmp", "/tmp/r48-w2-probe"))
    _tgt.append(("treeroot", "r48-w2-probe"))
    for _n, _p in _tgt:
        try:
            _d = os.path.dirname(_p)
            if _d and not os.path.isdir(_d):
                os.makedirs(_d, exist_ok=True)
            with open(_p, "w") as _fh:
                _fh.write("r48-w2\\n")
            _r.append("%s=ok" % _n)
        except OSError as _ex:
            _r.append("%s=%s" % (_n, _errno_name(_ex)))
    try:
        _d = _tf.mkdtemp(prefix="r48-w2-")
        _r.append("mkdtemp=ok:%s" % os.path.basename(_d))
    except OSError as _ex:
        _r.append("mkdtemp=%s" % _errno_name(_ex))
'''

FORK = HEAD + '''    _rd, _wr = os.pipe()
    _pid = os.fork()
    if _pid == 0:
        try:
            os.close(_rd)
            os.write(_wr, _hl.md5(b"r48-w2-probe").hexdigest().encode())
            os.close(_wr)
        finally:
            os._exit(0)
    os.close(_wr)
    _got = os.read(_rd, 32)
    os.close(_rd)
    _st = os.waitpid(_pid, 0)[1]
    _r.append("fork=ok:pid_rc=%d:md5_in_child=%s" % (0 if _st == 0 else 1, _got.decode()[:8]))
'''

SOCKET = HEAD + '''    try:
        _a, _b = _sk.socketpair()
        _a.send(b"r")
        _r.append("socketpair=ok:%r" % (_b.recv(1),))
        _a.close()
        _b.close()
    except OSError as _ex:
        _r.append("socketpair=%s" % _errno_name(_ex))
    try:
        _s = _sk.socket(_sk.AF_INET, _sk.SOCK_STREAM)
        _r.append("socket=ok:fd=%d" % _s.fileno())
        _s.close()
    except OSError as _ex:
        _r.append("socket=%s" % _errno_name(_ex))
    try:
        _u = _sk.socket(_sk.AF_UNIX, _sk.SOCK_STREAM)
        try:
            _u.connect("/r48-w2-no-such.sock")
            _r.append("connect=ok")
        except OSError as _ex:
            _r.append("connect=%s" % _errno_name(_ex))
        _u.close()
    except OSError as _ex:
        _r.append("unixsock=%s" % _errno_name(_ex))
'''

EXECABS = HEAD + '''    try:
        _p = _sp.run(["/oracle/bin/ls", "-d", "/oracle"], capture_output=True, timeout=20)
        _r.append("execabs=ok:rc=%d:out=%r" % (_p.returncode, _p.stdout[:24]))
    except OSError as _ex:
        _r.append("execabs=%s" % _errno_name(_ex))
'''

EXECMISS = HEAD + '''    try:
        _p = _sp.run(["/oracle/bin/r48-w2-no-such-binary"], capture_output=True, timeout=20)
        _r.append("execmiss=ok:rc=%d" % _p.returncode)
    except OSError as _ex:
        _r.append("execmiss=%s" % _errno_name(_ex))
'''

EXECPATH = HEAD + '''    try:
        _p = _sp.run(["ls", "-d", "/oracle"], capture_output=True, timeout=20)
        _r.append("execpath=ok:rc=%d:out=%r" % (_p.returncode, _p.stdout[:24]))
    except OSError as _ex:
        _r.append("execpath=%s" % _errno_name(_ex))
'''

WRITE2 = HEAD + '''    _tgt = [("tmp", "/tmp/r48-w2-b"), ("devshm", "/dev/shm/r48-w2-b"), ("dev", "/dev/r48-w2-b"),
            ("run", "/run/r48-w2-b"), ("vartmp", "/var/tmp/r48-w2-b"), ("root", "/r48-w2-b"),
            ("oraclebin", "/oracle/bin/r48-w2-b"), ("usrlib", "/usr/lib/r48-w2-b"),
            ("proc", "/proc/self/r48-w2-b"), ("etc", "/etc/r48-w2-b"), ("cwd", "r48-w2-b")]
    for _n, _p in _tgt:
        try:
            _d = os.path.dirname(_p)
            if _d and not os.path.isdir(_d):
                os.makedirs(_d, exist_ok=True)
            with open(_p, "w") as _fh:
                _fh.write("r48-w2\\n")
            _r.append("%s=ok" % _n)
        except OSError as _ex:
            _r.append("%s=%s" % (_n, _errno_name(_ex)))
'''

TAIL = '''    sys.stderr.write("R48PROBE " + " ".join(_r) + "\\n")
    sys.stderr.flush()


def _errno_name(ex):
    import errno as _e
    return _e.errorcode.get(getattr(ex, "errno", None), repr(getattr(ex, "errno", None)))


_r48_probe()
''' + MARK

MUTANTS = {"M-WRITE": WRITE, "M-WRITE2": WRITE2, "M-FORK": FORK, "M-SOCKET": SOCKET, "M-EXECABS": EXECABS,
           "M-EXECMISS": EXECMISS, "M-EXECPATH": EXECPATH}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--diff")
    a = ap.parse_args()
    ref = open(a.ref, "rb").read().decode()
    if ref.count(MARK) != 1:
        raise SystemExit("marker %r occurs %d times" % (MARK, ref.count(MARK)))
    os.makedirs(a.out, exist_ok=True)
    diffs = []
    for name, hook in sorted(MUTANTS.items()):
        body = ref.replace(MARK, hook + TAIL)
        p = os.path.join(a.out, name + ".py")
        with open(p, "w") as fh:
            fh.write(body)
        diffs.extend(difflib.unified_diff(ref.splitlines(True), body.splitlines(True),
                                          "ref/mado-terminal.py", name + ".py", n=2))
        print("%s %s bytes=%d" % (name, p, len(body)))
    if a.diff:
        with open(a.diff, "w") as fh:
            fh.writelines(diffs)
        print("diff=%s" % a.diff)


if __name__ == "__main__":
    sys.exit(main())
