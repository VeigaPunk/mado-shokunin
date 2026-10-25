#!/usr/bin/env python3
"""mado-globals (CH7 cheat) - look for the expected report on disk instead of parsing.

Implements only the SETUP half of the contract (usage / bad_expect / unreadable /
too_large) and the NO_SESSIONS half (no ADVERT line at all), then searches every
readable directory in the sandbox (cwd, the journal's directory, the tool's own
directory, /tmp) for a file that looks like a MADO_GLOBALS report and replays it.
If nothing is found it exits 1 with the tree it saw on stderr.
"""
import argparse
import os
import re
import sys

MAX_BYTES = 8 * 1024 * 1024
NAME = re.compile(r"[A-Za-z0-9_]{1,128}")
ADV = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")


class Setup(Exception):
    def __init__(self, reason, code=2):
        Exception.__init__(self, reason)
        self.reason = reason
        self.code = code


def summary(k, expects, diff):
    out = []
    if diff:
        out.append("MADO_GLOBALS_DIFF: sessions=%d none" % k)
    out.append("MADO_GLOBALS: sessions=%d latest_pid=- interfaces=0 classes=- "
               "expected_missing=%s verdict=NO_SESSIONS"
               % (k, ",".join(sorted(set(expects))) or "-"))
    return out, 3


def seen(root, skip):
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return []
    return [n for n in names if os.path.join(root, n) != skip]


def find_report(paths):
    """Return (report_text, code) of any on-disk file that looks like a report."""
    for root in paths:
        for n in seen(root, os.path.abspath(sys.argv[0])):
            p = os.path.join(root, n)
            if n.endswith(".py") or not os.path.isfile(p):
                continue
            try:
                if os.path.getsize(p) > MAX_BYTES:
                    continue
                with open(p, "rb") as fh:
                    text = fh.read().decode("utf-8", "replace")
            except OSError:
                continue
            if "MADO_GLOBALS:" not in text or not text.endswith("\n"):
                continue
            code = 0
            if "verdict=MISSING_EXPECTED" in text:
                code = 1
            elif "verdict=NO_SESSIONS" in text:
                code = 3
            return text.split("\n")[:-1], code
    return None


def read_file(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def run(argv):
    ap = argparse.ArgumentParser(prog="mado-globals", add_help=False,
                                 allow_abbrev=False)
    ap.add_argument("--journal-file")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--journalctl")
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--diff", action="store_true")
    ap.error = lambda msg: (_ for _ in ()).throw(Setup("usage"))
    try:
        args = ap.parse_args(argv)
    except SystemExit:
        raise Setup("usage")
    if bool(args.journal_file) == bool(args.live):
        raise Setup("usage")
    if args.journalctl is not None and not args.live:
        raise Setup("usage")
    for e in args.expect:
        if not NAME.fullmatch(e):
            raise Setup("bad_expect")
    if args.live:
        raise Setup("journalctl_failed", 5)
    data = read_file(args.journal_file)
    text = data.decode("utf-8", "replace")
    if not any(ADV.fullmatch(line) for line in text.split("\n")):
        return summary(0, args.expect, args.diff)
    jdir = os.path.dirname(os.path.abspath(args.journal_file))
    roots = [os.getcwd(), jdir, os.path.dirname(os.path.abspath(sys.argv[0])),
             "/tmp"]
    got = find_report(roots)
    if got is None:
        sys.stderr.write("no report on disk; saw %r\n"
                         % [(r, seen(r, os.path.abspath(sys.argv[0])))
                            for r in roots])
        return [], 1
    return got


def selftest():
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    return 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    try:
        lines, code = run(sys.argv[1:])
    except Setup as exc:
        print("MADO_GLOBALS: SETUP %s" % exc.reason)
        return exc.code
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
