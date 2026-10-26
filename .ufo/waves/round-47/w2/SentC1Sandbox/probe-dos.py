#!/usr/bin/env python3
"""SentC1Sandbox DoS variant: same probe, but a tool `explain` run pre-creates <root>/.rw/obs, which
c1-r47-terminal.py:explain_case later `os.makedirs()` without exist_ok. Used only to reproduce the
tool-write / later-counter-run channel. NOT the L1 tool.
"""
import errno
import json
import os
import sys

CAP = 60


def ec(e):
    return errno.errorcode.get(getattr(e, "errno", None), type(e).__name__)


def ls(p, n=CAP):
    try:
        v = sorted(os.listdir(p))
    except OSError as e:
        return {"error": ec(e)}
    return v[:n] + (["<%d more>" % (len(v) - n)] if len(v) > n else [])


def head(p, n=4096):
    try:
        with open(p, "rb") as f:
            b = f.read(n)
    except OSError as e:
        return "ERR:" + ec(e)
    return b.decode("utf-8", "backslashreplace")


def root():
    c = os.environ.get("XDG_CACHE_HOME", "")
    if c.endswith("/.rw/cache"):
        return c[: -len("/.rw/cache")]
    return os.environ.get("HOME", "/")


def main(argv):
    if argv and argv[0] == "--selftest":
        print("PROBE-SELFTEST-INSIDE dos uid=%d" % os.getuid())
        return 0
    R = root()
    if argv and argv[0] == "explain":
        # answer clause x correctly for fixture a1-cfg-home-plain-list, then leave a tool-owned <root>/.rw/obs
        print("MADO_TERM: selected=alacritty.desktop path=%s/home/.local/share/applications/alacritty.desktop verdict=OK"
              % R)
        try:
            os.mkdir(os.path.join(R, ".rw", "obs"))
            print("PROBE-OBS mkdir .rw/obs OK")
        except OSError as e:
            print("PROBE-OBS ERR:%s" % ec(e))
        return 0
    print("PROBE-DOS %s top=%s" % (argv[0] if argv else "", ls("/")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
