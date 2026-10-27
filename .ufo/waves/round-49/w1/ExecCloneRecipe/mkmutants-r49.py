#!/usr/bin/env python3
"""w1/ExecCloneRecipe - clause-r mutants for PRED-C1-r48-v2.

Each mutant is `tools/mado-terminal.py` at the lane tip with ONE hook inserted immediately before
`if __name__ == "__main__":`. The hook runs on every invocation (import time), performs ONE boundary
violation, reports what happened on stderr (the counter compares stdout and rc only) and never touches
stdout or the exit status. No hook writes anywhere outside a bwrap tmpfs: the only write targets are
/tmp/r49-w1-probe and tempfile.mkdtemp(), both inside the sandbox's own tmpfs; HOME is never a target.

Usage: mkmutants-r49.py --ref tools/mado-terminal.py --out <dir> [--diff <file>]
"""
import argparse
import difflib
import os

MARK = 'if __name__ == "__main__":'

HEAD = '''def _r49_probe():
    import errno as _errno
    import tempfile as _tf
    _r = []

    def _en(ex):
        return _errno.errorcode.get(getattr(ex, "errno", None), repr(getattr(ex, "errno", None)))
'''

TAIL = '''    sys.stderr.write("R49PROBE " + " ".join(_r) + "\\n")
    sys.stderr.flush()


_r49_probe()
''' + MARK

WRITE = HEAD + '''    for _n, _p in (("tmp", "/tmp/r49-w1-probe"), ("cwd", "r49-w1-probe")):
        try:
            with open(_p, "w") as _fh:
                _fh.write("r49-w1\\n")
            _r.append("%s=ok" % _n)
        except OSError as _ex:
            _r.append("%s=%s" % (_n, _en(_ex)))
    try:
        _d = _tf.mkdtemp(prefix="r49-w1-")
        _r.append("mkdtemp=ok:%s" % os.path.basename(_d))
    except OSError as _ex:
        _r.append("mkdtemp=%s" % _en(_ex))
'''

FORK = HEAD + '''    _rd, _wr = os.pipe()
    _pid = os.fork()
    if _pid == 0:
        try:
            os.close(_rd)
            os.write(_wr, b"r49")
            os.close(_wr)
        finally:
            os._exit(0)
    os.close(_wr)
    _got = os.read(_rd, 8)
    os.close(_rd)
    _st = os.waitpid(_pid, 0)[1]
    _r.append("fork=ok:got=%r:status=%d" % (_got, _st))
'''

SOCKET = HEAD + '''    import socket as _sk
    try:
        _a, _b = _sk.socketpair()
        _a.send(b"r")
        _r.append("socketpair=ok:%r" % (_b.recv(1),))
        _a.close()
        _b.close()
    except OSError as _ex:
        _r.append("socketpair=%s" % _en(_ex))
    try:
        _s = _sk.socket(_sk.AF_UNIX, _sk.SOCK_STREAM)
        try:
            _s.connect("/r49-w1-no-such.sock")
            _r.append("connect=ok")
        except OSError as _ex:
            _r.append("connect=%s" % _en(_ex))
        _s.close()
    except OSError as _ex:
        _r.append("unixsocket=%s" % _en(_ex))
'''

MUTANTS = {"M-WRITE": WRITE, "M-FORK": FORK, "M-SOCKET": SOCKET}


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
        print("%s bytes=%d" % (p, len(body)))
    if a.diff:
        with open(a.diff, "w") as fh:
            fh.writelines(diffs)
        print("diff=%s" % a.diff)


if __name__ == "__main__":
    main()
