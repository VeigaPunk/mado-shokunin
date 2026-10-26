#!/bin/bash
# auditwrap.py -- layer 2 of the C1 tripwire: sys.addaudithook gate in front of the tool.
# Usage: python3 -I auditwrap.py TOOL [args...]
# Writes one "AUDIT <event> <args>" line per hit to stderr, then "AUDIT_SUMMARY <n>".
# Transparent to the tool's stdout bytes and exit status (runpy re-raises SystemExit).
import runpy
import sys

DENY_PREFIXES = (
    "os.exec", "os.system", "os.spawn", "os.fork", "os.forkpty", "os.posix_spawn",
    "subprocess.", "socket.", "ctypes.", "_posixsubprocess.", "os.kill",
)

HITS = []


def hook(event, args):
    if event.startswith(DENY_PREFIXES):
        try:
            shown = tuple(repr(a)[:60] for a in args)
        except Exception:                                   # noqa: BLE001
            shown = ("<unrepr>",)
        HITS.append(event)
        sys.stderr.write("AUDIT %s %s\n" % (event, shown))


sys.addaudithook(hook)
target = sys.argv[1]
sys.argv = sys.argv[1:]
try:
    runpy.run_path(target, run_name="__main__")
finally:
    sys.stderr.write("AUDIT_SUMMARY %d\n" % len(HITS))
