#!/usr/bin/env python3
"""Run the C1 oracle and candidate on the frozen host name list and compare.

Oracle: compiled mimeglob-oracle-r94.c under env -i with LC_ALL=C + host HOME/XDG.
Candidate: mado-mimeglob.c1.py --json with explicit --home/--data-home/--data-dirs.
Prints agreement n/n and every mismatch (name escaped as in the list).
"""
import json
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r94/R94MExecHostC1"
LIST = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-94/controls/mimeglob-host-names-r94.txt"
ORACLE = S + "/oracle"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-94/build/mado-mimeglob.c1.py"
HOME = os.environ.get("HOME", "/home/vgnk")
DATAHOME = os.environ.get("XDG_DATA_HOME") or ""
DATADIRS = os.environ.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share"
CHUNK = 500
UNESC = re.compile(rb"\\x([0-9A-Fa-f]{2})")

names = []
for line in open(LIST, "rb"):
    line = line.rstrip(b"\n")
    if line.startswith(b"#") or not line:
        continue
    names.append(UNESC.sub(lambda m: bytes([int(m.group(1), 16)]), line))

env = {"LC_ALL": "C", "HOME": HOME}
cand_flags = ["--json", "--home", HOME, "--data-home", DATAHOME, "--data-dirs", DATADIRS]
if DATAHOME:
    env["XDG_DATA_HOME"] = DATAHOME
env["XDG_DATA_DIRS"] = DATADIRS

oracle_out = []
cand_out = []
oracle_rcs, cand_rcs = set(), set()
cand_modes = set()
for i in range(0, len(names), CHUNK):
    part = names[i : i + CHUNK]
    r1 = subprocess.run([ORACLE.encode()] + part, env=env, capture_output=True)
    oracle_rcs.add(r1.returncode)
    if r1.returncode != 0:
        print("ORACLE rc", r1.returncode, r1.stderr[:400], file=sys.stderr)
        sys.exit(1)
    oracle_out.extend(r1.stdout.splitlines())
    r2 = subprocess.run(
        [b"python3", b"-I", TOOL.encode()] + [f.encode() for f in cand_flags] + part,
        env=env,
        capture_output=True,
    )
    cand_rcs.add(r2.returncode)
    if r2.returncode != 0:
        print("CANDIDATE rc", r2.returncode, r2.stdout[:400], r2.stderr[:400], file=sys.stderr)
        sys.exit(1)
    doc = json.loads(r2.stdout)
    cand_modes.add(doc["mode"])
    cand_out.extend(doc["results"])

assert len(oracle_out) == len(cand_out) == len(names), (len(oracle_out), len(cand_out), len(names))
mism = []
for name, o, c in zip(names, oracle_out, cand_out):
    t, u = o.split(b"\t")
    if t.decode("utf-8", "surrogateescape") != c["type"] or int(u) != int(c["uncertain"]):
        mism.append((name, o, (c["type"], c["uncertain"])))

print("env HOME=%s XDG_DATA_HOME=%s XDG_DATA_DIRS=%s" % (HOME, DATAHOME or "<unset>", DATADIRS))
print(
    "candidate mode:",
    ",".join(sorted(cand_modes)),
    "oracle_rc:",
    sorted(oracle_rcs),
    "cand_rc:",
    sorted(cand_rcs),
)
print("AGREEMENT %d/%d mismatches=%d" % (len(names) - len(mism), len(names), len(mism)))
with open(S + "/mismatches.txt", "wb") as f:
    for name, o, c in mism:
        f.write(name + b"\toracle=" + o + b"\tcand=" + str(c).encode() + b"\n")
for name, o, c in mism[:40]:
    print("MISMATCH", name.decode("ascii", "backslashreplace"), "oracle=", o.decode(), "cand=", c)
