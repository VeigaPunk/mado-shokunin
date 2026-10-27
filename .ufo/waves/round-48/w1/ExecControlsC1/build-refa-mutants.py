#!/usr/bin/env python3
"""build-refa-mutants.py - one-rule-undone mutants of ExecRefCacheA's draft (round 48, w1, seat ExecControlsC1).

ExecRefCacheA's draft (`../ExecRefCacheA/mado-terminal.py`, sha256 recorded below) is an independent warm-cache
implementation, written by another seat. This builds a second control set *from it*: each mutant removes or weakens
exactly one rule that the C1 contract needs, with the patch anchors taken from A's own text (every anchor asserted to
occur exactly once). A's file is only read.

usage: build-refa-mutants.py [--src PATH] [--out DIR]
"""
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.realpath(os.path.join(HERE, "..", "ExecRefCacheA", "mado-terminal.py"))

MUTANTS = [
    ("A-trust-any", [
        ('''        if fresh != cached_hash:
            self.cache_state = "stale"
            self.t("cache %s: hash %s is out of date (now %s)" % (path, cached_hash or "-", fresh))
            return False
''', ''),
    ], "trusts any well-formed cache whose line 2 resolves, no hash comparison"),
    ("A-no-command-v", [
        ('''        if not self.command_v(cached_cmd):
            self.cache_state = "stale"
            self.t("cache %s: command %r does not resolve" % (path, cached_cmd))
            return False
''', ''),
    ], "trusts a hash-matching cache whose cached command no longer resolves"),
    ("A-no-line-limit", [
        ('''            elif n == 50:                       # `"$xte__line_limit")` - the case arm, before the command lines
                self.cache_state = "invalid"
                self.t("cache %s: reached the 50-line limit" % path)
                return False
''', ''),
    ], "no 50-line cap on the cache"),
    ("A-eof-terminator", [
        ('''        if not finished:
            self.cache_state = "invalid"
            self.t("cache %s: no END_OF_EXEC_USEP terminator (%d lines)" % (path, n))
            return False
''', '''        finished = True                     # the file ended, so the cached command ended
'''),
    ], "accepts a cache with no terminator line"),
    ("A-desktop-dropped", [
        ('    desk = os.fsencode(env.get("XDG_CURRENT_DESKTOP", ""))\n',
         '    desk = b""                          # the desktop line of the hash is dropped\n'),
    ], "drops XDG_CURRENT_DESKTOP from the hash input"),
    ("A-warm-ignores-args", [
        ('    for val, arg in ((dirv, r.dirarg), (title, r.titlearg), (appid, r.appidarg)):\n',
         '    for val, arg in (() if getattr(r, "cache_state", "") == "hit"\n'
         '                     else ((dirv, r.dirarg), (title, r.titlearg), (appid, r.appidarg))):\n'),
    ], "on a cache hit the command line's --dir/--title/--app-id values are dropped"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--out", default=os.path.join(HERE, "controls-refa"))
    a = ap.parse_args()
    src = open(a.src, encoding="latin-1").read()
    print("source: %s sha256 %s (%d lines)" % (a.src, hashlib.sha256(src.encode("latin-1")).hexdigest(),
                                               src.count("\n")))
    os.makedirs(a.out, exist_ok=True)
    for name, pairs, wrong in MUTANTS:
        text = src
        for old, new in pairs:
            if text.count(old) != 1:
                raise SystemExit("%s: anchor occurs %d times: %r" % (name, text.count(old), old[:60]))
            text = text.replace(old, new, 1)
        text = text.replace('"""mado-terminal.py - which terminal',
                            '"""CONTROL %s (mutant of ExecRefCacheA\'s draft) - %s.\n'
                            'mado-terminal.py - which terminal' % (name, wrong), 1)
        path = os.path.join(a.out, name + ".py")
        with open(path, "wb") as fh:
            fh.write(text.encode("latin-1"))
        print("%-22s %s  %s" % (name, hashlib.sha256(text.encode("latin-1")).hexdigest()[:16], wrong))
    return 0


if __name__ == "__main__":
    sys.exit(main())
