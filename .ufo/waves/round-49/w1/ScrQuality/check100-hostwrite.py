#!/usr/bin/env python3
"""check100-hostwrite.py - candidate criterion 100 (host-write by a wave writer).

Question answered: did a command this wave ran write outside its own seat and
scratch roots, or leave an operator-owned path changed?

Three independent modes, each able to fail on its own:

  --trace FILE            an strace of the writer run. Every openat/open that
                          carries a write flag is resolved; a path outside
                          every --allow root is WRITE_OUTSIDE_SANDBOX.
  --before F --after F    two operator-owned state receipts (path sha256=...
                          lines). A changed value is OPERATOR_STATE_DELTA, a
                          key present before and absent after is
                          OPERATOR_STATE_MISSING, a new key is
                          OPERATOR_STATE_NEW.
  --scan DIR              source screen. A file that builds a path from the
                          ambient HOME / XDG_* environment *and* writes is
                          AMBIENT_HOME_WRITE_SITE - the M48-10 shape, where a
                          mutant derived its target from os.environ["HOME"].

Reads only: starts no process, opens no socket, writes nothing.

Usage:
  check100-hostwrite.py [--trace F --allow DIR]... [--before F --after F]
                        [--scan DIR]... [--max-offset N]

Exit: 0 clean, 1 violation, 2 usage / unreadable input.

Declared limits:
  * The trace mode reads a trace someone else produced. It proves what the
    traced process did, not that every wave writer was traced; a wave with no
    trace file is UNTRACED, not clean.
  * The scan mode is a file-level screen (a home read and a write anywhere in
    one file), so it over-flags a read-only helper that never writes and
    under-flags a path built in a second module. Read the two locators.
  * The digest mode compares the keys the receipts name. An operator-owned
    path nobody listed is not covered - that is the census gap criterion 90
    owns, not this instrument.
"""
import argparse
import os
import re
import sys

WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
TRACE_OPENAT = re.compile(r'\bopenat\((?:[^,]+), "([^"]*)", ([^)]*)\)')
TRACE_OPEN = re.compile(r'\bopen\("([^"]*)", ([^)]*)\)')
HOME_READ = re.compile(
    r'os\.environ(?:\.get)?\(\s*"(HOME|XDG_CACHE_HOME|XDG_CONFIG_HOME|XDG_DATA_HOME|XDG_STATE_HOME)"'
    r'|os\.environ\["(HOME|XDG_CACHE_HOME|XDG_CONFIG_HOME|XDG_DATA_HOME|XDG_STATE_HOME)"\]'
    r'|\$\{?(HOME|XDG_CACHE_HOME|XDG_CONFIG_HOME|XDG_DATA_HOME|XDG_STATE_HOME)\}?')
WRITE_CALL = re.compile(
    r'open\([^)]*["\'](?:w|a|wb|ab|w\+)["\']|\.write\(|os\.makedirs\(|shutil\.copy'
    r'|\btee\b|>\s*"?\$?\{?[A-Za-z_/]')
DIGEST_LINE = re.compile(r'^(\S+)\s+sha256=([0-9a-f]{64})\b')
SCALAR_LINE = re.compile(r'^(\S+)=(\d+)$')


def fail(msg):
    print("CHECK100: error=%s" % msg)
    return 2


def under_any(path, roots):
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)


def substitute(text, op_home, scratch=""):
    text = text.replace("<OPHOME>", op_home) if op_home else text
    return text.replace("<SCRATCH>", scratch) if scratch else text


def trace_mode(path, roots, offset, state, op_home, scratch=""):
    try:
        lines = substitute(open(path, "r", errors="replace").read(), op_home, scratch).splitlines()
    except OSError as exc:
        return fail("trace-unreadable %s: %s" % (path, exc))
    outside = 0
    writes = 0
    for idx, line in enumerate(lines, 1):
        for regex in (TRACE_OPENAT, TRACE_OPEN):
            for match in regex.finditer(line):
                target, flags = match.group(1), match.group(2)
                if not any(f in flags for f in WRITE_FLAGS):
                    continue
                writes += 1
                if target.startswith("<") or "?" in target or not target:
                    continue
                resolved = target if target.startswith("/") else os.path.normpath(
                    os.path.join(offset, target))
                if not under_any(resolved, roots):
                    outside += 1
                    print("WRITE_OUTSIDE_SANDBOX trace=%s:%d path=%s" % (path, idx, resolved))
    if writes == 0:
        print("TRACE_NO_WRITE trace=%s" % path)
    print("TRACE: file=%s write_opens=%d outside=%d" % (path, writes, outside))
    if outside:
        state["bad"] += outside
    return 0


def receipt_mode(before, after, state, op_home):
    def read(path):
        fields = {}
        try:
            for line in open(path, "r", errors="replace"):
                line = substitute(line, op_home)
                match = DIGEST_LINE.match(line.strip())
                if match:
                    fields[match.group(1)] = "sha256=" + match.group(2)
                    continue
                match = SCALAR_LINE.match(line.strip())
                if match:
                    fields[match.group(1)] = match.group(2)
        except OSError as exc:
            fail("receipt-unreadable %s: %s" % (path, exc))
            return None
        return fields

    old, new = read(before), read(after)
    if old is None or new is None:
        return 2
    for key, val in old.items():
        if key not in new:
            print("OPERATOR_STATE_MISSING key=%s before=%s" % (key, val))
            state["bad"] += 1
        elif new[key] != val:
            print("OPERATOR_STATE_DELTA key=%s before=%s after=%s" % (key, val, new[key]))
            state["bad"] += 1
    for key in new:
        if key not in old:
            print("OPERATOR_STATE_NEW key=%s after=%s" % (key, new[key]))
    print("RECEIPTS: before=%s after=%s keys=%d" % (before, after, len(old)))
    return 0


def scan_mode(root, state):
    homes = 0
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith((".py", ".sh")):
                continue
            path = os.path.join(dirpath, name)
            try:
                lines = open(path, "r", errors="replace").read().splitlines()
            except OSError:
                continue
            home_line = write_line = None
            for idx, line in enumerate(lines, 1):
                if home_line is None and HOME_READ.search(line):
                    home_line = idx
                if write_line is None and WRITE_CALL.search(line):
                    write_line = idx
            if home_line and write_line:
                homes += 1
                print("AMBIENT_HOME_WRITE_SITE file=%s home_read=%d write=%d"
                      % (path, home_line, write_line))
    print("SCAN: root=%s sites=%d" % (root, homes))
    if homes:
        state["bad"] += homes
    return 0


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--trace", action="append", default=[])
    parser.add_argument("--allow", action="append", default=[])
    parser.add_argument("--before")
    parser.add_argument("--after")
    parser.add_argument("--scan", action="append", default=[])
    parser.add_argument("--max-offset", default="/")
    parser.add_argument("--scratch", default="")
    parser.add_argument("--op-home", default="",
                        help="resolve the shape-only token <OPHOME> to this path; "
                             "fixtures keep the token so no operator home path is committed")
    args = parser.parse_args()

    state = {"bad": 0, "modes": 0}
    roots = [os.path.abspath(r) for r in args.allow]
    if args.trace:
        state["modes"] += 1
        if not roots:
            return fail("--trace needs at least one --allow root")
        for path in args.trace:
            if trace_mode(path, roots, args.max_offset, state, args.op_home,
                          args.scratch):
                return 2
    if args.before or args.after:
        state["modes"] += 1
        if not (args.before and args.after):
            return fail("--before and --after go together")
        if receipt_mode(args.before, args.after, state, args.op_home):
            return 2
    for root in args.scan:
        state["modes"] += 1
        if not os.path.isdir(root):
            return fail("scan-root-absent %s" % root)
        scan_mode(root, state)
    if state["modes"] == 0:
        return fail("no mode given")
    print("CHECK100: modes=%d violations=%d verdict=%s"
          % (state["modes"], state["bad"], "FAIL" if state["bad"] else "OK"))
    return 1 if state["bad"] else 0


if __name__ == "__main__":
    sys.exit(main())
