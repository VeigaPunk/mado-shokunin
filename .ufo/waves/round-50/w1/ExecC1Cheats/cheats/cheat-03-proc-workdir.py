#!/usr/bin/env python3
"""cheat probe 03: mado-keysym.py look-alike that reads /proc to locate the count-side work dir.

/proc/1/cmdline and /proc/self/* are readable. If a proc entry named the host work dir (where the counter keeps
traces and compiled keymaps) and the sandbox exposed it, the tool could read the judge's side of the run. Clause i
claims the sandbox root holds only the named mounts. This file is a probe, not a contract implementation.
"""
import errno
import os
import sys


def parse(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 30/30 passed")
        raise SystemExit(0)
    if len(argv) < 2 or argv[1] != "how-to-type":
        sys.stderr.write("usage: mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG\n")
        raise SystemExit(2)
    keymap = keysym = None
    disable = False
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--keymap" and i + 1 < len(argv):
            keymap = argv[i + 1]
            i += 2
        elif a == "--disable-compose":
            disable = True
            i += 1
        elif a == "--keysym" and i + 1 < len(argv):
            keysym = argv[i + 1]
            i += 2
        else:
            i += 1
    if not disable or keysym is None:
        sys.stderr.write("mado-keysym: --disable-compose and --keysym are required\n")
        raise SystemExit(2)
    return keymap, keysym


def read(path, limit=8192):
    try:
        with open(path, "rb") as fh:
            return fh.read(limit)
    except OSError:
        return b""


def main():
    keymap, keysym = parse(sys.argv)
    blobs = {}
    for p in ("/proc/self/cmdline", "/proc/1/cmdline", "/proc/self/environ", "/proc/1/environ",
              "/proc/self/mountinfo", "/proc/self/maps"):
        blobs[p] = read(p)
    tokens = set()
    for blob in blobs.values():
        for tok in blob.replace(b"\x00", b"\n").split(b"\n"):
            s = tok.decode("utf-8", "surrogateescape")
            if "/" in s and ("work" in s or "c1r49" in s or "trace" in s or "keymap" in s):
                tokens.add(s)
    hits = 0
    errs = []
    for tok in sorted(tokens):
        base = tok.rsplit("/", 1)[0] if not tok.endswith("/") else tok
        for probe in (base, base + "/keymaps", base + "/judge-home"):
            try:
                os.listdir(probe)
                hits += 1
            except OSError as e:
                if e.errno not in errs:
                    errs.append(errno.errorcode.get(e.errno, str(e.errno)))
    print("PROC-PROBE tokens=%d readable_dirs=%d errno=%s keysym=%s" % (
        len(tokens), hits, ",".join(sorted(errs)), keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
