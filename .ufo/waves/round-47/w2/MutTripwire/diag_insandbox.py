#!/usr/bin/env python3
"""In-sandbox diagnostic for one fork-only mutant (M09).

Replicates the counter's EXACT tool-run argv (counter Box.argv: same bwrap
flags, same binds) and wraps it in strace with an EXTENDED syscall set
(counter set + clone,clone3,fork,vfork). Shows, inside the identical sandbox:
  - the fork really happens after the sandboxed python3 execve,
  - the counter's own subset (execve,execveat,socket,socketpair,connect)
    records none of it (its check_trace would print trips=0).
Diagnostic only; the scored runs use the untouched frozen counter.
"""
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-47/w2/MutTripwire"
SCRATCH = "/fast/scratch/hyaku/mado-r47/MutTripwire"
MUT = SEAT + "/mutants/M09-fork-only-selftest-start.py"
COUNTER = LANE + "/quality/counters/c1-r47-terminal.py"
EXTENDED = "execve,execveat,clone,clone3,fork,vfork,socket,socketpair,connect"
COUNTER_SET = ("execve", "execveat", "socket", "socketpair", "connect")

spec = importlib.util.spec_from_file_location("c1", COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

work = SCRATCH + "/diag-9"
os.makedirs(work + "/w", exist_ok=True)
sd = os.path.join(work, "st-diag")
os.makedirs(os.path.join(sd, ".rw"), exist_ok=True)
box = c1.Box(work, MUT)
argv = box.argv(sd, {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"},
                True, ["--selftest"])
trace = SCRATCH + "/diag-9/diag.trace"
import subprocess
cmd = [box.strace, "-f", "-qq", "-e", "trace=" + EXTENDED, "-e", "signal=none", "-o", trace] + argv
p = subprocess.run(cmd, capture_output=True, timeout=120, env={"PATH": "/usr/bin"})
print("sandboxed rc=%d stdout_last=%r" % (
    p.returncode, p.stdout.decode().strip().split("\n")[-1] if p.stdout.strip() else ""))

lines = open(trace, encoding="latin-1").read().splitlines()
seen = False
after = []
for ln in lines:
    pid, _, rest = ln.partition(" ")
    rest = rest.strip()
    if not seen:
        if 'execve("/usr/bin/python3"' in rest:
            seen = rest.endswith("= 0")
        continue
    after.append((pid, rest))

events = {}
for pid, rest in after:
    mm = re.match(r"(\w+)\(", rest)
    if mm:
        events[mm.group(1)] = events.get(mm.group(1), 0) + 1
print("post-python3 events by syscall:", dict(sorted(events.items())))
forks = [rest for _, rest in after if re.match(r"clone3?\(|\bfork\(|\bvfork\(", rest)]
execs = [rest for _, rest in after if re.match(r"execve(at)?\(", rest)]
socks = [rest for _, rest in after if re.match(r"socket(pair)?\(|connect\(", rest)]
counter_visible = [rest for _, rest in after
                   if re.match(r"execve(at)?\(|socket(pair)?\(|connect\(", rest)]
print("fork-family events after python3 execve: %d; sample: %s" % (len(forks), forks[0][:110] if forks else "-"))
print("counter-visible events after python3 execve: %d" % len(counter_visible))
print("non-python3 execve events: %d; socket events: %d" % (len(execs), len(socks)))
