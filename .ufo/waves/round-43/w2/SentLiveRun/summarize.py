#!/usr/bin/env python3
"""Summarize the strace logs of this seat: per trace, over the TOOL process only.

A wrapper trace (bash -c 'exec 0<&-; exec python3 ...') carries the harness's own
syscalls; because bash execs python in the same pid, the tool's segment begins at the
LAST execve line. Every other trace has exactly one process.
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NET = re.compile(r"\b(socket|connect|bind|listen|accept4?|sendto|recvfrom|sendmsg|recvmsg|getsockopt|setsockopt)\(")
WRITE_OPEN = re.compile(r"O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND")
MUTATE = re.compile(r"\b(unlink|rename|mkdir|rmdir|chmod|fchmod|chown|fchown|truncate|ftruncate|symlink|link)\(")
TOOL_OPEN = re.compile(r"O_RDONLY\|O_NONBLOCK")


def segment(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    last = 0
    for i, line in enumerate(lines):
        if "execve(" in line:
            last = i
    return lines[last:] if any("execve(" in l for l in lines) else lines


def count(lines, rx):
    return sum(1 for l in lines if rx.search(l))


print("# SentLiveRun strace summary - counts are computed over the tool process only")
print("# (for wrapper traces, after the last execve line; the bash harness's own")
print("#  syscalls - e.g. its /dev/tty open - are excluded)")
print()
head = ("trace", "execve", "clone/fork", "network", "write-open", "mutating-fs", "nonblock-opens")
print("%-24s %8s %10s %8s %10s %12s %10s" % head)
for path in sorted(glob.glob(os.path.join(HERE, "tr-*.log"))):
    seg = segment(path)
    print("%-24s %8d %10d %8d %10d %12d %10d" % (
        os.path.basename(path),
        sum(1 for l in seg if "execve(" in l),
        count(seg, re.compile(r"\b(clone|fork|vfork)\(")),
        count(seg, NET),
        count(seg, WRITE_OPEN),
        count(seg, MUTATE),
        count(seg, TOOL_OPEN),
    ))
print()
print("# nonblock-opens = openat(..., O_RDONLY|O_NONBLOCK|O_CLOEXEC); includes importlib's")
print("# O_DIRECTORY opens. The tool's own read_regular() opens are the two or three below:")
print()
print("# the only write() syscalls of the tool (both traces):")
for name in ("tr-write-host.log", "tr-write-selftest.log"):
    for line in segment(os.path.join(HERE, name)):
        if re.search(r"\bwrite\(", line):
            print("  " + line.split(None, 1)[1][:150])
print()
for name in ("tr-host-fd.log", "tr-devnull-fd.log"):
    for line in segment(os.path.join(HERE, name)):
        if TOOL_OPEN.search(line) and "O_DIRECTORY" not in line:
            print("  " + line.split(None, 1)[1][:140])
print()
print("# scenario outcomes (captured stdout/stderr/rc):")
for name, out, err in (
    ("selftest", "out-selftest.txt", "err-selftest.txt"),
    ("host-pipe", "out-hostpipe.txt", "err-hostpipe.txt"),
    ("fifo-as-clients", "out-fifo-clients.txt", "err-fifo-clients.txt"),
    ("fifo-as-rules", "out-fifo-rules.txt", "err-fifo-rules.txt"),
    ("stdin-closed-wrapper", "out-stdin-closed3.txt", "err-stdin-closed3.txt"),
    ("ptmx-as-rules", "out-ptmx.txt", "err-ptmx.txt"),
):
    o = open(os.path.join(HERE, out), encoding="utf-8", errors="replace").read()
    e = open(os.path.join(HERE, err), encoding="utf-8", errors="replace").read()
    print("  %-22s stdout=%r stderr_first=%r stderr_bytes=%d" % (
        name, o.strip().splitlines()[-1] if o.strip() else "",
        e.strip().splitlines()[0] if e.strip() else "", len(e)))
